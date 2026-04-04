"""Validator gate: verify validator correctness on known-good and known-bad inputs."""

from __future__ import annotations

from forge_contract_core.identity import compute_idempotency_key, verify_idempotency_key
from forge_contract_core.refs import InvalidRefError, parse_reference
from forge_contract_core.validators.families import (
    UnsupportedFamilyError,
    UnsupportedVersionError,
    validate_family_payload,
)


def run() -> list[str]:
    """Run the validator gate. Returns list of failure messages (empty = pass)."""
    failures: list[str] = []

    # Idempotency key stability
    key1 = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    key2 = compute_idempotency_key("source_drift_finding", "abc-123", 1, "abc-123")
    if key1 != key2:
        failures.append("IDEMPOTENCY_KEY_UNSTABLE: same inputs produced different keys")
    if len(key1) != 64:
        failures.append(f"IDEMPOTENCY_KEY_WRONG_LENGTH: expected 64, got {len(key1)}")

    # verify_idempotency_key should pass for matching
    if not verify_idempotency_key(key1, "source_drift_finding", "abc-123", 1, "abc-123"):
        failures.append("VERIFY_IDEMPOTENCY_KEY_FAILED: should have returned True")

    # verify_idempotency_key should fail for mismatching
    if verify_idempotency_key("0" * 64, "source_drift_finding", "abc-123", 1, "abc-123"):
        failures.append("VERIFY_IDEMPOTENCY_KEY_FALSE_POSITIVE: should have returned False")

    # Reference grammar parsing
    try:
        ref = parse_reference("source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1")
        if ref.family != "source_drift_finding":
            failures.append(f"REF_PARSE_FAMILY: expected source_drift_finding, got {ref.family}")
        if ref.version != 1:
            failures.append(f"REF_PARSE_VERSION: expected 1, got {ref.version}")
    except InvalidRefError as exc:
        failures.append(f"REF_PARSE_FAILED: {exc}")

    # Invalid reference must fail
    try:
        parse_reference("not-a-valid-reference")
        failures.append("REF_PARSE_INVALID: should have raised InvalidRefError")
    except InvalidRefError:
        pass  # Expected

    # Unsupported family must fail
    try:
        validate_family_payload("approval_artifact", 1, {})
        failures.append("UNSUPPORTED_FAMILY: should have raised UnsupportedFamilyError")
    except UnsupportedFamilyError:
        pass  # Expected

    # Unsupported version must fail
    try:
        validate_family_payload("source_drift_finding", 999, {})
        failures.append("UNSUPPORTED_VERSION: should have raised UnsupportedVersionError")
    except UnsupportedVersionError:
        pass  # Expected

    return failures
