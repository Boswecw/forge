# V1 Integration Plan — Centipede Feeding Registry and Self-Healing

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This plan locks the integration posture so **Centipede feeds Registry and Self-Healing** without becoming a competing top-level authority surface.

## Current conclusion

Centipede should become a producer of **two distinct downstream projection streams**:

1. **Self-Healing projection stream**
2. **Registry projection stream**

These streams may share evidence lineage, but they are **not the same payload**.

They have:
- different consumers
- different action semantics
- different authority boundaries

## Why this split is necessary

### Registry posture
Registry is documentation and governed-truth focused.

It needs payloads that answer questions like:
- what governed system is affected
- what truth surface drifted
- what claim target mismatched
- whether this is action-eligible for worker/runtime flows

### Self-Healing posture
Self-Healing is correction and proposal governance focused.

It needs payloads that answer questions like:
- what finding is fix-relevant
- what evidence supports action
- whether proposal generation is allowed
- whether operator review is required before any downstream mutation

## Contract split

### A. `CentipedeSelfHealingProjection`
Purpose: describe fix-relevant findings that may become incidents or proposal candidates.

Minimum fields:
- `projection_id`
- `source_run_id`
- `repository_id`
- `revision_anchor`
- `run_class`
- `finding_id`
- `finding_class`
- `severity`
- `confidence_posture`
- `affected_target_type`
- `affected_target_key`
- `evidence_bundle_id`
- `supporting_lane_ids`
- `supporting_trace_ids`
- `suggested_remediation_kind`
- `proposal_required`
- `operator_review_required`
- `blocked_reason`
- `produced_at`

### B. `CentipedeRegistryProjection`
Purpose: describe documentation, governance, and truth-surface findings that may trigger Registry workflows.

Minimum fields:
- `projection_id`
- `source_run_id`
- `repository_id`
- `governed_system_id`
- `revision_anchor`
- `mismatch_class`
- `claim_target_type`
- `claim_target_key`
- `documentation_surface_kind`
- `truth_posture`
- `drift_status`
- `evidence_bundle_id`
- `supporting_lane_ids`
- `supporting_trace_ids`
- `suggested_registry_action`
- `requires_system_resolution`
- `operator_review_required`
- `produced_at`

## Registry-specific requirements

Registry should **not** directly "run Centipede" as a second crawler.
Instead, it should receive **Centipede-originated projections** through a bounded intake adapter that can:

1. resolve repository to governed-system identity when possible
2. decide whether the projection is informative or action-eligible
3. enqueue existing Registry worker jobs where appropriate

### Best refactor posture for Registry
Do not build a second autonomous worker.
Refactor the existing worker/runtime to accept **upstream evidence-fed jobs**.

### Recommended additions
- new initiator/source classification for Centipede-fed work
- upstream evidence fields on queued worker jobs and receipts
- explicit linkage from Registry job and receipt records back to:
  - `source_run_id`
  - `projection_id`
  - `evidence_bundle_id`

## Preferred Registry flow

1. Centipede emits `CentipedeRegistryProjection` into a durable outbox.
2. Registry intake adapter reads new projections.
3. Registry resolves repository and governed-system linkage.
4. Registry decides one of these outcomes:
   - informational only
   - enqueue compliance refresh
   - enqueue proposal materialization
   - enqueue missing-doc recheck / system refresh
   - block due to unresolved identity or insufficient evidence
5. Registry worker runs existing job types with Centipede provenance attached.

## Self-Healing-specific requirements

Self-Healing needs a deeper contract than "run exists."

It needs finding-level evidence packages that can become:
- incident queue items
- proposal candidates
- blocked incidents when evidence is insufficient

## Preferred Self-Healing flow

1. Centipede emits `CentipedeSelfHealingProjection` into a durable outbox.
2. Self-Healing intake adapter turns those records into normalized incidents or proposal candidates.
3. Self-Healing UI shows Centipede evidence inside its existing incident and proposal surfaces.
4. Any mutation stays downstream of approval and execution boundaries.

## Refactor recommendation

### Registry
Yes, likely a **small but important refactor** is needed.
This is not a redesign.

### Self-Healing
Yes, more than Registry.
Self-Healing is currently closer to a coarse run-signal consumer and needs a real projection intake contract.

## UI direction

Centipede should **not** remain a primary page-first destination.
The preferred posture is:

- expose Centipede-derived evidence **inside Self-Healing**
- expose Centipede-derived governance/truth projections **inside Registry**
- keep `/centipede` only as a **debug / calibration / diagnostics surface** if it remains at all

## Implementation order

1. add the two projection contracts
2. add shared lineage primitives
3. add durable outbox persistence
4. add CLI and read surfaces
5. add Registry intake adapter
6. add Self-Healing intake adapter
7. consolidate UI so Centipede becomes downstream-fed rather than top-level
