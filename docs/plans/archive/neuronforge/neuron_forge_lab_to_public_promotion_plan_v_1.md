# NeuronForge Lab to Public Promotion Plan V1

**Date:** 2026-04-15  
**Time:** America/New_York  
**Status:** Draft V1  
**Scope:** Controlled promotion path from internal lab NeuronForge improvements into public-app NeuronForge runtimes.

## 1. Purpose

This plan defines how improvements proven inside your internal **lab NeuronForge** become safe, installable improvements for **public-app NeuronForge runtimes**.

The goal is not to sync your live lab state directly into public applications.

The goal is to turn proven lab improvements into governed, signed, versioned baseline assets that public NeuronForge runtimes can verify, stage, activate, and roll back safely.

## 2. The three operating zones

### 2.1 Lab NeuronForge

This is your internal proving ground.
It is where you test:

- contracts
- prompt profiles
- packet rules
- context assets
- route policies
- thresholds
- degradation policies
- model pairings
- regression packs

### 2.2 Public-app NeuronForge runtime

This is the NeuronForge runtime bundled into public-facing applications such as AuthorForge.

This runtime must be stable, upgradeable, and overlay-safe.

### 2.3 Optional external consumers

Some promoted artifacts may later be reusable by other approved runtimes or cloud-side systems, but that is secondary.

The primary bridge in this plan is:

**Lab NeuronForge -> promoted baseline assets -> public-app NeuronForge runtime**

## 3. Main rule

Lab NeuronForge must **not** push its live internal state directly into public applications.

Instead, lab NeuronForge must publish controlled baseline assets.

Public-app NeuronForge runtimes must consume those assets as a vendor baseline layer.

## 4. Runtime layering model

Every public-app NeuronForge runtime should have three layers.

### Layer 1 — Runtime defaults

Shipped code and built-in fallback behavior.

### Layer 2 — Vendor baseline

Approved promoted assets from lab NeuronForge.
This is where official improvements live.

### Layer 3 — User and project overlay

User-owned and project-owned local state.
Examples:

- user preferences
- project overrides
- local dictionaries
- suppression rules
- custom profiles
- local tuning
- project-local style settings

## 5. Precedence law

The precedence law must be:

**User and Project Overlay**  
overrides **Vendor Baseline**  
overrides **Runtime Defaults**

This is the heart of the promotion plan.

It lets public runtimes improve without wiping out user-local ownership.

## 6. What lab NeuronForge actually promotes

Lab NeuronForge is usually not promoting “the whole system.”

Most of the time it is promoting specific improvement assets such as:

- contract packs
- prompt/profile packs
- PACT packet packs
- context assembly packs
- route policy packs
- quality/scoring packs
- degradation policy packs
- model compatibility packs
- evaluation corpus additions
- telemetry-informed threshold improvements

Actual model or adapter artifacts are a separate promotion class and should be governed separately.

## 7. Promotion asset classes

At minimum, define these classes.

### 7.1 Contract Pack

Contracts, schemas, and structured output rules.

### 7.2 Prompt and Profile Pack

Approved prompt fragments, profile behavior, and model-family notes.

### 7.3 Context Assembly Pack

Precomputed-context and assembly rules, pruning rules, selection rules, and related logic.

### 7.4 PACT Runtime Pack

Packet schema, section rules, budget rules, trimming rules, and serialization behavior.

### 7.5 Route Policy Pack

Route mappings, hardware-tier posture, fallback policy.

### 7.6 Quality and Scoring Pack

Thresholds, regression gate rules, score posture.

### 7.7 Degradation Policy Pack

Fail-closed behavior, degraded-mode rules, posture reasons.

### 7.8 Model Compatibility Pack

Supported model families, hardware requirements, quantization posture, adapter compatibility.

### 7.9 Model or Adapter Pack

Optional separate class for real model-level improvements.

## 8. Manifest requirement

Every promoted asset or bundle needs a formal manifest.

Minimum manifest fields should include:

- asset or pack id
- asset or pack type
- version
- release channel
- created at
- created by
- source lab build id
- compatible runtime versions
- compatible app versions
- compatible hardware tiers
- compatible model families
- requires migration
- rollback supported
- content hash
- signature
- evidence bundle id
- eval corpus version
- regression status
- notes

## 9. Release channels

Define three release channels.

### Stable

Default public channel.

### Beta

Opt-in public testing.

### Experimental

Internal or tightly bounded testing only.

Public runtimes must never silently move users from stable to beta or experimental.

## 10. Promotion pipeline

### Step 1 — Lab proving

A candidate improvement is tested in lab NeuronForge using frozen evals, telemetry review, degradation checks, and regression checks.

### Step 2 — Packaging

If it proves out, it is frozen into one or more promoted baseline assets with manifests and evidence attached.

### Step 3 — Review

ForgeCommand or an equivalent trust surface reviews compatibility, regression posture, portability, and rollback readiness.

### Step 4 — Approval

If approved, the asset becomes an official candidate for publication.

### Step 5 — Publication

The approved asset is published to the canonical release location.

### Step 6 — Installation

The public-app NeuronForge runtime detects, verifies, stages, and activates the new baseline asset.

### Step 7 — Rollback safety

If activation fails, the runtime rolls back to the previous baseline asset without damaging user or project overlays.

## 11. What the public runtime must do

The public-app NeuronForge runtime must be able to:

- detect available baseline updates
- verify signatures and compatibility
- enforce release-channel rules
- stage updates before switching active baseline
- preserve all user and project overlays
- keep rollback pointers
- surface bounded installation failure reasons
- record activation success or failure truthfully

## 12. What must never be overwritten

Vendor baseline updates must not overwrite user-local state unless an explicit migration rule says so.

Do not overwrite:

- user preferences
- project-local overrides
- user dictionaries
- suppression rules
- project tuning
- custom style settings
- user-local history

The vendor baseline is your official improvement layer.
It is not the owner of the user’s machine.

## 13. Portability classes

Every promoted improvement should be classified as one of these:

- local runtime portable
- cloud portable
- both portable
- lab only

This prevents accidental leakage of lab-only or local-only assumptions into the wrong target.

## 14. Telemetry and longitudinal improvement

Promotion should be informed by durable telemetry over many runs, not by a one-off win.

That means the system should preserve longitudinal evidence such as:

- repeated overnight comparisons
- stability across runs
- regression frequency
- degradation frequency
- hardware-tier behavior
- activation success rate
- rollback frequency
- operator approval history

For this to work, promotion history and telemetry history should live in a durable canonical persistent store suitable for long-run learning.

## 15. Relationship to overnight shaping

Overnight shaping is the evidence engine for this promotion path.

It should test candidate assets over several overnight runs and package recommendations.

It must not directly publish or activate public baselines by itself.

It builds evidence.
ForgeCommand review and approval decide promotion.

## 16. Phase sequence

### Phase 0 — Vocabulary and schema lock

Lock pack types, manifest fields, release channels, portability classes, precedence law, and signature rules.

### Phase 1 — Lab export

Teach lab NeuronForge to export promotion-ready assets with evidence attached.

### Phase 2 — Review and approval

Wire review, approval, rejection, and publication through ForgeCommand or equivalent control surface.

### Phase 3 — Public runtime installer

Teach public-app NeuronForge runtimes to verify, stage, activate, and roll back promoted baseline assets safely.

### Phase 4 — Longitudinal telemetry loop

Collect enough activation and usage telemetry to judge whether promoted assets actually remain better over time.

### Phase 5 — Optional broader reuse

Allow explicitly portable approved artifacts to be reused by other approved runtimes.

## 17. Immediate next actions

1. Lock the NeuronForge promotion asset vocabulary.
2. Define the baseline asset manifest schema.
3. Lock the precedence law.
4. Decide the canonical publication location.
5. Decide bundle strategy: one signed bundle versus multiple coordinated assets.
6. Define portability classes and release-channel rules.
7. Define rollback requirements before installer work begins.
8. Choose the first proving target asset class.

## 18. Working definition

**The NeuronForge lab-to-public promotion system is the governed bridge that turns proven internal improvements into signed, versioned baseline assets that public-app NeuronForge runtimes can safely verify, install, activate, observe, and roll back without violating user-local ownership.**

