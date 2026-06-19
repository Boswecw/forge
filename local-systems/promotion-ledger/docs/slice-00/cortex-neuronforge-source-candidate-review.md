# Slice 00 Cortex And NeuronForge Source Candidate Review

Generated: `2026-06-19T09:28:31Z`

This reviews the first source-only promotion queue: Cortex and NeuronForge
runtime/capability, contract/schema, script, and paired test surfaces.

## Candidate Counts

| Repo pair | Candidate count |
| --- | ---: |
| `cortex__cortex` | 97 |
| `neuronforge-local-operator__neuronforge` | 122 |

## Proof

| Surface | Command | Result |
| --- | --- | --- |
| Cortex GNAT | `make test-gnats` | Passed; 87 tests. |
| NeuronForge prompt assembly | `python3 -m pytest prompt_assembly/tests/ -q` | Passed; 100 tests. |
| NeuronForge COR/GNAT handoff | `python3 tests/test-cor-gnat-semantic-handoff.py` | Passed; 6 tests. |
| NeuronForge continuity adjacent scene | `bash tests/test-continuity-adjacent-scene.sh` | Passed; 27 checks. |
| NeuronForge experiment memory | `python3 -m pytest tests/experiment_memory/ -q` | Passed; 61 passed, 1 skipped. |

The full NeuronForge `scripts/run-tests.sh` gate was interrupted because it hung
inside the style-analysis route test. Focused candidate subsets were run
separately and passed.

## Decisions

| Surface | Posture | Reason |
| --- | --- | --- |
| Cortex GNAT bundle | `hold_source_local` | Proved local-system capability; support Cortex currently exposes a narrower AuthorForge file-intelligence adapter. |
| NeuronForge prompt assembly | `hold_source_local` | Source-proved but not currently an app-support service lane. |
| NeuronForge experiment memory | `hold_source_local` | Local-system proving surface with Graphiti/runtime dependencies, not a current support target surface. |
| NeuronForge COR/GNAT handoff | `hold_source_local` | Source-proved, but support promotion needs an explicit endpoint and caller decision. |

## Next Gate

Review DataForge source-only migration/runtime/contracts, then FA Local thin
source-only surfaces.
