# VERITAS Forge Proof Engine — Metadata Plan

**Date:** 2026-02-26
**Version:** v1
**Author:** BDS Architecture
**Status:** Metadata (pre-spec planning)
**Target:** Forge Ecosystem governance layer (SMITH primary, extensible to all services)
**Context:** Solo developer, non-coder architect directing AI executor
**Stack:** Node/TypeScript — runs anywhere Forge runs, no Rust toolchain dependency
**Companion:** VERITAS T8–T10 Implementation Plan (TSA integration), VERITAS Foundation–T7 Metadata (supersedes T0–T6 for governance concerns)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-02-26 | Initial plan. Replaces VERITAS T0–T6 tool-heavy approach with Node-based exhaustive model checker for governance verification. Retains evidence schema, assurance levels, TSA integration, and traceability from original VERITAS. |

---

## 1. Problem Statement

VERITAS Foundation–T7 designed a 14-tool, 8-tier verification system targeting the general case: memory safety, concurrency, information flow, formal proofs. That plan requires 81–132 sessions for a non-coder architect working through AI, with the hardest tiers (loom, Verus) producing the most friction and the least governance-relevant output.

The actual failure modes that threaten Forge are governance failures:

- An illegal state transition (pipeline advances without approval)
- An AI agent bypassing authority gates
- Evidence being skipped or forged
- Authority mis-escalation (Ring 2 action executed at Ring 0)
- A fail-open condition (circuit breaker allows requests when it shouldn't)
- A hash chain fork (two entries claiming the same predecessor)
- A nonce replay (same nonce accepted twice)

Every one of these is a **state machine error**. Every one is **exhaustively verifiable** over a finite state space. None of them require Rust-tier tooling.

Rust already handles memory safety. Tauri handles IPC type safety. SQLite handles transaction atomicity. The 2,100 existing tests handle basic correctness. What's missing is mathematical proof that the governance logic is airtight.

A Node model checker provides that proof directly.

---

## 2. Classification

**Blast Radius:** Class B — Single subsystem (verification tooling, no production code changes)
**Frozen core:** RunIntent.v1, MRPA, ECD untouched. The model checker reads governance definitions — never modifies them.
**Relationship to VERITAS:** This IS VERITAS, rescoped. Same evidence schema, same assurance levels, same traceability. Different implementation strategy.

---

## 3. Naming

| Surface | Name |
|---------|------|
| Feature umbrella | VERITAS Forge Proof Engine |
| Core module | StateForge (the model checker) |
| Evidence output | Assurance Level (AL-0 through AL-5) |
| Configuration | `veritas.toml` |
| Integration | TSA (Typed Specification Algebra) for requirement-to-invariant extraction |

---

## 4. What a Node Model Checker Actually Is

Not a test suite. Not a fuzzer. Not a type checker. A model checker is a program that:

1. Takes a **model** — a complete definition of states, transitions, guards, and invariants
2. **Exhaustively explores** every reachable state through every possible transition sequence
3. **Verifies** that every invariant holds in every reachable state
4. **Reports** either "all invariants hold for all N reachable states" or "invariant X violated via path [S1 → S2 → S3]"

For finite state machines — which governance IS — exhaustive exploration is **mathematically complete**. It doesn't sample. It doesn't approximate. It checks everything. If it says the invariant holds, the invariant holds. Period.

This is what TLA+ does. What we're building is TLA+ semantics in TypeScript, purpose-built for Forge's governance vocabulary, readable by a non-coder, and integrated into the VERITAS evidence chain.

### What It Covers

| Concern | Verifiable? | Method |
|---------|-------------|--------|
| Illegal state transitions | Yes — exhaustive | Path exploration over transition graph |
| Approval bypass | Yes — exhaustive | Guard predicates checked at every transition |
| Evidence chain integrity | Yes — exhaustive | Invariant: every non-initial state has evidence |
| Authority escalation | Yes — exhaustive | Authority ring predicates on every transition |
| Fail-open conditions | Yes — exhaustive | Circuit breaker model with invariants |
| Hash chain fork | Yes — exhaustive | Invariant: single predecessor per entry |
| Nonce replay | Yes — exhaustive | Invariant: nonce uniqueness across state space |
| Reachability | Yes — exhaustive | "Can FAILED be reached from any non-terminal?" |
| Deadlock freedom | Yes — exhaustive | Every non-terminal state has at least one outgoing transition |
| Liveness | Yes — bounded | "Eventually reaches terminal" within bounded steps |

### What It Does NOT Cover

| Concern | Why Not | Fallback (if ever needed) |
|---------|---------|--------------------------|
| Memory safety | Rust ownership handles this | N/A — already solved |
| Concurrency races | Requires interleaving exploration | `loom` — targeted, per-function, future |
| Byte-level crypto correctness | Requires implementation-level proof | Verus — targeted, 3 functions, future |
| Crash recovery | Requires fault injection | `cargo-fuzz` — targeted, future |
| Performance regression | Requires benchmarking | `criterion` — lightweight, future |

The fallback column is not "never" — it's "not now." If you ever need to verify that Ed25519 signing handles degenerate keys correctly, you add a targeted Verus proof for that one function. You don't build an 8-tier system to get there.

---

## 5. Capability Decomposition

### 5.1 StateForge — The Model Checker Core

The heart of the system. A TypeScript library that defines, explores, and verifies state machine models.

**What it does:**
- Defines state machines as typed objects (states, transitions, guards, effects)
- Exhaustively generates every reachable state from the initial state
- At every state, checks every invariant
- At every transition, checks every guard
- Reports: total states explored, transitions taken, invariants checked, violations found
- On violation: produces the exact path from initial state to violation

**Architecture:**

```
Model Definition (TypeScript)
    │
    ▼
State Space Generator
    │ Breadth-first exploration
    │ Visited-state deduplication
    │ Cycle detection
    ▼
Invariant Checker
    │ Every invariant × every state
    ▼
Guard Validator
    │ Every guard × every transition
    ▼
Evidence Emitter
    │ Hash-chained verification record
    ▼
Report (pass/fail + counterexample paths)
```

### 5.2 Model Library — Forge Governance Models

Pre-built models for every governance-critical state machine in Forge.

**Model 1: Pipeline State Machine**
```
States: IDLE, PLANNING, PLAN_REVIEW, APPROVED, EXECUTING, 
        EVIDENCE_REVIEW, RELEASED, FAILED, ABANDONED
Locked: PLAN_REVIEW, EVIDENCE_REVIEW
Terminal: RELEASED, FAILED, ABANDONED
```

Invariants:
- No path from any locked state to any post-locked state without human approval
- FAILED is reachable from every non-terminal state
- RELEASED is only reachable through EVIDENCE_REVIEW
- Terminal states have no outgoing transitions
- Every non-terminal state has at least one outgoing transition (deadlock freedom)

**Model 2: Authority Ring System**
```
Rings: RING_0 (human only), RING_1 (human + SMITH), RING_2 (automated)
Actors: Human, SMITH, ForgeAgent, System
```

Invariants:
- No RING_0 action executed by non-Human actor
- RING_1 actions require SMITH authority token
- Authority never escalates without explicit grant
- Revocation propagates to all downstream grants

**Model 3: Circuit Breaker FSM**
```
States: CLOSED, OPEN, HALF_OPEN
Counters: failure_count, success_count, cooldown_elapsed
```

Invariants:
- No requests pass when OPEN (fail-closed guarantee)
- Transition to OPEN requires failure_count ≥ threshold
- HALF_OPEN allows exactly one probe request
- Return to CLOSED requires probe success
- Cooldown must elapse before OPEN → HALF_OPEN

**Model 4: Evidence Chain**
```
States: EMPTY, APPENDING, SEALED
Entries: { hash, prev_hash, data, timestamp }
```

Invariants:
- Every entry except genesis has exactly one predecessor
- No two entries share the same prev_hash (no fork)
- Hash is computed over (data ∥ prev_hash) — deterministic
- SEALED chains accept no new entries
- Entries are append-only (no modification after creation)

**Model 5: BugCheck Finding Lifecycle**
```
States: NEW, TRIAGED, IN_PROGRESS, BLOCKED, RESOLVED, 
        DISMISSED, VERIFIED, CLOSED
Severities: S0, S1, S2
```

Invariants:
- S0 findings cannot be DISMISSED
- S1 dismissals require justification (non-empty reason)
- No transition from CLOSED to any non-CLOSED state
- VERIFIED requires all linked code changes merged
- Every finding reaches a terminal state (CLOSED) — no orphans

**Model 6: MRPA Patch Workflow**
```
States: PENDING, BACKED_UP, STAGED, APPLYING, VERIFYING, 
        COMMITTED, ROLLING_BACK, ROLLED_BACK, FAILED
```

Invariants:
- COMMITTED only reachable through VERIFYING
- If VERIFYING fails, ROLLING_BACK is the only transition
- ROLLED_BACK means all files match BACKED_UP state
- No partial state: either all files applied or all files restored
- FAILED is reachable from every non-terminal state

**Model 7: Nonce Replay Prevention**
```
States: per-session nonce registry
Operations: generate, submit, validate, expire
```

Invariants:
- No nonce accepted twice within a session
- Expired nonces cannot be resubmitted
- Nonce generation produces unique values (model uses sequence counter)

**Model 8: Integration Law Composition**

Composes Models 1–7 at service boundaries to verify the Five Integration Laws:
- Law 1: ForgeCommand is single root of trust → Authority model
- Law 2: SMITH governs all execution → Pipeline × Authority composition
- Law 3: Evidence proves what happened → Pipeline × Evidence Chain composition
- Law 4: DataForge is single writer → Evidence Chain × MRPA composition
- Law 5: Humans override everything → Authority model ring validation

### 5.3 Invariant Language

Invariants are written in TypeScript predicates, but using a constrained vocabulary that maps to the TSA (Typed Specification Algebra) from the T8 plan.

```typescript
// Gate pattern
invariant("locked_requires_approval", (state) =>
  isLocked(state.pipeline) ? hasApproval(state.context) : true
);

// Boundary pattern  
invariant("no_escalation_without_grant", (state) =>
  state.actor.ring > state.action.requiredRing ? hasGrant(state) : true
);

// Temporal pattern (via path checking)
pathInvariant("evidence_before_release", (path) =>
  path.includes("RELEASED") ? 
    path.indexOf("EVIDENCE_REVIEW") < path.indexOf("RELEASED") : true
);

// Invariant pattern
invariant("terminal_is_absorbing", (state) =>
  isTerminal(state) ? outgoingTransitions(state).length === 0 : true
);

// Liveness pattern (bounded)
boundedLiveness("eventually_terminal", (path, bound) =>
  path.length <= bound ? reachesTerminal(path) : true
, 20);

// Atomicity pattern
invariant("mrpa_all_or_nothing", (state) =>
  state.phase === "COMMITTED" ? allFilesApplied(state) :
  state.phase === "ROLLED_BACK" ? allFilesRestored(state) : true
);
```

This is readable English wrapped in TypeScript syntax. You can verify what each invariant means without understanding programming.

### 5.4 Evidence Emitter

Every model check run produces a VERITAS evidence record.

```json
{
  "$schema": "veritas-evidence-v1",
  "module": "governance.pipeline_state_machine",
  "model": "pipeline_fsm_v1",
  "commit": "abc123",
  "timestamp": "2026-03-15T10:00:00Z",
  "result": "pass",
  "stats": {
    "states_explored": 847,
    "transitions_taken": 2341,
    "invariants_checked": 5,
    "invariant_checks_total": 4235,
    "paths_explored": 312,
    "max_path_length": 9,
    "duration_ms": 340
  },
  "invariants": [
    { "name": "locked_requires_approval", "status": "pass", "checks": 847 },
    { "name": "terminal_is_absorbing", "status": "pass", "checks": 847 },
    { "name": "failed_always_reachable", "status": "pass", "checks": 612 },
    { "name": "released_through_evidence_review", "status": "pass", "checks": 312 },
    { "name": "deadlock_free", "status": "pass", "checks": 612 }
  ],
  "violations": [],
  "evidence_hash": "sha256:...",
  "prev_hash": "sha256:...",
  "assurance_level": "AL-3"
}
```

On failure:
```json
{
  "violations": [
    {
      "invariant": "locked_requires_approval",
      "path": ["IDLE", "PLANNING", "PLAN_REVIEW", "APPROVED"],
      "state_at_violation": {
        "pipeline": "APPROVED",
        "context": { "approval": null, "actor": "ForgeAgent" }
      },
      "explanation": "Reached APPROVED from PLAN_REVIEW without human approval"
    }
  ]
}
```

That violation report is readable. You know exactly what went wrong, what path produced it, and what state the system was in when the invariant broke.

### 5.5 TSA Integration (from T8)

The Typed Specification Algebra pipeline feeds invariants into StateForge:

```
SYSTEM.md requirement
    │
    ▼ (LLM vocabulary mapper)
Typed terms + pattern
    │
    ▼ (Human confirmation gate)
Confirmed FSL property
    │
    ▼ (Rule-based translation)
StateForge invariant predicate
    │
    ▼ (Model checker)
Exhaustive verification result
    │
    ▼ (Evidence emitter)
Hash-chained proof record
```

Instead of translating to TLA+ / Verus / proptest (three targets), the TSA translates to one target: StateForge predicates. Simpler pipeline, same traceability.

### 5.6 Assurance Levels (Revised)

The original VERITAS had AL-0 through AL-6 tied to tool tiers. The Forge Proof Engine redefines ALs around verification depth:

| Level | Name | What It Means |
|-------|------|--------------|
| AL-0 | Compiled | Builds and passes written tests (existing state) |
| AL-1 | Model-Defined | State machine model exists and is syntactically valid |
| AL-2 | Invariant-Verified | All invariants hold for all reachable states in isolation |
| AL-3 | Composition-Verified | Cross-model invariants hold (Integration Law composition) |
| AL-4 | Spec-Traced | Every SYSTEM.md governance requirement has a verified invariant (TSA integration) |
| AL-5 | Complete | Behavior surface diffed, all governance behaviors specified and verified (T10 integration) |

AL-5 is the ceiling for the Node model checker. If you ever need implementation-level proof (memory, concurrency, crypto bytes), that's AL-6+ from the original VERITAS, added per-function with Rust tooling.

---

## 6. Dependency Ordering

```
Evidence Schema (§10.1)
    └── StateForge Core (5.1)
        ├── Pipeline Model (5.2 Model 1)
        ├── Authority Model (5.2 Model 2)
        ├── Circuit Breaker Model (5.2 Model 3)
        ├── Evidence Chain Model (5.2 Model 4)
        ├── BugCheck Model (5.2 Model 5)
        ├── MRPA Model (5.2 Model 6)
        ├── Nonce Model (5.2 Model 7)
        └── Integration Law Composition (5.2 Model 8)
            └── TSA Integration (5.5)
                └── Spec Traceability + Completeness (5.6 AL-4/AL-5)
```

Models are independent of each other until composition (Model 8). You can build and verify any model in any order. Composition comes last because it requires all component models to exist.

---

## 7. Implementation Phases

| Phase | Build | Scope | Sessions |
|-------|-------|-------|----------|
| 1. StateForge Core | A | Model checker engine: state definition, BFS exploration, invariant checking, guard validation, counterexample extraction, evidence emission | 2–3 |
| 2. Pipeline Model | A | Model 1: pipeline states, transitions, guards, 5 invariants. First proof-of-concept. | 1–2 |
| 3. Authority Model | A | Model 2: authority rings, actor types, escalation rules. | 1 |
| 4. Circuit Breaker Model | A | Model 3: CB states, counters, fail-closed invariant. | 1 |
| 5. Evidence Chain Model | B | Model 4: append-only chain, fork prevention, sealing. | 1 |
| 6. BugCheck Model | B | Model 5: finding lifecycle, severity gates, dismissal rules. | 1 |
| 7. MRPA Model | B | Model 6: patch workflow, atomic rollback, all-or-nothing. | 1 |
| 8. Nonce Model | B | Model 7: replay prevention, expiry, uniqueness. | 1 |
| 9. Integration Law Composition | B | Model 8: compose Models 1–7 for Five Integration Laws. Cross-model invariants. | 2–3 |
| 10. TSA Vocabulary + Patterns | C | Define typed vocabulary and six governance patterns for Forge (from T8 plan). | 1–2 |
| 11. TSA Extraction Pipeline | C | LLM mapper + human gate + rule-based translation to StateForge predicates. | 2–3 |
| 12. Traceability Matrix | C | SYSTEM.md requirement → invariant → verification result. Gap detection. | 1–2 |
| 13. Behavior Surface + Completeness | C | Extract governance behavior surface, diff against spec surface, triage gaps (from T10 plan). | 2–3 |
| 14. CI Integration | C | Run StateForge on commit. Evidence chain updated. AL scores in BuildGuard output. | 1 |

**Total: 16–24 sessions.**

At 3–4 sessions per week: **4–8 weeks.**

---

## 8. Session Detail

### Phase A: Core + First Models (Sessions 1–6)

**Session 1: StateForge Engine — State Definition + Exploration**

Tell Opus: "Build a TypeScript library called StateForge. It takes a model definition object with states (string enum), transitions (from/to/guard/effect tuples), and an initial state. It performs breadth-first exploration from the initial state, tracking visited states and building a reachability graph. Output: the full reachable state set and all valid paths up to a configurable depth bound."

What Opus produces: `stateforge/src/explorer.ts` — the BFS engine with visited-set deduplication and path recording.

What you verify: The engine explores a trivial 3-state model correctly. Count of states and transitions matches what you expect.

**Session 2: StateForge Engine — Invariant Checking + Evidence**

Tell Opus: "Add invariant checking to StateForge. Invariants are named predicate functions. After exploration, run every invariant against every reachable state. If any invariant fails, record the state and the path that reached it. Produce evidence output in the VERITAS evidence schema (provide the JSON schema). Hash-chain each evidence record."

What Opus produces: `stateforge/src/checker.ts` + `stateforge/src/evidence.ts`

What you verify: Add a deliberately broken invariant to the trivial model. The checker catches it and produces a readable counterexample path.

**Session 3: Pipeline State Machine Model**

Tell Opus: "Using StateForge, model the SMITH pipeline state machine. Here are the states: [list them from SYSTEM.md]. Here are the transitions: [list them]. Here are the guards: PLAN_REVIEW and EVIDENCE_REVIEW are locked states requiring human approval. Here are the invariants: [list the five from §5.2 Model 1]. Run the model checker and show me results."

What Opus produces: `stateforge/models/pipeline.ts`

What you verify: Read the results. The checker either says "all 5 invariants hold for N states" or it found a violation. If it found a violation, that's a real governance bug in your state machine design. If all pass, you have mathematical proof that your pipeline can't be subverted.

**This is the proof-of-concept moment.** Session 3 output either validates the entire approach or reveals that the model is wrong (which means either your state machine has a bug or the model doesn't match the implementation — both are findings worth having).

**Session 4: Authority Ring Model**

Tell Opus: "Model the authority ring system. Three rings: [describe]. Four actor types: [describe]. Invariants: [list from §5.2 Model 2]."

What Opus produces: `stateforge/models/authority.ts`

**Session 5: Circuit Breaker Model**

Tell Opus: "Model the circuit breaker. States: CLOSED, OPEN, HALF_OPEN. Include failure counter and cooldown timer as model variables. Invariants: [list from §5.2 Model 3]."

What Opus produces: `stateforge/models/circuit_breaker.ts`

Note: This model has state variables (counters), not just enum states. The state space is larger but still finite (bound the counter to max realistic value, e.g., 10). StateForge handles this because states are objects, not just strings.

**Session 6: Review + Fix**

Inevitably, Sessions 3–5 will surface issues: a model that doesn't match your actual implementation, an invariant that's too strict or too loose, a state space that's larger than expected. This session is for fixes and refinement.

### Phase B: Remaining Models + Composition (Sessions 7–12)

**Sessions 7–10: Evidence Chain, BugCheck, MRPA, Nonce Models**

One model per session. Same pattern: you describe the state machine and invariants from SYSTEM.md, Opus builds the model, StateForge verifies it, you read the results.

These four models are simpler than Pipeline and Authority because they have fewer interacting concerns. The Evidence Chain model is the most interesting — it needs to model append operations and verify the no-fork invariant.

**Sessions 11–12: Integration Law Composition**

Tell Opus: "Compose the Pipeline and Authority models. The composed state is the cross-product: (pipeline_state, authority_state). Add cross-model invariants for Integration Law 2: SMITH governs all execution — meaning no pipeline transition past APPROVED without SMITH authority token. Run the checker on the composed model."

This is where state spaces grow. Pipeline (9 states) × Authority (12 actor-ring combinations) = 108 composed states. Still tiny — the checker runs in milliseconds. But the invariants now span two models, which is where real emergent governance bugs live.

Repeat for each Integration Law, composing the relevant models.

### Phase C: TSA + Traceability + CI (Sessions 13–20)

**Sessions 13–14: TSA Vocabulary and Pattern Library**

Define the six governance patterns and typed vocabulary from the T8 plan, but targeting StateForge predicates instead of TLA+/Verus/proptest.

The vocabulary is the same. The patterns are the same. The translation target is different:

| Pattern | Original Target | New Target |
|---------|----------------|------------|
| Gate | TLA+ `\A s...`, Verus `requires`, proptest | StateForge `invariant()` |
| Boundary | CodeQL query, Verus `ensures` | StateForge `invariant()` |
| Temporal | TLA+ `AG(A => ...)` | StateForge `pathInvariant()` |
| Invariant | TLA+ `TypeInvariant`, Verus `invariant` | StateForge `invariant()` |
| Liveness | TLA+ `AG(... => AF(...))` | StateForge `boundedLiveness()` |
| Atomicity | TLA+ `\A op...`, Verus `ensures` | StateForge `invariant()` |

One target language instead of three. Simpler pipeline. Same formal strength for governance properties.

**Sessions 15–16: TSA Extraction Pipeline**

Build the LLM vocabulary mapper and human confirmation gate. Process SYSTEM.md governance requirements through the pipeline. Output: StateForge invariant predicates for every extractable requirement.

**Sessions 17–18: Traceability + Completeness**

Build the traceability matrix: SYSTEM.md section → TSA property → StateForge invariant → verification result. Run gap detection: requirements with no invariant, invariants with no requirement.

Build the governance behavior surface: enumerate all state transitions, authority checks, evidence operations, and circuit breaker actions in the models. Diff against the spec surface from SYSTEM.md. Triage ungoverned behaviors.

**Session 19: CI Integration**

Wire StateForge into the build pipeline. On every commit: run all models, check all invariants, emit evidence, update AL scores. Fail the build if any governance invariant is violated.

**Session 20: Review + Harden**

Final review. Fix edge cases. Ensure evidence chain integrity. Validate that AL scores compute correctly across all models.

---

## 9. Hard Rules

**Hard Rule #1: Models must match implementation — divergence is a finding.**

If the StateForge pipeline model says transition X→Y requires approval, but the Rust code allows X→Y without checking approval, the model is correct and the code has a bug. Models are the specification. Code must conform.

Corollary: When the Rust implementation changes a state machine, the model MUST be updated in the same session. Stale models produce false assurance.

**Hard Rule #2: Evidence is append-only and hash-chained.**

Same as VERITAS Foundation. Every run produces a hash-linked evidence record. No record is modified after creation. The chain is independently verifiable.

**Hard Rule #3: Invariant violations block merge.**

A StateForge invariant violation is a governance defect — equivalent to a BugCheck S0 finding. No exceptions. No dismissals. Fix the code or fix the model, then explain which one was wrong and why.

**Hard Rule #4: Composition before release.**

No service release without running the Integration Law composition models. Individual model verification is necessary but not sufficient. Cross-model invariants catch emergent governance failures that per-model checks miss.

---

## 10. Governance Layer

### 10.1 Evidence Schema

Identical to VERITAS Foundation §10.2, adapted for StateForge output fields. See §5.4 for the full schema.

### 10.2 Assurance Level Computation

```
AL-0: Module builds and passes tests (existing)
AL-1: StateForge model exists and is syntactically valid
AL-2: All model invariants pass for all reachable states
AL-3: Cross-model (composition) invariants pass
AL-4: Every governance requirement in SYSTEM.md has a verified invariant
AL-5: Governance behavior surface is complete (no ungoverned behaviors)
```

System AL = minimum across all governance-critical models (weakest link).

### 10.3 Model-to-Code Traceability

Each StateForge model maps to specific Rust source files:

| Model | Rust Source | Verification |
|-------|-------------|-------------|
| Pipeline FSM | `src-tauri/src/smith/pipeline.rs` | State enum + transition function must match model |
| Authority Rings | `src-tauri/src/smith/authority.rs` | Ring checks must match model guards |
| Circuit Breaker | `src-tauri/src/smith/circuit_breaker.rs` | FSM transitions must match model |
| Evidence Chain | `src-tauri/src/smith/ledger.rs` | Append logic must enforce model invariants |
| BugCheck | `src-tauri/src/smith/bugcheck.rs` | Lifecycle transitions must match model |
| MRPA | `src-tauri/src/smith/mrpa.rs` | Workflow states must match model |
| Nonce | `src-tauri/src/smith/nonce.rs` | Registry logic must enforce model invariants |

When any of these files change, the corresponding model must be re-verified in the same session.

---

## 11. Open Questions

| # | Question | Resolution |
|---|----------|------------|
| OQ-1 | State space size for composed models? | **Resolved: Bounded.** Largest composition (Pipeline × Authority × Evidence) is ~9 × 12 × 4 = 432 states. BFS explores this in milliseconds. |
| OQ-2 | How to handle state variables (counters, timestamps)? | **Resolved: Bounded abstraction.** Model counters with realistic bounds (e.g., failure_count 0–10). Timestamps modeled as ordinals (t1 < t2), not real values. |
| OQ-3 | TSA vocabulary mapper — Claude API or local? | **Open.** Claude API for accuracy, local embedding for speed. Decide in Session 13 based on requirement volume. |
| OQ-4 | Model drift from code — how to detect? | **Partially resolved.** Hard Rule #1 + model-to-code mapping. Future: AST extraction to auto-detect state enum changes and flag model staleness. |
| OQ-5 | Should StateForge be a standalone npm package? | **Resolved: Yes.** Usable across all Forge repos, not just SMITH. Published to internal registry. |

---

## 12. Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Model doesn't match Rust implementation | False assurance | Hard Rule #1 + model-to-code traceability. Future: AST-based model extraction. |
| State space too large for composed models | Exploration timeout | Bounded abstraction (counters capped, timestamps as ordinals). Largest expected: <10,000 states. |
| Invariants too strict (valid paths rejected) | Model refinement churn | Start with core invariants only. Add edge-case invariants incrementally. |
| Invariants too loose (bugs not caught) | False assurance | Composition catches cross-model issues. TSA extraction ensures coverage. |
| Node checker not fast enough | CI slowdown | Sub-second for individual models. <10 seconds for full composition suite. Not a realistic risk. |
| TSA extraction accuracy below 80% | Incomplete spec coverage | Human confirmation gate. Manual invariant writing for requirements that don't fit patterns. |

---

## 13. What This Replaces and What It Keeps

### From VERITAS Foundation–T7

| Component | Status |
|-----------|--------|
| Evidence schema (hash-chained, append-only) | **Kept** — same schema, StateForge output |
| Assurance levels (weakest-link) | **Kept** — redefined for governance tiers |
| Criticality classification | **Kept** — drives which models need composition |
| Hard rules (supplement BuildGuard, etc.) | **Kept** — adapted for StateForge |
| T0 proptest | **Replaced** — StateForge exhaustive > random sampling for governance |
| T1 cargo-mutants | **Deferred** — useful for implementation, not governance model |
| T2 cargo-fuzz | **Deferred** — useful for crash discovery, not governance |
| T3 CodeQL/Semgrep | **Deferred** — useful for taint, not governance |
| T4 loom | **Deferred** — useful for concurrency, not governance |
| T5 TLA+ | **Replaced** — StateForge IS TLA+ semantics in TypeScript |
| T6 criterion | **Deferred** — useful for performance, not governance |
| T7 Verus | **Deferred** — useful for crypto proofs, not governance |

### From VERITAS T8–T10

| Component | Status |
|-----------|--------|
| T8 Typed Specification Algebra | **Kept** — feeds StateForge instead of TLA+/Verus |
| T8 Human confirmation gate | **Kept** — unchanged |
| T8 Traceability matrix | **Kept** — unchanged |
| T9 Protocol grammars | **Partially kept** — Integration Law composition covers this |
| T9 Interaction recording | **Deferred** — runtime traces, future enhancement |
| T9 Dependency fingerprinting | **Deferred** — implementation concern, not governance |
| T10 Behavior surface extraction | **Kept** — governance behavior surface from models |
| T10 Spec surface extraction | **Kept** — from TSA pipeline |
| T10 Surface diff + triage | **Kept** — unchanged |
| T10 Mutation-driven completeness | **Deferred** — requires Rust mutation tooling |

---

## 14. Architect Assessment

**Status:** Immediately implementable. No research dependency. No Rust toolchain dependency. No tool installation beyond Node/TypeScript.

| Dimension | Rating |
|-----------|--------|
| Theoretical strength | Strong — exhaustive exploration is mathematically complete for finite state machines |
| Practical feasibility | Very high — 16–24 sessions, TypeScript only, Node runtime |
| Non-coder accessibility | Excellent — models are readable state/transition/invariant definitions |
| Governance coverage | Complete for state machine concerns — which is 90%+ of Forge risk |
| Implementation coverage | Partial — does not verify Rust code correctness at byte level |
| Tool overhead | Near zero — single npm package, sub-second execution |
| Evidence integrity | Strong — same hash-chained, append-only model as original VERITAS |
| Future extensibility | Full — Rust-tier tools (proptest, loom, Verus) can be added per-function later |

**Why this works:**
- Forge's critical risk is governance, not memory safety
- Governance is finite state machines
- Finite state machines are exhaustively verifiable
- TypeScript model checker is buildable in days, not months
- TSA integration gives formal requirement-to-proof traceability
- Evidence chain gives auditable verification history
- Non-coder architect can read models and results directly
- Opus 4.6 in VS Code can build and iterate on this with minimal friction

---

## 15. Next Steps

Phase A is next. Everything else waits.

- [ ] Session 1: StateForge BFS engine + path recording
- [ ] Session 2: Invariant checker + evidence emitter
- [ ] Session 3: Pipeline state machine model — **the proof-of-concept**
- [ ] If Session 3 produces clean results → continue to Sessions 4–6
- [ ] If Session 3 finds a governance violation → fix the violation, then continue

**Gate:** After Session 3, you know whether this works. Everything after that is expanding coverage.
