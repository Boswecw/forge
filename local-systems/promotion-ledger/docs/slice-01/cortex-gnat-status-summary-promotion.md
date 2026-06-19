# Slice 01 Cortex GNAT Status Summary Promotion

Generated: `2026-06-19T17:36:38Z`

This slice promotes only the Cortex GNAT service-status summary into `cortex`
app support. It gives support an honest GNAT readiness surface: serial proof by
default, admitted worker types from source lanes, capped concurrency, FA Local
required for parallel readiness, and serial fallback available.

It does not promote GNAT planners, workers, dispatch, persistence, retrieval
preparation, semantic handoff, execution runners, `gnat_core`, endpoints, queue,
watcher, retry, scheduler, or AuthorForge behavior.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/cortex` |
| Support commit | `c6d508fd6cb135b45ebd2a93636e30c077686bec` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/cortex` |
| Source commit | `98ac9ad521bb21c5956301ebfa410e520d331a70` |
| Status summary promoted | Yes |
| Execution runtime promoted | No |
| Endpoints promoted | No |
| AuthorForge behavior changed | No |

## Boundary

Promoted support-safe files:

- `cortex_runtime/gnats/__init__.py`
- `cortex_runtime/gnats/models.py`
- `cortex_runtime/gnats/status.py`
- `cortex_runtime/source_lanes.py`
- `cortex_runtime/service_status.py`
- `schemas/service-status.schema.json`
- `tests/runtime/test_gnat_status.py`
- `docs/source-lanes/gnat-target-role.md`

The support `gnats` package is intentionally trimmed. It exports only
`FaLocalCapabilityState` and `gnat_status_summary`; the execution runtime stays
source-local.

## Proof

| Surface | Result |
| --- | --- |
| Support GNAT status test | `3` tests passed |
| Support schema validation | `28` valid fixtures, `44` invalid fixtures, `16` schemas |
| Support runtime suite | `113` tests passed |
| Source GNAT status test | `3` tests passed |
| Source schema validation | `28` valid fixtures, `44` invalid fixtures, `16` schemas |
| Source GNAT suite | `87` tests passed |

## Drift Result After Resolution

| Classification | Cortex Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 1632 | 2288 |
| `intentional_app_support_adaptation` | 14 | 83 |
| `source_local_hold` | 273 | 588 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 16 | 136 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `588` source-local holds, with `237`
candidate-after-target-role items and no missing, unknown, or dangerous drift.
