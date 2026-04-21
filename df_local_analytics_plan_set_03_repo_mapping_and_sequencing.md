# 03. Repository Mapping and Implementation Sequencing

**Date:** 2026-04-17  
**Time:** America/New_York

## Objective

Map the local-systems analytics plan into real repo ownership and a bounded implementation sequence.

## Repo ownership

### DataForge Local repo owns

- FastAPI analytics routes
- analytics service layer
- analytics response models
- any derived query/read-model logic
- queue freshness/system posture computation
- associated backend tests

### ForgeCommand repo owns

- Axum proxy routes
- proxy client/service integration
- frontend types
- frontend data loading layer
- analytics pages
- UI posture rendering
- associated proxy/frontend tests

## Recommended file destinations

## DataForge Local

```text
app/
  api/
    analytics_router.py
  analytics/
    models.py
    services/
      overview.py
      systems.py
      queue.py
      freshness.py
  tests/
    analytics/
      test_overview.py
      test_systems.py
      test_queue.py
      test_freshness.py
```

## ForgeCommand

```text
src-tauri/
  src/
    api/
      routes/
        local_analytics.rs
    clients/
      dataforge_local.rs

src/
  lib/
    types/
      local-analytics.ts
    server/
      local-analytics.ts
  routes/
    local/
      analytics/
        +page.svelte
        systems/
          +page.svelte
        queue/
          +page.svelte
        freshness/
          +page.svelte

tests/
  local-analytics/
```

## Slice sequence

## Slice 0 — contract lock

Deliverables:

- endpoint names locked
- response fields locked
- enum vocabulary locked
- repo destinations locked

Proof:

- contract plan approved as implementation source

## Slice 1 — DataForge Local analytics scaffold

Deliverables:

- analytics router added
- models added
- stub services added
- health/basic wiring working

Proof:

- backend starts
- endpoints return typed stub payloads
- unit tests pass for stub contract shape

## Slice 2 — ForgeCommand proxy layer

Deliverables:

- Axum proxy routes added
- DataForge Local client added
- proxy error mapping added

Proof:

- ForgeCommand can retrieve all four contract payloads through proxy routes
- upstream failures map to degraded truth

## Slice 3 — ForgeCommand overview page

Deliverables:

- `/local/analytics` page
- overview cards
- posture summary band
- degraded banner behavior

Proof:

- page renders valid overview data
- stale/degraded states render correctly

## Slice 4 — systems / queue / freshness pages

Deliverables:

- systems page
- queue page
- freshness page
- typed view-model mapping

Proof:

- all pages render correctly from live or mocked data
- no direct calls to DataForge Local from the UI

## Slice 5 — hardening and verification

Deliverables:

- schema mismatch handling
- offline behavior
- fail-closed rules
- stronger tests

Proof:

- mismatch and offline scenarios behave correctly
- verification checklist passes end-to-end

## Sequencing rules

- do not build UI before contracts are locked
- do not add deeper analytics domains before overview/systems/queue/freshness are proven
- do not add write actions in the analytics namespace
- do not combine Phase 1 with later artifact analytics

## Change-control rules

Any change to endpoint names, enums, or envelope fields requires:

- contract update in plan docs
- model updates in both repos
- test updates in both repos
- explicit verification rerun

## Slice completion rule

A slice is complete only when:

- files are in the correct repo
- tests for that slice pass
- runtime proof exists
- failure posture for the slice is known
- next slice does not rely on guessed behavior

