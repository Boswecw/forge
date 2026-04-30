# Canvas 06 — Opus Implementation Execution
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Translate the plan set into execution-ready instructions for Opus so implementation stays slice-based, proof-first, and repo-bounded.

---

## Global execution rules for Opus

Opus should follow these rules for this work:

1. do not redesign the architecture
2. do not expand to wave 2
3. treat PACT manifest truth as upstream-owned
4. implement one bounded slice at a time
5. every slice must include:
   - file list
   - apply instructions
   - verification command
   - expected success condition
6. do not proceed to the next slice until the current verification command passes
7. if proof fails, issue the smallest possible correction slice

---

## Repo execution order

1. PACT source truth confirmation
2. neuronforge local seam
3. NeuroForge cloud seam
4. ForgeCommand operator surface
5. cross-repo orchestrator proof
6. rollout/approval hardening

---

## Opus work package A — source truth confirmation

### Objective
Confirm the current PACT wave-1 package is the promotion source and collect exact artifacts needed by downstream repos.

### Deliverables
- manifest path and hash
- promotion packet path and version
- strict success hash
- non-strict digest map
- supported packet/profile matrix
- current repo gate report

### Proof
A single verification command that shows the source package is green.

---

## Opus work package B — neuronforge local seam

### Objective
Implement promotion carriage, compatibility classification, and run logging extension in neuronforge.

### Deliverables
- contract/model file(s)
- compatibility checker
- run logging extension
- one seam verification script
- one evidence markdown example

### Proof cases
- strict admitted
- non-strict admitted
- manifest missing
- digest mismatch
- lineage preserved

### Required output format from Opus
For each slice, provide:
- zip bundle or exact file replacements
- exact terminal commands
- exact verification command

---

## Opus work package C — NeuroForge cloud seam

### Objective
Mirror the promotion carriage model into the cloud intake and persistence lane.

### Deliverables
- intake schema or DTO changes
- persistence field additions
- compatibility gate
- cloud verification script
- cloud evidence example

### Proof cases
- compatible admitted intake
- blocked partial envelope
- blocked unsupported profile
- persisted lineage/provenance

---

## Opus work package D — ForgeCommand operator surface

### Objective
Expose promotion state, compatibility posture, and operator approval actions.

### Deliverables
- shared type definitions
- backend route or tauri command additions
- Svelte UI components/pages
- operator approval recording
- UI verification or route proof

### Proof cases
- strict vs non-strict visibly distinct
- mismatch visibly distinct
- blocked visibly distinct
- approval does not mutate manifest truth

---

## Opus work package E — cross-repo proof

### Objective
Create the cross-repo verification layer that proves the admitted manifest remains coherent across all connected repos.

### Deliverables
- orchestrator script
- compatibility report
- replay/admission comparison report
- rollback proof case

### Proof cases
- all repos compatible
- one repo mismatched
- rollback posture visible
- stale approval rejected

---

## Recommended Opus instruction block

Use this exact working posture:

> Implement the promotion integration work as bounded proof-first slices.  
> Treat PACT wave-1 manifest truth as upstream-owned and immutable within consumer repos.  
> Start with carriage and compatibility only.  
> Do not begin wave-2 design.  
> For each slice, provide exact files, exact apply commands, exact verification command, and expected passing output.  
> If a verification step fails, remain on the same slice and issue only the minimal correction needed.

---

## Done definition

This plan set is complete only when:

- PACT source package is confirmed green
- neuronforge seam is green
- NeuroForge intake seam is green
- ForgeCommand operator surface is green
- cross-repo proof script is green
- approval and rollback posture are visible and governed
