# Drift Report: cortex__cortex

Generated: `2026-06-19T09:13:04+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/cortex`
Source branch: `master`
Source commit: `98ac9ad521bb21c5956301ebfa410e520d331a70`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/cortex`
Target branch: `master`
Target commit: `af2be69626dd26aec171dc2ea730bb4148373543`

Resolutions applied: `23`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 1587 |
| intentional_app_support_adaptation | 9 |
| missing_from_target | 319 |
| target_only_glue | 14 |
| dangerous_drift | 0 |
| unknown | 5 |

## Items

| Path | Classification | Resolution | Recommended action |
| --- | --- | --- | --- |
| `.codex` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `.gitignore` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `DECISIONS/0017-cortex-local-system-identity-and-cor-plan-lineage.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `DECISIONS/0018-gnat-bounded-parallel-worker-authorization.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `DECISIONS/0019-fa-local-owns-gnat-execution-routing.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `Makefile` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `SYSTEM.md` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `cortex_runtime/gnats/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/fa_local_client.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/models.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/operator_status.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/parallel_runner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/persistence.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/persistent_runner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/planner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/receipt.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/reconcile.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/registry.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/retrieval_prepare.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/schema_validation.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/semantic_handoff.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/serial_runner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/status.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/docx_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/epub_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/markdown_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/odt_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/pdf_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/plain_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/rtf_text.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/gnats/workers/text_common.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/health_cli.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `cortex_runtime/service_status.py` | intentional_app_support_adaptation | `slice-00-cortex-runtime-modified` | Keep as support runtime adaptation. Recompare before promoting changes back to the proving repo. |
| `cortex_runtime/source_lanes.py` | intentional_app_support_adaptation | `slice-00-cortex-runtime-modified` | Keep as support runtime adaptation. Recompare before promoting changes back to the proving repo. |
| `doc/CRTSYSTEM.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/SYSTEM.md` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `doc/cxSYSTEM.md` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `doc/system/00-overview.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/01-architecture.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/04-validation-and-delivery.md` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `doc/system/10-scope.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/20-structure.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/30-governance.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/40-change-control.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/90-appendices.md` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `doc/system/BUILD.sh` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `doc/system/_index.md` | intentional_app_support_adaptation | `slice-00-cortex-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime or service changes and compare before promotion. |
| `doc/system/validate_snapshots.sh` | target_only_glue | `slice-00-cortex-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same mirror designation and structure. |
| `docs/Worm.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/architecture/gnats-boundary-matrix.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-docx-lane-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-epub-lane-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-odt-lane-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-pdf-lane-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-phase4-parallel-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/benchmarks/gnat-rtf-lane-proof.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-cache-record.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-core.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-operator-run-status.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-retrieval-prepare.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-run-plan.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-run-request.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-run-summary.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-semantic-handoff.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-shard.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/contracts/gnat-worker-receipt.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/integration/df-local-gnat-persistence.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/integration/fa-local-gnat-dispatch.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/integration/operator-local-gnat-status.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/00_README.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/01_CURRENT_STATE_AUDIT.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/02_GNATS_TARGET_ARCHITECTURE.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/03_CONTRACT_AND_SCHEMA_PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/04_IMPLEMENTATION_PHASES.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/05_FILE_LEVEL_CHANGE_MAP.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/06_TEST_VALIDATION_AND_BENCHMARK_PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/07_FA_LOCAL_NEURONFORGE_DF_LOCAL_INTEGRATION.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/08_EXTRACTION_TO_SHARED_GNAT_CORE.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/09_RISKS_NON_GOALS_AND_ADRS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/10_CODEX_IMPLEMENTATION_PROMPTS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/11_MASTER_CHECKLIST.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/planning/COR_Gnats_Plan_Set/12_PHASE_10_SHARED_CORE_EXTRACTION.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/repo_crawler_parser_implementation_plan(1).md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/service/authorforge-service.md` | target_only_glue | `slice-00-cortex-authorforge-service-doc` | Keep in the support repo under /docs/service. Backport only if the local Cortex proving repo adds a generic service authority document. |
| `gnat_core/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_core/cache.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_core/hashing.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_core/interfaces.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_core/lifecycle.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `gnat_core/limits.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/APPLY.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/Cargo.lock` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/Cargo.toml` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/README.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/VERIFY.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/01_scope_and_authority.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/02_edge_taxonomy_and_evidence_schema.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/03_boundary_controls.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/04_discovery_adapters.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/05_target_identity_resolution.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/06_issue_classes_catalog.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/07_provenance_and_evidence_packaging.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/08_centipede_handoff_contract.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/09_contract_loader_scaffold.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/10_reference_audit_bin.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/11_target_normalizer_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/12_adapter_extract_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/13_resolution_pipeline_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/14_bundle_builder_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/15_centipede_handoff_builder_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/16_end_to_end_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/17_run_cli_smoke.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/18_run_from_files_cli.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/19_run_repo_surface_cli.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/20_cargo_manifest_adapter.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/21_pyproject_manifest_adapter.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/22_library_wiring_warning_cleanup.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/23_requirements_manifest_adapter.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/24_github_workflows_adapter.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/24b_github_workflow_parser_fix.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/25_pyproject_uv_sources_adapter.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/26_repo_surface_summary_evidence.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/27_nested_requirements_follow.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/adapter_emit_gitmodules.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/adapter_emit_package_manifest.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/boundary_policy_governed_external_reference.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/boundary_policy_local_repo_only.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/boundary_policy_same_org_governed.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/centipede_handoff_ambiguous_target.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/centipede_handoff_stale_submodule.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/edge_dependency_repo_reference.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/edge_git_submodule.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/evidence_bundle_ambiguous_docs.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/evidence_bundle_gitmodules.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/finding_ambiguous_docs_repo_reference.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/finding_catalog_ambiguous_target_identity.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/finding_catalog_stale_submodule_pointer.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/finding_stale_submodule_pointer.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/issue_catalog_ambiguous_target_identity.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/issue_catalog_stale_submodule_pointer.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/target_resolution_ambiguous_relative.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/target_resolution_resolved_https.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/examples/target_resolution_resolved_ssh.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-adapter-emission.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-centipede-handoff.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-edge.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-evidence-bundle.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-finding.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-reason-code-catalog.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-target-resolution.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/doc/system/worm/schema/worm-traversal-policy.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/ensure_toml_dependency.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_boundary_policy.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_centipede_handoff.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_contract_examples.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_discovery_adapters.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_evidence_bundle.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_issue_catalog.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/scripts/validate_worm_target_resolution.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_claim.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_claim_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_complete.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_complete_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_consumer_adversarial_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_consumer_stub.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_consumer_stub_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_enqueue.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_enqueue_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_export.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_export_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_export_validate_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_fail.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_fail_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_handoff_artifact.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_handoff_artifact_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_handoff_manifest.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_handoff_manifest_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_heartbeat.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_heartbeat_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_inbox_resolver.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_inbox_resolver_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_manifest_scan.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_manifest_scan_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_reclaim.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_reclaim_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_report.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/centipede_queue_report_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/svelte_probe_cli.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/svelte_probe_self_check.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_adapter_extract_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_bundle_builder_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_cargo_adapter_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_centipede_failure_handoff_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_centipede_handoff_builder_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_centipede_intake_consumer.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_centipede_intake_consumer_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_contract_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_end_to_end_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_github_workflow_adapter_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_nested_requirements_guardrails_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_nested_requirements_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_pyproject_adapter_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_pyproject_uv_sources_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_reference_audit.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_repo_surface_failure_evidence_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_repo_surface_summary_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_requirements_adapter_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_resolution_pipeline_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_run_from_files.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_run_repo_surface.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_run_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_symlink_containment_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/bin/worm_target_normalize_smoke.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_intake_normalizer.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_claim.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_complete.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_consumer_adversarial.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_consumer_stub.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_export.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_export_validate.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_fail.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_handoff_artifact.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_handoff_manifest.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_heartbeat.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_inbox_resolver.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_manifest_scan.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_reclaim.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_report.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/centipede_queue_writer.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/cli.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/config.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/discovery.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/error.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/extract.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/lang.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/lib.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/main.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/parser.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/policy.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/scanner.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/store.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/svelte_probe.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/watch.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_adapter_extractors.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_bundle_builder.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_centipede_handoff_builder.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_contract_audit.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_contracts.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_resolution_pipeline.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/src/worm_target_normalizer.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tests/repo_crawler_tests.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/centipede/capture_queue_working_set.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/centipede/queue_operator_surface_slice_40_plan.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/bun.lock` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/package.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/src/bin/svelte_probe_cli.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/src/probe.ts` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/tmp-smoke-test.svelte` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/tools/svelte-provider/src/probe.ts` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `repo-crawler/tools/svelte-provider/tsconfig.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `requirements.txt` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `schemas/gnat-cache-record.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-dispatch-envelope.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-operator-run-status.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-run-plan.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-run-request.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-run-summary.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-semantic-handoff.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-shard.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/gnat-worker-receipt.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/service-status.schema.json` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `scripts/benchmark_gnat_docx.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/benchmark_gnat_epub.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/benchmark_gnat_odt.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/benchmark_gnat_pdf.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/benchmark_gnat_rtf.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/benchmark_gnats.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/validate_schemas.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `service/__init__.py` | target_only_glue | `slice-00-cortex-service-target-only` | Keep as support adapter glue. Backport only if the local Cortex proving repo adopts the AuthorForge HTTP service boundary. |
| `service/__main__.py` | target_only_glue | `slice-00-cortex-service-target-only` | Keep as support adapter glue. Backport only if the local Cortex proving repo adopts the AuthorForge HTTP service boundary. |
| `service/authorforge_app.py` | target_only_glue | `slice-00-cortex-service-target-only` | Keep as support adapter glue. Backport only if the local Cortex proving repo adopts the AuthorForge HTTP service boundary. |
| `service/authorforge_translation.py` | target_only_glue | `slice-00-cortex-service-target-only` | Keep as support adapter glue. Backport only if the local Cortex proving repo adopts the AuthorForge HTTP service boundary. |
| `tests/contracts/fixtures/invalid/gnat-cache-record-missing-version.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-cortex-routes.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-raw-content.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-dispatch-envelope-unsupported-worker.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-operator-run-status-raw-preview.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-plan-missing-plan-hash.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-plan-orchestration-field.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-plan-unsupported-worker.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-request-missing-request-id.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-request-raw-path.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-request-unsupported-operation.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-summary-details-unredacted.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-summary-invalid-state.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-run-summary-missing-counts.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-semantic-handoff-missing-explicit-request.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-semantic-handoff-missing-model-disclosure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-semantic-handoff-raw-content.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-semantic-handoff-receipts-mutable.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-shard-negative-ordinal.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-shard-unscoped-path.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-shard-unsupported-media.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-worker-receipt-complete-missing-output.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-worker-receipt-failed-missing-reason.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/invalid/gnat-worker-receipt-raw-content-preview.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-cache-record-basic.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-dispatch-envelope-basic.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-operator-run-status-ready.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-run-plan-two-text-files.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-run-request-basic.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-run-summary-ready.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-semantic-handoff-basic.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-shard-markdown.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/contracts/fixtures/valid/gnat-worker-receipt-complete.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/fixtures/gnats/text-batch-small/chapter-01.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/fixtures/gnats/text-batch-small/note-plain.txt` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_core_shared.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_docx_lane.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_epub_lane.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_fa_local_client.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_odt_lane.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_operator_status.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_parallel_runner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_pdf_lane.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_persistence.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_planner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_retrieval_prepare.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_rtf_lane.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_semantic_handoff.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_serial_runner.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_gnat_status.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/runtime/test_service_status.py` | intentional_app_support_adaptation | `slice-00-cortex-runtime-test-modified` | Keep paired with the support runtime adaptation. |
| `worm/Cargo.lock` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/Cargo.toml` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/adapter.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/cli.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/engine.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/error.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/governance.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/lib.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/main.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/model.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/profiles.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/src/store.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `worm/tests/worm_tests.rs` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
