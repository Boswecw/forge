import { canonicalizeJson, JsonValue } from "./canonical_json.js";
import { sha256Prefixed } from "./hashes.js";
import {
  envelopeStatuses,
  riskFlags,
  retryReasons,
  EnvelopeStatus,
  RiskFlag,
  RetryReason,
} from "./vocab.js";

const ISO_TIMESTAMP_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const SHA256_PATTERN = /^sha256:[0-9a-f]{64}$/;

export interface NodeEnvelope {
  envelope_version: "NodeEnvelope.v1";
  envelope_id: string;
  node: {
    node_id: string;
    node_type?: string;
  };
  context: {
    workflow_id: string;
    session_id: string;
    run_id: string;
    trace_id: string;
    repo: {
      repo_id: string;
      repo_sha: string;
      branch: string;
    };
    environment: {
      mode: "interactive" | "batch" | "ci";
      invoker: "cli" | "ui" | "api";
    };
  };
  constraints: {
    constraint_version: string;
    tools_allowed: Array<"none" | "read_only">;
    expected_output_schema: {
      schema_id: string;
      schema_hash: string;
    };
    token_budget: {
      total: number;
      priority_order: string[];
      overrun_policy: "forbid" | "warn";
    };
    stop_conditions: string[];
  };
  inputs: Record<string, HashEntry>;
  execution: {
    attempt: number;
    max_retries: number;
    parallel_group: string;
    dependency_strategy: "wait_all" | "fail_fast";
    timeouts_ms: {
      soft: number;
      hard: number;
    };
    queued_at?: string;
  };
  outputs: {
    status: EnvelopeStatus;
    payload: {
      type: string;
      data: JsonValue;
    };
    messages: Message[];
    fault?: Fault;
  };
  provenance: {
    usage_stats: {
      input_tokens: number;
      output_tokens: number;
      total_tokens: number;
      model_id: string;
    };
    input_hashes: Record<string, string>;
    schema_manifest: {
      output_schema_id: string;
      output_schema_hash: string;
    };
    constraint_hash: string;
    node_runtime: {
      started_at: string;
      ended_at: string;
      latency_ms: number;
    };
    confidence_score: number;
    confidence_scale: string;
    confidence_source: "model" | "postprocessed";
    risk_flags: RiskFlag[];
    retry_reason?: RetryReason;
  };
}

export interface HashEntry {
  hash: string;
  schema_id?: string;
}

export interface Message {
  level: "info" | "warning" | "error";
  message: string;
}

export interface Fault {
  code: string;
  retryable: boolean;
  detail: string;
}

export type ValidatedNodeEnvelope = NodeEnvelope;

export interface ValidationError {
  path: string;
  message: string;
}

export type ValidationResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: ValidationError };

function fail<T>(message: string, path: string): ValidationResult<T> {
  return {
    ok: false,
    error: { message, path },
  };
}

function success<T>(value: T): ValidationResult<T> {
  return { ok: true, value };
}

function parseTimestamp(value: unknown, path: string): ValidationResult<Date> {
  if (typeof value !== "string" || !ISO_TIMESTAMP_PATTERN.test(value)) {
    return fail("timestamp must be ISO-8601 with Z suffix", path);
  }

  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) {
    return fail("timestamp is not a valid date", path);
  }

  return success(new Date(parsed));
}

function ensureSha256(value: unknown, path: string): ValidationResult<string> {
  if (typeof value !== "string" || !SHA256_PATTERN.test(value)) {
    return fail("value must be a lowercase sha256 hash", path);
  }
  return success(value);
}

function ensureNonEmptyString(value: unknown, path: string): ValidationResult<string> {
  if (typeof value !== "string" || value.trim() === "") {
    return fail("value must be a non-empty string", path);
  }
  return success(value);
}

export function validateNodeEnvelope(
  envelope: NodeEnvelope
): ValidationResult<ValidatedNodeEnvelope> {
  if (envelope.envelope_version !== "NodeEnvelope.v1") {
    return fail("unsupported envelope_version", "envelope_version");
  }

  if (!envelope.envelope_id || typeof envelope.envelope_id !== "string") {
    return fail("envelope_id is required", "envelope_id");
  }

  if (!envelope.node?.node_id) {
    return fail("node_id is required", "node.node_id");
  }

  const env = envelope.context;
  if (!env) {
    return fail("context block is required", "context");
  }

  const contextFields = [
    ["workflow_id", env.workflow_id],
    ["session_id", env.session_id],
    ["run_id", env.run_id],
    ["trace_id", env.trace_id],
  ] as const;
  for (const [name, value] of contextFields) {
    if (!value) {
      return fail(`${name} must be provided`, `context.${name}`);
    }
  }

  const repo = env.repo;
  if (!repo) {
    return fail("repo block is required", "context.repo");
  }
  if (!repo.repo_id || !repo.repo_sha || !repo.branch) {
    return fail("repo metadata must include id, sha, and branch", "context.repo");
  }

  const envMode = env.environment;
  if (!envMode) {
    return fail("environment block is required", "context.environment");
  }
  if (!["interactive", "batch", "ci"].includes(envMode.mode)) {
    return fail("environment.mode must be interactive | batch | ci", "context.environment.mode");
  }
  if (!["cli", "ui", "api"].includes(envMode.invoker)) {
    return fail("environment.invoker must be cli | ui | api", "context.environment.invoker");
  }

  const constraints = envelope.constraints;
  if (!constraints) {
    return fail("constraints block is required", "constraints");
  }

  if (
    !constraints.expected_output_schema ||
    !constraints.expected_output_schema.schema_id ||
    !constraints.expected_output_schema.schema_hash
  ) {
    return fail(
      "expected_output_schema must supply schema_id and schema_hash",
      "constraints.expected_output_schema"
    );
  }

  if (!constraints.token_budget) {
    return fail("token_budget is required", "constraints.token_budget");
  }

  if (
    !Array.isArray(constraints.token_budget.priority_order) ||
    constraints.token_budget.priority_order.length === 0
  ) {
    return fail("priority_order must list at least one bucket", "constraints.token_budget.priority_order");
  }

  if (
    !Number.isFinite(constraints.token_budget.total) ||
    constraints.token_budget.total < 0
  ) {
    return fail("token_budget.total must be a non-negative finite number", "constraints.token_budget.total");
  }

  if (!["forbid", "warn"].includes(constraints.token_budget.overrun_policy)) {
    return fail("invalid overrun_policy", "constraints.token_budget.overrun_policy");
  }

  if (
    !Array.isArray(constraints.tools_allowed) ||
    constraints.tools_allowed.some((tool) => tool !== "none" && tool !== "read_only")
  ) {
    return fail("tools_allowed entries must be none or read_only", "constraints.tools_allowed");
  }

  if (
    !Array.isArray(constraints.stop_conditions) ||
    constraints.stop_conditions.length === 0 ||
    constraints.stop_conditions.some((item) => typeof item !== "string" || item.trim() === "")
  ) {
    return fail("stop_conditions must be non-empty strings", "constraints.stop_conditions");
  }

  const inputs = envelope.inputs ?? {};
  for (const [key, entry] of Object.entries(inputs)) {
    if (!entry || typeof entry.hash !== "string") {
      return fail("input hash entries must include a hash string", `inputs.${key}.hash`);
    }
    if (!SHA256_PATTERN.test(entry.hash)) {
      return fail("input hashes must be sha256", `inputs.${key}.hash`);
    }
  }

  const execution = envelope.execution;
  if (!execution) {
    return fail("execution block is required", "execution");
  }
  if (!Number.isInteger(execution.attempt) || execution.attempt < 1) {
    return fail("attempt must be an integer >= 1", "execution.attempt");
  }
  if (!Number.isInteger(execution.max_retries) || execution.max_retries < 0) {
    return fail("max_retries must be a non-negative integer", "execution.max_retries");
  }
  if (!execution.parallel_group || typeof execution.parallel_group !== "string") {
    return fail("parallel_group is required", "execution.parallel_group");
  }
  if (!["wait_all", "fail_fast"].includes(execution.dependency_strategy)) {
    return fail("invalid dependency_strategy", "execution.dependency_strategy");
  }

  if (
    !execution.timeouts_ms ||
    typeof execution.timeouts_ms.soft !== "number" ||
    typeof execution.timeouts_ms.hard !== "number"
  ) {
    return fail("timeouts_ms must include soft and hard values", "execution.timeouts_ms");
  }
  if (execution.timeouts_ms.soft < 0 || execution.timeouts_ms.hard < 0) {
    return fail("timeouts must be non-negative", "execution.timeouts_ms");
  }

  if (execution.queued_at) {
    const queuedResult = parseTimestamp(execution.queued_at, "execution.queued_at");
    if (!queuedResult.ok) {
      return queuedResult;
    }
  }

  const outputs = envelope.outputs;
  if (!outputs) {
    return fail("outputs block is required", "outputs");
  }
  if (!envelopeStatuses.includes(outputs.status)) {
    return fail("invalid outputs.status", "outputs.status");
  }
  if (!outputs.payload?.type) {
    return fail("payload.type is required", "outputs.payload.type");
  }
  if (outputs.payload.type !== constraints.expected_output_schema.schema_id) {
    return fail(
      "payload.type must match constraints.expected_output_schema.schema_id",
      "outputs.payload.type"
    );
  }

  if (outputs.payload.data === undefined) {
    return fail("payload.data is required", "outputs.payload.data");
  }

  if (!Array.isArray(outputs.messages)) {
    return fail("outputs.messages must be an array", "outputs.messages");
  }

  for (let i = 0; i < outputs.messages.length; i += 1) {
    const message = outputs.messages[i];
    if (!message || typeof message.message !== "string" || message.message.trim() === "") {
      return fail("message text is required", `outputs.messages[${i}].message`);
    }
    if (!["info", "warning", "error"].includes(message.level)) {
      return fail("message level must be info|warning|error", `outputs.messages[${i}].level`);
    }
  }

  const statusRequiresFault: EnvelopeStatus[] = ["system_fault", "constraint_violation"];
  if (statusRequiresFault.includes(outputs.status) && !outputs.fault) {
    return fail("fault must be present for fault statuses", "outputs.fault");
  }
  if (!statusRequiresFault.includes(outputs.status) && outputs.fault) {
    return fail("fault must be absent for non-fault statuses", "outputs.fault");
  }

  if (outputs.status === "constraint_violation" && outputs.fault?.retryable !== false) {
    return fail("constraint_violation faults must not be retryable", "outputs.fault.retryable");
  }

  const provenance = envelope.provenance;
  if (!provenance) {
    return fail("provenance is required", "provenance");
  }

  if (
    !provenance.schema_manifest ||
    provenance.schema_manifest.output_schema_id !== constraints.expected_output_schema.schema_id
  ) {
    return fail(
      "schema_manifest.output_schema_id must match expected_output_schema.schema_id",
      "provenance.schema_manifest.output_schema_id"
    );
  }

  if (
    provenance.schema_manifest.output_schema_hash !==
    constraints.expected_output_schema.schema_hash
  ) {
    return fail(
      "schema_manifest.output_schema_hash must match constraints expected schema_hash",
      "provenance.schema_manifest.output_schema_hash"
    );
  }

  const schemaHashResult = ensureSha256(
    provenance.schema_manifest.output_schema_hash,
    "provenance.schema_manifest.output_schema_hash"
  );
  if (!schemaHashResult.ok) {
    return schemaHashResult;
  }

  const constraintHashResult = ensureSha256(provenance.constraint_hash, "provenance.constraint_hash");
  if (!constraintHashResult.ok) {
    return constraintHashResult;
  }

  const usage = provenance.usage_stats;
  if (!usage) {
    return fail("usage_stats is required", "provenance.usage_stats");
  }
  if (
    !Number.isFinite(usage.input_tokens) ||
    !Number.isFinite(usage.output_tokens) ||
    !Number.isFinite(usage.total_tokens)
  ) {
    return fail("usage stats must be numeric", "provenance.usage_stats");
  }

  if (!usage.model_id) {
    return fail("usage_stats.model_id is required", "provenance.usage_stats.model_id");
  }

  const runtime = provenance.node_runtime;
  if (!runtime) {
    return fail("node_runtime is required", "provenance.node_runtime");
  }

  const started = parseTimestamp(runtime.started_at, "provenance.node_runtime.started_at");
  if (!started.ok) {
    return started;
  }
  const ended = parseTimestamp(runtime.ended_at, "provenance.node_runtime.ended_at");
  if (!ended.ok) {
    return ended;
  }
  const durationMs = ended.value.getTime() - started.value.getTime();
  if (durationMs < 0) {
    return fail("ended_at must not be before started_at", "provenance.node_runtime");
  }
  if (typeof runtime.latency_ms !== "number" || runtime.latency_ms < 0) {
    return fail("latency_ms must be a non-negative number", "provenance.node_runtime.latency_ms");
  }
  if (runtime.latency_ms < durationMs) {
    return fail(
      "latency_ms must be greater than or equal to the observed duration",
      "provenance.node_runtime.latency_ms"
    );
  }

  if (provenance.confidence_score < 0 || provenance.confidence_score > 1) {
    return fail("confidence_score must be between 0 and 1", "provenance.confidence_score");
  }
  if (
    !provenance.confidence_scale ||
    typeof provenance.confidence_scale !== "string" ||
    provenance.confidence_scale.trim() === ""
  ) {
    return fail("confidence_scale is required", "provenance.confidence_scale");
  }
  if (!["model", "postprocessed"].includes(provenance.confidence_source)) {
    return fail("confidence_source must be model or postprocessed", "provenance.confidence_source");
  }

  if (!Array.isArray(provenance.risk_flags)) {
    return fail("risk_flags must be an array", "provenance.risk_flags");
  }
  for (let i = 0; i < provenance.risk_flags.length; i += 1) {
    if (!riskFlags.includes(provenance.risk_flags[i])) {
      return fail("risk_flags entry is invalid", `provenance.risk_flags[${i}]`);
    }
  }

  if (execution.attempt > 1) {
    if (!provenance.retry_reason) {
      return fail("retry_reason required for retries", "provenance.retry_reason");
    }
    if (!retryReasons.includes(provenance.retry_reason)) {
      return fail("retry_reason must be from the controlled vocabulary", "provenance.retry_reason");
    }
  } else if (provenance.retry_reason) {
    return fail("retry_reason must be absent when attempt equals 1", "provenance.retry_reason");
  }

  if (envelope.outputs.status === "success") {
    const totalTokens = provenance.usage_stats.total_tokens;
    if (
      constraints.token_budget.overrun_policy === "forbid" &&
      totalTokens > constraints.token_budget.total
    ) {
      return fail("token budget forbid policy blocks success when budget is exceeded", "outputs.status");
    }
  }

  const schemaHashMatches = ensureSha256(constraints.expected_output_schema.schema_hash, "constraints.expected_output_schema.schema_hash");
  if (!schemaHashMatches.ok) {
    return schemaHashMatches;
  }

  for (const [key, value] of Object.entries(provenance.input_hashes ?? {})) {
    if (!SHA256_PATTERN.test(value)) {
      return fail("input hash must be sha256", `provenance.input_hashes.${key}`);
    }
  }

  return success(envelope);
}

export function finalizeNodeEnvelope(envelope: NodeEnvelope): {
  envelope: NodeEnvelope;
  envelope_hash: string;
} {
  const bytes = canonicalizeJson(envelope as unknown as JsonValue);
  return {
    envelope,
    envelope_hash: sha256Prefixed(bytes),
  };
}
