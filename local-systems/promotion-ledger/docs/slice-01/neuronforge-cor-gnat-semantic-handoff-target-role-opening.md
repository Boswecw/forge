# Slice 01 NeuronForge COR GNAT Semantic Handoff Target-Role Opening

Generated: `2026-06-19T15:36:18Z`

This slice opens a NeuronForge support target role for future COR GNAT semantic
handoff promotion. It does not promote runtime code, copy schemas, add routes,
run a model, or change execution behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/neuronforge` |
| Support commit | `4aa1e98666dbb39380af7af93fe41e07a1759cb1` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/neuronforge-local-operator` |
| Source commit | `006ef57c9ece79b666581b303fce06e54debaa42` |
| Support document | `docs/contracts/cor-gnat-semantic-handoff-target-role.md` |
| Runtime promoted | No |
| Route promoted | No |
| Schema promoted | No |

## Boundary

The support document is target-only glue. It declares NeuronForge app support's
future role for COR GNAT semantic handoff while keeping handoff contract,
validator, route, and proof in the local-system NeuronForge repo.

COR GNAT semantic handoff remains `source_local_hold` until a later promotion
slice names exact files, source proof, support proof, service contract or adapter
target, regenerated drift report, and rollback path.

## Proof

| Surface | Result |
| --- | --- |
| NeuronForge support | `python3 -m pytest tests -q` passed: 45 passed, 3 warnings. |
| NeuronForge source | `python3 tests/test-cor-gnat-semantic-handoff.py` passed: 6 tests OK. |

The broader source `bash scripts/run-tests.sh` gate was attempted but interrupted
after no new output for more than two minutes inside the route-oriented
style-analysis suite; this target-role slice therefore records the focused COR
GNAT handoff proof as its source gate.

## Drift Result After Resolution

| Classification | Count |
| --- | ---: |
| `same` | 2233 |
| `intentional_app_support_adaptation` | 61 |
| `source_local_hold` | 652 |
| `missing_from_target` | 0 |
| `target_only_glue` | 133 |
| `dangerous_drift` | 0 |
| `unknown` | 0 |
