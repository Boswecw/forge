# Drift Report: dataforge-Local__df-local-foundation

Generated: `2026-06-19T08:22:16+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local`
Source branch: `master`
Source commit: `536b700fa7f11bf92c75e5f8c540c4b571ebb17b`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation`
Target branch: `main`
Target commit: `6760634671ff88eda50ec3d99dd9e524694be4d9`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 8 |
| intentional_app_support_adaptation | 0 |
| missing_from_target | 135 |
| target_only_glue | 0 |
| dangerous_drift | 0 |
| unknown | 82 |

## Items

| Path | Classification | Recommended action |
| --- | --- | --- |
| `.gitignore` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `CLAUDE.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `README.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `SYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `alembic.ini` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/README.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/env.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/script.py.mako` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_01_create_local_substrate_schemas.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_02_create_substrate_core_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_03_create_service_registry_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_04_create_service_status_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_05_create_runtime_governance_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_06_create_runtime_promotion_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_07_create_operator_control_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260402_08_create_bds_governance_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260404_09_create_proving_slice_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260606_01_create_healing_proposals.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260607_01_create_gnat_runtime_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260607_02_phase1_worker_remediation_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260607_03_phase1_worker_autonomy_truth_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260607_04_phase2_doppelcore_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260607_05_phase2_verification_results.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_01_phase2_scan_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_02_phase2_exceptions_centipede.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_03_phase2_compliance_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_04_phase2_events_table.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_05_phase2_core_registry_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260608_06_forge_lineage_tables.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260609_01_create_context_packs.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `alembic/versions/20260611_01_create_public_applications.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/__init__.py` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `app/__main__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `app/analytics_config.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/analytics_models.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/analytics_services.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/analytics_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/context_pack_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/healing_proposal_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/lineage_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/proving_slice_queue_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/api/public_applications_router.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/database.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/evaluation_spine/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/evaluation_spine/lineage.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/evaluation_spine/lineage_cli.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/evaluation_spine/triple_variant_audit_store.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `app/main.py` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `ci_gate.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/public_applications.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/read_models.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/runtime_actions.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/schemas.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/services.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `constants/vocabularies.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `contracts/app-registration.schema.json` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `contracts/health.schema.json` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `contracts/migration-status.schema.json` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/backup/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/backup/manager.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/backup/signing.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/config/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/config/settings.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/export/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/export/manager.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/health/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/health/reporter.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/lifecycle/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/lifecycle/compatibility.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/lifecycle/maintenance.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/lifecycle/manager.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `core/lifecycle/migration_lock.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/DFLSYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/DLOSYSTEM.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/SYSTEM.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/plans/local-analytics/df_local_analytics_slice_01.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/00-overview.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/00_overview/01-overview-philosophy.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/00_overview/02-architecture.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/00_overview/03-project-structure.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/01-architecture.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/01-overview-philosophy.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/02-architecture.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/03-tech-stack.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/04-project-structure.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/05-configuration.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/06-design-system.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/07-frontend.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/08-api-layer.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/09-backend.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/10-ecosystem-integration.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/10-scope.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/10_service-contract/04-design-system.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/10_service-contract/05-frontend.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/10_service-contract/06-api-layer.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/10_service-contract/07-proving-slice.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/11-database-schema.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/12-ai-integration.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/13-error-handling.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/14-testing-infrastructure.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/15-handover-migration-notes.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/20-structure.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/20_runtime/08-backend.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/20_runtime/09-database-schema.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/20_runtime/10-ai-integration.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/20_runtime/11-error-handling.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/30-governance.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/30_dependencies/12-tech-stack.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/30_dependencies/13-ecosystem-integration.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40-change-control.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/40_governance/14-scope.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40_governance/15-governance.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/40_governance/16-change-control.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/50_operations/17-configuration.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/50_operations/18-testing-infrastructure.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/50_operations/19-handover-migration-notes.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/90-appendices.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `doc/system/99_appendices/20-appendices.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/BUILD.sh` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `doc/system/_index.md` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `doc/system/validate_snapshots.sh` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `docs/closeout-initial-governed-implementation.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `docs/dataforge-local_architecture_spec.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/dataforge-local_extended_roadmap.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/df-local-foundation_extended_roadmap.md` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `docs/evaluation-spine-phase-08-dataforge-local-lineage.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/migration_order.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/read_models.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/repo_structure.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/schema_inventory.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/seed_strategy.md` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_runtime/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_runtime/persistence.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/models.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/artifact_ingest.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/promotion_admission.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/promotion_queue.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/promotion_reconciliation.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `proving_slice/services/read_models.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `pyproject.toml` | unknown | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `reports/contract_core_gate_20260404_093918.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260404_094503.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260614_002806.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260614_003357.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260614_004114.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260614_004902.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/contract_core_gate_20260614_004945.json` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260404_093918.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260404_094503.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260614_002806.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260614_003357.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260614_004114.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260614_004902.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `reports/local_tests_20260614_004945.xml` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/bootstrap_local_env.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/init_db.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/reset_db.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/run_local.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/run_migrations.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/seed_v1.sh` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/governed_action_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/public_application_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/read_model_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/schema_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `seeds/service_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `sql/apps/authorforge/0001_authorforge_attach.sql` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `sql/bootstrap.sql` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `sql/core/0001_core_foundation.sql` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `sql/core/0002_core_metadata.sql` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `sql/dev_reset.sql` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `sql/manual_checks.sql` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/api/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/api/test_analytics_compute.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/api/test_analytics_routes.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/api/test_context_pack_routes.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/api/test_health_api.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/backup_restore/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/backup_restore/test_envelope_signing.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/backup_restore/test_restore_redteam.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/backup_restore/test_restore_validation.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/first_integration/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/first_integration/test_authorforge_attachment.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/gnat_runtime/test_persistence.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/migration_status/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/migration_status/test_migration_contract.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/migration_status/test_migration_lock.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/proving_slice/__init__.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/proving_slice/conftest.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/proving_slice/test_admission.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/proving_slice/test_queue.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/proving_slice/test_read_models.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/proving_slice/test_reconciliation.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/registration/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/registration/test_app_registration.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/registration/test_compatibility_semantics.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/registration/test_config_bypass.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_constants.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test_evaluation_spine_phase08_lineage.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test_schema_registry_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test_service_seeds.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test_triple_variant_audit_store.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test_vocabularies.py` | missing_from_target | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/visibility_boundary/__init__.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/visibility_boundary/test_cli_authority.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/visibility_boundary/test_health_contract.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/visibility_boundary/test_health_event_discipline.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/visibility_boundary/test_status_redteam.py` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tools/db-backup` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tools/db-export` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tools/db-restore` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tools/db-status` | unknown | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
