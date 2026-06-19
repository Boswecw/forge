# Slice 01 DF Local Read-Only Analytics Runtime Promotion

Generated: `2026-06-19T15:53:14Z`

This slice promotes the DF Local read-only analytics runtime into
`df-local-foundation` as support-native adapters. It keeps the source envelope
and compute semantics while adapting the database boundary to the support
app's FastAPI/asyncpg foundation.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `e3c1e831dbaa8d3cf3ace31e6829ab243abcc4a6` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `c6ba6d14d21cd609563516c3758b583bb2cd9484` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /api/v1/analytics/overview`
- `GET /api/v1/analytics/systems`
- `GET /api/v1/analytics/queue`
- `GET /api/v1/analytics/freshness`

If the support reader cannot read the analytics source tables, the route returns
`503` with `error_class: analytics_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `179 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source analytics tests | `11 passed` |

Whole-repo `ruff check .` still has pre-existing failures outside this slice, so
the promotion proof uses a touched-file lint gate plus the full support pytest
suite.

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 18 | 68 |
| `source_local_hold` | 130 | 645 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 72 | 134 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `645` source-local holds, with `297`
candidate-after-target-role items and no unknown or dangerous drift.
