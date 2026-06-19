# Slice 00 Source-Only Backlog Inventory

Generated: `2026-06-19T09:24:52Z`

Unknown and dangerous drift are zero. The remaining backlog is 648
`missing_from_target` items: artifacts present in the local-system proving repos
but absent from app support.

## Repo Breakdown

| Repo pair | Count |
| --- | ---: |
| `cortex__cortex` | 319 |
| `neuronforge-local-operator__neuronforge` | 173 |
| `dataforge-Local__df-local-foundation` | 135 |
| `fa-local-operator__fa-local` | 20 |
| `forge-local-systems-runtime__forge-local-runtime-master-reference` | 1 |

## Like Types

| Type | Count | Promotion posture |
| --- | ---: | --- |
| `source_local_subproject` | 183 | Exclude by default; source-local subprojects. |
| `source_proof_tests` | 120 | Pair with runtime or contract promotions; do not promote alone. |
| `source_runtime_or_capability` | 107 | Promotion candidates after target-role and proof review. |
| `source_docs_or_doc_mirror` | 102 | Do not bulk-promote; `/docs` stays condensed and `/doc/system` is mirror-only. |
| `source_contract_schema_migration` | 53 | Promotion candidates after compatibility review. |
| `source_evidence_reports_prompts` | 52 | Exclude by default unless named evidence receipts. |
| `source_scripts_ci` | 24 | Promote only when tied to a support proof command. |
| `source_scaffold_config` | 7 | Exclude by default unless support adopts the dependency/runtime. |

## Candidate Queue

First review `source_runtime_or_capability` and
`source_contract_schema_migration`, paired with `source_proof_tests`. Cortex and
NeuronForge carry the largest candidate surfaces; DataForge follows with
migrations/contracts and source runtime.

No source-only artifact should be copied into app support without an explicit
target role, proof command, and post-promotion drift report.

The Cortex/NeuronForge candidate review is recorded in
`docs/slice-00/cortex-neuronforge-source-candidate-review.md`; reviewed
surfaces are source-proved but held source-local until a support target role is
opened.
