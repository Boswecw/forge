# Forge Implementation Pack 11 — DataForge Cloud Implementation Blueprint

**Date:** 2026-04-04 01:34 America/New_York  
**Purpose:** Give VSCode Opus 4.6 an implementation-ready blueprint for adding proving-slice shared intake, receipt, rejection, and duplicate reconciliation to the real DataForge Cloud system.

---

# 1. Mission

Implement the minimum cloud-side proving-slice boundary for:

**validated promoted artifact intake -> explicit accept/reject/duplicate outcome -> durable shared receipt/rejection truth -> bounded shared status surfaces**

This is not a broad new platform. It is a narrow intake and receipt slice.

---

# 2. Scope authorized in this blueprint

Only implement admitted support for:
- `source_drift_finding`
- `promotion_envelope`
- `promotion_receipt`

For the first implementation wave, Opus should optimize for one strong admitted-family path, not many partial ones.

---

# 3. First implementation tasks Opus should perform

## Task 1 — inspect the real DataForge Cloud repo structure
Because DataForge is already a mature service, Opus must fit the blueprint into the actual app structure instead of inventing a parallel stack.

Opus should inspect and map:
- router locations
- service layer locations
- schema model locations
- ORM model locations
- migration flow
- existing auth / policy surfaces

## Task 2 — add proving-slice intake schemas
Add typed request/response models for:
- promoted artifact intake request
- accepted response
- rejected response
- duplicate-reconciled response
- idempotency reconciliation lookup if used

## Task 3 — add persistence tables or columns
Implement durable persistence for:
- accepted shared records
- receipt records
- rejection records
- duplicate/replay observation metadata where needed

## Task 4 — add intake service
Implement untrusted-input validation and outcome classification.

## Task 5 — add receipt/rejection services
Implement explicit acceptance and rejection record persistence.

## Task 6 — add idempotency and duplicate reconciliation logic
Prevent duplicate canonical shared truth creation.

## Task 7 — expose bounded query/reconciliation surface
Support safe resolution of receipt ambiguity from local side.

## Task 8 — add tests and docs
Update docs to reflect actual proving-slice intake truth.

---

# 4. Required intake behavior

## 4.1 Validation order
Every inbound promoted artifact must be treated as untrusted until all of the following pass:
1. producer identity admitted
2. family admitted for that producer role
3. signature valid
4. envelope valid
5. payload valid
6. version admitted
7. sensitivity / visibility / promotion classes allowed
8. redaction class acceptable
9. payload size below ceiling
10. idempotency posture valid

## 4.2 Outcome rule
Each intake attempt must end in one explicit outcome:
- `accepted`
- `rejected`
- `duplicate_reconciled`

Do not blur acceptance and duplicate reconciliation into one vague success state.

---

# 5. Required persistence design

## 5.1 Shared accepted artifact table or extension
Opus should fit this to the real DataForge data model, but the proving slice requires durable storage for accepted shared artifacts.

Required fields include:
- `artifact_id`
- `artifact_family`
- `artifact_version`
- `lineage_root_id`
- `parent_artifact_id`
- `trace_id`
- `idempotency_key`
- `producer_identity`
- `signer_identity`
- serialized canonical body
- accepted timestamp
- sensitivity / visibility / promotion classes

## 5.2 Receipt table
Required receipt fields:
- `receipt_id`
- `related_artifact_ref`
- `intake_outcome`
- `shared_record_ref`
- `accepted_at`
- `idempotency_key`
- `producer_identity`
- `outcome_summary`

## 5.3 Rejection table
Required rejection fields:
- rejection id
- source artifact ref
- family
- producer identity
- rejection class
- rejection detail
- status code or internal code
- timestamp

## 5.4 Duplicate/replay metadata
At minimum, preserve:
- `artifact_id`
- `idempotency_key`
- `signer_identity`
- first seen time
- last seen time
- duplicate/replay disposition

---

# 6. Required services Opus should implement

## 6.1 `promotion_intake_service`
Responsibilities:
- validate incoming artifact using contract core
- validate producer admission and signature
- classify accepted / rejected / duplicate-reconciled outcome

## 6.2 `promotion_receipt_service`
Responsibilities:
- write durable receipt truth
- return bounded receipt response

## 6.3 `promotion_rejection_service`
Responsibilities:
- write durable rejection truth
- return bounded rejection response

## 6.4 `promotion_idempotency_service`
Responsibilities:
- detect already-accepted idempotency key
- bind duplicate send to existing shared truth
- return duplicate-safe reconciliation response

## 6.5 `promotion_reconciliation_query_service`
Responsibilities:
- support safe idempotency-based lookup for receipt ambiguity handling
- expose only bounded reconciliation information

---

# 7. API surfaces Opus should add

Opus should fit paths to actual DataForge conventions, but the cloud side requires:

## 7.1 Intake route
A bounded route for proving-slice family intake.

## 7.2 Reconciliation lookup route
A bounded route for idempotency-based reconciliation lookup or duplicate-safe receipt retrieval.

## 7.3 Optional bounded shared status read route
Only if needed for ForgeCommand or other read models, and only with visibility protection.

---

# 8. Contract-core integration

DataForge Cloud must import contract meaning from `forge-contract-core`.

Opus must not:
- redefine enums locally
- loosen field rules by convenience
- invent proving-slice wire fields not admitted in contract core

---

# 9. Security rules Opus must implement

## 9.1 Signature failures
Invalid signature -> non-retryable rejection -> durable rejection record -> no shared write.

## 9.2 Unsupported producer
Unsupported producer identity -> explicit rejection -> no shared write.

## 9.3 Oversize payload
Initial ceiling: **256 KB** canonical serialized envelope size.
Oversize -> explicit rejection -> no shared write.

## 9.4 Restricted visibility
Restricted or non-promotable payloads must never be exposed through broad review surfaces.

---

# 10. Required tests Opus must add

## 10.1 Acceptance tests
- valid artifact accepted
- receipt persisted
- shared record persisted

## 10.2 Rejection tests
- invalid schema rejected
- invalid signature rejected
- unsupported version rejected
- unsupported producer rejected
- oversize payload rejected

## 10.3 Duplicate/idempotency tests
- duplicate send does not create second shared record
- duplicate send returns duplicate-reconciled response
- idempotency lookup returns existing receipt/shared ref when appropriate

## 10.4 Adversarial tests
- same artifact replayed with altered metadata
- signature tamper attempt
- same idempotency key with conflicting body

---

# 11. Required documentation changes

Opus must update DataForge docs to include:
- proving-slice intake boundary
- acceptance/rejection/duplicate outcome semantics
- idempotency behavior
- receipt/reconciliation support
- producer identity and signature posture
- restricted-visibility handling

---

# 12. Anti-scope statement for Opus

Do not:
- add broad family intake beyond admitted families
- widen into recommendation or execution intake
- add speculative contradiction logic
- treat cloud intake as a generic telemetry sink
- flatten duplicate reconciliation into plain acceptance

Keep the cloud slice narrow and exact.

---

# 13. Implementation completion checklist

Opus should not declare this blueprint complete until:
- intake route exists
- validation pipeline exists
- acceptance/rejection persistence exists
- duplicate reconciliation exists
- bounded reconciliation lookup exists
- tests pass
- docs reflect implemented truth

If any are missing, shared intake is not ready.

