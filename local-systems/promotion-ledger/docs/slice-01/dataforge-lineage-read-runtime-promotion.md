# Slice 01 DF Local Lineage Read Runtime Promotion

Generated: `2026-06-19T16:37:26Z`

This slice promotes `GET /api/v1/lineage/nodes`,
`GET /api/v1/lineage/nodes/{node_id}`, and
`GET /api/v1/lineage/nodes/{node_id}/downstream` into
`df-local-foundation` as support-native read adapters. It preserves the source
lineage read shapes while keeping lineage writes, migrations, and schema
ownership held in the source local system.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `f581f2a681d50709678ddcd379e180cfee0f9c1b` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `50512dbf569795ec3744805e83005e3b8888f24d` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /api/v1/lineage/nodes`
- `GET /api/v1/lineage/nodes/{node_id}`
- `GET /api/v1/lineage/nodes/{node_id}/downstream`

Missing nodes return `404`. Reader failures return `503` with
`error_class: lineage_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `198 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source direct lineage handler proof | Passed |

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 30 | 80 |
| `source_local_hold` | 126 | 641 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 73 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `641` source-local holds, with `292`
candidate-after-target-role items and no unknown or dangerous drift.
