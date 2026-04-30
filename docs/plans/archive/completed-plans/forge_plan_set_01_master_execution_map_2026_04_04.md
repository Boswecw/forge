# Forge Plan Set 01 — Master Execution Map

**Date:** 2026-04-04 01:18 America/New_York  
**Purpose:** Establish the real implementation map for the next planning wave using the systems that actually exist now.

---

# 1. Planning rule

This plan set is written against the actual ecosystem as it exists today.

It does **not** assume that every intended repo is equally mature.  
It does **not** assign authority to placeholder or baseline-only surfaces just because they exist.  
It does **not** collapse future-state architecture into current-state implementation.

Every downstream plan in this set must obey that rule.

---

# 2. Actual authority map

## 2.1 Operator control and review
**ForgeCommand**

Owns:
- operator queue and detail views
- review workflow surfaces
- changed-since-last-view visibility
- dead-letter and retry visibility
- lifecycle rendering
- bounded operational follow-through visibility

Does not own:
- shared schema meaning
- canonical durable truth
- execution authority by convenience

## 2.2 Shared durable truth
**DataForge Cloud**

Owns:
- accepted shared truth for admitted promoted families
- shared receipts and rejection outcomes
- idempotent duplicate resolution
- shared lineage for admitted families

Does not own:
- local runtime control
- hidden execution authority
- convenience replication of local stores

## 2.3 Local durable truth and transport staging
**DataForge Local**

Intended to own:
- local canonical truth for admitted local artifacts
- local promotion staging
- queue truth
- reconciliation truth
- dead-letter truth

But:
- current documentation posture is still baseline
- this repo requires an explicit hardening phase before it can safely own the full slice

## 2.4 Future local execution authority
**FA Local**

Owns in future phases:
- bounded execution request intake
- policy-before-execution enforcement
- capability-scoped execution admission
- truthful execution status writeback
- review-package and forensic event support

Does not belong in proving slice 01.

## 2.5 Deterministic evidence producers
**Forge Eval**
- deterministic evaluation artifact producer only
- not shared-truth owner
- not transport owner
- not review owner

## 2.6 Canonical math/scoring authority
**ForgeMath**
- governed lane math authority
- not transport owner
- not operator approval owner
- not execution owner

## 2.7 Bounded proposal shaping
**forgeHQ**
- non-authoritative proposal-generation subsystem
- not truth owner
- not transport owner
- not execution owner

## 2.8 Real but not first-wave proving-slice backbone systems
**CortexBDS**  
**NeuronForge Local**  
**forge-local-runtime**

These are real ecosystem systems and matter architecturally.

But for the next implementation wave they should **not** be treated as the proving-slice backbone unless and until their role-specific contracts and runtime surfaces are explicitly authored and proven.

---

# 3. Repo maturity classification

## 3.1 Strong current anchors
Use these as immediate planning anchors:

- ForgeCommand
- DataForge Cloud
- FA Local
- Forge Eval
- ForgeMath

## 3.2 Real but still under-authored for critical proving-slice ownership
Treat these as requiring hardening before critical ownership:

- DataForge Local
- forge-local-runtime
- forgeHQ
- CortexBDS
- NeuronForge Local

## 3.3 New repo required
**forge-contract-core**

This repo must be created as a first-class prerequisite.  
Do not let contract meaning diffuse into existing repos.

---

# 4. Corrected proving slice 01

## 4.1 Narrow slice statement

**admitted local producer emits `source_drift_finding` -> DataForge Local durable write -> DataForge Local promotion staging and lease-safe queue -> DataForge Cloud receipt/rejection intake -> ForgeCommand truthful queue/detail rendering**

## 4.2 What slice 01 proves
- contract discipline
- local durability
- policy-gated promotion admission
- lease-safe queue behavior
- retry/reconciliation truth
- dead-letter truth
- receipt-based shared acceptance
- operator-visible lifecycle honesty

## 4.3 What slice 01 explicitly excludes
- FA Local execution
- approval families
- execution request families
- recommendation families
- contradiction arbitration
- rollback families
- calibration proposals
- multi-family promotion
- high-throughput optimization
- broad multi-producer expansion

---

# 5. Locked decisions for the next planning wave

## Lock 1
A new canonical contract repo named **`forge-contract-core`** is required before broader shared-family implementation.

## Lock 2
**DataForge Local** is the intended local durable truth and promotion-staging substrate, but only after an explicit hardening phase.

## Lock 3
**DataForge Cloud** remains the shared accepted-truth and receipt authority.

## Lock 4
**ForgeCommand** is the only proving-slice operator review surface.

## Lock 5
**FA Local** is the future execution consumer and remains excluded from proving slice 01.

## Lock 6
No repo with only baseline documentation-protocol adoption may be assigned critical proving-slice authority without a hardening phase.

## Lock 7
CortexBDS, NeuronForge Local, and forge-local-runtime remain real ecosystem systems but are not first-wave proving-slice backbone owners.

---

# 6. Required plan stack

This master map governs the following downstream plans:

1. **Plan 02 — forge-contract-core Bootstrap Plan**
2. **Plan 03 — DataForge Local Proving-Slice Hardening Plan**
3. **Plan 04 — DataForge Cloud Shared Intake and Receipt Plan**
4. **Plan 05 — ForgeCommand Proving-Slice Review UX Plan**
5. **Plan 06 — Cross-Repo Gate and Compatibility Rollout Plan**
6. **Plan 07 — Future Execution Bridge Plan (FA Local)**

---

# 7. Implementation sequence

## Phase A — Contract center first
Create and lock `forge-contract-core`.

## Phase B — DataForge Local hardening
Author local truth, staging, queue, reconciliation, and dead-letter surfaces.

## Phase C — DataForge Cloud intake hardening
Add shared intake, receipt, rejection, idempotency, and signature checks.

## Phase D — ForgeCommand review surface
Build the queue/detail review slice against real read models and real lifecycle states.

## Phase E — End-to-end proving slice 01
Connect one admitted producer, one admitted family, one truthful review surface.

## Phase F — Only then widen scope
Only after proving slice 01 is green should new families, more producers, and future execution bridges enter implementation.

---

# 8. Hard anti-rules

Do not:
- assign abstract “local runtime” ownership when a real repo should be named
- assume DataForge Local is already fully hardened because it is conceptually correct
- widen ForgeCommand into a speculative action console during proving slice 01
- smuggle FA Local execution into the first proving slice
- treat proposal, scoring, and execution systems as transport owners
- let contract meaning drift into multiple repos

---

# 9. Exit condition for this master map

This plan is considered ready when all downstream plans align to:

- real repo ownership
- explicit maturity-aware sequencing
- proving-slice narrowness
- honest authority boundaries
- contract-first implementation order

Anything that violates those rules should be revised before implementation starts.

