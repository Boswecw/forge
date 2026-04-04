# Forge Plan Set 05 — ForgeCommand Proving-Slice Review UX Plan

**Date:** 2026-04-04 01:19 America/New_York  
**Purpose:** Define the first truthful operator review surface inside ForgeCommand for proving slice 01, using ForgeCommand’s real role as the control-plane and review system.

---

# 1. UX mission

ForgeCommand must provide the first proving-slice operator workflow for:

**issue detected -> evidence inspected -> transport state understood -> current posture understood -> follow-through observed**

The first proving slice is not an action-heavy dashboard.
It is a calm, truthful review surface for a single operator.

---

# 2. Hard UX doctrine

## 2.1 Calm review over noise
Prioritize:
- what needs attention now
- what is blocked
- what is retrying
- what is dead-lettered
- what changed since the last review

## 2.2 Unknown remains explicit
The surface must distinguish:
- known
- inferred
- stale
- insufficient evidence
- pending reconciliation
- rejected
- dead-lettered

## 2.3 Single-operator burden is a hard constraint
The operator must not have to reconstruct truth from:
- multiple routes
- logs
- memory
- raw transport traces

## 2.4 Review first, action later
The proving slice should remain review-oriented.
Do not prematurely turn it into an execution or approval cockpit.

---

# 3. Queue model

## 3.1 Required queue sections
1. **Needs attention now**
2. **Retrying / awaiting reconciliation**
3. **Dead-letter / blocked**
4. **Recently changed**
5. **Informational / background**

## 3.2 Queue row required fields
- `system_id`
- `issue_summary`
- `artifact_family`
- `drift_class`
- `promotion_state`
- `confidence_posture`
- `created_at`
- `last_state_change_at`
- `staleness_posture`
- `changed_since_last_view`

## 3.3 Grouping rule
Group repeated near-identical rows when all of the following match:
- same `system_id`
- same `drift_class`
- same declared/observed truth pair or equivalent signature
- same effective promotion state bucket

## 3.4 Anti-spam rules
Do not show separate top-level rows for:
- near-identical repeated findings already grouped
- low-value informational noise in attention lanes
- stale retry churn with no meaningful state change

---

# 4. Detail view model

## 4.1 First screenful must answer
- what is wrong
- what system is affected
- what evidence supports it
- what is still uncertain
- what transport state it is in

## 4.2 Required detail sections in order
1. summary header
2. evidence summary block
3. reference block
4. contradiction / uncertainty block when applicable later
5. promotion lifecycle block
6. rejection or dead-letter reason block when applicable
7. audit/change history summary

## 4.3 Required summary header fields
- issue title
- target system / scope
- confidence posture
- staleness posture
- promotion lifecycle state
- concise explanation line

---

# 5. Promotion lifecycle presentation

## 5.1 States that must be visible
- staged
- retrying
- awaiting reconciliation
- accepted
- rejected
- dead-lettered

## 5.2 Rule
Each state must have plain-language explanation, not badge-only language.

## 5.3 Anti-rule
Do not rely on color alone to convey transport truth.

---

# 6. Decision-readiness posture for proving slice 01

The first slice should not jump to full recommendation/approval UX.

## 6.1 Required proving-slice posture states
- `informational_review`
- `needs_followup`
- `blocked_transport`
- `resolved_shared`

These are view/posture states, not approval or execution states.

## 6.2 Minimal first-slice actions
Allowed:
- refresh
- inspect references
- mark reviewed
- view latest state change

Not yet allowed:
- approve
- reject for execution
- execute
- rollback

---

# 7. Changed-since-last-view behavior

## 7.1 Required tracked changes
Each item should support visibility for:
- promotion state changed
- accepted receipt arrived
- rejection reason changed
- dead-letter entered or cleared
- staleness state changed

## 7.2 Queue indicator rule
Rows with meaningful changes should receive calm emphasis, not loud alert styling.

## 7.3 Single-operator memory rule
This feature is mandatory because the system is single-operator and should reduce memory tax directly.

---

# 8. Dead-letter workflow

## 8.1 Required queue behavior
Dead-letter items must appear in their own lane with:
- reason class
- oldest age
- affected system
- attempt count

## 8.2 Required detail behavior
The detail view must show:
- why automatic retry stopped
- what the last failure class was
- whether operator intervention is required
- whether retry later is possible

## 8.3 Anti-rule
Dead-letter items may not be flattened into ordinary retrying items.

---

# 9. Truthfulness rules

## 9.1 Stale rule
If evidence or derived state is stale, show that before any optimistic-looking state treatment.

## 9.2 Inconclusive rule
If reconciliation is incomplete, say so plainly.

## 9.3 Restricted visibility rule
Restricted payloads must not be broadly rendered in queue summaries or ordinary detail surfaces.

## 9.4 Derived read-model rule
ForgeCommand must consume canonical read models or canonical APIs only. It must not invent lifecycle truth unsupported by source artifacts.

---

# 10. Accessibility and interaction

## 10.1 Minimum requirements
- full keyboard navigation
- visible focus states
- semantic headings
- text labels on badges
- no color-only truth signaling

## 10.2 Interaction rule
The proving slice should feel disciplined and calm, not animated or flashy.

---

# 11. Data dependencies

ForgeCommand’s proving-slice review UX depends on:
- DataForge Local queue/detail read models
- DataForge Cloud receipt/rejection/shared-status truth
- contract-core vocabulary for lifecycle and posture semantics

ForgeCommand should not compensate for weak upstream truth by inventing UI semantics.

---

# 12. Implementation slices inside ForgeCommand

## Slice A — queue skeleton
Build queue sections and row posture against mock-but-contract-accurate data.

## Slice B — detail skeleton
Build ordered detail sections and plain-language lifecycle rendering.

## Slice C — changed-since-last-view
Add operator memory-reduction behavior.

## Slice D — read-model integration
Wire real DataForge Local / Cloud read-model inputs.

## Slice E — truthfulness hardening
Verify stale, blocked, rejected, dead-letter, and restricted states render honestly.

---

# 13. Verification plan

## 13.1 Required UI truthfulness tests
- accepted item looks accepted
- retrying item looks retrying
- rejected item looks rejected
- dead-letter item looks dead-lettered
- stale item does not look resolved
- restricted payload is not overexposed

## 13.2 Workflow tests
- queue grouping reduces noise
- changed-since-last-view indicator works
- detail shows lifecycle without route hunting
- operator can understand item state without raw logs

---

# 14. Exit criteria

The ForgeCommand proving-slice review surface is ready only when:
- queue sections are implemented
- detail sections are implemented
- transport state is plainly explained
- changed-since-last-view materially reduces memory burden
- dead-letter detail is truthful and useful
- stale/blocked/restricted states are highly legible
- verification gates pass

Until then, no broader operator workflow should be declared complete.

