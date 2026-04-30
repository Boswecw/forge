# NeuronForge Prompt Stack Master Plan V1

**Date:** 2026-04-15  
**Time:** America/New_York  
**Status:** Draft V1  
**Scope:** Internal NeuronForge prompt-system architecture for governed prompt construction, packetization, execution, telemetry, and improvement over time.

## 1. Purpose

This plan defines the full prompt-system stack for **NeuronForge**.

The goal is not to let prompts exist as scattered lane files, hidden strings, or app-specific one-offs.

The goal is to make prompting a governed subsystem with:

- contract-first execution
- reusable prompt assembly
- precomputed context support
- PACT-based packet construction
- route-aware delivery
- telemetry capture
- overnight evidence-building
- controlled baseline improvement over time

This is an internal business system plan.
It is not an MVP plan.

## 2. Executive model

The NeuronForge prompt stack should be treated as a layered control system.

It has four primary layers:

1. **Task Contract Layer**  
   Defines what is being requested, what inputs are legal, what outputs are allowed, and what degraded truth must be emitted.

2. **Precomputed Context Layer**  
   Builds and stores reusable context assets ahead of execution so prompt-time assembly is faster, cheaper, and more deterministic.

3. **PACT Runtime Layer**  
   Serializes the effective request into a governed packet with budgets, hashes, provenance, and portability posture.

4. **Prompt Assembly and Execution Layer**  
   Builds the final model-facing prompt bundle from contracts, profiles, context assets, and packet rules, then dispatches execution through NeuronForge route policy.

These are distinct layers.
They work together.
They must not be collapsed into one giant “prompt builder.”

## 3. Core rule

In NeuronForge, the caller should depend on:

- contract id
- contract version
- lane binding where applicable
- runtime guarantees
- packet class
- response envelope truth

The caller should **not** depend on:

- hidden raw prompt text
- model-specific formatting hacks
- app-specific one-off prompt structure
- undocumented context inclusion behavior

Prompt text is an implementation layer behind governed contracts.

## 4. System outcome

The stack should let NeuronForge do this cleanly:

**request -> contract resolution -> context selection -> PACT packet build -> prompt assembly -> route execution -> candidate output -> telemetry -> overnight comparison -> governed improvement**

That is the whole point.

## 5. Prompt stack layers

### 5.1 Contract layer

This layer owns:

- task family
- contract id and version
- required inputs
- optional inputs
- allowed evidence surfaces
- allowed supporting context scope
- output schema
- degraded-mode rules
- provenance requirements

This layer answers: **what is being asked?**

### 5.2 Prompt profile layer

This layer owns:

- instruction posture
- model-family compatibility
- tone/strictness for execution
- reasoning restraint rules
- schema-compliance rules
- evidence citation posture inside the response format
- extraction vs analysis vs transformation framing

This layer answers: **how should the contract be expressed to the model class?**

### 5.3 Precomputed context layer

This layer owns:

- reusable context artifacts
- deterministic context slices
- cached retrieval results
- prebuilt summaries
- scope-aware narrative windows
- context invalidation rules
- freshness and lineage

This layer answers: **what supporting material can be prepared before runtime?**

### 5.4 PACT packet layer

This layer owns:

- packet shape
- serialization contract
- token/size budgets
- section ordering
- hashing
- signatures where applicable
- portability class
- replayability
- evidence attachment references

This layer answers: **what exact bounded bundle is being handed to prompt assembly and execution?**

### 5.5 Prompt assembly layer

This layer owns:

- final bundle composition
- section stitching order
- contract instructions
- profile instructions
- context insertion
- packet envelope materialization
- route-aware rendering where needed

This layer answers: **what exact model-facing bundle gets emitted right now?**

### 5.6 Execution layer

This layer owns:

- route-class enforcement
- model/profile execution
- degraded-mode truth
- response envelope truth
- model id
- route class requested vs actual
- timing and warnings

This layer answers: **what actually ran?**

### 5.7 Telemetry and learning layer

This layer owns:

- execution telemetry
- packet stats
- prompt variant lineage
- validation outcomes
- scoring outcomes
- regression findings
- overnight challenger comparisons
- recommendation artifacts

This layer answers: **did this actually improve anything?**

## 6. Architectural split

### NeuronForge owns

- contract-driven prompt execution
- profile resolution
- context assembly intake
- PACT packet intake and validation
- prompt assembly
- route enforcement
- execution telemetry emission
- candidate output generation

### ForgeCommand owns

- operator review surfaces
- overnight run orchestration
- comparison review
- recommendation packaging
- approval and activation control
- trust/readiness posture

### Canonical persistent store owns

- run history
- telemetry history
- packet manifests
- score history
- recommendation history
- activation history
- promoted baseline history

For learning history and longitudinal improvement, use a **canonical persistent store**, not throwaway local SQLite as the long-term truth surface.

## 7. Prompt improvement doctrine

The stack must support improvement over time, but that improvement must be governed.

NeuronForge must not “self-improve” by mutating live prompt assets in place.

Instead:

1. candidate prompt/profile/context changes are created
2. those changes are run against frozen evals and bounded overnight batches
3. telemetry and scoring are captured
4. comparisons are reviewed
5. approved changes become promoted baseline assets
6. the next run uses the newly activated baseline

That keeps the learning loop real without turning it into uncontrolled self-modification.

## 8. Telemetry requirements

Every meaningful prompt execution should emit enough telemetry to support later comparison.

Minimum telemetry should include:

- run id
- contract id
- contract version
- lane id if bound
- profile id and version
- packet id and version
- context asset ids and versions
- route class requested
- route class actual
- model id
- degraded mode
- model swap indicator if relevant
- latency
- token or byte budget usage
- validation outcome
- score outcome when evaluated
- recommendation link if part of overnight shaping

Without this telemetry, the system cannot actually learn in a governed way.

## 9. Overnight learning relationship

Overnight shaping should be the main controlled improvement engine for the NeuronForge prompt stack.

Overnight shaping should test:

- prompt profile variants
- context assembly variants
- packet composition variants
- ordering changes
- pruning rules
- route-policy hypotheses
- threshold changes where allowed

Overnight shaping should not:

- silently rewrite live baseline prompts
- auto-promote itself
- become hidden training
- become a generic free-running research agent

It builds evidence.
The operator decides what advances.

## 10. Phase sequence

### Phase 0 — Contract and vocabulary lock

Lock:

- prompt asset vocabulary
- profile vocabulary
- packet classes
- context asset classes
- telemetry vocabulary
- promotion vocabulary

### Phase 1 — Prompt asset registry

Create governed registries for:

- contracts
- prompt profiles
- packet templates
- context asset definitions
- lane bindings

### Phase 2 — Precomputed context integration

Teach the stack to consume valid precomputed context assets instead of assembling everything at request time.

### Phase 3 — PACT runtime integration

Require packet construction before final prompt assembly for governed execution paths.

### Phase 4 — Telemetry and replay

Persist execution and packet telemetry with enough fidelity to support replay, comparison, and evidence review.

### Phase 5 — Overnight comparison loop

Run bounded overnight evaluations against baseline and challenger combinations.

### Phase 6 — Promotion path

Allow approved prompt-stack assets to become promoted baseline assets through explicit activation only.

## 11. Immediate next actions

1. Lock NeuronForge prompt-stack vocabulary.
2. Define the asset types that count as promotable prompt-stack components.
3. Lock the relationship between contract, precomputed context, and PACT packet.
4. Define the minimum telemetry envelope for every governed execution.
5. Define which prompt-stack elements overnight shaping is allowed to challenge first.
6. Decide the canonical persistent store for long-run telemetry and recommendation history.
7. Define the baseline activation path for promoted prompt-stack assets.

## 12. Working definition

**The NeuronForge prompt stack is the governed control system that turns contracts, profiles, precomputed context, and PACT packets into route-aware model executions with replayable telemetry and evidence-driven improvement over time.**