# Canvas 02 — neuronforge and NeuroForge Seam Implementation
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Define how the next promotion seam should be implemented for `Boswecw/neuronforge` and the NeuroForge cloud lane without letting those repos become alternate serialization authorities.

---

## Current posture to respect

The current public `Boswecw/neuronforge` README describes the repo as a **local-first experiment workspace** centered on controlled proofreading evaluation, explicit run logging, manual validation, baseline tracking, and controlled operational discipline. It also states the current posture is **manual-first** and **verification-heavy** rather than a broad general-purpose model lab. fileciteturn102file0

The workflow doc shows a baseline loop built around inputs, prompts, manual model runs, saved outputs, run registry entries, notes, and evaluations. fileciteturn105file0

That means the first integration wave must preserve:
- explicit run logging
- manual review posture
- baseline discipline
- separation between execution and acceptance

---

## Seam objective

Add promotion-aware intake and evidence carriage into neuronforge / NeuroForge so that a run can prove:

- which admitted PACT wave it relied on
- whether the run was strict-admitted or non-strict-admitted
- whether the context lineage fields survived intact
- whether the runtime output can be associated to a valid promotion manifest

This seam is about **governed intake and provenance**, not about handing TOON rendering authority to neuronforge / NeuroForge.

---

## Wave 1 target behavior

For an eligible promoted request, neuronforge / NeuroForge should:

1. accept a bounded promotion envelope
2. validate envelope compatibility against a local checked-in manifest mirror or cached trusted copy
3. preserve `task_intent_id`, `context_bundle_id`, and `context_bundle_hash`
4. record requested vs used serialization profile
5. record strict success hash or non-strict canonical digest as applicable
6. emit a run record showing admission class
7. refuse “promotion present” claims when the evidence is incomplete or incompatible

---

## Repo tasks — neuronforge local lane

### Slice NF-01 — contract carriage
Add a bounded request model or run metadata model that can carry:

- promotion manifest hash
- promotion packet version
- strict success hash
- non-strict digest
- requested profile
- used profile
- artifact kind
- fallback flags/reason
- context lineage identifiers

Success condition:
- request or run record can store the full promotion envelope without inference-time loss

### Slice NF-02 — compatibility checker
Add a small compatibility module that checks:

- manifest version supported
- requested/used profile pair supported
- packet class supported
- hash/digest present where required
- admission class derivable

Success condition:
- repo can deterministically classify promoted intake as compatible, mismatch, or blocked

### Slice NF-03 — run logging extension
Extend run logging/registry surfaces so each execution can record:

- promotion posture
- admission class
- manifest hash
- lineage identifiers
- operator review status

Success condition:
- promoted and non-promoted runs can be distinguished without ambiguity

### Slice NF-04 — proof script
Add a verification script that proves:
- compatible promotion intake accepted
- missing manifest blocked
- digest mismatch blocked
- lineage identifiers preserved

Success condition:
- one command gives a pass/fail summary for the seam

---

## Repo tasks — NeuroForge cloud lane

### Slice NG-01 — intake schema mirror
Create a cloud intake schema that mirrors the admitted envelope fields and rejects partial promotion claims.

### Slice NG-02 — provenance persistence
Persist the promotion lineage in the canonical run record or inference job record.

### Slice NG-03 — cloud mismatch posture
If a job arrives with a promotion envelope that is incompatible with the admitted manifest, mark it blocked or mismatch rather than silently degrading.

### Slice NG-04 — downstream evidence export
Make sure cloud-side evidence can be exported back to ForgeCommand in a compact operator-safe form.

---

## Boundaries to preserve

neuronforge / NeuroForge may:
- validate promotion envelope presence
- record compatibility posture
- store lineage and admission state
- expose operator evidence

neuronforge / NeuroForge may not in wave 1:
- invent new TOON segment formats
- alter success hash definitions
- relax fallback doctrine
- auto-promote new packet classes
- treat a missing digest as “good enough”

---

## First proof inventory

At minimum prove these cases:

1. strict-admitted promoted request
2. non-strict-admitted promoted request
3. missing manifest hash
4. unsupported requested profile
5. digest mismatch
6. lineage loss attempt
7. replay of same admitted input yields same admission classification

---

## Recommended repo deliverables

For neuronforge / NeuroForge, create these artifacts:

- a promotion compatibility module
- a promotion-aware run model or schema
- a verification script
- operator-readable evidence examples
- one ADR explaining why promotion truth remains upstream-owned by PACT
