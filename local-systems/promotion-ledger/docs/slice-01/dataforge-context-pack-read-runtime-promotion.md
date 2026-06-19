# Slice 01 DF Local Context-Pack Read Runtime Promotion

Generated: `2026-06-19T16:21:58Z`

This slice promotes `GET /df/rag/context-pack/{context_pack_id}` into
`df-local-foundation` as a support-native read adapter. It preserves the
NeuroForge-compatible source response shape while keeping context-pack writes
and schema ownership held in the source local system.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `283017da7d078ed5c29e38e2bf2e4b731e27bb4e` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `50512dbf569795ec3744805e83005e3b8888f24d` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /df/rag/context-pack/{context_pack_id}`

Missing packs return `404`. Reader failures return `503` with
`error_class: context_pack_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `187 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source direct context-pack handler proof | Passed |

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 24 | 74 |
| `source_local_hold` | 128 | 643 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 73 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `643` source-local holds, with `294`
candidate-after-target-role items and no unknown or dangerous drift.
