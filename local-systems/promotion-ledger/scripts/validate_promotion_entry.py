#!/usr/bin/env python3
"""Validate a Forge promotion ledger entry."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependent
    print(f"FAIL: PyYAML is required to load promotion YAML: {exc}", file=sys.stderr)
    sys.exit(2)


REQUIRED_FIELDS = [
    "promotion_id",
    "slice_name",
    "source_repo",
    "source_branch",
    "source_commit",
    "target_repo",
    "target_branch",
    "target_commit",
    "promoted_files",
    "excluded_files",
    "promotion_manifest",
    "proof_commands",
    "proof_results",
    "evidence_path",
    "runtime_status_proof",
    "authorforge_impact",
    "reviewer",
    "decision",
    "decision_reason",
    "created_at",
    "rollback_source_commit",
    "rollback_target_commit",
    "rollback_command",
    "rollback_evidence_path",
    "supersedes_promotion_id",
]

ALLOWED_DECISIONS = {"accepted", "rejected", "rollback", "needs-followup"}
LIST_FIELDS = {"promoted_files", "excluded_files", "promotion_manifest", "proof_commands"}


def load_yaml(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["promotion entry must be a YAML mapping"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")

    decision = data.get("decision")
    if decision not in ALLOWED_DECISIONS:
        errors.append(
            "decision must be one of: " + ", ".join(sorted(ALLOWED_DECISIONS))
        )

    for field in LIST_FIELDS:
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field} must be a list")

    evidence_path = data.get("evidence_path")
    if not isinstance(evidence_path, str) or not evidence_path.strip():
        errors.append("evidence_path must be present and non-empty")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_promotion_entry.py <promotion-entry.yaml>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"FAIL: promotion entry not found: {path}", file=sys.stderr)
        return 2

    try:
        data = load_yaml(path)
    except Exception as exc:
        print(f"FAIL: could not load YAML: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        print(f"FAIL: {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
