export const riskFlags = [
  "MEMORY_CONFLICT",
  "LOW_SAMPLE_SIZE",
  "SCHEMA_EDGECASE",
  "PROMPT_INJECTION_SIGNAL",
  "POLICY_AMBIGUITY",
  "PII_RISK_SUSPECTED",
  "TOOL_SCOPE_RISK",
] as const;
export type RiskFlag = (typeof riskFlags)[number];

export const retryReasons = [
  "TRANSIENT_TIMEOUT",
  "BUDGET_RETRY",
  "CONFIDENCE_LOW",
  "OTHER",
] as const;
export type RetryReason = (typeof retryReasons)[number];

export const envelopeStatuses = ["success", "revise", "reject", "system_fault", "constraint_violation"] as const;
export type EnvelopeStatus = (typeof envelopeStatuses)[number];

// Normalized terminal outcomes for RunEvidence.v1
export const resultStatuses = ["pass", "fail", "aborted", "system_fault"] as const;
export type RunResultStatus = (typeof resultStatuses)[number];

// Fail reason (stored in metadata when final_status == "fail")
// Preserves semantic meaning for analytics and learning loops
export const failReasons = [
  "quality_reject",         // Critic gate rejected output quality
  "constraint_violation",   // Output violated constraints
  "policy_violation",       // Policy engine rejected
  "max_retries_exceeded",   // Exhausted retry budget
  "node_failure",           // A node failed to execute
  "validation_error",       // Schema or data validation failed
  "timeout",                // Execution timed out
  "dependency_failure",     // Upstream dependency failed
] as const;
export type FailReason = (typeof failReasons)[number];

// Abort metadata (stored in metadata when final_status == "aborted")
export const abortKinds = ["graceful", "hard"] as const;
export type AbortKind = (typeof abortKinds)[number];

export const abortReasons = [
  "operator_cancel",    // User requested cancellation
  "safety_timeout",     // Safety brake timeout escalation
  "max_steps",          // Max retries/steps exceeded
  "policy_violation",   // Policy engine rejection
  "resource_limit",     // Resource exhaustion
  "external_signal",    // External termination signal
] as const;
export type AbortReason = (typeof abortReasons)[number];
