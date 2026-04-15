"""Canonical enum vocabularies for the Forge proving-slice.

These are the authoritative value sets. Consuming repos must import from here
and must NOT redefine or extend these values locally.
"""

from __future__ import annotations

from enum import StrEnum


class SourceScope(StrEnum):
    LOCAL = "local"
    SHARED = "shared"
    RESTRICTED = "restricted"


class SensitivityClass(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"


class VisibilityClass(StrEnum):
    PUBLIC = "public"
    OPERATOR = "operator"
    INTERNAL = "internal"
    RESTRICTED = "restricted"


class PromotionClass(StrEnum):
    PROMOTABLE = "promotable"
    LOCAL_ONLY = "local_only"
    BLOCKED = "blocked"


class ValidationStatus(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    UNKNOWN = "unknown"


class DriftClass(StrEnum):
    SCHEMA_DRIFT = "schema_drift"
    VERSION_DRIFT = "version_drift"
    CONTRACT_DRIFT = "contract_drift"
    CONFIG_DRIFT = "config_drift"
    RUNTIME_DRIFT = "runtime_drift"
    DEPENDENCY_DRIFT = "dependency_drift"
    BEHAVIORAL_DRIFT = "behavioral_drift"


class ImpactScope(StrEnum):
    LOCAL = "local"
    SERVICE = "service"
    CROSS_SERVICE = "cross_service"
    ECOSYSTEM = "ecosystem"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class RedactionClass(StrEnum):
    NONE = "none"
    PARTIAL = "partial"
    FULL = "full"


class PolicyCheckResult(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    WAIVED = "waived"


class IntakeOutcome(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DUPLICATE_RECONCILED = "duplicate_reconciled"


class AuthorizationClass(StrEnum):
    LOW_RISK_AUTOMATED = "low_risk_automated"
    MEDIUM_RISK_REVIEW = "medium_risk_review"
    HIGH_RISK_APPROVAL = "high_risk_approval"
    DENIED_CLASS = "denied_class"


class ApprovalPosture(StrEnum):
    DENIED = "denied"
    REVIEW_REQUIRED = "review_required"
    EXPLICIT_OPERATOR_APPROVAL = "explicit_operator_approval"
    POLICY_PREAPPROVED = "policy_preapproved"
    EXECUTE_ALLOWED = "execute_allowed"


class ExecutionState(StrEnum):
    DENIED = "denied"
    REVIEW_REQUIRED = "review_required"
    WAITING_EXPLICIT_APPROVAL = "waiting_explicit_approval"
    ADMITTED_NOT_STARTED = "admitted_not_started"
    IN_PROGRESS = "in_progress"
    DEGRADED = "degraded"
    PARTIAL_SUCCESS = "partial_success"
    COMPLETED_WITH_CONSTRAINTS = "completed_with_constraints"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class ApprovalDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"


class SideEffectClass(StrEnum):
    NONE = "none"
    LOCAL_FILE_WRITE = "local_file_write"
    LOCAL_DB_MUTATION = "local_db_mutation"
    LOCAL_PROCESS_SPAWN = "local_process_spawn"
    EXTERNAL_NETWORK_DENIED_BY_DEFAULT = "external_network_denied_by_default"
    OTHER_GOVERNED = "other_governed"


class RejectionClass(StrEnum):
    INVALID_SCHEMA = "invalid_schema"
    INVALID_SIGNATURE = "invalid_signature"
    UNSUPPORTED_VERSION = "unsupported_version"
    UNSUPPORTED_PRODUCER = "unsupported_producer"
    BLOCKED_POLICY = "blocked_policy"
    RESTRICTED_PAYLOAD = "restricted_payload"
    OVERSIZE_PAYLOAD = "oversize_payload"
    BLOCKED_FAMILY = "blocked_family"
    BLOCKED_SENSITIVITY_CLASS = "blocked_sensitivity_class"


# Admitted families — proving slice 01 + execution bridge v1
ADMITTED_FAMILIES: frozenset[str] = frozenset(
    {
        "source_drift_finding",
        "promotion_envelope",
        "promotion_receipt",
        "execution_request",
        "execution_status_event",
        "approval_artifact",
    }
)

# Admitted versions per family
ADMITTED_VERSIONS: dict[str, frozenset[int]] = {
    "source_drift_finding": frozenset({1}),
    "promotion_envelope": frozenset({1}),
    "promotion_receipt": frozenset({1}),
    "execution_request": frozenset({1}),
    "execution_status_event": frozenset({1}),
    "approval_artifact": frozenset({1}),
}

# Sensitivity classes that permit promotion
PROMOTABLE_SENSITIVITY_CLASSES: frozenset[str] = frozenset(
    {
        SensitivityClass.PUBLIC,
        SensitivityClass.INTERNAL,
    }
)
