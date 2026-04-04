# Forge Plan Set 02 — forge-contract-core Bootstrap Plan

**Date:** 2026-04-04 01:18 America/New_York  
**Purpose:** Define the exact first implementation plan for the canonical contract-center repo required by the ecosystem.

---

# 1. Mission

Create **`forge-contract-core`** as the single canonical home for shared contract meaning across the ecosystem.

This repo exists to stop semantic drift before multi-repo proving-slice implementation expands.

It must own:
- shared envelope schemas
- admitted family schemas
- enum vocabularies
- validator library
- fixtures
- compatibility notes
- version registry
- repo role-class registry
- canonical gate runner
- forbidden-pattern rules
- reference producer examples
- reference consumer examples

It must not become:
- a transport service
- a review UI
- a durable truth owner for runtime artifacts
- a second planning repo full of prose without executable contract assets

---

# 2. First admitted scope

## 2.1 Families admitted in the first wave
Only these families are admitted initially:

1. `source_drift_finding`
2. `promotion_envelope`
3. `promotion_receipt`

## 2.2 Why the scope stays this narrow
Because the ecosystem is already broad and the contract center must prove discipline before breadth.

Do not add:
- approval families
- execution families
- recommendation families
- contradiction families
- rollback families
- calibration families

until proving slice 01 is green.

---

# 3. Repository structure

```text
forge-contract-core/
├── README.md
├── SYSTEM.md
├── doc/system/
├── contracts/
│   ├── envelope/
│   ├── families/
│   │   ├── source_drift_finding/
│   │   ├── promotion_envelope/
│   │   └── promotion_receipt/
│   ├── enums/
│   └── compatibility/
├── fixtures/
│   ├── valid/
│   ├── invalid/
│   ├── duplicate/
│   ├── restricted/
│   └── read_model/
├── registry/
│   ├── artifact_family_registry.json
│   ├── version_registry.json
│   ├── deprecation_registry.json
│   └── repo_role_matrix.json
├── forbidden_patterns/
│   └── forbidden_patterns.json
├── forge_contract_core/
│   ├── __init__.py
│   ├── validators/
│   ├── identity/
│   ├── canonical_json/
│   ├── gates/
│   └── refs/
├── examples/
│   ├── producer/
│   └── consumer/
├── tests/
│   ├── schema/
│   ├── validator/
│   ├── gates/
│   └── property/
└── pyproject.toml
```

---

# 4. Required artifacts in the repo

## 4.1 Shared envelope schema
Must include required fields for:
- identity
- lineage
- timestamps
- source/promotion/visibility classes
- signer identity
- signature
- payload

## 4.2 Family schemas
One schema per admitted family.

## 4.3 Enum vocabularies
At minimum:
- `source_scope`
- `sensitivity_class`
- `visibility_class`
- `promotion_class`
- `validation_status`
- `drift_class`
- `impact_scope`
- `confidence`
- `redaction_class`
- `policy_check_result`

## 4.4 Version registry
Every admitted family must have a visible version entry.

## 4.5 Repo role matrix
Must define:
- repo name
- role classes
- allowed emit families
- allowed consume families
- promotion enabled flag
- review surface flag
- execution enabled flag
- forbidden payload classes
- required gate profiles

---

# 5. Canonical validator package

## 5.1 First validator requirements
The validator library must be able to:
- validate canonical envelope
- validate family payloads
- reject forbidden additional fields where proving-slice strictness requires it
- validate enum parity
- compute canonical idempotency key
- validate canonical reference grammar
- validate admitted producer identity against repo-role registry where applicable

## 5.2 Design rule
The validator must be usable from participating repos directly in CI and locally.

## 5.3 Required public surfaces
Examples:
- `validate_envelope(...)`
- `validate_artifact(...)`
- `compute_idempotency_key(...)`
- `parse_reference(...)`
- `run_all_gates(...)`

---

# 6. Fixture corpus

## 6.1 Required fixture classes
For each admitted family, publish:
- valid canonical examples
- invalid schema examples
- invalid enum examples
- backward-compatible examples where applicable
- duplicate/idempotent examples
- blocked/restricted examples where applicable
- stale/incomplete read-model examples for review-surface testing

## 6.2 Rule
No family is considered ready without fixtures.

---

# 7. Canonical gate runner

## 7.1 Required command
The repo must expose the canonical CI entry point:

```bash
python -m forge_contract_core.gates.run_all
```

## 7.2 Gate categories
The gate runner must cover:
- schema verification
- validator correctness
- compatibility checks
- fixture corpus checks
- role-matrix checks
- forbidden-pattern checks

## 7.3 Anti-rule
Participating repos may wrap this command, but may not replace it with weaker local-only checks.

---

# 8. Forbidden patterns file

The contract core must publish machine-readable forbidden patterns such as:
- nested shared envelope in payload
- enum redefinition by consuming repo
- additional undeclared proving-slice wire fields
- local-only truth promoted by convenience
- derived read model treated as canonical lifecycle truth
- families emitted by repos not admitted to emit them

---

# 9. Reference examples

## 9.1 Producer example
Provide a minimal reference producer for `source_drift_finding`.

## 9.2 Consumer example
Provide a minimal reference consumer for `promotion_receipt`.

## 9.3 Purpose
These examples are not production implementations. They are executable boundary examples to stop interpretation drift.

---

# 10. Testing plan

## 10.1 Required test classes
- envelope valid/invalid tests
- family valid/invalid tests
- enum parity tests
- idempotency-key stability tests
- reference grammar roundtrip tests
- validator mutation-resistance tests
- gate runner smoke tests

## 10.2 Property tests
Use property-based testing where practical for:
- idempotency-key stability
- reference grammar parsing
- schema roundtrip invariants

---

# 11. Documentation plan

The repo must have:
- SYSTEM.md assembled from `doc/system/`
- contract-center ownership doctrine
- contribution workflow
- RFC requirements
- versioning rules
- deprecation rules
- repo onboarding rules

This repo cannot be “just schemas in a folder.”

---

# 12. Ownership and workflow

## 12.1 Roles required
- contract owner
- reviewer pool
- release steward
- compatibility reviewer
- security reviewer for promotable families

## 12.2 Change workflow
An RFC is required for:
- new admitted family
- major-version change
- promotable family admission
- new restricted payload class
- contradiction or execution-family addition

---

# 13. Exit criteria

`forge-contract-core` is ready for broader implementation only when:
- the repo exists
- the three admitted families are fully modeled
- valid and invalid fixtures exist
- validator package works
- canonical gate runner works
- repo role matrix exists
- one producer example exists
- one consumer example exists
- docs and contribution rules are authored

If those are not true, broader multi-repo transport implementation should not proceed.

