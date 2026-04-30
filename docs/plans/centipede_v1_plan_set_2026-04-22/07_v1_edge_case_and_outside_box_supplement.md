# V1 Edge Case and Outside-the-Box Supplement

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This supplement hardens the V1 plan with edge cases and non-obvious additions that improve:

- evidence richness
- exploitability-aware prioritization
- correction safety
- boundary discipline
- autonomous-worker calibration
- repository-shape handling

This supplement is additive.
It does not replace the V1 initial plan.

## High-value additions

### 1. Make Centipede outputs attestation-shaped
Centipede should emit structured attestation-style evidence bundles, not only loose issue records.

Recommended envelope contents:
- finding identity
- repository identity
- commit/tree/ref identity
- execution environment
- detector identity and version
- detector configuration hash
- observed artifact set
- confidence posture
- affected scope
- non-affected scope
- reproduction contract
- evidence payload list
- downstream consumer hints

This makes the evidence more useful to both Self-Healing and Registry.

### 2. Separate severity from exploitability
Add explicit fields such as:
- `exploitability_posture`
- `execution_reach`
- `trigger_requirements`
- `proof_type`

A severe issue with no reachable path should not always outrank a moderate issue that is actually reachable in production.

### 3. Make negative evidence first-class
Centipede should preserve what was checked and found not applicable.

Examples:
- scanned and not present
- dependency reachable but not exploitable under current conditions
- rule matched pattern but failed semantic threshold
- repo shape discovered but excluded by policy
- documentation truth surface present and current
- proposed correction candidate rejected by a gate

This reduces repeat work and prevents noisy re-proposals.

### 4. Add contradiction bundles
Centipede should preserve structured disagreement when truth surfaces conflict.

Examples:
- code says one thing, docs say another
- package graph says reachable, runtime config says disabled
- static detector says vulnerable path exists, exploitability evidence says not affected
- Registry says canonical structure exists, repo-shape scan says generated output is stale

Recommended contradiction bundle fields:
- `truth_surface_a`
- `truth_surface_b`
- `conflict_type`
- supporting evidence per side
- resolution recommendation
- operator review requirement

### 5. Build steady-state correction testing before autonomy expansion
Before deeper autonomous correction, test whether the full correction loop stays stable under disruptions.

Examples:
- proposal generated but proof harness unavailable
- proposal generated from stale repo snapshot
- fix passes tests but breaks doc truth rebuild
- multiple candidate corrections race the same target
- dependency vulnerability marked present but product posture says not affected
- Registry and Self-Healing disagree on truth owner

## Edge cases the architecture should explicitly absorb

### Repo-shape edge cases
Centipede should classify repository shape before deeper scanning.

Needed flags include:
- `monorepo_root`
- `nested_repo`
- `submodule`
- `linked_worktree`
- `sparse_checkout`
- `partial_clone`
- `generated_vendor_tree`
- `detached_snapshot`
- `archived_mirror`
- `intentionally_unmanaged_subtree`

Repo shape should be treated as a **phase zero classification**, not a late afterthought.

### Drift edge cases
Not all drift is the same.

Useful drift classes:
- syntactic drift
- structural drift
- semantic drift
- evidence drift
- provenance drift
- stale projection drift
- authority drift

Auto-proposal should remain limited to bounded drift classes.
Authority drift and provenance drift should usually escalate.

### Correction-safety edge cases
Even successful tests can hide risky corrections.

Checks should include:
- fix widens an authority boundary
- fix masks a symptom without removing the cause
- fix updates code but not truth surface
- fix changes a contract without Registry update
- fix resolves one contradiction by creating another
- fix passes local proof but breaks a cross-repo invariant

## Operating-model additions

### Provenance-oriented lineage
Model evidence as linked:
- entities
- activities
- agents

That gives a cleaner path from discovery to proposal to execution to proof.

### Dependency visibility separate from exploitability
For dependency-related issues, separate:
- component present
- component reachable
- vulnerability relevant
- vulnerability exploitable
- vulnerability observed in the product path

### Machine-readable posture outputs
Emit posture values like:
- `vulnerability_asserted`
- `affected`
- `not_affected`
- `under_investigation`
- `fixed`
- `mitigated_by_environment`
- `mitigated_by_configuration`
- `unreachable_code_path`

## Planning consequence

V1 should not only move evidence forward.
It should move **richer, contradiction-aware, posture-aware, provenance-rich evidence** forward.
