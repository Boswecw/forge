# Forge Root Documentation Consolidation Report (Rev 1)

## Scope

Root governance repo surface only:

- worked only in `/home/charlie/Forge/ecosystem`
- nested implementation repos were not reorganized
- no documentation was silently deleted

## Target Root Documentation Surface

Intended minimal root documentation surface after cleanup:

- `README.md`
- `PORT_REGISTRY.md`
- `CLAUDE.md`

Rationale:

- `README.md` is the human/operator entrypoint
- `PORT_REGISTRY.md` is a canonical root governance artifact with direct operational value
- `CLAUDE.md` is an intentional AI-session entrypoint file and belongs at the root by tool contract

Everything else was evaluated for relocation.

## Initial Inventory And Classification

| Path | Doc type | Likely role | Recommended action |
|---|---|---|---|
| `README.md` | root overview | governance repo entrypoint | keep at root |
| `PORT_REGISTRY.md` | canonical registry | root governance source of truth for ports | keep at root |
| `CLAUDE.md` | AI context file | tool-facing root entrypoint | keep at root |
| `DOCUMENTATION_INDEX.md` | documentation map | docs hub index, not a root entrypoint | move to `docs/` |
| `NEUROFORGE_GOVERNANCE_HARDENING_PROMPT.md` | implementation prompt | one-off planning/prompt artifact | move to archive/holding |
| `PRESSFORGE_EAE_IMPLEMENTATION_SPEC_v1.md` | implementation spec | loose product/system spec, not part of active root surface | move to archive/holding |
| `RAKE_PRIVATE_SOURCE_INGESTION_PROMPTING_PLAN.md` | prompting/implementation plan | loose planning artifact | move to archive/holding |
| `VERITAS_FORGE_PROOF_ENGINE_METADATA_v1.md` | metadata plan | loose planning artifact | move to archive/holding |
| `VERITAS_FOUNDATION_T7_METADATA_v1.md` | metadata plan | loose planning artifact | move to archive/holding |
| `VERITAS_T8_T10_IMPLEMENTATION_PLAN.md` | implementation plan | loose planning artifact | move to archive/holding |
| `plan_v_3_smith_multi_stack_static_analysis_registry_build_guard_gates_aligned_to_forge_smithy_current_architecture.md` | implementation plan | loose planning artifact | move to archive/holding |

Notes:

- root-level non-document files such as `package.json`, shell scripts, deployment YAML, and artifact-like files without markdown extensions were outside this documentation-only consolidation slice
- unclear plan/spec ownership was handled conservatively by moving files into an explicit holding area instead of guessing their canonical destination

## Folders Created

- `docs/archive/root-holding/`
- `reports/`

## Files Moved

Moved into the active docs hub:

- `DOCUMENTATION_INDEX.md` -> `docs/DOCUMENTATION_INDEX.md`

Moved into explicit archive/holding:

- `NEUROFORGE_GOVERNANCE_HARDENING_PROMPT.md` -> `docs/archive/root-holding/NEUROFORGE_GOVERNANCE_HARDENING_PROMPT.md`
- `PRESSFORGE_EAE_IMPLEMENTATION_SPEC_v1.md` -> `docs/archive/root-holding/PRESSFORGE_EAE_IMPLEMENTATION_SPEC_v1.md`
- `RAKE_PRIVATE_SOURCE_INGESTION_PROMPTING_PLAN.md` -> `docs/archive/root-holding/RAKE_PRIVATE_SOURCE_INGESTION_PROMPTING_PLAN.md`
- `VERITAS_FORGE_PROOF_ENGINE_METADATA_v1.md` -> `docs/archive/root-holding/VERITAS_FORGE_PROOF_ENGINE_METADATA_v1.md`
- `VERITAS_FOUNDATION_T7_METADATA_v1.md` -> `docs/archive/root-holding/VERITAS_FOUNDATION_T7_METADATA_v1.md`
- `VERITAS_T8_T10_IMPLEMENTATION_PLAN.md` -> `docs/archive/root-holding/VERITAS_T8_T10_IMPLEMENTATION_PLAN.md`
- `plan_v_3_smith_multi_stack_static_analysis_registry_build_guard_gates_aligned_to_forge_smithy_current_architecture.md` -> `docs/archive/root-holding/plan_v_3_smith_multi_stack_static_analysis_registry_build_guard_gates_aligned_to_forge_smithy_current_architecture.md`

## References Updated

Updated local references so the moved documentation map still resolves cleanly:

- `README.md`
- `docs/README.md`
- `docs/DOCUMENTATION_INDEX.md`

`docs/DOCUMENTATION_INDEX.md` was also lightly refreshed to remove obviously stale protocol wording and to document the new `docs/archive/root-holding/` destination.

## Ambiguous Items Left For Follow-Up

These files were preserved in `docs/archive/root-holding/` because their active ownership/status was not clear enough to justify immediate promotion into `docs/canonical/`, `docs/plans/active/`, or another governed surface:

- `NEUROFORGE_GOVERNANCE_HARDENING_PROMPT.md`
- `PRESSFORGE_EAE_IMPLEMENTATION_SPEC_v1.md`
- `RAKE_PRIVATE_SOURCE_INGESTION_PROMPTING_PLAN.md`
- `VERITAS_FORGE_PROOF_ENGINE_METADATA_v1.md`
- `VERITAS_FOUNDATION_T7_METADATA_v1.md`
- `VERITAS_T8_T10_IMPLEMENTATION_PLAN.md`
- `plan_v_3_smith_multi_stack_static_analysis_registry_build_guard_gates_aligned_to_forge_smithy_current_architecture.md`

Follow-up question for each: should it be promoted into an active governed docs surface, or remain archived/holding?

## Final Root Documentation Surface Summary

Root markdown surface after consolidation:

- `README.md`
- `PORT_REGISTRY.md`
- `CLAUDE.md`

This is materially cleaner than the pre-cleanup root and leaves the governance repo with an explicit, minimal documentation surface.

## Verification Summary

- nested repos were not reorganized
- moved files still exist in intentional locations
- obvious local references to `DOCUMENTATION_INDEX.md` were updated
- no root markdown files were silently deleted
