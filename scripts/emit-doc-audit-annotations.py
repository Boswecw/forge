#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def gha_escape(value: str) -> str:
    return value.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')


def emit_annotation(level: str, message: str, *, file_path: str | None = None, title: str | None = None) -> None:
    parts: list[str] = []
    if file_path:
        parts.append(f"file={gha_escape(file_path)}")
    if title:
        parts.append(f"title={gha_escape(title)}")
    prefix = f"::{level}"
    if parts:
        prefix += f" {','.join(parts)}"
    prefix += "::"
    print(prefix + gha_escape(message))


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def append_summary(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "## Documentation Audit Summary",
        "",
        f"- Selected surfaces: `{len(payload['selection']['selected_repo_ids'])}`",
        f"- Changed-only: `{'yes' if payload['metadata']['changed_only'] else 'no'}`",
        f"- Strict: `{'yes' if payload['metadata']['strict'] else 'no'}`",
        f"- Errors: `{len(payload['summary']['errors'])}`",
        f"- Warnings: `{len(payload['summary']['warnings'])}`",
        "",
    ]

    if payload['selection']['selected_repo_ids']:
        lines.append("### Scoped Surfaces")
        lines.append("")
        for repo_id in payload['selection']['selected_repo_ids']:
            lines.append(f"- `{repo_id}`")
        lines.append("")

    freshness_items = [
        entry
        for entry in payload['freshness']['entries']
        if entry['repo_id'] in payload['freshness']['stale_or_changed'] or entry['repo_id'] in payload['freshness']['missing_outputs']
    ]
    if freshness_items:
        lines.append("### Stale Or Missing Documentation Outputs")
        lines.append("")
        for entry in freshness_items:
            lines.append(f"- `{entry['repo_id']}`: {entry['hint']}")
            for diff_line in entry.get('diff_preview', [])[:6]:
                lines.append(f"  - `{diff_line}`")
        lines.append("")

    if payload['summary']['errors']:
        lines.append("### Errors")
        lines.append("")
        for message in payload['summary']['errors']:
            lines.append(f"- {message}")
        lines.append("")

    if payload['summary']['warnings']:
        lines.append("### Warnings")
        lines.append("")
        for message in payload['summary']['warnings']:
            lines.append(f"- {message}")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def emit_from_payload(payload: dict[str, Any]) -> None:
    for entry in payload['freshness']['entries']:
        if entry['repo_id'] in payload['freshness']['stale_or_changed']:
            emit_annotation(
                'error',
                entry['hint'] or f"Documentation output requires rebuild: {entry['repo_id']}",
                file_path=entry.get('output'),
                title='Documentation Output Drift',
            )
        elif entry['repo_id'] in payload['freshness']['missing_outputs']:
            emit_annotation(
                'error',
                entry['hint'] or f"Documentation output missing: {entry['repo_id']}",
                file_path=entry.get('output'),
                title='Documentation Output Missing',
            )

    for message in payload['summary']['warnings']:
        emit_annotation('warning', message, title='Documentation Audit Warning')
    for message in payload['summary']['errors']:
        emit_annotation('error', message, title='Documentation Audit Error')


def main() -> int:
    parser = argparse.ArgumentParser(description='Emit GitHub annotations and step summary from doc-audit JSON output.')
    parser.add_argument('--json', required=True, help='Path to doc-audit JSON output.')
    parser.add_argument('--summary-out', help='Optional explicit markdown summary output path.')
    args = parser.parse_args()

    json_path = Path(args.json)
    if not json_path.exists():
        emit_annotation('warning', f'doc-audit JSON not found: {json_path}', title='Documentation Audit')
        return 0

    payload = load_payload(json_path)
    emit_from_payload(payload)

    summary_target = args.summary_out or os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_target:
        append_summary(Path(summary_target), payload)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
