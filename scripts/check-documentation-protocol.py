#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from doc_registry import REGISTRY_PATH, ROOT, DocumentationRegistry, DocumentationSurface, load_registry, registry_payload


PROTOCOL_LABEL = "Forge Documentation Protocol v1"
README_CONTRACT_HEADER = "## Documentation Contract"
README_CONTRACT_FIELDS = (
    "**Repo type:**",
    "**Authority boundary:**",
    "**Deep reference:**",
    "**README role:**",
    "**Truth note:**",
)
INDEX_REQUIRED_SNIPPETS = (
    f"**Protocol:** {PROTOCOL_LABEL}",
    "Canonical facts",
    "Snapshot facts",
    "Assembly contract:",
    "Command: `bash doc/system/BUILD.sh`",
    "Output:",
    "Last updated:",
)
BUILD_REQUIRED_SNIPPETS = (
    "#!/usr/bin/env bash",
    "set -euo pipefail",
    'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"',
    "_index.md",
    "[0-9][0-9]-*.md",
    "sort",
    "wc -l",
)
FORBIDDEN_PATTERNS = (
    re.compile(r"ECOSYSTEM_CANONICAL"),
    re.compile(r"\b8787\b"),
    re.compile(r"\b8788\b"),
    re.compile(r"\b8789\b"),
    re.compile(r"\b8800\b"),
    re.compile(r"BDS Documentation Protocol"),
    re.compile(r"BDS Protocol"),
)


class CheckState:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def payload(self, registry: DocumentationRegistry | None = None) -> dict[str, object]:
        payload: dict[str, object] = {
            "summary": {
                "passed": len(self.passes),
                "warnings": len(self.warnings),
                "errors": len(self.errors),
            },
            "passes": self.passes,
            "warnings": self.warnings,
            "errors": self.errors,
        }
        if registry is not None:
            payload["registry"] = registry_payload(registry)
        return payload


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, state: CheckState) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        state.error(f"missing file: {path.relative_to(ROOT)}")
        return ""


def ensure_contains(text: str, path: Path, snippets: tuple[str, ...], state: CheckState) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        state.error(f"{path.relative_to(ROOT)} missing required snippets: {', '.join(missing)}")
    else:
        state.ok(f"{path.relative_to(ROOT)} carries required protocol markers")


def latest_report_path(expected_date: str | None, state: CheckState) -> Path | None:
    audit_dir = ROOT / "docs" / "audits"
    if expected_date:
        report = audit_dir / f"documentation_protocol_canonicalization_report_{expected_date}.md"
        if not report.exists():
            state.error(f"missing expected audit report: {report.relative_to(ROOT)}")
            return None
        return report

    reports = sorted(audit_dir.glob("documentation_protocol_canonicalization_report_*.md"))
    if not reports:
        state.error("missing documentation protocol audit report in docs/audits/")
        return None
    return reports[-1]


def check_readme(surface: DocumentationSurface, state: CheckState) -> None:
    text = read_text(surface.readme_path, state)
    if not text:
        return
    ensure_contains(text, surface.readme_path, (README_CONTRACT_HEADER, *README_CONTRACT_FIELDS), state)


def check_index(surface: DocumentationSurface, state: CheckState) -> None:
    text = read_text(surface.index_path, state)
    if not text:
        return
    if surface.assembled_path is None:
        state.error(f"{surface.repo_id} requires doc/system but has no assembled_system_path in registry")
        return
    output_rel = surface.assembled_path.relative_to(surface.root)
    dynamic_snippets = (
        *INDEX_REQUIRED_SNIPPETS[:-1],
        f"Output: `{output_rel.as_posix()}`",
        INDEX_REQUIRED_SNIPPETS[-1],
    )
    ensure_contains(text, surface.index_path, dynamic_snippets, state)


def check_build(surface: DocumentationSurface, state: CheckState) -> None:
    text = read_text(surface.build_path, state)
    if not text:
        return
    ensure_contains(text, surface.build_path, BUILD_REQUIRED_SNIPPETS, state)


def scan_forbidden(paths: list[Path], state: CheckState) -> None:
    for path in paths:
        text = read_text(path, state)
        if not text:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                state.error(f"{path.relative_to(ROOT)} contains forbidden legacy marker: {pattern.pattern}")


def check_report(report_path: Path, registry: DocumentationRegistry, state: CheckState) -> None:
    text = read_text(report_path, state)
    if not text:
        return
    for surface in registry.surfaces_by_status("compliant", "partial", "deferred"):
        if not any(label in text for label in surface.required_report_labels):
            state.error(
                f"{report_path.relative_to(ROOT)} does not mention tracked surface: {surface.repo_id}"
            )
    state.ok(
        f"{report_path.relative_to(ROOT)} covers tracked compliant, partial, and deferred surfaces"
    )


def run_build(surface: DocumentationSurface, state: CheckState) -> None:
    result = subprocess.run(
        ["bash", str(surface.build_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        state.error(
            f"build failed for {surface.repo_id}: {surface.build_path.relative_to(ROOT)}\n"
            f"{result.stdout}{result.stderr}"
        )
        return
    state.ok(f"build succeeded for {surface.repo_id}: {surface.build_path.relative_to(ROOT)}")


def check_registry(state: CheckState) -> DocumentationRegistry | None:
    if not REGISTRY_PATH.exists():
        state.error(f"missing canonical documentation registry: {REGISTRY_PATH.relative_to(ROOT)}")
        return None
    try:
        registry = load_registry(REGISTRY_PATH)
    except Exception as exc:  # pragma: no cover - fail closed path
        state.error(f"invalid canonical documentation registry: {REGISTRY_PATH.relative_to(ROOT)} ({exc})")
        return None
    state.ok(f"canonical documentation registry present: {REGISTRY_PATH.relative_to(ROOT)}")
    return registry


def selected_surfaces(
    registry: DocumentationRegistry,
    requested_surface_ids: list[str],
    state: CheckState,
) -> tuple[DocumentationSurface, ...]:
    if not requested_surface_ids:
        return registry.surfaces

    surface_map = {surface.repo_id: surface for surface in registry.surfaces}
    selected: list[DocumentationSurface] = []
    for repo_id in requested_surface_ids:
        surface = surface_map.get(repo_id)
        if surface is None:
            state.error(f"requested surface is not registered: {repo_id}")
            continue
        selected.append(surface)

    if selected:
        state.ok(
            "protocol checker scoped to surfaces: "
            + ", ".join(surface.repo_id for surface in selected)
        )
    return tuple(selected)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Forge documentation protocol compliance.")
    parser.add_argument(
        "--expected-report-date",
        help="Require docs/audits/documentation_protocol_canonicalization_report_<date>.md to exist.",
    )
    parser.add_argument(
        "--run-builds",
        action="store_true",
        help="Run each registry surface's doc/system/BUILD.sh when the policy requires a doc/system.",
    )
    parser.add_argument(
        "--surface",
        action="append",
        default=[],
        help="Limit README/doc-system surface checks to the given registered repo_id; may be repeated.",
    )
    parser.add_argument(
        "--json-out",
        help="Write machine-readable results to the given JSON path.",
    )
    args = parser.parse_args()

    state = CheckState()
    registry = check_registry(state)

    protocol_doc = None if registry is None else registry.protocol_spec
    if protocol_doc is None:
        protocol_doc = ROOT / "docs" / "canonical" / "documentation_protocol_v1.md"

    if protocol_doc.exists():
        state.ok(f"canonical protocol spec present: {protocol_doc.relative_to(ROOT)}")
    else:
        state.error(f"missing canonical protocol spec: {protocol_doc.relative_to(ROOT)}")

    report = latest_report_path(args.expected_report_date, state)
    if report is not None:
        state.ok(f"audit report present: {report.relative_to(ROOT)}")
        if registry is not None:
            check_report(report, registry, state)

    if registry is not None:
        surfaces = selected_surfaces(registry, args.surface, state)
        for surface in surfaces:
            if not surface.root.exists():
                state.error(f"registry surface missing from workspace: {surface.path.as_posix()}")
                continue

            state.ok(
                f"registry surface present: {surface.path.as_posix()} ({surface.policy_class}, {surface.status})"
            )

            if surface.requires_readme_contract:
                check_readme(surface, state)

            if surface.requires_doc_system:
                check_index(surface, state)
                check_build(surface, state)
                if surface.assembled_path is None:
                    state.error(f"{surface.repo_id} requires assembled output but registry path is empty")
                elif surface.assembled_path.exists():
                    state.ok(f"assembled artifact present: {surface.assembled_path.relative_to(ROOT)}")
                else:
                    state.error(f"missing assembled artifact: {surface.assembled_path.relative_to(ROOT)}")

            if surface.status != "historical":
                scan_forbidden(surface.maintained_protocol_paths, state)

        if args.run_builds:
            for surface in surfaces:
                if not surface.requires_doc_system:
                    continue
                run_build(surface, state)

    if args.json_out:
        output_path = Path(args.json_out)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(state.payload(registry), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        state.ok(f"machine-readable results written: {display_path(output_path)}")

    for message in state.passes:
        print(f"PASS {message}")
    for message in state.warnings:
        print(f"WARN {message}")
    for message in state.errors:
        print(f"FAIL {message}")

    print(
        f"\nSummary: {len(state.passes)} passed, "
        f"{len(state.warnings)} warnings, {len(state.errors)} errors"
    )
    return 1 if state.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
