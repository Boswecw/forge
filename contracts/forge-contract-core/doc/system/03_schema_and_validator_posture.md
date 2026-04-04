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
