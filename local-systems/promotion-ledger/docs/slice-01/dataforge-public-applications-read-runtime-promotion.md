# Slice 01 DF Local Public Applications Read Runtime Promotion

Generated: `2026-06-19T16:14:36Z`

This slice promotes `GET /api/v1/public-applications` into
`df-local-foundation` as a support-native read adapter. It preserves the source
contract that only enabled public applications are returned.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `d93347c6963f82801a4af40bdbdb1f92cd616391` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `50512dbf569795ec3744805e83005e3b8888f24d` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /api/v1/public-applications`

If the support reader cannot read the source table, the route returns `503` with
`error_class: public_applications_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `183 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source public-applications tests | `4 passed` |

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 21 | 71 |
| `source_local_hold` | 130 | 645 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 73 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `645` source-local holds, with `296`
candidate-after-target-role items and no unknown or dangerous drift.
