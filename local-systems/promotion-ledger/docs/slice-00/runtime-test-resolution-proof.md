# Slice 00 Runtime And Test Resolution Proof

Generated: `2026-06-19T09:13:28Z`

This gate resolves runtime and test drift after support-side proof runs. It also
records the DF support fix committed as `b2f44d4`.

## Test Proof

| Target | Command | Result |
| --- | --- | --- |
| `cortex` | `make test-runtime` | Passed; 110 tests. |
| `df-local-foundation` | `env PYTHONPATH=. /tmp/df-local-support-verify-venv/bin/python -m pytest tests -q` | Passed; 169 passed, 7 skipped. |
| `fa-local` | `cargo test` | Passed; 119 tests across integration binaries. |
| `neuronforge` | `python3 -m pytest tests -q` | Passed; 45 tests. |

DF skipped tests are live PostgreSQL integration tests gated by `DF_LOCAL` env
vars. The hermetic suite required a temporary `/tmp` venv because the repo had
no local venv; editable install exposed missing Hatch package selection, so the
declared dependencies were installed directly and repo code was loaded with
`PYTHONPATH=.`.

## Drift Result

| Metric | Before runtime/test resolution | After runtime/test resolution |
| --- | ---: | ---: |
| `intentional_app_support_adaptation` | 27 | 40 |
| `target_only_glue` | 60 | 113 |
| `unknown` | 104 | 38 |
| runtime/test unknown | 66 | 0 |
| dangerous drift | 0 | 0 |

## Remaining Gate

The remaining 38 unknowns are contracts/schema/sql, promotion evidence,
operator tooling/scripts, and repo scaffold.
