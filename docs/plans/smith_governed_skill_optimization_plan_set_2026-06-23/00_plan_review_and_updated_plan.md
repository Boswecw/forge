# SMITH-Governed Skill Optimization Plan

Date: 2026-06-23
Status: Initial plan, board review, and revised implementation plan
Scope: Forge ecosystem skill-optimization governance

## Part 1 - Initial Plan

### 1. Purpose

Create a governed skill-optimization loop for Forge where agent skills can improve through evidence, frozen cases, bounded edits, and operator promotion without allowing agents to directly rewrite canonical rules or production behavior.

The working doctrine:

- Agents may propose skill edits.
- Evaluators may score candidate skill variants.
- DataForge stores evidence, rejected edits, accepted edits, and lineage.
- Forge_Command exposes review and promotion.
- SMITH remains the governance authority.
- AuthorForge consumes only promoted skills.

### 2. Problem

Current Forge skill and operating-procedure artifacts can be manually improved, but there is no first-class loop for:

- turning failed trajectories into candidate skill patches,
- measuring whether a skill patch improves a frozen eval set,
- preserving rejected edits as negative evidence,
- validating against held-out cases,
- promoting a skill only after governed review,
- proving that production apps consume only accepted skill versions.

Without this loop, skill improvement risks becoming ad hoc, non-repeatable, and hard to audit.

### 3. Target Architecture

The loop spans five systems:

| System | Responsibility |
| --- | --- |
| `neuronforge-local-operator` | Local experiment runner, baseline evals, candidate skill generation, train/validation execution |
| DataForge Local / Cloud | Durable skill-eval evidence, trajectory receipts, rejected edits, promotion receipts, lineage graph |
| Forge_Command | Operator review, promotion queue, dry-run validation, approval/rejection surface |
| NeuroForge | Optional cloud reflection/optimizer lane for expensive analysis, not promotion authority |
| AuthorForge | Consumer of promoted continuity/progression skills only |

### 4. First Target Lane

The first target should be `continuity-progression-reasoning`.

Reasons:

- already bounded by scene-local, adjacent-scene, and scene-window scopes,
- already candidate-only,
- already expects strict structured output,
- already requires evidence spans, confidence, uncertainty, and review notes,
- already has a frozen case-pack concept,
- false positives are a known and measurable risk,
- production consumption can remain read-only until trust improves.

### 5. Core Artifacts

Initial schema family:

- `SkillSpec.v1`
- `SkillCandidate.v1`
- `SkillEvalCase.v1`
- `SkillEvalRun.v1`
- `SkillPromotionReceipt.v1`

Second-stage schema family:

- `SkillPatch.v1`
- `RejectedSkillEdit.v1`
- `SkillRegressionReport.v1`
- `SkillConsumerCompatibilityReport.v1`

### 6. Candidate Flow

1. Establish a baseline skill file and immutable skill id.
2. Freeze train and validation eval packs.
3. Run the baseline skill through all train and validation cases.
4. Generate a candidate skill edit from failed or weak runs.
5. Enforce a bounded edit budget.
6. Run candidate against train cases.
7. Run candidate against held-out validation cases.
8. Run regression check against prior accepted skill.
9. Emit candidate package and evaluation receipt.
10. Queue package in Forge_Command.
11. Operator approves, rejects, or requests revision.
12. Promotion writes only to canonical skill location after approval.
13. AuthorForge consumes only the promoted skill version.

### 7. Bounded Edit Rules

Candidate edits must be:

- small,
- diffable,
- attributable to concrete failing eval evidence,
- reversible,
- linked to skill version and eval run ids,
- forbidden from modifying canonical docs directly,
- forbidden from modifying production AuthorForge behavior.

Allowed first-stage edits:

- add a decision rule,
- clarify evidence-span requirements,
- downgrade confidence rules,
- add explicit false-positive restraint instructions,
- adjust structured-output field guidance.

Forbidden first-stage edits:

- large rewrites,
- new product behavior,
- new runtime permissions,
- new model-provider routing,
- direct `doc/system` mutation,
- direct AuthorForge mutation,
- unreviewed promotion.

### 8. Initial Command Shape

```bash
forge-skillopt run \
  --skill skills/authorforge/continuity-progression-reasoning.skill.md \
  --train evals/continuity/train \
  --validation evals/continuity/validation \
  --budget 4 \
  --output docs/plans/skill-opt/candidates/
```

Promotion surface:

```bash
forge-smith verify skill-candidate
forge-command promote-skill
```

### 9. Initial Milestones

#### Milestone 0 - Intake and Alignment

- Locate current continuity/progression lane docs, eval docs, existing prompt/skill files, and promotion seams.
- Confirm the canonical target location for experimental versus promoted skills.
- Confirm that `doc/system` remains a canonical mirror, not an optimizer target.

#### Milestone 1 - Eval Pack Hardening

- Convert the continuity/progression case pack into structured JSON cases.
- Fill source packet references.
- Split cases into train, validation, and regression groups.
- Define scoring rubric.
- Add schema validation for eval cases.

#### Milestone 2 - Baseline Runner

- Build a deterministic local runner in `neuronforge-local-operator`.
- Capture model id, skill version, prompt hash, input hash, output hash, and validator result.
- Emit `SkillEvalRun.v1`.
- Produce a baseline report.

#### Milestone 3 - Candidate Skill Package

- Generate candidate skill edits as patch packages only.
- Enforce edit budget and forbidden-path policy.
- Store accepted and rejected candidate packages as evidence.

#### Milestone 4 - Forge_Command Review

- Add a read-only candidate queue first.
- Show diff, score movement, failed cases, risk notes, and validation receipts.
- Add approval only after dry-run proof exists.

#### Milestone 5 - Promotion

- Promote only through SMITH/Forge_Command.
- Write `SkillPromotionReceipt.v1`.
- Preserve old skill version.
- Make AuthorForge consume only promoted skill versions.

## Part 2 - Board Review

### Senior Engineer Review

What is strong:

- The candidate-only posture is clear.
- The plan starts with one bounded lane instead of broad system-wide optimization.
- The artifact flow is diffable and testable.

What is weak:

- The initial command names imply tools that may not exist yet.
- The plan does not define the exact runner interface or output validator contract.
- The baseline skill file location is assumed, not discovered.

What is missing:

- Concrete module boundaries inside `neuronforge-local-operator`.
- Definition of deterministic replay requirements.
- Failure behavior when the local model is unavailable or nondeterministic.

What is risky:

- Building optimizer behavior before the eval runner is trustworthy.
- Treating markdown skill deltas as easy to validate; natural-language edits can have broad side effects.

What should change immediately:

- Add a foundation phase that builds schema validation, baseline replay, and reports before any candidate-generation automation.

### Senior Architect Review

What is strong:

- The authority boundary is correctly separated: NLO experiments, DataForge evidence, Forge_Command promotion, AuthorForge consumption.
- Promotion is explicitly not automatic.

What is weak:

- The plan does not state whether skills are per-app, per-lane, per-model, or per-contract artifacts.
- It does not define the canonical relationship between `SkillSpec`, task contracts, lane contracts, and model profiles.

What is missing:

- A versioning model.
- Compatibility rules for consumers.
- A rollback story.
- A trust-state lifecycle.

What is risky:

- Skill versions may drift from runtime task contracts.
- A promoted skill could improve eval scores while breaking a downstream consumer expectation.

What should change immediately:

- Define skill identity, versioning, compatibility, lifecycle states, and rollback before implementation.

### Senior Repository Specialist Review

What is strong:

- The plan keeps experiments out of `doc/system`.
- It keeps AuthorForge out of the experimental mutation path.

What is weak:

- The plan suggests paths like `docs/plans/skill-opt/candidates/` but does not define repo ownership.
- It does not specify which repo owns schemas versus generated candidate packages.

What is missing:

- A repository layout table.
- Allowed-write and forbidden-write policies.
- Generated artifact ignore/retention policy.
- Cleanup rules for stale candidates.

What is risky:

- Candidate files can sprawl across repos.
- Experimental artifacts could be mistaken for canonical skill files.

What should change immediately:

- Add a repo map with exact ownership: NLO owns experiments and evals; shared schemas live in NLO first; Forge_Command mirrors only review contracts; AuthorForge receives promoted consumer copies only.

### Senior QA / Verification Engineer Review

What is strong:

- The plan recognizes false positives and held-out validation.
- It separates train, validation, and regression.

What is weak:

- Scoring is underdefined.
- It does not define pass thresholds.
- It does not define test-case invalidation or replacement protocol.

What is missing:

- Golden expected outputs or rubric-judge rules.
- Schema-validity gate.
- Confidence-calibration metrics.
- False-positive cap.
- Regression gate against prior accepted skill.

What is risky:

- A candidate could improve aggregate score while worsening high-risk false positives.
- Held-out cases can become contaminated if repeatedly inspected during optimization.

What should change immediately:

- Define hard gates: schema validity must be 100 percent, false-positive regressions block promotion, and validation improvement must exceed a minimum threshold.

### Senior DevOps / Platform Engineer Review

What is strong:

- The plan starts local-first and does not require cloud infrastructure for the first loop.
- It preserves optional NeuroForge escalation.

What is weak:

- Runtime dependencies are vague.
- It does not define CI or local command entrypoints.
- It does not define where receipts are stored when DataForge Local is offline.

What is missing:

- Make targets or scripts.
- Environment variables.
- Timeout and retry policy.
- Artifact retention policy.
- Offline degraded behavior.

What is risky:

- Local model availability can make verification flaky.
- Long-running eval loops could become expensive or unusable in developer workflows.

What should change immediately:

- Add a mock/deterministic runner mode and a real-model runner mode, with CI using deterministic fixtures first.

### Senior Security / Risk Engineer Review

What is strong:

- The plan blocks direct self-promotion.
- It explicitly forbids direct mutation of production AuthorForge behavior.

What is weak:

- It does not define prompt-injection handling for trajectory-derived reflections.
- It does not define what content can be sent to cloud reflection jobs.
- It does not define permission enforcement beyond policy language.

What is missing:

- Trust boundary table.
- Data classification for manuscript text, prompts, trajectories, and eval packets.
- Allowlist enforcement for paths and commands.
- Redaction policy for cloud escalation.

What is risky:

- Failed trajectories may contain untrusted content that tries to influence skill edits.
- A cloud optimizer could see private manuscript text unless escalation is explicitly constrained.

What should change immediately:

- Treat all trajectories, model outputs, and proposed patches as untrusted input. Add path allowlists, schema validation, and cloud-redaction rules before optimizer work.

### Senior Product / UX Systems Review

What is strong:

- Operator approval is explicit.
- The review surface can present concrete evidence instead of vague improvement claims.

What is weak:

- The plan does not define the operator workflow in enough detail.
- It does not say how to make score changes understandable.
- It does not define how review burden stays manageable.

What is missing:

- Candidate summary layout.
- Diff explanation.
- Case-level failure drilldown.
- Rejection reason capture.
- Compare-to-current accepted skill view.

What is risky:

- Operators may approve based on a single aggregate score without seeing high-risk failures.
- Too many candidate patches will create review fatigue.

What should change immediately:

- Design the Forge_Command review card around "why this candidate exists", "what improved", "what regressed", "what risks remain", and "what exact files would change".

### Senior Data / Schema / Contract Engineer Review

What is strong:

- The schema family is directionally right.
- The plan recognizes lineage and receipts.

What is weak:

- Too many schemas are listed before their minimum fields are known.
- Relationship cardinality is not defined.
- It does not define immutable ids or hash contracts.

What is missing:

- JSON schema definitions.
- Required ids and hashes.
- Run-to-case-to-output relationships.
- Candidate-to-patch-to-promotion relationships.
- Rejected edit semantics.

What is risky:

- Evidence may be stored but not queryable.
- Promotion receipts may not be enough to reconstruct why a skill was accepted.

What should change immediately:

- Start with four schemas only: `SkillSpec.v1`, `SkillEvalCase.v1`, `SkillEvalRun.v1`, and `SkillCandidate.v1`. Add promotion receipt only once review flow exists.

### Senior Maintainer / Long-Term Evolution Review

What is strong:

- The plan avoids immediate framework sprawl by choosing one lane.
- It keeps the first target close to existing Forge doctrine.

What is weak:

- It does not define when a skill should be retired, superseded, or split.
- It does not define how future lanes inherit the framework.
- It does not define maintenance ownership.

What is missing:

- Deprecation policy.
- Ownership policy.
- Migration strategy for old skill versions.
- Compatibility matrix across models and consumers.

What is risky:

- The system could produce many near-duplicate skills with unclear authority.
- Future maintainers may not know which skill version is safe to use.

What should change immediately:

- Add lifecycle states and ownership metadata from the start.

## Part 3 - Cross-Role Synthesis

### Shared Serious Concerns

The strongest shared concern is sequencing. The initial plan moves too quickly from concept to optimizer. The first deliverable must be an evaluation and evidence substrate, not mutation automation.

Second, identity and lifecycle are underdefined. A governed skill needs stable id, version, owner, lane, contract compatibility, model compatibility, state, and rollback metadata.

Third, evidence quality is more important than candidate generation. Without deterministic replay, structured eval cases, scoring rules, and false-positive gates, optimization becomes pseudo-rigorous.

Fourth, trust boundaries need enforcement, not just doctrine. Proposed edits, model outputs, trajectories, and manuscript-derived inputs are untrusted.

### Hidden Issues Across Roles

- Aggregate score improvement can hide safety regressions.
- Held-out validation can be contaminated by repeated manual inspection.
- Natural-language skill edits are hard to constrain unless the diff budget and allowed sections are enforced mechanically.
- Cloud reflection is a privacy risk if manuscript text or raw trajectories are not classified and redacted.
- Operators need evidence summaries, not raw logs.

### Internal Contradictions

- The plan says `doc/system` should not be touched directly, but the initial command emits under `docs/plans` without defining eventual canonical skill promotion location.
- The plan names promotion commands before defining promotion contracts.
- The plan lists many schemas while also trying to start small.

### Likely Execution Failure Points

- Eval cases remain markdown-only and never become executable.
- Candidate generation starts before baseline scoring is stable.
- Forge_Command UI is built before the underlying candidate package format is real.
- DataForge receives partial receipts that cannot reconstruct decisions.
- AuthorForge consumes skill versions without compatibility proof.

### Expensive Later Fixes If Ignored

- Retrofitting lineage after candidates have already been promoted.
- Splitting experimental artifacts from canonical artifacts after repo sprawl.
- Adding privacy boundaries after cloud optimizer jobs have seen sensitive content.
- Adding rollback after consumers depend on an unversioned skill.

## Part 4 - Improvement Plan

### Critical Fixes Before Implementation

1. Define skill identity and lifecycle.
   - Why it matters: every receipt and consumer reference depends on stable identity.
   - Risk reduced: ambiguous authority and untraceable promotion.
   - Concrete action: add `skill_id`, `skill_version`, `lane_id`, `owner`, `state`, `created_at`, `supersedes`, and `compatible_contracts`.

2. Build executable eval cases before optimizer work.
   - Why it matters: optimization without executable cases is manual prompt tweaking.
   - Risk reduced: fake validation.
   - Concrete action: convert continuity/progression cases to JSON with source refs, expected posture, scoring tags, and reviewer notes.

3. Add deterministic fixture mode.
   - Why it matters: CI cannot depend on local model availability.
   - Risk reduced: flaky proof.
   - Concrete action: support fixture outputs and real-model outputs through the same validator.

4. Enforce forbidden write paths.
   - Why it matters: governance cannot rely on convention.
   - Risk reduced: accidental canonical mutation.
   - Concrete action: allow candidate writes only under NLO candidate directories until Forge_Command promotion.

### Important Design Upgrades

1. Separate skill eval from skill mutation.
2. Add rollback and supersession semantics.
3. Treat confidence calibration and false positives as first-class metrics.
4. Add consumer compatibility reports before AuthorForge adoption.

### Repository And Structure Improvements

1. Put first executable work in `ecosystem/local-systems/neuronforge-local-operator`.
2. Put cross-system planning docs in `/docs/plans/active` until implementation starts.
3. Keep `doc/system` untouched until a validated implementation needs canonical mirror updates.
4. Keep generated candidate packages under an explicit candidate directory with retention rules.

### Testing And Verification Upgrades

1. JSON schema validation for all eval cases and run receipts.
2. Unit tests for scorer edge cases.
3. Golden fixture tests for false-positive resistance.
4. Regression test against last accepted skill.
5. Validation gate requiring no high-risk regression.

### Operational And Deployment Upgrades

1. Add local command wrappers before Forge_Command UI.
2. Add timeouts and run budgets.
3. Add offline DataForge fallback receipt storage.
4. Add report generation for operator review.

### Security And Governance Upgrades

1. Mark trajectories, model outputs, and patches untrusted.
2. Add path allowlist enforcement.
3. Add cloud-redaction rules before NeuroForge reflection.
4. Add explicit operator approval for promotion.
5. Preserve rejected edits as negative evidence.

### UX / Operator Workflow Improvements

1. Review cards must show diff, score movement, regressions, and exact target files.
2. Rejection reasons must be captured.
3. High-risk regressions must be shown above aggregate improvement.
4. Approval must require a dry-run receipt.

### Data, Schema, And Contract Improvements

1. Start with four schemas.
2. Add promotion receipt after review flow exists.
3. Add immutable hashes for skill, case input, output, and eval result.
4. Model relationships explicitly: skill -> candidate -> eval runs -> promotion decision.

### Long-Term Maintainability Improvements

1. Define skill retirement.
2. Define ownership per lane.
3. Add compatibility matrix by model, lane, and consuming app.
4. Avoid adding new lanes until continuity/progression proves the full loop.

## Part 5 - Readiness Assessment

This plan is partially ready.

It is not ready for optimizer implementation.

It is ready for an implementation slice that builds the governed evaluation substrate for one lane.

Must be corrected before execution begins:

- lock skill identity and lifecycle fields,
- define repo ownership and allowed writes,
- make continuity/progression eval cases executable,
- define scoring and gates,
- add deterministic fixture mode,
- define trust boundaries and data classification,
- defer Forge_Command promotion UI until candidate packages and reports exist.

## Part 6 - Rewrite Guidance

Rewrite these parts:

- Initial command shape: replace aspirational commands with concrete first-slice scripts.
- Core artifacts: reduce first-stage schema count.
- Candidate flow: split evaluation, candidate generation, review, and promotion into separate phases.
- Milestones: make Milestone 1 executable and measurable.

Split into separate documents later:

- Skill schema contract spec.
- Continuity/progression eval-pack spec.
- NLO runner implementation plan.
- Forge_Command skill-candidate review plan.
- DataForge skill evidence storage contract.
- AuthorForge promoted-skill consumption plan.

Decisions to lock before repo work starts:

- canonical experimental skill directory,
- canonical promoted skill directory,
- first schema locations,
- first scoring thresholds,
- allowed candidate write paths,
- cloud escalation data policy,
- promotion authority wording.

## Part 7 - Updated Plan After Review

### Updated Plan Summary

Build the SMITH-governed skill optimization loop in narrow phases. The first implementation phase does not optimize skills. It makes the continuity/progression lane evaluable, replayable, and governable. Only after baseline proof is stable do candidate skill patches enter the system.

### Phase 0 - Plan Lock And Repository Mapping

Owner: ecosystem planning and NLO implementation lead

Deliverables:

- repo ownership table,
- skill lifecycle table,
- allowed-write policy,
- forbidden-write policy,
- first schema location decision,
- initial continuity/progression skill id.

Required decisions:

- experimental skill candidates live under NLO,
- promoted skills live under the eventual canonical skill location,
- Forge_Command consumes review packages but does not own raw experiment execution,
- AuthorForge consumes promoted skill refs only.

Acceptance gate:

- planning doc identifies exact paths and owners before implementation starts.

### Phase 1 - Minimal Schema Foundation

Owner: NLO

Create:

- `SkillSpec.v1`
- `SkillEvalCase.v1`
- `SkillEvalRun.v1`
- `SkillCandidate.v1`

Required fields:

- stable ids,
- schema version,
- skill version,
- lane id,
- source hashes,
- model id or fixture id,
- eval case id,
- result status,
- score details,
- evidence-span validation,
- confidence-class validation,
- created timestamp.

Acceptance gate:

- schema validation tests pass against valid and invalid fixtures.

### Phase 2 - Continuity/Progression Eval Pack Execution

Owner: NLO

Tasks:

- convert the 16-case continuity/progression pack from markdown posture into JSON cases,
- fill source packet references or mark missing packets as blockers,
- split into train, validation, and regression groups,
- encode expected posture and restraint posture,
- define case invalidation protocol.

Acceptance gate:

- all active cases validate,
- missing source packet refs are either filled or explicitly blocked,
- train/validation/regression split is recorded before any candidate run.

### Phase 3 - Baseline Runner And Report

Owner: NLO

Tasks:

- implement deterministic fixture runner,
- implement real-model runner behind an explicit local command,
- validate outputs against expected structured-output contract,
- compute score components:
  - schema validity,
  - finding correctness,
  - restraint correctness,
  - evidence-span adequacy,
  - confidence calibration,
  - false-positive severity,
  - regression status.

Acceptance gate:

- baseline report is reproducible in fixture mode,
- real-model mode can fail closed without blocking fixture CI,
- baseline report records hashes and run ids.

### Phase 4 - Candidate Package Without Mutation Automation

Owner: NLO

Tasks:

- define `SkillCandidate.v1` package format,
- allow a manually supplied candidate skill patch,
- validate bounded edit policy,
- reject forbidden paths,
- run candidate against train and validation sets,
- compare against baseline.

Acceptance gate:

- candidate package can be accepted or rejected by evaluator logic without writing canonical skill files.

### Phase 5 - DataForge Evidence Storage

Owner: DataForge Local first, DataForge Cloud later

Tasks:

- store eval run summaries,
- store candidate package metadata,
- store rejected candidate reasons,
- store baseline and candidate hashes,
- preserve lineage from skill version to eval cases to candidate result.

Acceptance gate:

- a report can be reconstructed from stored receipts without reading raw transient logs.

### Phase 6 - Forge_Command Read-Only Review Surface

Owner: Forge_Command

Tasks:

- read candidate packages and evaluation reports,
- display score deltas and high-risk regressions,
- display skill diff,
- display case-level drilldowns,
- capture rejection reasons locally.

No approval action in this phase.

Acceptance gate:

- operator can inspect candidate package truth without any repo write or promotion action.

### Phase 7 - Governed Promotion

Owner: Forge_Command / SMITH boundary

Tasks:

- add promotion receipt schema,
- require dry-run receipt,
- require no blocking regression,
- require explicit operator approval,
- write promoted skill only to canonical promoted location,
- preserve previous skill version and rollback metadata.

Acceptance gate:

- a promoted skill has a receipt sufficient to prove source candidate, eval result, approver, target path, and rollback ref.

### Phase 8 - AuthorForge Consumption

Owner: AuthorForge

Tasks:

- consume only promoted skill refs,
- expose degraded/unknown state when promoted skill metadata is missing,
- keep outputs candidate-only,
- add compatibility test proving AuthorForge cannot consume experimental candidate skills.

Acceptance gate:

- AuthorForge test proves experimental skill paths are rejected and promoted skill refs are accepted.

### Updated Execution Order

1. Phase 0: lock repo map and lifecycle.
2. Phase 1: implement minimal schemas.
3. Phase 2: executable eval pack.
4. Phase 3: baseline runner and report.
5. Phase 4: candidate package validation.
6. Phase 5: evidence storage.
7. Phase 6: Forge_Command read-only review.
8. Phase 7: promotion.
9. Phase 8: AuthorForge consumption.

### Updated Hard Gates

- No optimizer before executable eval cases.
- No candidate package before baseline report.
- No Forge_Command approval before read-only review is stable.
- No promotion without dry-run receipt.
- No AuthorForge consumption without consumer compatibility proof.
- No cloud reflection on raw manuscript text without data-classification and redaction rules.
- No direct mutation of `doc/system`.

### Updated First Implementation Slice

Implement only:

- `SkillSpec.v1`,
- `SkillEvalCase.v1`,
- `SkillEvalRun.v1`,
- fixture validation tests,
- continuity/progression case-pack conversion skeleton,
- baseline report skeleton.

Do not implement:

- candidate generation,
- optimizer loops,
- Forge_Command approval,
- promotion writes,
- AuthorForge consumption.

This first slice proves the foundation without creating a self-mutation pathway.
