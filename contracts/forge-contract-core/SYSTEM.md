# forge-contract-core — System Reference

> Assembled from `doc/system/`. Edit the section files, then run `bash doc/system/BUILD.sh`.

**Document version:** 2026-04-04

---


# 01 — Purpose and Ownership

## What this repo is

`forge-contract-core` is the canonical contract center for the Forge ecosystem.

It exists to prevent semantic drift before multi-repo proving-slice implementation expands. It owns shared contract meaning and enforces discipline through machine-readable schemas, validators, and a canonical gate runner.

## What this repo owns

- Shared envelope schema (canonical wire format for all admitted artifact families)
- Admitted family schemas (proving slice 01: `source_drift_finding`, `promotion_envelope`, `promotion_receipt`)
- Canonical enum vocabularies (10 enums)
- Validator Python package (`forge_contract_core`)
- Fixture corpus (valid, invalid, duplicate, restricted, read-model)
- Canonical gate runner (`python -m forge_contract_core.gates.run_all`)
- Forbidden-pattern rules
- Repo role matrix (who may emit, consume, promote)
- Reference producer and consumer examples

## What this repo does NOT own

- Transport services
- Review UI or operator control surfaces
- Durable truth persistence for runtime artifacts
- Approval, execution, recommendation, contradiction, rollback, or calibration families (future phases only)
- Any application runtime code

## Authority position in the ecosystem

`forge-contract-core` is a prerequisite for all downstream proving-slice implementation.

No cross-repo transport work may proceed until:
- schemas exist
- validator package works
- gate runner passes
- role matrix exists
- fixture corpus exists

## Role class

`contract_core`

---

# 02 — Admitted Families

## Proving slice 01 admitted families

Only three families are admitted in the first implementation wave:

| Family | Version | Status | Promotable | Admitted Producers | Admitted Consumers |
|---|---|---|---|---|---|
| `source_drift_finding` | 1 | active | yes | dataforge-Local, forge-eval, ForgeMath | DataForge, Forge_Command |
| `promotion_envelope` | 1 | active | no | dataforge-Local | DataForge |
| `promotion_receipt` | 1 | active | no | DataForge | dataforge-Local, Forge_Command |

## Family descriptions

### `source_drift_finding`
Describes a detected drift between declared and observed truth for a system.

Schema: `contracts/families/source_drift_finding/source_drift_finding.v1.schema.json`

Required payload fields:
- `system_id` — the system where drift was observed
- `drift_class` — one of: schema_drift, version_drift, contract_drift, config_drift, runtime_drift, dependency_drift, behavioral_drift
- `declared_truth_ref` — reference to the expected/declared state
- `observed_truth_ref` — reference to the actual observed state
- `impact_scope` — one of: local, service, cross_service, ecosystem
- `confidence` — one of: high, medium, low, unknown
- `operator_summary` — plain-language operator-readable explanation

### `promotion_envelope`
Wraps a local artifact for promotion to shared truth. Not itself promotable.

Schema: `contracts/families/promotion_envelope/promotion_envelope.v1.schema.json`

Required payload fields:
- `promoted_artifact_ref` — canonical reference to the promoted artifact
- `promotion_reason` — plain-language promotion reason
- `redaction_class` — one of: none, partial, full
- `policy_check_result` — one of: passed, failed, blocked, waived
- `promotion_batch_id` — UUID grouping this promotion

### `promotion_receipt`
Durable receipt of a shared intake outcome. Must carry exactly one of: accepted, rejected, duplicate_reconciled.

Schema: `contracts/families/promotion_receipt/promotion_receipt.v1.schema.json`

Required payload fields:
- `receipt_id` — UUID for this receipt
- `related_artifact_ref` — reference to the artifact this covers
- `intake_outcome` — one of: accepted, rejected, duplicate_reconciled (must not be ambiguous)
- `received_at` — ISO 8601 timestamp of outcome determination
- `idempotency_key` — idempotency key of the covered artifact
- `outcome_summary` — plain-language explanation

## Excluded families (future phases only)

Do not add these until proving slice 01 is green:
- `approval_artifact`
- `execution_request`
- `execution_status_event`
- `verification_result`
- `rollback_result`
- `recommendation_artifact`
- `contradiction_artifact`
- `calibration_artifact`

---

# 03 — Schema and Validator Posture

## Schema format

All schemas are JSON Schema Draft-07. Schemas use `additionalProperties: false` for strict proving-slice mode to prevent undeclared field drift.

## Shared envelope fields

Every admitted artifact must carry these fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `artifact_id` | UUID string | yes | Stable instance UUID |
| `artifact_family` | string | yes | snake_case, admitted families only |
| `artifact_version` | integer | yes | Monotonic, ≥1 |
| `produced_by_system` | string | yes | Repo/system identity |
| `produced_by_component` | string | yes | Component within producing system |
| `source_scope` | enum | yes | local / shared / restricted |
| `lineage_root_id` | UUID | yes | Root of lineage chain (== artifact_id for root) |
| `parent_artifact_id` | UUID or null | no | null for root artifacts |
| `trace_id` | string | yes | Distributed trace identifier |
| `idempotency_key` | 64-char hex | yes | SHA-256 canonical key |
| `created_at` | ISO 8601 | yes | Producer creation timestamp |
| `recorded_at` | ISO 8601 | yes | Durable recording timestamp |
| `sensitivity_class` | enum | yes | public / internal / restricted / confidential |
| `visibility_class` | enum | yes | public / operator / internal / restricted |
| `promotion_class` | enum | yes | promotable / local_only / blocked |
| `validation_status` | enum | yes | valid / invalid / pending / unknown |
| `signer_identity` | string | yes | Signing party identity |
| `signature` | string | yes | Opaque signature over canonical payload |
| `payload` | object | yes | Family-specific payload |

## Idempotency key algorithm

```
sha256(artifact_family + "|" + artifact_id + "|" + str(artifact_version) + "|" + lineage_root_id)
```

All producers must use `forge_contract_core.identity.compute_idempotency_key()`. Never compute locally.

## Reference grammar

```
<artifact_family>:<artifact_id>:v<artifact_version>
```

Example: `source_drift_finding:a1b2c3d4-0001-0001-0001-000000000001:v1`

All cross-artifact references must follow this grammar. Use `forge_contract_core.refs.parse_reference()` and `format_reference()`.

## Validator package

The `forge_contract_core` package exposes:

| Function | Location | Purpose |
|---|---|---|
| `validate_envelope(artifact)` | `validators/envelope.py` | Validate against shared-envelope schema |
| `validate_family_payload(family, version, payload)` | `validators/families.py` | Validate against admitted family schema |
| `validate_artifact(artifact)` | `validators/artifact.py` | Full envelope + payload + idempotency validation |
| `compute_idempotency_key(...)` | `identity.py` | Canonical idempotency key computation |
| `verify_idempotency_key(...)` | `identity.py` | Verify a key against canonical algorithm |
| `parse_reference(ref)` | `refs.py` | Parse canonical reference grammar |
| `format_reference(...)` | `refs.py` | Format canonical reference string |
| `check_producer_admitted(...)` | `validators/role_matrix.py` | Role-matrix admission check |

## Enum policy

All enum values must be imported from `forge_contract_core.enums`. Consuming repos must never redefine or extend these values locally. This is Forbidden Pattern FP002.

## additionalProperties policy

Proving slice v1 schemas use `additionalProperties: false`. Submitting additional fields not declared in the schema is a gate failure (Forbidden Pattern FP003).

---

# 04 — Registries and Role Matrix

## Files

| File | Purpose |
|---|---|
| `registry/artifact_family_registry.json` | Admitted families, their versions, producers, consumers |
| `registry/version_registry.json` | Version status per family (active/deprecated/sunset) |
| `registry/deprecation_registry.json` | Deprecated version records |
| `registry/repo_role_matrix.json` | Per-repo role class, emit/consume permissions, gate profiles |

## Repo role matrix

The role matrix is the authoritative source for what each ecosystem repo may do.

### Direct proving-slice participants

| Repo | Role Class | Emits | Consumes | Promotes | Review Surface |
|---|---|---|---|---|---|
| `forge-contract-core` | contract_core | — | — | no | no |
| `dataforge-Local` | producer_promoter | source_drift_finding, promotion_envelope | promotion_receipt | yes | no |
| `DataForge` | shared_truth_consumer, shared_truth_owner | promotion_receipt | source_drift_finding, promotion_envelope | no | no |
| `Forge_Command` | review_surface | — | source_drift_finding, promotion_receipt | no | yes |

### Indirect / future participants

| Repo | Role Class | Notes |
|---|---|---|
| `fa-local` | execution_consumer | Excluded from proving slice 01 |
| `forge-eval` | evaluation_producer | Indirect first-wave participant |
| `ForgeMath` | evaluation_producer | Indirect first-wave participant |
| `forgeHQ` | producer_only | Excluded from proving slice 01 |

## Forbidden payload classes

The role matrix records what each repo must never emit:
- `execution_request`, `approval_artifact` — forbidden for all proving-slice participants
- `forge-contract-core` — forbidden from all runtime artifacts
- `Forge_Command` — forbidden from writing canonical lifecycle truth (read-only review surface)

## Required gate profiles

Each direct participant carries a required gate profile in the role matrix. These gate profiles must pass in CI for the repo to be considered proving-slice ready.

---

# 05 — Gate Runner Contract

## Canonical entry point

```bash
python -m forge_contract_core.gates.run_all
```

All direct proving-slice participating repos must wire this command into their CI. They may wrap it but must not replace it with weaker local-only checks.

Exit codes:
- `0` — all gates pass
- `1` — one or more gates failed

## Gate categories

| Gate | Module | What it checks |
|---|---|---|
| `schema` | `gates/schema_gate.py` | All admitted schemas exist and are valid JSON Schema |
| `fixture_corpus` | `gates/fixture_gate.py` | Valid fixtures pass, invalid fixtures fail, duplicate fixtures are structurally valid |
| `validator_correctness` | `gates/validator_gate.py` | Idempotency key stability, reference grammar, unsupported family/version rejection |
| `compatibility` | `gates/compatibility_gate.py` | Registry and compatibility notes are consistent |
| `forbidden_patterns` | `gates/forbidden_pattern_gate.py` | Forbidden patterns file is present, well-formed, and has no duplicate IDs |

## Gate failure behavior

Gate failures are blocking, not advisory. If any gate fails, the runner exits with code 1 and CI must fail.

## Temporary waivers

Temporary waivers may be issued for legitimate blockers. They must be:
- Explicit (documented in a waiver record)
- Time-bounded
- Governance-approved
- Visible (not hidden in CI configuration)

Waivers must never become permanent compatibility workarounds.

## Adding a new gate

1. Create a new gate module in `forge_contract_core/gates/`.
2. Implement `run() -> list[str]` returning failure messages.
3. Register the gate in `run_all.py`.
4. Add tests in `tests/gates/test_gates.py`.
5. Update this doc.

---

# 06 — Change Workflow and RFC Rules

## When an RFC is required

An RFC (Request for Contract Change) is required for:
- Adding a new admitted artifact family
- Making a breaking change to an existing admitted family schema
- Adding a new major version of an admitted family
- Admitting a new promotable family
- Adding a new restricted payload class
- Adding contradiction, execution, or approval families
- Changing the repo role matrix for a direct proving-slice participant

## When an RFC is NOT required

No RFC needed for:
- Adding optional fields to a family schema (non-breaking)
- Adding new valid fixtures
- Bug fixes to the validator that do not change behavior
- Documentation improvements
- Adding new gate checks that do not fail existing passing repos

## RFC process

1. Open a PR with a description of the proposed change.
2. Label it `rfc`.
3. Assign a contract owner reviewer, a compatibility reviewer, and (for promotable families) a security reviewer.
4. The RFC must document:
   - What is changing and why
   - Which repos are affected
   - What migration path exists for existing consumers
   - Whether backward compatibility is preserved
5. RFC must be approved before implementation merges.

## Breaking change policy

A breaking change to an admitted family requires a new major version (v2, v3...). v1 consumers must never be silently broken.

## Deprecation process

To deprecate a family version:
1. Add an entry to `registry/deprecation_registry.json`.
2. Set `deprecated_at` in `registry/version_registry.json`.
3. Set `sunset_at` to give consumers a migration window.
4. After sunset, the version may be removed from `ADMITTED_VERSIONS` in `enums.py`.

## Role class changes

Changes to admitted emit or consume families in the role matrix require an RFC because they affect proving-slice security boundaries.

---

# 07 — Deprecation and Versioning Rules

## Version scheme

Family versions are monotonic integers: v1, v2, v3...

- v1 is the first admitted version for all proving-slice families.
- Major-version bumps (v1→v2) are required for breaking changes.
- Minor additions (new optional fields) do not require a version bump but must be documented.

## Active version support

At any time, the set of supported versions per family is defined in `enums.py`:

```python
ADMITTED_VERSIONS: dict[str, frozenset[int]] = {
    "source_drift_finding": frozenset({1}),
    ...
}
```

Consumers must reject unsupported versions. Unsupported version rejection is a non-retryable outcome.

## Dual-read posture

Dual-read (supporting two concurrent major versions) is not active in proving slice v1.

It may be enabled for a specific family during a version transition window. The enabling of dual-read requires an RFC.

## Deprecation lifecycle

| Stage | When | Action |
|---|---|---|
| Deprecated | New version admitted | Add to deprecation_registry.json, set deprecated_at |
| Sunset window | Announced in RFC | Consumers given time to migrate |
| Removed | After sunset | Remove version from ADMITTED_VERSIONS |

## Removing a version

A version may only be removed after its sunset_at date has passed and there are no known active consumers. Removal requires an RFC.

## Family retirement

A family may be retired when it has no active admitted producers or consumers. Retirement requires an RFC and full removal from all registries.

## Proving slice scope

For proving slice 01, no deprecations are active. The version registry is empty on the deprecation side at inception.

---
