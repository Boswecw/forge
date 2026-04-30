# 05. Verification, Operations, and Governance

**Date:** 2026-04-17  
**Time:** America/New_York

## Objective

Define the verification posture, runtime expectations, and governance controls for the ForgeCommand ↔ DataForge Local local-systems analytics lane.

## Verification doctrine

Nothing in this plan is considered complete because the UI renders.
A slice is only complete when:

- contracts match in both repos
- runtime proof exists
- degraded/offline behavior is known
- test coverage proves success and failure posture

## Required test layers

### DataForge Local backend tests

Must cover:

- overview response shape
- systems response shape
- queue response shape
- freshness response shape
- freshness threshold logic
- stale lease logic
- unknown/missing timestamp handling
- schema version behavior

### ForgeCommand backend/proxy tests

Must cover:

- proxy route success cases
- upstream timeout cases
- upstream unavailable cases
- malformed upstream payload cases
- schema mismatch cases
- degraded response mapping

### ForgeCommand frontend tests

Must cover:

- overview page render
- systems page render
- queue page render
- freshness page render
- degraded/offline/stale/unknown rendering
- no direct UI dependency on DataForge Local

## Manual proof checklist

1. start DataForge Local
2. start ForgeCommand
3. load `/local/analytics`
4. verify overview values render correctly
5. verify systems page values render correctly
6. verify queue page values render correctly
7. verify freshness page values render correctly
8. stop DataForge Local
9. verify ForgeCommand shows degraded truth
10. restore DataForge Local
11. verify freshness recovers honestly

## Runtime guardrails

### Guardrail 1 — localhost only
DataForge Local remains local.

### Guardrail 2 — fail closed on schema mismatch
Do not silently accept mismatched contracts.

### Guardrail 3 — no silent green state
If upstream is absent or malformed, UI must not imply health.

### Guardrail 4 — freshness is operationally meaningful
Freshness thresholds must be configured and tested.

## Operational configuration

### DataForge Local

Recommended config:

- analytics enabled flag
- freshness threshold seconds
- queue stale-lease threshold seconds
- endpoint binding config

### ForgeCommand

Recommended config:

- DataForge Local URL
- timeout ms
- analytics enabled flag
- optional polling interval if polling is added later

## Governance rules

Any change to this lane requires review when it affects:

- endpoint names
- response envelope
- enum vocabulary
- freshness rules
- failure posture
- page route structure

## Change categories

### Low-risk changes

- copy adjustments
- non-contract visual refinements
- layout improvements that do not change semantics

### Medium-risk changes

- adding fields to responses
- adding new drill-down pages
- threshold tuning with verification updates

### High-risk changes

- changing enum values
- renaming endpoints
- changing envelope shape
- changing fail-closed behavior
- adding write actions into analytics namespace

## Operational readiness criteria

This lane is operationally ready only when:

- all four endpoints work end-to-end
- proxy and UI surfaces are typed and stable
- degraded/offline behavior is explicit
- thresholds are documented
- both repos have verification for contract integrity
- no part of the operator flow depends on hidden assumptions

## Future-phase governance notes

Later phases may add:

- artifact analytics
- historical trend windows
- export packet generation
- cloud persistence hooks

But those must be separate follow-on plans, not silent scope creep inside Phase 1.

