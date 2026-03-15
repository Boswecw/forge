# Plan / Prompt v1.1 — DF Local Foundation
**Date:** 2026-03-15  
**Revision:** v1.1  
**Change Summary:** Strengthened the original DF Local Foundation plan with senior-level boundary hardening, explicit fail-closed contracts, a narrower control surface, a concrete repo/control-plane posture, and a cleaner first-integration path for app-local authority.

---

# Prompt — Read First

You are implementing **v1.1 of DF Local Foundation** for the Forge ecosystem.

This is a **local-first data substrate and contract surface**, not a cloud service, not a universal business-schema repo, and not a replacement for DataForge.

Its job is to give Forge applications a **shared local data discipline** while preserving **app-owned authority**, **privacy-first operation**, and **bounded operational visibility**.

## READ FIRST — OPERATOR RULES
- Follow the steps exactly, in order.
- Do not invent cloud ownership, cross-app business schemas, or control-plane inspection powers.
- Preserve the doctrine that app-local customer/domain truth remains app-owned.
- Treat ForgeCommand visibility as **declared status only**, never raw database browsing.
- Treat NeuronForge Local as a bounded consumer/producer through contracts, never canonical truth owner.
- Keep the shared core minimal; if a table or module is not clearly cross-app, do not put it in DF Local Foundation.
- Fail closed on suspicious paths, invalid app registration, migration mismatch, restore validation failure, or unauthorized visibility expansion.
- Prefer minimal diffs and structure-sensitive examples only where they reduce ambiguity.
- Add tests and validation surfaces that prove privacy boundaries, deterministic lifecycle behavior, and migration/reporting integrity.
- If repo reality conflicts with this plan, stop and report the mismatch instead of improvising.

## GOAL
Build the first governed implementation path for **DF Local Foundation** as the shared local PostgreSQL control surface for Forge apps. It must standardize local DB lifecycle, migration/reporting posture, coarse health/status contracts, backup/export/restore discipline, and app registration shape — while leaving all app business truth, domain schemas, and authority rules inside the owning app.

## SCOPE
### In scope
- Foundation repo/control-surface definition
- Local PostgreSQL lifecycle conventions
- Config/env contract for local operation
- Migration framework and schema version reporting
- Coarse health/readiness/status contract
- App registration contract
- Backup/export/restore doctrine and initial tooling shape
- Bounded ForgeCommand visibility rules
- Bounded NeuronForge Local read/write contract rules
- First app integration pattern using an app-owned schema attachment model

### Out of scope
- Moving app business schemas into DF Local Foundation
- Making DF Local the cloud billing or entitlement authority
- Giving ForgeCommand customer-data introspection powers
- Turning NeuronForge Local into canonical memory owner
- Replacing DataForge cloud responsibilities
- Full multi-app rollout in the first implementation pass

## FILES TO TOUCH
Adapt to repo reality, but the control surface should roughly land in paths like:

- `df-local-foundation/README.md`
- `df-local-foundation/docs/architecture.md`
- `df-local-foundation/docs/privacy-doctrine.md`
- `df-local-foundation/docs/migration-doctrine.md`
- `df-local-foundation/docs/operational-visibility.md`
- `df-local-foundation/docs/app-integration-contract.md`
- `df-local-foundation/docs/backup-export-restore.md`
- `df-local-foundation/contracts/health.schema.json`
- `df-local-foundation/contracts/app-registration.schema.json`
- `df-local-foundation/contracts/migration-status.schema.json`
- `df-local-foundation/core/lifecycle/*`
- `df-local-foundation/core/config/*`
- `df-local-foundation/core/health/*`
- `df-local-foundation/core/backup/*`
- `df-local-foundation/core/export/*`
- `df-local-foundation/sql/core/0001_core_foundation.sql`
- `df-local-foundation/sql/core/0002_core_metadata.sql`
- `df-local-foundation/tools/db-status`
- `df-local-foundation/tools/db-backup`
- `df-local-foundation/tools/db-restore`
- `df-local-foundation/tools/db-export`
- test/fixture paths required to prove contract behavior

## IMPLEMENTATION STEPS
1. Lock doctrine and boundaries before writing operational code.
2. Create the repo skeleton and documentation/control contracts.
3. Define the minimal shared SQL/core metadata surface.
4. Implement local lifecycle + status/migration reporting.
5. Implement coarse health/readiness surfaces with strict non-goals.
6. Add app registration and compatibility declarations.
7. Add backup/export/restore contract and safety checks.
8. Prove the privacy boundary by ensuring only declared operational state is visible.
9. Integrate the first seed app using app-owned schema attachment.
10. Add NeuronForge Local bounded contract notes and tests.
11. Document hybrid/Pro augmentation rules without mixing billing truth into DF Local.

## ACCEPTANCE TESTS
- Foundation lifecycle start/status/readiness commands run deterministically
  - Expect: clear `ready | degraded | unavailable | migrating` state, with schema/migration metadata only
- Invalid migration state
  - Expect: fail-closed status and no silent promotion to ready
- App registration validation
  - Expect: invalid compatibility or malformed declaration rejected
- Backup/restore validation
  - Expect: restore blocked on integrity/compatibility mismatch
- Privacy boundary tests
  - Expect: no table contents, record counts, project names, or domain metadata exposed via status surfaces
- First app integration test
  - Expect: app-owned schema attaches cleanly without relocating domain authority into core

## DONE WHEN
- [ ] DF Local Foundation has a real repo/control-surface definition
- [ ] shared core is minimal and explicitly bounded
- [ ] lifecycle + migration/status surface exists
- [ ] ForgeCommand visibility is contract-bounded and privacy-safe
- [ ] NeuronForge Local contract is bounded and non-authoritative
- [ ] backup/export/restore posture exists with validation gates
- [ ] one seed app proves the attachment model works
- [ ] hybrid/Pro boundary is explicit and non-confused

---

# Locked Plan — v1.1

## 1. Purpose

Define **DF Local Foundation** as the shared **local-first PostgreSQL control surface** for Forge ecosystem applications.

DF Local Foundation exists to provide:

- privacy by default
- canonical on-device control for local app data
- disciplined local database lifecycle
- consistent migration and status posture
- bounded integration contracts for local AI/runtime consumers
- cleaner future hybrid augmentation paths

It is **not** the cloud DataForge service.  
It is **not** a universal business-schema repo.  
It is **not** a control-plane inspection backdoor.

---

## 2. Strategic Judgment

The original direction remains correct:

**Use a shared DF Local Foundation repo plus app-owned schemas.**

That remains the best balance between:

- cross-app local discipline
- privacy integrity
- reduced lifecycle drift
- app-level ownership
- future portability to hybrid or optional cloud augmentation

The plan is updated here because the first version needed more precision around:

- what the foundation may and may not own
- how ForgeCommand is allowed to see local state
- how NeuronForge Local interacts without becoming truth owner
- what constitutes the minimal shared metadata core
- how restore/export/backups must fail closed
- how first integration should prove the architecture

---

## 3. Non-Negotiable Architectural Rules

### 3.1 Local-first truth rule
Customer and app-domain truth remains local by default.

Cloud behavior is:
- additive
- selective
- opt-in where required
- explicitly policy-bound

### 3.2 App authority rule
Each app owns its own:
- domain schema
- migrations beyond shared core attachment
- repository/service layer
- domain invariants
- promotion/review workflows
- customer-facing business meaning

DF Local Foundation supplies the chassis, not the business ontology.

### 3.3 Control-plane privacy rule
ForgeCommand must consume **declared operational state only**.

ForgeCommand must **not**:
- browse app-local tables
- inspect customer records
- query manuscript/project names
- enumerate record counts
- treat app-local storage as a searchable authority surface

### 3.4 NeuronForge Local boundary rule
NeuronForge Local may:
- read bounded context through defined contracts
- write bounded run/provenance/eval artifacts through defined contracts

NeuronForge Local may **not** become owner of canonical customer memory.

### 3.5 Minimal shared-core rule
Any shared core table or module must justify itself as cross-app discipline.

If it is app business meaning, it does not belong in DF Local Foundation.

### 3.6 Fail-closed rule
The foundation must fail closed on:
- invalid migration state
- compatibility mismatch
- malformed app registration
- restore integrity mismatch
- unauthorized visibility expansion
- suspicious export/import payloads
- unsupported schema attachment shape

Silent fallback is banned.

---

## 4. What DF Local Foundation Owns

DF Local Foundation owns only the parts that should not drift across apps.

### 4.1 Local database lifecycle
- PostgreSQL bootstrap conventions
- init/start/stop/status lifecycle
- readiness checks
- degraded/unavailable/migrating classification
- local port/process ownership rules
- local test harness lifecycle rules

### 4.2 Configuration and environment contract
- canonical env variable names
- local data directory conventions
- connection-string conventions
- dev/test/prod-local profiles
- local secrets handling pattern

### 4.3 Migration framework
- migration tooling choice
- naming rules
- execution order rules
- startup migration posture
- rollback posture
- schema version reporting contract

### 4.4 Shared metadata conventions
- schema naming conventions
- id/timestamp conventions
- created/updated semantics where allowed
- provenance/audit metadata shape where truly cross-app
- retention metadata conventions

### 4.5 Operational visibility contract
- health command/endpoint shape
- migration status reporting
- coarse degraded/unavailable semantics
- backup/export readiness declarations
- ownership mode reporting (`app-local`)

### 4.6 Backup / export / restore foundation
- local backup conventions
- export format conventions
- restore validation rules
- compatibility checks
- operator safety notes

### 4.7 App registration pattern
- app identifier conventions
- compatibility/version declaration shape
- schema attachment declaration shape
- app mode declaration (`local | hybrid | cloud-enabled`)

---

## 5. What DF Local Foundation Must Not Own

DF Local Foundation must not own:

- manuscript content
- lore/business entities
- project/workspace domain truth
- campaign/outreach business tables
- market/watchlist/strategy entities
- app-specific review/promotion semantics
- billing/subscription authority
- generic "one schema to rule them all" abstractions

This is where overreach starts. The updated plan explicitly forbids it.

---

## 6. Shared Core Surface — Keep It Small

The shared core should be intentionally narrow.

### 6.1 Minimal SQL core
Allowed examples:
- `core_app_registry`
- `core_schema_versions`
- `core_backup_log`
- `core_export_log`
- `core_health_events` (only if actually useful)
- `core_provenance_policy` (only if it proves cross-app value)

### 6.2 Tables to reject from core
Do **not** add:
- app business entities
- customer content entities
- generic document stores
- shared “memory” abstractions pretending to help every app
- domain-object tables that belong to an app repo

### 6.3 Design bias
Bias toward **fewer shared tables**, not more.

The foundation should coordinate local posture, not centralize app semantics.

---

## 7. Operational Visibility Contract

This is the **maximum** baseline visibility allowed for control-plane consumption.

### 7.1 Required coarse health/status shape
```json
{
  "status": "ready | degraded | unavailable | migrating",
  "schema_version": "string",
  "expected_schema_version": "string",
  "migration_required": true,
  "last_error_class": "string | null",
  "started_at": "ISO8601 timestamp",
  "db_engine": "postgresql",
  "ownership": "app-local",
  "app_mode": "local | hybrid | cloud-enabled"
}
```

### 7.2 Explicit non-goals
Never expose:
- table contents
- record counts
- project names
- manuscript names
- customer-domain metadata
- query surfaces
- raw table list browsing

### 7.3 Control-plane contract rule
ForgeCommand should consume **app-declared status artifacts**, not database introspection.

That means the app exposes a bounded health/status surface; ForgeCommand reads that.

---

## 8. ForgeCommand Boundary

ForgeCommand is the root of trust and orchestration layer, but for DF Local it gets a **strictly limited lane**.

### Allowed
- health
- readiness
- migration/version state
- entitlement status declaration
- app mode declaration
- degraded-state declaration
- backup/export readiness signal

### Not allowed
- direct SQL inspection of app-local authority tables
- record browsing
- raw customer/local content access
- domain search against local customer truth

This boundary is critical. Once broken, the privacy story collapses.

---

## 9. NeuronForge Local Contract Doctrine

NeuronForge Local should interact with DF Local only through declared contracts.

### 9.1 Allowed read contracts
Examples:
- project lexicon lookup
- lore/entity context lookup
- bounded retrieval/context assembly
- lane/prompt/profile references where appropriate

### 9.2 Allowed write contracts
Examples:
- run metadata
- provenance markers
- evaluation artifacts
- candidate outputs where domain-appropriate

### 9.3 Explicit non-authority rule
NeuronForge Local may consume and emit through DF Local contracts, but it does not own canonical customer truth.

### 9.4 Anti-creep rule
Do not let NeuronForge Local build a parallel truth substrate just because it is convenient for AI features.

---

## 10. Backup / Export / Restore Hardening

The first plan mentioned this area; the revised plan locks it more tightly.

### 10.1 Backup doctrine
Backups must be:
- local-first
- explicit
- version-aware
- integrity-checked
- documented as operator actions, not magic background guarantees

### 10.2 Export doctrine
Exports must declare:
- app identifier
- schema compatibility/version
- export timestamp
- format version
- integrity/hash metadata

### 10.3 Restore doctrine
Restore must validate before applying:
- export integrity
- compatible app identity
- schema compatibility
- expected foundation/core version
- operator intent

### 10.4 Fail-closed restore rules
Restore must block if:
- integrity hash mismatch
- incompatible schema version
- wrong app target
- unsupported export format
- missing required metadata

---

## 11. Hybrid / Pro Augmentation Rule

DF Local remains meaningful even when the app offers Pro or hybrid features.

### 11.1 Keep local
- customer content
- project/workspace authority data
- local operating state
- minimal cached entitlement state where needed

### 11.2 Keep cloud-authoritative
- billing truth
- subscription truth
- seat/license truth
- entitlement issuance/revocation
- optional cloud-service enablement

### 11.3 Local cached Pro state allowed
Examples:
- install/account reference
- entitlement state snapshot
- last validation timestamp
- enabled feature flags snapshot
- sync enabled/disabled flag

### 11.4 Hard boundary
DF Local must not become the billing or subscription authority.

---

## 12. Recommended Repository Posture

### 12.1 Working name
Preferred:
- `df-local-foundation`

Acceptable:
- `df-local-core`
- `df-local-base`
- `df-local-substrate`

### 12.2 Repo role
This should be a **real shared control surface**, not a throwaway starter.

It should contain:
- doctrine docs
- lifecycle scripts/services
- migration framework
- health/status contract
- shared SQL helpers/utilities
- backup/export/import utilities
- app integration guidance
- tests proving privacy and compatibility rules

It should not become the place where every app’s business schema goes to die.

---

## 13. Proposed Repo Shape

```text
/df-local-foundation
  /docs
    architecture.md
    privacy-doctrine.md
    migration-doctrine.md
    operational-visibility.md
    app-integration-contract.md
    backup-export-restore.md
  /core
    lifecycle/
    config/
    health/
    backup/
    export/
  /sql
    /core
      0001_core_foundation.sql
      0002_core_metadata.sql
  /tools
    db-status
    db-backup
    db-restore
    db-export
  /contracts
    health.schema.json
    app-registration.schema.json
    migration-status.schema.json
  /tests
    visibility_boundary/
    registration/
    backup_restore/
    migration_status/
```

---

## 14. First Integration Strategy

The original plan named AuthorForge as the seed app. That still makes sense conceptually, but the updated plan reframes the first integration more carefully:

### 14.1 Goal of first integration
Prove the **attachment model**, not a giant feature rollout.

### 14.2 What first integration must prove
- app-owned schema remains outside foundation core ownership
- foundation lifecycle/status surfaces work in practice
- migration reporting is stable
- privacy boundary remains intact
- backup/export/restore metadata can carry app identity cleanly

### 14.3 What first integration must not do
- move app domain truth into the shared repo
- over-generalize from one app’s needs
- create universal abstractions too early

---

## 15. Execution Slices

## Slice 1 — Doctrine and boundary lock
### Scope
Lock meaning before implementation drift begins.

### Deliverables
- purpose/doctrine doc
- privacy boundary doc
- app authority rule
- ForgeCommand visibility boundary
- NeuronForge Local read/write boundary
- non-goals list

### Acceptance
- all ownership lines are explicit
- no ambiguous control-plane visibility language remains

---

## Slice 2 — Repo and contract skeleton
### Scope
Create the control surface as a real repo.

### Deliverables
- repo skeleton
- contracts folder
- docs folder
- initial SQL core folder
- tool placeholders
- test scaffolding

### Acceptance
- repo exists as a concrete governed target
- no business-schema leakage into core scaffold

---

## Slice 3 — Minimal operational core
### Scope
Implement the smallest viable shared local substrate.

### Deliverables
- startup/readiness/status commands
- schema version tracking
- migration status reporting
- health schema contract
- optional app registration support

### Acceptance
- apps can rely on stable local lifecycle and status behavior
- invalid migration states fail closed

---

## Slice 4 — Visibility boundary enforcement
### Scope
Prove that operational visibility stays coarse and privacy-safe.

### Deliverables
- health contract enforcement
- status redaction rules
- non-goal tests
- ForgeCommand-facing declaration examples

### Acceptance
- status surfaces expose no customer/domain truth
- direct raw inspection path does not exist

---

## Slice 5 — Backup / export / restore safety layer
### Scope
Make local-first operationally survivable.

### Deliverables
- backup convention
- export metadata shape
- restore validation flow
- integrity checks
- compatibility checks

### Acceptance
- invalid restore payloads block cleanly
- operator can prove what a backup/export belongs to

---

## Slice 6 — First app attachment
### Scope
Prove the model using one seed app.

### Deliverables
- app registration example
- schema attachment pattern
- migration integration notes
- privacy boundary verification

### Acceptance
- seed app works without surrendering domain ownership
- no cross-app abstraction creep introduced

---

## Slice 7 — NeuronForge Local bounded contract integration
### Scope
Define and prove bounded AI interaction with local truth.

### Deliverables
- read contract examples
- write contract examples
- provenance/eval artifact path
- explicit non-authority documentation

### Acceptance
- NeuronForge Local can participate without fragmenting canonical local memory

---

## Slice 8 — Hybrid augmentation contract
### Scope
Define local/cloud coexistence without mixing authority lanes.

### Deliverables
- entitlement cache shape
- app mode declaration shape
- hybrid policy notes
- local-to-cloud movement rules

### Acceptance
- Pro/hybrid features can exist without confusing billing truth and customer content truth

---

## 16. Invariants

These remain true across every slice:

1. App-local domain truth stays app-owned.
2. DF Local Foundation stays minimal.
3. ForgeCommand sees declared operational state only.
4. NeuronForge Local is not the owner of canonical truth.
5. Restore/export/backups are versioned and integrity-checked.
6. Suspicious or ambiguous states fail closed.
7. Local-first remains meaningful even when hybrid/cloud options exist.

---

## 17. Primary Risks to Prevent

### Risk 1 — Foundation overreach
The shared repo starts swallowing app business schemas.

### Risk 2 — Privacy erosion
ForgeCommand gains raw inspection powers over local authority data.

### Risk 3 — AI memory creep
NeuronForge Local accumulates shadow truth outside app-owned authority surfaces.

### Risk 4 — Restore ambiguity
Backups/exports exist but cannot safely prove compatibility or integrity.

### Risk 5 — Hybrid confusion
Entitlement/billing truth gets mixed with local content truth.

### Risk 6 — Premature abstraction
The first app integration causes generalized interfaces that do not actually represent cross-app reality.

---

## 18. Decisions Locked by This Revision

### Lock 1
DF Local Foundation is a **shared local control surface**, not a universal app-domain database.

### Lock 2
ForgeCommand consumes **declared app status**, not raw local DB truth.

### Lock 3
NeuronForge Local interacts through **bounded contracts only** and never becomes canonical truth owner.

### Lock 4
The shared core must stay minimal and metadata-oriented.

### Lock 5
Backup/export/restore is a required architectural surface, not a future nice-to-have.

### Lock 6
First integration proves the attachment model and privacy boundary before any broader rollout.

---

## 19. Senior Engineer Review Summary

The v1 concept was architecturally sound, but too permissive in how future implementation could drift.

This revision tightens the plan by:
- narrowing the shared core
- sharpening the privacy boundary
- making visibility contract-based instead of inspection-based
- making restore/export/backup first-class
- strengthening fail-closed behavior
- reframing first integration as a proof of attachment and boundaries, not a broad feature build

That makes the plan materially safer and more implementable.

---

## 20. Next Recommended Implementation Move

Start with **Slice 1 — Doctrine and boundary lock** and do not write operational code before those documents and contracts are explicit.

That is the point where DF Local Foundation becomes stable enough to build without accidental architectural drift.

