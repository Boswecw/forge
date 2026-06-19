# Slice 00 Documentation Drift Review

Generated: `2026-06-19T07:58:24+00:00`

This review applies Charlie Boswell's documentation rule to the conservative `unknown` drift items. It does not reclassify the canonical drift reports; all listed items remain blocking until reviewed.

## Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror, not the home for general documentation.

## Summary

Documentation-related unknowns: `109`

| Lane | Total | Target-only | Modified in both | First action |
| --- | ---: | ---: | ---: | --- |
| `doc_system_code_mirror` | 79 | 59 | 20 | Verify against live code and repo-local build/validation before accepting; do not treat as documentation promotion. |
| `docs_condensed_documentation` | 17 | 15 | 2 | Condense if inactive; if it contains foundational authority, backport to the proving repo before promotion. |
| `evidence_or_run_record` | 7 | 6 | 1 | Keep as evidence only; link from /docs summaries when needed. |
| `root_pointer_or_agent_metadata` | 6 | 0 | 6 | Condense root docs to pointers; leave CLAUDE as metadata unless it contains broad human documentation. |

## Completed Documentation Cleanup

- Moved misplaced docs into `/docs` for Cortex and NeuronForge.
- Condensed app-support root READMEs for DF Local Foundation, NeuronForge, and FA Local.
- Moved DF Local Foundation closeout evidence from root to `docs/closeout-initial-governed-implementation.md`.
- Left `CLAUDE.md` files in place as repo-local agent metadata.
- Ran all five app-support `/doc/system/BUILD.sh` mirror builders successfully.

## By Repo Pair

| Repo pair | Documentation unknowns | Lane counts |
| --- | ---: | --- |
| `cortex__cortex` | 16 | `doc_system_code_mirror`=15, `docs_condensed_documentation`=1 |
| `dataforge-Local__df-local-foundation` | 38 | `doc_system_code_mirror`=28, `docs_condensed_documentation`=8, `root_pointer_or_agent_metadata`=2 |
| `fa-local-operator__fa-local` | 20 | `doc_system_code_mirror`=18, `root_pointer_or_agent_metadata`=2 |
| `forge-local-systems-runtime__forge-local-runtime-master-reference` | 6 | `doc_system_code_mirror`=6 |
| `neuronforge-local-operator__neuronforge` | 29 | `doc_system_code_mirror`=12, `docs_condensed_documentation`=8, `evidence_or_run_record`=7, `root_pointer_or_agent_metadata`=2 |

## Lanes

### `doc_system_code_mirror` (79)

/doc/system and generated system outputs. Review as code mirror, not general documentation.

- `cortex__cortex` `modified_in_both` `SYSTEM.md`
- `cortex__cortex` `target_only` `doc/CRTSYSTEM.md`
- `cortex__cortex` `modified_in_both` `doc/SYSTEM.md`
- `cortex__cortex` `modified_in_both` `doc/cxSYSTEM.md`
- `cortex__cortex` `target_only` `doc/system/00-overview.md`
- `cortex__cortex` `target_only` `doc/system/01-architecture.md`
- `cortex__cortex` `modified_in_both` `doc/system/04-validation-and-delivery.md`
- `cortex__cortex` `target_only` `doc/system/10-scope.md`
- `cortex__cortex` `target_only` `doc/system/20-structure.md`
- `cortex__cortex` `target_only` `doc/system/30-governance.md`
- `cortex__cortex` `target_only` `doc/system/40-change-control.md`
- `cortex__cortex` `target_only` `doc/system/90-appendices.md`
- `cortex__cortex` `modified_in_both` `doc/system/BUILD.sh`
- `cortex__cortex` `modified_in_both` `doc/system/_index.md`
- `cortex__cortex` `target_only` `doc/system/validate_snapshots.sh`
- `dataforge-Local__df-local-foundation` `target_only` `SYSTEM.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/DFLSYSTEM.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/SYSTEM.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/00-overview.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/01-architecture.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/01-overview-philosophy.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/02-architecture.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/03-tech-stack.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/04-project-structure.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/05-configuration.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/06-design-system.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/07-frontend.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/08-api-layer.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/09-backend.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/10-ecosystem-integration.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/10-scope.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/11-database-schema.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/12-ai-integration.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/13-error-handling.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/14-testing-infrastructure.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/15-handover-migration-notes.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/20-structure.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/30-governance.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/40-change-control.md`
- `dataforge-Local__df-local-foundation` `target_only` `doc/system/90-appendices.md`
- `dataforge-Local__df-local-foundation` `modified_in_both` `doc/system/BUILD.sh`
- `dataforge-Local__df-local-foundation` `modified_in_both` `doc/system/_index.md`
- `dataforge-Local__df-local-foundation` `modified_in_both` `doc/system/validate_snapshots.sh`
- `fa-local-operator__fa-local` `target_only` `SYSTEM.md`
- `fa-local-operator__fa-local` `target_only` `doc/FLLSYSTEM.md`
- `fa-local-operator__fa-local` `target_only` `doc/SYSTEM.md`
- `fa-local-operator__fa-local` `modified_in_both` `doc/faSYSTEM.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/00-overview.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/01-architecture.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/01-overview-charter.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/02-boundaries-and-doctrine.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/03-contract-surface.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/04-validation-and-delivery.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/10-scope.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/20-structure.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/30-governance.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/40-change-control.md`
- `fa-local-operator__fa-local` `target_only` `doc/system/90-appendices.md`
- `fa-local-operator__fa-local` `modified_in_both` `doc/system/BUILD.sh`
- `fa-local-operator__fa-local` `modified_in_both` `doc/system/_index.md`
- `fa-local-operator__fa-local` `modified_in_both` `doc/system/validate_snapshots.sh`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `target_only` `doc/FOLSYSTEM.md`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `modified_in_both` `doc/SYSTEM.md`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `modified_in_both` `doc/system/90-appendices.md`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `modified_in_both` `doc/system/BUILD.sh`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `modified_in_both` `doc/system/_index.md`
- `forge-local-systems-runtime__forge-local-runtime-master-reference` `modified_in_both` `doc/system/validate_snapshots.sh`
- `neuronforge-local-operator__neuronforge` `target_only` `SYSTEM.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/NRNSYSTEM.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/00-overview.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/01-architecture.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/10-scope.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/20-structure.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/30-governance.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/40-change-control.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/90-appendices.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `doc/system/BUILD.sh`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `doc/system/_index.md`
- `neuronforge-local-operator__neuronforge` `target_only` `doc/system/validate_snapshots.sh`

### `docs_condensed_documentation` (17)

Material already under /docs. Keep only if condensed or actively driving implementation.

- `cortex__cortex` `target_only` `docs/service/authorforge-service.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/app-integration-contract.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/architecture.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/backup-export-restore.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/closeout-initial-governed-implementation.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/df-local-foundation_extended_roadmap.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/migration-doctrine.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/operational-visibility.md`
- `dataforge-Local__df-local-foundation` `target_only` `docs/privacy-doctrine.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/adr/ADR-2026-04-18-promotion-truth-upstream.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/authorforge-task-envelope-contract.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/authorforge-task-router-plan.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/local-first-cloud-assist-boundary.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/model-routing-doctrine.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `docs/neuronforge_architecture_spec.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `docs/neuronforge_extended_roadmap.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/registries/task-lanes.md`

### `root_pointer_or_agent_metadata` (6)

Root README, CLAUDE, and closeout files. Root README files should be short pointers; CLAUDE files are repo-local agent metadata.

- `dataforge-Local__df-local-foundation` `modified_in_both` `CLAUDE.md`
- `dataforge-Local__df-local-foundation` `modified_in_both` `README.md`
- `fa-local-operator__fa-local` `modified_in_both` `CLAUDE.md`
- `fa-local-operator__fa-local` `modified_in_both` `README.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `CLAUDE.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `README.md`

### `evidence_or_run_record` (7)

Evidence, output, run logs, and report records. These may remain outside /docs but must not become doctrine.

- `neuronforge-local-operator__neuronforge` `target_only` `docs/dogfood-cloud-quota-log.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_runs_demo.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_seam_example.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_seam_report.json`
- `neuronforge-local-operator__neuronforge` `target_only` `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-001.md`
- `neuronforge-local-operator__neuronforge` `target_only` `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-002.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `registry/runs.md`

## Next Documentation Pass

1. Treat every `/doc/system` item as code mirror drift and verify it from the proving repo, not from the app-support target.
2. Review the `/docs` condensed-documentation lane for inactive plans that still need shorter status records.
3. Keep evidence and run records as receipts only; link them from condensed `/docs` summaries when they matter.

## Blocking Note

These items remain `unknown` in the canonical drift reports. Documentation drift still blocks promotion until Charlie reviews, backports, or explicitly excepts it.
