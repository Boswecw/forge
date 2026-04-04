"""Role-matrix validation: check that a producer is admitted to emit a given family."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REGISTRY_PATH = (
    Path(__file__).parent.parent.parent / "registry" / "repo_role_matrix.json"
)

_matrix: dict[str, Any] | None = None


class RoleMatrixViolationError(ValueError):
    """Raised when a producer is not admitted to emit a family."""


def _load_matrix() -> dict[str, Any]:
    global _matrix
    if _matrix is None:
        _matrix = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
    return _matrix


def check_producer_admitted(produced_by_system: str, artifact_family: str) -> None:
    """Verify that produced_by_system is admitted to emit artifact_family.

    Raises RoleMatrixViolationError if the check fails.
    """
    matrix = _load_matrix()
    repos = {r["repo"]: r for r in matrix.get("repos", [])}

    if produced_by_system not in repos:
        raise RoleMatrixViolationError(
            f"Producer {produced_by_system!r} is not in the repo role matrix."
        )

    entry = repos[produced_by_system]
    allowed = entry.get("allowed_emit_families", [])
    if artifact_family not in allowed:
        raise RoleMatrixViolationError(
            f"Producer {produced_by_system!r} is not admitted to emit family "
            f"{artifact_family!r}. Allowed: {allowed}"
        )
