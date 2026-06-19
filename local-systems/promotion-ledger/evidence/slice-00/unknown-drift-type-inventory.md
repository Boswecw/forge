# Slice 00 Unknown Drift Type Inventory

Generated: `2026-06-19T07:57:42+00:00`

This addendum groups the conservative `unknown` drift items by review type. It does not accept, reject, promote, or reclassify any item in the source drift reports.

## Summary By Type

| Review type | Total | Target-only | Modified in both |
| --- | ---: | ---: | ---: |
| `generated_system_documentation` | 79 | 59 | 20 |
| `target_tests_and_validation_cases` | 29 | 26 | 3 |
| `service_runtime_and_glue_code` | 28 | 14 | 14 |
| `policy_architecture_integration_docs` | 17 | 15 | 2 |
| `data_foundation_runtime_core` | 15 | 15 | 0 |
| `repo_metadata_build_and_closeout` | 14 | 1 | 13 |
| `data_sql_cli_tools` | 7 | 7 | 0 |
| `evidence_outputs_and_run_records` | 7 | 6 | 1 |
| `shared_contract_schema_validation` | 7 | 4 | 3 |
| `private_local_config` | 1 | 1 | 0 |

## Summary By Repo Pair

| Repo pair | Unknowns | Dominant types |
| --- | ---: | --- |
| `cortex__cortex` | 28 | `generated_system_documentation`=15, `service_runtime_and_glue_code`=6, `repo_metadata_build_and_closeout`=3, `shared_contract_schema_validation`=2, `policy_architecture_integration_docs`=1, `target_tests_and_validation_cases`=1 |
| `dataforge-Local__df-local-foundation` | 88 | `generated_system_documentation`=28, `target_tests_and_validation_cases`=20, `data_foundation_runtime_core`=15, `policy_architecture_integration_docs`=8, `data_sql_cli_tools`=7, `repo_metadata_build_and_closeout`=4, `service_runtime_and_glue_code`=3, `shared_contract_schema_validation`=3 |
| `fa-local-operator__fa-local` | 28 | `generated_system_documentation`=18, `repo_metadata_build_and_closeout`=4, `service_runtime_and_glue_code`=4, `shared_contract_schema_validation`=1, `target_tests_and_validation_cases`=1 |
| `forge-local-systems-runtime__forge-local-runtime-master-reference` | 6 | `generated_system_documentation`=6 |
| `neuronforge-local-operator__neuronforge` | 54 | `service_runtime_and_glue_code`=15, `generated_system_documentation`=12, `policy_architecture_integration_docs`=8, `evidence_outputs_and_run_records`=7, `target_tests_and_validation_cases`=7, `repo_metadata_build_and_closeout`=3, `private_local_config`=1, `shared_contract_schema_validation`=1 |

## Review Type Definitions

- `private_local_config`: Local private/editor configuration that should not be promoted as authority.
- `repo_metadata_build_and_closeout`: Root metadata, dependency, build, closeout, and assistant instruction files.
- `generated_system_documentation`: Generated or assembled system documentation and doc/system snapshots that need lineage review before being treated as authoritative.
- `policy_architecture_integration_docs`: Non-generated architecture, policy, integration, ADR, model-routing, or local-first documentation.
- `shared_contract_schema_validation`: Schemas, contract files, validation scripts, or shared schema code.
- `service_runtime_and_glue_code`: Executable service, adapter, translation, promotion, or runtime code that may be app-support glue or behavior drift.
- `data_foundation_runtime_core`: DF Local Foundation target-only core runtime modules for backup, export, health, lifecycle, or config.
- `data_sql_cli_tools`: Target-only SQL migrations or local CLI database tools.
- `target_tests_and_validation_cases`: Target-side tests and validation fixtures that prove target behavior but may not exist in the proving repo.
- `evidence_outputs_and_run_records`: Run outputs, evidence records, promotion examples, and registries.

## Items By Type

### `private_local_config` (1)

- `neuronforge-local-operator__neuronforge` `target_only` `.claude/settings.local.json`

### `repo_metadata_build_and_closeout` (14)

- `cortex__cortex` `modified_in_both` `.gitignore`
- `cortex__cortex` `modified_in_both` `Makefile`
- `cortex__cortex` `target_only` `requirements.txt`
- `dataforge-Local__df-local-foundation` `modified_in_both` `.gitignore`
- `dataforge-Local__df-local-foundation` `modified_in_both` `CLAUDE.md`
- `dataforge-Local__df-local-foundation` `modified_in_both` `README.md`
- `dataforge-Local__df-local-foundation` `modified_in_both` `pyproject.toml`
- `fa-local-operator__fa-local` `modified_in_both` `.gitignore`
- `fa-local-operator__fa-local` `modified_in_both` `CLAUDE.md`
- `fa-local-operator__fa-local` `modified_in_both` `Cargo.toml`
- `fa-local-operator__fa-local` `modified_in_both` `README.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `.gitignore`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `CLAUDE.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `README.md`

### `generated_system_documentation` (79)

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

### `policy_architecture_integration_docs` (17)

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

### `shared_contract_schema_validation` (7)

- `cortex__cortex` `modified_in_both` `schemas/service-status.schema.json`
- `cortex__cortex` `modified_in_both` `scripts/validate_schemas.py`
- `dataforge-Local__df-local-foundation` `target_only` `contracts/app-registration.schema.json`
- `dataforge-Local__df-local-foundation` `target_only` `contracts/health.schema.json`
- `dataforge-Local__df-local-foundation` `target_only` `contracts/migration-status.schema.json`
- `fa-local-operator__fa-local` `modified_in_both` `src/domain/shared/schema.rs`
- `neuronforge-local-operator__neuronforge` `target_only` `promotion/mirror/wave1_promotion_envelope.schema.json`

### `service_runtime_and_glue_code` (28)

- `cortex__cortex` `modified_in_both` `cortex_runtime/service_status.py`
- `cortex__cortex` `modified_in_both` `cortex_runtime/source_lanes.py`
- `cortex__cortex` `target_only` `service/__init__.py`
- `cortex__cortex` `target_only` `service/__main__.py`
- `cortex__cortex` `target_only` `service/authorforge_app.py`
- `cortex__cortex` `target_only` `service/authorforge_translation.py`
- `dataforge-Local__df-local-foundation` `modified_in_both` `app/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `app/__main__.py`
- `dataforge-Local__df-local-foundation` `modified_in_both` `app/main.py`
- `fa-local-operator__fa-local` `modified_in_both` `src/app/intake_service.rs`
- `fa-local-operator__fa-local` `modified_in_both` `src/errors/mod.rs`
- `fa-local-operator__fa-local` `modified_in_both` `src/integrations/cortex/mod.rs`
- `fa-local-operator__fa-local` `modified_in_both` `src/integrations/df_local/mod.rs`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `promotion/__init__.py`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `promotion/compatibility.py`
- `neuronforge-local-operator__neuronforge` `target_only` `promotion/envelope.py`
- `neuronforge-local-operator__neuronforge` `target_only` `promotion/mirror/wave1_promotion_envelope.mirror.json`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `promotion/run_log.py`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `scripts/style_analysis/models.py`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `scripts/verify_promotion_seam.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/authorforge_task_contract.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/authorforge_task_service.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/cloud_escalation.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/dogfood_telemetry.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/local_runtime.py`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `service/main.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/proofread_lane.py`
- `neuronforge-local-operator__neuronforge` `target_only` `service/scene_lane.py`

### `data_foundation_runtime_core` (15)

- `dataforge-Local__df-local-foundation` `target_only` `core/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/backup/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/backup/manager.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/backup/signing.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/config/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/config/settings.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/export/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/export/manager.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/health/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/health/reporter.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/lifecycle/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/lifecycle/compatibility.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/lifecycle/maintenance.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/lifecycle/manager.py`
- `dataforge-Local__df-local-foundation` `target_only` `core/lifecycle/migration_lock.py`

### `data_sql_cli_tools` (7)

- `dataforge-Local__df-local-foundation` `target_only` `sql/apps/authorforge/0001_authorforge_attach.sql`
- `dataforge-Local__df-local-foundation` `target_only` `sql/core/0001_core_foundation.sql`
- `dataforge-Local__df-local-foundation` `target_only` `sql/core/0002_core_metadata.sql`
- `dataforge-Local__df-local-foundation` `target_only` `tools/db-backup`
- `dataforge-Local__df-local-foundation` `target_only` `tools/db-export`
- `dataforge-Local__df-local-foundation` `target_only` `tools/db-restore`
- `dataforge-Local__df-local-foundation` `target_only` `tools/db-status`

### `target_tests_and_validation_cases` (29)

- `cortex__cortex` `modified_in_both` `tests/runtime/test_service_status.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/api/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/api/test_health_api.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/backup_restore/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/backup_restore/test_envelope_signing.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/backup_restore/test_restore_redteam.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/backup_restore/test_restore_validation.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/first_integration/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/first_integration/test_authorforge_attachment.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/migration_status/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/migration_status/test_migration_contract.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/migration_status/test_migration_lock.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/registration/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/registration/test_app_registration.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/registration/test_compatibility_semantics.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/registration/test_config_bypass.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/visibility_boundary/__init__.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/visibility_boundary/test_cli_authority.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/visibility_boundary/test_health_contract.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/visibility_boundary/test_health_event_discipline.py`
- `dataforge-Local__df-local-foundation` `target_only` `tests/visibility_boundary/test_status_redteam.py`
- `fa-local-operator__fa-local` `modified_in_both` `tests/contracts_loading.rs`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `tests/test-style-analysis.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_authorforge_task_contract.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_authorforge_task_service.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_cloud_escalation.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_dogfood_telemetry.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_proofread_lane.py`
- `neuronforge-local-operator__neuronforge` `target_only` `tests/test_scene_lane.py`

### `evidence_outputs_and_run_records` (7)

- `neuronforge-local-operator__neuronforge` `target_only` `docs/dogfood-cloud-quota-log.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_runs_demo.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_seam_example.md`
- `neuronforge-local-operator__neuronforge` `target_only` `docs/evidence/promotion_seam_report.json`
- `neuronforge-local-operator__neuronforge` `target_only` `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-001.md`
- `neuronforge-local-operator__neuronforge` `target_only` `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-002.md`
- `neuronforge-local-operator__neuronforge` `modified_in_both` `registry/runs.md`

## Blocking Note

All items remain `unknown` in the canonical drift reports. They continue to block promotion until resolved by human decision, backport, or explicit exception.
