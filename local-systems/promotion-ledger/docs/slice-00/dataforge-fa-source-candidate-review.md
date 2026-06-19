# Slice 00 DataForge And FA Source Candidate Review

Generated: `2026-06-19T09:30:43Z`

This reviews the remaining runtime/contract/test source-only candidates for
DataForge Local and FA Local.

## Candidate Counts

| Repo pair | Candidate count |
| --- | ---: |
| `dataforge-Local__df-local-foundation` | 77 |
| `fa-local-operator__fa-local` | 8 |

## Proof

| Surface | Command | Result |
| --- | --- | --- |
| DataForge source CI | `bash ci_gate.sh` | Passed; contract-core gate passed, 89 local tests passed, bytecode compile passed. |
| FA Local source CI | `bash ci_gate.sh` | Passed; contract-core gate passed, Cargo tests passed including 12 GNAT dispatch tests. |

## Decisions

| Surface | Posture | Reason |
| --- | --- | --- |
| DataForge local substrate | `hold_source_local` | Source has a broader Alembic/proving-slice/analytics/runtime-governance substrate than the narrower app-support foundation copy. |
| FA Local GNAT dispatch | `hold_source_local` | Source-proved dispatch depends on opening a GNAT support role across Cortex and FA Local. |

## Next Gate

No source-only runtime/contract promotion is authorized yet. Decide whether to
open a GNAT support promotion slice or keep the source-only backlog as explicit
exclusions.
