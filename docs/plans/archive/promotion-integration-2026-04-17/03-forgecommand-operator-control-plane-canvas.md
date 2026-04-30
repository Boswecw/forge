# Canvas 03 — ForgeCommand Operator Control Plane
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Define the ForgeCommand lane for promotion integration so the control plane becomes the operator authority surface for admission, mismatch detection, and approval — without turning ForgeCommand into a serialization engine.

---

## ForgeCommand role

ForgeCommand should become the place where the operator can answer:

- which PACT wave-1 manifest is currently admitted
- which downstream repos are compatible
- which runs used strict admitted vs non-strict admitted outcomes
- where a mismatch occurred
- whether local use and cloud use are separately approved
- whether rollback is required

ForgeCommand should not:
- render TOON artifacts as a source of truth
- reclassify packet meaning on its own
- fabricate promotion status from partial data
- hide mismatch or missing-evidence states

---

## Required operator views

### View 1 — Promotion registry card
Shows:
- manifest version
- manifest hash
- source repo and commit
- admission stage
- supported packet classes
- supported profiles
- approval state

### View 2 — Repo compatibility matrix
Rows:
- PACT
- neuronforge
- NeuroForge
- ForgeCommand consumer surface

Columns:
- manifest loaded
- compatible
- last proof time
- mismatch count
- blocked count
- last approved by operator

### View 3 — Run evidence panel
For a selected run, show:
- task intent id
- context bundle id/hash
- requested profile
- used profile
- artifact kind
- fallback flags/reason
- strict success hash or non-strict digest
- admission class
- promotion posture

### View 4 — Mismatch / rollback panel
Show:
- reason for block or mismatch
- first failing repo
- failing field or digest
- recommended rollback target

---

## Operator actions

Wave-1 operator actions should be bounded to:

- load or refresh manifest evidence
- approve for local use
- approve for cloud use
- mark blocked
- record rollback
- view proof artifacts
- compare current repo state to admitted manifest

Do not add “edit manifest” or “override digest” actions in this wave.

---

## Data contract for ForgeCommand

ForgeCommand should consume a compact cross-repo summary payload such as:

- `manifest_hash`
- `manifest_version`
- `repo_name`
- `compatibility_state`
- `admission_class_counts`
- `mismatch_reason_codes`
- `last_proof_timestamp`
- `last_verified_commit`
- `operator_approval_state`

And for per-run drill-down:
- lineage identifiers
- requested/used profile
- artifact kind
- fallback fields
- success hash or canonical digest
- proof artifact path or report identifier

---

## Implementation slices

### Slice FC-01 — shared types
Add explicit frontend/backend types for:
- promotion manifest summary
- repo compatibility posture
- per-run promotion evidence
- approval state

### Slice FC-02 — Axum/Tauri backend route layer
Add bounded routes or commands to:
- read current promotion manifest summary
- read compatibility matrix
- read run evidence detail
- record operator approval actions

### Slice FC-03 — Svelte 5 operator UI
Add:
- registry summary card
- compatibility matrix table
- drill-down detail pane
- mismatch band / posture band

### Slice FC-04 — verification
Add proof that:
- blocked states surface visibly
- missing fields do not show as healthy
- non-strict admitted cases display distinctly from strict ones
- operator approvals never change underlying manifest truth

---

## UI language rules

Use explicit governance-first vocabulary:

- `compatible`
- `mismatch`
- `blocked`
- `strict admitted`
- `non-strict admitted`
- `not promoted`
- `rolled back`

Do not use loose labels like:
- good
- healthy-ish
- okay
- probably fine

---

## Initial approval doctrine

Approval is two-stage:

1. `approved_for_local_use`
2. `approved_for_cloud_use`

A local approval must not imply cloud approval automatically.
A compatibility state must not imply operator approval automatically.
