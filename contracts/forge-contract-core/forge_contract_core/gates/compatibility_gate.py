"""Compatibility gate: verify the compatibility notes are consistent with the registry."""

from __future__ import annotations

import json
from pathlib import Path

_REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry" / "artifact_family_registry.json"
_COMPAT_PATH = Path(__file__).parent.parent.parent / "contracts" / "compatibility" / "proving_slice_v1.json"


def run() -> list[str]:
    """Run the compatibility gate. Returns list of failure messages (empty = pass)."""
    failures: list[str] = []

    try:
        registry = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
        compat = json.loads(_COMPAT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        failures.append(f"MISSING_FILE: {exc}")
        return failures

    registry_families = {e["family"] for e in registry.get("families", [])}
    compat_families = {e["family"] for e in compat.get("admitted_families", [])}

    # Every admitted family in compat must be in registry
    for f in compat_families:
        if f not in registry_families:
            failures.append(f"COMPAT_FAMILY_NOT_IN_REGISTRY: {f!r}")

    # Every admitted family in registry must be in compat
    for f in registry_families:
        if f not in compat_families:
            failures.append(f"REGISTRY_FAMILY_NOT_IN_COMPAT: {f!r}")

    # Excluded families must not appear in admitted families
    excluded = set(compat.get("excluded_families", []))
    overlap = compat_families & excluded
    if overlap:
        failures.append(f"EXCLUDED_FAMILY_IN_ADMITTED: {overlap}")

    return failures
