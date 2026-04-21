# 01. Architecture and Authority Boundaries

**Date:** 2026-04-17  
**Time:** America/New_York

## Objective

Define the exact architecture and ownership boundaries for connecting ForgeCommand to DataForge Local for local systems analytics and information.

## System roles

### ForgeCommand
ForgeCommand is the **single-operator control surface**.
It owns:

- operator-facing analytics pages
- operator posture language
- route organization
- degraded/stale/offline presentation
- app-owned proxy routes
- export/review surfaces if added later

ForgeCommand does **not** own:

- raw analytics SQL
- aggregation logic
- local systems analytics storage semantics
- direct UI access to DataForge Local

### DataForge Local
DataForge Local is the **local systems analytics and information substrate**.
It owns:

- local analytics computation
- local systems inventory read models
- queue posture computation
- freshness/staleness computation
- derived summary models for ForgeCommand
- bounded local information staging

DataForge Local does **not** own:

- operator UX
- direct operator approval UX
- canonical long-lived business truth for the entire ecosystem
- cloud coordination logic inside this Phase 1 scope

### DataForge Cloud
DataForge Cloud is **not** the main actor in this first local analytics lane.
Its role is deferred to later phases when:

- information must outlive the machine/runtime
- local summaries need durable persistence elsewhere
- ecosystem-wide rollups are required

## Topology

```text
ForgeCommand UI (Svelte)
        │
        │ typed fetch
        ▼
ForgeCommand Axum API (:8004)
        │
        │ localhost-only proxy / contract boundary
        ▼
DataForge Local FastAPI (:8005)
        │
        │ analytics service layer / read-model computation
        ▼
Local PostgreSQL runtime storage
```

## Authority rules

### Rule 1 — UI never talks directly to DataForge Local
All UI traffic goes through ForgeCommand-owned routes.

### Rule 2 — Analytics are read-only
No write verbs in analytics routes.
Action/remediation routes must be separate if they exist later.

### Rule 3 — Derived is not canonical
All analytics surfaces must be explicitly marked derived.

### Rule 4 — Freshness is mandatory
No analytics payload may exist without freshness metadata.

### Rule 5 — No fake green state
If upstream is unavailable, stale, or inconsistent, ForgeCommand must surface degraded truth.

## Phase 1 scope boundary

Phase 1 is strictly:

- systems overview
- systems inventory/posture
- queue posture summary
- freshness posture summary

Phase 1 excludes:

- artifact deep-dive analytics
- long-history trend analytics
- remediation commands
- multi-machine federation
- cloud sync orchestration
- multi-user roles/permissions

## Local systems covered by this plan

This plan assumes DataForge Local may report on these local systems when present:

- ForgeCommand
- DataForge Local
- NeuronForge Local
- FA Local
- Cortex
- future governed local subsystems

## Architectural risks to guard against

### Risk: ForgeCommand becoming a second data platform
Mitigation: keep analytics storage and aggregation in DataForge Local.

### Risk: DataForge Local becoming a generic orchestrator
Mitigation: keep it limited to analytics/information/read-model ownership.

### Risk: hidden trust-boundary drift
Mitigation: all traffic stays behind app-owned Axum routes.

### Risk: stale data presented as healthy
Mitigation: freshness contract is mandatory and fail-closed.

## Architectural completion criteria

This architecture is considered correctly implemented only when:

- all local analytics traffic is proxied through ForgeCommand
- DataForge Local returns read-only derived payloads
- UI renders explicit degraded/stale/offline posture
- no direct frontend dependency on DataForge Local exists
- contract ownership is clear and testable

