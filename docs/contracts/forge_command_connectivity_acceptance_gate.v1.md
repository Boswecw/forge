# Forge_Command Connectivity Acceptance Gate v1

Status: Active Draft
Scope: `forge_command` connectivity contracts defined in `docs/contracts/forge_command_connectivity_ccr.v1.json`
Contract Basis: `docs/contracts/service_connectivity_contract_spec.v1.md`

## 1. Gate Outcome Semantics
- `PASS`: Requirement is implemented and evidenced.
- `FAIL`: Requirement is violated by current behavior.
- `BLOCKED`: Requirement cannot be verified from available implementation evidence.

Release rule:
- Governed release MUST be blocked if any critical gate item is `FAIL`.

## 2. Gate Criteria

| Gate ID | Requirement | Critical | Evidence Required |
|---|---|---|---|
| G1 | 100% runtime cross-service connections have CCR records | Yes | CCR inventory + command registry + client call graph |
| G2 | All governed control-plane write paths are `fail_closed` | Yes | Code path proof for reject-on-failure behavior |
| G3 | Divergence between control/execution/evidence is explicitly surfaced | Yes | Event/state emission proof + API/UI exposure |
| G4 | Every connection declares and enforces `max_staleness_ms` behavior | Yes | Timeout + stale-state transition tests |
| G5 | Restart recovery restores authoritative active state deterministically | Yes | Rehydrate tests for runs, tokens, sessions |
| G6 | Health/readiness separation: reachability != authority readiness | Yes | Distinct readiness contract + enforcement tests |
| G7 | Stream safety: disconnect/reorder causes `unknown` or divergence, not silent continuation | Yes | SSE reconnect/order tests + UI contract tests |
| G8 | Partition mode is explicit (`fail_closed` or `degraded_readonly`) per critical path | Yes | Partition policy mapping per connection |
| G9 | Credential connectivity does not imply authorization to resolve secrets | Yes | Caller-bound credential policy tests |
| G10 | Emergency halt path is invokable and contract-bound | Yes | invoke wiring + halt ack contract tests |

## 3. Current Gate Assessment (Forge_Command)

| Gate ID | Result | Rationale |
|---|---|---|
| G1 | PASS | CCR inventory created with explicit records in `forge_command_connectivity_ccr.v1.json`. |
| G2 | FAIL | Governed intent contract semantics are split (`pending` expected in Tauri vs `accepted` enforcement in orchestrator run binding). |
| G3 | FAIL | Divergence signaling exists in backend heuristics, but stream event channel mismatch prevents reliable consumer surfacing. |
| G4 | FAIL | Staleness is declared but not consistently enforced as authoritative state transition across all critical paths. |
| G5 | FAIL | Recovery gaps remain for full active authority state (not all tokens/sessions are restored consistently). |
| G6 | FAIL | Health checks are reachability-centric and can be interpreted as readiness confidence. |
| G7 | FAIL | Stream contract mismatch plus ordering assumptions can produce silent omission at consumer side. |
| G8 | FAIL | Partition behavior is not uniformly encoded/enforced as explicit mode contract for all governed paths. |
| G9 | PASS | Localhost/internal-caller constraints exist for orchestrator vault resolve; credential flows are caller-guarded at API boundary. |
| G10 | FAIL | Emergency brake command exists but is not currently wired into invoke handler path. |

## 4. CCR Traceability Matrix

| Connection ID | Gate IDs in Scope | Current Status |
|---|---|---|
| forge_command.tauri->orchestrator.intent_register | G1 G2 G8 | Implemented |
| forge_command.tauri->orchestrator.intent_get | G1 G2 G6 | Implemented with semantic drift |
| forge_command.tauri->orchestrator.intent_accept | G1 G2 G5 | Implemented |
| forge_command.tauri->orchestrator.pipeline_update_state | G1 G5 | Implemented with persistence gap |
| forge_command.tauri->forgeagents.run_start | G1 G2 G8 | Implemented |
| forge_command.tauri->forgeagents.run_cancel | G1 G2 G3 | Implemented with weak confirmation |
| forge_command.tauri->forgeagents.run_status_verify | G1 G3 G4 | Implemented |
| forge_command.tauri->forgeagents.sse_events | G1 G3 G4 G7 | Implemented with event contract drift |
| forge_command.tauri->dataforge.run_history | G1 G4 G8 | Implemented |
| forge_command.tauri->dataforge.run_detail | G1 G4 G8 | Implemented |
| forge_command.tauri->dataforge.run_evidence | G1 G3 G4 | Implemented |
| forge_command.tauri->dataforge.artifact_manifest | G1 G3 G4 | Implemented |
| forge_command.tauri->ecosystem.health_checks | G1 G6 | Implemented with authority gap |
| forge_command.tauri->orchestrator.process_management | G1 G5 G8 | Implemented |
| orchestrator.api_keys->vault_keyring | G1 G9 | Implemented |
| orchestrator.api_keys->dataforge.secrets_sync | G1 G8 G9 | Implemented |
| forge_command.tauri->localdb.api_keys | G1 G9 | Implemented with crypto compatibility risk |
| forge_command.tauri->frontend.run_events | G1 G3 G7 | Implemented with subscription mismatch |
| forge_command.tauri->ecosystem.emergency_brake | G1 G2 G8 G10 | Declared not wired |

## 5. Minimum Evidence Bundle Required for Gate Promotion

1. Contract conformance tests
- Control-plane fail-closed tests for governed write paths.
- Intent status semantic alignment tests across Tauri and orchestrator.

2. Stream integrity tests
- Event-name contract test (backend emit channel vs frontend subscription).
- Reconnect/reorder/omission tests proving transition to `unknown` or divergence.

3. Recovery tests
- Restart tests proving deterministic reconstruction of active runs, tokens, and sessions.

4. Partition behavior tests
- Per-critical-connection proof of explicit partition mode and behavior.

5. Halt authority tests
- End-to-end invoke path and halt acknowledgment proof for emergency control.

## 6. Gate Verdict (Current)
- Connectivity Acceptance Gate v1: `FAIL`
- Blocking reasons: `G2`, `G3`, `G4`, `G5`, `G6`, `G7`, `G8`, `G10`

A governed release should remain blocked until all critical failing gates are resolved and evidenced.
