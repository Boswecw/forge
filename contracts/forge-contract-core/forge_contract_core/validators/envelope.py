"""Envelope validation against the shared-envelope schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

_SCHEMA_PATH = (
    Path(__file__).parent.parent.parent
    / "contracts"
    / "envelope"
    / "shared-envelope.schema.json"
)

_schema: dict[str, Any] | None = None


def _load_schema() -> dict[str, Any]:
    global _schema
    if _schema is None:
        _schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    return _schema


class EnvelopeValidationError(ValueError):
    """Raised when an artifact envelope fails schema validation."""

    def __init__(self, message: str, errors: list[str]) -> None:
        super().__init__(message)
        self.errors = errors


def validate_envelope(artifact: dict[str, Any]) -> None:
    """Validate an artifact dict against the shared envelope schema.

    Raises EnvelopeValidationError if validation fails.
    """
    schema = _load_schema()
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(artifact), key=lambda e: list(e.path))
    if errors:
        messages = [f"{'.'.join(str(p) for p in e.path) or 'root'}: {e.message}" for e in errors]
        raise EnvelopeValidationError(
            f"Envelope validation failed with {len(messages)} error(s)",
            messages,
        )
