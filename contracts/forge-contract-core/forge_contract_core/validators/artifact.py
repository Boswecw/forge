"""Full artifact validation: envelope + family payload + idempotency key."""

from __future__ import annotations

from typing import Any

from forge_contract_core.identity import verify_idempotency_key
from forge_contract_core.validators.envelope import EnvelopeValidationError, validate_envelope
from forge_contract_core.validators.families import (
    FamilyValidationError,
    UnsupportedFamilyError,
    UnsupportedVersionError,
    validate_family_payload,
)


class ArtifactValidationError(ValueError):
    """Raised when full artifact validation fails."""

    def __init__(self, message: str, cause: str, errors: list[str] | None = None) -> None:
        super().__init__(message)
        self.cause = cause
        self.errors = errors or []


def validate_artifact(artifact: dict[str, Any], *, strict_idempotency: bool = True) -> None:
    """Validate a full proving-slice artifact.

    Checks:
    1. Envelope schema
    2. Family and version admitted
    3. Family payload schema
    4. Idempotency key integrity (if strict_idempotency=True)

    Raises ArtifactValidationError for any failure.
    """
    try:
        validate_envelope(artifact)
    except EnvelopeValidationError as exc:
        raise ArtifactValidationError(
            f"Envelope validation failed: {exc}",
            cause="invalid_envelope",
            errors=exc.errors,
        ) from exc

    family = artifact.get("artifact_family", "")
    version = artifact.get("artifact_version", 0)
    payload = artifact.get("payload", {})

    try:
        validate_family_payload(family, version, payload)
    except UnsupportedFamilyError as exc:
        raise ArtifactValidationError(str(exc), cause="unsupported_family") from exc
    except UnsupportedVersionError as exc:
        raise ArtifactValidationError(str(exc), cause="unsupported_version") from exc
    except FamilyValidationError as exc:
        raise ArtifactValidationError(
            f"Payload validation failed: {exc}",
            cause="invalid_payload",
            errors=exc.errors,
        ) from exc

    if strict_idempotency:
        key = artifact.get("idempotency_key", "")
        artifact_id = artifact.get("artifact_id", "")
        lineage_root_id = artifact.get("lineage_root_id", "")
        if not verify_idempotency_key(key, family, artifact_id, version, lineage_root_id):
            raise ArtifactValidationError(
                "Idempotency key does not match canonical computation. "
                "Use forge_contract_core.identity.compute_idempotency_key().",
                cause="invalid_idempotency_key",
            )
