# VERITAS Foundation–T7 — Metadata Plan

**Date:** 2026-02-26
**Version:** v1
**Author:** BDS Architecture
**Status:** Metadata (pre-spec planning)
**Target:** Forge:SMITH (forge-smithy), extensible to all Forge Ecosystem repos
**Context:** Unified code verification pipeline using existing, production-ready tools
**Companion:** THE_PROOF_ENGINE_VERITAS.md (architectural vision), VERITAS T8–T10 Implementation Plan (upper tiers)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-02-26 | Initial metadata plan. Foundation–T7 scoped to production-ready tools only. Session-level detail. Hard rules. Formal contracts for evidence schema and criticality classification. |

---

## 1. Problem Statement

SMITH has strong testing infrastructure: 2,100+ tests, security guards, governance policy checks, and the BuildGuard preflight pipeline. But this coverage has two gaps:

**Gap 1 — No verification above example tests.** Every test is an example: "given this specific input, expect this specific output." No test checks universal properties ("for ALL inputs, this invariant holds"). No test checks whether the test suite itself is effective (mutation testing). No test verifies data flow boundaries formally. The test suite answers "does it work for cases I thought of?" but not "does it work for cases I didn't think of?"

**Gap 2 — No unified assurance score.** Test results, lint findings, coverage reports, and security guard outputs are independent artifacts. Nothing aggregates them into a single, auditable confidence level per module. Nothing traces from "this module handles crypto" to "therefore it needs formal verification." Nothing records the verification state in the evidence chain.

VERITAS Foundation–T7 closes both gaps using tools that exist and work today.

---

## 2. Classification

**Blast Radius:** Class C — Multi-subsystem (affects testing, CI, evidence chain, BuildGuard)
**Frozen core:** RunIntent.v1, MRPA, ECD untouched. VERITAS wraps around BuildGuard, doesn't replace it.

---

## 3. Naming

| Surface | Name |
|---------|------|
| Feature umbrella | VERITAS (Verification Engine for Runtime Intention, Trust, Assurance & Specification) |
| Evidence output | Assurance Level (AL-0 through AL-7) |
| Configuration | `veritas.toml` (criticality overrides, tier targets, tool config) |
| CLI surface | Extensions to existing BuildGuard preflight, not a new binary |

---

## 4. Capability Decomposition

### 4.1 Foundation (Already Exists)

What SMITH has today: compilation (`cargo check`, `tsc`), linting (`clippy`, `eslint`), type checking (`svelte-check`), example tests (`cargo test`, `vitest`), security guards, governance policy checks, BuildGuard preflight.

**VERITAS contribution:** Normalize existing outputs into the unified evidence schema (§10.2). This is the baseline — every module starts at AL-0.

### 4.2 T0 — Property Verification

Universal invariants tested against thousands of random inputs using property-based testing.

**What it does:**
- Adds `proptest` to critical Rust modules
- Adds `fast-check` to critical frontend stores
- Checks properties like "hash chain never forks after any sequence of appends" and "serialization roundtrip always preserves the original value"
- Generates 10,000–1,000,000 random inputs per property

**Tools:**
- Rust: `proptest` (primary), `quickcheck`, `bolero`
- TypeScript: `fast-check`
- Python: `hypothesis`

**What it proves:** Universal properties hold for a statistically significant sample. Not mathematical proof, but vastly stronger than example tests.

**Evidence produced:** Per-property pass/fail, shrunk minimal counterexamples on failure, input distribution statistics.

### 4.3 T1 — Mutation Verification

Systematic introduction of small code changes to test whether the test suite catches them.

**What it does:**
- Runs `cargo-mutants` on critical Rust modules
- Runs `stryker-mutator` on critical frontend code (if warranted)
- Reports mutation kill rate per module
- Catalogs surviving mutants — each represents a class of bug the tests would miss

**Tools:**
- Rust: `cargo-mutants`
- TypeScript: `stryker-mutator`
- Python: `mutmut`

**Key metric:** Mutation kill rate. Target: >90% for critical code, >80% for standard code.

**Evidence produced:** Kill rate per module, surviving mutant catalog with classification, test effectiveness score.

**Feedback loop:** Surviving mutants in critical modules automatically generate property test suggestions for T0.

### 4.4 T2 — Attack Resistance

Adversarial input testing (fuzzing) and runtime failure injection (chaos testing).

**What it does:**
- Fuzzes every IPC boundary (serialization/deserialization)
- Fuzzes every parser (JSON, TOML, user input)
- Fuzzes cryptographic operation inputs (signature verification, hash computation)
- Injects runtime failures: network drops, disk full, service timeouts (chaos testing for circuit breakers)

**Tools:**
- Rust: `cargo-fuzz` (libFuzzer), `afl.rs`, `bolero`
- TypeScript: `jsfuzz` (if applicable)
- Chaos: Custom circuit breaker fault injection via existing test harness

**Key targets for SMITH:**
- MRPA patch file parsing
- Hash chain entry serialization
- RunIntent deserialization at IPC boundary
- State machine transition function under malformed input
- Service client behavior under simulated network partition

**Evidence produced:** Crash catalog with reproduction inputs, coverage maps, corpus statistics, chaos test resilience scores.

**Feedback loop:** Crash-inducing inputs analyzed for security implications and routed to T3 if they involve data that could leak.

### 4.5 T3 — Information Flow Verification

Taint analysis proving sensitive data never reaches forbidden sinks and untrusted input never reaches trusted operations without validation.

**What it does:**
- Traces API keys from ForgeCommand vault → verifies they never reach IPC boundary → never serialized to frontend
- Traces user-provided file paths → verifies validated for traversal → never reach filesystem operations without sanitization
- Traces LLM output → verifies classified by PromptSpec → never rendered in UI without classification gate
- Traces hash chain values → verifies never modified after computation

**Tools:**
- Cross-language: CodeQL (GitHub), Semgrep (taint mode)
- Rust: `cargo-geiger` (unsafe tracking), MIRAI (abstract interpretation)
- Custom: SMITH security guard scripts (already exist — pattern-based approximation of taint analysis)

**Hard Rule #1 applies:** CodeQL/Semgrep results supplement but do not replace the existing security guards. Both run. Security guards are the gate; CodeQL/Semgrep are the audit.

**Evidence produced:** Taint flow graphs, violation catalog, authorized flow whitelist, false positive suppressions with justification.

### 4.6 T4 — Concurrency Verification

Exhaustive or near-exhaustive exploration of thread interleavings.

**What it does:**
- Adds `loom` tests for concurrent state management in Rust
- Adds `shuttle` tests for randomized schedule exploration
- Verifies: pipeline state machine never has two concurrent transitions from same state
- Verifies: hash chain append is serialized (no two entries share the same prev_hash)
- Verifies: circuit breaker state transitions are atomic
- Verifies: MRPA single-writer lock is never held by dead process beyond heartbeat timeout

**Tools:**
- Rust: `loom` (exhaustive), `shuttle` (randomized), ThreadSanitizer
- Runtime: Tokio console (async task analysis)

**Scope constraint:** `loom` is exhaustive but has state space limits. Apply only to modules with shared mutable state. For SMITH, this is approximately 8–12 modules.

**Evidence produced:** Explored state count, schedule coverage, deadlock detection results, race condition catalog.

### 4.7 T5 — Model Checking

Exhaustive exploration of state machine behavior across ALL reachable states using TLA+.

**What it does:**
- Models the pipeline state machine (10 states, locked states, human approval gates)
- Models the circuit breaker FSM (Closed → Open → HalfOpen → Closed)
- Models the BugCheck finding lifecycle (NEW → TRIAGED → ... → CLOSED)
- Models the MRPA patch application workflow (Backup → Stage → Apply → Verify / Rollback)
- Verifies temporal properties in CTL/LTL

**Tools:**
- TLA+ / PlusCal (primary — industry standard, used by AWS, Azure, MongoDB)
- Alloy (lightweight relational modeling, optional complement)
- Kani (bounded model checking for Rust — bridges model to code)

**Key properties to verify:**

| State Machine | Property | Logic |
|--------------|----------|-------|
| Pipeline | No path from PLAN_REVIEW to APPROVED without HumanApproval | `AG(locked → A[¬advance U approval])` |
| Pipeline | FAILED is always reachable from any non-terminal state | `AG(¬terminal → EF(FAILED))` |
| Pipeline | Released is only reachable through EVIDENCE_REVIEW | `AG(Released → was_in(EVIDENCE_REVIEW))` |
| Circuit Breaker | Open is always reachable given sufficient failures | `AG(Closed ∧ failures ≥ threshold → EF(Open))` |
| Circuit Breaker | After Open, no requests pass until HalfOpen probe succeeds | `AG(Open → A[¬pass U HalfOpen])` |
| BugCheck | No transition from a terminal state | `AG(terminal → AG(terminal))` |
| MRPA | Partial application is never committed | `AG(¬(applied(some) ∧ committed))` |
| MRPA | If Verify fails, all files restored | `AG(verify_fail → AF(all_restored))` |

**Evidence produced:** State space size, property verification results, counterexample traces for violations, model-to-code traceability mapping.

### 4.8 T6 — Temporal & Performance Verification

Ordering invariants and resource bounds.

**What it does:**
- Verifies startup ordering: key initialization before any other operation
- Verifies evidence signing completes before DataForge persistence
- Verifies circuit breaker cooldown elapses before HalfOpen probe
- Benchmarks critical paths with statistical regression detection
- Empirical complexity analysis (run with increasing N, fit curve)

**Tools:**
- Rust benchmarks: `criterion` (primary), `divan`
- Regression detection: Statistical comparison against baseline benchmarks (`codspeed`)
- Temporal: Runtime verification monitors (custom — assertion-based ordering checks in test harness)

**Key performance properties:**

| Component | Bound | Type |
|-----------|-------|------|
| Hash chain verification | O(n) with chain length | Complexity |
| Pipeline state transition | < 10ms | Latency |
| Evidence bundle serialization | < 100ms for bundles under 1MB | Latency |
| Fuzzy search | < 200ms for indices under 100K documents | Latency |
| Memory per pipeline run | < 50MB | Resource |

**Evidence produced:** Temporal trace logs, performance benchmarks with statistical analysis, regression reports, complexity curve fits.

### 4.9 T7 — Formal Code Verification

Mathematical proof of code correctness for critical Rust functions.

**What it does:**
- Integrates Verus for SMITH Authority (Ed25519 signing, nonce uniqueness, key zeroing)
- Integrates Verus for hash chain (append integrity, chain never forks)
- Integrates Verus for MRPA (atomic rollback guarantee)
- Explores AutoVerus for AI-assisted proof generation (91.3% success rate on benchmarks)

**Tools:**
- Verus (primary — Rust-syntax formal verification, SMT-backed)
- AutoVerus (LLM-powered proof annotation generation)
- Kani (bounded model checking — bridges T5 models to T7 code proofs)

**Key verification targets:**

| Component | Specification | Priority |
|-----------|--------------|----------|
| Ed25519 signing | Signature over all RunIntent fields matches standard | Critical |
| Hash chain append | `hash(entry) == SHA-256(data \|\| prev_hash)` and chain never forks | Critical |
| Nonce replay prevention | No nonce accepted twice within a session | Critical |
| Pipeline state transitions | Only valid transitions per state machine contract | Critical |
| MRPA atomic rollback | If verify fails, all files restored to pre-apply state | Critical |
| Key material zeroing | Key bytes zeroed on drop, never observable after | Critical |
| Circuit breaker FSM | Transitions match specified FSM exactly | High |
| Evidence bundle integrity | Bundle hash covers all included gate results | High |
| Path sanitization | No path traversal escapes allowed directory | High |

**Scope constraint:** Verus supports a subset of Rust. Target approximately 20–30 critical functions, not all 352 Rust files. Proof-to-code ratio averages 2–4x (2–4 lines of annotation per line of code). This is realistic for the immutable core, not for the entire codebase.

**Evidence produced:** Verified function catalog, proof-to-code ratio, specification coverage map, unverified function list with reason.

---

## 5. The Assurance Level System

Each code module receives an Assurance Level based on the highest tier it has fully passed. The system's overall AL is the minimum across all critical-path modules (weakest link).

| Level | Name | Tiers Passed | Meaning |
|-------|------|-------------|---------|
| AL-0 | Compiled | Foundation | Builds and passes written tests |
| AL-1 | Property-Verified | Foundation + T0 + T1 | Universal properties hold; test suite catches mutations |
| AL-2 | Attack-Tested | AL-1 + T2 | Survives adversarial input and chaos |
| AL-3 | Flow-Secure | AL-2 + T3 | Data flows are proven safe |
| AL-4 | Concurrency-Safe | AL-3 + T4 | Thread safety verified |
| AL-5 | Model-Checked | AL-4 + T5 + T6 | State machines proven correct for all reachable states |
| AL-6 | Formally-Proven | AL-5 + T7 | Mathematical proof of code correctness |

---

## 6. Criticality Classification

Not all code needs AL-6. The system determines target AL based on code criticality.

| Signal | Criticality | Target AL |
|--------|------------|-----------|
| Handles cryptographic material (Zeroizing<T>, signing, hashing) | Critical | AL-6 |
| Controls state machine transitions | Critical | AL-5 |
| Processes untrusted input (IPC deserialization, file paths, user data) | High | AL-3 |
| Manages concurrent shared state (Arc<Mutex<T>>, channels) | High | AL-4 |
| Crosses trust boundary (IPC, network, filesystem) | High | AL-3 |
| Performs irreversible operations (delete, publish, sign) | Critical | AL-5 |
| Business logic (non-critical path) | Standard | AL-1 |
| UI presentation logic | Low | AL-0 |
| Test utilities | Low | AL-0 |

**Classification methods:**
- **Automatic:** Static analysis detects type usage (e.g., function touches `Zeroizing<String>` → Critical)
- **Annotated:** Developer marks functions with `#[veritas_criticality(high)]`
- **Policy-driven:** `veritas.toml` defines module-level criticality overrides

### Target ALs for SMITH Components

| Component | Current AL | Target AL | Gap |
|-----------|-----------|-----------|-----|
| SMITH Authority (signing, keys, nonces) | AL-0 | AL-6 | T0–T7 all needed |
| Pipeline state machine | AL-0 | AL-5 | T0–T6 needed |
| MRPA (patch apply/rollback) | AL-0 | AL-6 | T0–T7 all needed |
| Hash chain / ledger | AL-0 | AL-6 | T0–T7 all needed |
| BuildGuard gate execution | AL-0 | AL-4 | T0–T4 needed |
| IPC boundary (secrets) | AL-0 (partial T3 via guards) | AL-3 | T0–T3 needed |
| Security guard scripts | AL-0 (partial T3) | AL-3 | T0–T3 needed |
| Governance event chain | AL-0 | AL-5 | T0–T6 needed |
| UI components | AL-0 | AL-1 | T0–T1 needed |
| SMITH Assist (AI chat) | AL-0 | AL-1 | T0–T1 needed |

---

## 7. Dependency Ordering

```
4.1 Foundation (exists)
    ├── 4.2 T0 Property Testing       ← Needs Foundation passing
    │   └── 4.3 T1 Mutation Testing   ← Needs T0 properties to generate from surviving mutants
    │       └── 4.4 T2 Fuzzing + Chaos  ← Needs T0/T1 to identify targets
    │           └── 4.5 T3 Information Flow  ← Needs T2 crash analysis for security routing
    │               └── 4.6 T4 Concurrency  ← Needs T3 to identify shared-state modules
    │                   └── 4.7 T5 Model Checking  ← Needs T4 to identify concurrency-relevant state machines
    │                       └── 4.8 T6 Temporal + Perf  ← Needs T5 for ordering property targets
    │                           └── 4.9 T7 Formal Verification  ← Needs T5 model properties as Verus targets
    └── Evidence Schema (§10.2)  ← Required before any tier produces evidence
```

**Important:** While the dependency chain is linear in theory (each tier feeds the next), implementation can overlap. T0 and T1 can start immediately. T2 can start as soon as T0 identifies critical modules. T5 (TLA+) can start independently — it doesn't require T0–T4 outputs, only the state machine documentation.

---

## 8. Implementation Phases

| Phase | Build | Scope | Sessions |
|-------|-------|-------|----------|
| 0. Evidence Schema | A | Unified evidence schema (§10.2). `veritas.toml` config format. Criticality classification rules. AL computation logic. | 2–3 |
| 1. T0 Property Testing (Rust) | A | `proptest` for SMITH Authority, hash chain, pipeline transitions, MRPA, serialization roundtrips. 5–8 critical modules. | 2–3 |
| 2. T0 Property Testing (Frontend) | A | `fast-check` for critical Svelte stores: pipeline state store, governance event store. | 1–2 |
| 3. T1 Mutation Testing | A | `cargo-mutants` on SMITH Authority + BuildGuard. Kill rate analysis. Surviving mutant triage. | 2–3 |
| 4. Evidence Integration v1 | A | Wire T0 + T1 results into evidence schema. AL-1 computation for covered modules. BuildGuard integration. | 1–2 |
| 5. T2 Fuzzing | B | `cargo-fuzz` targets for IPC serialization, MRPA patch parsing, hash chain operations, RunIntent deserialization. | 3–4 |
| 6. T2 Chaos Testing | B | Circuit breaker fault injection. Service client timeout testing. Disk-full simulation for evidence persistence. | 2–3 |
| 7. T3 Information Flow | B | CodeQL setup for Rust taint analysis. Semgrep rules for secret-to-IPC flow. Validate against existing security guards. | 3–4 |
| 8. Evidence Integration v2 | B | Wire T2 + T3 results into evidence schema. AL-2 and AL-3 computation. | 1–2 |
| 9. T4 Concurrency (loom) | C | `loom` tests for pipeline state machine, hash chain append, circuit breaker transitions, MRPA lock. 8–12 modules. | 3–4 |
| 10. T5 Model Checking (TLA+) | C | TLA+ models for pipeline FSM, circuit breaker FSM, BugCheck lifecycle, MRPA workflow. 4 models, 8+ properties. | 4–5 |
| 11. T6 Temporal + Performance | C | `criterion` benchmarks for critical paths. Startup ordering verification. Regression detection baselines. | 2–3 |
| 12. Evidence Integration v3 | C | Wire T4 + T5 + T6 into evidence. AL-4 and AL-5 computation. Model-to-code traceability. | 2–3 |
| 13. T7 Verus Setup | D | Verus toolchain integration. Verify one function end-to-end (hash chain append). Prove the workflow works. | 2–3 |
| 14. T7 SMITH Authority | D | Verus specs + proofs for Ed25519 signing, nonce replay prevention, key zeroing. AutoVerus exploration. | 4–5 |
| 15. T7 Hash Chain + MRPA | D | Verus specs + proofs for hash chain integrity, MRPA atomic rollback. | 3–4 |
| 16. Evidence Integration v4 (Final) | D | Wire T7 into evidence. AL-6 computation. Full VERITAS evidence bundle. CI gate integration. | 2–3 |

**Total:** ~38–51 sessions across 17 phases.

---

## 9. Open Questions

| # | Question | Resolution |
|---|----------|------------|
| OQ-1 | Evidence storage: DataForge or local? | **Resolved: Both.** Local JSON for speed, DataForge persistence for audit trail. Evidence chain is hash-linked — integrity verifiable from either store. |
| OQ-2 | `cargo-mutants` runtime: too slow for CI? | **Resolved: Nightly profile.** Mutation testing runs in `nightly` profile, not `preflight` or `pr`. Kill rate tracked over time, not gated per-commit. |
| OQ-3 | TLA+ model-to-code gap: how to ensure models match code? | **Resolved: Kani bridge.** Kani does bounded model checking on actual Rust code. Use TLA+ for unbounded state exploration, Kani for code-level confirmation. |
| OQ-4 | Verus subset of Rust: does it cover SMITH's patterns? | **Open.** Need to audit SMITH Authority functions for Verus compatibility. Session 13 validates this. |
| OQ-5 | `loom` state space explosion for complex modules? | **Resolved: Scope to shared-state interfaces only.** Don't `loom`-test entire modules — test the synchronization boundary (the Mutex, the channel, the atomic). |
| OQ-6 | CodeQL vs Semgrep vs existing security guards: overlap? | **Resolved: Layered.** Guards are the gate (fast, in preflight). CodeQL/Semgrep are the audit (deeper, in nightly). Different tools catching different things. Guards stay. |
| OQ-7 | How does VERITAS interact with BuildGuard? | **Resolved: Extension, not replacement.** BuildGuard remains the preflight gate. VERITAS adds deeper verification tiers that run in `pr` and `nightly` profiles. AL score integrates into BuildGuard evidence bundle. |
| OQ-8 | AutoVerus maturity: ready for production proofs? | **Open.** 91.3% benchmark success is promising but benchmarks differ from production code. Session 14 validates with real SMITH functions. |
| OQ-9 | Performance impact of `proptest` in CI? | **Resolved: Budget control.** `proptest` configured with case count per profile: 100 for `fast`, 1000 for `pr`, 10000 for `nightly`. Time budget enforced via proptest config. |

---

## 10. Governance Layer

### 10.1 Hard Rules

**Hard Rule #1: VERITAS supplements BuildGuard — never replaces it.**

BuildGuard preflight (7-phase, 2-minute, red/green) remains the primary CI gate. VERITAS tiers run in addition to BuildGuard, in `pr` and `nightly` profiles. If VERITAS is unavailable or a tier fails to execute, BuildGuard still gates. VERITAS findings are additive — they never suppress a BuildGuard failure.

**Hard Rule #2: Evidence schema is append-only and hash-chained.**

Every VERITAS evidence entry is hash-linked to the previous entry. No entry is modified after creation. The chain is verifiable: given any entry, you can reconstruct the chain to the root. This is the same integrity model as the SMITH governance ledger. Evidence schema changes are versioned — old entries remain valid under their original schema.

**Hard Rule #3: AL computation is weakest-link, never averaged.**

A module's AL is the lowest tier it has fully passed, not an average across tiers. If a module passes T0–T5 but fails T3 (taint violation), its AL is AL-2, not "mostly AL-5." This prevents gaming: you can't skip a hard tier by excelling at easy ones.

**Hard Rule #4: Criticality classification determines target AL — human overrides are logged.**

The automatic criticality classifier sets the target AL. If a developer overrides it (e.g., marking a crypto function as "Standard" to avoid AL-6), the override is logged as a governance event with a required justification. Unjustified overrides are S1 findings.

---

### 10.2 Unified Evidence Schema (Phase A Contract #1)

Every tier produces evidence in a single format. This schema is the contract between VERITAS tiers and the evidence chain.

```json
{
  "$schema": "veritas-evidence-v1",
  "module": "src-tauri/src/smith/authority.rs::sign_run_intent",
  "commit": "abc123def456",
  "timestamp": "2026-03-01T10:00:00Z",
  "criticality": "critical",
  "target_al": "AL-6",
  "current_al": "AL-3",
  "tiers": {
    "foundation": {
      "status": "pass",
      "compiles": true,
      "tests_pass": true,
      "test_count": 12,
      "coverage": { "line": 98.2, "branch": 94.1 },
      "lint_findings": 0,
      "duration_ms": 340
    },
    "t0_properties": {
      "status": "pass",
      "properties_checked": 7,
      "all_hold": true,
      "total_inputs_tested": 70000,
      "counterexamples": [],
      "duration_ms": 4200
    },
    "t1_mutations": {
      "status": "pass",
      "mutations_generated": 23,
      "mutations_killed": 22,
      "kill_rate": 0.957,
      "surviving": ["changed_nonce_check_operator"],
      "duration_ms": 18000
    },
    "t2_fuzzing": {
      "status": "pass",
      "iterations": 500000,
      "crashes": 0,
      "hangs": 0,
      "corpus_size": 1247,
      "duration_ms": 120000
    },
    "t2_chaos": {
      "status": "pass",
      "scenarios_run": 5,
      "failures_injected": 15,
      "resilience_violations": 0
    },
    "t3_flow": {
      "status": "pass",
      "flows_analyzed": 12,
      "taint_violations": 0,
      "key_material_contained": true,
      "no_secret_reaches_ipc": true,
      "false_positives_suppressed": 1,
      "suppression_justification": "Ed25519 public key is not secret"
    },
    "t4_concurrency": {
      "status": "pass",
      "states_explored": 4821,
      "deadlocks_found": 0,
      "races_found": 0,
      "tool": "loom",
      "duration_ms": 8500
    },
    "t5_model": {
      "status": "pass",
      "model_file": "pipeline_fsm.tla",
      "states_explored": 1247,
      "properties_verified": 4,
      "counterexamples": 0,
      "model_to_code_mapping": "verified via kani"
    },
    "t6_temporal": {
      "status": "pass",
      "ordering_checks": 3,
      "ordering_violations": 0,
      "benchmarks": {
        "sign_run_intent": { "p50_ms": 0.8, "p99_ms": 2.1, "regression": false }
      }
    },
    "t7_formal": {
      "status": "pass",
      "verifier": "verus",
      "functions_verified": 3,
      "functions_total": 3,
      "specs": ["nonce_uniqueness", "signature_covers_all_fields", "key_zeroed_on_drop"],
      "proof_to_code_ratio": 2.3,
      "auto_verus_assisted": true
    }
  },
  "evidence_hash": "sha256:...",
  "prev_hash": "sha256:...",
  "signed_by": "smith_authority_ed25519"
}
```

**Schema rules:**
- Every tier has a `status` field: `pass`, `fail`, `skipped`, `error`
- `skipped` means the tier was not required for this module's target AL
- `error` means the tier failed to execute (tool crash, timeout) — distinct from `fail` (tier executed, found violations)
- Tier-specific fields vary by tier but always include enough detail to reproduce the finding
- Evidence hash covers the entire JSON object minus `evidence_hash` and `prev_hash`

**Phase 0 deliverable:** This schema, validated by generating mock evidence for SMITH Authority at AL-0 (Foundation only) and confirming the hash chain logic works.

---

### 10.3 veritas.toml Configuration Schema (Phase A Contract #2)

```toml
[global]
evidence_dir = ".veritas/evidence"
hash_algorithm = "sha256"

[profiles.fast]
# Preflight: only Foundation
tiers = ["foundation"]
time_budget_seconds = 120

[profiles.pr]
# PR gate: Foundation + T0 + T1 + T3 (security-relevant)
tiers = ["foundation", "t0", "t1", "t3"]
time_budget_seconds = 600
t0_cases = 1000
t1_enabled = true

[profiles.nightly]
# Full suite: all tiers up to target AL per module
tiers = ["foundation", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7"]
time_budget_seconds = 3600
t0_cases = 10000
t2_fuzz_iterations = 500000
t2_chaos_enabled = true

[criticality_overrides]
# Module-level target AL overrides (requires justification)
"src-tauri/src/smith/ui/" = { target = "AL-0", reason = "UI presentation only" }
"src-tauri/src/smith/assist/" = { target = "AL-1", reason = "Probabilistic by nature" }

[tool_config.proptest]
default_cases = 1000
max_shrink_iters = 1000

[tool_config.cargo_mutants]
timeout_multiplier = 3
exclude_patterns = ["test_", "mock_"]

[tool_config.cargo_fuzz]
max_total_time = 300
max_len = 65536

[tool_config.verus]
auto_verus_enabled = true
auto_verus_timeout_seconds = 60
```

**Phase 0 deliverable:** This schema, with defaults populated for SMITH.

---

### 10.4 Feedback Loop Contracts (Phase A Contract #3)

The feedback loop between tiers is a core VERITAS design principle. Each tier generates evidence that improves other tiers. These feedback mechanisms are specified here so they can be implemented incrementally.

| Source Tier | Finding | Target Tier | Automatic Action |
|-------------|---------|-------------|-----------------|
| T1 (Mutation) | Surviving mutant in critical module | T0 (Property) | Generate property test suggestion: "property that would catch mutation class X" |
| T0 (Property) | Property verified for 10,000+ inputs | T7 (Formal) | Promote to candidate Verus `ensures` clause |
| T2 (Fuzzing) | Crash involving data that could leak | T3 (Flow) | Route crash input to taint analysis for security assessment |
| T3 (Flow) | Taint violation involving crypto material | T7 (Formal) | Escalate to formal proof target: prove boundary mathematically |
| T4 (Concurrency) | Race in governance event chain | T5 (Model) | Escalate to model checking for exhaustive state exploration |
| T5 (Model) | Verified TLA+ property | T7 (Formal) | Translate to Verus specification (close model-code gap) |

**Implementation:** Feedback is implemented as "suggestions" stored in the evidence chain, not as automatic code changes. Each suggestion has a source finding, a target tier, a proposed action, and a status (`pending`, `accepted`, `rejected`, `implemented`). Human reviews suggestions. This keeps the feedback loop productive without creating autonomous code modification.

---

## 11. Tool Availability Matrix

All tools in this plan exist and are production-ready.

| Tool | Language | Maturity | License | Install |
|------|----------|----------|---------|---------|
| `proptest` | Rust | Stable (6+ years) | MIT/Apache-2.0 | `cargo add proptest --dev` |
| `fast-check` | TypeScript | Stable (5+ years) | MIT | `pnpm add -D fast-check` |
| `cargo-mutants` | Rust | Stable (3+ years) | MIT | `cargo install cargo-mutants` |
| `stryker-mutator` | TypeScript | Stable (7+ years) | Apache-2.0 | `pnpm add -D @stryker-mutator/core` |
| `cargo-fuzz` | Rust | Stable (7+ years) | MIT/Apache-2.0 | `cargo install cargo-fuzz` |
| CodeQL | Multi | Production (GitHub) | MIT (CLI) | GitHub Actions or local CLI |
| Semgrep | Multi | Production (5+ years) | LGPL-2.1 | `pip install semgrep` |
| `loom` | Rust | Stable (5+ years) | MIT | `cargo add loom --dev` |
| `shuttle` | Rust | Stable (3+ years) | MIT | `cargo add shuttle --dev` |
| TLA+ Toolbox | Spec | Production (20+ years) | MIT | Standalone install |
| Kani | Rust | Production (AWS) | MIT/Apache-2.0 | `cargo install kani-verifier` |
| `criterion` | Rust | Stable (6+ years) | MIT/Apache-2.0 | `cargo add criterion --dev` |
| Verus | Rust | Research-production (Microsoft) | MIT | Source build |
| AutoVerus | Rust | Research (2024–2025) | MIT | Source build + LLM API |

**All tools are MIT or permissive licensed.** No licensing risk.

---

## 12. Build Order

**Phase A: Schema + Property + Mutation (immediate value, no new infrastructure)**
- Evidence schema (§10.2) — lock format before any tier produces evidence
- `veritas.toml` configuration (§10.3) — lock profiles before any tier reads config
- Feedback loop contracts (§10.4) — lock inter-tier communication before building tiers
- `proptest` for 5–8 critical Rust modules (SMITH Authority, hash chain, pipeline, MRPA, serialization)
- `fast-check` for 2–3 critical frontend stores
- `cargo-mutants` on SMITH Authority + BuildGuard
- Evidence integration v1: AL-0 and AL-1 computation operational

**Phase B: Fuzzing + Flow (security hardening, no new conceptual complexity)**
- `cargo-fuzz` targets for IPC boundaries, MRPA parsing, hash chain, RunIntent
- Chaos testing for circuit breakers and service clients
- CodeQL + Semgrep taint analysis setup and validation against existing security guards
- Evidence integration v2: AL-2 and AL-3 computation operational

**Phase C: Concurrency + Model Checking (state machine verification)**
- `loom` tests for 8–12 concurrent modules
- TLA+ models for 4 state machines with 8+ temporal properties
- `criterion` benchmarks with regression baselines
- Evidence integration v3: AL-4 and AL-5 computation operational

**Phase D: Formal Verification (only after C proves the model-code pipeline works)**
- Verus toolchain integration and single-function proof
- SMITH Authority formal verification (3 critical functions)
- Hash chain + MRPA formal verification (4–5 critical functions)
- Evidence integration v4: AL-6 computation operational, full evidence bundle

**Why this order:** Phase A gives immediate value — property tests and mutation testing catch real bugs with zero infrastructure investment. Phase B adds security depth with well-understood tools. Phase C introduces the conceptual leap (model checking) but with a proven toolchain. Phase D is the frontier — only attempted after the lower tiers prove the evidence pipeline works.

---

## 13. Risks

### Structural Risks

**Risk 1: Evidence Schema Drift**

The evidence schema is the contract between all tiers. If it changes frequently, downstream consumers (BuildGuard integration, CI gates, future T8–T10 pipeline) break. Mitigation: Schema is versioned. Old entries remain valid under their original version. Schema changes require a governance event.

**Risk 2: Tool Version Churn**

VERITAS depends on 14 external tools. Any of them could release breaking changes. Mitigation: Pin tool versions in `veritas.toml`. Dependency fingerprinting (from T9 plan) applies to VERITAS tools themselves.

**Risk 3: Verus Subset Limitation**

Verus doesn't support all Rust patterns. SMITH Authority might use patterns Verus can't verify. Mitigation: Session 13 (Phase D) is specifically a feasibility check before committing to full T7 implementation. If Verus can't handle SMITH's patterns, Kani (bounded model checking) is the fallback — weaker guarantees but broader Rust support.

### Implementation Risks

| Risk | Mitigation |
|------|------------|
| `cargo-mutants` too slow for nightly | Run on critical modules only (8–12 modules, not all 352 files). Budget: 30 minutes max. |
| `loom` state explosion on complex modules | Scope to synchronization boundaries (Mutex, channel, atomic), not full modules. |
| TLA+ learning curve | Start with PlusCal (algorithmically closer to code). TLA+ community has extensive SMITH-relevant examples. |
| CodeQL false positives overwhelm triage | Start with high-confidence queries only. Suppress with justification. Track false positive rate. |
| `proptest` flaky failures from random generation | Regression seeds: when a property fails, the seed is saved and re-tested deterministically in future runs. |
| Evidence chain storage grows large | Pruning policy: keep last 90 days of evidence. Archive older entries. Hash chain remains verifiable from any retained entry. |

---

## 14. Known Fragility Points

| Fragility | When It Bites | Future Fix |
|-----------|---------------|------------|
| AL is weakest-link — one hard tier blocks all progress | Developer tempted to skip hard tiers or lower target AL | Hard Rule #4: overrides are logged governance events. Dashboard shows AL trajectory over time. |
| Feedback suggestions accumulate without action | Suggestion backlog grows, becomes noise | Periodic triage: unactioned suggestions older than 30 days are auto-closed with "deferred" status. |
| TLA+ models drift from code | Code refactored, TLA+ model not updated, model-code gap reopens | Kani bounded model checking runs on actual code, catching drift. TLA+ model update is a finding if Kani disagrees. |
| Verus annotations become maintenance burden | 2–4x annotation-to-code ratio means changes require proof updates | AutoVerus re-generates proofs on code change. If it fails, human proof update is a session task. |
| Nightly profile takes too long | Fuzzing + mutations + model checking exceed time budget | Per-tool time caps in `veritas.toml`. Prioritize critical modules. Degrade gracefully: partial results with coverage metric. |

---

## 15. Architect Assessment

**Status:** Fully implementable with existing tools. No research dependency below T7.

| Dimension | Rating |
|-----------|--------|
| Tool maturity | Strong — all tools production-ready, most 3+ years stable |
| Governance integrity | Strong — four hard rules, weakest-link AL, hash-chained evidence |
| Frozen core protection | Preserved — wraps BuildGuard, doesn't replace it |
| Phase discipline | Excellent — A/B/C/D ordering, three formal contracts gate Phase A |
| Feedback loop design | Novel — tier-to-tier evidence propagation, but implemented as suggestions not automation |
| Scope containment | Tight — 20–30 Verus functions, 8–12 loom modules, 4 TLA+ models |
| Human risk factor | Moderate — Verus annotation maintenance is the long-term cost |
| Implementation feasibility | High — 38–51 sessions, phased correctly |

**Why this works:**
- Every tool in the plan is production-ready and MIT/Apache licensed
- Phase A (property + mutation) catches real bugs with 6–8 sessions of investment
- Phase B (fuzzing + taint) uses tools already proven at scale (Google OSS-Fuzz, GitHub CodeQL)
- Phase C (model checking) uses TLA+, proven by AWS/Azure/MongoDB for exactly this class of problem
- Phase D (formal verification) is the stretch goal, scoped to 20–30 functions, with AutoVerus reducing proof burden
- Evidence schema is the backbone — lock it first, everything else follows
- BuildGuard remains the gate — VERITAS is additive, never subtractive

---

## 16. Next Steps

Phase A is next. Everything else waits.

**Three formal contracts to write:**
- [ ] Evidence schema (§10.2) — lock format, validate with mock evidence for SMITH Authority
- [ ] `veritas.toml` configuration (§10.3) — lock profiles, validate defaults for SMITH
- [ ] Feedback loop contracts (§10.4) — lock inter-tier communication format

**Phase A execution:**
- [ ] Add `proptest` dependency to `forge-smithy` Cargo.toml
- [ ] Write property tests for SMITH Authority: nonce uniqueness, signature coverage, key zeroing
- [ ] Write property tests for hash chain: append integrity, serialization roundtrip, no fork
- [ ] Write property tests for pipeline: monotonic transitions, locked state guards
- [ ] Run `cargo-mutants` on SMITH Authority — baseline kill rate
- [ ] Generate first evidence bundle — validate schema, hash chain, AL computation
- [ ] Integrate AL score into BuildGuard evidence output

**Validation before Phase B:**
- [ ] Confirm `proptest` catches at least one bug that example tests miss (or verify no such bug exists)
- [ ] Confirm `cargo-mutants` identifies at least 3 surviving mutants worth investigating
- [ ] Confirm evidence schema handles all Foundation + T0 + T1 outputs cleanly
- [ ] Confirm `veritas.toml` profile system correctly selects tiers per profile
