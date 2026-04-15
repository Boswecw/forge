# ForgeCommand — VS Code Opus 4.6 Implementation Prompt

**Date:** 2026-04-09  
**Target:** Repo-first Registry closure  
**Primary goal:** Make the Registry worktable flow from finding → review → fix → verify actually usable before broader automation

---

## Role

You are acting as a senior Rust + Svelte + Tauri engineer working inside the `Forge_Command` repo.

You must implement the next closure slice for the Registry subsystem.

This is **not** a greenfield design task.
This is a targeted implementation task against the current codebase.

You must work from the existing Registry substrate already present in the repo:
- discovery
- workflow
- persistence
- repo state derivation
- compliance
- remediation planning/apply/verify
- event sink
- UI surfaces already present for registry and remediation workflows

Do not invent a parallel system.
Do not rewrite Registry broadly.
Do not expand to Forge_Library.
Do not reopen Postgres / DataForge Local migration.
Do not broaden scope into unrelated UX polish.

Stay focused on getting the **repo-level worktable loop** working end to end.

---

## Problem to solve

ForgeCommand needs the Registry worktable to reliably support this flow:

1. find governed repos and intake candidates
2. evaluate canonical documentation compliance
3. show exactly what is wrong
4. produce bounded remediation actions
5. let the operator approve
6. apply repo-local scaffold/fix actions
7. rebuild canonical docs
8. verify honestly
9. reflect post-fix state back in the Registry/UI

Right now the substrate is real, but the loop is incomplete and partially legacy-bound.

The biggest current closure issue is that the compliance and validation posture still reflects legacy output expectations instead of the canonical repo-level doctrine.

---

## Canonical target

A governed repo should only be treated as documentation-compliant when all of the following are true:

- there is one active unique 3-letter designation
- the repo has an approved repo class
- `doc/system/` exists
- universal required structure exists
- class-aware required structure exists
- `doc/system/BUILD.sh` exists
- canonical assembled output exists at `doc/{DESIGNATION}SYSTEM.md`
- rebuild/verify evidence supports that state

Legacy outputs such as:
- `SYSTEM.md`
- `doc/SYSTEM.md`
- `doc/fcSYSTEM.md`

must be treated as migration signals only, not compliant success.

---

## Immediate implementation objective

Implement the first real closure slice:

# **Registry Worktable Closure Slice 1 — Canonical compliance + worktable actionability**

This slice must make the worktable actually useful for repo-level finding → fix operations.

That means:
- canonical finding generation
- precise remediation planning
- actionability in the worktable/read models
- approval-gated apply flow
- post-apply rebuild/verify wiring
- honest status reflection back to the operator

---

## Required outcome

After this slice, ForgeCommand must be able to take **one governed repo** through this loop:

1. Registry detects repo
2. Registry evaluates doc posture against canonical rules
3. worktable/detail surface clearly shows findings
4. remediation plan is bounded and specific
5. approved apply runs only the allowed actions
6. rebuild runs repo-local doc build
7. verification checks canonical output path
8. Registry reflects final state accurately

This must be real, not simulated.

---

## Constraints

### Stay repo-first
Do not implement estate-wide aggregation or Forge_Library work in this slice.

### Stay SQLite-backed
Do not reintroduce PostgreSQL / DataForge Local runtime changes.

### No broad refactor theater
Only refactor where necessary to make the worktable loop correct and maintainable.

### Do not loosen trust silently
If repo-local build/verify execution is used, keep it explicit and bounded.

### No fake compliance
A repo may not be marked compliant through legacy artifact names.

### No UI-only patching
Do not merely hide problems in the frontend. Fix backend truth first, then wire UI/read models cleanly.

---

## Priority order

### Priority 1 — Canonical compliance truth
Refactor compliance evaluation so it uses designation-bound canonical output instead of legacy artifact candidates.

### Priority 2 — Worktable actionability
Make findings/remediation/read-model outputs clear enough that the operator can move from finding to fix without inference.

### Priority 3 — Apply/rebuild/verify continuity
Ensure the existing remediation/apply/verify flow closes the loop cleanly for at least one repo.

### Priority 4 — Honest post-fix state
After apply/verify, the registry state and worktable must reflect reality, not stale status.

---

## Implementation tasks

## Task A — Audit the current registry path for the worktable loop

Inspect and map the current flow across these likely files/modules:

- `src-tauri/src/registry/compliance.rs`
- `src-tauri/src/registry/service.rs`
- `src-tauri/src/registry/workflow.rs`
- `src-tauri/src/registry/repo_state.rs`
- `src-tauri/src/registry/persistence/repository.rs`
- `src-tauri/src/models/registry.rs`
- registry-related Tauri commands
- frontend registry/worktable panes and types

Output for yourself before coding:
- where findings are generated
- where remediation actions are assembled
- where apply runs
- where build/verify runs
- where repo state is derived for the worktable
- where legacy output assumptions still exist

Do not skip this map.

---

## Task B — Replace legacy compliance artifact logic with canonical resolution

Implement a canonical artifact resolver.

Expected rule:
- if active designation exists and is valid, expected output path is exactly `doc/{DESIGNATION}SYSTEM.md`

Add or update compliance findings for:
- missing active designation
- invalid designation format
- missing `doc/system/`
- missing `doc/system/BUILD.sh`
- missing canonical output path
- legacy artifact detected
- missing universal structure
- missing class-aware required structure

Important:
- legacy artifacts may be reported
- legacy artifacts may support remediation planning
- legacy artifacts may **not** make the repo compliant

---

## Task C — Define the worktable-facing finding categories

The operator needs stable categories, not noise.

Ensure the backend/read-model/worktable can clearly distinguish at least:
- designation issue
- structure issue
- legacy migration issue
- build issue
- verification issue
- trust/execution blocked issue (if applicable)
- exception/override required issue (only if already supported cleanly)

The worktable must answer:
- what is wrong
- what can be fixed automatically
- what needs approval
- what still requires manual work

---

## Task D — Make remediation plans bounded and concrete

For this slice, remediation should be limited to bounded structural actions such as:
- create missing directories
- create missing stub files
- create/fix `doc/system/BUILD.sh`
- scaffold canonical doc structure
- rebuild
- verify

Do not let remediation invent large prose or fake architecture.
Do not let remediation overwrite authored material recklessly.

If an action is ambiguous or destructive, surface it as manual/operator-required instead of auto-applying it.

---

## Task E — Wire apply → rebuild → verify into one honest loop

Use the existing service/workflow substrate.

After approved apply:
- run repo-local build path
- verify the canonical output path
- classify result correctly
- persist apply and verify outcomes
- update worktable/read-model state

If apply succeeds but rebuild fails:
- do not mark compliant
- surface rebuild failure explicitly

If rebuild succeeds but canonical output path is wrong:
- do not mark compliant
- surface verification failure explicitly

---

## Task F — Make repo_state / read-model output useful for the worktable

The worktable/read-model should clearly expose:
- repo identity
- designation
- repo class
- compliance state
- blocking findings
- available remediation actions
- latest apply result
- latest verification result
- recommended next action

Do not bury this in raw event text.

---

## Task G — Keep the layer boundaries clean enough

Use this ownership split unless the code proves a better established pattern already exists:

- **compliance.rs** = pure rule evaluation / finding production
- **workflow.rs** = legal state transitions / execution outcome classification
- **service.rs** = orchestration of plan/apply/build/verify
- **repository.rs** = transactional persistence only
- **repo_state.rs** = derived operator/read-model shaping

Avoid moving more business rules into persistence.
Avoid making `service.rs` even more of a god object than necessary.

---

## Task H — Add or update tests before calling the slice done

You must add focused tests for at least:

### Compliance tests
- canonical output required when designation exists
- legacy output present but canonical output missing = not compliant
- missing BUILD.sh = finding
- missing required structure = finding

### Remediation/apply/verify tests
- one repo can go from missing structure → apply → rebuild → verify
- rebuild failure does not produce compliant status
- wrong output path does not produce compliant status

### Read-model/worktable tests
- derived state reflects blocking findings and next action correctly

Prefer narrow deterministic tests over broad vague tests.

---

## Deliverables expected from you

### 1. Code changes
Make the actual implementation changes.

### 2. File-by-file summary
For every changed file, explain briefly:
- why it changed
- what rule/behavior it now owns

### 3. Test proof
Show the exact commands you ran and their results.

Minimum expected:
- `cargo check --manifest-path src-tauri/Cargo.toml`
- targeted cargo tests for the new/changed registry logic

### 4. Risk notes
Call out anything still unresolved after this slice.

Do not pretend unresolved things are done.

---

## Definition of done

This slice is only done if all of the following are true:

- worktable-relevant findings are generated from canonical rules
- legacy artifacts no longer count as compliant success
- remediation plans are bounded and actionable
- apply/build/verify closes the loop for at least one repo path
- read-model/worktable state becomes meaningfully actionable
- tests cover the new canonical behavior
- `cargo check` passes

If any of those are missing, the slice is not done.

---

## Suggested execution order

1. map current worktable loop
2. refactor canonical compliance rules
3. update finding/remediation categories
4. wire apply/build/verify loop correctly
5. update repo_state/read-model output
6. add tests
7. run `cargo check` and targeted tests
8. summarize changed files and residual gaps

---

## Non-goals for this slice

Do not do these now:
- Forge_Library compilation
- full estate automation
- trust-model redesign across the whole ecosystem
- semantic code↔docs truth engine
- HQ integration
- broad UI redesign
- PostgreSQL runtime migration
- new large repo-class taxonomy expansion

This slice is about getting the **repo-level worktable from finding to fixing** working first.

---

## Final instruction

Be disciplined.
Use the existing Registry substrate.
Close the real loop.
Do not broaden scope.
Do not leave the operator with a pretty surface that still cannot take a repo from finding to verified fix.

