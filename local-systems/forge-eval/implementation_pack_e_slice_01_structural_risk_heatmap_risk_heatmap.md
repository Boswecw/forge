# Implementation Pack E — Slice 01 Structural Risk Heatmap (risk_heatmap.json)

Owner: Charlie
Scope: Slice 01 — compute deterministic structural risk per target (file) and emit `risk_heatmap.json` matching Pack D schema.

This pack extends Pack A scaffolding by adding:
- `signalforge/features/churn.py`
- `signalforge/features/deps_graph.py`
- `signalforge/models/structural_risk.py`
- updates to `signalforge/pipeline/run.py` to call the real stage for `risk_heatmap`
- tests with a tiny fixture repo

---

## 0) Design choices (v1)

- Targets = **files changed** in the commit diff (commit vs parent). If parent is unavailable, fall back to `git diff --name-only` against `HEAD~1` and fail-closed if that fails.
- Churn component `C` = normalized LOC change magnitude per file (added+deleted).
- Dependency component `D` = normalized in-degree + out-degree on a lightweight import graph built from repo files (py/ts). Regex-based parsing is acceptable for v1.
- Tests/violations/history components are present but default to 0.0 in v1 (adapters later).
- Risk raw = weighted sum; risk_norm = min-max normalize across targets.

Determinism:
- All ordering is sorted by `path`.
- Normalizations use stable min/max and avoid division by zero.

---

## 1) Files to add

### `signalforge/features/churn.py`

```python
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from signalforge.core.errors import StageError


@dataclass(frozen=True)
class FileChurn:
    path: str
    added: int
    deleted: int

    @property
    def total(self) -> int:
        return int(self.added + self.deleted)


_DIFF_NUMSTAT_RE = re.compile(r"^(?P<add>\d+|-)\t(?P<del>\d+|-)\t(?P<path>.+)$")


def _run_git(repo: Path, args: List[str]) -> str:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
    except OSError as e:
        raise StageError(f"git exec failed: {e}") from e

    if p.returncode != 0:
        raise StageError(f"git failed: {' '.join(args)} stderr={p.stderr.strip()}")
    return p.stdout


def get_parent_commit(repo: Path, commit_sha: str) -> str:
    out = _run_git(repo, ["rev-list", "--parents", "-n", "1", commit_sha]).strip()
    parts = out.split()
    if len(parts) < 2:
        raise StageError(f"No parent commit found for {commit_sha}")
    return parts[1]


def diff_numstat(repo: Path, commit_sha: str) -> List[FileChurn]:
    """Return numstat between parent and commit. Fail-closed if git cannot compute."""
    parent = get_parent_commit(repo, commit_sha)
    out = _run_git(repo, ["diff", "--numstat", f"{parent}..{commit_sha}"])

    churn: List[FileChurn] = []
    for line in out.splitlines():
        m = _DIFF_NUMSTAT_RE.match(line.strip())
        if not m:
            continue
        add_s = m.group("add")
        del_s = m.group("del")
        path = m.group("path")

        # '-' appears for binary files; treat as 0 but keep the file as changed
        added = int(add_s) if add_s.isdigit() else 0
        deleted = int(del_s) if del_s.isdigit() else 0
        churn.append(FileChurn(path=path, added=added, deleted=deleted))

    churn.sort(key=lambda x: x.path)
    return churn


def changed_files(repo: Path, commit_sha: str) -> List[str]:
    parent = get_parent_commit(repo, commit_sha)
    out = _run_git(repo, ["diff", "--name-only", f"{parent}..{commit_sha}"])
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    files = sorted(set(files))
    return files


def churn_map(repo: Path, commit_sha: str) -> Dict[str, FileChurn]:
    items = diff_numstat(repo, commit_sha)
    return {c.path: c for c in items}
```

---

### `signalforge/features/deps_graph.py`

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


# Very lightweight import regexes (v1)
PY_IMPORT_RE = re.compile(r"^\s*(?:from\s+([a-zA-Z0-9_\.]+)\s+import|import\s+([a-zA-Z0-9_\.]+))")
TS_IMPORT_RE = re.compile(r"^\s*import\s+(?:.+\s+from\s+)?['\"]([^'\"]+)['\"];?")


@dataclass(frozen=True)
class DepGraph:
    nodes: List[str]  # file paths
    edges: List[Tuple[str, str]]  # (src -> dst)

    def degrees(self) -> Dict[str, Tuple[int, int]]:
        """Return {node: (out_degree, in_degree)}."""
        out_d: Dict[str, int] = {n: 0 for n in self.nodes}
        in_d: Dict[str, int] = {n: 0 for n in self.nodes}
        for s, d in self.edges:
            if s in out_d:
                out_d[s] += 1
            if d in in_d:
                in_d[d] += 1
        return {n: (out_d[n], in_d[n]) for n in self.nodes}


def _iter_source_files(repo: Path) -> List[Path]:
    exts = {".py", ".ts", ".tsx", ".js", ".jsx"}
    files: List[Path] = []
    for p in repo.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in exts:
            files.append(p)
    files.sort()
    return files


def _normalize_rel(repo: Path, path: Path) -> str:
    return path.relative_to(repo).as_posix()


def build_import_graph(repo: Path) -> DepGraph:
    """Build a lightweight file-level graph: if file A imports module/file B, add edge A->B.

    v1 approach:
    - For Python: only consider absolute module names and map to files by suffix matching (best-effort).
    - For TS/JS: resolve relative imports starting with './' or '../' to files.

    Determinism:
    - nodes and edges are sorted.
    """

    files = _iter_source_files(repo)
    nodes = [_normalize_rel(repo, p) for p in files]
    node_set = set(nodes)

    # simple lookup maps
    py_module_to_files: Dict[str, List[str]] = {}
    for n in nodes:
        if n.endswith(".py"):
            # module name by stripping .py and converting / to .
            mod = n[:-3].replace("/", ".")
            py_module_to_files.setdefault(mod, []).append(n)

    edges: Set[Tuple[str, str]] = set()

    for fp in files:
        rel = _normalize_rel(repo, fp)
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for line in text.splitlines():
            # Python
            m = PY_IMPORT_RE.match(line)
            if m and fp.suffix.lower() == ".py":
                mod = m.group(1) or m.group(2)
                if not mod:
                    continue
                # map module to file(s) best-effort
                for cand in (py_module_to_files.get(mod, []) + py_module_to_files.get(mod + ".__init__", [])):
                    if cand in node_set and cand != rel:
                        edges.add((rel, cand))
                continue

            # TS/JS
            m2 = TS_IMPORT_RE.match(line)
            if m2 and fp.suffix.lower() in {".ts", ".tsx", ".js", ".jsx"}:
                spec = m2.group(1)
                if not spec:
                    continue
                if spec.startswith("./") or spec.startswith("../"):
                    target = (fp.parent / spec).resolve()
                    # try common extensions
                    candidates = []
                    if target.suffix:
                        candidates.append(target)
                    else:
                        for ext in [".ts", ".tsx", ".js", ".jsx"]:
                            candidates.append(Path(str(target) + ext))
                        # index files
                        for ext in [".ts", ".tsx", ".js", ".jsx"]:
                            candidates.append(target / ("index" + ext))

                    for cand in candidates:
                        if cand.exists() and cand.is_file():
                            rel_c = _normalize_rel(repo, cand)
                            if rel_c in node_set and rel_c != rel:
                                edges.add((rel, rel_c))
                            break

    edge_list = sorted(edges)
    return DepGraph(nodes=nodes, edges=edge_list)


def centrality_scores(graph: DepGraph) -> Dict[str, float]:
    """Compute a simple centrality proxy: out_degree + in_degree, normalized to [0,1]."""
    deg = graph.degrees()
    raw: Dict[str, float] = {}
    for n, (out_d, in_d) in deg.items():
        raw[n] = float(out_d + in_d)

    if not raw:
        return {}

    mn = min(raw.values())
    mx = max(raw.values())
    if mx == mn:
        return {k: 0.0 for k in raw.keys()}

    return {k: (v - mn) / (mx - mn) for k, v in raw.items()}
```

---

### `signalforge/models/structural_risk.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from signalforge.config import SignalForgeConfig
from signalforge.features.churn import churn_map, changed_files
from signalforge.features.deps_graph import build_import_graph, centrality_scores


@dataclass(frozen=True)
class RiskTarget:
    target_id: str
    path: str
    risk_raw: float
    risk_norm: float
    components: Dict[str, float]


def _normalize(values: Dict[str, float]) -> Dict[str, float]:
    if not values:
        return {}
    mn = min(values.values())
    mx = max(values.values())
    if mx == mn:
        return {k: 0.0 for k in values}
    return {k: (v - mn) / (mx - mn) for k, v in values.items()}


def compute_risk_heatmap(repo: Path, commit_sha: str, cfg: SignalForgeConfig) -> dict:
    """Compute risk_heatmap.json artifact."""
    # Targets = changed files
    files = changed_files(repo, commit_sha)
    churn = churn_map(repo, commit_sha)

    # Dependency centrality over full repo sources
    graph = build_import_graph(repo)
    cent = centrality_scores(graph)

    # Churn component raw values
    churn_raw: Dict[str, float] = {}
    for f in files:
        c = churn.get(f)
        churn_raw[f] = float(c.total) if c else 0.0

    churn_norm = _normalize(churn_raw)

    # Deps component per file (centrality proxy from full graph)
    deps_raw = {f: float(cent.get(f, 0.0)) for f in files}
    deps_norm = _normalize(deps_raw)

    # tests/violations/history v1 defaults
    tests_norm = {f: 0.0 for f in files}
    viol_norm = {f: 0.0 for f in files}
    hist_norm = {f: 0.0 for f in files}

    risk_raw: Dict[str, float] = {}
    for f in files:
        risk_raw[f] = (
            cfg.w_churn * churn_norm.get(f, 0.0)
            + cfg.w_deps * deps_norm.get(f, 0.0)
            + cfg.w_tests * tests_norm.get(f, 0.0)
            + cfg.w_violations * viol_norm.get(f, 0.0)
            + cfg.w_history * hist_norm.get(f, 0.0)
        )

    risk_norm = _normalize(risk_raw)

    targets: List[dict] = []
    for f in sorted(files):
        targets.append(
            {
                "target_id": f,
                "path": f,
                "risk_raw": float(risk_raw.get(f, 0.0)),
                "risk_norm": float(risk_norm.get(f, 0.0)),
                "components": {
                    "churn": float(churn_norm.get(f, 0.0)),
                    "deps": float(deps_norm.get(f, 0.0)),
                    "tests": float(tests_norm.get(f, 0.0)),
                    "violations": float(viol_norm.get(f, 0.0)),
                    "history": float(hist_norm.get(f, 0.0)),
                },
            }
        )

    return {
        "schema_version": "v1",
        "kind": "risk_heatmap",
        "run_id": "__RUN_ID__",  # injected by pipeline
        "commit_sha": commit_sha,
        "generated_at": "__GENERATED_AT__",  # injected by pipeline
        "weights": {
            "w_churn": cfg.w_churn,
            "w_deps": cfg.w_deps,
            "w_tests": cfg.w_tests,
            "w_violations": cfg.w_violations,
            "w_history": cfg.w_history,
        },
        "targets": targets,
    }
```

---

## 2) Wire Slice 01 into the runner

Update `signalforge/pipeline/run.py` from Pack A to accept a `stage_ctx` dict and implement the `risk_heatmap` stage.

### Patch: `signalforge/pipeline/run.py`

Replace your current `run_stages(...)` with the version below:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Optional
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
    stages: Optional[Dict[str, Callable[[], dict]]] = None,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stages = stages or {}

    for kind in STAGE_ORDER:
        try:
            obj = stages.get(kind, lambda k=kind: placeholder_artifact(k, run_id, commit_sha))()
            # inject standard fields if stage used placeholders
            obj["run_id"] = run_id
            obj["commit_sha"] = commit_sha
            obj["kind"] = kind
            obj.setdefault("schema_version", "v1")
            obj["generated_at"] = _utc_now_iso()

            schema = load_schema(schema_dir, kind)
            validate_artifact(schema, obj, kind=kind)

            (out_dir / f"{kind}.json").write_text(
                json.dumps(obj, indent=2, sort_keys=True),
                encoding="utf-8",
            )
        except Exception as e:
            raise StageError(f"Stage failed: {kind}: {e}") from e
```

Now update `signalforge/cli.py` to pass a real `risk_heatmap` callable.

### Patch: `signalforge/cli.py` (inside `cmd_run` before calling `run_stages`)

Add:

```python
from signalforge.models.structural_risk import compute_risk_heatmap

stages = {
    "risk_heatmap": lambda: compute_risk_heatmap(repo, ctx.commit_sha, cfg),
}

run_stages(out_dir=out_dir, schema_dir=schema_dir, run_id=ctx.run_id, commit_sha=ctx.commit_sha, stages=stages)
```

And remove the old call that didn’t pass stages.

---

## 3) Tests

### `tests/fixtures/tiny_repo/` (minimal git repo)

Create a tiny fixture repo as a folder committed in tests, and in the test, initialize git and create two commits.

### `tests/test_risk_scoring.py`

```python
import subprocess
from pathlib import Path

from signalforge.config import SignalForgeConfig
from signalforge.models.structural_risk import compute_risk_heatmap


def _git(repo: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return p.stdout.strip()


def test_risk_heatmap_basic(tmp_path: Path):
    repo = tmp_path / "r"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    (repo / "a.py").write_text("import os\n\nprint('hi')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "c1")
    c1 = _git(repo, "rev-parse", "HEAD")

    # modify a.py and add b.py
    (repo / "a.py").write_text("import os\nimport sys\n\nprint('hi2')\n", encoding="utf-8")
    (repo / "b.py").write_text("from os import path\n\nprint(path)\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "c2")
    c2 = _git(repo, "rev-parse", "HEAD")

    cfg = SignalForgeConfig()
    art = compute_risk_heatmap(repo, c2, cfg)

    assert art["kind"] == "risk_heatmap"
    assert art["commit_sha"] == c2
    assert len(art["targets"]) >= 1

    # Changed files should include a.py and b.py
    paths = [t["path"] for t in art["targets"]]
    assert "a.py" in paths
    assert "b.py" in paths

    # risk_norm must be in [0,1]
    for t in art["targets"]:
        rn = t["risk_norm"]
        assert 0.0 <= rn <= 1.0
```

---

## 4) Run instructions

```bash
pytest -q

python -m signalforge.cli run --repo /path/to/a/git/repo --commit <sha> --out ./out --seed 1337
python -m signalforge.cli validate --dir ./out
cat out/risk_heatmap.json
```

---

## 5) Notes / Next

- Pack F will consume `risk_heatmap.json` + git diff hunks to produce deterministic `context_slices.json`, enforcing `max_total_lines`.
- Keep deps parsing best-effort for v1; we’ll tighten in v1.1 with language-aware parsers if needed.

