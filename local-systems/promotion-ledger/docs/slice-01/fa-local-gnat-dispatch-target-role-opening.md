# Slice 01 FA Local GNAT Dispatch Target-Role Opening

Generated: `2026-06-19T15:01:59Z`

This slice opens an FA Local support target role for future GNAT dispatch
promotion. It does not promote runtime code, copy schemas, add queues, or change
execution behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/fa-local` |
| Support commit | `2f3698deddf0e080286dd28b6cdf51dc7cd3db40` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/fa-local-operator` |
| Source commit | `5f6a7dad737f7366403a09711bc3d57a48a725cd` |
| Support document | `docs/contracts/gnat-dispatch-target-role.md` |
| Runtime promoted | No |
| Schema promoted | No |

## Boundary

The support document is target-only glue. It declares FA Local's app-support role
for GNAT execution routing while keeping the GNAT dispatch contract, validator,
and proof in the local-system FA Local repo.

GNAT dispatch remains `source_local_hold` until a later promotion slice names
exact files, source proof, support proof, service contract or adapter target,
regenerated drift report, and rollback path.

## Proof

| Surface | Result |
| --- | --- |
| FA Local support | `cargo test` passed. |
| FA Local source | `bash ci_gate.sh` passed. |

## Drift Result After Resolution

| Classification | Count |
| --- | ---: |
| `same` | 2233 |
| `intentional_app_support_adaptation` | 61 |
| `source_local_hold` | 652 |
| `missing_from_target` | 0 |
| `target_only_glue` | 132 |
| `dangerous_drift` | 0 |
| `unknown` | 0 |
