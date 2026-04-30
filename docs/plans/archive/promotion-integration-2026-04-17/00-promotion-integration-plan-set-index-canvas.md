# Promotion Integration Plan Set — Index
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

This canvas set is the initial implementation package for promoting the proved PACT TOON wave-1 work into the next repo seams:

- `Boswecw/neuronforge`
- NeuroForge cloud lane
- ForgeCommand operator/control-plane lane

The plan assumes the PACT wave-1 package is already proved and treated as the upstream source of serialization truth, replay truth, and admission evidence.

---

## Why this plan starts here

PACT already proved the bounded wave-1 shape:
- serialization boundary
- rendering/fallback doctrine
- observability
- repo gate
- extension governance
- promotion packet
- replay matrix
- strict and non-strict digest locks
- wave-1 manifest

The next step is **not** “add more TOON features.”
The next step is **promote only the already-proved wave-1 truth** into the consumer seams without allowing the consuming repos to redefine packet meaning, rendering meaning, or evidence meaning.

That means the next repos become:
- carriers of promotion metadata
- bounded consumers of admission truth
- bounded producers of operator evidence
- not alternate serialization authorities

---

## Canvas Set Contents

1. `01-promotion-contract-and-admission-model-canvas.md`
   - locks what gets promoted out of PACT
   - defines canonical truth ownership
   - defines admissible vs non-admissible fields

2. `02-neuronforge-and-neuroforge-seam-implementation-canvas.md`
   - defines the inference/runtime seam
   - defines what neuronforge/neuroforge must accept, preserve, and emit
   - defines repo tasks and boundaries

3. `03-forgecommand-operator-control-plane-canvas.md`
   - defines the operator surface
   - defines what ForgeCommand shows vs what it never invents
   - defines review/approval posture

4. `04-proof-gates-repo-map-and-evidence-canvas.md`
   - defines tests, fixtures, proof sequence, and file ownership
   - defines cross-repo evidence requirements

5. `05-rollout-security-and-governance-canvas.md`
   - defines staged admission
   - defines promotion safety
   - defines rollback and drift handling

6. `06-opus-implementation-execution-canvas.md`
   - turns the plan set into repo-by-repo Opus execution instructions
   - keeps the work sliceable and proof-first

---

## Execution Order

Use the canvases in this order:

1. Canvas 01
2. Canvas 02
3. Canvas 03
4. Canvas 04
5. Canvas 05
6. Canvas 06

---

## Initial decision lock

Before implementation begins, lock these decisions:

- PACT remains the upstream authority for TOON wave-1 serialization rules
- neuronforge/neuroforge do not define alternate rendering rules
- ForgeCommand does not generate promotion truth; it only displays, compares, and governs it
- admission to later waves requires a new promotion packet and new proof gates
- promotion work must stay copy/paste-slice friendly
