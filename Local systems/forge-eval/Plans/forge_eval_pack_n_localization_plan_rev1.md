# Pack N — Localization Pack Implementation Plan
**Revision:** 1
**Date:** 2026-03-06
**Owner:** Charlie
**Status:** Active — ready for implementation
**Exact intent of this revision:** Incorporated four structural fixes from architectural review: (1) removed top-level `language` field, moved to per-candidate `detected_language`; (2) moved confidence to per-candidate level with conservative summary aggregate; (3) defined LocalizationPack integration contract with existing NeuroForge patch governance chain including `LOC-GATE-*` error codes; (4) replaced free-string hypothesis fields with bounded enum, aligned `hazard_tier` vocabulary with Pack K, corrected `fastapi` language tag. Added `localization_summary.json` schema sketch required for Slice 1 exit criteria.

---

## Purpose

Add a new governed stage to Forge Eval that compiles existing defect evidence into an LLM-facing localization artifact, then make NeuroForge consume that artifact as a required input for localized code review and repair.

This plan assumes the current ecosystem realities already documented:

- NeuroForge is the provider-agnostic inference layer with fail-closed degraded modes, bounded patch behavior, and PromptSpec-based execution. Patch governance is enforced through the MAPO/MRPA chain: `mapo_root_hash` + `workspace_root` + `patch_targets` are required for repair tasks, validated by the evaluator gate (`MAPO-TGT-GATE-*` error codes).
- Forge Eval already emits deterministic artifacts through Packs A–M, including `context_slices`, `review_findings`, `telemetry_matrix`, `occupancy_snapshot`, `hazard_map`, and `evidence_bundle`.
- MAPO / concern spans / patch targets / MRPA already provide deterministic navigation and bounded patch enforcement.
- DataForge remains durable truth and audit persistence.

The goal is to add the missing bridge between existing evidence and localized LLM review — not to redesign the system.

---

## Executive Summary

The ecosystem already has strong error signals, deterministic block extraction, normalized reviewer findings, hazard/confidence math, bounded patch targets, and fail-closed patch application.

What is still missing is a canonical artifact that says:

- these files are most suspicious,
- these blocks/slices are most suspicious,
- these constructs are highest risk inside those regions,
- this is the approved review scope,
- this is the approved patch scope.

That artifact is: **`LocalizationPack.v1`**

Produced by: **Forge Eval Pack N — `localization_pack`**

Consumed by: **NeuroForge localized review / repair mode**

---

## Architectural Doctrine

### New doctrine

**No repair-capable NeuroForge code task may proceed without either a valid `LocalizationPack` or an explicit operator override that downgrades the request to analysis-only.**

### Supporting doctrine

1. Detection may come from tests, static analysis, runtime failures, governed review findings, or Forge Eval evidence.
2. Localization compiles those signals into bounded candidate regions.
3. NeuroForge reviews and repairs only within localized review scope.
4. If patch targets exist, localization scope must intersect bounded patch scope before any repair prompt is rendered.
5. Missing or invalid localization must fail closed for repair-capable paths.

### Patch governance integration doctrine

`localization_pack_ref` binds to the existing patch governance chain under the same rules as `patch_targets_ref`:

- resolves against trusted workspace roots (`NEUROFORGE_PATCH_WORKSPACE_ROOTS`)
- relative refs resolved against request `workspace_root`
- unsupported URI schemes rejected
- the evaluator localization gate (`LOC-GATE-*`) runs **before** the MRPA range containment check
- if localization scope excludes a target region, request fails with `LOC-GATE-NO-SCOPE` before MRPA runs
- if LocalizationPack is missing for a repair task, request fails with `LOC-GATE-MISSING` unless caller explicitly passes `allow_analysis_only=true`

---

## Corrected Schema — `localization_pack.json`

### Key corrections from Rev 0

1. **No top-level `language` field.** Language is per-candidate only. A single diff may span Python, Rust, TypeScript, and Svelte simultaneously. Artifact-level language tagging would truncate evidence.
2. **Confidence is per-candidate.** Each `file_candidate` and `block_candidate` carries its own `evidence_density` and `confidence`. The pack-level `summary_confidence` is a conservative aggregate (minimum across candidates).
3. **Hypothesis fields use bounded enum.** No free-string LLM inference in a deterministic artifact.
4. **`hazard_tier` uses Pack K vocabulary.** `low | guarded | elevated | high | critical` — not `low | medium | high`.
5. **Language enum is corrected.** `fastapi` removed — it is a framework, not a language. Framework detection is a separate optional field.

### Schema

```json
{
  "artifact_version": "localization_pack.v1",
  "kind": "localization_pack",
  "run_id": "string",
  "source_artifacts": {
    "risk_heatmap_ref": "string",
    "context_slices_ref": "string",
    "review_findings_ref": "string",
    "telemetry_matrix_ref": "string",
    "occupancy_snapshot_ref": "string|null",
    "hazard_map_ref": "string|null",
    "patch_targets_ref": "string|null",
    "concernspans_ref": "string|null"
  },
  "file_candidates": [
    {
      "file_path": "string",
      "detected_language": "python|rust|typescript|svelte|other|null",
      "detected_framework": "fastapi|tauri|svelte_kit|other|null",
      "score": 0.0,
      "evidence_density": 0.0,
      "confidence": 0.0,
      "reason_codes": ["string"],
      "defect_keys": ["string"]
    }
  ],
  "function_candidates": [
    {
      "symbol": "string",
      "file_path": "string",
      "detected_language": "python|rust|typescript|svelte|other|null",
      "score": 0.0,
      "confidence": 0.0,
      "reason_codes": ["string"]
    }
  ],
  "block_candidates": [
    {
      "slice_id": "string",
      "file_path": "string",
      "detected_language": "python|rust|typescript|svelte|other|null",
      "start_line": 1,
      "end_line": 1,
      "score": 0.0,
      "evidence_density": 0.0,
      "confidence": 0.0,
      "defect_keys": ["string"],
      "support_count": 0,
      "likely_constructs": ["string"],
      "root_cause_hypothesis": "boundary_violation|null_path|async_race|missing_guard|serialization_boundary|ownership_violation|reactive_state_mutation|other|null",
      "reason_codes": ["string"]
    }
  ],
  "review_scope": [
    {
      "file_path": "string",
      "start_line": 1,
      "end_line": 1
    }
  ],
  "patch_scope": [
    {
      "target_id": "string",
      "file_path": "string",
      "allow_ranges": [[1, 10]]
    }
  ],
  "summary": {
    "summary_confidence": 0.0,
    "evidence_density_mean": 0.0,
    "hazard_tier": "low|guarded|elevated|high|critical",
    "file_candidate_count": 0,
    "block_candidate_count": 0,
    "review_scope_line_count": 0,
    "patch_scope_present": false
  },
  "model": {
    "ranking_policy": "heuristic_v1",
    "scope_merge_policy": "deterministic_merge_v1",
    "construct_extraction_policy": "ast_heuristic_v1"
  },
  "provenance": {
    "algorithm": "localization_pack_v1",
    "deterministic": true
  }
}
```

### `localization_summary.json` schema

Required output alongside the main pack. Contains the operator-facing summary without full candidate arrays.

```json
{
  "artifact_version": "localization_summary.v1",
  "kind": "localization_summary",
  "run_id": "string",
  "localization_pack_ref": "string",
  "summary_confidence": 0.0,
  "hazard_tier": "low|guarded|elevated|high|critical",
  "file_candidate_count": 0,
  "block_candidate_count": 0,
  "review_scope_line_count": 0,
  "patch_scope_present": false,
  "top_files": ["string"],
  "top_reason_codes": ["string"],
  "provenance": {
    "algorithm": "localization_pack_v1",
    "deterministic": true
  }
}
```

---

## PromptSpec localization extension (corrected)

```json
{
  "localization_input": {
    "required": true,
    "artifact_ref": "string|null",
    "artifact_workspace_root": "string|null",
    "max_files": 3,
    "max_blocks": 5,
    "review_scope_required": true,
    "patch_scope_required_for_repair": true,
    "allow_analysis_only": false
  }
}
```

`artifact_ref` resolves under the same trusted workspace root rules as `patch_targets_ref`. `allow_analysis_only=true` is the explicit operator downgrade path — it must be declared, it cannot be inferred.

---

## LOC-GATE error codes (new)

| Code | Condition | Recoverable |
|---|---|---|
| `LOC-GATE-MISSING` | Repair requested, no localization artifact supplied, `allow_analysis_only=false` | false |
| `LOC-GATE-NO-SCOPE` | Localization scope excludes requested patch target | false |
| `LOC-GATE-INVALID-REF` | `artifact_ref` cannot be resolved under trusted roots | false |
| `LOC-GATE-SCHEMA-INVALID` | LocalizationPack fails schema validation | false |
| `LOC-GATE-RUN-MISMATCH` | `run_id` in LocalizationPack does not match request run context | false |
| `LOC-GATE-SCOPE-EMPTY` | `review_scope` is present but empty | false |

All `LOC-GATE-*` codes carry `recoverable: false` and use `category: "LOCALIZATION_CONTRACT"` in the error envelope, mirroring the existing `PATCH_CONTRACT` category pattern.

---

## Pack N Inputs

### Required
- `risk_heatmap.json`
- `context_slices.json`
- `review_findings.json`
- `telemetry_matrix.json`
- `hazard_map.json`

### Optional
- `occupancy_snapshot.json`
- `patch_targets.json`
- `concernspans.json`
- test-failure metadata
- static analysis findings

---

## Pack N Outputs

### Required
- `localization_pack.json`
- `localization_summary.json`

### Optional (v1)
- `construct_map.json`
- `candidate_rank_explain.json`

---

## Candidate Ranking Strategy (v1 — heuristic, deterministic)

### File candidate score
- slice count in file
- reviewer support count
- defect density
- hazard contribution
- repeated support across reviewers
- concernspan overlap if available

### Block candidate score
- slice-level reviewer support
- number of distinct `defect_key`s
- hazard tier/contribution
- occupancy or hidden-defect pressure where available
- overlap with changed hunks
- overlap with patch targets or concern spans

### Per-candidate confidence
```
confidence = clamp(
    (support_count / max_support) * evidence_density_weight
    + (defect_key_count / total_defects) * defect_weight
    + hazard_contribution_normalized * hazard_weight,
    0.0, 1.0
)
```

All weights are config-locked. `summary_confidence = min(confidence across all block candidates)` — conservative aggregate.

### Function candidate derivation
Optional. Group block candidates by detected symbol span. Do not fail the stage if function-level derivation is unavailable.

---

## Construct Hypothesis Extraction (v1)

Per candidate block, derive likely high-risk constructs from AST/heuristic analysis. Deterministic — no LLM inference for construct labeling in v1.

### Construct vocabulary per language

**Python**
- `if_guard`, `async_call`, `try_except`, `return_boundary`, `serialization_boundary`, `dependency_call`

**Rust**
- `if_guard`, `match_arm`, `borrow_boundary`, `async_task_boundary`, `trait_dispatch`, `error_propagation`

**TypeScript**
- `if_guard`, `async_call`, `null_check`, `type_assertion`, `promise_chain`

**Svelte**
- `if_guard`, `reactive_state` (`$state`), `derived_state` (`$derived`), `effect_boundary` (`$effect`), `prop_mutation`, `async_ui_transition`

### `root_cause_hypothesis` enum (locked v1 vocabulary)
- `boundary_violation` — logic crosses a trust or ownership boundary incorrectly
- `null_path` — null/undefined/None not handled
- `async_race` — async operation timing or ordering issue
- `missing_guard` — conditional check absent
- `serialization_boundary` — data transformation at API/model boundary
- `ownership_violation` — Rust borrow/lifetime issue
- `reactive_state_mutation` — Svelte reactive state mutated incorrectly
- `other` — construct detected but hypothesis not classifiable
- `null` — no hypothesis available

---

## Review Scope Compilation

Rules:
1. Scope is line-bounded per file
2. File identity preserved
3. Overlapping candidate blocks merge deterministically (union, then clamp to `max_scope_lines_per_file`)
4. Total review scope capped at `max_review_scope_lines` (config-locked)
5. If patch targets exist, review scope for repair-capable flows is intersected against allowed patch ranges
6. If no valid review scope can be compiled → stage failure, not empty scope

---

## NeuroForge Integration

### Phase A — PromptSpec and localization gate

Add `localization_input` to PromptSpec validation. Implement `LOC-GATE-*` error codes in the evaluator. Wire `artifact_ref` resolution under trusted workspace roots.

**Gate execution order for repair tasks:**
1. `LOC-GATE-MISSING` / `LOC-GATE-INVALID-REF` / `LOC-GATE-SCHEMA-INVALID` (localization pre-check)
2. `LOC-GATE-NO-SCOPE` (scope intersection check)
3. `MAPO-TGT-GATE-*` (existing patch range containment — unchanged)
4. MRPA apply

### Phase B — Prompt compiler

When localization input is valid:
- render only approved block context
- include candidate reasons and construct hints
- include `root_cause_hypothesis` if non-null
- suppress broad repo/file context outside review scope

### Phase C — Output contracts

Localized review/repair outputs include:
- candidate block id or target id
- classification (construct type, hypothesis)
- minimal diff patch bounded by `patch_scope`
- explanation tied to localized root cause

---

## New Prompt Contract Text

```text
You are operating in localized review mode.

Review only the approved candidate blocks listed in review_scope.
Do not inspect or patch outside review_scope.
If patch_scope is provided, do not propose edits outside target-bound ranges.

Before fixing, classify:
1. semantic mistake type
2. syntactic construct (from likely_constructs)
3. likely root cause (from root_cause_hypothesis if present)

Inspect first:
- conditionals and guards
- API or framework calls
- boundary logic (serialization, ownership, async)
- reactive state transitions (Svelte)

For each suspicious construct:
- state the intended invariant
- name one edge case
- identify one adjacent statement that must be checked with it

Only then propose a minimal bounded fix.
```

---

## Fail-Closed Rules

### Forge Eval Pack N
- required source artifacts missing → stage failure
- candidate ranking cannot be performed deterministically → stage failure
- review scope cannot be compiled → stage failure
- line bounds invalid → stage failure
- patch scope intersection invalid for repair mode → stage failure
- schema validation failure → stage failure

### NeuroForge
- repair requested, no valid localization, `allow_analysis_only=false` → `LOC-GATE-MISSING`
- localization artifact ref unresolvable → `LOC-GATE-INVALID-REF`
- localization scope excludes target → `LOC-GATE-NO-SCOPE`
- schema invalid → `LOC-GATE-SCHEMA-INVALID`
- run_id mismatch → `LOC-GATE-RUN-MISMATCH`

---

## Implementation Slices

### Slice 1 — Schema + stage scaffold
- `localization_pack.v1` schema (corrected)
- `localization_summary.v1` schema
- Pack N stage scaffold wired into `stage_runner.py`
- PromptSpec `localization_input` fields
- Stage compiles placeholder pack from fixed fixtures

### Slice 2 — Block ranking + review scope
- file/block ranking logic with per-candidate confidence
- `summary_confidence` as conservative aggregate
- review scope compilation with deterministic merge/clamp
- golden tests for fixed inputs

### Slice 3 — Construct extraction + patch scope intersection
- per-language construct extraction (bounded vocabulary)
- `root_cause_hypothesis` bounded enum derivation
- patch target intersection logic
- `localization_summary.json` assembly

### Slice 4 — NeuroForge localized review mode
- `LOC-GATE-*` error codes in evaluator
- `localization_pack_ref` resolution under trusted workspace roots
- gate execution order (LOC-GATE before MAPO-TGT-GATE)
- prompt compiler updates
- analysis-only downgrade path (`allow_analysis_only`)

### Slice 5 — End-to-end governed path
- Forge Eval → NeuroForge → bounded repair integration
- telemetry and DataForge persistence
- operator-visible error handling
- one end-to-end localized repair run succeeds in-scope
- one out-of-scope repair attempt blocked deterministically

---

## Final Doctrine

**Detection comes from tests, static analysis, runtime failures, governed review findings, and Forge Eval evidence. Pack N compiles that evidence into bounded localization targets. NeuroForge reviews and repairs only within localized scope. LOC-GATE enforces localization before MAPO-TGT-GATE enforces patch range containment. MRPA enforces final patch boundaries. DataForge stores the audit trail.**

---
---

# VS Code Claude Opus 4.6 — Implementation Prompt

## PREFLIGHT CONTEXT — READ THIS FIRST

### What you are implementing

**Forge Eval Pack N** — a new deterministic stage that compiles the existing A-M artifact chain into a `localization_pack.json` artifact. This artifact tells NeuroForge exactly which files, blocks, and constructs are most suspicious so it can review and repair only within bounded scope.

This is not a redesign of Forge Eval. It is a new stage that extends the existing A-M pipeline:

```
config -> risk_heatmap -> context_slices -> review_findings -> telemetry_matrix
-> occupancy_snapshot -> capture_estimate -> hazard_map -> merge_decision
-> evidence_bundle -> localization_pack  ← NEW
```

You are also adding the NeuroForge integration that consumes the localization artifact.

### Repository locations

```
/home/charlie/Forge/ecosystem/forge-eval/repo     ← Pack N goes here
/home/charlie/Forge/ecosystem/NeuroForge           ← NeuroForge integration (Slices 4–5)
```

### Key files to read before writing any code

**Forge Eval:**
```
src/forge_eval/stage_runner.py
src/forge_eval/stages/hazard_map.py          ← most recent prior stage, use as model
src/forge_eval/stages/evidence_bundle.py     ← Pack M, use as model for stage wiring
src/forge_eval/schemas/hazard_map.schema.json
src/forge_eval/schemas/evidence_bundle.schema.json
src/forge_eval/config.py
doc/system/16-hazard-map-stage.md
doc/system/18-evidence-bundle-stage.md
```

**NeuroForge (read before Slice 4):**
```
neuroforge_backend/services/patch_governance.py   ← MAPO-TGT-GATE logic, mirror for LOC-GATE
neuroforge_backend/models/prompt_spec.py          ← PromptSpec model, add localization_input
neuroforge_backend/services/evaluator.py          ← Gate execution, add LOC-GATE checks
neuroforge_backend/routers/inference.py           ← Understand request flow
```

### Forge Eval doctrine — non-negotiable

1. Deterministic output — identical inputs must produce byte-identical artifacts
2. Fail closed — missing required inputs, invalid ranges, unresolvable scope → stage failure
3. Strict JSON schema contracts — `additionalProperties: false` at root
4. No silent truncation — explicit policy-driven caps only
5. Stable artifact serialization — `sort_keys=True`, compact separators, single trailing newline
6. No LLM inference in Pack N — construct extraction is AST/heuristic only in v1

### Install posture
```bash
pip install -e .                          # networked
pip install --no-build-isolation -e .     # offline/pre-provisioned
```

---

## IMPLEMENTATION PROMPT — EXECUTE IN SLICE ORDER

Implement in strict slice order. Do not skip ahead. Read source files before writing code in each slice.

---

### SLICE 1 — Schema + Stage Scaffold

**Objective:** Define both artifact schemas and wire the Pack N stage scaffold into the pipeline. Stage produces placeholder output from fixed fixtures at this point — full ranking logic comes in Slice 2.

---

**Step 1.1 — Read these files first**

```
src/forge_eval/stages/evidence_bundle.py
src/forge_eval/schemas/evidence_bundle.schema.json
src/forge_eval/stage_runner.py
src/forge_eval/config.py
```

Understand: how a stage is wired into `stage_runner.py`, how config keys are declared, how artifacts reference upstream inputs.

---

**Step 1.2 — Create `localization_pack.schema.json`**

Path: `src/forge_eval/schemas/localization_pack.schema.json`

Enforce this exact shape. All objects strict (`additionalProperties: false`). All listed fields required unless explicitly marked optional.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LocalizationPack",
  "type": "object",
  "additionalProperties": false,
  "required": ["artifact_version", "kind", "run_id", "source_artifacts",
               "file_candidates", "function_candidates", "block_candidates",
               "review_scope", "patch_scope", "summary", "model", "provenance"],
  "properties": {
    "artifact_version": {"type": "string", "const": "localization_pack.v1"},
    "kind": {"type": "string", "const": "localization_pack"},
    "run_id": {"type": "string"},
    "source_artifacts": {
      "type": "object",
      "additionalProperties": false,
      "required": ["risk_heatmap_ref", "context_slices_ref",
                   "review_findings_ref", "telemetry_matrix_ref"],
      "properties": {
        "risk_heatmap_ref": {"type": "string"},
        "context_slices_ref": {"type": "string"},
        "review_findings_ref": {"type": "string"},
        "telemetry_matrix_ref": {"type": "string"},
        "occupancy_snapshot_ref": {"type": ["string", "null"]},
        "hazard_map_ref": {"type": ["string", "null"]},
        "patch_targets_ref": {"type": ["string", "null"]},
        "concernspans_ref": {"type": ["string", "null"]}
      }
    },
    "file_candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["file_path", "score", "evidence_density", "confidence",
                     "reason_codes", "defect_keys"],
        "properties": {
          "file_path": {"type": "string"},
          "detected_language": {"type": ["string", "null"],
            "enum": ["python", "rust", "typescript", "svelte", "other", null]},
          "detected_framework": {"type": ["string", "null"],
            "enum": ["fastapi", "tauri", "svelte_kit", "other", null]},
          "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "evidence_density": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "reason_codes": {"type": "array", "items": {"type": "string"}},
          "defect_keys": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "function_candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["symbol", "file_path", "score", "confidence", "reason_codes"],
        "properties": {
          "symbol": {"type": "string"},
          "file_path": {"type": "string"},
          "detected_language": {"type": ["string", "null"],
            "enum": ["python", "rust", "typescript", "svelte", "other", null]},
          "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "reason_codes": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "block_candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["slice_id", "file_path", "start_line", "end_line",
                     "score", "evidence_density", "confidence",
                     "defect_keys", "support_count", "likely_constructs",
                     "root_cause_hypothesis", "reason_codes"],
        "properties": {
          "slice_id": {"type": "string"},
          "file_path": {"type": "string"},
          "detected_language": {"type": ["string", "null"],
            "enum": ["python", "rust", "typescript", "svelte", "other", null]},
          "start_line": {"type": "integer", "minimum": 1},
          "end_line": {"type": "integer", "minimum": 1},
          "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "evidence_density": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
          "defect_keys": {"type": "array", "items": {"type": "string"}},
          "support_count": {"type": "integer", "minimum": 0},
          "likely_constructs": {"type": "array", "items": {"type": "string"}},
          "root_cause_hypothesis": {"type": ["string", "null"],
            "enum": ["boundary_violation", "null_path", "async_race",
                     "missing_guard", "serialization_boundary",
                     "ownership_violation", "reactive_state_mutation",
                     "other", null]},
          "reason_codes": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "review_scope": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["file_path", "start_line", "end_line"],
        "properties": {
          "file_path": {"type": "string"},
          "start_line": {"type": "integer", "minimum": 1},
          "end_line": {"type": "integer", "minimum": 1}
        }
      }
    },
    "patch_scope": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["target_id", "file_path", "allow_ranges"],
        "properties": {
          "target_id": {"type": "string"},
          "file_path": {"type": "string"},
          "allow_ranges": {
            "type": "array",
            "items": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2}
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "required": ["summary_confidence", "evidence_density_mean", "hazard_tier",
                   "file_candidate_count", "block_candidate_count",
                   "review_scope_line_count", "patch_scope_present"],
      "properties": {
        "summary_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "evidence_density_mean": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "hazard_tier": {"type": "string",
          "enum": ["low", "guarded", "elevated", "high", "critical"]},
        "file_candidate_count": {"type": "integer", "minimum": 0},
        "block_candidate_count": {"type": "integer", "minimum": 0},
        "review_scope_line_count": {"type": "integer", "minimum": 0},
        "patch_scope_present": {"type": "boolean"}
      }
    },
    "model": {
      "type": "object",
      "additionalProperties": false,
      "required": ["ranking_policy", "scope_merge_policy", "construct_extraction_policy"],
      "properties": {
        "ranking_policy": {"type": "string"},
        "scope_merge_policy": {"type": "string"},
        "construct_extraction_policy": {"type": "string"}
      }
    },
    "provenance": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "deterministic"],
      "properties": {
        "algorithm": {"type": "string"},
        "deterministic": {"type": "boolean", "const": true}
      }
    }
  }
}
```

---

**Step 1.3 — Create `localization_summary.schema.json`**

Path: `src/forge_eval/schemas/localization_summary.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LocalizationSummary",
  "type": "object",
  "additionalProperties": false,
  "required": ["artifact_version", "kind", "run_id", "localization_pack_ref",
               "summary_confidence", "hazard_tier", "file_candidate_count",
               "block_candidate_count", "review_scope_line_count",
               "patch_scope_present", "top_files", "top_reason_codes", "provenance"],
  "properties": {
    "artifact_version": {"type": "string", "const": "localization_summary.v1"},
    "kind": {"type": "string", "const": "localization_summary"},
    "run_id": {"type": "string"},
    "localization_pack_ref": {"type": "string"},
    "summary_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    "hazard_tier": {"type": "string",
      "enum": ["low", "guarded", "elevated", "high", "critical"]},
    "file_candidate_count": {"type": "integer", "minimum": 0},
    "block_candidate_count": {"type": "integer", "minimum": 0},
    "review_scope_line_count": {"type": "integer", "minimum": 0},
    "patch_scope_present": {"type": "boolean"},
    "top_files": {"type": "array", "items": {"type": "string"}},
    "top_reason_codes": {"type": "array", "items": {"type": "string"}},
    "provenance": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "deterministic"],
      "properties": {
        "algorithm": {"type": "string"},
        "deterministic": {"type": "boolean", "const": true}
      }
    }
  }
}
```

---

**Step 1.4 — Add Pack N config keys to `config.py`**

Add to the normalized config surface:

```python
# Pack N — localization pack
localization_model_version = "localization_pack_rev1"
localization_max_file_candidates = 10       # int >= 1
localization_max_block_candidates = 20      # int >= 1
localization_max_review_scope_lines = 500   # int >= 1
localization_max_scope_lines_per_file = 150 # int >= 1
localization_round_digits = 6               # int [0, 12]
localization_ranking_weights = {            # normalized to unit sum
    "support_count": 0.35,
    "defect_density": 0.25,
    "hazard_contribution": 0.25,
    "churn": 0.15
}
```

---

**Step 1.5 — Create `stages/localization_pack.py` scaffold**

Wire it identically to how `stages/evidence_bundle.py` is structured. The stage must:

- accept required upstream artifacts: `risk_heatmap`, `context_slices`, `review_findings`, `telemetry_matrix`, `hazard_map`
- accept optional upstream artifacts: `occupancy_snapshot`, `patch_targets` (null if not present)
- validate all required artifacts are present and run_id consistent
- emit placeholder `localization_pack.json` and `localization_summary.json` from deterministic fixture data
- validate both outputs against their schemas before writing
- fail closed if validation fails

Add `localization_pack` to the stage dependency chain in `stage_runner.py`:
```
evidence_bundle requires merge_decision
localization_pack requires evidence_bundle
```

---

**Step 1.6 — Add PromptSpec `localization_input` fields (NeuroForge)**

Read `neuroforge_backend/models/prompt_spec.py` first.

Add to the PromptSpec model:

```python
class LocalizationInput(BaseModel):
    required: bool = True
    artifact_ref: Optional[str] = None
    artifact_workspace_root: Optional[str] = None
    max_files: int = 3
    max_blocks: int = 5
    review_scope_required: bool = True
    patch_scope_required_for_repair: bool = True
    allow_analysis_only: bool = False
```

Add `localization_input: Optional[LocalizationInput] = None` to the main PromptSpec model. Do not make it required yet — that comes in Slice 4.

---

**Step 1.7 — Tests**

Required:
1. `localization_pack.schema.json` validates a correctly shaped artifact
2. Missing required field fails schema validation
3. `additionalProperties` violation fails schema validation
4. Unknown `detected_language` value fails (not in enum)
5. Unknown `root_cause_hypothesis` value fails (not in enum)
6. `hazard_tier` value `"medium"` fails (wrong vocabulary — must use Pack K vocabulary)
7. `localization_summary.schema.json` validates a correctly shaped summary
8. Stage scaffold runs and emits both artifacts from fixture data
9. Both emitted artifacts validate against their schemas
10. Stage fails closed when a required upstream artifact is missing

**Exit criteria for Slice 1:**
- Both schemas exist and validate correctly
- Stage scaffold is wired and runs
- Config keys are declared
- PromptSpec model extended
- All 10 tests pass

---

### SLICE 2 — Block Ranking + Review Scope

**Objective:** Implement deterministic file/block ranking with per-candidate confidence, and compile review scope with deterministic merge/clamp.

---

**Step 2.1 — Read these files first**

```
src/forge_eval/services/hazard_rows.py
src/forge_eval/services/hazard_summary.py
src/forge_eval/services/occupancy_rows.py
```

Understand: how per-row scoring is computed from upstream artifacts, how summary aggregation works.

---

**Step 2.2 — Implement `services/localization_ranker.py`**

File candidate scoring:
```python
def score_file_candidate(file_path, context_slices, review_findings,
                         telemetry_matrix, hazard_map, config) -> FileCandidateScore:
    slice_count = count_slices_for_file(file_path, context_slices)
    support_count = max_support_count_for_file(file_path, review_findings, telemetry_matrix)
    defect_density = defect_count_for_file(file_path, review_findings) / max(slice_count, 1)
    hazard_contribution = max_hazard_contribution_for_file(file_path, hazard_map)

    raw_score = (
        config.ranking_weights["support_count"] * normalize(support_count) +
        config.ranking_weights["defect_density"] * normalize(defect_density) +
        config.ranking_weights["hazard_contribution"] * hazard_contribution +
        config.ranking_weights["churn"] * normalize(slice_count)
    )
    score = round(clamp(raw_score, 0.0, 1.0), config.round_digits)
    evidence_density = round(clamp(defect_density, 0.0, 1.0), config.round_digits)
    confidence = round(clamp(
        (support_count / max_support_in_run) * 0.5 + evidence_density * 0.5,
        0.0, 1.0
    ), config.round_digits)

    return FileCandidateScore(
        file_path=file_path, score=score,
        evidence_density=evidence_density, confidence=confidence, ...
    )
```

Block candidate scoring follows the same pattern at slice granularity.

Rules:
- All normalization is relative to the current run's max values — deterministic per run
- `summary_confidence = min(block_candidate.confidence for all block candidates)`
- Candidates sorted by score descending, then `file_path` + `slice_id` for tie-breaking
- Truncate to `localization_max_file_candidates` and `localization_max_block_candidates` after sorting

---

**Step 2.3 — Implement `services/review_scope_compiler.py`**

Rules:
1. Take top-ranked block candidates
2. Group by `file_path`
3. Sort ranges by `start_line` within each file
4. Merge overlapping/adjacent ranges (union)
5. Clamp each file's total scope to `localization_max_scope_lines_per_file`
6. Clamp total scope to `localization_max_review_scope_lines`
7. If patch targets present and repair mode: intersect review scope against `allow_ranges`
8. If resulting scope is empty after intersection → fail closed (`StageError`)
9. If no candidates produce any valid scope → fail closed

Emit sorted by `(file_path, start_line)`.

---

**Step 2.4 — Wire into `stages/localization_pack.py`**

Replace placeholder fixture logic with real ranking and scope compilation. Emit real `localization_pack.json` and `localization_summary.json`.

`localization_summary.json` top_files = top 3 file candidates by score. `top_reason_codes` = most frequent reason codes across all block candidates (deterministic sort on tie).

---

**Step 2.5 — Tests**

Required:
1. File ranking produces correct deterministic order for fixed inputs
2. Block ranking produces correct deterministic order for fixed inputs
3. Tie-breaking is stable (same score → sorted by file_path + slice_id)
4. Truncation to `max_file_candidates` / `max_block_candidates` works
5. `summary_confidence` = min of block confidences
6. Review scope merges overlapping ranges correctly
7. Review scope clamps to `max_review_scope_lines`
8. Review scope fails closed when no valid scope can be compiled
9. Patch target intersection constrains scope correctly
10. Patch target intersection → empty scope → fail closed
11. Golden artifact test: fixed inputs produce byte-identical output on repeated runs

**Exit criteria for Slice 2:**
- Ranking is deterministic and correct
- Review scope compiles correctly
- Fail-closed cases trigger correctly
- Golden test passes (byte-identical on repeated runs)
- All 11 tests pass

---

### SLICE 3 — Construct Extraction + Patch Scope + Summary Assembly

**Objective:** Add per-language construct extraction, `root_cause_hypothesis` derivation, patch scope passthrough/intersection, and complete `localization_summary.json` assembly.

---

**Step 3.1 — Implement `services/construct_extractor.py`**

Language detection from file extension:
```python
LANGUAGE_MAP = {
    ".py": "python", ".rs": "rust",
    ".ts": "typescript", ".tsx": "typescript",
    ".svelte": "svelte",
}
FRAMEWORK_HINTS = {
    "fastapi": ["from fastapi", "APIRouter", "@app."],
    "tauri": ["use tauri::", "#[tauri::command]"],
    "svelte_kit": ["load(", "PageLoad", "LayoutLoad"],
}
```

Construct vocabulary per language — keyword/pattern heuristics only, no LLM inference:

```python
CONSTRUCT_PATTERNS = {
    "python": {
        "if_guard": [r"\bif\b", r"\belif\b"],
        "async_call": [r"\bawait\b"],
        "try_except": [r"\btry\b", r"\bexcept\b"],
        "return_boundary": [r"\breturn\b"],
        "serialization_boundary": [r"\.model_dump\(", r"\.dict\(", r"json\."],
        "dependency_call": [r"Depends\("],
    },
    "rust": {
        "if_guard": [r"\bif\b", r"\bif let\b"],
        "match_arm": [r"\bmatch\b"],
        "borrow_boundary": [r"&mut\b", r"\.borrow\(", r"\.borrow_mut\("],
        "async_task_boundary": [r"\.await\b", r"tokio::spawn"],
        "trait_dispatch": [r"\.into\(\)", r"\.as_ref\(", r"dyn "],
        "error_propagation": [r"\?\s*;", r"unwrap\(\)", r"expect\("],
    },
    "typescript": {
        "if_guard": [r"\bif\b"],
        "async_call": [r"\bawait\b"],
        "null_check": [r"\?\.", r"!\."],
        "type_assertion": [r" as \w"],
        "promise_chain": [r"\.then\(", r"\.catch\("],
    },
    "svelte": {
        "if_guard": [r"\{#if\b"],
        "reactive_state": [r"\$state\("],
        "derived_state": [r"\$derived\("],
        "effect_boundary": [r"\$effect\("],
        "prop_mutation": [r"bind:"],
        "async_ui_transition": [r"\{#await\b"],
    },
}
```

`root_cause_hypothesis` derivation rules (deterministic, first-match):
- `ownership_violation` if language=rust and `borrow_boundary` or `error_propagation` constructs detected
- `reactive_state_mutation` if language=svelte and `reactive_state` or `prop_mutation` detected
- `serialization_boundary` if `serialization_boundary` construct detected
- `async_race` if `async_call` or `async_task_boundary` detected in a block with `support_count > 1`
- `null_path` if `null_check` or `if_guard` detected with zero support from `changed_lines` reviewer
- `missing_guard` if `if_guard` construct absent but `hazard_contribution > 0.5`
- `boundary_violation` if block crosses file boundary (last slice in file)
- `other` if constructs detected but no rule matches
- `null` if no constructs detected

---

**Step 3.2 — Implement `services/patch_scope_builder.py`**

If `patch_targets_ref` is present and resolves:
- load `patch_targets.json`
- for each patch target, build a `patch_scope` entry with `target_id`, `file_path`, `allow_ranges`
- intersect `allow_ranges` with the compiled review scope for that file
- if the intersection is empty for a repair-required target → fail closed

If no patch targets: `patch_scope = []`, `patch_scope_present = false`.

---

**Step 3.3 — Wire construct extraction and patch scope into stage**

Update `stages/localization_pack.py` to call both services. Block candidates now carry `detected_language`, `likely_constructs`, and `root_cause_hypothesis`.

---

**Step 3.4 — Tests**

Required:
1. Language detected correctly from file extension for all supported languages
2. Framework hint detected correctly (python + FastAPI → `detected_framework: "fastapi"`)
3. Construct patterns match correctly for each language
4. Unknown language → `detected_language: "other"`, empty `likely_constructs`
5. `root_cause_hypothesis` = `ownership_violation` for Rust block with borrow constructs
6. `root_cause_hypothesis` = `null` when no constructs detected
7. `root_cause_hypothesis` enum value is always valid (never a free string)
8. Patch scope builds correctly from `patch_targets.json`
9. Empty patch scope intersection → fail closed
10. No patch targets → `patch_scope = []`, `patch_scope_present = false`
11. Complete stage produces byte-identical `localization_pack.json` for fixed inputs (golden test)

**Exit criteria for Slice 3:**
- Construct extraction deterministic and bounded to enum vocabulary
- `root_cause_hypothesis` always from locked enum or null
- Patch scope intersection correct and fail-closed
- Golden test passes
- All 11 tests pass

---

### SLICE 4 — NeuroForge Localized Review Mode

**Objective:** Add `LOC-GATE-*` error codes to the NeuroForge evaluator, wire `localization_pack_ref` resolution under trusted workspace roots, enforce gate execution order, and update the prompt compiler.

---

**Step 4.1 — Read these files first**

```
neuroforge_backend/services/patch_governance.py
neuroforge_backend/services/evaluator.py
neuroforge_backend/routers/inference.py
neuroforge_backend/models/prompt_spec.py
```

Understand: how `MAPO-TGT-GATE-*` codes are raised, how `patch_targets_ref` is resolved, how the evaluator gate sequence works.

---

**Step 4.2 — Implement `LOC-GATE-*` error codes**

Add to the governance error vocabulary, mirroring `MAPO-TGT-GATE-*` pattern:

```python
LOC_GATE_CODES = {
    "LOC-GATE-MISSING": "Repair requested but no localization artifact supplied",
    "LOC-GATE-INVALID-REF": "localization_pack_ref cannot be resolved under trusted roots",
    "LOC-GATE-SCHEMA-INVALID": "LocalizationPack artifact fails schema validation",
    "LOC-GATE-RUN-MISMATCH": "run_id in LocalizationPack does not match request run context",
    "LOC-GATE-SCOPE-EMPTY": "review_scope is present but empty",
    "LOC-GATE-NO-SCOPE": "Localization scope excludes requested patch target",
}
```

All `LOC-GATE-*` codes: `recoverable=False`, `category="LOCALIZATION_CONTRACT"`.

---

**Step 4.3 — Add `localization_pack_ref` resolution**

Implement resolution under the same trusted workspace roots as `patch_targets_ref`:
- `NEUROFORGE_PATCH_WORKSPACE_ROOTS` is already configured
- relative refs resolve against request `workspace_root`
- unsupported URI schemes → `LOC-GATE-INVALID-REF`
- file outside trusted roots → `LOC-GATE-INVALID-REF`

---

**Step 4.4 — Wire LOC-GATE into evaluator gate sequence**

Gate execution order for repair tasks (enforce this exact order):

```
1. LOC-GATE-MISSING          (localization pre-check)
2. LOC-GATE-INVALID-REF      (ref resolution)
3. LOC-GATE-SCHEMA-INVALID   (schema validation)
4. LOC-GATE-RUN-MISMATCH     (run context alignment)
5. LOC-GATE-SCOPE-EMPTY      (scope sanity)
6. LOC-GATE-NO-SCOPE         (scope intersection with patch target)
7. MAPO-TGT-GATE-*           (existing patch range containment — UNCHANGED)
8. MRPA apply
```

LOC-GATE checks run before MAPO-TGT-GATE. Do not modify existing MAPO-TGT-GATE logic.

---

**Step 4.5 — Update prompt compiler**

When `localization_input` is valid and artifact is loaded:
- render only candidate blocks within `review_scope`
- include `likely_constructs` and `root_cause_hypothesis` per block
- include `reason_codes` per block
- suppress file/repo context outside `review_scope`
- prepend the localized review contract text:

```text
You are operating in localized review mode.

Review only the approved candidate blocks listed in review_scope.
Do not inspect or patch outside review_scope.
If patch_scope is provided, do not propose edits outside target-bound ranges.

Before fixing, classify:
1. semantic mistake type
2. syntactic construct (from likely_constructs)
3. likely root cause (from root_cause_hypothesis if present)

Inspect first:
- conditionals and guards
- API or framework calls
- boundary logic (serialization, ownership, async)
- reactive state transitions (Svelte)

For each suspicious construct:
- state the intended invariant
- name one edge case
- identify one adjacent statement that must be checked with it

Only then propose a minimal bounded fix.
```

---

**Step 4.6 — Tests**

Required:
1. `LOC-GATE-MISSING` raised when repair requested, no localization, `allow_analysis_only=false`
2. `LOC-GATE-MISSING` not raised when `allow_analysis_only=true`
3. `LOC-GATE-INVALID-REF` raised for refs outside trusted workspace roots
4. `LOC-GATE-SCHEMA-INVALID` raised for malformed LocalizationPack
5. `LOC-GATE-RUN-MISMATCH` raised when run_id does not match
6. `LOC-GATE-NO-SCOPE` raised when patch target is outside localization scope
7. All `LOC-GATE-*` codes carry `recoverable=False` and `category="LOCALIZATION_CONTRACT"`
8. LOC-GATE runs before MAPO-TGT-GATE (gate order test)
9. Prompt compiler includes only review_scope blocks
10. Prompt compiler suppresses out-of-scope context
11. `allow_analysis_only=true` downgrades to analysis mode — no patch scope rendered

**Exit criteria for Slice 4:**
- All LOC-GATE codes implemented and tested
- Gate execution order enforced
- Prompt compiler renders localized context only
- Existing MAPO-TGT-GATE tests still pass (regression)
- All 11 tests pass

---

### SLICE 5 — End-to-End Governed Path

**Objective:** Prove the full Forge Eval → NeuroForge → bounded repair chain works. Add telemetry and DataForge persistence. Verify both success and failure paths end-to-end.

---

**Step 5.1 — Forge Eval integration test**

Run `forge-eval run` with Pack N enabled against the DataForge target repo:

```bash
forge-eval run \
  --repo /home/charlie/Forge/ecosystem/DataForge \
  --base <base-ref> \
  --head <head-ref> \
  --config /path/to/config.yaml \
  --out /tmp/pack_n_artifacts/
```

Verify:
- `localization_pack.json` emitted and schema-valid
- `localization_summary.json` emitted and schema-valid
- `file_candidates` non-empty
- `block_candidates` non-empty
- `review_scope` non-empty
- `summary_confidence` is the minimum of block confidences
- Repeated identical runs produce byte-identical artifacts

---

**Step 5.2 — Add Pack N telemetry logging**

Add to Pack N stage telemetry (following Pack K/M pattern):
- `localization_model_version`
- input artifact refs
- `file_candidate_count`
- `block_candidate_count`
- `review_scope_line_count`
- `patch_scope_present`
- `summary_confidence`
- `hazard_tier`

---

**Step 5.3 — Add NeuroForge telemetry**

Log on each localization-aware inference:
- `localization_artifact_ref`
- `localized_review_mode_enabled`
- `repair_blocked_reason` (if LOC-GATE fired)
- `repair_downgraded` (if `allow_analysis_only`)
- `approved_region_count`

---

**Step 5.4 — DataForge persistence**

Wire DataForge persistence for:
- localization artifacts (store `localization_pack.json` ref)
- review/repair linkage to `localization_pack_ref`
- blocked/downgraded repair audit records

---

**Step 5.5 — End-to-end governed path tests**

Required:
1. One end-to-end localized repair run succeeds with valid LocalizationPack
2. Repair prompt contains only approved regions (no out-of-scope code)
3. One out-of-scope repair attempt blocked by `LOC-GATE-NO-SCOPE`
4. One repair attempt blocked by `LOC-GATE-MISSING`
5. `allow_analysis_only=true` downgrade produces analysis output, no patch
6. Artifact chain is auditable: `localization_pack_ref` present in NeuroForge run record
7. Byte-identical `localization_pack.json` on repeated Forge Eval runs with identical inputs

---

**Step 5.6 — Write implementation report**

Write to: `forge-eval/repo/reports/forge_eval_pack_n_implementation_report_rev1.md`

Structure:
```markdown
# Forge Eval Pack N — Localization Pack Implementation Report (Rev 1)

## 1. Executive verdict
[Implemented | Implemented with gaps | Partially implemented | Blocked]

## 2. Schema and artifact contracts
- localization_pack.v1 schema: status
- localization_summary.v1 schema: status
- PromptSpec localization_input: status

## 3. Pack N stage implementation
- Files added/changed
- Ranking implementation
- Construct extraction
- Review scope compilation
- Patch scope intersection

## 4. NeuroForge integration
- LOC-GATE codes implemented
- Gate execution order
- Prompt compiler changes
- Telemetry additions

## 5. Test and verification results
- pytest commands run
- test counts and results
- golden artifact determinism result
- end-to-end path results

## 6. DataForge persistence
- what is persisted
- audit trail coverage

## 7. Documentation updates
- feSYSTEM.md Pack N section added
- doc/system/19-localization-pack-stage.md written
- BUILD.sh updated

## 8. Remaining open items
[Only confirmed unresolved items]

## 9. Recommended next actions
```

---

**Step 5.7 — Documentation**

Add `doc/system/19-localization-pack-stage.md` to Forge Eval following the structure of `16-hazard-map-stage.md`.

Update `doc/system/_index.md` table to include `§19`.

Rebuild docs:
```bash
bash doc/system/BUILD.sh
```

Confirm `doc/feSYSTEM.md` is updated.

---

## Final Acceptance Criteria

You are done only when all of the following are true:

- [ ] `localization_pack.schema.json` and `localization_summary.schema.json` exist and validate
- [ ] Pack N stage is wired into `stage_runner.py` after `evidence_bundle`
- [ ] `detected_language` is per-candidate — no top-level language field
- [ ] Confidence is per-candidate — `summary_confidence` is min aggregate
- [ ] `hazard_tier` uses Pack K vocabulary (`low|guarded|elevated|high|critical`)
- [ ] `root_cause_hypothesis` uses locked bounded enum — no free strings
- [ ] `LOC-GATE-*` codes implemented with `recoverable=False`, `category="LOCALIZATION_CONTRACT"`
- [ ] LOC-GATE runs before MAPO-TGT-GATE in evaluator gate sequence
- [ ] `localization_pack_ref` resolves under trusted workspace roots
- [ ] Prompt compiler renders only review_scope context
- [ ] All slice tests pass (10 + 11 + 11 + 11 + 7 = 50 required tests)
- [ ] Byte-identical `localization_pack.json` on repeated identical runs
- [ ] `doc/system/19-localization-pack-stage.md` written
- [ ] `bash doc/system/BUILD.sh` succeeds
- [ ] Implementation report written to `reports/forge_eval_pack_n_implementation_report_rev1.md`

---

## What NOT to do

- Do not add a top-level `language` field to `localization_pack.json`
- Do not use free-form LLM inference for construct labeling in v1
- Do not modify MAPO-TGT-GATE logic or MRPA
- Do not build function candidates as a required feature — optional only
- Do not implement learned ranking models — heuristic only in v1
- Do not add clock fields to canonical Pack N artifacts
- Do not skip slices — implement in order 1 → 5

Proceed now. Start with Slice 1 Step 1.1 — read the source files before writing any code.
