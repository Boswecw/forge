# Forge Implementation Pack 14 — Opus Run Order and Handoff Checklist

**Date:** 2026-04-04 01:35 America/New_York  
**Purpose:** Give VSCode Opus 4.6 a concrete repo-by-repo run order and handoff checklist so implementation starts in the correct sequence and stays narrow.

---

# 1. Run order rule

Opus must work in the order below.

If one stage is not complete enough to support the next, Opus must stop and report the exact blocking gap.

Do not jump ahead because later repo work feels more interesting.

---

# 2. Repo-by-repo run order

## Step 1 — create `forge-contract-core`

### Goal
Create the canonical shared contract center.

### Minimum handoff output
- repo scaffold exists
- shared envelope schema exists
- three admitted family schemas exist
- enum pack exists
- validator package exists
- fixture corpus exists
- gate runner exists
- docs exist

### Stop condition
Do not proceed to downstream repo work if contract-core is still partly conceptual.

---

## Step 2 — harden `dataforge-Local`

### Goal
Make DataForge Local capable of local artifact persistence, staging, queueing, reconciliation, dead-letter truth, and ForgeCommand read models.

### Minimum handoff output
- migrations exist
- local canonical artifact persistence exists
- staging table exists
- queue states exist
- lease behavior exists
- retry/dead-letter behavior exists
- read models exist
- tests exist
- docs no longer remain baseline-only for the proving slice

### Stop condition
Do not proceed to cloud integration if DataForge Local cannot truthfully manage local state first.

---

## Step 3 — harden `DataForge` cloud

### Goal
Add proving-slice intake, receipt, rejection, and duplicate reconciliation.

### Minimum handoff output
- intake route exists
- intake validation pipeline exists
- accepted shared storage exists
- receipt storage exists
- rejection storage exists
- duplicate reconciliation exists
- bounded reconciliation query exists
- tests exist
- docs reflect the new intake boundary

### Stop condition
Do not proceed to end-to-end transport if cloud acceptance/rejection truth is still weak.

---

## Step 4 — implement `Forge_Command` review slice

### Goal
Render truthful proving-slice queue/detail UX using real read models.

### Minimum handoff output
- queue route or pane exists
- detail view exists
- changed-since-last-view exists
- real data integration exists
- truthfulness tests exist
- docs reflect the route and scope

### Stop condition
Do not declare proving-slice success if the review surface still hides stale, blocked, rejected, or dead-letter truth.

---

## Step 5 — wire cross-repo gates

### Goal
Prove compatibility end to end.

### Minimum handoff output
- contract-core gate runner wired in first-wave repos
- scenario tests exist
- adversarial tests exist
- CI blocks on required failures
- test evidence is retained in reviewable form

### Stop condition
Do not widen scope while compatibility remains declarative instead of enforced.

---

# 3. Per-step Opus working checklist

For each repo step, Opus should complete the following checklist.

## 3.1 Inspect first
- inspect real repo layout
- identify real entry points
- identify persistence pattern
- identify test pattern
- identify doc assembly pattern

## 3.2 Fit implementation to reality
- use existing structure where sound
- avoid parallel shadow architecture
- name exact files to change or create

## 3.3 Implement narrow slice only
- no extra families
- no extra ownership
- no speculative platform work

## 3.4 Test immediately
- add or update tests with each slice
- do not leave testing to the end

## 3.5 Update docs immediately
- do not let SYSTEM docs lag behind code truth

---

# 4. Required Opus output format at each handoff

At the end of each repo step, Opus should produce a clean handoff summary containing:

1. files created
2. files changed
3. migrations added
4. routes added or changed
5. services added or changed
6. tests added
7. docs updated
8. scope explicitly excluded
9. remaining blockers

This keeps implementation reviewable and prevents hidden drift.

---

# 5. Allowed blockers Opus should report immediately

If encountered, Opus should stop and report blockers such as:
- repo structure too incomplete to place blueprint cleanly
- existing migration strategy unclear or conflicting
- read surface cannot be implemented honestly because upstream contract is missing
- baseline docs contradict real code shape materially
- contract-core semantics missing for required behavior

Opus should not silently “solve” these by inventing broad new architecture.

---

# 6. Definition of ready-to-hand-off by repo

## 6.1 Contract core ready
Only when schemas, validator, fixtures, role matrix, and gate runner are real.

## 6.2 DataForge Local ready
Only when local truth, staging, queue, reconciliation, dead-letter, and read models are real.

## 6.3 DataForge Cloud ready
Only when intake validation, receipts, rejections, and duplicate reconciliation are real.

## 6.4 ForgeCommand ready
Only when queue/detail/changed-since-last-view truthfulness is real.

## 6.5 Cross-repo proving slice ready
Only when required gates and scenario tests are passing.

---

# 7. Hard anti-rules for run order

Do not:
- start with ForgeCommand polish before contract/persistence truth exists
- start cloud intake before contract core exists
- start FA Local execution-family work during this proving wave
- widen to additional families before the first family is fully proven
- call a repo “done” while its docs still describe baseline placeholders

---

# 8. Final instruction to Opus

The correct implementation sequence is a discipline problem, not just a coding problem.

If Opus follows this order, the ecosystem gets a real proving slice.
If Opus skips the order, the ecosystem gets architecture drift wearing implementation clothes.

Implement in order. Prove each boundary. Then move.

