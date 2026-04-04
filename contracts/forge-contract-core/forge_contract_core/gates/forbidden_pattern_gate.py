"""Forbidden pattern gate: verify the forbidden_patterns.json is present and well-formed."""

from __future__ import annotations

import json
from pathlib import Path

_PATTERNS_PATH = Path(__file__).parent.parent.parent / "forbidden_patterns" / "forbidden_patterns.json"

_REQUIRED_FIELDS = {"id", "name", "severity", "description", "detection_hint", "why"}
_VALID_SEVERITIES = {"blocking", "warning"}


def run() -> list[str]:
    """Run the forbidden pattern gate. Returns list of failure messages (empty = pass)."""
    failures: list[str] = []

    if not _PATTERNS_PATH.exists():
        failures.append(f"MISSING: {_PATTERNS_PATH}")
        return failures

    try:
        data = json.loads(_PATTERNS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"INVALID_JSON: {_PATTERNS_PATH}: {exc}")
        return failures

    patterns = data.get("patterns", [])
    if not patterns:
        failures.append("NO_PATTERNS: forbidden_patterns.json has no pattern entries")

    seen_ids: set[str] = set()
    for i, p in enumerate(patterns):
        missing = _REQUIRED_FIELDS - set(p.keys())
        if missing:
            failures.append(f"PATTERN[{i}]_MISSING_FIELDS: {missing}")
        pid = p.get("id", f"[{i}]")
        if pid in seen_ids:
            failures.append(f"PATTERN_DUPLICATE_ID: {pid}")
        seen_ids.add(pid)
        if p.get("severity") not in _VALID_SEVERITIES:
            failures.append(f"PATTERN[{pid}]_INVALID_SEVERITY: {p.get('severity')!r}")

    return failures
