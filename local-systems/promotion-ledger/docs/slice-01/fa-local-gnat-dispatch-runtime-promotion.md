# Slice 01 FA Local GNAT Dispatch Runtime Promotion

Generated: `2026-06-19T17:20:11Z`

This slice promotes FA Local GNAT dispatch into `fa-local` app support as a
bounded contract/schema and validator surface. It validates Cortex-originated
`GnatDispatchEnvelope.v1` requests and decides whether FA Local can admit
bounded local dispatch or whether an explicit serial fallback is allowed. It
does not add execution queues, watchers, retry schedulers, durable GNAT records,
semantic labels, or canonical content behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/fa-local` |
| Support commit | `457c2838f9df2f631cb8c93906b6e139a53e71be` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/fa-local-operator` |
| Source commit | `5f6a7dad737f7366403a09711bc3d57a48a725cd` |
| Runtime promoted | Yes |
| Schema promoted | Yes |
| Execution service behavior promoted | No |
| Durable storage promoted | No |

## Boundary

The support runtime promotes:

- `GnatDispatchEnvelope.v1`
- Cortex integration validator/types
- schema registry wiring
- diagnostic/status CLI binary
- GNAT dispatch proof tests and contract fixture coverage

Required invariants:

- FA Local owns execution routing
- Cortex validates receipts
- retry policy is infrastructure-only
- requested concurrency is clamped to admitted FA capability
- serial fallback is explicit and contract-authorized
- unsupported worker types, unsupported contract versions, malformed shard
  plans, and Cortex-owned execution routing are denied

## Proof

| Surface | Result |
| --- | --- |
| Source GNAT dispatch test | `12 passed, 0 failed` |
| Support GNAT dispatch test | `12 passed, 0 failed` |
| Support contract loading | `13 passed, 0 failed` |
| Support full Cargo suite | `147 passed, 0 failed` |
| Support format | `cargo fmt --check` passed |
| Source format note | Source `cargo fmt --check` reports pre-existing formatting diffs; support promoted files are formatted |

## Drift Result After Resolution

| Classification | FA Local Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 140 | 2243 |
| `intentional_app_support_adaptation` | 12 | 82 |
| `source_local_hold` | 15 | 634 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 15 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `634` source-local holds, with `283`
candidate-after-target-role items and no missing, unknown, or dangerous drift.
