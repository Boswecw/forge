# Slice 01 Cortex GNAT Target-Role Opening

Generated: `2026-06-19T09:51:48Z`

This slice opens a Cortex support target role for future GNAT promotion. It does
not promote GNAT runtime code, add endpoints, or change AuthorForge behavior.

Status update: this target-role opening is now partially implemented by
`2026-06-19--slice-01--cortex-gnat-contract-schemas` and
`2026-06-19--slice-01--cortex-gnat-status-summary`. The receipts are
`cortex-gnat-contract-schema-promotion.md` and
`cortex-gnat-status-summary-promotion.md`; GNAT execution runtime remains
source-local.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/cortex` |
| Support commit | `f0275e42fc429434dd8a66c8283d5bad9ebf69e0` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/cortex` |
| Source commit | `98ac9ad521bb21c5956301ebfa410e520d331a70` |
| Support document | `docs/source-lanes/gnat-target-role.md` |
| Runtime promoted | No |

## Boundary

The support document is target-only glue. It declares the app-support role for
the promoted GNAT contract schema and status-summary surfaces while keeping GNAT
execution implementation and proof authority in the local-system Cortex repo.

GNAT execution runtime remains `source_local_hold` until a later promotion slice
names exact files, source proof, support proof, service contract or adapter
target, regenerated drift report, and rollback path.

## Proof

| Surface | Result |
| --- | --- |
| Cortex support schemas | `make validate` passed; 19 valid fixtures, 20 invalid fixtures, 7 schemas. |
| Cortex support runtime | `make test-runtime` passed; 110 tests. |
| Cortex source GNAT | `make test-gnats` passed; 87 tests. |

## Drift Result After Resolution

| Classification | Count |
| --- | ---: |
| `same` | 2233 |
| `intentional_app_support_adaptation` | 61 |
| `source_local_hold` | 651 |
| `missing_from_target` | 0 |
| `target_only_glue` | 131 |
| `dangerous_drift` | 0 |
| `unknown` | 0 |
