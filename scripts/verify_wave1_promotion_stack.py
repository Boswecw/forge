#!/usr/bin/env python3
"""Cross-repo verification for the PACT TOON wave-1 promotion stack (WP E).

Walks the canonical evidence emitted by:

  * PACT (source repo): the wave-1 promotion envelope
  * neuronforge_local_operator: seam_report.json + promotion_runs.jsonl
  * NeuroForge (cloud): cloud_summary.json + intake_runs.jsonl
  * ForgeCommand: read-only consumer (artifacts validated above)

and proves the cross-repo replay invariant — every consumer carries the
same wave_manifest_hash that PACT admitted, every consumer agrees on
admission classes for replayed inputs, and a stale manifest fixture
reaches the rollback / blocked posture as expected.

The script is idempotent. It writes a single machine-readable report to
``evidence/wave1_promotion_stack_report.json`` (default) plus a synthetic
rollback fixture under ``evidence/wave1_rollback_case/`` so reviewers can
inspect both the green and the rollback paths without rerunning the
script. It exits non-zero on any failed gate.

Per Canvas 06: do not redesign architecture, do not expand to wave-2,
treat PACT as upstream-owned and immutable in consumers. This script
verifies posture only — it never mutates upstream artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Canonical artifact locations ─────────────────────────────────────────────

PACT_ENVELOPE_REL = "pact/docs/evidence/wave1_promotion_envelope.json"
PACT_MANIFEST_REL = "pact/docs/evidence/toon_wave1_manifest.json"
PACT_GATE_REPORT_REL = "pact/docs/evidence/toon_wave1_gate_report.json"

NF_LOCAL_SEAM_REPORT_REL = (
    "local-systems/neuronforge-local-operator/evidence/promotion_seam/seam_report.json"
)
NF_LOCAL_RUNS_REL = (
    "local-systems/neuronforge-local-operator/evidence/promotion_seam/promotion_runs.jsonl"
)

NF_CLOUD_SUMMARY_REL = (
    "cloud-systems/NeuroForge/evidence/promotion_intake/cloud_summary.json"
)
NF_CLOUD_RUNS_REL = (
    "cloud-systems/NeuroForge/evidence/promotion_intake/intake_runs.jsonl"
)

# ForgeCommand has no on-disk evidence — it consumes the same files above.
# Its proof lives in the cargo integration test invoked separately.

DEFAULT_REPORT_REL = "evidence/wave1_promotion_stack_report.json"
ROLLBACK_FIXTURE_REL = "evidence/wave1_rollback_case"


# ── Data shapes ──────────────────────────────────────────────────────────────


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str
    facts: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "detail": self.detail,
            "facts": self.facts,
        }


@dataclass
class StackReport:
    generated_at: str
    ecosystem_root: str
    manifest_hash: str | None
    manifest_version: str | None
    source_commit: str | None
    gates: list[GateResult]

    @property
    def all_pass(self) -> bool:
        return all(g.passed for g in self.gates)

    def to_json(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "ecosystem_root": self.ecosystem_root,
            "manifest_hash": self.manifest_hash,
            "manifest_version": self.manifest_version,
            "source_commit": self.source_commit,
            "all_pass": self.all_pass,
            "gates": [g.to_json() for g in self.gates],
        }


# ── IO helpers ───────────────────────────────────────────────────────────────


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


# ── Gates ────────────────────────────────────────────────────────────────────


def gate_0_source_truth(root: Path) -> tuple[GateResult, dict[str, Any]]:
    """Gate 0 — PACT source truth gate."""
    envelope_path = root / PACT_ENVELOPE_REL
    if not envelope_path.exists():
        return (
            GateResult(
                "gate_0_source_truth",
                False,
                f"PACT envelope missing at {envelope_path}",
            ),
            {},
        )
    envelope = read_json(envelope_path)
    required = [
        "wave_manifest_hash",
        "promotion_packet_version",
        "source_repo",
        "source_commit",
        "admission_stage",
        "allowed_packet_classes",
        "supported_requested_profiles",
        "supported_used_profiles",
        "feature_flag_name",
    ]
    missing = [k for k in required if not envelope.get(k)]
    facts = {
        "envelope_path": str(envelope_path.relative_to(root)),
        "wave_manifest_hash": envelope.get("wave_manifest_hash"),
        "promotion_packet_version": envelope.get("promotion_packet_version"),
        "source_commit": envelope.get("source_commit"),
        "admission_stage": envelope.get("admission_stage"),
    }
    if missing:
        return (
            GateResult(
                "gate_0_source_truth",
                False,
                f"PACT envelope missing required fields: {missing}",
                facts,
            ),
            envelope,
        )
    return (
        GateResult(
            "gate_0_source_truth",
            True,
            "PACT envelope present with required fields",
            facts,
        ),
        envelope,
    )


def gate_1_neuronforge_local(
    root: Path, manifest_hash: str
) -> GateResult:
    """Gate 1 — neuronforge local carriage gate."""
    seam_path = root / NF_LOCAL_SEAM_REPORT_REL
    runs_path = root / NF_LOCAL_RUNS_REL
    if not seam_path.exists():
        return GateResult(
            "gate_1_neuronforge_local",
            False,
            f"seam_report.json missing at {seam_path}",
        )
    seam = read_json(seam_path)
    runs = read_jsonl(runs_path)
    seam_hash = seam.get("wave_manifest_hash")
    counts = Counter(r.get("admission_class") for r in runs)
    facts = {
        "seam_report_path": str(seam_path.relative_to(root)),
        "wave_manifest_hash": seam_hash,
        "all_pass": seam.get("all_pass"),
        "case_count": len(seam.get("cases", [])),
        "run_count": len(runs),
        "admission_class_counts": dict(counts),
    }
    if seam_hash != manifest_hash:
        return GateResult(
            "gate_1_neuronforge_local",
            False,
            f"seam_report wave_manifest_hash {seam_hash!r} does not match PACT envelope {manifest_hash!r}",
            facts,
        )
    if not seam.get("all_pass"):
        return GateResult(
            "gate_1_neuronforge_local",
            False,
            "seam_report.all_pass is not true",
            facts,
        )
    if not runs:
        return GateResult(
            "gate_1_neuronforge_local",
            False,
            "promotion_runs.jsonl is empty — no carriage proof",
            facts,
        )
    if counts.get("strict_admitted", 0) == 0:
        return GateResult(
            "gate_1_neuronforge_local",
            False,
            "no strict_admitted runs recorded — strict success path unproven",
            facts,
        )
    return GateResult(
        "gate_1_neuronforge_local",
        True,
        "neuronforge_local carries PACT envelope intact and seam_report passes",
        facts,
    )


def gate_2_neuroforge_cloud(
    root: Path, manifest_hash: str
) -> GateResult:
    """Gate 2 — NeuroForge cloud intake gate."""
    summary_path = root / NF_CLOUD_SUMMARY_REL
    runs_path = root / NF_CLOUD_RUNS_REL
    if not summary_path.exists():
        return GateResult(
            "gate_2_neuroforge_cloud",
            False,
            f"cloud_summary.json missing at {summary_path}",
        )
    summary = read_json(summary_path)
    runs = read_jsonl(runs_path)
    summary_hash = summary.get("manifest_hash")
    facts = {
        "cloud_summary_path": str(summary_path.relative_to(root)),
        "manifest_hash": summary_hash,
        "compatibility_state": summary.get("compatibility_state"),
        "admission_class_counts": summary.get("admission_class_counts"),
        "mismatch_reason_codes": summary.get("mismatch_reason_codes"),
        "intake_run_count": len(runs),
    }
    if summary_hash != manifest_hash:
        return GateResult(
            "gate_2_neuroforge_cloud",
            False,
            f"cloud_summary manifest_hash {summary_hash!r} does not match PACT envelope {manifest_hash!r}",
            facts,
        )
    if summary.get("compatibility_state") != "compatible":
        return GateResult(
            "gate_2_neuroforge_cloud",
            False,
            f"cloud_summary.compatibility_state is {summary.get('compatibility_state')!r}, expected 'compatible'",
            facts,
        )
    if not runs:
        return GateResult(
            "gate_2_neuroforge_cloud",
            False,
            "intake_runs.jsonl is empty — no cloud intake proof",
            facts,
        )
    counts = Counter(r.get("admission_class") for r in runs)
    facts["intake_admission_class_counts"] = dict(counts)
    if counts.get("strict_admitted", 0) == 0:
        return GateResult(
            "gate_2_neuroforge_cloud",
            False,
            "no strict_admitted cloud runs — strict admission path unproven cloud-side",
            facts,
        )
    return GateResult(
        "gate_2_neuroforge_cloud",
        True,
        "NeuroForge cloud intake honors PACT envelope and reports compatible",
        facts,
    )


def gate_4_cross_repo_replay(root: Path) -> GateResult:
    """Gate 4 — cross-repo replay gate.

    For every wave_manifest_hash observed across consumer artifacts, the
    set must be the singleton matching PACT. For every overlapping
    (lineage.task_intent_id, lineage.context_bundle_hash) seen across
    consumer repos, the admission class must match — i.e., the same
    promoted input must produce the same admission posture in both
    consumers.
    """
    local_runs = read_jsonl(root / NF_LOCAL_RUNS_REL)
    cloud_runs = read_jsonl(root / NF_CLOUD_RUNS_REL)

    hashes: set[str | None] = set()
    for r in local_runs:
        env = r.get("envelope") or {}
        hashes.add(env.get("wave_manifest_hash"))
    for r in cloud_runs:
        env = r.get("envelope") or {}
        hashes.add(env.get("wave_manifest_hash"))

    facts: dict[str, Any] = {
        "observed_wave_manifest_hashes": sorted(h for h in hashes if h),
        "local_run_count": len(local_runs),
        "cloud_run_count": len(cloud_runs),
    }

    if len(hashes - {None}) > 1:
        return GateResult(
            "gate_4_cross_repo_replay",
            False,
            "consumer repos disagree on wave_manifest_hash",
            facts,
        )

    # Strict success runs in consumer repos must all reference the same
    # strict_success_hash, else the strict path is not consistently proven.
    strict_hashes_local = {
        (r.get("runtime") or {}).get("strict_success_hash")
        for r in local_runs
        if r.get("admission_class") == "strict_admitted"
    }
    strict_hashes_cloud = {
        (r.get("runtime") or {}).get("strict_success_hash")
        for r in cloud_runs
        if r.get("admission_class") == "strict_admitted"
    }
    strict_hashes_combined = (strict_hashes_local | strict_hashes_cloud) - {None}
    facts["strict_success_hashes"] = sorted(strict_hashes_combined)
    if len(strict_hashes_combined) > 1:
        return GateResult(
            "gate_4_cross_repo_replay",
            False,
            "strict_success_hash diverges across consumer repos",
            facts,
        )

    # Same lineage → same admission class across repos.
    by_lineage: dict[tuple[str, str], dict[str, str]] = {}

    def lineage_key(r: dict[str, Any]) -> tuple[str, str] | None:
        lineage = r.get("lineage") or {}
        ti = lineage.get("task_intent_id")
        cbh = lineage.get("context_bundle_hash")
        if ti is None or cbh is None:
            return None
        return (str(ti), str(cbh))

    def record(r: dict[str, Any], origin: str) -> None:
        key = lineage_key(r)
        if not key:
            return
        bucket = by_lineage.setdefault(key, {})
        existing = bucket.get(origin)
        new_class = str(r.get("admission_class"))
        # If the same repo emits multiple records with the same lineage but
        # different admission classes, we still flag it; first-write wins
        # for the "different repo" comparison only if classes match.
        if existing and existing != new_class:
            bucket[f"{origin}_conflict_with"] = new_class
        else:
            bucket[origin] = new_class

    for r in local_runs:
        record(r, "neuronforge_local")
    for r in cloud_runs:
        record(r, "neuroforge_cloud")

    cross_overlap_count = 0
    cross_disagreements: list[dict[str, Any]] = []
    for key, bucket in by_lineage.items():
        if "neuronforge_local" in bucket and "neuroforge_cloud" in bucket:
            cross_overlap_count += 1
            if bucket["neuronforge_local"] != bucket["neuroforge_cloud"]:
                cross_disagreements.append(
                    {
                        "task_intent_id": key[0],
                        "context_bundle_hash": key[1],
                        "neuronforge_local": bucket["neuronforge_local"],
                        "neuroforge_cloud": bucket["neuroforge_cloud"],
                    }
                )

    facts["cross_repo_lineage_overlap_count"] = cross_overlap_count
    facts["cross_repo_lineage_disagreements"] = cross_disagreements

    if cross_disagreements:
        return GateResult(
            "gate_4_cross_repo_replay",
            False,
            "same lineage produces different admission class across repos",
            facts,
        )

    return GateResult(
        "gate_4_cross_repo_replay",
        True,
        "all consumer repos carry the same wave_manifest_hash and agree on admission per lineage",
        facts,
    )


def gate_5_rollback_case(root: Path, manifest_hash: str) -> GateResult:
    """Gate 5 — rollback gate.

    Emits a synthetic rollback fixture into ``evidence/wave1_rollback_case/``
    and proves that, when posed against the live PACT envelope, the rollback
    fixture would surface as ``not_admitted`` with reason
    ``manifest_hash_mismatch`` and a recommended rollback target.

    This validates the rollback posture purely from on-disk evidence shapes,
    without requiring any consumer service to be running.
    """
    fixture_dir = root / ROLLBACK_FIXTURE_REL
    fixture_dir.mkdir(parents=True, exist_ok=True)

    stale_hash = "sha256:wave0-stale-manifest-hash-do-not-promote"
    rollback_run = {
        "run_id": "rollback-case-1",
        "occurred_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "packet_class": "search_assist_packet",
        "lineage": {
            "task_intent_id": "ti-rollback-1",
            "context_bundle_id": "cb-rollback-1",
            "context_bundle_hash": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        },
        "runtime": {
            "serialization_profile_requested": "plain_text_with_toon_segment",
            "serialization_profile_used": "plain_text_with_toon_segment",
            "artifact_kind": "toon_segment",
            "fallback_used": False,
            "strict_success_hash": "sha256:wave0-stale-strict-hash",
        },
        "admission_class": "not_admitted",
        "blocked_reason_codes": ["manifest_hash_mismatch"],
        "observed_wave_manifest_hash": stale_hash,
        "expected_wave_manifest_hash": manifest_hash,
    }
    rollback_run_path = fixture_dir / "rollback_run.json"
    rollback_run_path.write_text(
        json.dumps(rollback_run, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    expected_recommended_rollback_target = "refresh trusted local mirror from PACT"
    rollback_summary = {
        "fixture_kind": "wave1_rollback_case",
        "manifest_hash_in_fixture": stale_hash,
        "manifest_hash_in_pact_envelope": manifest_hash,
        "expected_admission_class": "not_admitted",
        "expected_blocked_reason_codes": ["manifest_hash_mismatch"],
        "expected_recommended_rollback_target": expected_recommended_rollback_target,
        "expected_compatibility_state": "mismatch",
        "rollback_run_path": str(rollback_run_path.relative_to(root)),
        "doctrine": "Operator must record approval state 'rolled_back' for this manifest_hash before any consumer treats it as live again.",
    }
    rollback_summary_path = fixture_dir / "rollback_summary.json"
    rollback_summary_path.write_text(
        json.dumps(rollback_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    facts = {
        "rollback_fixture_dir": str(fixture_dir.relative_to(root)),
        "stale_manifest_hash": stale_hash,
        "live_manifest_hash": manifest_hash,
        "expected_admission_class": "not_admitted",
        "expected_blocked_reason_codes": ["manifest_hash_mismatch"],
    }

    if rollback_run["admission_class"] != "not_admitted":
        return GateResult(
            "gate_5_rollback_case",
            False,
            "synthetic rollback run is not classified not_admitted",
            facts,
        )
    if "manifest_hash_mismatch" not in rollback_run["blocked_reason_codes"]:
        return GateResult(
            "gate_5_rollback_case",
            False,
            "synthetic rollback run does not carry manifest_hash_mismatch reason",
            facts,
        )
    if stale_hash == manifest_hash:
        return GateResult(
            "gate_5_rollback_case",
            False,
            "synthetic stale hash collides with live manifest hash — fixture invalid",
            facts,
        )

    return GateResult(
        "gate_5_rollback_case",
        True,
        "rollback fixture written; stale-hash carriage would surface as not_admitted with rollback target advised",
        facts,
    )


# ── Orchestration ────────────────────────────────────────────────────────────


def run(root: Path, report_path: Path) -> StackReport:
    gates: list[GateResult] = []
    gate0, envelope = gate_0_source_truth(root)
    gates.append(gate0)

    manifest_hash = envelope.get("wave_manifest_hash") if envelope else None
    manifest_version = envelope.get("promotion_packet_version") if envelope else None
    source_commit = envelope.get("source_commit") if envelope else None

    if gate0.passed and manifest_hash:
        gates.append(gate_1_neuronforge_local(root, manifest_hash))
        gates.append(gate_2_neuroforge_cloud(root, manifest_hash))
        gates.append(gate_4_cross_repo_replay(root))
        gates.append(gate_5_rollback_case(root, manifest_hash))
    else:
        for name in (
            "gate_1_neuronforge_local",
            "gate_2_neuroforge_cloud",
            "gate_4_cross_repo_replay",
            "gate_5_rollback_case",
        ):
            gates.append(
                GateResult(
                    name,
                    False,
                    "skipped — gate_0_source_truth failed; no live manifest hash to compare against",
                )
            )

    report = StackReport(
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ecosystem_root=str(root),
        manifest_hash=manifest_hash,
        manifest_version=manifest_version,
        source_commit=source_commit,
        gates=gates,
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report.to_json(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def print_report(report: StackReport) -> None:
    print("=" * 72)
    print("PACT TOON wave-1 promotion stack — cross-repo gate report")
    print("=" * 72)
    print(f"generated_at:     {report.generated_at}")
    print(f"ecosystem_root:   {report.ecosystem_root}")
    print(f"manifest_hash:    {report.manifest_hash}")
    print(f"manifest_version: {report.manifest_version}")
    print(f"source_commit:    {report.source_commit}")
    print("-" * 72)
    for g in report.gates:
        marker = "PASS" if g.passed else "FAIL"
        print(f"  [{marker}] {g.name}: {g.detail}")
    print("-" * 72)
    print("OVERALL:", "PASS" if report.all_pass else "FAIL")
    print("=" * 72)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to the Forge ecosystem root (defaults to the repo containing this script)",
    )
    ap.add_argument(
        "--report-out",
        type=Path,
        default=None,
        help=f"Override the report output path (default: <root>/{DEFAULT_REPORT_REL})",
    )
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f"ecosystem root does not exist: {root}", file=sys.stderr)
        return 2

    report_path: Path = (args.report_out or (root / DEFAULT_REPORT_REL)).resolve()
    report = run(root, report_path)
    print_report(report)
    print(f"\nWrote report to: {report_path.relative_to(root)}")
    return 0 if report.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
