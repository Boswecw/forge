"""Family payload validation against admitted family schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from forge_contract_core.enums import ADMITTED_FAMILIES, ADMITTED_VERSIONS

_SCHEMAS_DIR = Path(__file__).parent.parent.parent / "contracts" / "families"

_schemas: dict[tuple[str, int], dict[str, Any]] = {}


class FamilyValidationError(ValueError):
    """Raised when a family payload fails schema validation."""

    def __init__(self, message: str, errors: list[str]) -> None:
        super().__init__(message)
        self.errors = errors


class UnsupportedFamilyError(ValueError):
    """Raised when the artifact_family is not admitted."""


class UnsupportedVersionError(ValueError):
    """Raised when the artifact_version is not admitted for this family."""


def _load_family_schema(family: str, version: int) -> dict[str, Any]:
    key = (family, version)
    if key not in _schemas:
        path = _SCHEMAS_DIR / family / f"{family}.v{version}.schema.json"
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")
        _schemas[key] = json.loads(path.read_text(encoding="utf-8"))
    return _schemas[key]


def validate_family_payload(
    family: str,
    version: int,
    payload: dict[str, Any],
) -> None:
    """Validate a payload dict against the admitted family schema.

    Raises:
    - UnsupportedFamilyError if family is not admitted
    - UnsupportedVersionError if version is not admitted for this family
    - FamilyValidationError if payload fails schema validation
    """
    if family not in ADMITTED_FAMILIES:
        raise UnsupportedFamilyError(
            f"Family {family!r} is not admitted in proving slice 01. "
            f"Admitted families: {sorted(ADMITTED_FAMILIES)}"
        )
    if version not in ADMITTED_VERSIONS.get(family, frozenset()):
        raise UnsupportedVersionError(
            f"Version {version} is not admitted for family {family!r}. "
            f"Admitted versions: {sorted(ADMITTED_VERSIONS.get(family, frozenset()))}"
        )

    schema = _load_family_schema(family, version)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        messages = [f"{'.'.join(str(p) for p in e.path) or 'root'}: {e.message}" for e in errors]
        raise FamilyValidationError(
            f"Payload validation failed for {family} v{version} with {len(messages)} error(s)",
            messages,
        )
