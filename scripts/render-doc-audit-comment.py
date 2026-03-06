#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COMMENT_MARKER = "<!-- doc-audit-comment -->"
COMMENT_CHANGED_PATH_LIMIT = 8


def load_payload(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def overall_status(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return "missing"
    if payload["summary"]["errors"]:
        return "fail"
    if payload["summary"]["warnings"]:
        return "warn"
    return "pass"


def truncate(items: list[str], limit: int = 8) -> list[str]:
    if len(items) <= limit:
        return items
    return items[:limit] + [f"... and {len(items) - limit} more"]


def render_comment(payload: dict[str, Any] | None, *, run_url: str | None, artifact_name: str | None) -> str:
    status = overall_status(payload)
    lines = [COMMENT_MARKER, "## Documentation Audit", ""]

    if payload is None:
        lines.extend(
            [
                "- Status: `missing`",
                "- Structured `doc-audit` JSON output was not available for this run.",
            ]
        )
    else:
        selected = payload["selection"].get("selected_repo_ids", [])
        changed_paths = payload["selection"].get("changed_paths", [])
        changed_paths_source = payload["selection"].get("changed_paths_source", "unknown")
        lines.extend(
            [
                f"- Status: `{status}`",
                f"- Scope mode: `{payload['selection'].get('mode', 'unknown')}`",
                f"- Changed-only: `{'yes' if payload['metadata'].get('changed_only') else 'no'}`",
                f"- Strict: `{'yes' if payload['metadata'].get('strict') else 'no'}`",
                f"- Selected surfaces: `{len(selected)}`",
                f"- Changed paths: `{len(changed_paths)}`",
                f"- Errors: `{len(payload['summary']['errors'])}`",
                f"- Warnings: `{len(payload['summary']['warnings'])}`",
                "",
            ]
        )

        if selected:
            lines.append("### Scoped Surfaces")
            lines.append("")
            for repo_id in truncate(selected, limit=10):
                lines.append(f"- `{repo_id}`")
            lines.append("")

        if changed_paths and payload["metadata"].get("changed_only"):
            lines.append("### Changed Paths")
            lines.append("")
            lines.append(f"- Source: `{changed_paths_source}`")
            if len(changed_paths) <= COMMENT_CHANGED_PATH_LIMIT:
                for path in changed_paths:
                    lines.append(f"- `{path}`")
            else:
                for path in changed_paths[:COMMENT_CHANGED_PATH_LIMIT]:
                    lines.append(f"- `{path}`")
                lines.append(f"- ... and {len(changed_paths) - COMMENT_CHANGED_PATH_LIMIT} more")
            lines.append("")

        global_trigger_paths = payload["selection"].get("global_trigger_paths", [])
        if global_trigger_paths:
            lines.append("### Full-Audit Escalation")
            lines.append("")
            lines.append("- Changed paths triggered a full governance audit:")
            for item in truncate(global_trigger_paths, limit=6):
                lines.append(f"- `{item}`")
            lines.append("")

        freshness_items = [
            entry
            for entry in payload["freshness"]["entries"]
            if entry["repo_id"] in payload["freshness"]["stale_or_changed"]
            or entry["repo_id"] in payload["freshness"]["missing_outputs"]
        ]
        if freshness_items:
            lines.append("### Stale Or Missing Documentation Outputs")
            lines.append("")
            for entry in freshness_items[:6]:
                lines.append(f"- `{entry['repo_id']}`: {entry['hint']}")
            if len(freshness_items) > 6:
                lines.append(f"- ... and {len(freshness_items) - 6} more")
            lines.append("")

        if payload["summary"]["errors"]:
            lines.append("### Errors")
            lines.append("")
            for message in truncate(payload["summary"]["errors"], limit=10):
                lines.append(f"- {message}")
            lines.append("")

        if payload["summary"]["warnings"]:
            lines.append("### Warnings")
            lines.append("")
            for message in truncate(payload["summary"]["warnings"], limit=10):
                lines.append(f"- {message}")
            lines.append("")

        if not payload["summary"]["errors"] and not payload["summary"]["warnings"]:
            lines.append("### Outcome")
            lines.append("")
            lines.append("- No documentation protocol violations were detected in the scoped audit.")
            lines.append("")

    if artifact_name or run_url:
        lines.append("### Full Details")
        lines.append("")
        if artifact_name:
            lines.append(f"- Artifact: `{artifact_name}`")
        if run_url:
            lines.append(f"- Workflow run: {run_url}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a PR comment body from doc-audit JSON output.")
    parser.add_argument("--json", required=True, help="Path to doc-audit JSON output.")
    parser.add_argument("--out", required=True, help="Path to write the markdown comment body.")
    parser.add_argument("--run-url", help="Optional workflow run URL for the footer.")
    parser.add_argument("--artifact-name", help="Optional uploaded artifact name for the footer.")
    args = parser.parse_args()

    payload = load_payload(Path(args.json))
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_comment(payload, run_url=args.run_url, artifact_name=args.artifact_name),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
