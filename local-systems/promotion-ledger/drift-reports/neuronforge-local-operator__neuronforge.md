# Drift Report: neuronforge-local-operator__neuronforge

Generated: `2026-06-19T08:55:43+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/neuronforge-local-operator`
Source branch: `master`
Source commit: `006ef57c9ece79b666581b303fce06e54debaa42`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/neuronforge`
Target branch: `master`
Target commit: `dc67b04863e313f3116565ddf1e7e369d6349a67`

Resolutions applied: `17`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 392 |
| intentional_app_support_adaptation | 7 |
| missing_from_target | 173 |
| target_only_glue | 10 |
| dangerous_drift | 0 |
| unknown | 30 |

## Items

| Path | Classification | Resolution | Recommended action |
| --- | --- | --- | --- |
| `.claude/settings.local.json` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `.env.graphiti` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `.env.graphiti.example` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `.gitignore` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `CLAUDE.md` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `GEMINI.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `NLOSYSTEM.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `README.md` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `SYSTEM.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/NRNSYSTEM.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/00-overview.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/01-architecture.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/07-experiment-memory-graphiti-pilot.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/system/10-scope.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/20-structure.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/30-governance.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/40-change-control.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/90-appendices.md` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `doc/system/BUILD.sh` | intentional_app_support_adaptation | `slice-00-neuronforge-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after service or mirror-index changes. |
| `doc/system/_index.md` | intentional_app_support_adaptation | `slice-00-neuronforge-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after service or mirror-index changes. |
| `doc/system/validate_snapshots.sh` | target_only_glue | `slice-00-neuronforge-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same support mirror structure. |
| `docker-compose.graphiti-pilot.yml` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/adr/ADR-001-promotion-truth-upstream-of-pact.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/adr/ADR-2026-04-18-promotion-truth-upstream.md` | intentional_app_support_adaptation | `slice-00-neuronforge-promotion-adr-doc` | Keep as historical support doctrine. Do not back-promote its target mirror path claims as source authority without a fresh proving repo ADR update. |
| `docs/cor-gnat-semantic-handoff.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/dogfood-cloud-quota-log.md` | intentional_app_support_adaptation | `slice-00-neuronforge-dogfood-quota-doc` | Keep as support planning documentation until telemetry is implemented and proved in the local system. |
| `docs/evidence/promotion_runs_demo.md` | intentional_app_support_adaptation | `slice-00-neuronforge-promotion-runs-demo` | Keep as support evidence. Regenerate from the proving repo seam when the promotion seam changes. |
| `docs/evidence/promotion_seam_example.md` | intentional_app_support_adaptation | `slice-00-neuronforge-promotion-seam-example` | Keep as support evidence. Refresh from the proving repo when the seam proof changes. |
| `docs/evidence/promotion_seam_report.json` | intentional_app_support_adaptation | `slice-00-neuronforge-promotion-seam-report` | Keep as support evidence. Regenerate from the local proving repo verification output when the seam changes. |
| `docs/forge-command-integration-handoff.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/01-PILOT-ARCHITECTURE.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/02-EXPERIMENT-RECORD-AUTHORITY-MATRIX.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/03-GRAPH-IDENTITY-AND-FINGERPRINT-CONTRACT.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/04-TEMPORAL-SEMANTICS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/05-DATA-SECURITY-AND-CLASSIFICATION.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/06-SCHEMA-AND-CONTRACT-PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/07-REPOSITORY-STRUCTURE.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/08-OPERATOR-QUERY-CONTRACTS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/09-VERIFICATION-PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/10-PLATFORM-AND-DEPLOYMENT-PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/11-IMPLEMENTATION-SLICES.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/12-GO-NO-GO-EVALUATION.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/13-DECOMMISSION-PLAN.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/14-RISKS-ANTI-PATTERNS-AND-DECISIONS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/G-09-COMPARATIVE-EVALUATION.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/G-10-DECISION-RECORD.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/MAPPING-SPEC.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/README.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `docs/plans/graphiti/REVIEW.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `evals/beat_candidate_bakeoff/beat_candidate_bakeoff_status.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `evidence/promotion_seam/operator_examples.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `evidence/promotion_seam/promotion_runs.jsonl` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `evidence/promotion_seam/seam_report.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `inputs/beat_candidate_bakeoff/scene_001.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `inputs/beat_candidate_bakeoff/scene_002.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_001/phi4_14b-20260404-144643.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_001/phi4_14b-20260404-150014.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_001/qwen2.5_14b-20260404-144509.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_001/qwen2.5_14b-20260404-145805.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_001/qwen2.5_14b-20260404-160612.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_002/phi4_14b-20260404-145120.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_002/phi4_14b-20260404-150443.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_002/qwen2.5_14b-20260404-144839.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_002/qwen2.5_14b-20260404-150145.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/beat_candidate_bakeoff/scene_002/qwen2.5_14b-20260404-160832.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-001.md` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-04-17-002.md` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `promotion/__init__.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `promotion/compatibility.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `promotion/envelope.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `promotion/mirror/wave1_promotion_envelope.mirror.json` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `promotion/mirror/wave1_promotion_envelope.schema.json` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `promotion/models.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `promotion/run_log.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `promotions/promotion-2026-05-29-001/manifest.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/AGENTS.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/README.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/config/defaults.yaml` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/common_enums.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/compiled_bundle.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/constraint_surface.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/long_context.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/prompt_assembly_input.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/prompt_assembly_manifest.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/contracts/redaction_policy.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/runtime/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/runtime/errors.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/runtime/models.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/conftest.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/fixtures/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/fixtures/builders.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/integration/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/integration/test_validate_registry.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/test_alignment.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/test_errors.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/test_models.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tests/test_schemas.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tools/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompt_assembly/tools/validate_registry.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `prompts/beat_candidate_bakeoff/beat_candidate_extraction_v1.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `registry/pact_wave1_envelope_mirror.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `registry/runs.md` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `requirements-dev.txt` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `requirements-graphiti.txt` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `requirements.txt` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `runtime/graph/export.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `runtime/graph/report.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-evaluation-record.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-experiment-event.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-failure-observation.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-hardware-profile.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-operator-decision.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/nlo-run-record.v1.schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/experiment-record-type.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/experiment-status.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/failure-taxonomy.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/graph-entity-type.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/graph-health-status.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/graph-relationship-type.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `schemas/experiment_memory/registries/projection-status.v1.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/_compose.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/capture-hardware-profile.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/graph-doctor.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/graph-down.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/graph-reset.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/graph-up.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/graph/nlo-graph` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/run-tests.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/run_beat_candidate_bakeoff.sh` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/style_analysis/models.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `scripts/validate_beat_candidate_output.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `scripts/verify_promotion_seam.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `service/authorforge_task_contract.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/authorforge_task_service.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/cloud_escalation.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/cor_gnat_semantic_handoff.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `service/dogfood_telemetry.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/local_runtime.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/main.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `service/proofread_lane.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `service/scene_lane.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `src/nlo_experiment_memory/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/cli/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/cli/__main__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/contracts/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/contracts/integrity.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/contracts/loader.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/enrichment/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/identity/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/identity/ids.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/identity/normalize.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/projection/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/projection/backends.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/projection/live_backend.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/projection/mapping.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/projection/projector.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/queries/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/queries/evidence.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/queries/narrative.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/stores/__init__.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/stores/dataforge_local.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `src/nlo_experiment_memory/stores/fixture_store.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/conftest.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_contracts.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_fail_open.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_hardware_capture.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_identity.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_live_backend.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_projection.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/experiment_memory/test_queries.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/README.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/baseline-history.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/compare-runs.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/current-baseline.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/explain-candidate.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/fingerprint.txt` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/golden/recurring-failures.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/decision-superseded-before-effective.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/eval-bad-reference.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/eval-temporal-invalid.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/failure-prohibited-content.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/failure-taxonomy-mismatch.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/run-bad-enum.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/run-bad-hash.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/run-missing-required.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/run-unknown-field.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/invalid/run-unsupported-schema.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/decision-2026-03-13-lore-safe-baseline-001.decision.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/decision-2026-03-13-reject-016-01.decision.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/eval-run-2026-03-13-002-review-01.evaluation.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/eval-run-2026-03-13-005-review-01.evaluation.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/eval-run-2026-03-13-016-review-01.evaluation.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/exp-2026-03-13-002-review-01.event.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/exp-2026-03-13-003-run-01.event.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/exp-2026-03-13-005-review-01.event.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/exp-2026-03-13-016-review-01.event.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/exp-fixture-oom-001.event.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-fixture-oom-001.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-002-meaning-drift-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-002-over-editing-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-002-schema-invalid-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-003-schema-invalid-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-016-false-negative-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/failure-run-2026-03-13-016-style-regression-01.failure.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/hw-fixture-constrained-001.hardware.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/run-2026-03-13-002.run.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/run-2026-03-13-003.run.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/run-2026-03-13-005.run.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/run-2026-03-13-016.run.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/fixtures/experiment_memory/records/run-fixture-oom-001.run.json` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test-cor-gnat-semantic-handoff.py` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `tests/test-style-analysis.py` | unknown |  | Compare source and target intent; resolve by human decision, backport, or explicit exception. |
| `tests/test_authorforge_task_contract.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_authorforge_task_service.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_cloud_escalation.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_dogfood_telemetry.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_proofread_lane.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |
| `tests/test_scene_lane.py` | unknown |  | Classify as target_only_glue, intentional_app_support_adaptation, dangerous_drift, or backport to the proving repo. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
