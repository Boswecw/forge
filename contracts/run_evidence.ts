import {
  canonicalizeJson,
  JsonValue,
} from "./canonical_json.js";
import { sha256Prefixed } from "./hashes.js";
import {
  envelopeStatuses,
  riskFlags,
  retryReasons,
  resultStatuses,
  RiskFlag,
  RetryReason,
  RunResultStatus,
  EnvelopeStatus,
} from "./vocab.js";
import {
  NodeEnvelope,
  ValidationResult,
  validateNodeEnvelope,
  finalizeNodeEnvelope,
} from "./node_envelope.js";

const ISO_TIMESTAMP_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const SHA256_PATTERN = /^sha256:[0-9a-f]{64}$/;

export interface RunEvidence {
  evidence_version: "RunEvidence.v1";
  trace_id: string;
  run_id: string;
  session_id: string;
  workflow_id: string;
  created_at: string;
  runner: {
    service: string;
    module: string;
    version: string;
    host: {
      machine_id: string;
      os: string;
      arch: string;
    };
    mode: "interactive" | "batch" | "ci";
  };
  inputs: {
    stdin_hash: string;
    stdin_normalized_hash: string;
    repo: {
      repo_id: string;
      repo_sha: string;
      branch: string;
    };
    constraint_version: string;
    constraint_hash: string;
  };
  plan: {
    nodes: PlanNode[];
    dependency_strategy_default: "wait_all" | "fail_fast";
    max_retries_default: number;
  };
  windows: {
    attempt_windows: AttemptWindow[];
  };
  node_executions: NodeExecution[];
  orchestration: {
    parallel_groups: ParallelGroup[];
    retries: OrchestrationRetry[];
    skips: OrchestrationSkip[];
  };
  result: {
    final_status: RunResultStatus;
    promotion_ready: boolean;
    confidence_floor: number;
    highest_risk_flags: RiskFlag[];
    notes: string;
  };
  hashes: {
    run_evidence_hash: string;
    node_envelope_hashes: Array<{
      envelope_id: string;
      hash: string;
    }>;
  };
}

export interface PlanNode {
  node_id: string;
  parallel_group: string;
  depends_on: string[];
}

export interface AttemptWindow {
  attempt_index: number;
  node_windows: NodeWindow[];
}

export interface NodeWindow {
  node_id: string;
  allowed_start: string;
  allowed_end: string;
}

export interface NodeExecution {
  attempt_index: number;
  node_id: string;
  envelope_id: string;
  envelope_hash: string;
  status: EnvelopeStatus;
  started_at: string;
  ended_at: string;
}

export interface ParallelGroup {
  name: string;
  nodes: string[];
  dependency_strategy: "wait_all" | "fail_fast";
}

export interface OrchestrationRetry {
  node_id: string;
  attempt_index: number;
  reason: RetryReason;
}

export interface OrchestrationSkip {
  node_id: string;
  reason: string;
}

export type ValidatedRunEvidence = RunEvidence;

function fail<T>(message: string, path: string): ValidationResult<T> {
  return { ok: false, error: { message, path } };
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

function cloneWithoutRunHash(evidence: RunEvidence): JsonValue {
  const clone = JSON.parse(JSON.stringify(evidence)) as JsonValue;
  if (typeof clone === "object" && clone !== null) {
    const cloneObj = clone as Record<string, unknown>;
    if (cloneObj.hashes && typeof cloneObj.hashes === "object") {
      const hashes = cloneObj.hashes as Record<string, unknown>;
      delete hashes.run_evidence_hash;
    }
  }
  return clone;
}

function computeRunEvidenceHash(evidence: RunEvidence): string {
  return sha256Prefixed(canonicalizeJson(cloneWithoutRunHash(evidence)));
}

export function validateRunEvidence(
  evidence: RunEvidence
): ValidationResult<ValidatedRunEvidence> {
  if (evidence.evidence_version !== "RunEvidence.v1") {
    return fail("unsupported evidence_version", "evidence_version");
  }

  for (const [key, value] of [
    ["trace_id", evidence.trace_id],
    ["run_id", evidence.run_id],
    ["session_id", evidence.session_id],
    ["workflow_id", evidence.workflow_id],
  ] as const) {
    if (!value || typeof value !== "string") {
      return fail(`${key} is required`, key);
    }
  }

  const createdResult = parseTimestamp(evidence.created_at, "created_at");
  if (!createdResult.ok) {
    return createdResult;
  }

  const runner = evidence.runner;
  if (!runner) {
    return fail("runner block is required", "runner");
  }
  if (!runner.service || !runner.module || !runner.version) {
    return fail("runner metadata must include service/module/version", "runner");
  }
  if (!runner.host || !runner.host.machine_id || !runner.host.os || !runner.host.arch) {
    return fail("runner.host must include machine_id/os/arch", "runner.host");
  }
  if (!["interactive", "batch", "ci"].includes(runner.mode)) {
    return fail("runner.mode must be interactive | batch | ci", "runner.mode");
  }

  const inputs = evidence.inputs;
  if (!inputs) {
    return fail("inputs block is required", "inputs");
  }
  const shaFields = [
    ["stdin_hash", inputs.stdin_hash],
    ["stdin_normalized_hash", inputs.stdin_normalized_hash],
    ["constraint_hash", inputs.constraint_hash],
  ] as const;
  for (const [path, value] of shaFields) {
    const hashCheck = ensureSha256(value, `inputs.${path}`);
    if (!hashCheck.ok) {
      return hashCheck;
    }
  }

  if (!inputs.repo || !inputs.repo.repo_id || !inputs.repo.repo_sha || !inputs.repo.branch) {
    return fail("inputs.repo must include repo_id/repo_sha/branch", "inputs.repo");
  }

  if (!inputs.constraint_version) {
    return fail("constraint_version is required", "inputs.constraint_version");
  }

  const plan = evidence.plan;
  if (!plan || !Array.isArray(plan.nodes) || plan.nodes.length === 0) {
    return fail("plan.nodes must include at least one node", "plan.nodes");
  }

  if (!["wait_all", "fail_fast"].includes(plan.dependency_strategy_default)) {
    return fail(
      "plan.dependency_strategy_default must be wait_all or fail_fast",
      "plan.dependency_strategy_default"
    );
  }
  if (!Number.isInteger(plan.max_retries_default) || plan.max_retries_default < 0) {
    return fail("plan.max_retries_default must be a non-negative integer", "plan.max_retries_default");
  }

  const nodeIdSet = new Set(plan.nodes.map((entry) => entry.node_id));
  if (nodeIdSet.size !== plan.nodes.length) {
    return fail("plan.nodes must use unique node_id values", "plan.nodes");
  }

  for (const node of plan.nodes) {
    if (!node.node_id || !node.parallel_group || !Array.isArray(node.depends_on)) {
      return fail("plan node must include node_id, parallel_group, depends_on", "plan.nodes");
    }
    for (const dep of node.depends_on) {
      if (!nodeIdSet.has(dep)) {
        return fail("plan.depends_on entries must reference defined nodes", "plan.nodes.depends_on");
      }
    }
  }

  const visitState = new Map<string, "visiting" | "visited">();
  const detectCycle = (nodeId: string): ValidationResult<void> => {
    const state = visitState.get(nodeId);
    if (state === "visiting") {
      return fail("plan nodes must form a DAG", `plan.nodes:${nodeId}`);
    }
    if (state === "visited") {
      return success(undefined);
    }
    visitState.set(nodeId, "visiting");
    const node = plan.nodes.find((entry) => entry.node_id === nodeId);
    if (!node) {
      return fail("plan node missing during cycle detection", `plan.nodes:${nodeId}`);
    }
    for (const dep of node.depends_on) {
      const result = detectCycle(dep);
      if (!result.ok) {
        return result;
      }
    }
    visitState.set(nodeId, "visited");
    return success(undefined);
  };

  for (const nodeId of nodeIdSet) {
    const cycleResult = detectCycle(nodeId);
    if (!cycleResult.ok) {
      return cycleResult;
    }
  }

  const windows = evidence.windows;
  if (!windows || !Array.isArray(windows.attempt_windows) || windows.attempt_windows.length === 0) {
    return fail("windows.attempt_windows must exist", "windows.attempt_windows");
  }

  if (!windows.attempt_windows.some((window) => window.attempt_index === 1)) {
    return fail("attempt_windows must include attempt_index 1", "windows.attempt_windows");
  }

  for (const attemptWindow of windows.attempt_windows) {
    if (!Number.isInteger(attemptWindow.attempt_index) || attemptWindow.attempt_index < 1) {
      return fail("attempt_index must be >= 1", "windows.attempt_windows.attempt_index");
    }
    if (!Array.isArray(attemptWindow.node_windows)) {
      return fail("node_windows must be an array", "windows.attempt_windows.node_windows");
    }
    for (const nodeWindow of attemptWindow.node_windows) {
      if (!nodeWindow.node_id || !nodeWindow.allowed_start || !nodeWindow.allowed_end) {
        return fail(
          "node_window entries require node_id, allowed_start, allowed_end",
          "windows.attempt_windows.node_windows"
        );
      }
      const startResult = parseTimestamp(nodeWindow.allowed_start, "windows.allowed_start");
      if (!startResult.ok) {
        return startResult;
      }
      const endResult = parseTimestamp(nodeWindow.allowed_end, "windows.allowed_end");
      if (!endResult.ok) {
        return endResult;
      }
      if (endResult.value.getTime() < startResult.value.getTime()) {
        return fail("allowed_end must not precede allowed_start", "windows.attempt_windows.node_windows");
      }
    }
  }

  const nodeExecutions = evidence.node_executions;
  if (!Array.isArray(nodeExecutions) || nodeExecutions.length === 0) {
    return fail("node_executions must include at least one entry", "node_executions");
  }

  const executionEnvelopeIds = new Set<string>();
  for (const execution of nodeExecutions) {
    if (!execution.envelope_id || !execution.envelope_hash) {
      return fail("node_execution entries must include envelope metadata", "node_executions");
    }
    if (!SHA256_PATTERN.test(execution.envelope_hash)) {
      return fail("node_execution.envelope_hash must be sha256", "node_executions.envelope_hash");
    }
    if (!envelopeStatuses.includes(execution.status)) {
      return fail("node_execution.status must be a valid envelope status", "node_executions.status");
    }
    if (!nodeIdSet.has(execution.node_id)) {
      return fail("node_execution.node_id must refer to a plan node", "node_executions.node_id");
    }
    if (!Number.isInteger(execution.attempt_index) || execution.attempt_index < 1) {
      return fail("node_execution.attempt_index must be >=1", "node_executions.attempt_index");
    }
    const started = parseTimestamp(execution.started_at, "node_executions.started_at");
    if (!started.ok) {
      return started;
    }
    const ended = parseTimestamp(execution.ended_at, "node_executions.ended_at");
    if (!ended.ok) {
      return ended;
    }
    if (ended.value.getTime() < started.value.getTime()) {
      return fail("node_execution.ended_at must be >= started_at", "node_executions");
    }
    if (executionEnvelopeIds.has(execution.envelope_id)) {
      return fail("duplicate envelope_id in node_executions", "node_executions.envelope_id");
    }
    executionEnvelopeIds.add(execution.envelope_id);
  }

  const orchestration = evidence.orchestration;
  if (!orchestration) {
    return fail("orchestration block is required", "orchestration");
  }

  if (!Array.isArray(orchestration.parallel_groups)) {
    return fail("parallel_groups must be an array", "orchestration.parallel_groups");
  }
  for (const group of orchestration.parallel_groups) {
    if (!group.name || !Array.isArray(group.nodes) || group.nodes.length === 0) {
      return fail("parallel_group entries require name and nodes", "orchestration.parallel_groups");
    }
    if (!["wait_all", "fail_fast"].includes(group.dependency_strategy)) {
      return fail(
        "parallel_group dependency_strategy must be wait_all | fail_fast",
        "orchestration.parallel_groups.dependency_strategy"
      );
    }
    for (const nodeId of group.nodes) {
      if (!nodeIdSet.has(nodeId)) {
        return fail("parallel_group nodes must come from plan.nodes", "orchestration.parallel_groups.nodes");
      }
    }
  }

  for (const retry of orchestration.retries ?? []) {
    if (!retry.node_id || !nodeIdSet.has(retry.node_id)) {
      return fail("retry.node_id must reference a plan node", "orchestration.retries.node_id");
    }
    if (!Number.isInteger(retry.attempt_index) || retry.attempt_index < 1) {
      return fail("retry.attempt_index must be >= 1", "orchestration.retries.attempt_index");
    }
    if (!retry.reason || !retryReasons.includes(retry.reason)) {
      return fail("retry.reason must come from the controlled vocabulary", "orchestration.retries.reason");
    }
  }

  for (const skip of orchestration.skips ?? []) {
    if (!skip.node_id || !nodeIdSet.has(skip.node_id)) {
      return fail("skip.node_id must reference a plan node", "orchestration.skips.node_id");
    }
    if (!skip.reason) {
      return fail("skip.reason must be provided", "orchestration.skips.reason");
    }
  }

  const result = evidence.result;
  if (!result) {
    return fail("result block is required", "result");
  }
  if (!resultStatuses.includes(result.final_status)) {
    return fail("result.final_status must be a known state", "result.final_status");
  }
  if (typeof result.promotion_ready !== "boolean") {
    return fail("result.promotion_ready must be boolean", "result.promotion_ready");
  }
  if (
    typeof result.confidence_floor !== "number" ||
    result.confidence_floor < 0 ||
    result.confidence_floor > 1
  ) {
    return fail("result.confidence_floor must be between 0 and 1", "result.confidence_floor");
  }
  if (!Array.isArray(result.highest_risk_flags)) {
    return fail("result.highest_risk_flags must be an array", "result.highest_risk_flags");
  }
  for (const [index, flag] of result.highest_risk_flags.entries()) {
    if (!riskFlags.includes(flag)) {
      return fail("result.highest_risk_flags entries must be whitelisted", `result.highest_risk_flags[${index}]`);
    }
  }
  if (!result.notes || typeof result.notes !== "string") {
    return fail("result.notes must be a non-empty string", "result.notes");
  }

  const hashes = evidence.hashes;
  if (!hashes || !hashes.run_evidence_hash || !Array.isArray(hashes.node_envelope_hashes)) {
    return fail("hashes block must include run_evidence_hash and node_envelope_hashes", "hashes");
  }

  const runHashCheck = ensureSha256(hashes.run_evidence_hash, "hashes.run_evidence_hash");
  if (!runHashCheck.ok) {
    return runHashCheck;
  }

  const envelopeHashMap = new Map<string, string>();
  for (const entry of hashes.node_envelope_hashes) {
    if (
      !entry.envelope_id ||
      !entry.hash ||
      !SHA256_PATTERN.test(entry.hash) ||
      envelopeHashMap.has(entry.envelope_id)
    ) {
      return fail("node_envelope_hashes entries must include unique sha256 hashes", "hashes.node_envelope_hashes");
    }
    envelopeHashMap.set(entry.envelope_id, entry.hash);
  }

  if (envelopeHashMap.size !== nodeExecutions.length) {
    return fail(
      "node_envelope_hashes must cover each node_execution entry",
      "hashes.node_envelope_hashes"
    );
  }

  for (const execution of nodeExecutions) {
    const mappedHash = envelopeHashMap.get(execution.envelope_id);
    if (!mappedHash) {
      return fail(
        "each node_execution.envelope_id must appear in hashes.node_envelope_hashes",
        "hashes.node_envelope_hashes"
      );
    }
    if (mappedHash !== execution.envelope_hash) {
      return fail(
        "node_execution.envelope_hash must match the ledger entry",
        "node_executions.envelope_hash"
      );
    }
  }

  const canonicalHash = computeRunEvidenceHash(evidence);
  if (canonicalHash !== hashes.run_evidence_hash) {
    return fail("run_evidence_hash mismatch", "hashes.run_evidence_hash");
  }

  return success(evidence);
}

export function finalizeRunEvidence(evidence: RunEvidence): {
  evidence: RunEvidence;
  run_evidence_hash: string;
} {
  const runEvidenceHash = computeRunEvidenceHash(evidence);
  return {
    run_evidence_hash: runEvidenceHash,
    evidence: {
      ...evidence,
      hashes: {
        ...evidence.hashes,
        run_evidence_hash: runEvidenceHash,
      },
    },
  };
}

export function verifyEnvelopeAgainstEvidence(
  envelope: NodeEnvelope,
  evidence: RunEvidence
): ValidationResult<void> {
  const envelopeValidation = validateNodeEnvelope(envelope);
  if (!envelopeValidation.ok) {
    return envelopeValidation;
  }

  const evidenceValidation = validateRunEvidence(evidence);
  if (!evidenceValidation.ok) {
    return evidenceValidation;
  }

  const attemptIndex = envelope.execution.attempt;
  const nodeId = envelope.node.node_id;
  const runtime = envelope.provenance.node_runtime;

  const attemptWindow = evidence.windows.attempt_windows.find(
    (window) => window.attempt_index === attemptIndex
  );
  if (!attemptWindow) {
    return fail("missing attempt window for envelope's attempt", "windows.attempt_windows");
  }

  const nodeWindow = attemptWindow.node_windows.find((entry) => entry.node_id === nodeId);
  if (!nodeWindow) {
    return fail("missing node window for envelope.node.node_id", "windows.node_windows");
  }

  const started = parseTimestamp(runtime.started_at, "provenance.node_runtime.started_at");
  if (!started.ok) {
    return started;
  }
  const ended = parseTimestamp(runtime.ended_at, "provenance.node_runtime.ended_at");
  if (!ended.ok) {
    return ended;
  }

  const allowedStart = parseTimestamp(nodeWindow.allowed_start, "windows.allowed_start");
  if (!allowedStart.ok) {
    return allowedStart;
  }
  const allowedEnd = parseTimestamp(nodeWindow.allowed_end, "windows.allowed_end");
  if (!allowedEnd.ok) {
    return allowedEnd;
  }

  if (started.value.getTime() < allowedStart.value.getTime()) {
    return fail("envelope start precedes allowed window", "provenance.node_runtime.started_at");
  }
  if (ended.value.getTime() > allowedEnd.value.getTime()) {
    return fail("envelope ended after allowed window", "provenance.node_runtime.ended_at");
  }

  const executionRecord = evidence.node_executions.find(
    (entry) => entry.envelope_id === envelope.envelope_id
  );
  if (!executionRecord) {
    return fail("no node_execution recorded for envelope_id", "node_executions");
  }

  if (executionRecord.node_id !== nodeId) {
    return fail("node_execution.node_id mismatch", "node_executions.node_id");
  }
  if (executionRecord.attempt_index !== attemptIndex) {
    return fail("node_execution.attempt_index mismatch", "node_executions.attempt_index");
  }
  if (executionRecord.status !== envelope.outputs.status) {
    return fail("node_execution.status must mirror envelope.status", "node_executions.status");
  }

  const { envelope_hash } = finalizeNodeEnvelope(envelope);
  if (executionRecord.envelope_hash !== envelope_hash) {
    return fail("node_execution.hash does not match envelope hash", "node_executions.envelope_hash");
  }

  const ledgerHash = evidence.hashes.node_envelope_hashes.find(
    (entry) => entry.envelope_id === envelope.envelope_id
  );
  if (!ledgerHash) {
    return fail("ledger missing envelope hash entry", "hashes.node_envelope_hashes");
  }
  if (ledgerHash.hash !== envelope_hash) {
    return fail("ledger hash must match envelope hash", "hashes.node_envelope_hashes");
  }

  return success(undefined);
}
