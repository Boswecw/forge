# Forge Implementation Pack 08 — Opus Master Build Protocol

**Date:** 2026-04-04 01:33 America/New_York  
**Purpose:** Give VSCode Opus 4.6 one master execution protocol for implementing the proving-slice architecture against the real Forge ecosystem.

---

# 1. What this implementation pack is for

This pack is not architecture discussion.
This pack is not critique.
This pack is not future-vision prose.

This pack exists so VSCode Opus 4.6 can begin implementation in a disciplined order without inventing system roles or flattening repo boundaries.

The implementation target is the narrow proving slice:

**admitted local producer emits `source_drift_finding` -> DataForge Local durable write -> DataForge Local promotion staging and lease-safe queue -> DataForge Cloud intake + receipt/rejection -> ForgeCommand truthful queue/detail rendering**

Nothing broader is authorized in the first wave.

---

# 2. Non-negotiable implementation truths

## 2.1 Real repo ownership
Opus must implement against actual repo roles:

- **ForgeCommand** = operator review/control surface
- **DataForge Cloud** = shared accepted-truth intake and receipt authority
- **DataForge Local** = intended local truth and staging substrate, after hardening
- **FA Local** = future bounded execution consumer, not in proving slice 01
- **Forge Eval** = deterministic evidence producer, not transport owner
- **ForgeMath** = canonical math authority where admitted, not transport owner
- **forgeHQ** = bounded proposal shaping, not truth owner

## 2.2 Maturity honesty
Opus must not assume that a repo with baseline documentation is already implementation-ready for critical ownership.

This especially applies to:
- DataForge Local
- forge-local-runtime

## 2.3 Contract-first order
No cross-repo implementation may proceed until the contract center exists.

---

# 3. Authorized implementation order

## Stage 1
Create **`forge-contract-core`**.

## Stage 2
Harden **DataForge Local** for local truth, staging, queue, reconciliation, and dead-letter behavior.

## Stage 3
Harden **DataForge Cloud** for shared intake, receipt, rejection, and duplicate reconciliation.

## Stage 4
Implement **ForgeCommand** proving-slice review UX and read-model integration.

## Stage 5
Wire cross-repo gates and run the end-to-end proving slice.

No execution-family work is allowed before those stages are real and green.

---

# 4. Opus operating rules

## 4.1 Do not invent hidden scope
If a family, route, table, or adapter is not explicitly in the proving-slice plan, Opus must not add it by convenience.

## 4.2 Do not widen family scope
Only these families are authorized in the first wave:
- `source_drift_finding`
- `promotion_envelope`
- `promotion_receipt`

## 4.3 Do not collapse truth layers
Opus must keep distinct:
- local canonical truth
- local staging truth
- shared accepted truth
- derived read models
- operator review state

## 4.4 Do not smuggle execution into slice 01
FA Local execution work is future-phase only.

## 4.5 Do not re-interpret shared semantics locally
Each repo must import shared meaning from `forge-contract-core`.

---

# 5. Required delivery style for implementation

Opus should work in bounded slices.
Each slice should produce:
- exact files changed
- exact new files created
- exact schema or table additions
- exact route additions
- exact tests added
- exact docs updated
- explicit anti-scope statement

If a slice cannot be stated that concretely, it is too large.

---

# 6. Definition of done for each repo slice

A repo slice is only done when all are true:
- code exists
- tests exist
- docs reflect implemented truth
- no hidden TODO is carrying required behavior
- no placeholder name remains where real semantics were required
- scope did not drift beyond admitted proving-slice needs

---

# 7. Required downstream implementation canvases in this pack

Opus should use the following companion documents from this implementation pack:

1. **Pack 09 — forge-contract-core Implementation Blueprint**
2. **Pack 10 — DataForge Local Implementation Blueprint**
3. **Pack 11 — DataForge Cloud Implementation Blueprint**
4. **Pack 12 — ForgeCommand Implementation Blueprint**
5. **Pack 13 — Cross-Repo Test and Gate Blueprint**
6. **Pack 14 — Opus Repo-by-Repo Run Order and Handoff Checklist**

---

# 8. Final instruction to Opus

Implement the proving slice as a narrow architecture proof, not a platform rollout.

The goal is not to make the ecosystem feel broad.
The goal is to prove that one admitted family can survive:
- contract validation
- local durability
- lease-safe transport
- remote acceptance/rejection
- idempotent reconciliation
- dead-letter truth
- honest operator rendering

If that proof is weak, do not widen scope.
If that proof is strong, future slices can follow.

