# Forge Implementation Pack 09 — forge-contract-core Implementation Blueprint

**Date:** 2026-04-04 01:33 America/New_York  
**Purpose:** Give VSCode Opus 4.6 an implementation-ready blueprint for creating the new `forge-contract-core` repo.

---

# 1. Mission

Create a new repo named **`forge-contract-core`**.

This repo is the canonical contract center for the proving slice.

It must ship:
- machine-readable schemas
- fixtures
- validator package
- repo role matrix
- canonical gate runner
- forbidden-pattern rules
- reference producer and consumer examples

It must not ship:
- runtime transport services
- operator UI
- durable truth persistence for real ecosystem artifacts

---

# 2. First repo structure Opus should create

```text
forge-contract-core/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── SYSTEM.md
├── doc/system/
├── contracts/
│   ├── envelope/
│   │   └── shared-envelope.schema.json
│   ├── families/
│   │   ├── source_drift_finding/
│   │   │   └── source_drift_finding.v1.schema.json
│   │   ├── promotion_envelope/
│   │   │   └── promotion_envelope.v1.schema.json
│   │   └── promotion_receipt/
│   │       └── promotion_receipt.v1.schema.json
│   ├── enums/
│   │   ├── source_scope.enum.json
│   │   ├── sensitivity_class.enum.json
│   │   ├── visibility_class.enum.json
│   │   ├── promotion_class.enum.json
│   │   ├── validation_status.enum.json
│   │   ├── drift_class.enum.json
│   │   ├── impact_scope.enum.json
│   │   ├── confidence.enum.json
│   │   ├── redaction_class.enum.json
│   │   └── policy_check_result.enum.json
│   └── compatibility/
│       └── proving_slice_v1.json
├── registry/
│   ├── artifact_family_registry.json
│   ├── version_registry.json
│   ├── deprecation_registry.json
│   └── repo_role_matrix.json
├── forbidden_patterns/
│   └── forbidden_patterns.json
├── fixtures/
│   ├── valid/
│   ├── invalid/
│   ├── duplicate/
│   ├── restricted/
│   └── read_model/
├── examples/
│   ├── producer/
│   └── consumer/
├── forge_contract_core/
│   ├── __init__.py
│   ├── canonical_json.py
│   ├── refs.py
│   ├── identity.py
│   ├── enums.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── envelope.py
│   │   ├── families.py
│   │   ├── artifact.py
│   │   └── role_matrix.py
│   └── gates/
│       ├── __init__.py
│       ├── run_all.py
│       ├── schema_gate.py
│       ├── fixture_gate.py
│       ├── validator_gate.py
│       ├── compatibility_gate.py
│       └── forbidden_pattern_gate.py
└── tests/
    ├── schema/
    ├── validator/
    ├── property/
    └── gates/
```

---

# 3. Exact first implementation tasks

## Task 1 — repo scaffold
Create the repo structure above with Python packaging and documentation scaffold.

## Task 2 — shared envelope schema
Implement `shared-envelope.schema.json` with required fields and constraints for:
- artifact identity
- lineage
- timestamps
- class vocabularies
- signer identity
- signature
- payload

## Task 3 — admitted family schemas
Implement exactly three family schemas:
- `source_drift_finding.v1`
- `promotion_envelope.v1`
- `promotion_receipt.v1`

## Task 4 — enum pack
Implement the first canonical enum pack as machine-readable artifacts plus Python enum accessors if helpful.

## Task 5 — validator package
Implement Python validators for:
- envelope validation
- family validation
- full artifact validation
- role-matrix checks
- reference grammar parsing
- idempotency-key generation

## Task 6 — registries
Implement:
- artifact family registry
- version registry
- deprecation registry
- repo role matrix

## Task 7 — fixture corpus
Create valid and invalid fixtures for all three admitted families.

## Task 8 — canonical gate runner
Implement `python -m forge_contract_core.gates.run_all`.

## Task 9 — reference examples
Add one producer example and one consumer example.

## Task 10 — docs
Author `doc/system/` and assemble `SYSTEM.md` so this repo is governed, not just present.

---

# 4. Required schema details

## 4.1 Shared envelope required fields
- `artifact_id`
- `artifact_family`
- `artifact_version`
- `produced_by_system`
- `produced_by_component`
- `source_scope`
- `lineage_root_id`
- `parent_artifact_id`
- `trace_id`
- `idempotency_key`
- `created_at`
- `recorded_at`
- `sensitivity_class`
- `visibility_class`
- `promotion_class`
- `validation_status`
- `signer_identity`
- `signature`
- `payload`

## 4.2 `source_drift_finding` required payload fields
- `system_id`
- `drift_class`
- `declared_truth_ref`
- `observed_truth_ref`
- `impact_scope`
- `confidence`
- `operator_summary`

## 4.3 `promotion_envelope` required payload fields
- `promoted_artifact_ref`
- `promotion_reason`
- `redaction_class`
- `policy_check_result`
- `promotion_batch_id`

## 4.4 `promotion_receipt` minimum proving-slice fields
Opus should define a bounded first receipt schema including at least:
- `receipt_id`
- `related_artifact_ref`
- `intake_outcome`
- `shared_record_ref`
- `received_at`
- `idempotency_key`
- `outcome_summary`

---

# 5. Required validator behavior

## 5.1 Artifact validation
Validator must:
- reject invalid envelope
- reject invalid family payload
- reject undeclared required-field omissions
- reject proving-slice additional fields where prohibited
- reject unsupported family/version

## 5.2 Reference grammar
Validator must enforce canonical reference grammar:

`<artifact_family>:<artifact_id>:v<artifact_version>`

## 5.3 Idempotency key
Implement canonical proving-slice algorithm:

`sha256(artifact_family + "|" + artifact_id + "|" + artifact_version + "|" + lineage_root_id)`

---

# 6. Required repo role matrix content

For first wave, `repo_role_matrix.json` should include at least:
- `forge-contract-core`
- `dataforge-Local`
- `DataForge`
- `Forge_Command`
- `fa-local`
- `forge-eval`
- `ForgeMath`
- `forgeHQ`

Each row should declare:
- repo name
- role classes
- allowed emit families
- allowed consume families
- promotion enabled
- review surface enabled
- execution enabled
- forbidden payload classes
- local-only truth classes
- required gate profiles

---

# 7. Required tests Opus must add

## 7.1 Schema tests
- valid envelope fixtures pass
- invalid envelope fixtures fail
- valid family fixtures pass
- invalid family fixtures fail

## 7.2 Validator tests
- artifact validation works end to end
- reference grammar roundtrip works
- idempotency key is stable
- unsupported version fails

## 7.3 Gate tests
- gate runner exits green on correct fixture corpus
- gate runner fails when invalid fixtures are accepted
- gate runner fails when required fixtures are missing

## 7.4 Property tests
Where practical:
- idempotency-key stability
- reference grammar parsing
- schema roundtrip invariants

---

# 8. Required docs Opus must create

Minimum `doc/system/` topics:
- repo purpose and ownership
- admitted family set
- schema and validator posture
- registries and role matrix
- gate runner contract
- change workflow and RFC rules
- deprecation/versioning rules

---

# 9. Required anti-scope statement for Opus

When implementing this repo, Opus must not:
- add transport runtime code
- add shared-truth persistence code
- add review UI
- admit extra families
- blur reference examples into production runtime modules

---

# 10. Implementation completion checklist

Opus should not declare this repo ready until all are true:
- repo scaffold exists
- three admitted family schemas exist
- shared envelope exists
- validator package exists
- registries exist
- fixture corpus exists
- gate runner exists
- tests pass
- `SYSTEM.md` is assembled and truthful

If any are missing, contract-core is not ready.

