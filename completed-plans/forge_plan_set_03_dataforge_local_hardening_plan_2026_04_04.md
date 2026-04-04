# Forge Plan Set 03 — DataForge Local Proving-Slice Hardening Plan

**Date:** 2026-04-04 01:18 America/New_York  
**Purpose:** Turn DataForge Local from a baseline-documented repo into the actual local durable truth and promotion-staging substrate for proving slice 01.

---

# 1. Why this plan exists

DataForge Local is the right conceptual home for local truth and promotion staging.

But its current documented posture is still baseline-level. That means the ecosystem cannot safely assign proving-slice backbone authority to it without an explicit hardening plan.

This plan is that hardening plan.

---

# 2. Intended authority after hardening

Once this plan is implemented, DataForge Local should own:
- local canonical storage for admitted local artifacts
- promotion admission evaluation results
- durable staging rows
- lease-safe outbound queue truth
- retry/reconciliation state
- dead-letter truth
- local promotion attempt audit history
- read models or APIs consumed by ForgeCommand

It should not own:
- shared accepted truth
- operator review UX
- execution authority
- recommendation/proposal semantics by convenience

---

# 3. Required proving-slice family support

Initial admitted support only for:
1. `source_drift_finding`
2. `promotion_envelope`
3. `promotion_receipt`

No other family should be implemented in this wave.

---

# 4. Local persistence model

## 4.1 Canonical local artifact storage
DataForge Local must persist validated local artifacts durably before any transport logic begins.

### Required core fields
- `artifact_id`
- `artifact_family`
- `artifact_version`
- `lineage_root_id`
- `parent_artifact_id`
- `trace_id`
- `idempotency_key`
- `produced_by_system`
- `produced_by_component`
- `created_at`
- `recorded_at`
- `sensitivity_class`
- `visibility_class`
- `promotion_class`
- `validation_status`
- `signer_identity`
- `signature`
- canonical serialized payload body

## 4.2 Staging table
A separate durable staging table is required.

### Required fields
- `staged_promotion_id`
- `artifact_ref`
- `artifact_family`
- `artifact_version`
- `queue_status`
- `promotion_attempt_count`
- `claim_lease_owner`
- `claim_lease_expires_at`
- `last_attempted_at`
- `next_retry_at`
- `last_transport_error`
- `last_remote_status_code`
- `last_remote_error_class`
- `remote_receipt_ref`
- `dead_letter_reason`
- `created_at`
- `updated_at`

## 4.3 Audit table
Promotion attempts must also be recorded append-only.

### Required fields
- attempt id
- staged promotion id
- timestamp
- attempt number
- transport action
- outcome class
- remote status code if present
- remote rejection class if present
- receipt ref if present
- transport error class if present

## 4.4 Dead-letter visibility
Dead-letter items must remain visible as first-class persistent rows, not hidden logs.

---

# 5. Queue state machine

## 5.1 Required states
- `staged`
- `queued`
- `claimed_for_send`
- `send_failed_retryable`
- `awaiting_receipt_reconciliation`
- `accepted`
- `rejected`
- `dead_lettered`

## 5.2 State transition rules

### `staged -> queued`
Only after promotion admission passes.

### `queued -> claimed_for_send`
Only through a durable lease claim.

### `claimed_for_send -> accepted`
Only on explicit valid remote receipt.

### `claimed_for_send -> rejected`
Only on explicit non-retryable remote rejection.

### `claimed_for_send -> send_failed_retryable`
Only on retryable failure.

### `claimed_for_send -> awaiting_receipt_reconciliation`
Only when send may have succeeded but receipt truth is uncertain.

### `send_failed_retryable -> queued`
Only when retry timer matures.

### `awaiting_receipt_reconciliation -> accepted | rejected | queued | dead_lettered`
Must resolve explicitly.

### `* -> dead_lettered`
Only under dead-letter doctrine conditions.

---

# 6. Lease model

## 6.1 Required lease fields
- `claim_lease_owner`
- `claim_lease_expires_at`

## 6.2 First proving-slice posture
Recommended initial lease:
- duration: 60 seconds
- renewable while send/reconciliation is active
- expired lease returns the item to retryable eligibility

## 6.3 Anti-rules
Do not:
- use ambient in-memory ownership only
- allow indefinite claim locks
- allow send without durable claim semantics

---

# 7. Retry and reconciliation behavior

## 7.1 Retryable failure examples
- network timeout
- remote 5xx
- temporary overload
- temporary remote unavailability
- unreadable response body with uncertain outcome

## 7.2 Non-retryable failure examples
- invalid schema
- invalid signature
- blocked policy
- restricted payload
- unsupported version
- forbidden sensitivity class
- oversize payload

## 7.3 Retry parameters for slice 01
- exponential backoff base: 2
- initial delay: 30 seconds
- max delay: 15 minutes
- jitter required
- retry ceiling: 5 attempts

## 7.4 Receipt ambiguity rule
If a send may have succeeded but no trustworthy receipt exists:
- set state to `awaiting_receipt_reconciliation`
- do not mark accepted
- reconcile by idempotency key or explicit duplicate-safe recheck path

---

# 8. Promotion admission checks

A local artifact may enter staging only if all of the following pass:
- family admitted
- envelope valid
- payload valid
- signature present where required
- signer identity present
- sensitivity class permits promotion
- redaction policy passes
- payload size below ceiling
- version admitted
- policy checks pass

If any fail:
- do not stage it
- preserve durable local outcome
- classify the reason

---

# 9. Size and protection rules

## 9.1 Initial ceiling
Maximum canonical serialized envelope size: **256 KB**

## 9.2 Oversize behavior
Oversize items:
- do not proceed through normal staging
- remain local truth only
- record a durable blocked outcome
- appear in operator-visible blocked/dead-letter posture as policy requires

---

# 10. API / read-model surface for ForgeCommand

DataForge Local must expose a bounded read surface for ForgeCommand.

## 10.1 Required queue read model fields
- `system_id`
- `issue_summary`
- `artifact_family`
- `drift_class`
- `promotion_state`
- `confidence_posture`
- `created_at`
- `last_state_change_at`
- `staleness_posture`
- `changed_since_last_view`

## 10.2 Required detail read model fields
- canonical summary block
- evidence/reference summary
- lifecycle block
- rejection/dead-letter reason block
- audit/change history summary

## 10.3 Truthfulness rule
Derived read models must be explicitly derived and must never replace canonical lifecycle truth.

---

# 11. Validation integration

DataForge Local must consume `forge-contract-core` as its contract authority.

Required integration:
- canonical validator usage
- admitted family enforcement
- enum parity enforcement
- reference grammar enforcement
- idempotency-key generation via contract-core
- role/matrix constraints where applicable

No local redefinition of shared semantics is allowed.

---

# 12. Verification plan

## 12.1 Required test categories
- valid artifact persistence
- invalid artifact rejection
- promotion admission pass/fail
- queue lease claim behavior
- retry path
- rejection path
- dead-letter path
- duplicate send path
- receipt ambiguity path
- stale read-model truthfulness path

## 12.2 Property tests
Use property tests where practical for:
- queue-state invariants
- lease-expiry reclaim behavior
- idempotency-key stability

---

# 13. Documentation requirements

Before DataForge Local is considered proving-slice ready, it must no longer remain a baseline-only SYSTEM surface.

It must document:
- real runtime boundary
- real local-truth boundary
- real staging boundary
- real queue semantics
- real reconciliation/dead-letter rules
- real APIs/read models consumed by ForgeCommand

---

# 14. Exit criteria

DataForge Local is ready for slice 01 only when:
- local artifact persistence is real
- staging is real
- queue states are real
- lease semantics are real
- retry/reconciliation/dead-letter logic is real
- ForgeCommand-consumable read models are real
- all required verification gates pass
- SYSTEM docs reflect the implemented truth instead of baseline placeholders

Until then, DataForge Local should be treated as the intended target, not a completed proving-slice substrate.

