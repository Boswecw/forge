# Forge Eval — Pack J Chao2 Revision
## VS Code Claude Opus 4.6 — Implementation Prompt (Rev 1)

**Date:** 2026-03-06
**Owner:** Charlie
**Target:** VS Code Claude Opus 4.6
**Purpose:** Single-paste implementation prompt. Contains all preflight context and execution instructions needed to implement the Pack J Chao2 revision without additional input.

---

## PREFLIGHT CONTEXT — READ THIS FIRST

### What Forge Eval is

`forge-eval` is a deterministic, fail-closed standalone CLI evaluation subsystem.

It runs a fixed pipeline of stages (Packs A–M), each producing a schema-validated JSON artifact. The full implemented pipeline is:

```
config -> risk_heatmap -> context_slices -> review_findings -> telemetry_matrix
-> occupancy_snapshot -> capture_estimate -> hazard_map -> merge_decision -> evidence_bundle
```

All stages are implemented. All artifacts are real and schema-locked.

### What Pack J is

Pack J is the `capture_estimate` stage. It produces `capture_estimate.json`.

Pack J's job: given the telemetry matrix and occupancy snapshot, estimate how many defects are likely hidden (not yet found by reviewers).

It does this using statistical estimators that operate on **incidence data** — specifically how many reviewers observed each defect.

Current Pack J estimators:
- **Chao1** (bias-corrected) — singleton/doubleton frequency estimator
- **ICE** (Incidence-based Coverage Estimator) — rare/frequent split estimator

Selection policy: `max_hidden` — the most conservative (highest) hidden estimate governs downstream.

### What this revision adds

Add **Chao2** as a third estimator alongside Chao1 and ICE.

Chao2 is appropriate here because Pack J already works with incidence/sample-style data (reviewer observations per defect), which is exactly what Chao2 expects.

Chao1 is **retained** — it is not replaced. Both serve as conservative comparators.

After this revision, Pack J computes all three, records evidence of all three, and selects the governing hidden estimate via the same fixed `max_hidden` policy.

### Governing doctrine — non-negotiable

These rules apply to this revision. Do not deviate.

1. **Deterministic outputs** — identical inputs must produce byte-identical `capture_estimate.json` every time.
2. **Fail closed** — invalid inputs, bad counts, divide-by-zero, unsatisfied Chao2 assumptions → fail explicitly or mark unavailable. Never emit a clean-looking estimate from garbage inputs.
3. **Evidence of execution** — the artifact must record estimator inputs, outputs, guard flags, selection policy, selected method, and selected hidden estimate. Not just the final number.
4. **No estimator shopping** — no case-by-case discretionary selection. One fixed rule: `max_hidden`.
5. **Strict schema contracts** — all changes to `capture_estimate.json` shape must be reflected in `capture_estimate.schema.json`. Schema is `additionalProperties: false` at root. Validation must pass.
6. **Keep the revision small** — do not build statistical abstractions or frameworks. Add one small service file and extend what exists.
7. **Do not touch Pack K, L, or M** — they are downstream and already implemented. This revision is bounded to Pack J only.

### Repository location

```
/home/charlie/Forge/ecosystem/forge-eval/repo
```

### Key source files for this revision

Inspect these before writing any code:

```
src/forge_eval/stages/capture_estimate.py
src/forge_eval/services/capture_counts.py
src/forge_eval/services/chao1.py
src/forge_eval/services/ice.py
src/forge_eval/services/capture_selection.py
src/forge_eval/services/capture_summary.py
src/forge_eval/schemas/capture_estimate.schema.json
tests/test_capture_estimate_stage.py
```

### Install posture

```bash
# Networked / default
pip install -e .

# Offline / pre-provisioned
pip install --no-build-isolation -e .
```

### Run tests

```bash
pytest tests/test_capture_estimate_stage.py -v
pytest tests/ -v  # full suite after revision
```

---

## IMPLEMENTATION PROMPT — EXECUTE THIS

You are implementing a **bounded revision to Forge Eval Pack J** to add **Chao2** as a third hidden-defect estimator alongside the existing Chao1 and ICE estimators.

Do not redesign the eval system.
Do not touch Pack K, L, or M.
Do not remove Chao1 or ICE.
Do not build a statistical abstraction layer.
Keep this revision small, explicit, and governance-clean.

---

### Step 1 — Inspect current Pack J

Read these files before writing any code:

- `src/forge_eval/stages/capture_estimate.py`
- `src/forge_eval/services/capture_counts.py`
- `src/forge_eval/services/chao1.py`
- `src/forge_eval/services/ice.py`
- `src/forge_eval/services/capture_selection.py`
- `src/forge_eval/services/capture_summary.py`
- `src/forge_eval/schemas/capture_estimate.schema.json`
- `tests/test_capture_estimate_stage.py`

In your output, explain:
- What counts Pack J currently derives (f1, f2, histogram, ICE rare/frequent split)
- What the current sampling/incidence interpretation is
- Exactly where Chao2 should attach (what counts it will consume)
- What the current `capture_estimate.json` shape looks like

Do not write any code in this step. Understand the system first.

---

### Step 2 — Implement Chao2 service

Add a new file: `src/forge_eval/services/chao2.py`

The Chao2 estimator uses incidence-based data from multiple sampling units (reviewers). In Pack J, each reviewer is a sampling unit and each defect is a species.

**Chao2 formula:**

```
Q1 = number of defects detected by exactly 1 reviewer (uniques)
Q2 = number of defects detected by exactly 2 reviewers (duplicates)
m  = number of sampling units (reviewers with usable coverage)

If Q2 > 0:
    chao2_hidden = ((m - 1) / m) * (Q1^2 / (2 * Q2))

If Q2 == 0 and Q1 > 0:
    chao2_hidden = ((m - 1) / m) * (Q1 * (Q1 - 1) / 2)  # conservative guard

If Q1 == 0:
    chao2_hidden = 0.0  # no singletons, no hidden pressure signal
```

The service must:
- Accept `q1` (int), `q2` (int), `m` (int, usable reviewer count), and `round_digits` (int)
- Compute Chao2 deterministically
- Return a result dict with: `enabled`, `available`, `hidden_estimate`, `total_estimate`, `guard_flags`, `inputs_used`
- Set `available: false` with `reason_unavailable` when:
  - `m < 2` (not enough sampling units for Chao2 to be meaningful)
  - inputs are negative or nonsensical
- Set guard flags explicitly when Q2 == 0 fallback is used
- Never divide by zero
- Never emit a hidden estimate from invalid inputs
- Round all float outputs using `round_digits`

Keep the service small. No class hierarchy. A function or two is fine.

---

### Step 3 — Derive Q1, Q2, m for Chao2 from existing Pack J counts

Chao2 needs Q1, Q2, and m derived from the existing Pack J incidence data.

These map as follows:
- **Q1** = number of defects with `support_count == 1` (seen by exactly 1 reviewer) — this is the existing `f1` count or derivable from the histogram
- **Q2** = number of defects with `support_count == 2` (seen by exactly 2 reviewers) — this is the existing `f2` count or derivable from the histogram
- **m** = number of usable reviewers (reviewers with `usable: true` in the telemetry matrix)

Wire these derivations into `capture_counts.py` or `capture_estimate.py` — wherever is cleanest given what you find in Step 1. Do not invent new data structures if existing ones already carry the needed values.

---

### Step 4 — Extend schema and artifact contract

Update `src/forge_eval/schemas/capture_estimate.schema.json` to add:

**Inside `estimators`:** Add a `chao2` block parallel to the existing `chao1` and `ice` blocks.

Required fields for `chao2`:
- `enabled` (boolean)
- `available` (boolean)
- `hidden_estimate` (number or null)
- `total_estimate` (number or null)
- `guard_flags` (object with explicit boolean fields)
- `inputs_used` (object recording q1, q2, m actually used)
- `reason_unavailable` (string or null)

**Inside `summary`:** Add or confirm these fields exist:
- `selection_policy` (string, value: `"max_hidden"`)
- `selected_method` (string — which estimator was selected)
- `selected_hidden` (number)
- `selected_total` (number)
- `unavailable_estimators` (array of strings, can be empty)

Preserve strict schema behavior (`additionalProperties: false` at root and on nested objects where it already exists). Update any schema tests in `tests/test_schemas.py` if needed.

---

### Step 5 — Update selection logic

Update `src/forge_eval/services/capture_selection.py` (or wherever selection currently lives) so that:

1. All three estimators are computed: Chao1, Chao2, ICE
2. All three outputs are recorded in the artifact
3. One fixed deterministic rule selects the governing hidden estimate:
   - `selection_policy = "max_hidden"`
   - `selected_hidden = max(chao1_hidden, chao2_hidden, ice_hidden)` among **available** estimators only
   - `selected_method` records which estimator won
4. Unavailable estimators are recorded in `unavailable_estimators` — never silently dropped

No discretionary selection. No case-by-case heuristics. The rule is `max_hidden`, always.

---

### Step 6 — Add tests

Add tests to `tests/test_capture_estimate_stage.py` (or a new focused file if it gets crowded):

Required test cases:

1. **Chao2 positive calculation** — valid Q1, Q2, m inputs produce correct deterministic hidden estimate
2. **Chao2 Q2=0 guard** — Q2==0 with Q1>0 uses the fallback formula and sets guard flag
3. **Chao2 unavailable** — m < 2 marks Chao2 unavailable with explicit reason, does not fail the stage
4. **Selection policy — Chao2 wins** — set up inputs where Chao2 produces the highest hidden estimate and confirm it is selected
5. **Selection policy — Chao1 wins** — set up inputs where Chao1 produces the highest hidden estimate
6. **Selection policy — ICE wins** — set up inputs where ICE produces the highest hidden estimate
7. **Unavailable estimator recording** — when Chao2 is unavailable, it appears in `unavailable_estimators` in the artifact
8. **Schema validation** — revised `capture_estimate.json` with Chao2 block validates against the updated schema
9. **Schema rejection** — malformed Chao2 block (missing required field) fails schema validation
10. **Determinism** — run Pack J twice with identical inputs, confirm byte-identical `capture_estimate.json` output

All tests must pass. No skipped tests.

---

### Step 7 — Update docs

Update the following doc files:

- `doc/system/15-capture-estimate-stage.md` — primary Pack J doc
  - Add Chao2 to the estimator list
  - Document the Q1/Q2/m incidence interpretation for Chao2
  - Explain why Chao2 was added (incidence/sample alignment)
  - Explain why Chao1 is retained (conservative comparator)
  - Explain the fixed `max_hidden` selection rule
  - Document that estimator execution evidence is recorded in the artifact
- `README.md` — update Pack J description if it lists estimators explicitly
- Any schema/validation chapter that lists Pack J estimator contents

After updating docs, rebuild assembled docs:

```bash
bash doc/system/BUILD.sh
```

Confirm the build succeeds and `doc/feSYSTEM.md` is updated.

---

### Step 8 — Write revision report

Write a report to:

```
reports/forge_eval_pack_j_chao2_revision_report_rev1.md
```

Use exactly this structure:

```markdown
# Forge Eval Pack J Chao2 Revision Report (Rev 1)

## 1. Executive verdict
[One of: Implemented | Implemented with gaps | Partially implemented | Blocked]

## 2. Current Pack J baseline
[Starting estimator set, artifact shape, counts derivation — what existed before this revision]

## 3. Chao2 implementation
- Files changed
- Sampling unit / incidence interpretation used
- Q1, Q2, m derivation from existing Pack J counts
- Guard/fallback behavior (Q2==0 case, m<2 unavailable case)

## 4. Schema and artifact changes
- Schema file updated
- New fields added to `estimators.chao2`
- New fields added to `summary`
- Validation behavior

## 5. Selection policy
- Policy: max_hidden
- How selected_method is determined
- How unavailable estimators are recorded
- Execution evidence in artifact

## 6. Test and verification results
- Exact pytest commands run
- Test counts and results
- Determinism check result (byte-identical artifact on repeated runs)

## 7. Documentation updates
- Files changed
- Doc rebuild command and result

## 8. Remaining open items
[Only confirmed unresolved items — none if complete]

## 9. Recommended next actions
[Minimal and real — e.g. "Run full A-M pipeline integration test against DataForge target"]
```

---

### Acceptance criteria

You are done only when all of the following are true:

- [ ] `src/forge_eval/services/chao2.py` exists and is correct
- [ ] Chao2 is wired into `capture_estimate` stage and emitted in `capture_estimate.json`
- [ ] Schema updated — `estimators.chao2` block and `summary` execution-evidence fields present
- [ ] Selection logic uses `max_hidden` across all available estimators deterministically
- [ ] Estimator execution evidence is recorded (all three estimator outputs + selection policy + selected_method)
- [ ] All 10 required tests pass
- [ ] Repeated identical runs produce byte-identical `capture_estimate.json`
- [ ] `doc/system/15-capture-estimate-stage.md` updated
- [ ] `bash doc/system/BUILD.sh` succeeds
- [ ] `reports/forge_eval_pack_j_chao2_revision_report_rev1.md` written to disk

If you cannot fully complete the revision, be explicit about what remains incomplete and still deliver the strongest partial revision possible. Do not claim completion if any acceptance criterion is unmet.

---

### What NOT to do

- Do not redesign Pack J from scratch
- Do not remove Chao1 or ICE
- Do not invent a general statistical framework or abstract estimator class hierarchy
- Do not touch Pack K, L, or M — they are downstream and already implemented
- Do not blur the evidence boundary — `forge-evidence` is real but not invoked in Pack J; Pack M is where it enters the pipeline
- Do not emit a clean-looking Chao2 estimate from invalid or sparse inputs
- Do not add clock fields to the artifact
- Do not use non-deterministic operations (random, UUID without seed, etc.)

---

Proceed now. Start with Step 1 — read the source files before writing any code.
