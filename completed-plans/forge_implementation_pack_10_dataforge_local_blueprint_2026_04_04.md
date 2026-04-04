# Forge Implementation Pack 10 — DataForge Local Implementation Blueprint

**Date:** 2026-04-04 01:34 America/New_York  
**Purpose:** Give VSCode Opus 4.6 an implementation-ready blueprint for turning DataForge Local into the real local durable truth and promotion-staging substrate for proving slice 01.

---

# 1. Mission

Implement the minimum real DataForge Local surfaces required for:

**local artifact persistence -> promotion admission -> durable staging -> lease-safe outbound queue -> retry/reconciliation/dead-letter truth -> read models for ForgeCommand**

This is a hardening slice, not a broad product build.

---

# 2. Scope authorized in this blueprint

Only implement support for:
- `source_drift_finding`
- `promotion_envelope`
- `promotion_receipt`

Do not add:
- execution families
- approval families
- recommendation families
- contradiction families
- rollback families
- calibration families

---

# 3. First implementation tasks Opus should perform

## Task 1 — inspect the real DataForge Local repo structure
Opus should first inspect the actual repo and determine:
- current package/runtime entry points
- database/migration pattern
- test pattern
- existing schema or persistence modules

Then Opus should fit this blueprint into the repo’s real structure instead of forcing a fake layout.

## Task 2 — add proving-slice schema models
Create local typed schema models for:
- canonical local artifact record
- promotion admission result
- staging row
- queue status record
- receipt/rejection reconciliation record
- queue/detail read models

## Task 3 — add migrations
Implement database migrations for proving-slice persistence.

## Task 4 — implement validators through contract core
Integrate `forge-contract-core` validation and idempotency logic.

## Task 5 — implement local persistence service
Persist valid local artifacts durably.

## Task 6 — implement promotion admission service
Check admission rules before staging.

## Task 7 — implement staging + queue service
Create durable queue state and lease-safe claim behavior.

## Task 8 — implement reconciliation service
Handle accepted, rejected, retry-pending, ambiguity, and dead-letter transitions.

## Task 9 — expose bounded read models
Provide the queue/detail surface consumed by ForgeCommand.

## Task 10 — add tests and documentation
Update repo docs from baseline to actual proving-slice truth.

---

# 4. Required persistence design

## 4.1 Local canonical artifacts table
Opus should implement one local canonical artifacts table with fields covering:
- `artifact_id`
- `artifact_family`
- `artifact_version`
- `produced_by_system`
- `produced_by_component`
- `source_scope`
- `lineage_root_id`
- `parent_artifact_id`
- `trace_id`
- `idempotency_key`
- `created_at`
- `recorded_at`
- `sensitivity_class`
- `visibility_class`
- `promotion_class`
- `validation_status`
- `signer_identity`
- `signature`
- serialized payload body

## 4.2 Promotion staging table
Implement one staging table with fields covering:
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

## 4.3 Promotion attempt audit table
Append-only audit records for each transport attempt.

## 4.4 Optional separate local blocked-outcome table
If the real repo structure benefits from it, Opus may add a dedicated blocked/rejected-local-outcome table instead of overloading staging for pre-stage failures.

---

# 5. Queue and lifecycle semantics

## 5.1 Required queue states
- `staged`
- `queued`
- `claimed_for_send`
- `send_failed_retryable`
- `awaiting_receipt_reconciliation`
- `accepted`
- `rejected`
- `dead_lettered`

## 5.2 Required lease posture
Initial proving-slice lease behavior:
- 60 second lease
- renewable while active work continues
- expired leases return item to eligible retry path
- no indefinite lock ownership

## 5.3 Retry posture
- initial delay: 30 seconds
- exponential backoff base 2
- max delay: 15 minutes
- jitter required
- retry ceiling: 5 attempts

## 5.4 Dead-letter posture
Automatic transport stops and item becomes operator-visible dead-letter truth when:
- retries exhausted
- structural invalidity is non-retryable
- policy rejection requires review
- receipt ambiguity exceeds safe ceiling
- repeated signature/version failure persists

---

# 6. Services Opus should implement

## 6.1 `artifact_ingest_service`
Responsibilities:
- validate artifact through contract core
- persist local canonical artifact
- reject invalid local ingest cleanly

## 6.2 `promotion_admission_service`
Responsibilities:
- determine whether local artifact may enter staging
- enforce family/version/sensitivity/redaction/size rules
- emit durable local admission outcome

## 6.3 `promotion_queue_service`
Responsibilities:
- create staging rows
- move rows into queued state
- claim lease
- release expired claim
- prepare rows for remote transport worker

## 6.4 `promotion_reconciliation_service`
Responsibilities:
- process accepted receipts
- process explicit rejections
- process retryable failures
- process receipt ambiguity
- resolve dead-letter transitions

## 6.5 `promotion_read_model_service`
Responsibilities:
- build queue rows for ForgeCommand
- build detail view records for ForgeCommand
- preserve derived/read-model labeling

---

# 7. Bounded API or read surface

Opus must fit this to the repo’s real runtime style, but the proving slice requires a bounded read surface.

At minimum, implement surfaces for:
- queue listing
- queue section filtering
- detail retrieval by item id or artifact ref
- audit/change-history summary retrieval

If the repo is not yet exposing a network API, Opus may first implement a service/read-model layer plus tests, but should state that explicitly and not pretend the API already exists.

---

# 8. Required read-model fields for ForgeCommand

## Queue row
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

## Detail model
- summary header data
- evidence summary
- references summary
- promotion lifecycle block
- rejection/dead-letter reason block
- audit/change history summary

---

# 9. Required validation integration

Every admitted artifact entering DataForge Local must use `forge-contract-core` for:
- envelope validation
- family payload validation
- enum parity
- reference grammar
- idempotency-key generation
- supported version checks

No local semantic overrides are allowed.

---

# 10. Required tests Opus must add

## 10.1 Persistence tests
- valid artifact persists
- invalid artifact does not persist as valid
- local blocked outcome is durable

## 10.2 Staging tests
- admitted artifact stages successfully
- blocked artifact does not stage
- oversize or restricted artifact is blocked

## 10.3 Queue tests
- claim lease works
- expired claim returns to queue eligibility
- retry state computes next retry time
- retry ceiling dead-letters correctly

## 10.4 Reconciliation tests
- accepted receipt resolves accepted state
- explicit rejection resolves rejected state
- ambiguous receipt resolves to awaiting reconciliation
- duplicate-safe behavior preserves truthfulness

## 10.5 Read-model tests
- queue row reflects real state
- dead-letter reason surfaces correctly
- stale or unknown state does not appear accepted

---

# 11. Required documentation changes

Opus must upgrade DataForge Local docs from baseline posture.

Minimum new authored topics:
- proving-slice local truth role
- staging and queue state model
- lease/retry/dead-letter semantics
- read-model surfaces for ForgeCommand
- contract-core integration
- hard anti-scope statement

---

# 12. Anti-scope statement for Opus

Do not:
- implement execution handoff
- add recommendation logic
- add contradiction arbitration
- add broad multi-family support
- add speculative throughput optimization
- assign shared-truth authority to DataForge Local

Keep this repo hardening slice narrow.

---

# 13. Implementation completion checklist

Opus should not declare this blueprint complete until:
- migrations exist
- canonical local artifact persistence exists
- staging exists
- queue states exist
- lease logic exists
- retry/dead-letter logic exists
- read models exist
- tests pass
- docs reflect implemented truth

If docs remain baseline-only afterward, the repo is not ready.

