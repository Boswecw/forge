# Implementation Pack C — Slice 00.5b Python Wrapper (evidence_cli)

Owner: Charlie
Scope: `signalforge/core/evidence_cli.py` wrapper for the Rust `forge-evidence` binary.

Hard rules:
- Fail-closed: any nonzero exit must raise a typed exception containing stderr.
- Deterministic: wrapper does not mutate inputs; Rust controls canonicalization/hashing.

---

## File: `signalforge/core/evidence_cli.py`

```python
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from signalforge.core.errors import SignalForgeError


class EvidenceCliError(SignalForgeError):
    pass


@dataclass(frozen=True)
class EvidenceCli:
    """Thin wrapper around the `forge-evidence` binary."""

    binary: str = "forge-evidence"
    float_precision: int = 8

    def _require_binary(self) -> None:
        if shutil.which(self.binary) is None:
            raise EvidenceCliError(
                f"Missing required binary '{self.binary}' on PATH. Build/install forge_evidence first."
            )

    def _run(self, args: List[str], *, stdin_bytes: Optional[bytes] = None) -> bytes:
        self._require_binary()
        cmd = [self.binary, "--float-precision", str(self.float_precision), *args]
        try:
            p = subprocess.run(
                cmd,
                input=stdin_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as e:
            raise EvidenceCliError(f"Failed to execute {cmd}: {e}") from e

        if p.returncode != 0:
            stderr = (p.stderr or b"").decode("utf-8", errors="replace").strip()
            raise EvidenceCliError(
                f"forge-evidence failed (code {p.returncode}) for args={args}. stderr={stderr}"
            )
        return p.stdout or b""

    def canonicalize_json_bytes(self, json_bytes: bytes) -> bytes:
        return self._run(["canonicalize"], stdin_bytes=json_bytes)

    def sha256_hex(self, raw_bytes: bytes) -> str:
        out = self._run(["sha256"], stdin_bytes=raw_bytes)
        return out.decode("utf-8", errors="replace").strip()

    def artifact_id_hex(self, kind: str, json_bytes: bytes) -> str:
        out = self._run(["artifact-id", "--kind", kind], stdin_bytes=json_bytes)
        return out.decode("utf-8", errors="replace").strip()

    def hashchain_from_manifest(self, manifest_path: str | Path) -> Dict[str, Any]:
        mp = str(Path(manifest_path))
        out = self._run(["hashchain", "--manifest", mp])
        try:
            return json.loads(out.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise EvidenceCliError(f"forge-evidence hashchain output was not valid JSON: {e}") from e


# Convenience module-level helpers (single default instance)
_default = EvidenceCli()


def canonicalize_json_bytes(json_bytes: bytes) -> bytes:
    return _default.canonicalize_json_bytes(json_bytes)


def sha256_hex(raw_bytes: bytes) -> str:
    return _default.sha256_hex(raw_bytes)


def artifact_id_hex(kind: str, json_bytes: bytes) -> str:
    return _default.artifact_id_hex(kind, json_bytes)


def hashchain_from_manifest(manifest_path: str | Path) -> Dict[str, Any]:
    return _default.hashchain_from_manifest(manifest_path)
```

---

## Tests (integration)

Create: `tests/test_hashchain_integration.py`

```python
import json
import os
import shutil
from pathlib import Path

import pytest

from signalforge.core.evidence_cli import EvidenceCli


pytestmark = pytest.mark.integration


def _have_binary(name: str) -> bool:
    return shutil.which(name) is not None


@pytest.mark.skipif(not _have_binary("forge-evidence"), reason="forge-evidence not on PATH")
def test_canonicalize_and_sha256(tmp_path: Path):
    cli = EvidenceCli(float_precision=8)

    raw = b'{"b":0.5,"a":1.234567891,"c":[3,2,1]}'
    canon = cli.canonicalize_json_bytes(raw)
    s = canon.decode("utf-8")

    assert s.startswith('{"a":')
    assert "0.50000000" in s
    assert "1.23456789" in s

    h = cli.sha256_hex(canon)
    assert len(h) == 64


@pytest.mark.skipif(not _have_binary("forge-evidence"), reason="forge-evidence not on PATH")
def test_hashchain_from_manifest(tmp_path: Path):
    cli = EvidenceCli(float_precision=8)

    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text('{"x":1,"y":0.5}', encoding="utf-8")
    b.write_text('{"y":0.5,"x":1}', encoding="utf-8")

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            [
                {"kind": "a", "path": str(a)},
                {"kind": "b", "path": str(b)},
            ]
        ),
        encoding="utf-8",
    )

    out = cli.hashchain_from_manifest(manifest)
    assert out["schema_version"] == "v1"
    assert len(out["artifact_hashes"]) == 2
    assert len(out["chain_hashes"]) == 3  # H0 + 2 steps
    assert out["final_chain_hash"] == out["chain_hashes"][-1]

    # because a.json and b.json canonicalize to identical bytes, their artifact hashes must match
    h0 = out["artifact_hashes"][0]["artifact_sha256"]
    h1 = out["artifact_hashes"][1]["artifact_sha256"]
    assert h0 == h1
```

---

## Notes

- This wrapper is used everywhere you need hashes/IDs. Python should never re-implement canonicalization.
- If you want, we can add a small `signalforge/core/evidence_manifest.py` helper later to build the manifest in the fixed artifact order.

