# Slice 01 DF Local Read-Only Analytics Target-Role Opening

Generated: `2026-06-19T16:12:44Z`

This slice opens a DF Local support target role for future read-only analytics
promotion. It does not promote runtime code, copy migrations, add routes, copy
models, or change execution behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `90b3926745bc7fd5d63255602ec04b21313a8dd5` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `c6ba6d14d21cd609563516c3758b583bb2cd9484` |
| Support document | `docs/contracts/read-only-analytics-target-role.md` |
| Runtime promoted | No |
| Route promoted | No |
| Migration promoted | No |
| Schema promoted | No |

## Boundary

The support document is target-only glue. It declares DF Local app support's
future role for read-only derived analytics while keeping analytics routes,
models, services, migrations, and proof in the local-system DataForge repo.

Read-only analytics remains `source_local_hold` until a later promotion slice
names exact files, source proof, support proof, service contract or adapter
target, regenerated drift report, and rollback path.

## Proof

| Surface | Result |
| --- | --- |
| Support documentation | `git diff --check` passed. |
| Support pytest | `env PYTHONPATH=. /tmp/df-local-support-venv/bin/python -m pytest tests -q` passed: 169 passed, 7 skipped, 1 warning. |
| Source analytics compute | `timeout 20s python3 -m pytest tests/api/test_analytics_compute.py -q` passed: 6 passed. |
| Source analytics routes | `timeout 20s python3 -m pytest tests/api/test_analytics_routes.py -q` passed: 5 passed. |

This target-role slice is documentation-opened only. Runtime, route, migration,
and schema promotion still require a later named promotion slice with exact file
scope and regenerated drift.

## Drift Result After Resolution

| Classification | Count |
| --- | ---: |
| `same` | 2233 |
| `intentional_app_support_adaptation` | 61 |
| `source_local_hold` | 652 |
| `missing_from_target` | 0 |
| `target_only_glue` | 134 |
| `dangerous_drift` | 0 |
| `unknown` | 0 |
