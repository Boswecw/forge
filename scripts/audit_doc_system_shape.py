#!/usr/bin/env python3
"""Audit repo-local doc/system trees against the ForgeAgents exemplar shape."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRUNE_DIRS = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".svelte-kit",
    ".venv",
    ".venv_verify",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "out",
    "playwright-report",
    "target",
    "test-results",
}

REQUIRED_DIRS = [
    "00_overview",
    "10_service-contract",
    "20_runtime",
    "30_dependencies",
    "40_governance",
    "50_operations",
    "99_appendices",
]

INDEX_REQUIRED_MARKERS = [
    "**Designation:**",
    "**Source:** `doc/system/`",
    "**Build command:** `bash doc/system/BUILD.sh`",
    "Generated artifact warning",
    "Primary output: `doc/",
    "truth classes",
]

BUILD_REQUIRED_MARKERS = [
    "set -euo pipefail",
    "DESIGNATION=",
    "REQUIRED_DIRS=",
    "validate_snapshots.sh",
    "BUILD_OK",
]

VALIDATOR_REQUIRED_MARKERS = [
    "set -euo pipefail",
    "require_contains",
    "snapshot validation",
]


def discover_repos(root: Path) -> list[Path]:
    repos: list[Path] = []
    for dirpath, dirnames, _filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in PRUNE_DIRS and not dirname.endswith(".egg-info")
        ]
        if (current / ".git").exists():
            repos.append(current)
    return sorted(set(repos), key=lambda path: str(path.relative_to(root)))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def numbered_chapters(directory: Path) -> list[str]:
    if not directory.is_dir():
        return []
    return sorted(path.name for path in directory.glob("[0-9][0-9]-*.md") if path.is_file())


def find_compiled_outputs(repo: Path) -> list[str]:
    doc = repo / "doc"
    if not doc.is_dir():
        return []
    outputs = []
    for path in doc.glob("*SYSTEM.md"):
        if path.is_file():
            outputs.append(str(path.relative_to(repo)))
    return sorted(outputs)


def shell_build(repo: Path) -> dict[str, str]:
    cmd = ["bash", "doc/system/BUILD.sh"]
    completed = subprocess.run(
        cmd,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    return {
        "exit_code": str(completed.returncode),
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def marker_gaps(text: str, markers: list[str]) -> list[str]:
    lower = text.lower()
    gaps = []
    for marker in markers:
        haystack = lower if marker == "truth classes" else text
        needle = marker.lower() if marker == "truth classes" else marker
        if needle not in haystack:
            gaps.append(marker)
    return gaps


def audit_repo(root: Path, repo: Path, run_build: bool) -> dict[str, Any]:
    rel = "." if repo == root else str(repo.relative_to(root))
    doc_system = repo / "doc" / "system"
    index = doc_system / "_index.md"
    build = doc_system / "BUILD.sh"
    validator = doc_system / "validate_snapshots.sh"

    findings: list[str] = []
    required_dir_state = {}
    if not doc_system.is_dir():
        findings.append("missing doc/system")
    if not index.is_file():
        findings.append("missing doc/system/_index.md")
    if not build.is_file():
        findings.append("missing doc/system/BUILD.sh")
    if not validator.is_file():
        findings.append("missing doc/system/validate_snapshots.sh")

    for dirname in REQUIRED_DIRS:
        chapters = numbered_chapters(doc_system / dirname)
        required_dir_state[dirname] = chapters
        if not chapters:
            findings.append(f"missing numbered chapters in {dirname}")

    index_gaps: list[str] = []
    build_gaps: list[str] = []
    validator_gaps: list[str] = []
    if index.is_file():
        index_gaps = marker_gaps(read_text(index), INDEX_REQUIRED_MARKERS)
        findings.extend(f"_index.md missing marker: {gap}" for gap in index_gaps)
    if build.is_file():
        build_gaps = marker_gaps(read_text(build), BUILD_REQUIRED_MARKERS)
        findings.extend(f"BUILD.sh missing marker: {gap}" for gap in build_gaps)
    if validator.is_file():
        validator_gaps = marker_gaps(read_text(validator), VALIDATOR_REQUIRED_MARKERS)
        findings.extend(f"validate_snapshots.sh missing marker: {gap}" for gap in validator_gaps)

    compiled_outputs = find_compiled_outputs(repo)
    if not compiled_outputs:
        findings.append("missing designation-bound doc/*SYSTEM.md compiled output")

    build_result = None
    if run_build and build.is_file():
        try:
            build_result = shell_build(repo)
            if build_result["exit_code"] != "0":
                findings.append("BUILD.sh failed")
        except subprocess.TimeoutExpired:
            build_result = {"exit_code": "timeout", "stdout": "", "stderr": "timed out after 30s"}
            findings.append("BUILD.sh timed out")

    status = "aligned" if not findings else "needs_update"
    return {
        "relative_path": rel,
        "name": repo.name,
        "status": status,
        "findings": findings,
        "doc_system": str(doc_system.relative_to(repo)) if doc_system.exists() else "",
        "compiled_outputs": compiled_outputs,
        "required_dirs": required_dir_state,
        "marker_gaps": {
            "index": index_gaps,
            "build": build_gaps,
            "validator": validator_gaps,
        },
        "build_result": build_result,
    }


def build_payload(root: Path, exemplar: Path, run_build: bool) -> dict[str, Any]:
    repos = [audit_repo(root, repo, run_build) for repo in discover_repos(root)]
    statuses = Counter(repo["status"] for repo in repos)
    exemplar_rel = str(exemplar.resolve().relative_to(root.resolve()))
    exemplar_entry = next((repo for repo in repos if repo["relative_path"] == exemplar_rel), None)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(root),
        "exemplar": exemplar_rel,
        "exemplar_is_aligned": exemplar_entry is not None and exemplar_entry["status"] == "aligned",
        "standard": {
            "required_dirs": REQUIRED_DIRS,
            "index_required_markers": INDEX_REQUIRED_MARKERS,
            "build_required_markers": BUILD_REQUIRED_MARKERS,
            "validator_required_markers": VALIDATOR_REQUIRED_MARKERS,
        },
        "summary": {
            "total": len(repos),
            "statuses": dict(sorted(statuses.items())),
        },
        "repositories": repos,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# doc/system Shape Audit",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Root: `{payload['root']}`",
        f"Exemplar: `{payload['exemplar']}`",
        f"Exemplar aligned: `{str(payload['exemplar_is_aligned']).lower()}`",
        "",
        "ForgeAgents is treated as a structural exemplar, not a content template. Repo-specific truth must stay repo-specific.",
        "",
        "## Exemplar Decision",
        "",
        "ForgeAgents is an acceptable example for the ecosystem `doc/system` shape because it has:",
        "",
        "- a modular `doc/system/` source tree",
        "- designation-bound compiled output under `doc/FORSYSTEM.md`",
        "- a generated-artifact warning in `_index.md`",
        "- explicit truth-class language",
        "- fail-closed `BUILD.sh` assembly",
        "- `validate_snapshots.sh` validation wired into the build",
        "- the seven canonical section folders used by the current compliant repos",
        "",
        "## Summary",
        "",
        f"- Total repositories discovered: `{payload['summary']['total']}`",
    ]
    for status, count in payload["summary"]["statuses"].items():
        lines.append(f"- {status}: `{count}`")
    aligned = [
        repo["relative_path"]
        for repo in payload["repositories"]
        if repo["status"] == "aligned"
    ]
    lines.append(f"- aligned repositories: {', '.join(f'`{repo}`' for repo in aligned)}")
    lines.extend(
        [
            "",
            "## Standard Checked",
            "",
        ]
    )
    for dirname in payload["standard"]["required_dirs"]:
        lines.append(f"- `doc/system/{dirname}/` with numbered markdown chapters")
    lines.extend(
        [
            "- `doc/system/_index.md` with designation, source, build command, primary output, generated-artifact warning, and truth-class language",
            "- `doc/system/BUILD.sh` with fail-closed assembly and validation",
            "- `doc/system/validate_snapshots.sh` with explicit snapshot markers",
            "- designation-bound compiled output under `doc/*SYSTEM.md`",
            "",
            "## Repository Results",
            "",
            "| Status | Repository | Compiled outputs | Findings |",
            "|---|---|---|---|",
        ]
    )
    for repo in payload["repositories"]:
        outputs = ", ".join(f"`{output}`" for output in repo["compiled_outputs"]) or "none"
        findings = "<br>".join(repo["findings"]) if repo["findings"] else "aligned with exemplar shape"
        lines.append(f"| {repo['status']} | `{repo['relative_path']}` | {outputs} | {findings} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--exemplar", type=Path, default=Path("cloud-systems/ForgeAgents"))
    parser.add_argument("--json", type=Path, help="write JSON report")
    parser.add_argument("--markdown", type=Path, help="write Markdown report")
    parser.add_argument("--run-build", action="store_true", help="also run doc/system/BUILD.sh where present")
    parser.add_argument("--strict", action="store_true", help="exit non-zero if any repo needs update")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    exemplar = (root / args.exemplar).resolve() if not args.exemplar.is_absolute() else args.exemplar.resolve()
    payload = build_payload(root, exemplar, args.run_build)
    if args.json:
        write_json(args.json, payload)
    if args.markdown:
        write_markdown(args.markdown, payload)
    if not args.json and not args.markdown:
        print(json.dumps(payload, indent=2, sort_keys=True))
    if args.strict and payload["summary"]["statuses"].get("needs_update", 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
