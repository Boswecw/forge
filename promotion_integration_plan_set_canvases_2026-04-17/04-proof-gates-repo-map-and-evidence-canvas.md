# Canvas 04 — Proof Gates, Repo Map, and Evidence
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Turn the promotion integration work into a proof-first cross-repo package with explicit file ownership and gate order.

---

## Repo map

## PACT
Owns:
- promotion packet
- wave manifest
- strict success hash lock
- non-strict digest lock
- upstream verification scripts

Key outputs already expected:
- manifest JSON
- promotion packet JSON
- gate report
- replay evidence
- operator examples

## neuronforge / NeuroForge
Will add:
- promotion compatibility module
- promotion-aware run schema/model
- seam verification script
- operator evidence examples
- local ADR or design note

## ForgeCommand
Will add:
- promotion summary types
- compatibility routes/commands
- operator pages/panels
- approval recording
- UI proof tests

---

## Gate order

### Gate 0 — source truth gate
Must prove:
- PACT wave-1 manifest exists
- source repo gate is green
- manifest hash and packet version are present

### Gate 1 — neuronforge local carriage gate
Must prove:
- admitted envelope can be stored intact
- lineage identifiers survive
- strict/non-strict cases classify correctly

### Gate 2 — NeuroForge cloud intake gate
Must prove:
- cloud schema accepts only compatible promotion envelopes
- missing or mismatched envelopes are blocked
- provenance persists

### Gate 3 — ForgeCommand visibility gate
Must prove:
- manifest loads
- matrix surfaces mismatches
- drill-down shows exact admission posture
- operator action state is separate from compatibility state

### Gate 4 — cross-repo replay gate
Must prove:
- same promoted input yields same admission classification across repos
- strict success case remains strict
- non-strict cases preserve canonical digests

### Gate 5 — rollback gate
Must prove:
- outdated or mismatched manifest causes blocked posture
- operator can mark rollback cleanly
- no repo falsely reports admitted state after rollback

---

## Required evidence files

For each repo seam, include:

### Human-readable evidence
- one strict admitted example
- one non-strict admitted example
- one mismatch example
- one blocked example

### Machine-readable evidence
- seam report JSON
- compatibility summary JSON
- replay or digest comparison report
- gate summary JSON

---

## Recommended verification script names

### neuronforge local
`scripts/verify_promotion_seam.py`

### NeuroForge cloud
`scripts/verify_promotion_intake.py`

### ForgeCommand
`src-tauri/scripts/verify_promotion_operator_surface.sh`
or a repo-native equivalent

### cross-repo orchestrator
`scripts/verify_wave1_promotion_stack.py`

---

## Merge checklist

- [ ] PACT source gate green
- [ ] neuronforge seam gate green
- [ ] NeuroForge intake gate green
- [ ] ForgeCommand operator gate green
- [ ] cross-repo replay gate green
- [ ] rollback evidence proved
- [ ] ADRs/design notes added
- [ ] operator examples added
