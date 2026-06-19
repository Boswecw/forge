# Drift Report: fa-local-operator__fa-local

Generated: `2026-06-19T15:59:45+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/fa-local-operator`
Source branch: `master`
Source commit: `5f6a7dad737f7366403a09711bc3d57a48a725cd`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/fa-local`
Target branch: `master`
Target commit: `2f3698deddf0e080286dd28b6cdf51dc7cd3db40`

Resolutions applied: `51`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 131 |
| intentional_app_support_adaptation | 14 |
| source_local_hold | 22 |
| missing_from_target | 0 |
| target_only_glue | 15 |
| dangerous_drift | 0 |
| unknown | 0 |

## Items

| Path | Classification | Resolution | Recommended action |
| --- | --- | --- | --- |
| `.gitignore` | intentional_app_support_adaptation | `slice-00-fa-local-scaffold-modified` | Keep as support scaffold adaptation. |
| `CLAUDE.md` | intentional_app_support_adaptation | `slice-00-fa-local-scaffold-modified` | Keep as support scaffold adaptation. |
| `Cargo.toml` | intentional_app_support_adaptation | `slice-00-fa-local-scaffold-modified` | Keep as support scaffold adaptation. |
| `README.md` | intentional_app_support_adaptation | `slice-00-fa-local-scaffold-modified` | Keep as support scaffold adaptation. |
| `SYSTEM.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `ci_gate.sh` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/FLLSYSTEM.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/FLOSYSTEM.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/SYSTEM.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/faSYSTEM.md` | intentional_app_support_adaptation | `slice-00-fa-local-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after code or mirror-index changes. |
| `doc/system/00-overview.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/00_overview/01-overview-charter.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/01-architecture.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/01-overview-charter.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/02-boundaries-and-doctrine.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/03-contract-surface.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/04-validation-and-delivery.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/10-scope.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/10_service-contract/02-contract-surface.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/20-structure.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/20_runtime/03-execution-bridge-writeback.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/30-governance.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/30_dependencies/04-dependencies.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/40-change-control.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/40_governance/05-scope.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/40_governance/06-governance.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/40_governance/07-change-control.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/40_governance/08-boundaries-and-doctrine.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/50_operations/09-validation-and-delivery.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/90-appendices.md` | target_only_glue | `slice-00-fa-local-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/99_appendices/10-appendices.md` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `doc/system/BUILD.sh` | intentional_app_support_adaptation | `slice-00-fa-local-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after code or mirror-index changes. |
| `doc/system/_index.md` | intentional_app_support_adaptation | `slice-00-fa-local-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after code or mirror-index changes. |
| `doc/system/validate_snapshots.sh` | intentional_app_support_adaptation | `slice-00-fa-local-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after code or mirror-index changes. |
| `docs/contracts/gnat-dispatch-target-role.md` | target_only_glue | `slice-01-fa-local-gnat-dispatch-target-role-doc` | Keep as support target-role glue. Promote GNAT dispatch runtime/schema only through a later named slice with exact files, source proof, support proof, and regenerated drift report. |
| `reports/contract_core_gate_20260404_102436.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `reports/contract_core_gate_20260619_053018.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `reports/contract_core_gate_20260619_110109.json` | source_local_hold | `slice-01-fa-local-gnat-dispatch-proof-report` | Keep source-local as proof evidence. Do not copy into app support except as a named evidence receipt. |
| `schemas/gnat-dispatch-envelope.schema.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `src/app/intake_service.rs` | intentional_app_support_adaptation | `slice-00-fa-local-runtime-modified` | Keep as support runtime adaptation. Reconcile source authority only through a bounded Rust promotion slice. |
| `src/bin/fa_local_run.rs` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `src/domain/shared/schema.rs` | intentional_app_support_adaptation | `slice-00-fa-local-runtime-modified` | Keep as support runtime adaptation. Reconcile source authority only through a bounded Rust promotion slice. |
| `src/errors/mod.rs` | intentional_app_support_adaptation | `slice-00-fa-local-runtime-modified` | Keep as support runtime adaptation. Reconcile source authority only through a bounded Rust promotion slice. |
| `src/integrations/cortex/mod.rs` | intentional_app_support_adaptation | `slice-00-fa-local-runtime-modified` | Keep as support runtime adaptation. Reconcile source authority only through a bounded Rust promotion slice. |
| `src/integrations/df_local/mod.rs` | intentional_app_support_adaptation | `slice-00-fa-local-runtime-modified` | Keep as support runtime adaptation. Reconcile source authority only through a bounded Rust promotion slice. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-cortex-routes.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-raw-content.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-unsupported-worker.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `tests/contracts/fixtures/valid/gnat-dispatch-envelope-basic.json` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |
| `tests/contracts_loading.rs` | intentional_app_support_adaptation | `slice-00-fa-local-test-modified` | Keep paired with the FA Local support runtime adaptation. |
| `tests/gnat_dispatch.rs` | source_local_hold | `slice-00-fa-local-source-local-hold` | Keep source-local. Do not copy into app support without a bounded promotion slice, explicit support role, proof command, and regenerated drift report. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
