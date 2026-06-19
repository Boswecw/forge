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
| Source commit | `536b700fa7f11bf92c75e5f8c540c4b571ebb17b` |
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
| Support pytest | Blocked: system Python is missing `pydantic_settings`, `asyncpg`, and `pytest_asyncio`; no `.venv/bin/python` exists in this checkout. |
| Source analytics compute | `timeout 20s python3 -m pytest tests/api/test_analytics_compute.py -q` passed: 6 passed. |
| Source analytics routes | Blocked: `timeout 20s python3 -m pytest tests/api/test_analytics_routes.py -q` timed out with no output. |

This target-role slice is therefore documentation-opened with follow-up required
before any runtime, route, migration, or schema promotion.

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
