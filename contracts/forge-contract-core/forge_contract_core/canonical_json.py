"""Canonical JSON serialization for Forge proving-slice artifacts.

Canonical JSON is used for idempotency-key computation and signature verification.
Rules:
- Keys sorted lexicographically
- No extra whitespace
- UTF-8 encoding
- No trailing newline
"""

from __future__ import annotations

import json


def canonical_dumps(obj: object) -> str:
    """Serialize obj to canonical JSON string (keys sorted, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_bytes(obj: object) -> bytes:
    """Serialize obj to canonical JSON bytes (UTF-8)."""
    return canonical_dumps(obj).encode("utf-8")
