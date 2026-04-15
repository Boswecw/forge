# 02 — Admitted Families

## Proving slice 01 families

Three families were admitted in the first implementation wave:

| Family | Version | Status | Promotable | Admitted Producers | Admitted Consumers |
|---|---|---|---|---|---|
| `source_drift_finding` | 1 | active | yes | dataforge-Local, forge-eval, ForgeMath | DataForge, Forge_Command |
| `promotion_envelope` | 1 | active | no | dataforge-Local | DataForge |
| `promotion_receipt` | 1 | active | no | DataForge | dataforge-Local, Forge_Command |

## Execution bridge v1 families

Admitted after proving slice 01 green. FA Local is the canonical execution consumer.

| Family | Version | Status | Promotable | Admitted Producers | Admitted Consumers |
|---|---|---|---|---|---|
| `execution_request` | 1 | active | yes | fa-local-operator | dataforge-Local, DataForge, Forge_Command |
| `execution_status_event` | 1 | active | yes | fa-local-operator | dataforge-Local, DataForge, Forge_Command |
| `approval_artifact` | 1 | active | no | Forge_Command | fa-local-operator, dataforge-Local, DataForge |

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

### `execution_request`
Transport artifact carrying a bounded execution request from FA Local through the proving-slice pipeline for operator review and approval.

Schema: `contracts/families/execution_request/execution_request.v1.schema.json`

Required payload fields:
- `request_id` — UUID of the original FA Local execution request
- `correlation_id` — lineage correlation UUID
- `requester_identity` — identity string of the requesting agent or service
- `environment_mode` — one of: dev, test, staging, prod, airgapped, test_harness
- `requested_capability_id` — UUID of the specific capability being requested
- `requested_side_effect_class` — one of: none, local_file_write, local_db_mutation, local_process_spawn, external_network_denied_by_default, other_governed
- `authorization_class` — one of: low_risk_automated, medium_risk_review, high_risk_approval, denied_class
- `intent_summary` — machine-readable statement of execution intent (max 240 chars)
- `requested_at` — ISO 8601 timestamp of request origination
- `operator_summary` — plain-language summary for operator review

### `execution_status_event`
Truthful execution status snapshot emitted by FA Local, transported through the proving-slice pipeline for operator visibility.

Schema: `contracts/families/execution_status_event/execution_status_event.v1.schema.json`

Required payload fields:
- `request_id` — UUID of the original execution request
- `correlation_id` — lineage correlation UUID
- `state` — one of: denied, review_required, waiting_explicit_approval, admitted_not_started, in_progress, degraded, partial_success, completed_with_constraints, completed, failed, canceled
- `current_posture` — one of: denied, review_required, explicit_operator_approval, policy_preapproved, execute_allowed
- `execution_plan_id` — UUID of the bounded execution plan (nullable)
- `stable_plan_hash` — 64-char SHA-256 hash of the plan (nullable)
- `degraded_subtype` — nullable degraded subtype enum
- `updated_at_utc` — ISO 8601 timestamp of this status event
- `started_at_utc` — nullable start timestamp
- `completed_at_utc` — nullable completion timestamp
- `current_step` — nullable current declared step ID
- `completion_summary` — nullable completion summary (max 160 chars)
- `failure_summary` — nullable failure summary (max 160 chars)
- `truthful_operator_summary` — always-present plain-language summary (max 160 chars)

### `approval_artifact`
Explicit operator approval or rejection decision for a pending execution request that required `explicit_operator_approval` posture.

Schema: `contracts/families/approval_artifact/approval_artifact.v1.schema.json`

Required payload fields:
- `request_id` — UUID of the original execution request this decision covers
- `correlation_id` — lineage correlation UUID
- `approval_decision` — one of: approved, rejected (must be unambiguous)
- `decided_by` — identity of the deciding operator (max 256 chars)
- `decided_at` — ISO 8601 timestamp of the decision
- `decision_summary` — plain-language summary for audit and review surfaces (max 160 chars)

## Excluded families (future phases only)

Do not add these until execution bridge v1 is proven:
- `verification_result`
- `rollback_result`
- `recommendation_artifact`
- `contradiction_artifact`
- `calibration_artifact`
