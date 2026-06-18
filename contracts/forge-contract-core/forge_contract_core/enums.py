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


class SourceTrustClassification(StrEnum):
    OFFICIAL = "OFFICIAL"
    TRUSTED_SECONDARY = "TRUSTED_SECONDARY"
    ADVISORY = "ADVISORY"
    BLOCKED = "BLOCKED"


class LLMProviderId(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    XAI = "xai"
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"


class LLMIntelClaimType(StrEnum):
    PRICING = "pricing"
    MODEL_AVAILABILITY = "model_availability"
    DEPRECATION = "deprecation"
    CONTEXT_WINDOW = "context_window"
    MODALITY = "modality"
    API_BEHAVIOR = "api_behavior"
    TERMS_SAFETY = "terms_safety"
    CAPABILITY = "capability"
    MODEL_METADATA = "model_metadata"


class LLMIntelPromotionState(StrEnum):
    CANDIDATE_DETECTED = "candidate_detected"
    EVIDENCE_COLLECTED = "evidence_collected"
    DRIFT_CLASSIFIED = "drift_classified"
    MAID_REVIEW_REQUIRED = "maid_review_required"
    MAID_REVIEWED = "maid_reviewed"
    QUEUED_FOR_OPERATOR_REVIEW = "queued_for_operator_review"
    APPROVED_FOR_PROMOTION = "approved_for_promotion"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    MORE_EVIDENCE_REQUIRED = "more_evidence_required"
    PROMOTED = "promoted"
    SUPERSEDED = "superseded"
    ROLLBACK_REQUESTED = "rollback_requested"
    ROLLBACK_COMPLETED = "rollback_completed"
    ARCHIVED = "archived"


class TripleVariantAuditLane(StrEnum):
    CONTRACT = "contract"
    FUNCTIONAL = "functional"
    DRIFT_RESILIENCE = "drift_resilience"


class TripleVariantAuditLaneStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    NEEDS_OPERATOR_REVIEW = "NEEDS_OPERATOR_REVIEW"


class TripleVariantAuditFindingSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


class TripleVariantAuditFindingCategory(StrEnum):
    SCHEMA = "schema"
    RECEIPT = "receipt"
    RUNTIME = "runtime"
    TEST = "test"
    DRIFT = "drift"
    INSTRUCTION = "instruction"
    EVIDENCE = "evidence"
    SECURITY = "security"
    OPERATOR_REVIEW = "operator_review"
    MUTATION_AUTHORITY = "mutation_authority"


class TripleVariantAuditEvidenceType(StrEnum):
    TERMINAL_LOG = "terminal_log"
    SCHEMA_FIXTURE = "schema_fixture"
    TEST_REPORT = "test_report"
    DIFF = "diff"
    GENERATED_INSTRUCTION = "generated_instruction"
    PROVIDER_RESPONSE = "provider_response"
    OPERATOR_NOTE = "operator_note"
    DATAFORGE_RECORD = "dataforge_record"
    REPLAY_MANIFEST = "replay_manifest"


class TripleVariantAuditEvidenceProducer(StrEnum):
    FORGE_CONTRACT_CORE = "forge_contract_core"
    FORGE_SMITHY = "forge-smithy"
    FORGE_AGENTS = "Forge-Agents"
    DATAFORGE_LOCAL = "DataForge Local"
    FORGE_COMMAND = "Forge_Command"
    NEUROFORGE = "NeuroForge"
    OPERATOR = "operator"


class TripleVariantAuditTargetType(StrEnum):
    REPO = "repo"
    PATCH = "patch"
    AGENT_RUN = "agent_run"
    AAR_RECORD = "aar_record"
    PROVIDER_RESULT = "provider_result"
    REVIEW_ARTIFACT = "review_artifact"


class TripleVariantAuditTier(StrEnum):
    FAST_PR = "FAST_PR"
    STANDARD_PR = "STANDARD_PR"
    NIGHTLY_FULL = "NIGHTLY_FULL"
    RELEASE_GATE = "RELEASE_GATE"
    INCIDENT_REPLAY = "INCIDENT_REPLAY"


class TripleVariantAuditRerunReason(StrEnum):
    REQUEST_REPAIR = "REQUEST_REPAIR"
    ESCALATE_TO_SMITH = "ESCALATE_TO_SMITH"
    OPERATOR_RECHECK = "OPERATOR_RECHECK"
    INCIDENT_REPLAY = "INCIDENT_REPLAY"
    CACHE_REVALIDATION = "CACHE_REVALIDATION"


class TripleVariantAuditFinalStatus(StrEnum):
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    NEEDS_OPERATOR_REVIEW = "NEEDS_OPERATOR_REVIEW"
    BLOCKED_CONTRACT_FAILURE = "BLOCKED_CONTRACT_FAILURE"
    BLOCKED_RUNTIME_FAILURE = "BLOCKED_RUNTIME_FAILURE"
    BLOCKED_DRIFT_RISK = "BLOCKED_DRIFT_RISK"
    BLOCKED_MISSING_RECEIPT = "BLOCKED_MISSING_RECEIPT"
    BLOCKED_UNAUTHORIZED_MUTATION = "BLOCKED_UNAUTHORIZED_MUTATION"


class TripleVariantAuditGateDecision(StrEnum):
    ALLOW_PROMOTION = "ALLOW_PROMOTION"
    BLOCK_PROMOTION = "BLOCK_PROMOTION"
    REQUIRE_OPERATOR_REVIEW = "REQUIRE_OPERATOR_REVIEW"
    ESCALATE_TO_SMITH = "ESCALATE_TO_SMITH"


class TripleVariantAuditProviderMode(StrEnum):
    NONE = "none"
    MOCKED = "mocked"
    REPLAYED = "replayed"
    LIVE = "live"


# Admitted families — proving slice 01 + execution bridge v1 + evaluation spine phase 02
# + LLM provider intelligence contract slice 01 + triple-variant audit proof slice 01.
ADMITTED_FAMILIES: frozenset[str] = frozenset(
    {
        "source_drift_finding",
        "promotion_envelope",
        "promotion_receipt",
        "execution_request",
        "execution_status_event",
        "approval_artifact",
        "forge_eval_evidence_bundle",
        "eval_calibration_report",
        "forgemath_lane_evaluation_ref",
        "forgehq_upstream_evidence_refs",
        "evaluation_spine_detail_model",
        "llm_intel_weekly_run",
        "llm_intel_approved_source",
        "source_trust_classification",
        "provider_extraction_profile",
        "provider_adapter_receipt",
        "llm_intel_fetch_receipt",
        "llm_intel_source_fingerprint",
        "llm_intel_extracted_claim",
        "llm_intel_drift_report",
        "llm_intel_review_packet",
        "llm_intel_promotion_decision",
        "llm_intel_promoted_record",
        "promotion_state_machine",
        "triple_variant_audit_receipt",
        "triple_variant_audit_lane_result",
        "triple_variant_audit_finding",
        "triple_variant_audit_evidence_ref",
        "triple_variant_audit_gate_decision",
        "triple_variant_audit_replay_manifest",
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
    "forge_eval_evidence_bundle": frozenset({1}),
    "eval_calibration_report": frozenset({1}),
    "forgemath_lane_evaluation_ref": frozenset({1}),
    "forgehq_upstream_evidence_refs": frozenset({1}),
    "evaluation_spine_detail_model": frozenset({1}),
    "llm_intel_weekly_run": frozenset({1}),
    "llm_intel_approved_source": frozenset({1}),
    "source_trust_classification": frozenset({1}),
    "provider_extraction_profile": frozenset({1}),
    "provider_adapter_receipt": frozenset({1}),
    "llm_intel_fetch_receipt": frozenset({1}),
    "llm_intel_source_fingerprint": frozenset({1}),
    "llm_intel_extracted_claim": frozenset({1}),
    "llm_intel_drift_report": frozenset({1}),
    "llm_intel_review_packet": frozenset({1}),
    "llm_intel_promotion_decision": frozenset({1}),
    "llm_intel_promoted_record": frozenset({1}),
    "promotion_state_machine": frozenset({1}),
    "triple_variant_audit_receipt": frozenset({1}),
    "triple_variant_audit_lane_result": frozenset({1}),
    "triple_variant_audit_finding": frozenset({1}),
    "triple_variant_audit_evidence_ref": frozenset({1}),
    "triple_variant_audit_gate_decision": frozenset({1}),
    "triple_variant_audit_replay_manifest": frozenset({1}),
}

# Sensitivity classes that permit promotion
PROMOTABLE_SENSITIVITY_CLASSES: frozenset[str] = frozenset(
    {
        SensitivityClass.PUBLIC,
        SensitivityClass.INTERNAL,
    }
)
