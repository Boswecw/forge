# Forge Plan Set 07 — FA Local Future Execution Bridge Plan

**Date:** 2026-04-04 01:20 America/New_York  
**Purpose:** Define the future execution-family bridge using FA Local as the real bounded local execution consumer after proving slice 01 succeeds.

---

# 1. Why this plan exists

The ecosystem already has a real bounded local execution-control service: **FA Local**.

That means future execution-family planning should stop using vague “local runtime execution layer” wording and instead align to FA Local’s actual architecture and doctrine.

This plan is intentionally future-phase.
It is **not** part of proving slice 01.

---

# 2. Actual FA Local posture that matters

FA Local already has strong bounded doctrine:
- requester trust before admission
- policy before execution
- capability-scoped execution
- fail closed by default
- review-package emission when work is not directly admissible
- truthful execution status
- minimized forensics

That makes it the correct target for future execution-family consumption.

It is **not**:
- a product UI
- a semantic authority
- a hidden planner
- a generic agent runtime
- an unbounded orchestration layer

Any future bridge must respect that.

---

# 3. What this plan does not do

This plan does not:
- move execution into slice 01
- assume broad adapter support already exists
- assume multi-adapter runtime maturity
- assume persistence is already built in FA Local
- assume approval semantics can be invented by convenience

It only defines the bridge target and the execution-family posture that should be pursued later.

---

# 4. Future role class

## 4.1 FA Local role class
- `execution_consumer`

## 4.2 What that means
FA Local should eventually consume only admitted execution-request families and write back truthful execution-status artifacts.

It should not own:
- recommendation generation
- approval semantics
- candidate proposal meaning
- operator decision authority

---

# 5. Future execution-family preconditions

No execution-family work should begin until all of the following are true:

1. proving slice 01 is green
2. contract core exists and is stable
3. admitted execution-family schemas exist in contract core
4. DataForge Local and DataForge Cloud proving-slice transport is stable
5. ForgeCommand review surfaces are truthful
6. FA Local adapter and persistence posture are sufficiently authored for execution-family work

If those preconditions are not met, execution-family implementation is premature.

---

# 6. Future family set

These are future families only, not current admitted proving-slice families:
- `approval_artifact`
- `execution_request`
- `execution_status_event`
- `verification_result`
- `rollback_result`

Do not admit them early.

---

# 7. Correct future authority chain

The future execution bridge should follow this posture:

**upstream evidence or recommendation artifacts -> review and approval surfaces -> admitted execution request artifact -> FA Local policy/capability admission -> bounded adapter delivery -> execution-status writeback -> review visibility in ForgeCommand**

This keeps the system honest.

---

# 8. Why FA Local is the right bridge target

FA Local already aligns with the execution doctrine the ecosystem needs:
- policy-first admission
- capability registry
- bounded execution plans
- explicit approval posture
- truthful degraded/partial/completed states
- review-package support when direct execution is not allowed

That makes it a far better real target than abstract future “local runtime shell” language.

---

# 9. What must be added before execution-family work

## 9.1 Contract-core additions
Before FA Local execution-family work begins, contract core must add:
- execution request schema
- execution status schema
- approval artifact schema
- authorization class vocabulary
- verification-result schema
- rollback-result schema

## 9.2 FA Local-specific hardening likely needed
Because FA Local is still intentionally bounded, future work will need to determine:
- persistence strategy
- execution status writeback destination and contract binding
- adapter expansion roadmap
- execution-family verification gates

## 9.3 ForgeCommand implications
ForgeCommand will later need:
- approval review surfaces
- execution status surfaces
- bounded follow-through visibility

But none of that should enter slice 01.

---

# 10. Hard anti-rules

Do not:
- treat FA Local as a hidden planner
- feed it recommendation candidates as if they were execution requests
- collapse approval and execution status into one state model
- bypass policy/capability admission because an upstream system “already checked it”
- let execution work start before transport/read-model truth is proven first

---

# 11. Future phased plan

## Phase X1 — execution-family contract admission
Add the future execution-family schemas and gates in contract core.

## Phase X2 — FA Local contract integration
Map admitted execution-family schemas to FA Local’s actual execution request / status / review-package posture.

## Phase X3 — bounded persistence and writeback design
Decide how FA Local writes truthful execution status back into local/shared truth without violating existing authority boundaries.

## Phase X4 — first bounded adapter-backed execution path
Implement one bounded, capability-scoped execution family through FA Local.

## Phase X5 — ForgeCommand execution review slice
Add truthful operator follow-through surfaces after the first execution path is real.

---

# 12. Exit condition for this plan

This plan is ready when the ecosystem is locked on one future execution target:

**FA Local is the future bounded execution consumer.**

That decision should now be treated as a planning anchor so later phases do not drift back into vague execution-layer wording.

