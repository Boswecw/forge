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


# Admitted families — only these are valid in proving slice 01
ADMITTED_FAMILIES: frozenset[str] = frozenset(
    {
        "source_drift_finding",
        "promotion_envelope",
        "promotion_receipt",
    }
)

# Admitted versions per family
ADMITTED_VERSIONS: dict[str, frozenset[int]] = {
    "source_drift_finding": frozenset({1}),
    "promotion_envelope": frozenset({1}),
    "promotion_receipt": frozenset({1}),
}

# Sensitivity classes that permit promotion
PROMOTABLE_SENSITIVITY_CLASSES: frozenset[str] = frozenset(
    {
        SensitivityClass.PUBLIC,
        SensitivityClass.INTERNAL,
    }
)
