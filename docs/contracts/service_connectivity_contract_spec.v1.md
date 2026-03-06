# Service Connectivity Contract Spec v1

Status: Draft v1
Scope: Forge:SMITH, Forge_Command, ForgeAgents, DataForge, NeuroForge, Rake, downstream products

## 1. Purpose
This contract defines connectivity correctness for Forge services:

`All connected participants either converge on shared truth, or surface explicit disagreement.`

Silence, stale state, and reachability-only checks are not treated as correctness.

## 2. Normative Terms
- MUST: mandatory behavior.
- MUST NOT: forbidden behavior.
- SHOULD: strong recommendation with documented exception.
- MAY: optional behavior.

## 3. Core Connectivity Invariants
1. Authority is explicit:
- A successful network call MUST NOT be treated as authority to act.
- Action authorization MUST be bound to a fresh authority artifact (for example `RunIntent.v1` + accepted state).

2. Connectivity and correctness are distinct:
- Health success MUST NOT imply execution readiness.
- Readiness MUST encode authority-path availability, not only transport reachability.

3. Divergence is first-class:
- If two observers disagree (stream/control/evidence), system MUST emit `state_divergence` with both views.
- Divergence MUST block governed continuation until resolved by contract, not heuristic UI assumptions.

4. Stream omission is failure:
- Missing events during an active run MUST be modeled as unknown state, not implicit success.
- Consumers MUST transition from `active` to `unknown` on stream ambiguity.

5. Recovery is deterministic:
- Restarted services MUST restore active state from durable authority records.
- In-memory caches MUST NOT become authoritative after restart.

## 4. Connectivity Classes
Each connection MUST declare class and semantics.

### 4.1 Control-Plane Connection
Used for authority, intent, cancel/abort, approval.

Required fields:
- `connection_id`
- `initiator`
- `receiver`
- `protocol`
- `authority_required` (bool)
- `failure_policy` (`fail_closed` | `degraded_readonly`)
- `max_staleness_ms`
- `truth_source`

Rules:
- Control-plane calls MUST be fail-closed for governed writes.
- Cancel/abort acknowledgments MUST be confirmed against authoritative run state before success is returned.

### 4.2 Data-Plane Connection
Used for execution, inference, ingestion.

Rules:
- Data-plane success MUST carry a causally linked control-plane authorization reference (`intent_id`, `run_id`, token binding).
- If data-plane continues while control-plane is unavailable, mode MUST downgrade to non-governed and emit explicit authority-loss state.

### 4.3 Observability Connection
Used for SSE, polling, telemetry, health.

Rules:
- Observability channels MUST be advisory only.
- Observability MUST NOT be used as sole source for authoritative state transitions.
- Event consumers MUST reconcile against authoritative status endpoints on reconnect.

### 4.4 Credential Connection
Used for vault/keyring/brokered secrets.

Rules:
- Reachability to credential service MUST NOT imply permission to resolve secrets.
- Credential resolution MUST include caller identity and policy decision in response metadata.

## 5. Connection Contract Record (CCR)
Every runtime connection MUST have a machine-readable CCR.

```json
{
  "connection_id": "forge_command.tauri->orchestrator.intent_get",
  "class": "control_plane",
  "initiator": "forge_command_tauri",
  "receiver": "orchestrator",
  "protocol": "http",
  "path": "/api/v1/intents/{intent_id}",
  "authority_required": true,
  "truth_source": "orchestrator.intent_store",
  "blocking_semantics": "blocking",
  "failure_policy": "fail_closed",
  "max_staleness_ms": 0,
  "degraded_behavior": "reject_governed_start",
  "divergence_event": "state_divergence",
  "contract_version": "1.0"
}
```

## 6. Authority Boundaries
1. Authority source precedence (highest to lowest):
- Durable control-plane state
- Durable execution ledger/index
- Stream/events
- UI local cache

2. Services MUST expose current authority epoch/version for state reads used by orchestrators.

3. Governed actions MUST include:
- `intent_id`
- accepted intent status proof
- run binding proof (`run_id` + token scope)

## 7. State Agreement Model
For each run, system MUST evaluate a 3-observer agreement tuple:
- `control_state`
- `execution_state`
- `evidence_state`

Agreement result:
- `agreed`
- `diverged_detected`
- `unknown_due_to_connectivity`

Governed progression rule:
- MUST proceed only on `agreed`.
- MUST halt on `diverged_detected` or `unknown_due_to_connectivity`.

## 8. Event/Stream Contract
1. Ordering:
- Streams MUST provide monotonic sequence per run.
- If monotonicity breaks, consumer MUST mark stream as non-authoritative and reconcile via control plane.

2. Reconnect:
- Reconnect MUST provide replay token (`Last-Event-ID` equivalent).
- Missing replay MUST produce `unknown_due_to_connectivity`.

3. Idempotency:
- Consumers MUST dedup by `(run_id, sequence, event_hash)`.

4. Omission handling:
- If heartbeat exceeded and control-plane terminal not confirmed, run state MUST be `unknown`, not `running`.

## 9. Partition Behavior Contract
During partial partitions, each service MUST choose exactly one partition mode:
- `fail_closed`
- `degraded_readonly`

Forbidden:
- `continue_write_without_authority`

Required partition declaration:
- reason
- impacted connections
- authority impact
- expiry/reevaluation timestamp

## 10. Downstream Product Rules
For AuthorForge, Leopold, Livy, VibeForge and other downstream consumers:

1. Upstream authority loss detection:
- MUST explicitly detect governance-control unreachability.

2. Safe halt behavior:
- Governed write actions MUST halt on upstream authority loss.

3. No autonomous governance bypass:
- Local fallback execution MAY run only in explicitly non-governed mode.
- UI/UX MUST label this mode as non-authoritative.

## 11. Connectivity Acceptance Gate (minimum)
A build/release is connectivity-compliant only if all pass:

1. Connection declarations:
- 100% runtime cross-service connections have CCR records.

2. Fail policy:
- 100% control-plane governed write paths are `fail_closed`.

3. Divergence surfacing:
- For every run path, disagreement between control/execution/evidence produces explicit divergence state.

4. Restart correctness:
- Active run and token authority state rehydrates deterministically from durable store.

5. Stream safety:
- Stream disconnect/reorder leads to `unknown` or `diverged_detected`, never silent continuation.

## 12. Current Gaps to Resolve for Compliance (Forge_Command-focused)
1. Event channel contract mismatch must be eliminated (`forge_run_event` vs `forge_run_events`).
2. Governed intent status contract must be unified (`pending` vs `accepted` expectations).
3. Health/readiness contract must separate reachability from authority readiness.
4. Orchestrator recovery contract must include full active authority state (sessions + tokens + status normalization).
5. Emergency brake must be wired as an invokable authoritative control-plane action, or removed from contract claims.

## 13. Versioning and Evolution
1. CCR and this spec use semantic contract versioning:
- patch: clarifications only
- minor: additive fields/rules
- major: incompatible authority or state semantics

2. Any change that alters fail policy, truth source precedence, or divergence behavior requires major version bump and migration plan.

## 14. Compliance Statement Template
```text
Service: <service_id>
Contract Version: 1.0
Connection Coverage: <n/n>
Governed Fail-Closed Coverage: <n/n>
Divergence Surfacing Coverage: <n/n>
Partition Mode(s): <mode list>
Known Exceptions: <none or explicit list>
Approved By: <owner>
Date: <ISO-8601>
```
