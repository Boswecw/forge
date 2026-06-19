#!/usr/bin/env python3
"""Generate a condensed queue for source-local holds that may need support promotion."""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependent
    print(f"FAIL: PyYAML is required to load drift reports: {exc}", file=sys.stderr)
    sys.exit(2)


LEDGER_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = LEDGER_ROOT / "drift-reports"
OUT_DIR = LEDGER_ROOT / "docs" / "slice-01"
QUEUE_YAML = OUT_DIR / "support-promotion-candidate-queue.yaml"
QUEUE_MD = OUT_DIR / "support-promotion-candidate-queue.md"

PROMOTION_CANDIDATE_CLASSES = {
    "source_runtime_or_capability",
    "source_contract_schema_migration",
    "source_scripts_ci",
    "source_proof_tests",
}

CATEGORY_POSTURE = {
    "source_local_subproject": "default_hold",
    "source_proof_tests": "pair_with_promoted_runtime_or_contract",
    "source_runtime_or_capability": "candidate_after_target_role",
    "source_docs_or_doc_mirror": "default_hold_docs_rule",
    "source_contract_schema_migration": "candidate_after_contract_compatibility",
    "source_evidence_reports_prompts": "default_hold_evidence_receipt_only",
    "source_scripts_ci": "candidate_when_tied_to_support_proof_command",
    "source_scaffold_config": "default_hold_dependency_adoption_required",
    "other": "requires_manual_triage",
}


def categorize(path: str) -> str:
    top = path.split("/", 1)[0]
    if top in {"repo-crawler", "worm"}:
        return "source_local_subproject"
    if path.startswith("tests/"):
        return "source_proof_tests"
    if top in {
        "cortex_runtime",
        "gnat_core",
        "gnat_runtime",
        "app",
        "constants",
        "src",
        "runtime",
        "service",
        "prompt_assembly",
    }:
        return "source_runtime_or_capability"
    if top in {"schemas", "sql", "alembic"} or path == "alembic.ini":
        return "source_contract_schema_migration"
    if top in {"docs", "doc"} or path in {"NLOSYSTEM.md", "GEMINI.md"}:
        return "source_docs_or_doc_mirror"
    if top == "scripts" or path == "ci_gate.sh":
        return "source_scripts_ci"
    if top in {
        "reports",
        "outputs",
        "evidence",
        "inputs",
        "seeds",
        "proving_slice",
        "evals",
        "promotion",
        "promotions",
        "registry",
        "prompts",
    } or path.startswith("DECISIONS/"):
        return "source_evidence_reports_prompts"
    if top.startswith(".env") or path in {
        ".codex",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-graphiti.txt",
        "docker-compose.graphiti-pilot.yml",
    }:
        return "source_scaffold_config"
    return "other"


def load_reports(report_dir: Path) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for path in sorted(report_dir.glob("*.drift.yaml")):
        with path.open("r", encoding="utf-8") as handle:
            report = yaml.safe_load(handle) or {}
        if not isinstance(report, dict):
            raise ValueError(f"drift report must be a mapping: {path}")
        reports.append(report)
    if not reports:
        raise FileNotFoundError(f"no drift reports found in {report_dir}")
    return reports


def build_queue(reports: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    category_counts: Counter[str] = Counter()
    repo_counts: Counter[str] = Counter()
    repo_category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    samples: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    blocking_counts: Counter[str] = Counter()

    for report in reports:
        pair = report["repo_pair"]
        summary = report.get("classification_summary", {})
        for classification in ("missing_from_target", "unknown", "dangerous_drift"):
            blocking_counts[classification] += int(summary.get(classification, 0))

        for item in report.get("items", []):
            if item.get("classification") != "source_local_hold":
                continue
            path = item["path"]
            category = categorize(path)
            category_counts[category] += 1
            repo_counts[pair] += 1
            repo_category_counts[pair][category] += 1
            if len(samples[pair][category]) < 5:
                samples[pair][category].append(path)

    candidate_categories = {
        category: count
        for category, count in sorted(category_counts.items())
        if category in PROMOTION_CANDIDATE_CLASSES
    }
    default_hold_categories = {
        category: count
        for category, count in sorted(category_counts.items())
        if category not in PROMOTION_CANDIDATE_CLASSES
    }

    return {
        "generated_at": generated_at,
        "scope": "Slice 01 support promotion candidate queue from reviewed source-local holds",
        "input_reports": str(REPORT_DIR),
        "summary": {
            "source_local_hold": sum(category_counts.values()),
            "candidate_after_target_role": sum(candidate_categories.values()),
            "default_hold": sum(default_hold_categories.values()),
            "missing_from_target": int(blocking_counts["missing_from_target"]),
            "unknown": int(blocking_counts["unknown"]),
            "dangerous_drift": int(blocking_counts["dangerous_drift"]),
        },
        "promotion_rule": (
            "A source-local hold may enter app support only after a named promotion "
            "slice declares the target role, source proof command, support proof "
            "command, and post-promotion drift report."
        ),
        "category_summary": {
            category: {
                "count": int(count),
                "posture": CATEGORY_POSTURE.get(category, "requires_manual_triage"),
            }
            for category, count in sorted(category_counts.items())
        },
        "candidate_categories": candidate_categories,
        "default_hold_categories": default_hold_categories,
        "repo_breakdown": dict(sorted(repo_counts.items())),
        "repo_category_breakdown": {
            repo: dict(sorted(counter.items()))
            for repo, counter in sorted(repo_category_counts.items())
        },
        "samples": {
            repo: {category: paths for category, paths in sorted(categories.items())}
            for repo, categories in sorted(samples.items())
        },
        "next_gate": (
            "Select exactly one candidate category and repo pair, then create a "
            "promotion slice with explicit support target role and proof commands."
        ),
    }


def write_yaml(queue: dict[str, Any], path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing queue: {path}")
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(queue, handle, sort_keys=False, allow_unicode=False)


def write_markdown(queue: dict[str, Any], path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing queue: {path}")
    summary = queue["summary"]
    with path.open("w", encoding="utf-8") as handle:
        handle.write("# Slice 01 Support Promotion Candidate Queue\n\n")
        handle.write(f"Generated: `{queue['generated_at']}`\n\n")
        handle.write(
            "This queue is generated from reviewed `source_local_hold` drift. It "
            "does not authorize copying artifacts into app support.\n\n"
        )
        handle.write("## Summary\n\n")
        handle.write("| Metric | Count |\n")
        handle.write("| --- | ---: |\n")
        for key in (
            "source_local_hold",
            "candidate_after_target_role",
            "default_hold",
            "missing_from_target",
            "unknown",
            "dangerous_drift",
        ):
            handle.write(f"| `{key}` | {summary[key]} |\n")

        handle.write("\n## Like Types\n\n")
        handle.write("| Type | Count | Posture |\n")
        handle.write("| --- | ---: | --- |\n")
        for category, detail in queue["category_summary"].items():
            handle.write(
                f"| `{category}` | {detail['count']} | `{detail['posture']}` |\n"
            )

        handle.write("\n## Repo Breakdown\n\n")
        handle.write("| Repo pair | Source-local holds |\n")
        handle.write("| --- | ---: |\n")
        for repo, count in queue["repo_breakdown"].items():
            handle.write(f"| `{repo}` | {count} |\n")

        handle.write("\n## Gate\n\n")
        handle.write(queue["promotion_rule"] + "\n\n")
        handle.write(
            "Select exactly one candidate category and repo pair before opening a "
            "support promotion slice. The slice must name the support target role, "
            "source proof command, support proof command, and regenerated drift "
            "report.\n"
        )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-dir", default=str(REPORT_DIR))
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv[1:])

    report_dir = Path(args.report_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        queue = build_queue(load_reports(report_dir), generated_at)
        write_yaml(queue, out_dir / QUEUE_YAML.name, args.overwrite)
        write_markdown(queue, out_dir / QUEUE_MD.name, args.overwrite)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: generated support promotion candidate queue")
    print(out_dir / QUEUE_YAML.name)
    print(out_dir / QUEUE_MD.name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
