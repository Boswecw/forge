# PACT V1 Runtime Plan for NeuronForge

**Date:** 2026-04-15  
**Time:** America/New_York  
**Status:** Draft V1  
**Scope:** Runtime plan for using PACT inside NeuronForge as the governed packetization and serialization layer for prompt execution, replay, budgets, telemetry, and promotion.

## 1. Purpose

This plan defines how **PACT** should function inside **NeuronForge**.

PACT is not the same thing as NeuronForge.

NeuronForge is the governed local execution and routing substrate.
PACT is the packet and serialization system that prepares bounded execution bundles for NeuronForge to run.

PACT exists to make prompt execution:

- bounded
- serializable
- hashable
- budget-aware
- replayable
- portable where allowed
- inspectable
- evaluable over time

## 2. Core role of PACT

PACT should sit between:

- contract resolution
- precomputed context selection
- final prompt assembly and execution

PACT takes the effective request ingredients and turns them into a governed packet.

That packet becomes the official input bundle for a NeuronForge execution event.

## 3. What PACT is responsible for

PACT should own:

- packet schema
- section vocabulary
- ordering law
- serialization rules
- budget surfaces
- trimming doctrine
- content hashing
- signature hooks where applicable
- portability classification
- packet manifest truth
- replay compatibility

PACT should not own:

- lane trust decisions
- model inference semantics
- operator approvals
- baseline promotion by itself
- canonical app truth

## 4. Why this layer matters

Without PACT, NeuronForge risks falling back into:

- ad hoc prompt assembly
- inconsistent section ordering
- hidden inclusion/exclusion behavior
- weak replayability
- budget drift across repeated runs
- poor overnight comparability

PACT fixes that by making the prompt bundle a governed artifact rather than a temporary string.

## 5. Packet model

A PACT packet should be a structured execution bundle composed from approved sections.

At minimum, a packet may contain:

- request envelope
- contract metadata
- lane binding metadata where applicable
- profile metadata
- precomputed context references or embedded sections
- constraints and guardrails
- user/project overlay material where allowed
- packet budget metadata
- provenance metadata
- compatibility metadata

The exact final model-facing prompt may be derived from this packet, but the packet itself is the first-class governed artifact.

## 6. Section doctrine

Each packet section should be typed.

Start with explicit section classes such as:

- `request_header`
- `contract_rules`
- `profile_instructions`
- `context_support`
- `constraints`
- `schema_requirements`
- `degraded_mode_notice`
- `response_shape`
- `provenance_footer`

Do not allow arbitrary unnamed sections in governed paths.

## 7. Budget doctrine

PACT must enforce budget truth.

Budgeting should exist before final execution, not after the fact.

Minimum budget surfaces should include:

- total packet budget
- per-section budget
- reserved response budget where applicable
- trimming order
- hard-stop conditions
- degrade-allowed fallback rules

This is critical for local execution, especially on writer-laptop and midrange hardware.

## 8. Trimming doctrine

When a packet exceeds budget, PACT should not improvise.

It should follow a locked trimming order.

That order should be contract-aware and class-aware.

Example posture:

1. drop lowest-priority optional support sections
2. reduce support-window size
3. reduce auxiliary notes
4. fall back to preapproved compact context asset
5. emit degraded-mode truth if required material no longer fits safely

PACT must never silently trim required contract-critical sections.

## 9. Hashing and signatures

Every governed packet should carry enough integrity data to support later review.

Minimum integrity fields should include:

- packet id
- packet version
- packet hash
- section hashes or equivalent integrity detail where justified
- build timestamp
- builder id or source component
- compatibility version markers

Where promotion or distribution matters, signature support should exist at the manifest layer.

## 10. Portability doctrine

Not every packet is equally portable.

PACT should classify packet portability explicitly.

Suggested classes:

- local-only
- lab-only
- app-runtime-portable
- cross-runtime-portable
- cloud-portable

This matters because some packet contents may depend on local-only assumptions, private overlays, or lab-only artifacts.

## 11. Relationship to precomputed context

PACT should support both:

- embedding precomputed context directly into the packet
- referencing a registered precomputed context asset by id/version

The choice should be explicit.

Use embedding when replay simplicity matters.
Use referencing when reuse and storage efficiency matter and the referenced asset is durably retrievable.

## 12. Relationship to prompt assembly

Prompt assembly should consume a PACT packet, not loose ingredients.

That means the assembly layer should know:

- which sections are present
- which version of each section class is present
- what trimming already occurred
- what degraded posture, if any, already exists

This keeps final prompt rendering controlled and inspectable.

## 13. Telemetry requirements

Each packetized execution should emit telemetry including:

- packet id
- packet version
- portability class
- embedded asset ids if present
- referenced asset ids if present
- budget requested
- budget used
- trimming actions taken
- degraded mode due to budget or not
- route class requested
- route class actual
- contract id/version
- model id
- validation result

This is required for honest overnight comparison.

## 14. Overnight learning use

PACT should be one of the main challengable surfaces in overnight shaping.

The overnight system should be able to test:

- alternate section orders
- alternate budget allocations
- alternate trimming rules
- compact versus full packet shapes
- embedded versus referenced context posture
- packet class differences per contract family

But it must do so through bounded challenger packets, never by rewriting live packet templates in place.

## 15. Persistent truth posture

For longitudinal learning and promotion history, packet manifests, telemetry, validation outcomes, and recommendation lineage should live in a durable canonical persistent store.

Do not treat temporary SQLite state as the long-term truth surface for NeuronForge packet learning.

## 16. Promotion posture

Approved packet templates, section-order rules, budget rules, and trimming rules should become promoted baseline PACT assets.

They should be versioned and activated explicitly.

Rollback must be possible.

## 17. Phase sequence

### Phase 0 — Schema and vocabulary lock

Lock packet schema, section vocabulary, portability classes, and budget vocabulary.

### Phase 1 — Packet builder core

Implement builder logic for a small set of governed contract families.

### Phase 2 — Budget and trimming engine

Implement deterministic budget enforcement and trimming order.

### Phase 3 — Prompt assembly integration

Require governed prompt execution to consume PACT-built packets.

### Phase 4 — Telemetry and replay

Persist packet telemetry and support packet replay for overnight evidence work.

### Phase 5 — Overnight challenger support

Allow baseline and challenger packet variants to be compared.

### Phase 6 — Promotion and rollback

Allow approved packet assets to become active baseline packet configurations.

## 18. Immediate next actions

1. Lock the PACT packet schema for NeuronForge.
2. Define the first approved section classes.
3. Define budget surfaces and trimming order.
4. Decide when embedding is required versus allowed referencing.
5. Define portability classes and their rules.
6. Define packet telemetry minimums.
7. Define baseline activation and rollback for PACT assets.

## 19. Working definition

**PACT in NeuronForge is the governed packetization layer that turns resolved execution ingredients into bounded, hashable, budget-aware, replayable packets that prompt assembly and routing ca