# V1 Initial Plan — Centipede, DoppelCore, and the Correction Fabric

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Plan position

This is the **initial implementation plan** for the architecture direction already established in the surrounding canvases.

The point of this phase is not to build the whole ecosystem.
The point is to **lock boundaries, define first artifacts, and constrain future implementation**.

## Goal

Create the first implementation-ready foundation for this architecture:

- **Centipede** produces findings and evidence
- **DoppelCore** becomes the truth-core and correction-ready artifact producer
- **Registry** consumes documentation and governed-truth projections
- **Self-Healing** consumes correction-oriented evidence and proposal inputs
- **forgeHQ / ForgeMath / forge-eval / eval-cal-node** form the correction-fabric proposal stack
- **FA-Local-Operator** executes approved local corrections
- **ForgeAgents** executes approved cloud corrections

## What this phase must accomplish

By the end of this phase, the system should have:

1. a frozen boundary doctrine
2. named upstream and downstream flows
3. first contract definitions for projection artifacts
4. a durable outbox model for Centipede projections
5. a clear split between Registry projections and Self-Healing projections
6. no authority confusion between truth, proposals, approval, and execution

## What this phase does not attempt yet

This phase does **not** attempt to fully implement:

- the complete DoppelCore repo
- the full correction-fabric runtime
- final execution automation
- final naming cleanup
- final UI polish
- final calibration-pack coverage

This is the phase for **structural lock and first governed contracts**.

## Architectural decisions to lock now

### 1. Centipede role
Centipede is a governed evidence and reconciliation producer.

It:
- produces findings
- produces evidence
- emits downstream projections

It does **not**:
- execute fixes
- become the top-level operator surface
- take ownership of documentation truth
- take ownership of proposal evaluation

### 2. DoppelCore role
DoppelCore is the truth-core.

It:
- normalizes governed findings
- produces truth-surface artifacts
- produces correction-ready artifacts
- carries lineage forward

It does **not**:
- execute fixes
- become a UI shell
- replace Registry
- replace Self-Healing

### 3. Registry role
Registry consumes governance, documentation, and truth-surface projections.

It should:
- reuse its existing worker/runtime model
- accept Centipede-fed work through a bounded intake adapter
- remain the governance/operator consumer for documentation truth

It should **not** become a second crawler.

### 4. Self-Healing role
Self-Healing consumes correction-oriented inputs.

It governs:
- review
- approval
- posture
- tracking
- downstream handoff to execution lanes

It does **not** define truth.

### 5. Execution role split
- **FA-Local-Operator** = approved local execution
- **ForgeAgents** = approved cloud execution

### 6. Correction-fabric role
The proposal stack sits between DoppelCore and execution:

- **forgeHQ**
- **ForgeMath**
- **forge-eval**
- **eval-cal-node**

These systems plan, score, evaluate, and calibrate correction proposals.
They are not the truth-core, and they are not the final execution authority.

## First artifact families

### High-priority outbound artifacts from Centipede
- `CentipedeSelfHealingProjection`
- `CentipedeRegistryProjection`

### Shared evidence-lineage primitives
- `EvidenceBundleRef`
- `RunProvenance`
- `SupportingLaneRef`
- `SupportingTraceRef`
- `RevisionAnchor`

### Named downstream follow-on artifacts
- `CorrectionOpportunity`
- `ProposalPacket`
- `ApprovedLocalExecutionPacket`
- `ApprovedCloudExecutionPacket`
- `ExecutionReceipt`

## Initial implementation slices

### Slice 1 — Boundary lock
Required outputs:
- boundary doctrine
- artifact boundary map
- role split table

Completion test:
You can state, on one page:
- who finds
- who normalizes truth
- who proposes
- who approves
- who executes

### Slice 2 — Projection contract definitions
Required outputs:
- `CentipedeSelfHealingProjection`
- `CentipedeRegistryProjection`
- shared evidence-lineage primitives

Completion test:
The contracts stand on their own without any UI discussion.

### Slice 3 — Durable outbox design
Required outputs:
- local persistence shape
- outbox lifecycle
- replay/retry posture
- provenance linkage to source runs

Recommended statuses:
- `pending`
- `exported`
- `consumed`
- `blocked`
- `failed`

Completion test:
A projection can exist durably before any consumer reads it.

### Slice 4 — Read/export surfaces
Required outputs:
- CLI reads
- optional backend reads
- lineage visibility
- run/repo/status filters

Completion test:
The projections are inspectable without a page-first workflow.

### Slice 5 — Registry intake adapter
Required outputs:
- Registry intake adapter
- governed-system resolution
- action-eligibility gate
- provenance attachment on worker jobs and receipts

Allowed outcomes:
- informational only
- enqueue compliance refresh
- enqueue proposal materialization
- enqueue missing-doc recheck / system refresh
- blocked due to unresolved identity or insufficient evidence

### Slice 6 — Self-Healing intake adapter
Required outputs:
- incident/proposal intake mapping
- support for evidence bundles
- support for lanes and traces
- explicit blocked posture when evidence is insufficient

Completion test:
Self-Healing shows Centipede-derived evidence, not just shallow summary counts.

## First success criteria

This phase is successful when all of the following are true:

1. Centipede emits two distinct projection types
2. those projections are durable and inspectable
3. Registry consumes its projection stream with provenance
4. Self-Healing consumes its projection stream with real evidence
5. no system silently crosses into another system's authority

## Immediate next move

Start with **Slice 1 and Slice 2 only**.

That means the next real work should be:

1. freeze the role and boundary doctrine
2. define the two outbound projection contracts
3. define shared evidence-lineage primitives

Do not jump to execution automation before those are real.
