# Slice 01 NeuronForge COR GNAT Semantic Handoff Runtime Promotion

Generated: `2026-06-19T17:07:39Z`

This slice promotes `POST /api/v1/cortex/gnat-semantic-handoff` into
`neuronforge` app support as a candidate-generation receipt adapter. It accepts
referenced Cortex GNAT retrieval-package artifacts and returns an acceptance
receipt only. It does not run a model, mutate COR receipts, or create canonical
semantic truth.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/neuronforge` |
| Support commit | `69b10fe340b19ec33b1fe36006956fdad67be9f1` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/neuronforge-local-operator` |
| Source commit | `006ef57c9ece79b666581b303fce06e54debaa42` |
| Runtime promoted | Yes |
| Model execution promoted | No |
| Durable storage promoted | No |

## Boundary

The support runtime exposes only:

- `POST /api/v1/cortex/gnat-semantic-handoff`

Required invariants:

- `semantic_result_posture: non_canonical_candidate`
- `cor_receipts_mutation_allowed: false`
- raw content rejected by `extra="forbid"`
- model/resource disclosure required
- receipt only, no semantic output

## Proof

| Surface | Result |
| --- | --- |
| Support handoff test | `Ran 6 tests - OK` |
| Source handoff test | `Ran 6 tests - OK` |
| Support touched-file compile | Passed |
| Support standalone scripts | `45 passed, 0 failed`; continuity shell `27 passed, 0 failed` |
| Known environment gap | Existing support venv lacks `pytest`/`httpx`, so pytest all-tests and style-analysis route tests could not run through that path |

## Drift Result After Resolution

| Classification | NeuronForge Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 393 | 2234 |
| `intentional_app_support_adaptation` | 19 | 84 |
| `source_local_hold` | 172 | 642 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 30 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `642` source-local holds, with `291`
candidate-after-target-role items and no missing, unknown, or dangerous drift.
