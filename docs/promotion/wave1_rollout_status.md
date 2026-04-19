# PACT TOON Wave-1 Promotion — Rollout Status

**Date:** 2026-04-18
**Source plan:** `promotion_integration_plan_set_canvases_2026-04-17/`
**Cross-repo orchestrator:** `scripts/verify_wave1_promotion_stack.py`
**Generated stack report:** `evidence/wave1_promotion_stack_report.json`

This document records where the PACT TOON wave-1 promotion stack sits in the Canvas 05 staging model and which evidence files prove the posture for each stage. Update this file after any change to a promotion-relevant artifact and re-run the orchestrator.

---

## Stage matrix

| Stage | Posture | Status | Evidence |
|-------|---------|--------|----------|
| Stage 0 — passive visibility | Manifest can be loaded by consumers; no runtime behavior change | Reached | `pact/docs/evidence/wave1_promotion_envelope.json` |
| Stage 1 — local carriage admitted | neuronforge_local_operator records admitted envelopes; operator can approve local use | Reached | `local-systems/neuronforge-local-operator/evidence/promotion_seam/seam_report.json`, `…/promotion_runs.jsonl` |
| Stage 2 — cloud intake admitted | NeuroForge accepts only compatible promotion envelopes; operator can separately approve cloud use | Reached | `cloud-systems/NeuroForge/evidence/promotion_intake/cloud_summary.json`, `…/intake_runs.jsonl` |
| Stage 3 — control-plane governed | ForgeCommand becomes the working approval and mismatch surface; rollback state visible across repos | Reached | ForgeCommand `/promotion` route, `Forge_Command/src-tauri/tests/promotion_verification.rs` (FC-04), rollback fixture under `evidence/wave1_rollback_case/` |
| Stage 4 — active runtime dependence | Runtime decisions may depend on admitted promotion state | **Deferred (intentional)** | Out of scope for this wave (Canvas 05 line 32; Canvas 06 wave-1 boundary) |

---

## Stage 3 readiness checklist

All items below must be true for Stage 3 to remain reached. The cross-repo orchestrator re-verifies each item from artifacts on disk:

- [x] PACT envelope present with required fields (`gate_0_source_truth`)
- [x] neuronforge_local seam report passes; promotion_runs.jsonl carries strict and non-strict cases (`gate_1_neuronforge_local`)
- [x] NeuroForge cloud summary reports `compatibility_state = compatible`; intake_runs.jsonl carries strict cases (`gate_2_neuroforge_cloud`)
- [x] All consumer repos carry the same `wave_manifest_hash`; same lineage produces the same admission class across repos (`gate_4_cross_repo_replay`)
- [x] Rollback fixture written; stale-hash carriage surfaces as `not_admitted` with `manifest_hash_mismatch` and a recommended rollback target (`gate_5_rollback_case`)
- [x] ForgeCommand FC-04 invariant test passes:
  - blocked surfaces visible (no silent downgrade to `compatible`)
  - missing fields collapse to `unknown` (never `compatible`)
  - strict and non-strict admission counts remain in distinct buckets
  - operator approvals never mutate manifest truth fields

Run command for the cross-repo evidence:

```bash
python3 scripts/verify_wave1_promotion_stack.py
```

Run command for the ForgeCommand invariant test:

```bash
cd Forge_Command/src-tauri && cargo test --test promotion_verification
```

Both commands must exit zero. The stack report is written to `evidence/wave1_promotion_stack_report.json` on every run.

---

## Operator approval doctrine (Canvas 03)

Approval is two-stage and never auto-coupled:

1. `approved_for_local_use` — gates downstream behavior on neuronforge_local_operator only.
2. `approved_for_cloud_use` — gates downstream behavior on NeuroForge cloud only.

A local approval **must not** imply a cloud approval, and a `compatible` compatibility state **must not** imply operator approval. Approval state is stored exclusively in the ForgeCommand local SQLite table `promotion_operator_approvals` and never flows back into upstream artifacts.

`blocked` and `rolled_back` dominate any positive approval — if either scope records one of these states, the combined operator state is reported as the dominating state.

---

## Stage 4 prerequisites (deferred)

Before Stage 4 may be considered, all of the following must be true (none are implemented in this wave):

- All Stage 3 evidence holds for at least one stable observation window operator-defined (TBD).
- A documented runtime contract exists describing what consumer code is allowed to gate on the admitted promotion state.
- A drift detector exists that can demote `compatible` to `mismatch` automatically when consumer artifacts diverge.
- A rollback execution path exists (not just a posture) that can roll consumers off a manifest hash without manual intervention.

These are intentionally not in scope for this wave per Canvas 06.
