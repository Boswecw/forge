"""Schema gate: verify all admitted family schemas and the shared envelope schema exist and are valid JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

_CONTRACTS_DIR = Path(__file__).parent.parent.parent / "contracts"
_FAMILY_REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry" / "artifact_family_registry.json"


class SchemaGateError(Exception):
    """Raised when the schema gate fails."""


def run() -> list[str]:
    """Run the schema gate. Returns list of failure messages (empty = pass)."""
    failures: list[str] = []

    # Verify shared envelope schema
    envelope_path = _CONTRACTS_DIR / "envelope" / "shared-envelope.schema.json"
    if not envelope_path.exists():
        failures.append(f"MISSING: {envelope_path}")
    else:
        try:
            schema = json.loads(envelope_path.read_text(encoding="utf-8"))
            jsonschema.Draft7Validator.check_schema(schema)
        except Exception as exc:
            failures.append(f"INVALID_SCHEMA: {envelope_path}: {exc}")

    # Verify all admitted family schemas
    registry = json.loads(_FAMILY_REGISTRY_PATH.read_text(encoding="utf-8"))
    for entry in registry.get("families", []):
        schema_path = Path(__file__).parent.parent.parent / entry["schema_path"]
        if not schema_path.exists():
            failures.append(f"MISSING: {schema_path}")
            continue
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.Draft7Validator.check_schema(schema)
        except Exception as exc:
            failures.append(f"INVALID_SCHEMA: {schema_path}: {exc}")

    return failures
