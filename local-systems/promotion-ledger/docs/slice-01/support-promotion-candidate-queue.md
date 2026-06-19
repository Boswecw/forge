# Slice 01 Support Promotion Candidate Queue

Generated: `2026-06-19T17:23:37+00:00`

This queue is generated from reviewed `source_local_hold` drift. It does not authorize copying artifacts into app support.

## Summary

| Metric | Count |
| --- | ---: |
| `source_local_hold` | 592 |
| `candidate_after_target_role` | 241 |
| `default_hold` | 351 |
| `missing_from_target` | 0 |
| `unknown` | 0 |
| `dangerous_drift` | 0 |

## Like Types

| Type | Count | Posture |
| --- | ---: | --- |
| `source_contract_schema_migration` | 43 | `candidate_after_contract_compatibility` |
| `source_docs_or_doc_mirror` | 103 | `default_hold_docs_rule` |
| `source_evidence_reports_prompts` | 58 | `default_hold_evidence_receipt_only` |
| `source_local_subproject` | 183 | `default_hold` |
| `source_proof_tests` | 79 | `pair_with_promoted_runtime_or_contract` |
| `source_runtime_or_capability` | 95 | `candidate_after_target_role` |
| `source_scaffold_config` | 7 | `default_hold_dependency_adoption_required` |
| `source_scripts_ci` | 24 | `candidate_when_tied_to_support_proof_command` |

## Repo Breakdown

| Repo pair | Source-local holds |
| --- | ---: |
| `cortex__cortex` | 277 |
| `dataforge-Local__df-local-foundation` | 127 |
| `fa-local-operator__fa-local` | 15 |
| `forge-local-systems-runtime__forge-local-runtime-master-reference` | 1 |
| `neuronforge-local-operator__neuronforge` | 172 |

## Gate

A source-local hold may enter app support only after a named promotion slice declares the target role, source proof command, support proof command, and post-promotion drift report.

Select exactly one candidate category and repo pair before opening a support promotion slice. The slice must name the support target role, source proof command, support proof command, and regenerated drift report.
