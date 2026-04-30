# V1 Plan Set Index — Centipede, DoppelCore, and Correction Fabric

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This zip is the **V1 plan set** for the current architecture direction where:

- **Centipede** is the governed evidence and reconciliation producer
- **DoppelCore** is the truth-core and correction-ready artifact producer
- **Registry** and **Self-Healing** are the primary downstream operator consumers
- **forgeHQ / ForgeMath / forge-eval / eval-cal-node** are the correction-fabric proposal systems
- **FA-Local-Operator** and **ForgeAgents** are the execution lanes

This package is meant to be read as a controlled planning set, not as scattered notes.

## Recommended read order

1. `01_v1_initial_plan.md`
2. `02_v1_integration_plan_centipede_registry_self_healing.md`
3. `03_v1_doppelcore_position_and_role.md`
4. `04_v1_system_boundaries_and_artifact_flows.md`
5. `05_v1_correction_fabric_process_diagrams.md`
6. `06_v1_self_healing_current_evidence_integration.md`
7. `07_v1_edge_case_and_outside_box_supplement.md`
8. `08_v1_external_review_fold_in.md`
9. `09_v1_initial_execution_order.md`
10. `99_v1_source_map.md`

## What this V1 set locks

- Centipede is **not** the top-level page authority
- Centipede should feed **Self-Healing** and **Registry**
- Registry and Self-Healing need **different projection contracts**
- DoppelCore should live as a **standalone internal ecosystem component**
- Correction proposal work belongs **downstream of DoppelCore**
- Execution belongs to:
  - **FA-Local-Operator** for local work
  - **ForgeAgents** for cloud work

## V1 package intent

This set is designed to give you a practical foundation for the next implementation tranche without re-opening the whole architecture every time you touch one subsystem.
