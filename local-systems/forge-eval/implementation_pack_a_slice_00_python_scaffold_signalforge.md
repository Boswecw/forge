# Implementation Pack A — Slice 00 Python Scaffold (signalforge)

Owner: Charlie
Scope: Slice 00 foundation (CLI + config + run context + schema validation + placeholder stage runner). Offline-first.

---

## Folder layout

```
SignalForge/
  signalforge/
    __init__.py
    cli.py
    config.py
    core/
      run_context.py
      errors.py
    pipeline/
      validation.py
      run.py
    schemas/
      risk_heatmap.schema.json
      context_slices.schema.json
      review_findings.schema.json
      telemetry_matrix.schema.json
      occupancy_snapshot.schema.json
      capture_estimate.schema.json
      hazard_map.schema.json
      merge_decision.schema.json
      evidence_bundle.schema.json
  tests/
    test_cli_smoke.py
  pyproject.toml
```

---

## `signalforge/config.py`

```python
from __future__ import annotations

from typing import Dict, List, Literal
from pydantic import BaseModel, Field, ConfigDict

RiskBucket = Literal["low", "medium", "high"]


class BucketThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")
    low_lt: float = 0.33
    medium_lt: float = 0.66


class SignalForgeConfig(BaseModel):
    """Central config. CLI flags override these."""

    model_config = ConfigDict(extra="forbid")

    # Risk weights
    w_churn: float = 1.0
    w_deps: float = 1.0
    w_tests: float = 0.0
    w_violations: float = 0.0
    w_history: float = 0.0

    # Thresholds
    tau: float = 0.70
    theta: float = 2.0
    psi_threshold: float = 0.75
    hazard_threshold: float = 0.75

    # Telemetry health
    required_methods: List[str] = Field(default_factory=lambda: ["reviewer_rule", "reviewer_ast"])
    fail_closed_on_null: bool = True

    # Correlation guard
    k_eff_threshold: float = 2.0

    # Capture–recapture
    safety_margin: float = 1.25

    # Occupancy bucketed p(method|bucket)
    p_by_method_bucketed: Dict[RiskBucket, Dict[str, float]] = Field(
        default_factory=lambda: {
            "low": {
                "reviewer_rule": 0.20,
                "reviewer_ast": 0.25,
                "reviewer_llm": 0.35,
                "tests": 0.55,
                "static": 0.30,
            },
            "medium": {
                "reviewer_rule": 0.30,
                "reviewer_ast": 0.40,
                "reviewer_llm": 0.45,
                "tests": 0.60,
                "static": 0.35,
            },
            "high": {
                "reviewer_rule": 0.40,
                "reviewer_ast": 0.50,
                "reviewer_llm": 0.55,
                "tests": 0.65,
                "static": 0.45,
            },
        }
    )

    bucket_thresholds: BucketThresholds = Field(default_factory=BucketThresholds)

    # Hazard betas
    beta0: float = -2.0
    beta1: float = 1.2
    beta2: float = 0.8
    beta3: float = 0.5
    beta4: float = 0.7

    # Context extraction limits
    expansion_lines: int = 20
    max_slices_per_target: int = 10
    max_lines_per_slice: int = 200
    max_total_lines: int = 2000

    # Defect identity
    context_window_size_lines: int = 50
    violation_category_map: Dict[str, str] = Field(
        default_factory=lambda: {
            "style": "STYLE",
            "security": "SECURITY",
            "correctness": "CORRECTNESS",
            "performance": "PERFORMANCE",
            "tests": "TESTS",
            "docs": "DOCS",
            "uncategorized_other": "UNCATEGORIZED_OTHER",
        }
    )

    # Calibration
    beta_strength_s: float = 10.0
    calibration_consensus_k: int = 2
    calibration_high_weight_methods: List[str] = Field(default_factory=list)


def clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x
```

---

## `signalforge/core/run_context.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone


@dataclass(frozen=True)
class RunContext:
    run_id: str
    seed: int
    commit_sha: str
    repo_path: Path
    out_dir: Path
    config_path: Path | None
    started_at: datetime

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)
```

---

## `signalforge/core/errors.py`

```python
class SignalForgeError(Exception):
    pass


class SchemaValidationError(SignalForgeError):
    pass


class StageError(SignalForgeError):
    pass


class ConfigError(SignalForgeError):
    pass
```

---

## `signalforge/pipeline/validation.py`

```python
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

from signalforge.core.errors import SchemaValidationError


def load_schema(schema_dir: Path, kind: str) -> dict:
    p = schema_dir / f"{kind}.schema.json"
    if not p.exists():
        raise SchemaValidationError(f"Missing schema file: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def validate_artifact(schema: dict, obj: dict, *, kind: str) -> None:
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(obj), key=lambda e: e.path)
    if errors:
        msg = "\n".join([f"{kind}: {list(e.path)}: {e.message}" for e in errors[:25]])
        raise SchemaValidationError(msg)
```

---

## `signalforge/pipeline/run.py`

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict
from datetime import datetime, timezone

from signalforge.core.errors import StageError
from signalforge.pipeline.validation import load_schema, validate_artifact


STAGE_ORDER = [
    "risk_heatmap",
    "context_slices",
    "review_findings",
    "telemetry_matrix",
    "occupancy_snapshot",
    "capture_estimate",
    "hazard_map",
    "merge_decision",
    "evidence_bundle",
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def placeholder_artifact(kind: str, run_id: str, commit_sha: str) -> dict:
    return {
        "schema_version": "v1",
        "kind": kind,
        "run_id": run_id,
        "commit_sha": commit_sha,
        "generated_at": _utc_now_iso(),
        "data": {},
    }


def run_stages(
    *,
    out_dir: Path,
    schema_dir: Path,
    run_id: str,
    commit_sha: str,
    stages: Dict[str, Callable[[], dict]] | None = None,
) -> None:
    """Slice 00 runner: emits placeholders (or supplied stage callables) and validates schemas."""

    out_dir.mkdir(parents=True, exist_ok=True)

    stages = stages or {}
    for kind in STAGE_ORDER:
        try:
            obj = stages.get(kind, lambda k=kind: placeholder_artifact(k, run_id, commit_sha))()
            schema = load_schema(schema_dir, kind)
            validate_artifact(schema, obj, kind=kind)
            (out_dir / f"{kind}.json").write_text(
                json.dumps(obj, indent=2, sort_keys=True),
                encoding="utf-8",
            )
        except Exception as e:
            raise StageError(f"Stage failed: {kind}: {e}") from e
```

---

## `signalforge/cli.py`

```python
from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from pydantic import ValidationError

from signalforge.config import SignalForgeConfig
from signalforge.core.run_context import RunContext
from signalforge.core.errors import ConfigError
from signalforge.pipeline.run import run_stages
from signalforge.pipeline.validation import load_schema, validate_artifact


def _load_config(path: Path | None) -> SignalForgeConfig:
    if path is None:
        return SignalForgeConfig()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return SignalForgeConfig.model_validate(data)
    except (OSError, json.JSONDecodeError, ValidationError) as e:
        raise ConfigError(f"Invalid config: {path}: {e}") from e


def cmd_run(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    schema_dir = Path(__file__).with_name("schemas")

    cfg_path = Path(args.config).expanduser().resolve() if args.config else None
    cfg = _load_config(cfg_path)

    # Example overrides (extend as needed)
    if args.tau is not None:
        cfg.tau = float(args.tau)
    if args.theta is not None:
        cfg.theta = float(args.theta)

    run_id = str(uuid.uuid4())
    ctx = RunContext(
        run_id=run_id,
        seed=int(args.seed),
        commit_sha=args.commit,
        repo_path=repo,
        out_dir=out_dir,
        config_path=cfg_path,
        started_at=RunContext.now_utc(),
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "config.json").write_text(cfg.model_dump_json(indent=2), encoding="utf-8")

    run_stages(out_dir=out_dir, schema_dir=schema_dir, run_id=ctx.run_id, commit_sha=ctx.commit_sha)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    out_dir = Path(args.dir).expanduser().resolve()
    schema_dir = Path(__file__).with_name("schemas")

    for p in sorted(out_dir.glob("*.json")):
        kind = p.stem
        if kind == "config":
            continue
        schema = load_schema(schema_dir, kind)
        obj = json.loads(p.read_text(encoding="utf-8"))
        validate_artifact(schema, obj, kind=kind)
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="signalforge")
    sub = ap.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--repo", required=True)
    run.add_argument("--commit", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--seed", required=True, type=int)
    run.add_argument("--config", required=False)
    run.add_argument("--tau", required=False)
    run.add_argument("--theta", required=False)
    run.set_defaults(fn=cmd_run)

    val = sub.add_parser("validate")
    val.add_argument("--dir", required=True)
    val.set_defaults(fn=cmd_validate)

    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## Minimal schemas (repeat per artifact kind)

Create each file under `signalforge/schemas/` with this content (update only the filename; schema stays the same for Slice 00 placeholders):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "data"],
  "properties": {
    "schema_version": { "type": "string" },
    "kind": { "type": "string" },
    "run_id": { "type": "string" },
    "commit_sha": { "type": "string" },
    "generated_at": { "type": "string" },
    "data": { "type": "object" }
  }
}
```

---

## `tests/test_cli_smoke.py`

```python
import subprocess
import sys
from pathlib import Path


def test_cli_smoke(tmp_path: Path):
    out_dir = tmp_path / "out"
    cmd = [
        sys.executable,
        "-m",
        "signalforge.cli",
        "run",
        "--repo",
        str(tmp_path),
        "--commit",
        "deadbeef",
        "--out",
        str(out_dir),
        "--seed",
        "1337",
    ]
    subprocess.check_call(cmd)

    assert (out_dir / "risk_heatmap.json").exists()

    subprocess.check_call(
        [sys.executable, "-m", "signalforge.cli", "validate", "--dir", str(out_dir)]
    )
```

---

## Run

```bash
python -m signalforge.cli run --repo . --commit deadbeef --out ./out --seed 1337
python -m signalforge.cli validate --dir ./out
pytest -q
```

