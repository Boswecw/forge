"""Tests: schema validity and fixture compliance."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"
CONTRACTS_DIR = Path(__file__).parent.parent.parent / "contracts"
REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry" / "artifact_family_registry.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _clean(fixture: dict) -> dict:
    """Strip _fixture metadata keys."""
    return {k: v for k, v in fixture.items() if not k.startswith("_")}


# ── Schema self-validation ────────────────────────────────────────────────────

def test_shared_envelope_schema_is_valid_json_schema():
    path = CONTRACTS_DIR / "envelope" / "shared-envelope.schema.json"
    schema = _load(path)
    jsonschema.Draft7Validator.check_schema(schema)


@pytest.mark.parametrize("family,version", [
    ("source_drift_finding", 1),
    ("promotion_envelope", 1),
    ("promotion_receipt", 1),
])
def test_family_schema_is_valid_json_schema(family: str, version: int):
    path = CONTRACTS_DIR / "families" / family / f"{family}.v{version}.schema.json"
    assert path.exists(), f"Schema file not found: {path}"
    schema = _load(path)
    jsonschema.Draft7Validator.check_schema(schema)


# ── Valid fixtures pass envelope schema ───────────────────────────────────────

@pytest.mark.parametrize("fixture_name", [
    "source_drift_finding.v1.valid.json",
    "promotion_envelope.v1.valid.json",
    "promotion_receipt.v1.valid.json",
])
def test_valid_fixture_passes_envelope_schema(fixture_name: str):
    envelope_schema = _load(CONTRACTS_DIR / "envelope" / "shared-envelope.schema.json")
    artifact = _clean(_load(FIXTURES_DIR / "valid" / fixture_name))
    validator = jsonschema.Draft7Validator(envelope_schema)
    errors = list(validator.iter_errors(artifact))
    assert not errors, f"Valid fixture failed envelope schema: {[e.message for e in errors]}"


# ── Valid fixtures pass family payload schema ──────────────────────────────────

@pytest.mark.parametrize("fixture_name,family,version", [
    ("source_drift_finding.v1.valid.json", "source_drift_finding", 1),
    ("promotion_envelope.v1.valid.json", "promotion_envelope", 1),
    ("promotion_receipt.v1.valid.json", "promotion_receipt", 1),
])
def test_valid_fixture_passes_family_schema(fixture_name: str, family: str, version: int):
    family_schema = _load(
        CONTRACTS_DIR / "families" / family / f"{family}.v{version}.schema.json"
    )
    artifact = _clean(_load(FIXTURES_DIR / "valid" / fixture_name))
    payload = artifact["payload"]
    validator = jsonschema.Draft7Validator(family_schema)
    errors = list(validator.iter_errors(payload))
    assert not errors, f"Valid payload failed family schema: {[e.message for e in errors]}"


# ── Invalid fixtures fail schema ──────────────────────────────────────────────

@pytest.mark.parametrize("fixture_name,expected_error_fragment", [
    ("source_drift_finding.v1.missing_required.json", "required"),
    ("source_drift_finding.v1.invalid_enum.json", "enum"),
    ("envelope.missing_envelope_field.json", "required"),
    ("promotion_receipt.v1.missing_required.json", "required"),
])
def test_invalid_fixture_fails_validation(fixture_name: str, expected_error_fragment: str):
    envelope_schema = _load(CONTRACTS_DIR / "envelope" / "shared-envelope.schema.json")
    artifact = _clean(_load(FIXTURES_DIR / "invalid" / fixture_name))
    validator = jsonschema.Draft7Validator(envelope_schema)
    envelope_errors = list(validator.iter_errors(artifact))

    # Also check family payload if envelope passes
    family = artifact.get("artifact_family")
    version = artifact.get("artifact_version")
    all_errors = list(envelope_errors)
    if not envelope_errors and family and version:
        family_path = CONTRACTS_DIR / "families" / family / f"{family}.v{version}.schema.json"
        if family_path.exists():
            family_schema = _load(family_path)
            payload = artifact.get("payload", {})
            fv = jsonschema.Draft7Validator(family_schema)
            all_errors.extend(fv.iter_errors(payload))

    assert all_errors, f"Invalid fixture {fixture_name!r} should have failed but passed validation"


# ── Duplicate fixture is structurally valid ────────────────────────────────────

def test_duplicate_fixture_is_structurally_valid():
    envelope_schema = _load(CONTRACTS_DIR / "envelope" / "shared-envelope.schema.json")
    artifact = _clean(_load(FIXTURES_DIR / "duplicate" / "source_drift_finding.v1.duplicate.json"))
    validator = jsonschema.Draft7Validator(envelope_schema)
    errors = list(validator.iter_errors(artifact))
    assert not errors, f"Duplicate fixture failed envelope schema: {[e.message for e in errors]}"


# ── Duplicate fixture has same idempotency_key as valid fixture ────────────────

def test_duplicate_fixture_shares_idempotency_key_with_valid():
    valid = _clean(_load(FIXTURES_DIR / "valid" / "source_drift_finding.v1.valid.json"))
    dup = _clean(_load(FIXTURES_DIR / "duplicate" / "source_drift_finding.v1.duplicate.json"))
    assert valid["idempotency_key"] == dup["idempotency_key"], (
        "Duplicate fixture must share idempotency_key with valid fixture"
    )
    assert valid["artifact_id"] == dup["artifact_id"], (
        "Duplicate fixture must share artifact_id with valid fixture"
    )
