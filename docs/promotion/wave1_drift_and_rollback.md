# PACT TOON Wave-1 Promotion — Drift & Rollback Doctrine

**Date:** 2026-04-18
**Source plan:** `promotion_integration_plan_set_canvases_2026-04-17/`
**Companion doc:** `wave1_rollout_status.md`

This doc fixes the operator-facing meaning of *drift* and *rollback* for the wave-1 promotion stack and points to the on-disk evidence that backs each doctrinal claim. Update this file alongside any change to the cross-repo evidence shape.

---

## Fail-closed rules (Canvas 05 §Fail-closed rules)

A consumer must mark `not_admitted` and surface a reason code — never silently downgrade to `admitted` and never invent missing truth — when any of the following hold:

| Condition | Reason code | Failing field |
|-----------|-------------|---------------|
| Manifest hash missing | `manifest_hash_missing` | `manifest_file` |
| Manifest hash mismatched | `manifest_hash_mismatch` | `wave_manifest_hash` |
| Manifest version unsupported | (carrier-specific) | (carrier-specific) |
| Packet class not in `allowed_packet_classes` | `packet_class_unsupported` | `allowed_packet_classes` |
| Requested profile not in `supported_requested_profiles` | `requested_profile_unsupported` | `supported_requested_profiles` |
| Used profile not in `supported_used_profiles` | `used_profile_unsupported` | `supported_used_profiles` |
| Strict success hash mismatched in strict case | `strict_success_hash_mismatch` | `strict_success_hash` |
| Non-strict canonical digest missing in non-strict case | `non_strict_canonical_digest_missing` | `non_strict_canonical_digests` |
| Fallback reason not in `fallback_reason_codes` | `fallback_reason_unsupported` | `fallback_reason_codes` |
| Lineage identifiers absent where required by the seam | (seam-specific) | `lineage` |
| Evidence report cannot be loaded | `partial_envelope_rejected` | `envelope_shape` |

The reason → failing field mapping is the same one ForgeCommand uses to populate the mismatch / rollback band. See `Forge_Command/src-tauri/src/services/promotion_service.rs` (`failing_field_for_reason`, `rollback_target_for_reason`).

---

## Drift classes (Canvas 05 §Drift doctrine)

### Class 1 — source drift (PACT-side)

PACT's manifest or digest package changed. Effect: every downstream repo must be re-verified before any consumer treats it as `compatible` again. Detect by re-running the cross-repo orchestrator after a PACT update — `gate_4_cross_repo_replay` will fail if consumer evidence still references the old hash.

Operator action: re-emit downstream evidence (re-run seam tests, re-mirror the envelope), then re-record approvals against the new manifest hash. Old approvals are stale, not transferable.

### Class 2 — consumer drift (downstream-side)

A downstream repo changed its local schema or carrier fields without re-proving against PACT. Effect: compatibility becomes `mismatch` until re-proved. Detect by `cloud_summary.compatibility_state` flipping to `mismatch`, by `seam_report.all_pass` turning false, or by a non-empty `mismatch_reason_codes` list.

Operator action: hold the consumer in `mismatch` state and refuse to re-approve until the downstream artifact is re-emitted clean.

### Class 3 — operator-state drift (approval-side)

Approval records exist for an older manifest hash. Effect: those approvals are stale and **must not** count as current approval for the live manifest. ForgeCommand enforces this by scoping approval queries to a specific `manifest_hash` — approvals against the previous hash are visible in history but are not aggregated into the current `operator_approval_state`. See `latest_approval_for_scope` and `latest_combined_approval_state` in `promotion_service.rs`.

Operator action: explicitly re-record approvals against the new manifest hash. The old approval records remain in the audit trail but no longer gate downstream behavior.

---

## Rollback doctrine (Canvas 05 §Rollback doctrine)

A rollback is required when any of the following hold:

- Source manifest replaced upstream without downstream proof of the new hash.
- Consumer mismatch persists beyond a triage window.
- Operator evidence is missing or contradictory for a manifest that previously held approval.
- Replay classification (gate 4) no longer matches admitted expectations.

Every rollback record must capture:

- Repo name being rolled back
- Manifest hash being exited
- Reason code (must be a value from the fail-closed table above)
- Time of rollback
- Operator note (free-text, optional but strongly recommended for non-obvious rollbacks)

ForgeCommand records this via `promotion_record_operator_approval` with `state = "rolled_back"` and `note = "<operator rationale>"`. The `rolled_back` state dominates any positive approval — `combine_scope_states` returns `rolled_back` whenever either local or cloud scope holds it.

---

## Rollback evidence (synthetic fixture)

The cross-repo orchestrator (`scripts/verify_wave1_promotion_stack.py`, gate 5) writes a synthetic rollback fixture on every run:

| Path | Purpose |
|------|---------|
| `evidence/wave1_rollback_case/rollback_run.json` | A single promotion-run record carrying a stale wave-0 manifest hash. Demonstrates the `not_admitted` + `manifest_hash_mismatch` posture as it would appear in `promotion_runs.jsonl` or `intake_runs.jsonl`. |
| `evidence/wave1_rollback_case/rollback_summary.json` | The expected admission verdict, blocked reason codes, recommended rollback target, and operator-doctrine reminder. |

The fixture is regenerated on every orchestrator run and is therefore always paired with the live `wave_manifest_hash` from the PACT envelope. It is not a record of an actual rollback — it is proof that the system would correctly classify a stale-hash carriage if one occurred.

---

## Cross-references

| Concern | Authority |
|---------|-----------|
| Fail-closed rules | Canvas 05 §Fail-closed rules |
| Drift class definitions | Canvas 05 §Drift doctrine |
| Rollback definitions | Canvas 05 §Rollback doctrine |
| Two-stage approval doctrine | Canvas 03 §Initial approval doctrine; `wave1_rollout_status.md` |
| Approval state combination | `Forge_Command/src-tauri/src/services/promotion_service.rs::combine_scope_states` |
| Rollback target text per reason | `Forge_Command/src-tauri/src/services/promotion_service.rs::rollback_target_for_reason` |
| FC-04 invariant proofs | `Forge_Command/src-tauri/tests/promotion_verification.rs` |
| Cross-repo gate proofs | `scripts/verify_wave1_promotion_stack.py`, latest run in `evidence/wave1_promotion_stack_report.json` |
