# VERITAS T8–T10 Implementation Plan

## Typed Specification Algebra + Protocol Grammar + Behavior Lattice

**Codename:** VERITAS Upper Tiers  
**Version:** 0.1  
**Status:** Implementation Plan — Session-Level Detail  
**Author:** BDS Architecture  
**Prerequisite:** VERITAS Foundation–T7 producing properties, proofs, and evidence  
**Estimated Total Effort:** 30–42 sessions across three phases

---

## §1 — The Core Innovation

Current state-of-the-art for translating natural language requirements into formal specifications achieves 44–71% correctness (GPT-4o on aerospace requirements: 44%; BOSCH Req2Spec on automotive: 71%; SpecSyn: ~72%). All fail silently — they produce formulas that look correct but contain wrong quantifiers, missing temporal operators, or inverted logic.

VERITAS T8–T10 takes a different approach: a **Typed Specification Algebra (TSA)** where specification elements are algebraic objects with types, and composition follows grammatical rules that enforce logical correctness by construction. The LLM handles vocabulary mapping (98.5% demonstrated recall on atomic propositions). Deterministic type-checked algebra handles logical composition. The result: ~80%+ correct formalization with the remaining 20% explicitly flagged for human review rather than silently wrong.

This is built on three mathematical foundations:
- **Montague Grammar:** Every word has a type; grammar is function application
- **Compositional Distributional Semantics:** Words live in geometric spaces where distance encodes meaning
- **Domain-Specific Algebraic Laws:** Governance patterns reduce to a finite set of composable templates

---

## §2 — Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    T8: Intention Verification                │
│                                                              │
│  SYSTEM.md ──► Vocabulary   ──► Typed     ──► Formal        │
│  ADRs          Mapper (LLM)    Composer       Properties    │
│  Doc Comments                  (Algebra)      + Traceability │
│                                                              │
│  Human Confirmation Gate between Mapper and Composer         │
├─────────────────────────────────────────────────────────────┤
│                    T9: Emergent Behavior                      │
│                                                              │
│  Service APIs ──► Protocol    ──► Interaction  ──► Conformance│
│  IPC Contracts    Grammars       Recorder         Checker    │
│  Integration      (FSA)          (Traces)         + Coverage │
│  Laws                                                        │
│                                                              │
│  Compositional TLA+ for cross-service model checking         │
├─────────────────────────────────────────────────────────────┤
│                    T10: Specification Completeness            │
│                                                              │
│  Code AST ──► Behavior     ──► Surface    ──► Gap           │
│  Commands     Extractor        Differ         Catalog       │
│  Schemas      (Static)         (Bidirectional) + Triage     │
│  Events                                                      │
│                                                              │
│  Mutation-driven completeness: surviving mutants = spec gaps │
└─────────────────────────────────────────────────────────────┘
```

---

## §3 — T8: The Typed Specification Algebra

### 3.1 The Type System

Every term in the specification vocabulary has a type. Types determine how terms compose. Ill-typed compositions are rejected at construction time — no runtime surprises.

**Base Types:**

| Type | Description | Examples |
|------|-------------|---------|
| `Entity` | A thing in the system | `locked_state`, `pipeline`, `secret`, `hash_chain`, `human` |
| `Bool` | True/false | Result of property evaluation |
| `Proposition` | A formal claim | `requires(transition(s), approval)` |
| `Action` | Something that happens | `transition`, `sign`, `persist`, `emit` |
| `Event` | Observable occurrence | `approval_granted`, `circuit_trip`, `evidence_created` |
| `Time` | Temporal reference | `before`, `after`, `within(ms)` |

**Higher-Order Types (functions over base types):**

| Type Signature | Description | Examples |
|----------------|-------------|---------|
| `Entity → Bool` | Property of an entity | `is_locked`, `is_signed`, `is_secret` |
| `Entity → Entity` | Modifier | `locked`, `signed`, `validated` |
| `Entity → Entity → Proposition` | Binary relation | `requires`, `produces`, `contains` |
| `Action → Action → Proposition` | Ordering relation | `precedes`, `follows`, `concurrent_with` |
| `Proposition → Proposition` | Temporal modifier | `always`, `eventually`, `never`, `until` |
| `(Entity → Proposition) → Proposition` | Quantifier | `for_all`, `there_exists` |

### 3.2 The Governance Pattern Templates

Analysis of SYSTEM.md, Five Integration Laws, and Forge Ecosystem specs reveals six core governance patterns. These are the algebraic "shapes" that ~80–90% of requirements reduce to.

**Pattern 1 — Access Control (Gate)**
```
Template:  for_all(e: Entity where P(e), requires(A(e), authority_level))
English:   "Locked states require human approval to transition"
Formal:    for_all(s where is_locked(s), requires(transition(s), human_approval))
TLA+:      \A s \in {s \in States : IsLocked(s)} : Transition(s) => HasApproval(s)
Verus:     requires(self.state.is_locked() ==> approval.is_some())
```

**Pattern 2 — Data Flow Constraint (Boundary)**
```
Template:  for_all(v: Entity where P(v), never_reaches(v, sink))
English:   "No secret crosses the IPC boundary"
Formal:    for_all(v where is_secret(v), never_reaches(v, ipc_boundary))
CodeQL:    @source is_secret(v) @sink ipc_serialize(v) → violation
Verus:     ensures(!output.contains_secret())
```

**Pattern 3 — Ordering Constraint (Temporal)**
```
Template:  always(precedes(event_a, event_b))
English:   "Evidence signing completes before persistence is attempted"
Formal:    always(precedes(evidence_signed, dataforge_persist))
TLA+:      AG(evidence_signed => A[~dataforge_persist U evidence_signed])
Proptest:  assert!(log.index_of(signed) < log.index_of(persisted))
```

**Pattern 4 — Invariant (State)**
```
Template:  always(when(condition, property))
English:   "The hash chain never forks"
Formal:    always(when(chain_appended, single_predecessor))
TLA+:      \A e \in Entries : Len(Predecessors(e)) = 1
Verus:     invariant(self.chain.iter().all(|e| e.prev_count() == 1))
```

**Pattern 5 — Liveness (Progress)**
```
Template:  always(when(trigger, eventually(outcome)))
English:   "Every circuit breaker trip eventually produces a governance event"
Formal:    always(when(circuit_trip, eventually(governance_event_emitted)))
TLA+:      AG(circuit_trip => AF(governance_event))
Proptest:  eventually!(events, |e| e.is_governance(), after: circuit_trip)
```

**Pattern 6 — Atomicity (Transaction)**
```
Template:  atomic(operation_set, on_failure: rollback_action)
English:   "MRPA patch application is all-or-nothing with rollback"
Formal:    atomic([backup, stage, apply, verify], on_failure: restore_backup)
TLA+:      \A op \in PatchOps : Completed(op) \/ AllRolledBack(op)
Verus:     ensures(result.is_ok() ==> all_applied() || result.is_err() ==> all_restored())
```

### 3.3 The Vocabulary

The domain vocabulary is the finite set of typed terms that the TSA recognizes. It is specific to the Forge Ecosystem but extensible.

**Entity Vocabulary (partial):**

| Term | Type | Source |
|------|------|--------|
| `locked_state` | Entity | SYSTEM.md §Pipeline States |
| `pipeline` | Entity | SYSTEM.md §Pipeline |
| `secret` / `api_key` / `credential` | Entity | SYSTEM.md §Security |
| `hash_chain` / `ledger` | Entity | SYSTEM.md §Evidence |
| `evidence_bundle` | Entity | SYSTEM.md §Evidence |
| `ipc_boundary` | Entity | Architecture Spec |
| `trust_boundary` | Entity | Five Integration Laws |
| `human` / `operator` | Entity | SYSTEM.md §Governance |
| `smith_authority` | Entity | SYSTEM.md §Authority |
| `run_intent` | Entity | SYSTEM.md §Pipeline |
| `nonce` | Entity | SYSTEM.md §Replay Prevention |

**Property Vocabulary (partial):**

| Term | Type | Maps To |
|------|------|---------|
| `is_locked` | Entity → Bool | state ∈ {PLAN_REVIEW, EVIDENCE_REVIEW} |
| `is_secret` | Entity → Bool | Zeroizing<T>, vault-sourced |
| `is_signed` | Entity → Bool | has valid Ed25519 signature |
| `is_valid` | Entity → Bool | passes schema + policy |
| `is_terminal` | Entity → Bool | state ∈ {RELEASED, FAILED, ABANDONED} |

**Relation Vocabulary (partial):**

| Term | Type | Pattern |
|------|------|---------|
| `requires` | Entity → Entity → Proposition | Gate |
| `produces` | Entity → Entity → Proposition | Liveness |
| `never_reaches` | Entity → Entity → Proposition | Boundary |
| `precedes` | Action → Action → Proposition | Temporal |
| `contains` | Entity → Entity → Proposition | Invariant |

### 3.4 The Composition Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Spec Text   │───►│  Vocabulary  │───►│   Human      │───►│   Typed      │
│  (English)   │    │  Mapper      │    │   Confirm    │    │   Composer   │
│              │    │  (LLM)       │    │   Gate       │    │   (Algebra)  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                           │                    │                    │
                    Typed terms +         Confirmed          Formal property
                    pattern guess         composition        in canonical form
                                                                    │
                                                                    ▼
                                                          ┌──────────────┐
                                                          │  Translation │
                                                          │  Engine      │
                                                          │  (Rules)     │
                                                          └──────────────┘
                                                                    │
                                                    ┌───────────────┼───────────────┐
                                                    ▼               ▼               ▼
                                              TLA+ Property   Verus Spec     Property Test
```

**Stage 1: Vocabulary Mapping (LLM)**

Input: One requirement sentence from SYSTEM.md
Output: Structured JSON of typed terms + candidate pattern

```json
{
  "source": "SYSTEM.md §3.2 line 47",
  "text": "Locked states require explicit human authority to transition",
  "atoms": [
    { "phrase": "locked states", "term": "locked_state", "type": "Entity", "confidence": 0.95 },
    { "phrase": "explicit human authority", "term": "human_approval", "type": "Entity", "confidence": 0.88 },
    { "phrase": "transition", "term": "transition", "type": "Action", "confidence": 0.97 }
  ],
  "relation": { "phrase": "require...to", "term": "requires", "type": "Entity→Entity→Proposition", "confidence": 0.92 },
  "pattern_guess": "access_control",
  "composition_guess": "for_all(s where is_locked(s), requires(transition(s), human_approval))"
}
```

The LLM is doing vocabulary lookup, not logical reasoning. This plays to demonstrated strengths.

**Stage 2: Human Confirmation Gate**

The operator sees:

```
Requirement: "Locked states require explicit human authority to transition"
Extracted:   for_all(s where is_locked(s), requires(transition(s), human_approval))
Pattern:     Access Control (Gate)

Atoms:
  ✓ "locked states" → locked_state (Entity)        [0.95]
  ? "explicit human authority" → human_approval     [0.88]
  ✓ "transition" → transition (Action)              [0.97]

Relation:
  ✓ "require...to" → requires                      [0.92]

[Confirm] [Edit] [Reject] [Flag Ambiguous]
```

Time per confirmation: 5–15 seconds for clear cases. 1–2 minutes for ambiguous ones. For a system with ~100 extractable requirements, this is a single afternoon of work.

**Stage 3: Typed Composition (Deterministic)**

No LLM. No randomness. The confirmed atoms are composed according to their types:

1. `is_locked` is type `Entity → Bool` and `s` is type `Entity` → `is_locked(s)` is type `Bool` ✓
2. `transition` is type `Action` applied to `s: Entity` → `transition(s)` is type `Action` ✓
3. `requires` is type `Entity → Entity → Proposition` → `requires(transition(s), human_approval)` is type `Proposition` ✓
4. `for_all` is type `(Entity → Proposition) → Proposition` → `for_all(s where is_locked(s), ...)` is type `Proposition` ✓

Type error example (caught at this stage):
```
"approval requires locked states" 
→ requires(human_approval, locked_state)
→ Type check: requires expects (Action|Entity, Authority) — locked_state is not an Authority
→ TYPE ERROR: rejected, flagged for human review
```

**Stage 4: Translation to Verification Targets (Rule-based)**

Each canonical pattern maps deterministically to one or more verification languages. These mappings are written once, tested, and reused.

| Pattern | TLA+ | Verus | Property Test | CodeQL |
|---------|------|-------|---------------|--------|
| Gate | `\A s \in Set : Action(s) => Guard(s)` | `requires(guard ==> action_allowed)` | `proptest! { assert!(guarded) }` | N/A |
| Boundary | `\A v \in Tainted : v \notin Sinks` | `ensures(!output.tainted())` | `assert!(!reaches_sink(v))` | `@source → @sink` query |
| Temporal | `AG(A => A[~B U A])` | N/A (runtime monitor) | `assert!(index_a < index_b)` | N/A |
| Invariant | `TypeInvariant == ...` | `invariant(...)` | `proptest! { assert!(inv) }` | N/A |
| Liveness | `AG(trigger => AF(outcome))` | N/A (runtime monitor) | `eventually!(outcome)` | N/A |
| Atomicity | `\A op : Done(op) \/ AllRolled(op)` | `ensures(ok ==> applied \|\| err ==> restored)` | `assert!(atomic_or_rolled)` | N/A |

### 3.5 Traceability Matrix

Every extracted property maintains a full trace:

```
SYSTEM.md §3.2 line 47
  └── FSL: for_all(s where is_locked(s), requires(transition(s), human_approval))
       ├── TLA+: PipelineSpec.tla line 34 [Model-checked: 1247 states, 0 violations]
       ├── Verus: authority.rs::advance_pipeline requires clause [Verified: ✓]
       ├── Property test: test_locked_requires_approval [10,000 inputs, all pass]
       └── Example test: test_locked_state_blocks_without_approval [Pass]
```

Gap detection:
- **Unverified intention:** Requirement has FSL property but no verification result at any tier
- **Orphaned verification:** Formal property exists but traces to no requirement
- **Intention drift:** Code change invalidated a previously-passing verification

---

## §4 — T9: Protocol Grammar + Interaction Model

### 4.1 Protocol Grammars

Each service boundary gets a formal protocol grammar — a finite state automaton describing legal interaction sequences.

**ForgeCommand → SMITH Protocol:**
```
START → authenticate → AUTHENTICATED
AUTHENTICATED → submit_intent → PENDING
PENDING → poll_status → PENDING
PENDING → receive_result → COMPLETE
PENDING → receive_error → FAILED  
PENDING → timeout → TIMEOUT
TIMEOUT → retry → PENDING  (max 3)
TIMEOUT → abort → FAILED
COMPLETE → acknowledge → START
FAILED → acknowledge → START
```

**SMITH → ForgeAgents Protocol:**
```
START → sign_intent → SIGNED
SIGNED → dispatch → DISPATCHED
DISPATCHED → poll_progress → DISPATCHED
DISPATCHED → receive_evidence → EVALUATING
DISPATCHED → receive_failure → FAILED
DISPATCHED → timeout → TIMEOUT
EVALUATING → validate_evidence → COMPLETE
EVALUATING → reject_evidence → RETRY
RETRY → re_dispatch → DISPATCHED  (max 2)
COMPLETE → persist_evidence → DONE
FAILED → emit_governance_event → DONE
```

**Grammar format:** Each protocol is stored as a JSON FSA:

```json
{
  "protocol": "smith_to_forgeagents",
  "version": "1.0",
  "states": ["START", "SIGNED", "DISPATCHED", "EVALUATING", "COMPLETE", "FAILED", "RETRY", "TIMEOUT", "DONE"],
  "initial": "START",
  "terminal": ["DONE"],
  "transitions": [
    { "from": "START", "action": "sign_intent", "to": "SIGNED" },
    { "from": "SIGNED", "action": "dispatch", "to": "DISPATCHED" },
    { "from": "DISPATCHED", "action": "receive_evidence", "to": "EVALUATING" },
    { "from": "DISPATCHED", "action": "receive_failure", "to": "FAILED" },
    { "from": "DISPATCHED", "action": "timeout", "to": "TIMEOUT", "guard": "elapsed > 30s" }
  ],
  "invariants": [
    "FAILED always followed by emit_governance_event",
    "RETRY count never exceeds 2"
  ]
}
```

### 4.2 Interaction Recording

Instrument every service boundary to record interaction traces during all test execution and development.

**Trace format:**
```json
{
  "trace_id": "uuid",
  "protocol": "smith_to_forgeagents",
  "timestamp_start": "2026-03-01T10:00:00Z",
  "events": [
    { "seq": 0, "action": "sign_intent", "from_state": "START", "to_state": "SIGNED", "ts": "..." },
    { "seq": 1, "action": "dispatch", "from_state": "SIGNED", "to_state": "DISPATCHED", "ts": "..." },
    { "seq": 2, "action": "receive_evidence", "from_state": "DISPATCHED", "to_state": "EVALUATING", "ts": "..." }
  ],
  "result": "DONE",
  "conformant": true
}
```

**Two analyses on recorded traces:**

1. **Conformance checking:** Does every recorded trace follow the protocol grammar? Non-conformant traces indicate emergent behavior — something happened that the protocol doesn't describe.

2. **Path coverage:** What percentage of the grammar's transitions have been exercised? Unreached transitions are verification gaps. A protocol with 12 transitions where only 8 have been exercised has 67% coverage — the other 4 are untested interaction patterns.

### 4.3 Compositional Model Checking

For cross-service workflows governed by the Five Integration Laws, compose service protocols into a joint model.

**Key abstraction:** Each service is modeled not by its internal states but by its **interaction-relevant** states. SMITH internally has 10+ pipeline states, but from ForgeAgents' perspective, SMITH is either requesting, waiting, or done (3 states).

**Composition for Integration Law 1 (ForgeCommand Root of Trust):**
```
ForgeCommand states: {idle, authenticating, authorized, revoking}
SMITH states:        {waiting_auth, executing, reporting}
Composed:            4 × 3 = 12 states

Property: AG(smith.executing => forgecommand.authorized)
  "SMITH never executes without ForgeCommand authorization"
```

**Composition for Integration Law 2 (SMITH Governs):**
```
SMITH states:        {evaluating, approved, denied}
ForgeAgents states:  {idle, running, completed}
Composed:            3 × 3 = 9 states

Property: AG(forgeagents.running => smith.approved)
  "ForgeAgents never runs without SMITH approval"
```

These are small enough for exhaustive TLA+ model checking — 9 to 27 states for each law.

### 4.4 Dependency Behavior Fingerprinting

For external dependencies, build behavioral fingerprints — property tests that exercise the behaviors YOUR code relies on.

**Example fingerprint for `ed25519-dalek`:**
```rust
#[test]
fn fingerprint_ed25519_sign_verify_roundtrip() {
    // Our code assumes: sign then verify always succeeds for valid keypair
    let keypair = SigningKey::generate(&mut OsRng);
    let msg = b"test message";
    let sig = keypair.sign(msg);
    assert!(keypair.verifying_key().verify(msg, &sig).is_ok());
}

#[test]
fn fingerprint_ed25519_different_msg_fails() {
    // Our code assumes: verification fails for wrong message
    let keypair = SigningKey::generate(&mut OsRng);
    let sig = keypair.sign(b"message A");
    assert!(keypair.verifying_key().verify(b"message B", &sig).is_err());
}

#[test]
fn fingerprint_ed25519_sig_length() {
    // Our code assumes: signatures are exactly 64 bytes
    let keypair = SigningKey::generate(&mut OsRng);
    let sig = keypair.sign(b"test");
    assert_eq!(sig.to_bytes().len(), 64);
}
```

Run fingerprint tests after every `cargo update`. If one fails, a dependency changed behavior your code depends on.

---

## §5 — T10: Behavior Enumeration Lattice

### 5.1 Define "Behavior" at the Contract Surface

Not every control flow path. Not every possible state. Instead: **observable state changes that cross a trust or persistence boundary.**

**The finite behavior surface:**

| Category | Source | Count (est.) | Extraction Method |
|----------|--------|--------------|-------------------|
| Tauri commands | `#[tauri::command]` | ~400 | AST/regex scan |
| DataForge writes | SQL INSERT/UPDATE/DELETE | ~73 tables | Schema scan |
| Governance events | Event enum variants | ~30-50 | Type scan |
| IPC message types | Invoke handler signatures | ~100 | AST scan |
| Error types | Public Result::Err variants | ~80-120 | Type scan |
| State transitions | State machine transition fns | ~30-40 | Pattern scan |

Total estimated behavior surface: **700–800 discrete behaviors.** This is finite and enumerable.

### 5.2 Auto-Extract Behavior Surface from Code

**Rust extraction (src-tauri):**
```bash
# Tauri commands
grep -rn '#\[tauri::command\]' src-tauri/src/ | extract_fn_signatures

# Error variants
grep -rn 'enum.*Error' src-tauri/src/ | extract_enum_variants

# State transitions
grep -rn 'fn.*transition\|fn.*advance\|fn.*move_to' src-tauri/src/ | extract_fn_signatures

# Governance events
grep -rn 'GovernanceEvent\|emit_event' src-tauri/src/ | extract_event_types
```

**Frontend extraction (Svelte/TS):**
```bash
# IPC invocations (what the frontend asks the backend to do)
grep -rn 'invoke(' src/lib/ | extract_invoke_signatures

# Store mutations (observable state changes in the UI)
grep -rn '\$state\|\.set(' src/lib/stores/ | extract_store_mutations
```

**Output: `behavior_surface.json`**
```json
{
  "version": "1.0",
  "extracted_at": "2026-03-01T10:00:00Z",
  "commit": "abc123",
  "behaviors": [
    {
      "id": "cmd::advance_pipeline",
      "category": "tauri_command",
      "signature": "fn advance_pipeline(state: PipelineState, approval: Option<Approval>) -> Result<PipelineState, SmithError>",
      "file": "src-tauri/src/smith/pipeline.rs",
      "line": 142,
      "inputs": ["PipelineState", "Option<Approval>"],
      "outputs": ["PipelineState"],
      "errors": ["SmithError::Unauthorized", "SmithError::InvalidTransition"],
      "side_effects": ["governance_event_emitted", "dataforge_write"]
    }
  ]
}
```

### 5.3 Auto-Extract Spec Surface from Documentation

Parse SYSTEM.md and all spec documents for behavioral claims.

**Extraction targets:**
- Imperative: "the system shall," "ForgeCommand must," "SMITH always"
- Descriptive: "evidence is persisted," "keys are zeroed," "nonces are unique"
- Constraint: "never," "only when," "at most," "before," "after"
- Conditional: "if...then," "when...must," "unless"

**Leverage T8 FSL extraction:** Every requirement that T8 already translated into a typed property is automatically a spec-surface entry. T10 adds a second pass for behavioral descriptions that aren't formal requirements but still describe what the system does.

**Output: `spec_surface.json`**
```json
{
  "version": "1.0",
  "extracted_at": "2026-03-01T10:00:00Z",
  "claims": [
    {
      "id": "spec::pipeline_locked_approval",
      "source": "SYSTEM.md §3.2 line 47",
      "text": "Locked states require explicit human authority to transition",
      "fsl_property": "for_all(s where is_locked(s), requires(transition(s), human_approval))",
      "behaviors_covered": ["cmd::advance_pipeline"],
      "verification_tier": "T7"
    }
  ]
}
```

### 5.4 Surface Diff

Compare the two surfaces. Three categories:

| Category | Meaning | Action |
|----------|---------|--------|
| **Specified + Implemented** | Behavior exists in both surfaces | No action — this is the goal state |
| **Specified + Not Implemented** | Spec describes something the code doesn't do | Either aspirational spec or missing implementation |
| **Implemented + Not Specified** | Code does something the spec doesn't describe | **Finding** — ungoverned behavior |

The third category is the primary output. Each ungoverned behavior gets triaged:

| Triage Level | Description | Example |
|-------------|-------------|---------|
| **Obvious Implicit** | Covered by language/framework guarantees | Rust ownership prevents double-free |
| **Reasonable Default** | Standard error handling, sensible fallback | Timeout returns error after 30s |
| **Spec Debt** | Should be specified, behavior is correct | Retry logic on network failure |
| **Genuine Gap** | Behavior was never intentionally designed | Silent retry on auth failure |
| **Potential Bug** | Behavior contradicts other spec entries | State transition bypasses gate |

### 5.5 Implicit Behavior Whitelist

Behaviors that DON'T need specification because they're guaranteed by infrastructure:

| Infrastructure | Behaviors Covered |
|---------------|-------------------|
| Rust ownership model | No double-free, no use-after-free, no data races on non-Sync types |
| Rust type system | No null pointer dereference, no type confusion |
| Tauri IPC serialization | Type-safe deserialization, no arbitrary code execution from frontend |
| Serde derive | Serialization roundtrip preserves all fields |
| SQLite ACID | Transaction atomicity, isolation |
| Tokio runtime | Async task scheduling, executor lifecycle |

These are excluded from the completeness check. What remains is the application-level behavior surface.

### 5.6 Mutation-Driven Completeness

Connect T1 (mutation testing) to T10: instead of checking whether tests catch a mutation, check whether the spec PREDICTS the mutation's effect.

**Process:**
1. `cargo-mutants` introduces a mutation (e.g., removes a state transition guard)
2. For each surviving mutant, query the spec surface: "is there a spec entry that describes what should happen when this guard is present?"
3. If no spec entry exists → **the spec is incomplete for this behavior**
4. If a spec entry exists but no verification covers it → **the spec is unverified for this behavior**

This transforms surviving mutants from "test gaps" into "spec gaps" — a much more fundamental finding.

---

## §6 — Session-by-Session Implementation Plan

### Phase A: T8 — Typed Specification Algebra (Sessions 1–12)

**Session A1: Vocabulary Definition**
- Input: SYSTEM.md, Five Integration Laws, Architecture Spec
- Task: Define the complete typed vocabulary (entities, properties, relations, quantifiers, temporal modifiers)
- Output: `tsa_vocabulary.json` — the typed term catalog
- Acceptance: Every term has a type, every type has a composition rule, vocabulary covers all Integration Laws

**Session A2: Pattern Template Library**
- Input: Vocabulary from A1, requirement samples from SYSTEM.md
- Task: Define the six governance patterns with full type signatures and composition rules
- Output: `tsa_patterns.rs` (or `.ts`) — pattern definitions with type-checking logic
- Acceptance: Each pattern can type-check a well-formed composition and reject an ill-formed one

**Session A3: Vocabulary Mapper (LLM Prompt Engineering)**
- Input: Vocabulary from A1, patterns from A2
- Task: Design and test the LLM prompt that maps English sentences to typed vocabulary terms
- Output: `vocabulary_mapper.py` — prompt + parser for structured output
- Test: Run against 20 sample requirements from SYSTEM.md, measure extraction accuracy
- Acceptance: ≥90% atomic proposition recall, ≥80% correct pattern classification

**Session A4: Human Confirmation UI**
- Input: Mapper output format from A3
- Task: Build a simple confirmation interface (CLI or lightweight web) showing extracted terms, types, confidence scores, and pattern guess
- Output: `confirm_gate.py` (or Svelte component if integrating into SMITH)
- Acceptance: Operator can confirm/edit/reject each extraction in <15 seconds

**Session A5: Typed Composer**
- Input: Pattern library from A2, confirmed extractions from A4
- Task: Build the deterministic algebraic composer that takes confirmed typed terms and produces canonical formal properties
- Output: `tsa_composer.rs` — takes typed terms + pattern, outputs canonical FSL form
- Test: All six patterns compose correctly; ill-typed inputs rejected with clear error
- Acceptance: Zero silent failures — every composition either succeeds or produces a type error

**Session A6: Translation Engine — TLA+**
- Input: Canonical FSL forms from A5
- Task: Build rule-based translation from FSL to TLA+ property syntax
- Output: `translate_tla.py` — FSL → TLA+ property
- Test: Generate TLA+ for all six pattern types, validate syntax with TLA+ toolbox
- Acceptance: Generated TLA+ parses without error for all supported patterns

**Session A7: Translation Engine — Verus**
- Input: Canonical FSL forms from A5
- Task: Build rule-based translation from FSL to Verus specification syntax
- Output: `translate_verus.py` — FSL → Verus requires/ensures clauses
- Test: Generate Verus specs for Gate, Boundary, Invariant, Atomicity patterns
- Acceptance: Generated Verus specs parse without error in Verus toolchain

**Session A8: Translation Engine — Property Tests**
- Input: Canonical FSL forms from A5
- Task: Build rule-based translation from FSL to proptest/fast-check assertions
- Output: `translate_proptest.py` — FSL → Rust proptest or TS fast-check code
- Test: Generate property tests for all six patterns, verify they compile and run
- Acceptance: Generated tests catch known violations (inject mutation, verify test fails)

**Session A9: Full Pipeline Integration**
- Input: All components from A1–A8
- Task: Wire the pipeline end-to-end: SYSTEM.md → Mapper → Confirm → Compose → Translate
- Output: `tsa_pipeline.py` — orchestrator that runs the full extraction pipeline
- Test: Process the Five Integration Laws end-to-end, produce TLA+, Verus, and proptest outputs
- Acceptance: All five laws produce valid formal properties in all three target languages

**Session A10: Traceability Matrix**
- Input: Pipeline output from A9, existing VERITAS evidence chain
- Task: Build the bidirectional traceability system linking SYSTEM.md sections → FSL properties → verification results
- Output: `traceability.json` schema + update logic in evidence chain
- Acceptance: Can answer "which requirement covers this code path?" and "which code paths verify this requirement?"

**Session A11: Gap Detection**
- Input: Traceability matrix from A10
- Task: Build detection for unverified intentions (requirement with no verification) and orphaned verifications (proof with no requirement)
- Output: Gap detection report integrated into VERITAS evidence output
- Acceptance: Identifies at least one real gap in current SMITH verification coverage

**Session A12: Drift Detection**
- Input: Traceability from A10, git diff integration
- Task: On code change, re-evaluate affected FSL properties and flag drift
- Output: `drift_detector.py` — runs on CI, produces drift findings
- Acceptance: Modifying a state transition guard produces an intention drift finding

---

### Phase B: T10 — Specification Completeness (Sessions 13–24)

**Session B1: Rust Behavior Extractor**
- Input: SMITH source code (src-tauri/)
- Task: Build AST-based extractor for Tauri commands, error variants, state transitions, event types
- Output: `extract_behaviors_rust.py` — produces behavior_surface.json for Rust code
- Acceptance: Extracts all ~400 Tauri commands with signatures, errors, and side effects

**Session B2: Frontend Behavior Extractor**
- Input: SMITH frontend source (src/lib/)
- Task: Build extractor for IPC invocations, store mutations, event handlers
- Output: `extract_behaviors_frontend.py` — produces behavior_surface.json for TS/Svelte code
- Acceptance: Extracts all invoke() calls with parameter types and error handling

**Session B3: Schema Behavior Extractor**
- Input: DataForge schema (73 tables)
- Task: Extract all write operations, constraints, triggers from database schema
- Output: `extract_behaviors_schema.py` — produces behavior_surface.json for persistence layer
- Acceptance: Every table write operation is cataloged with its constraints

**Session B4: Unified Behavior Surface**
- Input: Extractors from B1–B3
- Task: Merge all behavior extractions into a single deduplicated behavior surface
- Output: `behavior_surface.json` — the complete catalog of what the code CAN do
- Acceptance: Coverage check against known major features — no major subsystem missing

**Session B5: Spec Surface Extractor**
- Input: SYSTEM.md, all spec documents, T8 FSL properties
- Task: Extract behavioral claims from documentation using NLP pattern matching + T8 FSL output
- Output: `spec_surface.json` — the complete catalog of what the spec SAYS the code does
- Acceptance: Every Integration Law appears as a spec-surface entry; every T8 property included

**Session B6: Surface Differ**
- Input: behavior_surface.json, spec_surface.json
- Task: Build the bidirectional diff that identifies specified+implemented, specified+not-implemented, implemented+not-specified
- Output: `surface_diff.py` — produces gap report
- Acceptance: Produces a categorized gap report with zero false positives for "obvious implicit" behaviors

**Session B7: Implicit Behavior Whitelist**
- Input: Gap report from B6
- Task: Define and apply the infrastructure whitelist (Rust guarantees, Tauri guarantees, SQLite guarantees)
- Output: `implicit_whitelist.json` — behaviors excluded from completeness check with justification
- Acceptance: Reduces false positives by ≥50% without missing genuine gaps

**Session B8: Triage Engine**
- Input: Filtered gap report from B6+B7
- Task: Build automated triage that classifies ungoverned behaviors into the five triage levels
- Output: `triage_engine.py` — classifies each gap with confidence score
- Acceptance: ≥70% of auto-triaged gaps match human triage judgment

**Session B9: Mutation-Driven Completeness**
- Input: cargo-mutants output (from T1), spec_surface.json
- Task: For each surviving mutant, check whether the spec predicts the mutation's effect
- Output: `mutation_spec_gaps.py` — transforms surviving mutants into spec-gap findings
- Acceptance: Identifies at least 3 spec gaps that surviving mutants reveal and pure surface diff misses

**Session B10: Completeness Score**
- Input: All T10 outputs
- Task: Define and compute a specification completeness score
- Output: Completeness metric integrated into VERITAS assurance level
- Formula: `completeness = specified_and_implemented / (total_behaviors - implicit_whitelisted)`
- Acceptance: Score computes correctly and changes when spec or code changes

**Session B11: Evidence Integration**
- Input: All T10 outputs, VERITAS evidence chain
- Task: Integrate T10 findings into the hash-chained evidence ledger
- Output: T10 evidence entries in the VERITAS bundle
- Acceptance: Evidence chain includes completeness score, gap catalog, triage results

**Session B12: CI Integration**
- Input: Full T10 pipeline
- Task: Run T10 checks in CI, fail on untriaged genuine gaps or potential bugs
- Output: CI step that runs behavior extraction, spec extraction, diff, and triage
- Acceptance: PR that introduces ungoverned behavior without spec update gets flagged

---

### Phase C: T9 — Protocol Grammar + Emergent Behavior (Sessions 25–38)

**Session C1: Protocol Grammar — ForgeCommand ↔ SMITH**
- Input: ForgeCommand/SMITH integration docs, IPC contract
- Task: Define the formal protocol grammar as a JSON FSA
- Output: `protocol_forgecommand_smith.json`
- Acceptance: Grammar covers all known interaction patterns including error and timeout paths

**Session C2: Protocol Grammar — SMITH ↔ ForgeAgents**
- Task: Define FSA for SMITH ↔ ForgeAgents interaction
- Output: `protocol_smith_forgeagents.json`

**Session C3: Protocol Grammar — SMITH ↔ DataForge**
- Task: Define FSA for SMITH ↔ DataForge interaction
- Output: `protocol_smith_dataforge.json`

**Session C4: Protocol Grammar — SMITH ↔ NeuroForge**
- Task: Define FSA for SMITH ↔ NeuroForge interaction
- Output: `protocol_smith_neuroforge.json`

**Session C5: Protocol Grammar — SMITH ↔ Rake**
- Task: Define FSA for SMITH ↔ Rake interaction
- Output: `protocol_smith_rake.json`

**Session C6: Interaction Recorder**
- Input: Protocol grammars from C1–C5
- Task: Build instrumentation that records interaction traces at every service boundary during test execution
- Output: `interaction_recorder.rs` (Rust middleware) + `interaction_recorder.ts` (frontend interceptor)
- Acceptance: Running the test suite produces trace files for every cross-service interaction

**Session C7: Conformance Checker**
- Input: Recorded traces from C6, protocol grammars from C1–C5
- Task: Build checker that validates every trace against its protocol grammar
- Output: `conformance_checker.py` — flags non-conformant traces
- Acceptance: Injecting an out-of-order interaction produces a conformance violation

**Session C8: Path Coverage Analyzer**
- Input: Protocol grammars, recorded traces
- Task: Compute which grammar transitions have been exercised by traces
- Output: Coverage report per protocol — transitions hit, transitions missed
- Acceptance: Identifies at least one untested error/timeout path per protocol

**Session C9: Compositional Model — Integration Law 1**
- Input: Protocol grammars for ForgeCommand ↔ SMITH
- Task: Write TLA+ model composing ForgeCommand and SMITH abstractions, verify root-of-trust property
- Output: `integration_law_1.tla`
- Acceptance: TLA+ model checker verifies the property for all reachable states

**Session C10: Compositional Model — Integration Law 2**
- Input: Protocol grammars for SMITH ↔ ForgeAgents
- Task: Write TLA+ model composing SMITH and ForgeAgents abstractions, verify governance property
- Output: `integration_law_2.tla`
- Acceptance: Property verified for all reachable states

**Session C11: Compositional Model — Integration Laws 3–5**
- Input: Remaining protocol grammars
- Task: Write TLA+ models for remaining Integration Laws (Evidence, Single Writer, Human Override)
- Output: `integration_law_3.tla`, `integration_law_4.tla`, `integration_law_5.tla`
- Acceptance: All properties verified

**Session C12: Dependency Fingerprinting**
- Input: Cargo.toml dependencies, package.json dependencies
- Task: Write behavioral fingerprint tests for critical dependencies (ed25519-dalek, serde, tokio, sqlx)
- Output: `fingerprint_tests/` directory with property tests per critical dependency
- Acceptance: Tests pass on current versions; manually downgrading a dependency breaks at least one fingerprint

**Session C13: Fingerprint CI Integration**
- Input: Fingerprint tests from C12
- Task: Run fingerprint tests on `cargo update` and `pnpm update`, fail on regression
- Output: CI step that catches dependency behavior drift
- Acceptance: Simulated dependency behavior change (via mock) triggers CI failure

**Session C14: Evidence Integration**
- Input: All T9 outputs
- Task: Integrate protocol conformance, path coverage, model checking results, and fingerprint results into VERITAS evidence chain
- Output: T9 evidence entries in the VERITAS bundle
- Acceptance: Evidence chain includes conformance results per protocol, coverage per protocol, TLA+ verification results, fingerprint status

---

## §7 — Assurance Level Integration

With T8–T10 complete, the full VERITAS Assurance Level system is operational:

| Level | Tiers | Verification |
|-------|-------|-------------|
| AL-7 | T8 + T9 + T10 | Spec ↔ code alignment proven bidirectionally |

**AL-7 gate criteria:**
- T8: Every SYSTEM.md requirement has at least one verified formal property (no unverified intentions)
- T9: All protocol grammars have ≥90% path coverage; all Integration Law models verified; all dependency fingerprints pass
- T10: Specification completeness score ≥85%; zero untriaged genuine gaps; zero potential bugs

**AL-7 target components:**
- Five Integration Laws (the governance core)
- Pipeline state machine (the execution engine)
- SMITH Authority (the trust anchor)

Not everything needs AL-7. UI components stay at AL-1. Service clients stay at AL-3. Only the governance core — the part where correctness IS the product — needs the full T8–T10 treatment.

---

## §8 — Dependencies and Prerequisites

### Required Before Phase A
- VERITAS T0 (property testing) operational — provides target for generated property tests
- VERITAS T5 (model checking) operational — provides TLA+ infrastructure for generated properties
- VERITAS T7 (formal verification) at least prototyped — provides Verus infrastructure for generated specs

### Required Before Phase B
- Phase A complete (T8 FSL properties feed T10 spec surface)
- VERITAS T1 (mutation testing) operational — provides surviving mutants for mutation-driven completeness

### Required Before Phase C
- Phase A complete (T8 property templates inform protocol invariants)
- Phase B complete (T10 behavior surface identifies service boundaries to instrument)
- VERITAS T5 (model checking) operational — provides TLA+ infrastructure for compositional models

### Tool Requirements
- Python 3.11+ (pipeline orchestration, extractors)
- Rust nightly (Verus integration)
- TLA+ toolbox (model checking)
- tree-sitter (AST parsing for behavior extraction)
- LLM API access (vocabulary mapping — Claude or equivalent)

---

## §9 — Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| LLM vocabulary mapping accuracy below 80% | Phase A delays | Fallback to manual vocabulary mapping for first pass; improve prompts iteratively |
| TSA patterns don't cover edge-case requirements | Incomplete T8 coverage | Add a "custom" pattern type with manual composition for the ~10-20% that don't fit |
| Behavior extraction misses code paths | False completeness in T10 | Cross-validate with coverage tools; mutation testing catches extractor gaps |
| Protocol grammars too complex for TLA+ | Phase C model checking fails | Abstract more aggressively; verify critical paths only, not full protocols |
| Human confirmation becomes bottleneck | Slow iteration on spec changes | Batch confirmations; cache confirmed mappings; only re-confirm on vocabulary changes |
| Spec surface extraction has high false positive rate | Noisy T10 results | Tune NLP patterns conservatively; human review for first pass; improve iteratively |

---

## §10 — Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| T8 formalization accuracy | ≥80% correct (remainder flagged, not silent) | Manual review of 50 extracted properties vs. intended meaning |
| T8 coverage | Every Integration Law has ≥1 verified formal property | Traceability matrix completeness |
| T9 protocol conformance | 100% of recorded traces conform to grammar | Conformance checker output |
| T9 path coverage | ≥90% of protocol transitions exercised | Coverage analyzer output |
| T9 model checking | All Integration Laws verified for all reachable states | TLA+ model checker output |
| T10 completeness score | ≥85% for governance core modules | Surface diff metric |
| T10 ungoverned behaviors | Zero untriaged genuine gaps in governance core | Triage report |
| End-to-end | At least 3 SMITH components reach AL-7 | VERITAS evidence chain |
| Time-to-value | Useful findings from Phase A alone | Gap report identifies real issues by session A11 |
