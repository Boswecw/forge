# Slice 01 DF Local Healing-Proposals Read Runtime Promotion

Generated: `2026-06-19T16:31:19Z`

This slice promotes `GET /api/v1/healing-proposals` and
`GET /api/v1/healing-proposals/{proposal_id}` into `df-local-foundation` as
support-native read adapters. It preserves the source proposal response shape
while keeping proposal ingest, decision updates, migrations, and schema ownership
held in the source local system.

## Decision

| Field | Value |
| --- | --- |
| Support repo | `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` |
| Support commit | `50a36e61974e80a855704ed431809f9e483f1d93` |
| Source repo | `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` |
| Source commit | `50512dbf569795ec3744805e83005e3b8888f24d` |
| Runtime promoted | Yes |
| Migrations promoted | No |
| Write routes promoted | No |

## Boundary

The support runtime exposes only:

- `GET /api/v1/healing-proposals`
- `GET /api/v1/healing-proposals/{proposal_id}`

Missing proposals return `404`. Reader failures return `503` with
`error_class: healing_proposals_read_failure`.

## Proof

| Surface | Result |
| --- | --- |
| Support full tests | `192 passed, 7 skipped, 1 warning` |
| Support touched-file lint | `All checks passed` |
| Source direct healing-proposals handler proof | Passed |

## Drift Result After Resolution

| Classification | DF Pair | All Pairs |
| --- | ---: | ---: |
| `same` | 8 | 2233 |
| `intentional_app_support_adaptation` | 27 | 77 |
| `source_local_hold` | 127 | 642 |
| `missing_from_target` | 0 | 0 |
| `target_only_glue` | 73 | 135 |
| `dangerous_drift` | 0 | 0 |
| `unknown` | 0 | 0 |

The support promotion queue now has `642` source-local holds, with `293`
candidate-after-target-role items and no unknown or dangerous drift.
