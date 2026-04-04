"""Adversarial tests for the proving-slice contract path.

These tests attempt to bypass, forge, or mutate artifacts in ways that
should be caught by forge-contract-core validation. Each test documents
an attack vector and the expected defence.

All attacks are caught before any database write — the validator is the
single enforcement boundary shared by all participating repos.
"""

from __future__ import annotations

import pytest

from forge_contract_core.identity import compute_idempotency_key
from forge_contract_core.validators.artifact import ArtifactValidationError, validate_artifact
from forge_contract_core.validators.role_matrix import (
    RoleMatrixViolationError,
    check_producer_admitted,
)

# ── Shared helpers ────────────────────────────────────────────────────────────

_ROOT_ID = "adv00000-0000-0000-0000-000000000000"
_ARTIFACT_ID = "adv00000-0001-0001-0001-000000000001"


def _base_finding() -> dict:
    """Return a structurally valid finding with a correct idempotency key."""
    return {
        "artifact_id": _ARTIFACT_ID,
        "artifact_family": "source_drift_finding",
        "artifact_version": 1,
        "produced_by_system": "dataforge-Local",
        "produced_by_component": "drift_detector.schema_checker",
        "source_scope": "local",
        "lineage_root_id": _ROOT_ID,
        "parent_artifact_id": None,
        "trace_id": "trace-adversarial-0001",
        "idempotency_key": compute_idempotency_key(
            "source_drift_finding", _ARTIFACT_ID, 1, _ROOT_ID
        ),
        "created_at": "2026-04-04T10:00:00Z",
        "recorded_at": "2026-04-04T10:00:01Z",
        "sensitivity_class": "internal",
        "visibility_class": "operator",
        "promotion_class": "promotable",
        "validation_status": "valid",
        "signer_identity": "dataforge-Local/drift_detector@proving-slice-v1",
        "signature": "sha256:adversarial-sig-placeholder",
        "payload": {
            "system_id": "dataforge-Local",
            "drift_class": "schema_drift",
            "declared_truth_ref": f"source_drift_finding:{_ARTIFACT_ID}:v1",
            "observed_truth_ref": "runtime_state:dataforge-Local:2026-04-04T10:00:00Z",
            "impact_scope": "service",
            "confidence": "high",
            "operator_summary": "Adversarial test finding.",
            "evidence_refs": ["run_evidence:00000000-0000-0000-0000-000000000001:v1"],
            "affected_components": ["schema_registry"],
            "detection_source": "schema_checker_v1",
        },
    }


# ── Attack 1: Tampered idempotency key ────────────────────────────────────────

def test_adversarial_tampered_idempotency_key_is_caught():
    """An attacker replaces the correct idempotency key with an all-zero key.
    Strict validation must detect the mismatch and reject the artifact.

    Defence: validate_artifact(strict_idempotency=True) recomputes the key
    from (family, artifact_id, version, lineage_root_id) and compares.
    """
    artifact = _base_finding()
    artifact["idempotency_key"] = "0" * 64  # tampered

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=True)

    assert exc_info.value.cause == "invalid_idempotency_key"


# ── Attack 2: Cross-family key smuggling ─────────────────────────────────────

def test_adversarial_cross_family_key_does_not_verify():
    """An attacker reuses a valid key computed for family A to submit it as
    part of a family B artifact. The key is structurally valid (64-char hex)
    but does not match the B identity.

    Defence: strict idempotency recomputation binds the key to the declared
    (family, id, version, lineage_root_id) — a key for family A cannot pass
    for family B.
    """
    finding_key = compute_idempotency_key(
        "source_drift_finding", _ARTIFACT_ID, 1, _ROOT_ID
    )
    envelope_key = compute_idempotency_key(
        "promotion_envelope", _ARTIFACT_ID, 1, _ROOT_ID
    )

    # A valid key for source_drift_finding must NOT equal a key for promotion_envelope
    # with the same artifact_id (the family component differs in the hash input).
    assert finding_key != envelope_key


# ── Attack 3: Forbidden family injection ─────────────────────────────────────

def test_adversarial_forbidden_family_is_blocked():
    """An attacker attempts to inject an artifact with a family outside the
    proving-slice-01 admitted set (e.g. approval_artifact).

    Defence: validate_artifact raises ArtifactValidationError(cause="unsupported_family")
    before any payload validation or database write.
    """
    artifact = _base_finding()
    artifact["artifact_family"] = "approval_artifact"

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    assert exc_info.value.cause == "unsupported_family"


@pytest.mark.parametrize("family", [
    "rollback_artifact",
    "execution_directive",
    "contradiction_report",
    "calibration_record",
    "",
    "source_drift_finding; DROP TABLE ps_local_artifacts; --",
])
def test_adversarial_unadmitted_family_variants_are_blocked(family: str):
    """All variants of unadmitted families — including SQL injection attempts —
    are rejected by the unsupported-family check before any downstream processing.
    """
    artifact = _base_finding()
    artifact["artifact_family"] = family

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    # SQL injection strings and empty strings fail at envelope level (pattern check)
    # or family level (admitted set check) — either way they are rejected
    assert exc_info.value.cause in ("unsupported_family", "invalid_envelope")


# ── Attack 4: Version forgery (underflow) ────────────────────────────────────

def test_adversarial_version_zero_is_rejected():
    """An attacker submits version=0 to bypass version-specific validation.

    Defence: version 0 is not in ADMITTED_VERSIONS for any family.
    """
    artifact = _base_finding()
    artifact["artifact_version"] = 0
    # Recompute key for the forged version
    artifact["idempotency_key"] = compute_idempotency_key(
        "source_drift_finding", _ARTIFACT_ID, 0, _ROOT_ID
    )

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=True)

    # Envelope schema requires artifact_version >= 1; caught at envelope level
    assert exc_info.value.cause in ("unsupported_version", "invalid_envelope")


# ── Attack 5: Version forgery (overflow) ─────────────────────────────────────

def test_adversarial_future_version_is_rejected():
    """An attacker submits version=999 to target a schema slot that doesn't
    yet exist, potentially bypassing payload validation.

    Defence: validate_family_payload raises UnsupportedVersionError for any
    version not in ADMITTED_VERSIONS.
    """
    artifact = _base_finding()
    artifact["artifact_version"] = 999
    artifact["idempotency_key"] = compute_idempotency_key(
        "source_drift_finding", _ARTIFACT_ID, 999, _ROOT_ID
    )

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=True)

    assert exc_info.value.cause == "unsupported_version"


# ── Attack 6: Unadmitted producer ────────────────────────────────────────────

@pytest.mark.parametrize("bad_producer", [
    "forgeHQ",
    "unknown-service",
    "DataForge",  # Cloud DataForge is not admitted to produce source_drift_finding
    "",
    "dataforge-local",  # wrong capitalisation
])
def test_adversarial_unadmitted_producers_fail_role_matrix(bad_producer: str):
    """Only admitted producers may emit artifacts for a given family.
    The role matrix check provides a defence-in-depth boundary beyond schema.

    Defence: check_producer_admitted raises RoleMatrixViolationError for
    any producer not explicitly listed for the family in the role matrix registry.
    """
    with pytest.raises(RoleMatrixViolationError):
        check_producer_admitted(bad_producer, "source_drift_finding")


# ── Attack 7: Empty payload bypass ───────────────────────────────────────────

def test_adversarial_empty_payload_is_rejected():
    """An attacker submits a completely empty payload dict to bypass payload
    validation (e.g. to insert a row with no meaningful content).

    Defence: family schema requires multiple fields; an empty payload fails
    family payload validation with cause=invalid_payload.
    """
    artifact = _base_finding()
    artifact["payload"] = {}

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    assert exc_info.value.cause == "invalid_payload"


# ── Attack 8: Null payload fields ────────────────────────────────────────────

def test_adversarial_null_required_payload_fields_are_rejected():
    """An attacker sets required payload fields to null (JSON null) in an
    attempt to pass schema required-field checks while injecting empty data.

    Defence: family schemas declare required fields as specific types (e.g. string);
    null values fail type validation → cause=invalid_payload.
    """
    artifact = _base_finding()
    artifact["payload"]["operator_summary"] = None  # required string field nulled

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    assert exc_info.value.cause == "invalid_payload"
