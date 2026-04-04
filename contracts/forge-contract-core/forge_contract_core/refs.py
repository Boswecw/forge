"""Canonical reference grammar for Forge proving-slice artifacts.

Grammar (from Pack 09 §5.2):
  <artifact_family>:<artifact_id>:v<artifact_version>

Examples:
  source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1
  promotion_receipt:c3d4e5f6-0003-0003-0003-000000000003:v1
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_REF_PATTERN = re.compile(
    r"^(?P<family>[a-z][a-z0-9_]*):"
    r"(?P<artifact_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}):"
    r"v(?P<version>[1-9][0-9]*)$"
)


@dataclass(frozen=True)
class ArtifactRef:
    family: str
    artifact_id: str
    version: int

    def __str__(self) -> str:
        return f"{self.family}:{self.artifact_id}:v{self.version}"


class InvalidRefError(ValueError):
    """Raised when a reference string does not match canonical grammar."""


def parse_reference(ref: str) -> ArtifactRef:
    """Parse a canonical artifact reference string.

    Raises InvalidRefError if the string does not match canonical grammar.
    """
    m = _REF_PATTERN.match(ref)
    if not m:
        raise InvalidRefError(
            f"Invalid artifact reference: {ref!r}. "
            f"Expected format: <family>:<uuid>:v<version>"
        )
    return ArtifactRef(
        family=m.group("family"),
        artifact_id=m.group("artifact_id"),
        version=int(m.group("version")),
    )


def format_reference(family: str, artifact_id: str, version: int) -> str:
    """Format a canonical artifact reference string."""
    return f"{family}:{artifact_id}:v{version}"
