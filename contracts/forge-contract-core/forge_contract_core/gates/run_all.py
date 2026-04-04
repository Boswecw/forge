"""Canonical gate runner for forge-contract-core.

Entry point: python -m forge_contract_core.gates.run_all

All participating repos must wire this command into their CI. They may wrap it
but must not replace it with weaker local-only checks.

Exit codes:
  0 — all gates pass
  1 — one or more gates failed
"""

from __future__ import annotations

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


def run_all(*, exit_on_failure: bool = True) -> bool:
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

    if not all_passed and exit_on_failure:
        sys.exit(1)

    return all_passed


if __name__ == "__main__":
    run_all()
