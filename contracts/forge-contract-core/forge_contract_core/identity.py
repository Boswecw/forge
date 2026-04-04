"""Idempotency-key generation for Forge proving-slice artifacts.

Algorithm (from Pack 09 §5.3):
  sha256(artifact_family + "|" + artifact_id + "|" + str(artifact_version) + "|" + lineage_root_id)
"""

from __future__ import annotations

import hashlib


def compute_idempotency_key(
    artifact_family: str,
    artifact_id: str,
    artifact_version: int,
    lineage_root_id: str,
) -> str:
    """Return a 64-char hex SHA-256 idempotency key for the given artifact identity.

    This is the canonical proving-slice algorithm. All producers and consumers
    must use this function to compute idempotency keys; never compute locally.
    """
    raw = f"{artifact_family}|{artifact_id}|{artifact_version}|{lineage_root_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def verify_idempotency_key(
    key: str,
    artifact_family: str,
    artifact_id: str,
    artifact_version: int,
    lineage_root_id: str,
) -> bool:
    """Return True if key matches the computed canonical idempotency key."""
    return key == compute_idempotency_key(
        artifact_family, artifact_id, artifact_version, lineage_root_id
    )
