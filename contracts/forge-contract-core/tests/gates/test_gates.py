"""Tests: gate runner behavior."""

from __future__ import annotations

from forge_contract_core.gates import (
    compatibility_gate,
    fixture_gate,
    forbidden_pattern_gate,
    schema_gate,
    validator_gate,
)
from forge_contract_core.gates.run_all import run_all


def test_schema_gate_passes():
    failures = schema_gate.run()
    assert not failures, f"Schema gate failed:\n" + "\n".join(failures)


def test_fixture_gate_passes():
    failures = fixture_gate.run()
    assert not failures, f"Fixture gate failed:\n" + "\n".join(failures)


def test_validator_gate_passes():
    failures = validator_gate.run()
    assert not failures, f"Validator gate failed:\n" + "\n".join(failures)


def test_compatibility_gate_passes():
    failures = compatibility_gate.run()
    assert not failures, f"Compatibility gate failed:\n" + "\n".join(failures)


def test_forbidden_pattern_gate_passes():
    failures = forbidden_pattern_gate.run()
    assert not failures, f"Forbidden pattern gate failed:\n" + "\n".join(failures)


def test_run_all_passes_without_exit():
    result = run_all(exit_on_failure=False)
    assert result is True, "run_all() should return True when all gates pass"
