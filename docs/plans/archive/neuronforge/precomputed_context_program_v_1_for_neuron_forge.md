# Precomputed Context Program V1 for NeuronForge

**Date:** 2026-04-15  
**Time:** America/New_York  
**Status:** Draft V1  
**Scope:** Governed precomputed-context subsystem for NeuronForge prompt execution, budget control, replayability, and longitudinal improvement.

## 1. Purpose

This plan defines the **precomputed context program** for NeuronForge.

The purpose is to stop NeuronForge from rebuilding all useful context at the exact moment of execution.

Instead, NeuronForge should be able to prepare, validate, cache, version, and reuse bounded context assets ahead of time.

This reduces:

- prompt-time latency
- token waste
- repeated assembly cost
- inconsistency across repeated runs
- avoidable retrieval drift

It improves:

- determinism
- replayability
- cost control
- prompt quality
- overnight comparison quality
- promotion safety

## 2. What precomputed context is

Precomputed context is **not** just a cache blob.

It is a governed asset class.

A precomputed context asset is a bounded, versioned, lineage-bearing artifact that NeuronForge may reuse during prompt assembly instead of recomputing the same supporting material from scratch.

## 3. Core rule

Precomputed context must never become hidden truth.

It is a support artifact for execution.
It is not canonical app truth.
It is not user-authority truth.
It is not a silent substitute for current source state.

Every precomputed context asset must remain:

- versioned
- attributable
- scope-bounded
- freshness-aware
- invalidation-aware
- replayable or replaceable

## 4. Why this program exists

Without a precomputed-context program, NeuronForge risks:

- rebuilding the same narrative windows over and over
- re-running expensive selection logic for identical requests
- prompt-size instability across repeated runs
- inconsistent context inclusion between baseline and challenger runs
- higher latency during local execution
- polluted overnight comparisons because the context bundle itself drifted between runs

A governed precomputed-context layer solves that.

## 5. Context asset classes

Start with a small, explicit set.

### 5.1 Scope window asset

A bounded text window or structured scene/chapter neighborhood prepared in advance for a known scope rule.

Examples:

- adjacent scene window
- prior scene summary window
- next scene support window
- chapter-local window

### 5.2 Deterministic summary asset

A summary derived through deterministic or highly bounded rules rather than ad hoc run-time improvisation.

Examples:

- chapter synopsis snapshot
- scene metadata rollup
- entity-presence rollup

### 5.3 Retrieval candidate set asset

A preselected set of ranked candidate records, excerpts, or support items prepared before prompt execution.

Examples:

- lore retrieval candidate set
- project-style reference set
- house-style rule candidate set

### 5.4 Constraint surface asset

A prebuilt bundle of constraints or policy material likely to recur.

Examples:

- house style rules
- project-specific suppression profile
- lane-specific evidence requirements

### 5.5 Budget planning asset

A precomputed estimate or bounded plan for section sizing.

Examples:

- narrative window budget plan
- packet section byte allocation
- fallback trimming sequence

## 6. What this layer must not do

It must not:

- silently replace current source truth without freshness checks
- pretend stale material is fresh
- blur authored truth with inferred support material
- bypass contract scope restrictions
- inject global context when the contract only allows local context
- hide invalidation events from execution telemetry

## 7. Lifecycle model

Every precomputed context asset should move through this lifecycle.

### Stage 1 — Build

The asset is created from allowed source material.

### Stage 2 — Validate

The asset is checked for schema shape, scope correctness, and freshness metadata.

### Stage 3 — Register

The asset receives an id, version, lineage, source references, and compatibility metadata.

### Stage 4 — Consume

PACT and prompt assembly may reference it during execution.

### Stage 5 — Invalidate or supersede

If source truth changes, policy changes, or asset-age rules expire, the asset is invalidated or superseded.

### Stage 6 — Retain for replay where appropriate

Historical runs may still reference the exact asset version used so overnight evidence remains interpretable.

## 8. Invalidation doctrine

Invalidation is one of the most important parts of this entire program.

A context asset should be invalidated when relevant:

- source text changed
- metadata changed
- contract scope rules changed
- ranking logic changed materially
- retrieval corpus changed materially
- policy or constraint surfaces changed materially
- freshness threshold expired
- compatibility with current packet schema no longer holds

An invalidated asset should never be silently treated as current.

## 9. Storage and truth posture

For serious use, the asset registry and the telemetry about asset usage should live in a **durable canonical persistent store** suitable for longitudinal comparison and overnight evidence history.

Do not treat throwaway local SQLite as the long-term learning memory for this program.

The system needs durable history for:

- asset lineage
- usage frequency
- invalidation reasons
- replay references
- baseline/challenger comparisons
- promotion evidence

## 10. Relationship to PACT

PACT does not replace precomputed context.

PACT packages and serializes the effective execution bundle.

The precomputed-context program produces reusable assets that PACT may reference or embed.

Simple relationship:

- precomputed context decides what reusable support artifacts exist
- PACT decides how those artifacts are carried in the governed execution packet

## 11. Relationship to prompt assembly

Prompt assembly should not query the whole world every time.

Instead, prompt assembly should prefer:

1. valid precomputed context asset
2. governed fallback build if asset missing or invalid
3. explicit degraded truth if neither safe path is available

This keeps prompt assembly leaner and more deterministic.

## 12. Telemetry requirements

When a precomputed context asset is used, telemetry should capture:

- asset id
- asset version
- asset class
- build timestamp
- source lineage
- freshness state
- invalidation state if relevant
- whether asset was embedded or referenced
- whether fallback rebuild occurred
- effect on budget if measurable

This is necessary for repeatable overnight evaluation.

## 13. Overnight learning use

The overnight system should be able to test context hypotheses such as:

- does a different scene-window shape improve continuity review?
- does a smaller support set improve schema compliance?
- does a stricter retrieval candidate set reduce noise?
- does a different trimming order preserve quality better under budget pressure?

That means context assets must be first-class challengable components.

But overnight shaping must never silently rewrite the live precomputed baseline.

It should:

- build challenger assets
- run comparisons
- score evidence
- recommend promotion or rejection
- preserve lineage to the exact asset versions used

## 14. Promotion posture

Only approved context assets should become promoted baseline assets for NeuronForge.

Promotion should occur through an explicit activation path, not by replacing files in place.

## 15. Recommended initial proving targets

Best first proving targets:

1. adjacent-scene continuity window asset
2. scene-local beat extraction support window asset
3. lore-safe reference candidate set asset
4. prompt-budget trimming plan asset

These are high-value and bounded enough to govern well.

## 16. Phase sequence

### Phase 0 — Asset vocabulary lock

Define allowed asset classes, state vocabulary, invalidation reasons, and lineage fields.

### Phase 1 — Registry and schema lock

Define the schema for context assets, invalidation events, and consumption telemetry.

### Phase 2 — Builder services

Implement deterministic builders for the first approved asset classes.

### Phase 3 — PACT linkage

Allow PACT packets to include references to or embedded forms of approved assets.

### Phase 4 — Prompt assembly consumption

Require prompt assembly to prefer valid precomputed assets where contract rules allow.

### Phase 5 — Telemetry and replay

Persist asset-usage truth for replay and overnight comparison.

### Phase 6 — Overnight challenger loop

Allow bounded challenger asset variants to be tested against baseline assets.

## 17. Immediate next actions

1. Lock the NeuronForge precomputed-context asset vocabulary.
2. Define the minimum lineage and freshness fields every asset must carry.
3. Define invalidation reason codes.
4. Pick the first two asset classes to implement.
5. Define how PACT references an asset versus embedding it.
6. Define the canonical persistent store for asset registry and usage history.
7. Define promotion and rollback rules for baseline context assets.

## 18. Working definition

**The NeuronForge precomputed-context program is the governed system for preparing, versioning, validating, reusing, invalidating, and promoting bounded support artifacts so prompt execution becomes faster, cheaper, more deterministic, and more evaluable over time.**