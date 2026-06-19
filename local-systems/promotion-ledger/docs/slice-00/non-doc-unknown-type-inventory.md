# Slice 00 Non-Doc Unknown Type Inventory

Generated: `2026-06-19T08:53:30Z`

After source-backed docs and target-only `/docs` receipts were resolved, the
ledger has 183 remaining `unknown` items. None are `/docs` unknowns.

## Lineage

| Gate | Unknown count |
| --- | ---: |
| Original drift parse | 204 |
| After source-backed doc reconciliation | 191 |
| After target-only `/docs` resolution | 183 |

## Shape Summary

| Shape | Count |
| --- | ---: |
| `target_only` | 129 |
| `modified_in_both` | 54 |

## Like Types

| Type | Count | Primary action |
| --- | ---: | --- |
| `doc_system_mirror_or_root_system` | 79 | Treat as code mirror drift; rebuild or compare `/doc/system` against live code. |
| `runtime_or_adapter_code` | 37 | Review as implementation drift with tests before promotion. |
| `test_surface` | 29 | Keep paired with the runtime or contract surface it proves. |
| `repo_scaffold_config` | 15 | Classify as repo-local scaffold unless it affects runtime behavior. |
| `promotion_evidence_runtime` | 9 | Resolve against promotion seam provenance; mirror drift can block. |
| `contract_schema_sql` | 7 | Review with runtime tests and source authority. |
| `operator_tooling_scripts` | 7 | Tie each tool or script to a proof command. |

## Repo Breakdown

| Repo pair | Unknown | Dominant type |
| --- | ---: | --- |
| `dataforge-Local__df-local-foundation` | 80 | `doc_system_mirror_or_root_system`, tests, runtime code |
| `neuronforge-local-operator__neuronforge` | 42 | `/doc/system`, promotion evidence, service code |
| `fa-local-operator__fa-local` | 28 | `/doc/system`, runtime code, scaffold |
| `cortex__cortex` | 27 | `/doc/system`, service/runtime code |
| `forge-local-systems-runtime__forge-local-runtime-master-reference` | 6 | `/doc/system` |

## Next Gate

`/doc/system` mirror drift is resolved in
`docs/slice-00/doc-system-mirror-resolution-proof.md`. Runtime and test drift is
resolved in `docs/slice-00/runtime-test-resolution-proof.md`. The final 38
unknowns are resolved in `docs/slice-00/final-unknown-resolution-proof.md`.
Unknown and dangerous drift are now zero.
