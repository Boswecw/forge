# Forge Plan Set 04 — DataForge Cloud Shared Intake and Receipt Plan

**Date:** 2026-04-04 01:19 America/New_York  
**Purpose:** Define the exact cloud-side intake and shared-truth receipt boundary for proving slice 01 using the real DataForge Cloud system.

---

# 1. Mission

DataForge Cloud must act as the **shared accepted-truth intake and receipt authority** for admitted proving-slice families.

It must:
- validate incoming promoted artifacts as untrusted input
- accept only admitted families and versions
- preserve idempotent shared truth
- emit explicit receipts or explicit rejections
- maintain shared lineage for accepted artifacts

It must not:
- act like a free-form telemetry collector
- silently coerce invalid payloads into storage
- replicate local stores wholesale
- become hidden execution authority

---

# 2. First admitted intake scope

Admit only:
1. `source_drift_finding`
2. `promotion_envelope`
3. `promotion_receipt`

For proving slice 01, intake should primarily support the shared acceptance flow for `source_drift_finding` plus the receipt/rejection contract.

No approval, execution, recommendation, contradiction, rollback, or calibration families are allowed in this wave.

---

# 3. Intake boundary behavior

## 3.1 Core posture
Every inbound payload is untrusted until all validation gates pass.

## 3.2 Required validations before shared storage
DataForge Cloud must validate:
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

## 3.3 Outcome rule
Every intake attempt must end in one explicit outcome:
- accepted
- rejected
- duplicate_reconciled
- quarantined (only where explicitly admitted later; not default proving-slice behavior)

---

# 4. Shared persistence model

## 4.1 Accepted shared artifact storage
Accepted artifacts must be stored durably as shared truth with lineage-preserving identity.

### Required fields
- `artifact_id`
- `artifact_family`
- `artifact_version`
- `lineage_root_id`
- `parent_artifact_id`
- `trace_id`
- `idempotency_key`
- `signer_identity`
- canonical serialized body
- shared accepted timestamp
- source producer identity
- sensitivity/visibility/promotion classes

## 4.2 Receipt storage
Every acceptance or duplicate reconciliation must have a durable receipt record.

### Required fields
- `receipt_id`
- `receipt_family`
- `related_artifact_ref`
- `intake_outcome`
- `idempotency_key`
- `accepted_at`
- `shared_record_ref`
- `producer_identity`
- `intake_version`
- `validation_result_summary`

## 4.3 Rejection storage
Explicit rejections must also be durable.

### Required fields
- rejection id
- source artifact id/ref
- family
- producer identity
- rejection class
- rejection reason detail
- status code or internal code
- timestamp

---

# 5. Idempotency behavior

## 5.1 Rule
The same effective promoted artifact must never create multiple shared canonical records.

## 5.2 Required behavior on duplicate send
If the same effective artifact arrives again with the same idempotency key:
- do not create a second shared record
- return a duplicate-reconciled or existing-receipt response
- preserve linkage to existing shared truth

## 5.3 Anti-rule
Do not treat duplicates as generic conflicts without duplicate-safe reconciliation semantics.

---

# 6. Remote response contract

## 6.1 Accepted response
Must include:
- acceptance outcome
- shared record reference
- receipt reference
- timestamp
- idempotency linkage

## 6.2 Rejected response
Must include:
- rejection outcome
- rejection class
- rejection summary
- whether retry is allowed
- timestamp

## 6.3 Duplicate-reconciled response
Must include:
- duplicate-reconciled outcome
- existing shared record reference
- existing receipt reference
- idempotency linkage
- timestamp

## 6.4 Truthfulness rule
The remote side must never blur fresh acceptance and duplicate reconciliation into one ambiguous success response.

---

# 7. Security checks

## 7.1 Producer identity
Accept only admitted producer identities.

## 7.2 Signature validation
If signature validation fails:
- reject as non-retryable
- do not stage shared truth
- record the attempt durably

## 7.3 Size protection
Initial maximum canonical serialized payload size: **256 KB**.

Oversize behavior:
- reject non-retryable
- no shared write
- durable rejection record required

## 7.4 Restricted visibility handling
Restricted or non-promotable payload classes must never be exposed broadly to the review surface.

---

# 8. Version handling

## 8.1 Supported version rule
Only admitted supported versions may be accepted.

## 8.2 Unsupported version rule
Unsupported versions must be explicitly rejected.

## 8.3 Future dual-read posture
Dual-read support may exist later for version transitions, but should not widen proving slice 01 unnecessarily.

---

# 9. DataForge Cloud API surface

## 9.1 Required proving-slice intake route
A bounded intake route should accept only the admitted family set.

## 9.2 Required query/reconciliation support
A bounded idempotency-based reconciliation lookup path is required for safe receipt ambiguity handling.

## 9.3 Required read model for ForgeCommand
ForgeCommand should not read raw restricted payloads directly.

Instead, DataForge Cloud should expose or support derived shared-status read models where needed, with visibility constraints preserved.

---

# 10. Verification plan

## 10.1 Required tests
- valid acceptance path
- explicit rejection path
- duplicate reconciliation path
- invalid signature path
- unsupported version path
- oversize payload path
- blocked family path
- blocked sensitivity/visibility path
- idempotency conflict safety path

## 10.2 Adversarial tests
- replay of same artifact with altered metadata
- duplicate send with same idempotency key
- duplicate send after accepted receipt already exists
- tampered signature with admitted producer identity

---

# 11. Integration with contract core

DataForge Cloud must import shared contract meaning from `forge-contract-core`.

It may not:
- redefine family semantics locally
- reinterpret enums by convenience
- invent undocumented additional proving-slice wire fields

---

# 12. Documentation requirements

DataForge Cloud SYSTEM-level docs must explicitly reflect:
- proving-slice intake boundary
- receipt and rejection semantics
- idempotency behavior
- producer identity checks
- shared-truth ownership rules
- review-surface visibility boundaries

---

# 13. Exit criteria

DataForge Cloud is ready for proving slice 01 only when:
- admitted family intake is implemented
- all required validation checks are implemented
- receipt and rejection records are durable
- duplicate reconciliation is real
- restricted visibility handling is real
- verification gates pass
- documentation reflects the live intake truth

Until then, broader shared transport should not be declared ready.

