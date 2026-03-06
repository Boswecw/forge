#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from doc_registry import REGISTRY_PATH, ROOT, DocumentationRegistry, DocumentationSurface, load_registry, registry_payload


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
}
ROOT_GOVERNANCE_PREFIXES = (
    "README.md",
    "doc/",
    "docs/",
    "scripts/",
    ".github/workflows/",
)
FULL_AUDIT_TRIGGER_PATHS = {
    "docs/canonical/documentation_protocol_v1.md",
    "docs/canonical/documentation_registry_v1.json",
    "scripts/check-documentation-protocol.py",
    "scripts/doc-audit",
    "scripts/doc-audit.py",
    "scripts/doc_registry.py",
    ".github/workflows/documentation_protocol.yml",
}
FULL_AUDIT_TRIGGER_PREFIXES = (
    "docs/canonical/",
    "scripts/",
    ".github/workflows/",
)


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_path(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover_git_repositories(root: Path) -> list[str]:
    discovered: list[str] = []
    for current_root, dirs, _files in os.walk(root, topdown=True):
        current = Path(current_root)
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS or name == ".git"]
        if ".git" in dirs:
            rel = current.relative_to(root)
            discovered.append(rel.as_posix() if rel != Path(".") else ".")
            dirs.remove(".git")
    return sorted(discovered)


def discover_git_submodules(root: Path) -> list[dict[str, str]]:
    submodules: list[dict[str, str]] = []
    for gitmodules in sorted(root.glob("**/.gitmodules")):
        for line in gitmodules.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("path = "):
                submodules.append(
                    {
                        "gitmodules_path": gitmodules.relative_to(root).as_posix(),
                        "path": line.split("=", 1)[1].strip(),
                    }
                )
    return submodules


def source_files_for_surface(surface: DocumentationSurface) -> list[Path]:
    if not surface.requires_doc_system:
        return []
    files = [surface.index_path, surface.build_path]
    files.extend(sorted(surface.doc_system_dir.glob("[0-9][0-9]-*.md")))
    return [path for path in files if path.exists()]


def normalize_changed_path(raw_path: str) -> str | None:
    candidate = Path(raw_path.strip())
    if not raw_path.strip():
        return None
    if candidate.is_absolute():
        try:
            candidate = candidate.relative_to(ROOT)
        except ValueError:
            return None
    normalized = candidate.as_posix().lstrip("./")
    return normalized or None


def parse_changed_paths_file(path: Path) -> list[str]:
    return [item for item in (normalize_changed_path(line) for line in path.read_text(encoding="utf-8").splitlines()) if item]


def parse_git_status_paths(stdout: str) -> list[str]:
    changed: list[str] = []
    for line in stdout.splitlines():
        if not line:
            continue
        if len(line) < 4:
            continue
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        normalized = normalize_changed_path(payload)
        if normalized:
            changed.append(normalized)
    return changed


def auto_discovered_changed_paths(registry: DocumentationRegistry) -> list[str]:
    discovered: list[str] = []
    for surface in registry.surfaces:
        if not (surface.root / ".git").exists():
            continue
        result = subprocess.run(
            ["git", "-C", str(surface.root), "status", "--porcelain=1", "--untracked-files=all"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            continue
        for rel_path in parse_git_status_paths(result.stdout):
            discovered.append((surface.path / rel_path).as_posix())
    return sorted(set(discovered))


def surface_matches_path(surface: DocumentationSurface, rel_path: str) -> bool:
    if surface.path == Path("."):
        if rel_path == "README.md":
            return True
        return any(rel_path.startswith(prefix) for prefix in ROOT_GOVERNANCE_PREFIXES if prefix.endswith("/"))

    prefix = surface.path.as_posix()
    return rel_path == prefix or rel_path.startswith(prefix + "/")


def surface_scope_description(surface: DocumentationSurface) -> str:
    return f"{surface.repo_id} ({surface.path.as_posix()})"


def selected_surfaces(
    registry: DocumentationRegistry,
    changed_only: bool,
    changed_paths: list[str],
) -> tuple[list[DocumentationSurface], dict[str, Any]]:
    metadata: dict[str, Any] = {
        "mode": "all-surfaces",
        "changed_paths": changed_paths,
        "selected_repo_ids": [surface.repo_id for surface in registry.surfaces],
        "global_trigger": False,
        "global_trigger_paths": [],
    }
    if not changed_only:
        return list(registry.surfaces), metadata

    global_trigger_paths = [
        path
        for path in changed_paths
        if path in FULL_AUDIT_TRIGGER_PATHS or any(path.startswith(prefix) for prefix in FULL_AUDIT_TRIGGER_PREFIXES)
    ]
    if global_trigger_paths:
        metadata.update(
            {
                "mode": "changed-only-escalated-to-full",
                "global_trigger": True,
                "global_trigger_paths": global_trigger_paths,
            }
        )
        return list(registry.surfaces), metadata

    matched: list[DocumentationSurface] = []
    for surface in registry.surfaces:
        if any(surface_matches_path(surface, rel_path) for rel_path in changed_paths):
            matched.append(surface)

    metadata.update(
        {
            "mode": "changed-only",
            "selected_repo_ids": [surface.repo_id for surface in matched],
        }
    )
    return matched, metadata


def build_diff_preview(before_text: str, after_text: str, *, max_lines: int = 20) -> list[str]:
    diff_lines = list(
        difflib.unified_diff(
            before_text.splitlines(),
            after_text.splitlines(),
            fromfile="before",
            tofile="after",
            n=1,
            lineterm="",
        )
    )
    return diff_lines[:max_lines]


def stale_info(surface: DocumentationSurface) -> dict[str, Any]:
    output = surface.assembled_path
    sources = source_files_for_surface(surface)
    payload: dict[str, Any] = {
        "repo_id": surface.repo_id,
        "path": surface.path.as_posix(),
        "output": None if output is None else output.relative_to(ROOT).as_posix(),
        "source_count": len(sources),
        "source_files": [source.relative_to(ROOT).as_posix() for source in sources],
        "stale_sources": [],
        "missing_output": output is None or not output.exists(),
        "stale_by_mtime": False,
        "pre_build_hash": sha256_path(output),
        "post_build_hash": None,
        "changed_after_build": False,
        "diff_preview": [],
        "hint": None,
        "build_command": f"bash {surface.build_path.relative_to(ROOT).as_posix()}",
    }
    if output is None or not sources:
        if output is None:
            payload["hint"] = "Registry entry requires doc/system freshness checks but assembled output path is empty."
        return payload

    if not output.exists():
        payload["hint"] = f"Assembled artifact is missing. Rebuild with `{payload['build_command']}`."
        return payload

    output_mtime = output.stat().st_mtime
    stale_sources = [source.relative_to(ROOT).as_posix() for source in sources if source.stat().st_mtime > output_mtime]
    payload["stale_sources"] = stale_sources
    payload["stale_by_mtime"] = bool(stale_sources)
    if stale_sources:
        preview = ", ".join(stale_sources[:3])
        suffix = "" if len(stale_sources) <= 3 else f" (+{len(stale_sources) - 3} more)"
        payload["hint"] = (
            f"Assembled artifact is older than source docs. Rebuild with `{payload['build_command']}`; newer sources: {preview}{suffix}."
        )
    return payload


def run_build(surface: DocumentationSurface) -> dict[str, Any]:
    output = surface.assembled_path
    before_text = "" if output is None or not output.exists() else output.read_text(encoding="utf-8")
    result = subprocess.run(
        ["bash", str(surface.build_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    after_text = "" if output is None or not output.exists() else output.read_text(encoding="utf-8")
    return {
        "repo_id": surface.repo_id,
        "build_path": surface.build_path.relative_to(ROOT).as_posix(),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "before_text": before_text,
        "after_text": after_text,
    }


def run_protocol_checker(expected_report_date: str | None, surface_ids: Iterable[str]) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile(prefix="doc-protocol-", suffix=".json", delete=False) as handle:
        json_path = Path(handle.name)

    cmd = [
        "python3",
        str(ROOT / "scripts" / "check-documentation-protocol.py"),
        "--json-out",
        str(json_path),
    ]
    if expected_report_date:
        cmd.extend(["--expected-report-date", expected_report_date])
    for surface_id in surface_ids:
        cmd.extend(["--surface", surface_id])

    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    json_path.unlink(missing_ok=True)
    payload["returncode"] = result.returncode
    payload["stdout"] = result.stdout
    payload["stderr"] = result.stderr
    return payload


def build_markdown_report(payload: dict[str, Any]) -> str:
    lines = [
        f"# Documentation Audit Report — {payload['metadata']['generated_at'][:10]}",
        "",
        "## Audit Metadata",
        "",
        f"- Mode: `{'strict' if payload['metadata']['strict'] else 'standard'}`",
        f"- Builds run: `{'yes' if payload['metadata']['run_builds'] else 'no'}`",
        f"- Discover only: `{'yes' if payload['metadata']['discover_only'] else 'no'}`",
        f"- Changed only: `{'yes' if payload['metadata']['changed_only'] else 'no'}`",
        f"- Registry: `{payload['metadata']['registry_path']}`",
        f"- Scope mode: `{payload['selection']['mode']}`",
        "",
        "## Scope",
        "",
        f"- Selected surfaces: `{len(payload['selection']['selected_repo_ids'])}`",
    ]

    if payload["selection"]["selected_repo_ids"]:
        for repo_id in payload["selection"]["selected_repo_ids"]:
            lines.append(f"- `{repo_id}`")
    else:
        lines.append("- None")

    if payload["selection"]["changed_paths"]:
        lines.extend(["", "## Changed Paths", ""])
        for path in payload["selection"]["changed_paths"]:
            lines.append(f"- `{path}`")

    lines.extend(
        [
            "",
            "## Registry Status",
            "",
            f"- Surfaces tracked: `{payload['registry']['surface_count']}`",
            f"- Protocol spec: `{payload['registry']['protocol_spec']}`",
            "",
            "## Repo Inventory Comparison",
            "",
            f"- Discovered nested repos: `{len(payload['discovery']['nested_git_repos'])}`",
            f"- Unregistered nested repos: `{len(payload['discovery']['unregistered_nested_git_repos'])}`",
            f"- Git submodules discovered: `{len(payload['discovery']['git_submodules'])}`",
            "",
            "## Protocol Check Summary",
            "",
            f"- Passed: `{payload['checker']['summary']['passed']}`",
            f"- Warnings: `{payload['checker']['summary']['warnings']}`",
            f"- Errors: `{payload['checker']['summary']['errors']}`",
            "",
            "## Builder Verification",
            "",
            f"- Builds attempted: `{len(payload['builders'])}`",
            f"- Build failures: `{sum(1 for item in payload['builders'] if item['returncode'] != 0)}`",
            "",
            "## Assembled Artifact Freshness",
            "",
            f"- Surfaces with stale outputs: `{len(payload['freshness']['stale_or_changed'])}`",
            f"- Surfaces with missing outputs: `{len(payload['freshness']['missing_outputs'])}`",
        ]
    )

    if payload["freshness"]["stale_or_changed"] or payload["freshness"]["missing_outputs"]:
        lines.extend(["", "### Freshness Hints", ""])
        for entry in payload["freshness"]["entries"]:
            if entry["repo_id"] in payload["freshness"]["stale_or_changed"] or entry["repo_id"] in payload["freshness"]["missing_outputs"]:
                lines.append(f"- `{entry['repo_id']}`: {entry['hint']}")
                for diff_line in entry["diff_preview"][:6]:
                    lines.append(f"  `{diff_line}`")

    lines.extend(["", "## Unresolved Items", ""])
    if payload["summary"]["errors"]:
        for item in payload["summary"]["errors"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def scoped_surfaces_for_doc_checks(selected: list[DocumentationSurface]) -> list[DocumentationSurface]:
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Registry-driven Forge documentation audit.")
    parser.add_argument("--run-builds", action="store_true", help="Run deterministic doc/system builders for the selected scope.")
    parser.add_argument("--strict", action="store_true", help="Fail on unregistered repos, stale assembled docs, and scope mismatches.")
    parser.add_argument("--discover-only", action="store_true", help="Only perform registry and workspace discovery checks.")
    parser.add_argument("--changed-only", action="store_true", help="Scope protocol and builder checks to surfaces impacted by changed paths.")
    parser.add_argument("--changed-path", action="append", default=[], help="Explicit changed path relative to the workspace root; may be repeated.")
    parser.add_argument("--changed-paths-file", help="Read changed paths from a file, one path per line.")
    parser.add_argument("--expected-report-date", help="Pass through an expected protocol audit report date.")
    parser.add_argument("--report-out", help="Write a markdown audit report to the given path.")
    parser.add_argument("--json-out", help="Write machine-readable audit output to the given path.")
    args = parser.parse_args()

    try:
        registry = load_registry(REGISTRY_PATH)
    except Exception as exc:  # pragma: no cover - fail closed path
        print(f"FAIL unable to load documentation registry: {REGISTRY_PATH.relative_to(ROOT)} ({exc})")
        print("\nDoc-audit summary: 0 passed, 0 warnings, 1 errors")
        return 1

    explicit_changed_paths = [item for item in (normalize_changed_path(path) for path in args.changed_path) if item]
    if args.changed_paths_file:
        explicit_changed_paths.extend(parse_changed_paths_file(Path(args.changed_paths_file)))
    explicit_changed_paths = sorted(set(explicit_changed_paths))

    changed_paths = explicit_changed_paths
    changed_paths_source = "explicit"
    if args.changed_only and not changed_paths:
        changed_paths = auto_discovered_changed_paths(registry)
        changed_paths_source = "auto-git-status"

    discovered_repos = discover_git_repositories(ROOT)
    discovered_submodules = discover_git_submodules(ROOT)
    registered_repo_paths = sorted(
        surface.path.as_posix()
        for surface in registry.surfaces
        if (surface.root / ".git").exists()
    )
    unregistered_nested = sorted(set(discovered_repos) - set(registered_repo_paths))
    unregistered_submodules = sorted(
        item["path"]
        for item in discovered_submodules
        if item["path"] not in {surface.path.as_posix() for surface in registry.surfaces}
    )

    selected, selection = selected_surfaces(registry, args.changed_only, changed_paths)
    protocol_surfaces = scoped_surfaces_for_doc_checks(selected)
    doc_system_surfaces = [surface for surface in selected if surface.requires_doc_system]
    freshness = [stale_info(surface) for surface in doc_system_surfaces]
    builders: list[dict[str, Any]] = []
    messages = {"passes": [], "warnings": [], "errors": []}

    selection["changed_paths_source"] = changed_paths_source

    if unregistered_nested:
        target = "errors" if args.strict else "warnings"
        messages[target].append(f"unregistered nested git repos discovered: {', '.join(unregistered_nested)}")
    else:
        messages["passes"].append("all discovered nested git repos are registered")

    if unregistered_submodules:
        target = "errors" if args.strict else "warnings"
        messages[target].append(f"unregistered git submodules discovered: {', '.join(unregistered_submodules)}")
    else:
        messages["passes"].append("no unregistered git submodules discovered")

    if args.changed_only:
        if changed_paths:
            messages["passes"].append(
                f"changed-only mode selected {len(protocol_surfaces)} surfaces from {len(changed_paths)} changed paths ({changed_paths_source})"
            )
        else:
            target = "errors" if args.strict else "warnings"
            messages[target].append(
                "changed-only mode found no changed paths; pass --changed-path for workspace-root surfaces or use full audit mode"
            )

    if args.run_builds and not args.discover_only:
        for surface in doc_system_surfaces:
            result = run_build(surface)
            builders.append({key: value for key, value in result.items() if key not in {"before_text", "after_text"}})
            fresh_entry = next(item for item in freshness if item["repo_id"] == surface.repo_id)
            fresh_entry["post_build_hash"] = sha256_path(surface.assembled_path)
            fresh_entry["changed_after_build"] = fresh_entry["pre_build_hash"] != fresh_entry["post_build_hash"]
            if result["returncode"] != 0:
                messages["errors"].append(f"builder failed for {surface.repo_id}: {result['build_path']}")
            else:
                messages["passes"].append(f"builder succeeded for {surface.repo_id}: {result['build_path']}")
                if fresh_entry["changed_after_build"]:
                    fresh_entry["diff_preview"] = build_diff_preview(result["before_text"], result["after_text"])
                    fresh_entry["hint"] = (
                        f"Assembled artifact changed when rebuilt. Commit the rebuilt output from `{fresh_entry['build_command']}`."
                    )

    stale_or_changed: list[str] = []
    missing_outputs: list[str] = []
    for item in freshness:
        if item["missing_output"]:
            missing_outputs.append(item["repo_id"])
            target = "errors" if args.strict else "warnings"
            messages[target].append(f"assembled artifact missing for {item['repo_id']}: {item['output']} ({item['hint']})")
            continue

        if args.run_builds and item["changed_after_build"]:
            stale_or_changed.append(item["repo_id"])
            target = "errors" if args.strict else "warnings"
            messages[target].append(f"assembled artifact changed under BUILD.sh for {item['repo_id']}: {item['output']} ({item['hint']})")
        elif not args.run_builds and item["stale_by_mtime"]:
            stale_or_changed.append(item["repo_id"])
            target = "errors" if args.strict else "warnings"
            messages[target].append(f"assembled artifact appears stale for {item['repo_id']}: {item['output']} ({item['hint']})")

    checker_payload: dict[str, Any] = {
        "summary": {"passed": 0, "warnings": 0, "errors": 0},
        "passes": [],
        "warnings": [],
        "errors": [],
        "returncode": 0,
        "stdout": "",
        "stderr": "",
    }
    if not args.discover_only:
        if args.changed_only and not protocol_surfaces:
            messages["passes"].append("documentation protocol checker skipped because changed-only scope matched no surfaces")
        else:
            checker_payload = run_protocol_checker(args.expected_report_date, [surface.repo_id for surface in protocol_surfaces])
            if checker_payload["returncode"] != 0:
                messages["errors"].append("documentation protocol checker reported failures")
            else:
                scope_count = len(protocol_surfaces)
                messages["passes"].append(f"documentation protocol checker passed for {scope_count} scoped surfaces")

    payload = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "strict": args.strict,
            "run_builds": args.run_builds,
            "discover_only": args.discover_only,
            "changed_only": args.changed_only,
            "expected_report_date": args.expected_report_date,
            "registry_path": REGISTRY_PATH.relative_to(ROOT).as_posix(),
        },
        "selection": selection,
        "registry": registry_payload(registry),
        "discovery": {
            "nested_git_repos": discovered_repos,
            "registered_git_repo_paths": registered_repo_paths,
            "unregistered_nested_git_repos": unregistered_nested,
            "git_submodules": discovered_submodules,
            "unregistered_git_submodules": unregistered_submodules,
        },
        "builders": builders,
        "freshness": {
            "entries": freshness,
            "stale_or_changed": stale_or_changed,
            "missing_outputs": missing_outputs,
        },
        "checker": checker_payload,
        "summary": messages,
    }

    if args.report_out:
        report_path = Path(args.report_out)
        if not report_path.is_absolute():
            report_path = ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(build_markdown_report(payload), encoding="utf-8")
        messages["passes"].append(f"markdown report written: {display_path(report_path)}")

    if args.json_out:
        json_path = Path(args.json_out)
        if not json_path.is_absolute():
            json_path = ROOT / json_path
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        messages["passes"].append(f"machine-readable report written: {display_path(json_path)}")

    for message in messages["passes"]:
        print(f"PASS {message}")
    for message in messages["warnings"]:
        print(f"WARN {message}")
    for message in messages["errors"]:
        print(f"FAIL {message}")

    if not args.discover_only:
        print(checker_payload["stdout"], end="")
        if checker_payload["stderr"]:
            print(checker_payload["stderr"], end="")

    print(
        f"\nDoc-audit summary: {len(messages['passes'])} passed, "
        f"{len(messages['warnings'])} warnings, {len(messages['errors'])} errors"
    )
    return 1 if messages["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
