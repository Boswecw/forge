# Slice 01 Cortex GNAT Contract Schema Promotion

Generated: `2026-06-19T17:24:14Z`

This slice promotes the Cortex GNAT contract schemas and matching valid/invalid
contract fixtures into `cortex` app support. It gives support a validated
contract surface for GNAT requests, plans, shards, receipts, summaries,
dispatch envelopes, semantic handoff, cache records, and operator run status.
It does not promote GNAT runtime modules, workers, `gnat_core`, service
endpoints, queues, watchers, retry schedulers, persistence, or AuthorForge
behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/cortex` |
| Support commit | `a85a72bff50f9b9e7f0d2991926bc98e002a09e3` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/cortex` |
| Source commit | `98ac9ad521bb21c5956301ebfa410e520d331a70` |
| Contract schemas promoted | Yes |
| Runtime promoted | No |
| Endpoints promoted | No |
| AuthorForge behavior changed | No |

## Boundary

Promoted schemas:

- `GnatRunRequest.v1`
- `GnatRunPlan.v1`
- `GnatShard.v1`
- `GnatWorkerReceipt.v1`
- `GnatRunSummary.v1`
- `GnatDispatchEnvelope.v1`
- `GnatSemanticHandoff.v1`
- `GnatCacheRecord.v1`
- `GnatOperatorRunStatus.v1`

Runtime remains source-local until a later promotion slice names exact runtime
files, source proof, support proof, service contract or adapter target,
regenerated drift report, and rollback path.

## Proof

| Surface | Result |
| --- | --- |
| Support schema validation | `28` valid fixtures, `44` invalid fixtures, `16` schemas |
| Support runtime suite | `110` tests passed |
| Source schema validation | `28` valid fixtures, `44` invalid fixtures, `16` schemas |
| Source GNAT suite | `87` tests passed |

## Drift Result After Resolution

| Classification | Cortex Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 1629 | 2285 |
| `intentional_app_support_adaptation` | 13 | 82 |
| `source_local_hold` | 277 | 592 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 16 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `592` source-local holds, with `241`
candidate-after-target-role items and no missing, unknown, or dangerous drift.
