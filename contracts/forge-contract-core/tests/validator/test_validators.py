"""Tests: validator package behavior."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forge_contract_core.identity import compute_idempotency_key, verify_idempotency_key
from forge_contract_core.refs import ArtifactRef, InvalidRefError, format_reference, parse_reference
from forge_contract_core.validators.artifact import ArtifactValidationError, validate_artifact
from forge_contract_core.validators.families import (
    UnsupportedFamilyError,
    UnsupportedVersionError,
    validate_family_payload,
)
from forge_contract_core.validators.role_matrix import (
    RoleMatrixViolationError,
    check_producer_admitted,
)

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"


def _load_clean(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


# ── Full artifact validation ───────────────────────────────────────────────────

def test_validate_artifact_accepts_valid_source_drift_finding():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "source_drift_finding.v1.valid.json")
    validate_artifact(artifact, strict_idempotency=False)  # fixture uses placeholder key


def test_validate_artifact_accepts_valid_promotion_envelope():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "promotion_envelope.v1.valid.json")
    validate_artifact(artifact, strict_idempotency=False)


def test_validate_artifact_accepts_valid_promotion_receipt():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "promotion_receipt.v1.valid.json")
    validate_artifact(artifact, strict_idempotency=False)


def test_validate_artifact_rejects_missing_envelope_field():
    artifact = _load_clean(FIXTURES_DIR / "invalid" / "envelope.missing_envelope_field.json")
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)
    assert exc_info.value.cause == "invalid_envelope"


def test_validate_artifact_rejects_missing_payload_field():
    artifact = _load_clean(FIXTURES_DIR / "invalid" / "source_drift_finding.v1.missing_required.json")
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)
    assert exc_info.value.cause == "invalid_payload"


def test_validate_artifact_rejects_invalid_enum():
    artifact = _load_clean(FIXTURES_DIR / "invalid" / "source_drift_finding.v1.invalid_enum.json")
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)
    assert exc_info.value.cause == "invalid_payload"


def test_validate_artifact_rejects_unsupported_family():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "source_drift_finding.v1.valid.json")
    artifact["artifact_family"] = "approval_artifact"
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)
    assert exc_info.value.cause == "unsupported_family"


def test_validate_artifact_rejects_unsupported_version():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "source_drift_finding.v1.valid.json")
    artifact["artifact_version"] = 999
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=False)
    assert exc_info.value.cause == "unsupported_version"


# ── Idempotency key ────────────────────────────────────────────────────────────

def test_idempotency_key_is_64_hex_chars():
    key = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    assert len(key) == 64
    assert all(c in "0123456789abcdef" for c in key)


def test_idempotency_key_is_stable():
    k1 = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    k2 = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    assert k1 == k2


def test_idempotency_key_differs_on_different_inputs():
    k1 = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    k2 = compute_idempotency_key("source_drift_finding", "abc-456", 1, "abc-456")
    assert k1 != k2


def test_verify_idempotency_key_passes_for_correct_key():
    k = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    assert verify_idempotency_key(k, "source_drift_finding", "abc-123", 1, "abc-123")


def test_verify_idempotency_key_fails_for_wrong_key():
    assert not verify_idempotency_key("0" * 64, "source_drift_finding", "abc-123", 1, "abc-123")


def test_strict_idempotency_rejects_wrong_key():
    artifact = _load_clean(FIXTURES_DIR / "valid" / "source_drift_finding.v1.valid.json")
    artifact["idempotency_key"] = "0" * 64
    with pytest.raises(ArtifactValidationError) as exc_info:
        validate_artifact(artifact, strict_idempotency=True)
    assert exc_info.value.cause == "invalid_idempotency_key"


# ── Reference grammar ─────────────────────────────────────────────────────────

def test_parse_reference_valid():
    ref = parse_reference("source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1")
    assert ref.family == "source_drift_finding"
    assert ref.artifact_id == "a1b2c3d4-0001-0001-0001-000000000001"
    assert ref.version == 1


def test_parse_reference_roundtrip():
    original = "source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1"
    ref = parse_reference(original)
    assert str(ref) == original


def test_format_reference():
    result = format_reference("source_drift_finding", "a1b2c3d4-0001-0001-0001-000000000001", 1)
    assert result == "source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1"


@pytest.mark.parametrize("bad_ref", [
    "not-a-valid-reference",
    "source_drift_finding:not-a-uuid:v1",
    "source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:0",
    "",
    "source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001",
])
def test_parse_reference_invalid(bad_ref: str):
    with pytest.raises(InvalidRefError):
        parse_reference(bad_ref)


# ── Role matrix ───────────────────────────────────────────────────────────────

def test_admitted_producer_passes_role_matrix():
    check_producer_admitted("dataforge-Local", "source_drift_finding")


def test_unadmitted_producer_fails_role_matrix():
    with pytest.raises(RoleMatrixViolationError):
        check_producer_admitted("forgeHQ", "source_drift_finding")


def test_unadmitted_family_fails_role_matrix():
    with pytest.raises(RoleMatrixViolationError):
        check_producer_admitted("dataforge-Local", "approval_artifact")


def test_unknown_repo_fails_role_matrix():
    with pytest.raises(RoleMatrixViolationError):
        check_producer_admitted("nonexistent-repo", "source_drift_finding")


# ── Family validation ─────────────────────────────────────────────────────────

def test_unsupported_family_raises():
    with pytest.raises(UnsupportedFamilyError):
        validate_family_payload("approval_artifact", 1, {})


def test_unsupported_version_raises():
    with pytest.raises(UnsupportedVersionError):
        validate_family_payload("source_drift_finding", 999, {})
