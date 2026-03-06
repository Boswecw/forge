import assert from "node:assert";
import { canonicalizeJson } from "../canonical_json.js";
import { sha256Prefixed } from "../hashes.js";
import {
  finalizeNodeEnvelope,
  validateNodeEnvelope,
  NodeEnvelope,
  ValidationResult,
} from "../node_envelope.js";
import {
  finalizeRunEvidence,
  validateRunEvidence,
  verifyEnvelopeAgainstEvidence,
  RunEvidence,
} from "../run_evidence.js";

type TestCase = {
  name: string;
  fn: () => void;
};

function expectValid<T>(result: ValidationResult<T>, label: string): void {
  if (!result.ok) {
    throw new Error(`${label} expected valid but failed: ${result.error.message}`);
  }
}

function expectInvalid<T>(result: ValidationResult<T>, label: string): void {
  if (result.ok) {
    throw new Error(`${label} expected invalid but succeeded`);
  }
}

function buildBaseEnvelope(): NodeEnvelope {
  return {
    envelope_version: "NodeEnvelope.v1",
    envelope_id: "env-test",
    node: {
      node_id: "memory_preflight",
    },
    context: {
      workflow_id: "forge-run/code-review",
      session_id: "session-123",
      run_id: "run-123",
      trace_id: "trace-123",
      repo: {
        repo_id: "forge-smithy",
        repo_sha: "abc123",
        branch: "main",
      },
      environment: {
        mode: "interactive",
        invoker: "cli",
      },
    },
    constraints: {
      constraint_version: "Doctrine.v3.2",
      tools_allowed: ["none"],
      expected_output_schema: {
        schema_id: "memory_packet.v1",
        schema_hash:
          "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      },
      token_budget: {
        total: 1000,
        priority_order: ["constraints", "memory", "stdin"],
        overrun_policy: "forbid",
      },
      stop_conditions: ["schema_violation"],
    },
    inputs: {
      stdin: {
        hash: "sha256:1111111111111111111111111111111111111111111111111111111111111111",
        schema_id: "stdin.v1",
      },
    },
    execution: {
      attempt: 1,
      max_retries: 2,
      parallel_group: "preflight",
      dependency_strategy: "wait_all",
      timeouts_ms: {
        soft: 500,
        hard: 2000,
      },
    },
    outputs: {
      status: "success",
      payload: {
        type: "memory_packet.v1",
        data: {
          result: "ok",
        },
      },
      messages: [{ level: "info", message: "ok" }],
    },
    provenance: {
      usage_stats: {
        input_tokens: 50,
        output_tokens: 50,
        total_tokens: 100,
        model_id: "google:gemini-1.5-pro",
      },
      input_hashes: {
        stdin: "sha256:2222222222222222222222222222222222222222222222222222222222222222",
      },
      schema_manifest: {
        output_schema_id: "memory_packet.v1",
        output_schema_hash:
          "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      },
      constraint_hash: "sha256:3333333333333333333333333333333333333333333333333333333333333333",
      node_runtime: {
        started_at: "2026-01-15T20:10:00Z",
        ended_at: "2026-01-15T20:10:01Z",
        latency_ms: 1000,
      },
      confidence_score: 0.87,
      confidence_scale: "0..1",
      confidence_source: "model",
      risk_flags: ["MEMORY_CONFLICT"],
    },
  };
}

function buildRunEvidence(envelope: NodeEnvelope): RunEvidence {
  const { envelope_hash } = finalizeNodeEnvelope(envelope);
  const raw: RunEvidence = {
    evidence_version: "RunEvidence.v1",
    trace_id: envelope.context.trace_id,
    run_id: envelope.context.run_id,
    session_id: envelope.context.session_id,
    workflow_id: envelope.context.workflow_id,
    created_at: "2026-01-15T20:10:05Z",
    runner: {
      service: "forgeagents",
      module: "script_runner",
      version: "1.0.0",
      host: {
        machine_id: "host-1",
        os: "linux",
        arch: "x86_64",
      },
      mode: "interactive",
    },
    inputs: {
      stdin_hash:
        "sha256:4444444444444444444444444444444444444444444444444444444444444444",
      stdin_normalized_hash:
        "sha256:5555555555555555555555555555555555555555555555555555555555555555",
      repo: {
        repo_id: envelope.context.repo.repo_id,
        repo_sha: envelope.context.repo.repo_sha,
        branch: envelope.context.repo.branch,
      },
      constraint_version: envelope.constraints.constraint_version,
      constraint_hash: envelope.provenance.constraint_hash,
    },
    plan: {
      nodes: [
        {
          node_id: envelope.node.node_id,
          parallel_group: envelope.execution.parallel_group,
          depends_on: [],
        },
      ],
      dependency_strategy_default: "fail_fast",
      max_retries_default: 1,
    },
    windows: {
      attempt_windows: [
        {
          attempt_index: envelope.execution.attempt,
          node_windows: [
            {
              node_id: envelope.node.node_id,
              allowed_start: "2026-01-15T20:09:59Z",
              allowed_end: "2026-01-15T20:10:05Z",
            },
          ],
        },
      ],
    },
    node_executions: [
      {
        attempt_index: envelope.execution.attempt,
        node_id: envelope.node.node_id,
        envelope_id: envelope.envelope_id,
        envelope_hash,
        status: envelope.outputs.status,
        started_at: envelope.provenance.node_runtime.started_at,
        ended_at: envelope.provenance.node_runtime.ended_at,
      },
    ],
    orchestration: {
      parallel_groups: [
        {
          name: "preflight",
          nodes: [envelope.node.node_id],
          dependency_strategy: "wait_all",
        },
      ],
      retries: [],
      skips: [],
    },
    result: {
      final_status: "pass",
      promotion_ready: false,
      confidence_floor: 0.8,
      highest_risk_flags: ["MEMORY_CONFLICT"],
      notes: "ok",
    },
    hashes: {
      run_evidence_hash:
        "sha256:0000000000000000000000000000000000000000000000000000000000000000",
      node_envelope_hashes: [
        {
          envelope_id: envelope.envelope_id,
          hash: envelope_hash,
        },
      ],
    },
  };

  return finalizeRunEvidence(raw).evidence;
}

const tests: TestCase[] = [
  {
    name: "base envelope validates",
    fn: () => {
      const envelope = buildBaseEnvelope();
      expectValid(validateNodeEnvelope(envelope), "base envelope");
    },
  },
  {
    name: "success with fault is rejected",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.outputs.fault = {
        code: "FAULT",
        retryable: false,
        detail: "faulty",
      };
      expectInvalid(validateNodeEnvelope(envelope), "success-with-fault");
    },
  },
  {
    name: "system_fault without fault is rejected",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.outputs.status = "system_fault";
      delete envelope.outputs.fault;
      expectInvalid(validateNodeEnvelope(envelope), "system_fault-fault");
    },
  },
  {
    name: "constraint_violation with retryable true is rejected",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.outputs.status = "constraint_violation";
      envelope.outputs.fault = {
        code: "SCHEMA",
        retryable: true,
        detail: "bad",
      };
      expectInvalid(validateNodeEnvelope(envelope), "constraint_violation-retryable");
    },
  },
  {
    name: "schema hash mismatch is rejected",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.provenance.schema_manifest.output_schema_hash =
        "sha256:9999999999999999999999999999999999999999999999999999999999999999";
      expectInvalid(validateNodeEnvelope(envelope), "schema-hash-mismatch");
    },
  },
  {
    name: "retry_reason missing when attempt > 1 is rejected",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.execution.attempt = 2;
      envelope.provenance.retry_reason = undefined;
      expectInvalid(validateNodeEnvelope(envelope), "retry-reason");
    },
  },
  {
    name: "token overrun in forbid mode blocks success",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.constraints.token_budget.total = 10;
      envelope.provenance.usage_stats.total_tokens = 100;
      expectInvalid(validateNodeEnvelope(envelope), "token-overrun");
    },
  },
  {
    name: "replay window inside allowed window passes",
    fn: () => {
      const envelope = buildBaseEnvelope();
      const evidence = buildRunEvidence(envelope);
      expectValid(validateRunEvidence(evidence), "run evidence base");
      const verification = verifyEnvelopeAgainstEvidence(envelope, evidence);
      expectValid(verification, "window pass");
    },
  },
  {
    name: "replay window outside allowed window fails",
    fn: () => {
      const envelope = buildBaseEnvelope();
      envelope.provenance.node_runtime.started_at = "2026-01-15T20:09:50Z";
      envelope.provenance.node_runtime.ended_at = "2026-01-15T20:09:51Z";
      envelope.provenance.node_runtime.latency_ms = 1000;
      const evidence = buildRunEvidence(envelope);
      const verification = verifyEnvelopeAgainstEvidence(envelope, evidence);
      expectInvalid(verification, "window outside");
    },
  },
  {
    name: "missing node window fails",
    fn: () => {
      const envelope = buildBaseEnvelope();
      let evidence = buildRunEvidence(envelope);
      evidence.windows.attempt_windows[0].node_windows = [];
      evidence = finalizeRunEvidence(evidence).evidence;
      expectInvalid(verifyEnvelopeAgainstEvidence(envelope, evidence), "missing node window");
    },
  },
  {
    name: "hash determinism same object",
    fn: () => {
      const data = { a: 1, b: { c: 2 } };
      const hash1 = sha256Prefixed(canonicalizeJson(data));
      assert.strictEqual(hash1, sha256Prefixed(canonicalizeJson(data)));
    },
  },
  {
    name: "hash determinism ignores key order",
    fn: () => {
      const left = { b: 1, a: 2 };
      const right = { a: 2, b: 1 };
      assert.strictEqual(
        sha256Prefixed(canonicalizeJson(left)),
        sha256Prefixed(canonicalizeJson(right))
      );
    },
  },
];

async function runTests(): Promise<void> {
  for (const test of tests) {
    try {
      test.fn();
      console.log(`[PASS] ${test.name}`);
    } catch (error) {
      console.error(`[FAIL] ${test.name}`);
      console.error(error);
      throw error;
    }
  }
}

runTests()
  .then(() => {
    console.log("All contract tests passed.");
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
