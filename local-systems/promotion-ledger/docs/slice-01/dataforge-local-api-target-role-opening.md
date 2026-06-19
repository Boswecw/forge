# Slice 01 DF Local API Target-Role Opening

Generated: `2026-06-19T15:58:37Z`

This slice opens a support target role for the remaining DF Local source API
candidates. It does not promote runtime code, routes, migrations, schemas, or
write behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `e0f56d6696c000ff44f5161d68daf0f0c58c197a` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `c6ba6d14d21cd609563516c3758b583bb2cd9484` |
| Support document | `docs/contracts/local-api-target-roles.md` |
| Runtime promoted | No |

## Boundary

The document separates future read-only support adapter candidates from
durable-truth mutation endpoints. The mutation endpoints remain held until a
later slice proves schema ownership, idempotency, authorization, rollback, and
consumer compatibility.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `179 passed, 7 skipped, 1 warning` |
| Source proving-slice read models | `31 passed` |
| Source context-pack direct handler proof | Passed |
| Source context-pack TestClient harness | Blocked by local TestClient hang; source unchanged |

## Next Gate

Select one read-only candidate lane and create a runtime promotion slice with
exact files, source proof, support proof, migration/schema decision, regenerated
drift report, and rollback path.
