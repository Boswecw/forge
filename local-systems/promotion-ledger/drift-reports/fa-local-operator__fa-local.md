# Drift Report: fa-local-operator__fa-local

Generated: `2026-06-19T08:18:09+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/fa-local-operator`
Source branch: `master`
Source commit: `5f6a7dad737f7366403a09711bc3d57a48a725cd`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/fa-local`
Target branch: `master`
Target commit: `6608a60f40e47a5473cd85a1fbbf9e587e053509`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 131 |
| intentional_app_support_adaptation | 0 |
| missing_from_target | 20 |
| target_only_glue | 0 |
| dangerous_drift | 0 |
| unknown | 28 |

## Items

| Path | Classification | Recommended action |
| --- | --- | --- |
| `.gitignore` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `CLAUDE.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `Cargo.toml` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `README.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `SYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `ci_gate.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/FLLSYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/FLOSYSTEM.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/SYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/faSYSTEM.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `doc/system/00-overview.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/00_overview/01-overview-charter.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/01-architecture.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/01-overview-charter.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/02-boundaries-and-doctrine.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/03-contract-surface.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/04-validation-and-delivery.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/10-scope.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/10_service-contract/02-contract-surface.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/20-structure.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/20_runtime/03-execution-bridge-writeback.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/30-governance.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/30_dependencies/04-dependencies.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40-change-control.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/40_governance/05-scope.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40_governance/06-governance.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40_governance/07-change-control.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40_governance/08-boundaries-and-doctrine.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/50_operations/09-validation-and-delivery.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/90-appendices.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/99_appendices/10-appendices.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/BUILD.sh` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `doc/system/_index.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `doc/system/validate_snapshots.sh` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `reports/contract_core_gate_20260404_102436.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-dispatch-envelope.schema.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/app/intake_service.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `src/bin/fa_local_run.rs` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/domain/shared/schema.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `src/errors/mod.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `src/integrations/cortex/mod.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `src/integrations/df_local/mod.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-cortex-routes.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-raw-content.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-unsupported-worker.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-dispatch-envelope-basic.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts_loading.rs` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `tests/gnat_dispatch.rs` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
