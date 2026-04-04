"""Canonical gate runner for forge-contract-core.

Entry point: python -m forge_contract_core.gates.run_all

All participating repos must wire this command into their CI. They may wrap it
but must not replace it with weaker local-only checks.

Exit codes:
  0 — all gates pass
  1 — one or more gates failed

Optional flags:
  --report-out FILE   Write a JSON evidence report to FILE in addition to
                      printing results to stdout. The report records the gate
                      set, pass/fail per gate, commit sha, and timestamp.
                      The directory is created if it does not exist.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time

from forge_contract_core.gates import (
    compatibility_gate,
    fixture_gate,
    forbidden_pattern_gate,
    schema_gate,
    validator_gate,
)

_GATES = [
    ("schema", schema_gate),
    ("fixture_corpus", fixture_gate),
    ("validator_correctness", validator_gate),
    ("compatibility", compatibility_gate),
    ("forbidden_patterns", forbidden_pattern_gate),
]

_WIDTH = 72


def _banner(text: str) -> None:
    print(f"\n{'─' * _WIDTH}")
    print(f"  forge-contract-core gate runner — {text}")
    print(f"{'─' * _WIDTH}")


def _section(name: str) -> None:
    print(f"\n[gate: {name}]")


def _current_commit_sha() -> str:
    """Best-effort commit SHA: env var override, then git command, else 'unknown'."""
    for env_var in ("GIT_COMMIT", "GITHUB_SHA", "CI_COMMIT_SHA"):
        val = os.environ.get(env_var, "").strip()
        if val:
            return val
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        return sha if sha else "unknown"
    except Exception:
        return "unknown"


def _write_report(
    path: str,
    repo: str,
    results: list[tuple[str, bool, list[str]]],
    all_passed: bool,
    elapsed: float,
) -> None:
    report = {
        "repo": repo,
        "gate_set": "proving_slice_v1",
        "commit_sha": _current_commit_sha(),
        "run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 3),
        "overall": "PASS" if all_passed else "FAIL",
        "gates": [
            {
                "name": name,
                "passed": passed,
                "failures": failures,
            }
            for name, passed, failures in results
        ],
    }
    dir_part = os.path.dirname(path)
    if dir_part:
        os.makedirs(dir_part, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"  report written: {path}")


def run_all(
    *,
    exit_on_failure: bool = True,
    report_out: str | None = None,
    repo: str = "forge-contract-core",
) -> bool:
    """Run all gates and return True if all pass."""
    _banner("proving slice v1")
    start = time.monotonic()

    all_passed = True
    results: list[tuple[str, bool, list[str]]] = []

    for gate_name, gate_module in _GATES:
        _section(gate_name)
        failures = gate_module.run()
        passed = len(failures) == 0
        results.append((gate_name, passed, failures))
        if passed:
            print(f"  ✓ PASS")
        else:
            all_passed = False
            for msg in failures:
                print(f"  ✗ {msg}")

    elapsed = time.monotonic() - start
    _banner(f"{'PASS' if all_passed else 'FAIL'} — {elapsed:.2f}s")

    for gate_name, passed, failures in results:
        status = "PASS" if passed else f"FAIL ({len(failures)} issue(s))"
        print(f"  {gate_name:<30} {status}")

    if report_out:
        _write_report(report_out, repo, results, all_passed, elapsed)

    if not all_passed and exit_on_failure:
        sys.exit(1)

    return all_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="forge-contract-core canonical gate runner"
    )
    parser.add_argument(
        "--report-out",
        default=None,
        metavar="FILE",
        help="Write JSON evidence report to FILE (directory created if needed)",
    )
    parser.add_argument(
        "--repo",
        default="forge-contract-core",
        help="Repo name to embed in the report (default: forge-contract-core)",
    )
    args = parser.parse_args()
    run_all(report_out=args.report_out, repo=args.repo)
