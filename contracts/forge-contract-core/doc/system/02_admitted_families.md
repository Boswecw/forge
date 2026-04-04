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
