# 04. UI, Operator Workflow, and Analytics Surfaces

**Date:** 2026-04-17  
**Time:** America/New_York

## Objective

Define the operator-facing UX for local systems analytics inside ForgeCommand.

## UX doctrine

This is an **operator truth surface**, not a vanity dashboard.
The UI must optimize for:

- trust
- clarity
- degradation visibility
- low cognitive overhead for a single operator
- fast recognition of what needs attention

## Page set

### `/local/analytics`
Top-level landing page.

Sections:

- posture summary band
- systems summary cards
- queue summary cards
- freshness summary cards
- degradation flags panel
- quick links into drill-down pages

### `/local/analytics/systems`
Shows all local systems and their posture.

Columns/fields:

- system name
- role
- enabled state
- operational status
- freshness posture
- last OK time
- last error time
- endpoint/info notes

### `/local/analytics/queue`
Shows the queue operational surface.

Sections:

- counts by status
- stale lease warnings
- oldest item age
- average dwell time
- queue degradation notes

### `/local/analytics/freshness`
Shows trust and source age.

Sections:

- overall freshness band
- source-by-source age list
- stale/aging sources
- degraded reason text where present

## UI posture vocabulary

### System health labels

- Healthy
- Degraded
- Offline
- Unknown

### Freshness labels

- Fresh
- Aging
- Stale
- Unknown

## UI rendering rules

### Rule 1 — degraded truth must be obvious
A stale or degraded state must be impossible to miss.

### Rule 2 — unknown is not healthy
Unknown must render as its own posture.

### Rule 3 — timestamps must be visible
The operator needs to see when data was computed and how old it is.

### Rule 4 — no decorative ambiguity
Avoid vague green/yellow states without explicit labels.

### Rule 5 — summary first, detail second
The landing page should tell the operator what matters before requiring drill-down.

## Interaction model

The primary operator loop is:

1. open `/local/analytics`
2. scan posture summary band
3. identify degraded/stale/offline posture
4. drill into systems, queue, or freshness page
5. decide whether deeper remediation work is needed elsewhere

## Phase 1 UX exclusions

Phase 1 should not include:

- custom charting for the sake of charting
- deep historical analytics graphs
- remediation action buttons
- approval workflow buttons
- multi-operator collaboration features

## Accessibility and readability rules

- labels must be explicit, not icon-only
- state should never be color-only
- timestamps should be human-readable
- pages should be readable at a glance
- copy should use controlled operational vocabulary

## UX completion criteria

The UX is acceptable only when:

- the landing page immediately reveals current posture
- drill-down pages do not invent business logic beyond the contract
- stale/degraded/offline states are unambiguous
- the single-operator workflow feels lighter, not heavier

