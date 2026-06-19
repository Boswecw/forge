# Slice 01 DF Local Proving-Slice Queue Read Runtime Promotion

Generated: `2026-06-19T16:44:14Z`

This slice promotes `GET /api/v1/proving-slice/queue` and
`GET /api/v1/proving-slice/queue/{staged_promotion_id}` into
`df-local-foundation` as support-native read adapters. It preserves the source
derived queue/detail read model while keeping proving-slice lifecycle mutation,
artifact ingest, reconciliation, migrations, and schema ownership held in the
source local system.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `7d0e5479157f608e57507a0750a19cc2baf5fc0f` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `50512dbf569795ec3744805e83005e3b8888f24d` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /api/v1/proving-slice/queue`
- `GET /api/v1/proving-slice/queue/{staged_promotion_id}`

Missing queue entries return `404`. Reader failures return `503` with
`error_class: proving_slice_queue_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `204 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source direct proving-slice queue handler proof | Passed |

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 33 | 83 |
| `source_local_hold` | 125 | 640 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 73 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `640` source-local holds, with `291`
candidate-after-target-role items and no unknown or dangerous drift. The named
DF Local read-only candidate lane is closed; durable-truth write surfaces remain
held.
