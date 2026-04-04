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

## Adding a new gate

1. Create a new gate module in `forge_contract_core/gates/`.
2. Implement `run() -> list[str]` returning failure messages.
3. Register the gate in `run_all.py`.
4. Add tests in `tests/gates/test_gates.py`.
5. Update this doc.
