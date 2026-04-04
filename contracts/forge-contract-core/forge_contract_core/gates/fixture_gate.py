"""Fixture gate: verify all valid fixtures pass validation, all invalid fixtures fail."""

from __future__ import annotations

import json
from pathlib import Path

from forge_contract_core.validators.artifact import ArtifactValidationError, validate_artifact

_FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"


def run() -> list[str]:
    """Run the fixture gate. Returns list of failure messages (empty = pass)."""
    failures: list[str] = []

    # Valid fixtures must pass
    for path in sorted((_FIXTURES_DIR / "valid").glob("*.json")):
        try:
            artifact = json.loads(path.read_text(encoding="utf-8"))
            # Strip _fixture metadata before validation
            artifact_clean = {k: v for k, v in artifact.items() if not k.startswith("_")}
            validate_artifact(artifact_clean, strict_idempotency=False)
        except ArtifactValidationError as exc:
            failures.append(f"VALID_FIXTURE_FAILED: {path.name}: {exc}")
        except Exception as exc:
            failures.append(f"VALID_FIXTURE_ERROR: {path.name}: {exc}")

    # Invalid fixtures must fail validation
    for path in sorted((_FIXTURES_DIR / "invalid").glob("*.json")):
        try:
            artifact = json.loads(path.read_text(encoding="utf-8"))
            artifact_clean = {k: v for k, v in artifact.items() if not k.startswith("_")}
            validate_artifact(artifact_clean, strict_idempotency=False)
            failures.append(f"INVALID_FIXTURE_PASSED: {path.name}: expected validation failure but got none")
        except ArtifactValidationError:
            pass  # Expected — invalid fixture correctly rejected
        except Exception as exc:
            failures.append(f"INVALID_FIXTURE_ERROR: {path.name}: {exc}")

    # Duplicate fixtures must be structurally valid (they test idempotency, not schema)
    for path in sorted((_FIXTURES_DIR / "duplicate").glob("*.json")):
        try:
            artifact = json.loads(path.read_text(encoding="utf-8"))
            artifact_clean = {k: v for k, v in artifact.items() if not k.startswith("_")}
            validate_artifact(artifact_clean, strict_idempotency=False)
        except ArtifactValidationError as exc:
            failures.append(f"DUPLICATE_FIXTURE_FAILED: {path.name}: {exc}")
        except Exception as exc:
            failures.append(f"DUPLICATE_FIXTURE_ERROR: {path.name}: {exc}")

    return failures
