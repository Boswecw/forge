# BDS AI-Assisted Development Operations Protocol

**Date:** April 2, 2026  
**Time:** 12:35 PM America/New_York

---

## Intended destination

`01-company-core/ai-assisted-operations/BDS_AI_ASSISTED_DEVELOPMENT_OPERATIONS_PROTOCOL.md`

---

## Purpose

This protocol defines how BDS uses AI inside development work without allowing AI usage to erode engineering discipline, documentation truth, test integrity, security posture, or operator authority.

The purpose is not to maximize AI output volume.

The purpose is to make AI use:

- governed
- reviewable
- test-bounded
- security-bounded
- documentation-aligned
- useful inside a real single-operator engineering environment

This protocol assumes a **local-first**, **single-operator**, **Ubuntu-terminal-driven** operating model on the development machine.

---

## Core doctrine

### 1. Human authority is absolute

AI may assist.
AI does not own truth.
AI does not approve its own changes.
AI does not define architectural authority.
AI does not redefine system boundaries.

The operator remains the final authority for:

- architecture
- implementation acceptance
- merge readiness
- release readiness
- doctrine acceptance
- risk acceptance
- final documentation truth

### 2. AI is an accelerator, not an authority surface

AI is used to accelerate work that already has a governed structure.

AI must never become a substitute for:

- architectural reasoning
- testing proof
- boundary verification
- security review
- documentation maintenance
- change-control discipline

### 3. Evidence beats output

An AI suggestion is not accepted because it looks correct.
It is accepted only when supported by evidence such as:

- passing tests
- schema validation
- contract verification
- deterministic checks
- manual review against protocol
- successful local runtime behavior
- updated canonical documentation where required

### 4. Local-first usage is preferred by default

When practical, BDS should prefer:

- local models
- local tools
- local repo context
- local documentation grounding
- local terminal execution
- local validation

Cloud AI use is allowed where useful, but must remain bounded by governance, cost, security, and documentation rules.

### 5. AI must operate inside existing doctrine

AI-assisted development must obey all established BDS doctrine, including:

- architecture and systems design
- backend engineering
- frontend and UX/UI engineering
- security and hardening
- testing and verification
- release and change-control
- documentation lifecycle and drift

This protocol is downstream of those protocols, not above them.

---

## Scope

This protocol governs AI use in:

- architecture planning
- implementation planning
- coding assistance
- refactoring assistance
- debugging assistance
- test generation planning
- documentation drafting
- documentation reconciliation
- review preparation
- release preparation
- local operational support

This protocol applies whether AI is accessed through:

- ChatGPT
- Claude
- Codex-style tools
- local model runners
- agentic systems
- repo assistants
- internal assistance surfaces

---

## Allowed AI roles

### 1. Drafting role

AI may draft:

- protocols
- plans
- implementation outlines
- route scaffolds
- model scaffolds
- schema candidates
- test candidates
- documentation candidates
- review summaries

Drafted output is always provisional until reviewed.

### 2. Analysis role

AI may analyze:

- repo structure
- code organization
- likely gaps
- likely drift
- dependency posture
- test posture
- failure patterns
- documentation inconsistencies

Analysis is advisory unless confirmed.

### 3. Translation role

AI may translate between:

- architecture and implementation language
- doctrine and concrete action steps
- test failures and likely cause areas
- raw technical material and operator-readable summaries

### 4. Review-support role

AI may support review by:

- identifying likely risk areas
- proposing test targets
- surfacing contract concerns
- flagging missing documentation updates
- comparing intended versus implemented behavior

### 5. Controlled generation role

AI may generate code or documents when bounded by:

- explicit file target
- explicit subsystem boundary
- explicit acceptance criteria
- explicit validation path

---

## Disallowed AI roles

AI must not be treated as:

### 1. Autonomous architecture authority

AI may not unilaterally:

- redefine subsystem ownership
- collapse boundaries
- invent new authority lines
- replace canonical architecture with convenience patterns

### 2. Unverified merge authority

AI-generated code may not be accepted without:

- review
- validation
- testing appropriate to the change

### 3. Documentation truth authority

AI may help draft docs, but it may not declare documentation canonical by itself.

### 4. Secret handling authority

AI may not be trusted as the authoritative handling path for:

- secret storage
- secret transport
- credential governance
- vault policy

### 5. Silent fixer

AI must not make hidden or poorly explained changes that cannot be traced by the operator.

---

## Approved operating modes

### Mode 1 — Planning assist

Used for:

- protocol drafting
- roadmap construction
- build sequencing
- architecture review preparation

Requirements:

- output must remain aligned to current doctrine
- intended destination must be stated for documents
- planning must distinguish current reality vs future design

### Mode 2 — Implementation assist

Used for:

- code scaffolds
- file rewrites
- migration drafts
- route/controller/service skeletons
- test scaffolds

Requirements:

- exact target file/path must be known
- output must respect repo-local conventions
- operator validates before acceptance
- tests/checks must follow

### Mode 3 — Documentation assist

Used for:

- canonical doc drafting
- system doc module drafting
- reconciliation support
- drift analysis support
- handoff writing

Requirements:

- canonical vs snapshot facts must remain distinct
- generated docs must include Date and Time
- intended destination must be stated
- docs must not overwrite truth without review

### Mode 4 — Review assist

Used for:

- code review prep
- architectural review prep
- test coverage reasoning
- protocol compliance review

Requirements:

- AI findings are hypotheses
- evidence must be gathered before adoption

### Mode 5 — Local operator support

Used for:

- Ubuntu terminal guidance
- copy/paste-safe command sequencing
- repo navigation support
- command explanation

Requirements:

- steps must be explicit
- commands must be minimal and safe
- guidance must match the real local environment

---

## Prompt governance for development work

Every meaningful AI development request should be bounded by as much of the following as possible:

- system or repo name
- exact objective
- current state
- target state
- constraints
- files involved
- acceptance checks
- known non-goals

Good AI-assisted development prompts should reduce ambiguity, not invite improvisation.

### Required prompt qualities

Prompts for real implementation work should prefer:

- exact file paths
- exact subsystem names
- explicit constraints
- fail-closed assumptions
- current environment reality
- explicit next step

### Prompt anti-patterns

Avoid prompts that are:

- vague
- architecture-blind
- unconstrained
- detached from repo truth
- detached from documentation truth
- detached from testing expectations

---

## Context grounding rules

AI-assisted development should be grounded in real project context before high-impact output is accepted.

Approved grounding sources include:

- current repo files
- canonical protocol files
- system documentation
- current test outputs
- current migration state
- current environment configuration
- operator-provided local context

Ungrounded generation is allowed only for clearly marked brainstorming or provisional planning.

---

## Code generation rules

### 1. Generate into known boundaries

AI-generated code should target known files, known modules, or clearly defined new files.

### 2. Do not blur layers

Generated code must not collapse layers such as:

- UI and secret management
- service logic and persistence authority
- orchestration and durable truth
- documentation truth and implementation guesses

### 3. Preserve established patterns

Generated code should match the repo’s actual posture.

That includes where relevant:

- language version
- framework conventions
- architectural layering
- typing style
- schema discipline
- existing naming patterns
- local operational assumptions

### 4. Prefer full-file replacements when the workflow requires it

For copy/paste workflows, full exact replacement files are preferred over partial ambiguous snippets.

### 5. Generated code is provisional until validated

No AI-generated code should be treated as correct before checks run.

---

## Testing obligations for AI-generated work

Any AI-assisted implementation that changes behavior must trigger appropriate testing thought.

### Minimum expectation

For every substantive change, determine:

- what could break
- what must be tested
- what current tests already cover
- what new tests are needed

### Required rule

AI-generated code must never be treated as self-validating.

### Typical validation surfaces

Depending on the change, validation may include:

- unit tests
- integration tests
- schema validation
- migration checks
- local runtime checks
- API contract checks
- linting
- type checks
- manual UI verification
- deterministic artifact verification

---

## Documentation obligations for AI-generated work

AI-assisted work must not increase documentation drift.

If a change affects:

- architecture
- interfaces
- authority boundaries
- lifecycle rules
- operational posture
- configuration truth
- testing truth
- handoff truth

then documentation impact must be reviewed.

### Documentation rule

If implementation changes structural truth, documentation update is part of completion.

### Required doc behavior

AI-generated documentation must:

- include Date and Time
- state intended destination when delivered as a planning/protocol artifact
- distinguish canonical truth from snapshot facts where applicable
- avoid overstating implementation reality

---

## Security rules for AI-assisted work

### 1. Never let convenience override security boundaries

AI suggestions that weaken:

- auth boundaries
- secret handling
- permission enforcement
- fail-closed behavior
- validation requirements

must be rejected.

### 2. Do not trust generated security claims automatically

Any security-sensitive suggestion requires heightened review.

### 3. Avoid leaking operational secrets into broad-context prompts when unnecessary

Use minimum necessary secret exposure.

### 4. Security-sensitive changes require explicit review posture

This includes work touching:

- credentials
- auth flows
- encryption
- token logic
- access control
- boundary enforcement
- approval workflows

---

## Drift control rules

AI can introduce drift in at least five ways:

1. code that no longer matches docs
2. docs that no longer match code
3. plans that no longer match current architecture
4. tests that no longer match behavior
5. naming and boundary erosion over repeated AI sessions

### Anti-drift requirements

To reduce AI-induced drift:

- ground on current files before major edits
- preserve naming consistency
- preserve architectural boundaries
- update related docs when truth changes
- prefer deterministic build/check steps after changes
- treat AI summaries as provisional until compared with reality

---

## Single-operator doctrine

Because this environment is single-operator, AI usage must help reduce overload without weakening discipline.

This means AI should help with:

- compression of complex material
- sequencing of next steps
- draft generation under constraints
- structured review assistance
- documentation maintenance support

But it must not create:

- hidden complexity
- unreviewed sprawl
- uncontrolled branching plans
- false confidence

The standard is not maximum automation.
The standard is maximum useful leverage under disciplined control.

---

## Local terminal support doctrine

Because implementation is currently being done through Ubuntu terminal work on the dev machine, AI-assisted operational guidance should:

- assume real terminal execution
- prefer short explicit commands
- minimize brittle multi-line terminal payloads when possible
- support copy/paste-safe workflow
- keep steps sequential and testable

Where command sequences are given, they should be:

- explicit
- environment-aware
- minimal
- ordered

---

## Acceptance rules for AI-assisted outputs

AI-assisted output may be accepted only when all applicable conditions are satisfied.

### Acceptance checklist

1. the output fits the system boundary
2. the output fits repo conventions
3. the output does not violate doctrine
4. the output is understandable by the operator
5. the output passes required checks
6. the output does not create unacknowledged drift
7. documentation has been considered where needed
8. security posture is preserved

If any of these fail, the output remains provisional or is rejected.

---

## Review classes for AI-generated changes

### Class A — Low-risk drafting

Examples:

- prose cleanups
- planning drafts
- internal note structure
- non-authoritative summaries

Review level:

- normal operator review

### Class B — Moderate implementation support

Examples:

- route scaffolds
- component scaffolds
- test scaffolds
- documentation module drafting

Review level:

- operator review plus local validation

### Class C — High-impact system changes

Examples:

- auth changes
- schema changes
- migration changes
- lifecycle/state logic
- release path changes
- boundary changes
- security-sensitive logic

Review level:

- elevated review posture
- explicit validation steps
- documentation impact review

---

## Standard workflow for AI-assisted development

### Phase 1 — Frame

Define:

- subsystem
- goal
- current state
- constraints
- files or surfaces involved

### Phase 2 — Ground

Gather:

- current code truth
- current doc truth
- current test truth
- current environment truth

### Phase 3 — Generate

Use AI to draft:

- plan
- code
- tests
- docs
- review notes

### Phase 4 — Verify

Run:

- checks
- tests
- schema validation
- manual inspection
- doc comparison

### Phase 5 — Reconcile

Update:

- docs
- handoff notes
- drift-sensitive records
- next-step plans

### Phase 6 — Accept or reject

The operator decides whether the change is accepted, revised, or discarded.

---

## Failure modes to watch for

Common AI-assisted development failure modes include:

- confident but wrong code
- repo-pattern mismatch
- framework-version mismatch
- hidden drift from outdated assumptions
- incomplete file changes
- missing validation logic
- invented APIs or paths
- documentation overclaiming
- skipped test reasoning

This protocol treats those as expected hazards that must be actively controlled.

---

## Enforcement posture

This protocol should be enforced through practice, templates, reviews, and workflow expectations.

Recommended enforcement mechanisms:

- prompt templates for implementation work
- copy/paste-safe review workflow
- protocol-aware planning canvases
- documentation destination discipline
- explicit testing follow-through
- explicit acceptance checklist use

---

## Final rule

AI-assisted development at BDS is only successful when it increases speed **without reducing truth, safety, test rigor, or operator control**.

If speed is gained by weakening those things, the AI usage is out of policy.

---

## Status

This document is intended to serve as the canonical BDS doctrine for AI-assisted development operations within the company-core protocol stack.

