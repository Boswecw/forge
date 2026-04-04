"""Scenario tests for the proving-slice contract path.

These are end-to-end contract-level tests. They validate the full
proving-slice path — from artifact emission through intake validation
to receipt verification — using only the forge-contract-core library.
No live database is required.

7 scenarios:
  1. Happy path: valid source_drift_finding passes strict validation
  2. Family gate: unsupported family raises at the family boundary
  3. Contract core rejects invalid payload (missing required field)
  4. Idempotency deduplication boundary: same identity → same key
  5. Promotion receipt structure: cloud receipt is a valid artifact
  6. Lineage chain integrity: finding → envelope → receipt share lineage
  7. Admission evidence: promotion_class field carries admission semantics
"""

from __future__ import annotations

import pytest

from forge_contract_core.identity import compute_idempotency_key
from forge_contract_core.validators.artifact import ArtifactValidationError, validate_artifact
from forge_contract_core.validators.families import UnsupportedFamilyError

# ── Shared artifact builders ──────────────────────────────────────────────────

_ROOT_ID = "d4e5f6a7-0004-0004-0004-000000000004"
_FINDING_ID = "d4e5f6a7-0004-0004-0004-000000000004"
_ENVELOPE_ID = "e5f6a7b8-0005-0005-0005-000000000005"
_RECEIPT_ID = "f6a7b8c9-0006-0006-0006-000000000006"


def _finding_artifact(
    *,
    artifact_id: str = _FINDING_ID,
    lineage_root_id: str = _ROOT_ID,
    promotion_class: str = "promotable",
    payload_override: dict | None = None,
) -> dict:
    """Build a minimal valid source_drift_finding artifact with a computed idempotency key."""
    payload = {
        "system_id": "dataforge-Local",
        "drift_class": "schema_drift",
        "declared_truth_ref": f"source_drift_finding:{artifact_id}:v1",
        "observed_truth_ref": "runtime_state:dataforge-Local:2026-04-04T10:00:00Z",
        "impact_scope": "service",
        "confidence": "high",
        "operator_summary": "Schema drift detected.",
        "evidence_refs": ["run_evidence:00000000-0000-0000-0000-000000000001:v1"],
        "affected_components": ["schema_registry"],
        "detection_source": "schema_checker_v1",
    }
    if payload_override:
        payload.update(payload_override)

    return {
        "artifact_id": artifact_id,
        "artifact_family": "source_drift_finding",
        "artifact_version": 1,
        "produced_by_system": "dataforge-Local",
        "produced_by_component": "drift_detector.schema_checker",
        "source_scope": "local",
        "lineage_root_id": lineage_root_id,
        "parent_artifact_id": None,
        "trace_id": "trace-scenario-0001",
        "idempotency_key": compute_idempotency_key(
            "source_drift_finding", artifact_id, 1, lineage_root_id
        ),
        "created_at": "2026-04-04T10:00:00Z",
        "recorded_at": "2026-04-04T10:00:01Z",
        "sensitivity_class": "internal",
        "visibility_class": "operator",
        "promotion_class": promotion_class,
        "validation_status": "valid",
        "signer_identity": "dataforge-Local/drift_detector@proving-slice-v1",
        "signature": "sha256:scenario-sig-placeholder-0001",
        "payload": payload,
    }


def _promotion_envelope_artifact(
    *,
    artifact_id: str = _ENVELOPE_ID,
    finding_id: str = _FINDING_ID,
    lineage_root_id: str = _ROOT_ID,
    policy_check_result: str = "passed",
    promotion_class: str = "promotable",
) -> dict:
    return {
        "artifact_id": artifact_id,
        "artifact_family": "promotion_envelope",
        "artifact_version": 1,
        "produced_by_system": "dataforge-Local",
        "produced_by_component": "promotion_queue_service",
        "source_scope": "local",
        "lineage_root_id": lineage_root_id,
        "parent_artifact_id": finding_id,
        "trace_id": "trace-scenario-0002",
        "idempotency_key": compute_idempotency_key(
            "promotion_envelope", artifact_id, 1, lineage_root_id
        ),
        "created_at": "2026-04-04T10:01:00Z",
        "recorded_at": "2026-04-04T10:01:01Z",
        "sensitivity_class": "internal",
        "visibility_class": "internal",
        "promotion_class": promotion_class,
        "validation_status": "valid",
        "signer_identity": "dataforge-Local/promotion_queue_service@proving-slice-v1",
        "signature": "sha256:scenario-sig-placeholder-0002",
        "payload": {
            "promoted_artifact_ref": f"source_drift_finding:{finding_id}:v1",
            "promotion_reason": "Drift finding meets promotion admission criteria.",
            "redaction_class": "none",
            "policy_check_result": policy_check_result,
            "promotion_batch_id": lineage_root_id,
            "policy_check_detail": "All admission checks passed.",
        },
    }


def _promotion_receipt_artifact(
    *,
    artifact_id: str = _RECEIPT_ID,
    finding_id: str = _FINDING_ID,
    lineage_root_id: str = _ROOT_ID,
    intake_outcome: str = "accepted",
) -> dict:
    return {
        "artifact_id": artifact_id,
        "artifact_family": "promotion_receipt",
        "artifact_version": 1,
        "produced_by_system": "DataForge",
        "produced_by_component": "proving_slice_intake",
        "source_scope": "shared",
        "lineage_root_id": lineage_root_id,
        "parent_artifact_id": finding_id,
        "trace_id": "trace-scenario-0003",
        "idempotency_key": compute_idempotency_key(
            "promotion_receipt", artifact_id, 1, lineage_root_id
        ),
        "created_at": "2026-04-04T10:02:00Z",
        "recorded_at": "2026-04-04T10:02:01Z",
        "sensitivity_class": "internal",
        "visibility_class": "operator",
        "promotion_class": "local_only",
        "validation_status": "valid",
        "signer_identity": "DataForge/proving_slice_intake@proving-slice-v1",
        "signature": "sha256:scenario-sig-placeholder-0003",
        "payload": {
            "receipt_id": artifact_id,
            "related_artifact_ref": f"source_drift_finding:{finding_id}:v1",
            "intake_outcome": intake_outcome,
            "shared_record_ref": f"source_drift_finding:{finding_id}:v1:shared" if intake_outcome == "accepted" else None,
            "received_at": "2026-04-04T10:02:00Z",
            "idempotency_key": compute_idempotency_key(
                "source_drift_finding", finding_id, 1, lineage_root_id
            ),
            "outcome_summary": "Artifact accepted and recorded as shared truth.",
            "rejection_class": None,
            "retry_allowed": False,
            "producer_identity": "dataforge-Local",
        },
    }


# ── Scenario 1: Happy path ────────────────────────────────────────────────────

def test_scenario_1_happy_path_source_drift_finding_passes_strict_validation():
    """A correctly formed source_drift_finding with a computed idempotency key
    passes strict validation end-to-end — the exact path that DataForge Cloud
    intake uses via validate_artifact(artifact, strict_idempotency=True).
    """
    artifact = _finding_artifact()
    validate_artifact(artifact, strict_idempotency=True)  # must not raise


# ── Scenario 2: Family gate ───────────────────────────────────────────────────

def test_scenario_2_family_gate_rejects_unadmitted_family():
    """An artifact claiming an unadmitted family is stopped at the family gate.
    This is the first line of defence in both DataForge Local admission and
    DataForge Cloud intake.
    """
    artifact = _finding_artifact()
    artifact["artifact_family"] = "approval_artifact"

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    assert exc_info.value.cause == "unsupported_family"


# ── Scenario 3: Contract core rejects invalid payload ────────────────────────

def test_scenario_3_missing_required_payload_field_is_rejected():
    """A source_drift_finding with a missing required payload field fails with
    cause=invalid_payload. This is the rejection path in DataForge Cloud intake
    that triggers a rejected promotion_receipt.
    """
    artifact = _finding_artifact(payload_override={"drift_class": None})
    # Remove a required field entirely
    del artifact["payload"]["operator_summary"]

    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)

    assert exc_info.value.cause == "invalid_payload"


# ── Scenario 4: Idempotency deduplication boundary ───────────────────────────

def test_scenario_4_same_artifact_identity_produces_same_idempotency_key():
    """The idempotency key algorithm is deterministic. Two calls with identical
    (family, artifact_id, version, lineage_root_id) always produce the same key.
    This is the deduplication boundary used by both DataForge Local
    (UNIQUE constraint on ps_local_artifacts) and DataForge Cloud
    (UNIQUE constraint on ps_cloud_intake_records).
    """
    key_a = compute_idempotency_key("source_drift_finding", _FINDING_ID, 1, _ROOT_ID)
    key_b = compute_idempotency_key("source_drift_finding", _FINDING_ID, 1, _ROOT_ID)

    assert key_a == key_b
    assert len(key_a) == 64


def test_scenario_4b_different_artifact_id_produces_different_key():
    """A different artifact_id yields a different idempotency key — ruling out
    collision between distinct artifacts in the same lineage.
    """
    alt_id = "aaaaaaaa-0000-0000-0000-000000000099"
    key_original = compute_idempotency_key("source_drift_finding", _FINDING_ID, 1, _ROOT_ID)
    key_alt = compute_idempotency_key("source_drift_finding", alt_id, 1, _ROOT_ID)

    assert key_original != key_alt


# ── Scenario 5: Promotion receipt structure ───────────────────────────────────

def test_scenario_5_accepted_promotion_receipt_is_valid():
    """A promotion_receipt artifact emitted by DataForge Cloud for an accepted
    intake passes full contract validation. DataForge Local consumes these
    receipts and validates them via validate_artifact() on receipt.
    """
    receipt = _promotion_receipt_artifact(intake_outcome="accepted")
    validate_artifact(receipt, strict_idempotency=True)  # must not raise


def test_scenario_5b_rejected_promotion_receipt_is_valid():
    """A rejected promotion_receipt is also a valid artifact — the contract
    only constrains structure, not outcome semantics.
    """
    receipt = _promotion_receipt_artifact(intake_outcome="rejected")
    validate_artifact(receipt, strict_idempotency=True)


# ── Scenario 6: Lineage chain integrity ───────────────────────────────────────

def test_scenario_6_lineage_chain_shares_root():
    """source_drift_finding → promotion_envelope → promotion_receipt form a
    valid lineage chain: all three artifacts share the same lineage_root_id,
    and each links its parent via parent_artifact_id.
    """
    finding = _finding_artifact(artifact_id=_FINDING_ID, lineage_root_id=_ROOT_ID)
    envelope = _promotion_envelope_artifact(
        finding_id=_FINDING_ID, lineage_root_id=_ROOT_ID
    )
    receipt = _promotion_receipt_artifact(
        finding_id=_FINDING_ID, lineage_root_id=_ROOT_ID
    )

    # All share the same lineage root
    assert finding["lineage_root_id"] == _ROOT_ID
    assert envelope["lineage_root_id"] == _ROOT_ID
    assert receipt["lineage_root_id"] == _ROOT_ID

    # Envelope's parent is the finding
    assert envelope["parent_artifact_id"] == _FINDING_ID

    # Receipt's parent is the finding (direct receipt of the finding)
    assert receipt["parent_artifact_id"] == _FINDING_ID

    # All three are individually valid artifacts
    validate_artifact(finding, strict_idempotency=True)
    validate_artifact(envelope, strict_idempotency=True)
    validate_artifact(receipt, strict_idempotency=True)


# ── Scenario 7: Admission evidence via promotion_class ───────────────────────

def test_scenario_7_local_only_promotion_class_is_identifiable():
    """An artifact with promotion_class=local_only carries the correct envelope
    field for the admission gate to block it. The artifact itself is structurally
    valid — the admission gate reads promotion_class at the application layer,
    not at the schema layer.
    """
    artifact = _finding_artifact(promotion_class="local_only")
    # Structurally valid regardless of promotion_class
    validate_artifact(artifact, strict_idempotency=True)
    # The admission gate (DataForge Local) would block this based on the field value
    assert artifact["promotion_class"] == "local_only"


def test_scenario_7b_promotable_class_passes_through():
    """An artifact with promotion_class=promotable passes the admission field check."""
    artifact = _finding_artifact(promotion_class="promotable")
    validate_artifact(artifact, strict_idempotency=True)
    assert artifact["promotion_class"] == "promotable"
