# 05 — Gate Runner Contract

## Canonical entry point

```bash
python -m forge_contract_core.gates.run_all
```

All direct proving-slice participating repos must wire this command into their CI. They may wrap it but must not replace it with weaker local-only checks.

Exit codes:
- `0` — all gates pass
- `1` — one or more gates failed

## Gate categories

| Gate | Module | What it checks |
|---|---|---|
| `schema` | `gates/schema_gate.py` | All admitted schemas exist and are valid JSON Schema |
| `fixture_corpus` | `gates/fixture_gate.py` | Valid fixtures pass, invalid fixtures fail, duplicate fixtures are structurally valid |
| `validator_correctness` | `gates/validator_gate.py` | Idempotency key stability, reference grammar, unsupported family/version rejection |
| `compatibility` | `gates/compatibility_gate.py` | Registry and compatibility notes are consistent |
| `forbidden_patterns` | `gates/forbidden_pattern_gate.py` | Forbidden patterns file is present, well-formed, and has no duplicate IDs |

## Gate failure behavior

Gate failures are blocking, not advisory. If any gate fails, the runner exits with code 1 and CI must fail.

## Temporary waivers

Temporary waivers may be issued for legitimate blockers. They must be:
- Explicit (documented in a waiver record)
- Time-bounded
- Governance-approved
- Visible (not hidden in CI configuration)

Waivers must never become permanent compatibility workarounds.

## Participating repos and CI gate scripts

Each proving-slice participating repo carries a `ci_gate.sh` at its root. These
scripts resolve the contract-core path relative to the ecosystem root and invoke
the canonical gate runner.

| Repo | Script | Path resolution |
|------|--------|-----------------|
| `contracts/forge-contract-core` | `ci_gate.sh` | Self |
| `Local systems/dataforge-Local` | `ci_gate.sh` | `../../contracts/forge-contract-core` |
| `Cloud Systems/DataForge` | `ci_gate.sh` | `../../contracts/forge-contract-core` |

All scripts use the contract-core `.venv/bin/python` if present, falling back to the
local venv or system Python.

## Scenario and adversarial test suite

`tests/scenario/` contains two test files that validate the full proving-slice
contract path without a live database:

| File | Coverage |
|------|---------|
| `test_proving_slice_scenarios.py` | 7 named scenarios: happy path, family gate, invalid payload rejection, idempotency boundary, receipt structure, lineage chain, and admission evidence |
| `test_adversarial.py` | 8 adversarial cases: tampered idempotency key, cross-family key smuggling, forbidden family injection, unadmitted family variants (incl. SQL injection), version forgery (v0 + v999), unadmitted producers, empty payload bypass, null required field |

These tests are included in the default `pytest tests/` run and must stay green.

## Adding a new gate

1. Create a new gate module in `forge_contract_core/gates/`.
2. Implement `run() -> list[str]` returning failure messages.
3. Register the gate in `run_all.py`.
4. Add tests in `tests/gates/test_gates.py`.
5. Update this doc.
