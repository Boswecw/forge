# V1 External Review Fold-In

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This document folds in the **supplemental strategic review themes** raised after the V1 planning pass, especially around:

- cascading hallucination prevention
- durable outbox hardening
- state drift control
- lifecycle freshness
- adversarial reconciliation

This is a fold-in document, not a replacement doctrine.

## 1. Cascading-hallucination control

### Concern
In multi-agent or multi-system correction architectures, one weak inference can become another system's assumed truth.

### V1 answer
The architecture already leans the right way because:
- Centipede is an evidence producer, not an execution authority
- DoppelCore is the truth-core, not the proposal executor
- Self-Healing approves but does not invent truth
- execution is downstream and bounded

### Additional V1 strengthening
Projection contracts should explicitly carry:
- `evidence_bundle_id`
- `confidence_posture`
- `operator_review_required`
- `blocked_reason`

This acts as a circuit breaker against unsupported correction flow.

## 2. Durable outbox hardening

### Concern
A simple exported/unexported status is too weak for high-discipline audit posture.

### V1 strengthening
The durable outbox should evolve toward a governed audit log with fields such as:
- projection payload hash
- producer identity
- producer version
- signing key id
- emitted_at
- consumed_at
- superseded_by
- delivery status
- consumer receipt reference

### Recommended posture
Treat the outbox as a **governed transport and evidence ledger**, not as a throwaway queue table.

## 3. State-drift control between Registry and Self-Healing

### Concern
Registry and Self-Healing can drift if one works from stale findings or stale truth artifacts.

### V1 strengthening
Every downstream artifact should be tied to a revision anchor and lifecycle controls such as:
- `revision_anchor`
- `valid_until`
- `superseded_by`
- `artifact_freshness_posture`

DoppelCore should be the source of artifact invalidation when a newer governed truth revision appears.

## 4. Freshness and TTL discipline

The plan should explicitly support lifecycle expiration for findings and proposals.

Recommended fields:
- `detected_at`
- `valid_until`
- `stale_after`
- `superseded_by`
- `invalidated_reason`

This prevents long-lived stale correction proposals from floating around as if they are still safe.

## 5. Signed or integrity-checked projections

Where practical, the system should support:
- payload hashing
- integrity verification
- producer-side signing or equivalent attestation

This is especially valuable if the outbox becomes the basis for broader audit posture later.

## 6. Adversarial reconciliation

A useful outside-the-box addition is a skeptical or adversarial review path.

Concept:
- one system produces the finding and evidence
- a second bounded review checks whether the evidence can be disproven, downgraded, or blocked
- only unresolved or reinforced findings move forward at higher confidence

This does not need to be a full "AI red team" in V1.
It can begin as a bounded contradiction or challenge lane.

## 7. V1 planning changes to adopt now

These are the best fold-in changes to adopt immediately:

1. make `revision_anchor` mandatory everywhere
2. add freshness fields such as `valid_until` and `superseded_by`
3. harden the durable outbox toward a governed audit posture
4. preserve contradiction bundles and negative evidence
5. keep proposal flow blocked when evidence posture is weak

## Bottom line

The V1 architecture is already pointed in the right direction.
The strongest fold-in is not to make it more complex.
It is to make the existing handoff artifacts:
- more integrity-aware
- more freshness-aware
- more contradiction-aware
- more resistant to unsupported proposal flow
