# V1 Initial Execution Order

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This file turns the V1 planning set into a practical order of work.

It is intentionally biased toward **boundary lock and artifact contracts first**.

## Phase 0 — Freeze architecture posture

### Objective
Stop accidental scope drift before more implementation expands the wrong seams.

### Outputs
- approve the role split
- approve the system-boundary diagram
- approve the Centipede feeding posture
- approve DoppelCore standalone placement

### Exit condition
You can describe the architecture clearly without blurring:
- truth
- proposal
- approval
- execution

## Phase 1 — Define first contracts

### Objective
Make Centipede's downstream outputs real.

### Outputs
- `CentipedeSelfHealingProjection`
- `CentipedeRegistryProjection`
- shared evidence-lineage primitives
- required lifecycle fields:
  - `revision_anchor`
  - `produced_at`
  - `valid_until`
  - `superseded_by`
  - `confidence_posture`

### Exit condition
The contracts stand on their own without needing UI screenshots or implementation excuses.

## Phase 2 — Harden evidence structure

### Objective
Ensure Centipede emits rich enough evidence to support both Registry and Self-Healing.

### Outputs
- attestation-style evidence envelope
- contradiction bundle shape
- negative evidence shape
- exploitability posture fields
- repo-shape classification fields

### Exit condition
A consumer can distinguish:
- what is wrong
- what was checked and not wrong
- what truth surfaces disagree
- how fresh and how trustworthy the finding is

## Phase 3 — Build durable outbox

### Objective
Persist outbound projections before building automated consumers.

### Outputs
- durable projection storage
- lifecycle statuses
- retry and replay posture
- integrity fields
- consumer receipt linkage

### Suggested statuses
- `pending`
- `exported`
- `consumed`
- `blocked`
- `failed`
- `superseded`

### Exit condition
A projection can be created, inspected, retried, superseded, and traced without any downstream consumer running.

## Phase 4 — Add read and debug surfaces

### Objective
Make the data inspectable.

### Outputs
- CLI reads
- optional backend reads
- filters by run, repo, revision, status
- lineage inspection
- contradiction inspection

### Exit condition
You can inspect V1 artifacts without needing a page-first workflow.

## Phase 5 — Registry intake adapter

### Objective
Feed Registry first through a bounded intake path.

### Why Registry first
Registry already has a more mature worker/runtime substrate and can reuse it with less churn.

### Outputs
- Registry intake adapter
- governed-system resolution
- action-eligibility gate
- provenance-aware worker jobs
- provenance-aware receipts

### Exit condition
Registry accepts Centipede-fed work without becoming a second crawler.

## Phase 6 — Self-Healing evidence adapter

### Objective
Improve Self-Healing now using current Centipede evidence.

### Outputs
- evidence adapter from current run detail, lane admissions, and decision traces
- storage for raw evidence plus normalized digests
- evidence display inside incident surfaces

### Exit condition
Self-Healing stops using Centipede as only a shallow queue signal.

## Phase 7 — Self-Healing projection intake

### Objective
Upgrade Self-Healing from current-evidence adapter to formal projection intake.

### Outputs
- incident mapping from `CentipedeSelfHealingProjection`
- proposal-candidate mapping
- blocked posture for insufficient evidence
- review posture wiring

### Exit condition
Self-Healing can hold evidence-backed incidents and proposal candidates without collapsing them into the same object.

## Phase 8 — DoppelCore repo initiation

### Objective
Start DoppelCore as a real internal ecosystem component.

### Outputs
- repo scaffold
- schema ownership boundary
- truth-record definitions
- proof-obligation definitions
- evaluation-packet definitions

### Exit condition
DoppelCore is real enough to own the truth-core contracts even if the entire runtime is not finished yet.

## Phase 9 — Correction-fabric hookup

### Objective
Feed downstream proposal systems from DoppelCore outputs.

### Outputs
- correction-opportunity handoff
- scoring inputs
- evaluation packets
- calibration hooks

### Exit condition
Proposal generation begins downstream of truth, not upstream of it.

## Phase 10 — Execution-lane integration

### Objective
Connect approved proposals to bounded local and cloud execution.

### Outputs
- approved local execution packet for FA-Local-Operator
- approved cloud execution packet for ForgeAgents
- execution receipts
- post-change verification
- re-crawl triggers

### Exit condition
State mutation stays downstream of approval and can be traced back to evidence, truth, proposal, and approval.

## Best immediate move

The very next real implementation move should still be:

1. boundary lock
2. projection contracts
3. evidence-lineage primitives
4. durable outbox shape

That is the cleanest starting tranche for V1.
