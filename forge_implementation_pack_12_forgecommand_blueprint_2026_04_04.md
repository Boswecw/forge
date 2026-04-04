# Forge Implementation Pack 12 — ForgeCommand Implementation Blueprint

**Date:** 2026-04-04 01:34 America/New_York  
**Purpose:** Give VSCode Opus 4.6 an implementation-ready blueprint for building the first proving-slice operator review surface inside ForgeCommand.

---

# 1. Mission

Implement a calm, truthful proving-slice review surface in ForgeCommand for:

**queue visibility -> detail visibility -> lifecycle understanding -> changed-since-last-view awareness**

This is not an execution console.
This is not a recommendation cockpit.
This is not a generic new dashboard.

It is a narrow operator review slice.

---

# 2. Real ForgeCommand fit

This blueprint must be implemented inside the real ForgeCommand architecture:
- desktop UI in `src/`
- Rust Tauri runtime in `src-tauri/`
- orchestrator/Axum surfaces where appropriate
- existing control-plane posture and evidence-oriented UX

Opus must not build a parallel fake UI architecture for this slice.

---

# 3. First implementation tasks Opus should perform

## Task 1 — identify the right existing route and surface placement
Opus should inspect the real ForgeCommand app and decide where the proving-slice review route belongs in the existing information architecture.

## Task 2 — define typed frontend view models
Add typed queue row and detail view models based on the proving-slice read-model contract.

## Task 3 — implement queue route and components
Build the first proving-slice queue surface.

## Task 4 — implement detail panel / route
Build the first proving-slice detail surface.

## Task 5 — implement changed-since-last-view behavior
Add operator memory-reduction behavior.

## Task 6 — wire real read-model APIs
Connect to DataForge Local / shared status surfaces using the actual ForgeCommand data-fetching patterns.

## Task 7 — add tests and docs
Verify truthfulness and document the slice.

---

# 4. Queue implementation requirements

## 4.1 Required sections
The queue must render:
1. Needs attention now
2. Retrying / awaiting reconciliation
3. Dead-letter / blocked
4. Recently changed
5. Informational / background

## 4.2 Required queue row fields
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

## 4.3 Grouping rule
Rows representing repeated near-identical findings should be grouped when contract-compatible.

## 4.4 Anti-spam rule
Do not flood the queue with duplicate retry noise or informational clutter in the attention lanes.

---

# 5. Detail implementation requirements

## 5.1 First screenful must answer
- what is wrong
- which system is affected
- what evidence supports it
- what remains uncertain
- what the current transport state is

## 5.2 Required sections in order
1. summary header
2. evidence summary block
3. references block
4. contradiction / uncertainty block if applicable later
5. promotion lifecycle block
6. rejection or dead-letter reason block
7. audit/change history summary

## 5.3 Promotion lifecycle states to render
- staged
- retrying
- awaiting reconciliation
- accepted
- rejected
- dead-lettered

Each state must have plain-language explanation.

---

# 6. Minimal proving-slice actions

Allowed first-slice actions:
- refresh
- inspect references
- mark reviewed
- view latest state change

Not allowed in this slice:
- approve
- deny for execution
- execute
- rollback
- recommendation acceptance workflows

Opus must keep the action model narrow.

---

# 7. Changed-since-last-view behavior

## 7.1 Must track at least
- promotion state changed
- receipt arrived
- rejection reason changed
- dead-letter entered or cleared
- staleness changed

## 7.2 UX rule
Use calm emphasis, not noisy alerts.

## 7.3 Persistence rule
Fit this behavior into the real ForgeCommand local state/store strategy rather than inventing a detached memory mechanism.

---

# 8. Truthfulness rules Opus must enforce in UI

## 8.1 Accepted looks accepted

## 8.2 Retrying looks retrying

## 8.3 Rejected looks rejected

## 8.4 Dead-letter looks dead-lettered

## 8.5 Stale or unknown must not look resolved

## 8.6 Restricted payloads must not be overexposed

## 8.7 Color-only signaling is forbidden

---

# 9. Data integration requirements

ForgeCommand should consume:
- DataForge Local queue/detail read models
- DataForge Cloud shared receipt/status truth where required
- contract-core vocabulary-backed state semantics

It must not invent lifecycle semantics in the UI to compensate for missing upstream truth.

---

# 10. Suggested implementation slices

## Slice A — typed models and mock contract-accurate UI state
Build the queue/detail components first against contract-accurate local mock data.

## Slice B — queue layout and grouping
Implement the queue sections and row grouping behavior.

## Slice C — detail layout and lifecycle rendering
Implement the detail structure and plain-language lifecycle explanations.

## Slice D — changed-since-last-view
Add calm operator memory-reduction signals.

## Slice E — data integration
Wire actual read-model APIs.

## Slice F — truthfulness hardening
Add tests for stale/blocked/rejected/dead-letter/restricted rendering behavior.

---

# 11. Required tests Opus must add

## 11.1 Component tests
- queue row renders all required fields
- grouping logic behaves correctly
- detail view sections render in correct order
- lifecycle block explains state in plain language

## 11.2 State tests
- accepted item renders as accepted
- retrying item renders as retrying
- rejected item renders as rejected
- dead-letter item renders as dead-lettered
- stale item cannot look resolved
- restricted item does not overexpose content

## 11.3 Workflow tests
- changed-since-last-view indicator appears on meaningful state change
- operator can understand item status without opening raw logs

---

# 12. Required documentation updates

Opus must update ForgeCommand docs to include:
- proving-slice route placement
- queue model
- detail model
- state vocabulary
- changed-since-last-view behavior
- review-first narrow scope

---

# 13. Anti-scope statement for Opus

Do not:
- widen this into generic operational dashboard work
- add execution workflows
- add recommendation approval UI
- add contradiction resolution UI beyond what proving-slice read models actually support
- treat visual polish as more important than truthfulness

The success condition is honest state communication, not UI breadth.

---

# 14. Implementation completion checklist

Opus should not declare this blueprint complete until:
- queue sections exist
- detail sections exist
- changed-since-last-view exists
- real data integration exists
- truthfulness tests pass
- docs reflect the real route and behavior

If the UI looks polished but still hides stale, blocked, or dead-letter truth, it is not complete.

