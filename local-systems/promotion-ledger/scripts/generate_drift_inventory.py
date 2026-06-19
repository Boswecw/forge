#!/usr/bin/env python3
"""Generate conservative drift reports for Forge promotion repo pairs."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependent
    print(f"FAIL: PyYAML is required to load registry YAML: {exc}", file=sys.stderr)
    sys.exit(2)


LEDGER_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = LEDGER_ROOT / "repo-registry.yaml"
REPORT_DIR = LEDGER_ROOT / "drift-reports"
RESOLUTION_DIR = LEDGER_ROOT / "resolutions"

CLASSIFICATIONS = [
    "same",
    "intentional_app_support_adaptation",
    "source_local_hold",
    "missing_from_target",
    "target_only_glue",
    "dangerous_drift",
    "unknown",
]

RESOLUTION_SHAPES = {
    "source_only",
    "target_only",
    "modified_in_both",
}

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
}

IGNORED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".swp",
    ".tmp",
}


def run_git(repo: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip() or "unknown"


def git_branch(repo: Path) -> str:
    return run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])


def git_commit(repo: Path) -> str:
    return run_git(repo, ["rev-parse", "HEAD"])


def should_ignore(path: Path) -> bool:
    if any(part in IGNORED_DIRS for part in path.parts):
        return True
    if path.suffix in IGNORED_SUFFIXES:
        return True
    return False


def inventory(repo: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in repo.rglob("*"):
        rel = path.relative_to(repo)
        if should_ignore(rel):
            continue
        if not path.is_file():
            continue
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            continue
        files[rel.as_posix()] = digest
    return files


def make_item(
    path: str,
    classification: str,
    justification: str,
    source_commit: str,
    target_commit: str,
    recommended_action: str,
) -> dict[str, Any]:
    return {
        "path": path,
        "classification": classification,
        "justification": justification,
        "source_commit": source_commit,
        "target_commit": target_commit,
        "recommended_action": recommended_action,
    }


def resolution_source(path: Path) -> str:
    try:
        return path.relative_to(LEDGER_ROOT).as_posix()
    except ValueError:
        return str(path)


def resolution_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    if path.is_file():
        return [path]
    files = list(path.glob("*.yaml"))
    files.extend(path.glob("*.yml"))
    return sorted(files)


def load_resolutions(path: Path) -> dict[tuple[str, str, str], dict[str, Any]]:
    resolutions: dict[tuple[str, str, str], dict[str, Any]] = {}
    for file_path in resolution_files(path):
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError(f"resolution file must be a mapping: {file_path}")
        entries = data.get("resolutions", [])
        if not isinstance(entries, list):
            raise ValueError(f"resolutions must be a list: {file_path}")
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                raise ValueError(f"resolution entry {index} must be a mapping: {file_path}")
            missing = [
                field
                for field in ("resolution_id", "repo_pair", "shape", "classification")
                if not entry.get(field)
            ]
            if missing:
                raise ValueError(
                    f"resolution entry {index} missing required fields {missing}: {file_path}"
                )
            if entry.get("path") and entry.get("paths"):
                raise ValueError(
                    f"resolution entry {index} must use either path or paths, not both: "
                    f"{file_path}"
                )
            if entry.get("path"):
                paths = [entry["path"]]
            else:
                paths = entry.get("paths", [])
            if (
                not isinstance(paths, list)
                or not paths
                or any(not isinstance(path, str) or not path for path in paths)
            ):
                raise ValueError(
                    f"resolution entry {index} must provide path or non-empty paths: "
                    f"{file_path}"
                )
            classification = entry["classification"]
            if classification not in CLASSIFICATIONS or classification == "same":
                raise ValueError(
                    f"resolution {entry['resolution_id']} has invalid classification: "
                    f"{classification}"
                )
            shape = entry["shape"]
            if shape not in RESOLUTION_SHAPES:
                raise ValueError(
                    f"resolution {entry['resolution_id']} has invalid shape: {shape}"
                )
            for resolved_path in paths:
                key = (entry["repo_pair"], resolved_path, shape)
                if key in resolutions:
                    raise ValueError(f"duplicate resolution for {key}: {file_path}")
                stored = dict(entry)
                stored["path"] = resolved_path
                stored.pop("paths", None)
                stored["_resolution_source"] = resolution_source(file_path)
                resolutions[key] = stored
    return resolutions


def resolved_item(
    resolutions: dict[tuple[str, str, str], dict[str, Any]],
    repo_pair: str,
    path: str,
    shape: str,
    default_classification: str,
    default_justification: str,
    source_commit: str,
    target_commit: str,
    default_recommended_action: str,
) -> dict[str, Any]:
    resolution = resolutions.get((repo_pair, path, shape))
    if resolution is None:
        return make_item(
            path,
            default_classification,
            default_justification,
            source_commit,
            target_commit,
            default_recommended_action,
        )

    item = make_item(
        path,
        resolution["classification"],
        resolution.get("justification", default_justification),
        source_commit,
        target_commit,
        resolution.get("recommended_action", default_recommended_action),
    )
    item["resolution_id"] = resolution["resolution_id"]
    item["resolved_shape"] = shape
    item["resolution_source"] = resolution["_resolution_source"]
    if "evidence" in resolution:
        item["resolution_evidence"] = resolution["evidence"]
    return item


def add_drift_item(
    items: list[dict[str, Any]],
    counts: Counter[str],
    resolutions: dict[tuple[str, str, str], dict[str, Any]],
    repo_pair: str,
    path: str,
    shape: str,
    default_classification: str,
    default_justification: str,
    source_commit: str,
    target_commit: str,
    default_recommended_action: str,
) -> None:
    item = resolved_item(
        resolutions,
        repo_pair,
        path,
        shape,
        default_classification,
        default_justification,
        source_commit,
        target_commit,
        default_recommended_action,
    )
    counts[item["classification"]] += 1
    items.append(item)


def compare_pair(
    pair: dict[str, Any],
    generated_at: str,
    resolutions: dict[tuple[str, str, str], dict[str, Any]],
) -> dict[str, Any]:
    source_repo = Path(pair["source_repo"])
    target_repo = Path(pair["target_repo"])
    if not source_repo.exists():
        raise FileNotFoundError(f"source repo does not exist: {source_repo}")
    if not target_repo.exists():
        raise FileNotFoundError(f"target repo does not exist: {target_repo}")

    source_commit = git_commit(source_repo)
    target_commit = git_commit(target_repo)
    source_files = inventory(source_repo)
    target_files = inventory(target_repo)
    all_paths = sorted(set(source_files) | set(target_files))
    pair_name = pair["repo_pair"]

    counts: Counter[str] = Counter({classification: 0 for classification in CLASSIFICATIONS})
    items: list[dict[str, Any]] = []

    for path in all_paths:
        in_source = path in source_files
        in_target = path in target_files
        if in_source and in_target and source_files[path] == target_files[path]:
            counts["same"] += 1
            continue
        if in_source and not in_target:
            add_drift_item(
                items,
                counts,
                resolutions,
                pair_name,
                path,
                "source_only",
                "missing_from_target",
                "Source artifact exists in the proving repo but is absent from the app-support target.",
                source_commit,
                target_commit,
                "Review whether this source artifact should be promoted or intentionally excluded.",
            )
            continue
        if in_target and not in_source:
            add_drift_item(
                items,
                counts,
                resolutions,
                pair_name,
                path,
                "target_only",
                "unknown",
                "Target-only artifact requires human classification before promotion.",
                source_commit,
                target_commit,
                "Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo.",
            )
            continue

        add_drift_item(
            items,
            counts,
            resolutions,
            pair_name,
            path,
            "modified_in_both",
            "unknown",
            "Artifact exists in both repos but content differs. Slice 00 does not infer intent.",
            source_commit,
            target_commit,
            "Compare source and target intent; resolve by human decision, backport, or explicit exception.",
        )

    return {
        "repo_pair": pair_name,
        "source_repo": str(source_repo),
        "target_repo": str(target_repo),
        "source_branch": git_branch(source_repo),
        "target_branch": git_branch(target_repo),
        "source_commit": source_commit,
        "target_commit": target_commit,
        "generated_at": generated_at,
        "classification_summary": {key: int(counts[key]) for key in CLASSIFICATIONS},
        "resolutions_applied": sum(1 for item in items if "resolution_id" in item),
        "items": items,
    }


def write_yaml(report: dict[str, Any], path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing report: {path}")
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(report, handle, sort_keys=False, allow_unicode=False)


def write_markdown(report: dict[str, Any], path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing report: {path}")
    summary = report["classification_summary"]
    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"# Drift Report: {report['repo_pair']}\n\n")
        handle.write(f"Generated: `{report['generated_at']}`\n\n")
        handle.write(f"Source repo: `{report['source_repo']}`\n")
        handle.write(f"Source branch: `{report['source_branch']}`\n")
        handle.write(f"Source commit: `{report['source_commit']}`\n\n")
        handle.write(f"Target repo: `{report['target_repo']}`\n")
        handle.write(f"Target branch: `{report['target_branch']}`\n")
        handle.write(f"Target commit: `{report['target_commit']}`\n\n")
        handle.write(f"Resolutions applied: `{report.get('resolutions_applied', 0)}`\n\n")
        handle.write("## Classification Summary\n\n")
        handle.write("| Classification | Count |\n")
        handle.write("| --- | ---: |\n")
        for classification in CLASSIFICATIONS:
            handle.write(f"| {classification} | {summary[classification]} |\n")
        handle.write("\n## Items\n\n")
        if not report["items"]:
            handle.write("No differing items found.\n")
        else:
            handle.write("| Path | Classification | Resolution | Recommended action |\n")
            handle.write("| --- | --- | --- | --- |\n")
            for item in report["items"]:
                resolution = item.get("resolution_id", "")
                resolution_cell = f"`{resolution}`" if resolution else ""
                handle.write(
                    f"| `{item['path']}` | {item['classification']} | "
                    f"{resolution_cell} | {item['recommended_action']} |\n"
                )
        handle.write("\n## Blocking Rule\n\n")
        handle.write(
            "Dangerous drift and unknown drift block promotion until resolved by "
            "human decision, backport, or explicit exception.\n"
        )
        handle.write("\n## Documentation Placement Rule\n\n")
        handle.write("- Documentation belongs in `/docs`.\n")
        handle.write(
            "- Inactive plans should be condensed to status, decision, evidence, "
            "and next action.\n"
        )
        handle.write(
            "- `/doc/system` is the canonical code mirror. Treat `/doc/system` "
            "drift as mirror drift to verify against live code and repo-local "
            "build outputs, not as general documentation promotion.\n"
        )


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("repo_pairs"), list):
        raise ValueError("repo-registry.yaml must contain a repo_pairs list")
    return data


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default=str(REGISTRY_PATH))
    parser.add_argument("--out-dir", default=str(REPORT_DIR))
    parser.add_argument("--resolutions-dir", default=str(RESOLUTION_DIR))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv[1:])

    registry_path = Path(args.registry)
    out_dir = Path(args.out_dir)
    resolutions_path = Path(args.resolutions_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        registry = load_registry(registry_path)
        resolutions = load_resolutions(resolutions_path)
    except Exception as exc:
        print(f"FAIL: could not load registry or resolutions: {exc}", file=sys.stderr)
        return 2

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    written: list[Path] = []
    try:
        for pair in registry["repo_pairs"]:
            report = compare_pair(pair, generated_at, resolutions)
            stem = pair["repo_pair"]
            yaml_path = out_dir / f"{stem}.drift.yaml"
            md_path = out_dir / f"{stem}.md"
            write_yaml(report, yaml_path, args.overwrite)
            write_markdown(report, md_path, args.overwrite)
            written.extend([yaml_path, md_path])
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: generated drift inventory")
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
