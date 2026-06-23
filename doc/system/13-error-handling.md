# §13 — Error Handling

## Ecosystem-Wide Philosophy

Forge follows three inviolable error handling principles:

1. **Fail fast.** Ambiguous states are not tolerated. Invariant violations cause immediate system faults.
2. **Degrade explicitly.** When dependencies are unavailable, the system continues with reduced functionality but annotates all affected outputs with a degradation flag.
3. **No silent fallbacks.** Every degradation is declared, logged, and communicated to callers.

---

## NeuroForge — 5 Degraded Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **FULL** | All systems operational | Full pipeline with RAG + evaluation |
| **CACHE_ONLY** | DataForge unavailable | SQLite fallback cache for context; no live RAG |
| **MODEL_ONLY** | DataForge + cache unavailable | LLM inference without context |
| **DEGRADED_NO_RAG** | RAG subsystem failure | Pipeline runs without context enrichment |
| **OFFLINE** | All LLM providers unavailable | Returns error with explicit offline status |

The current mode is declared in every inference response via the `degraded_mode` field and exposed at `GET /degraded`.

### NeuroForge Error Response Envelope

```json
{
  "detail": "Human-readable error message",
  "error_code": "NEUROFORGE_ERROR_CODE",
  "degraded_mode": "FULL | CACHE_ONLY | MODEL_ONLY | DEGRADED_NO_RAG | OFFLINE",
  "recoverable": true
}
```

### NeuroForge Patch-Task Contract Failures

Patch-task governance failures use a stricter envelope for machine routing:

```json
{
  "error": "HTTP 422",
  "category": "PATCH_CONTRACT",
  "error_code": "PATCH_TARGETS_REF_NOT_FOUND",
  "detail": {
    "error": "PATCH_TASK_CONTRACT_ERROR",
    "category": "PATCH_CONTRACT",
    "error_code": "PATCH_TARGETS_REF_NOT_FOUND",
    "detail": "/abs/path/to/patch_targets.json",
    "recoverable": false
  },
  "recoverable": false
}
```

Operational notes:
- `patch_tasks_enabled` is exposed on `GET /health`, `GET /health/ready`, and `GET /ready`.
- It is `true` only when at least one trusted patch workspace root is configured and valid.
- Current limitation: request-validation `422` responses generated before patch-contract guards
  may not yet carry `category: PATCH_CONTRACT`.

### Circuit Breaker Pattern

`context_builder_fixed.py` implements a circuit breaker for DataForge calls:
- Trips after repeated failures (configurable threshold)
- Half-open state: periodic health probes
- Recovery: auto-recover when DataForge responds

### LLM Provider Fallback

```
Provider failure → Fallback chain: PREMIUM → STANDARD → FAST
Champion unavailable → Next model in tier by EMA score
All providers in tier fail → Drop to next tier
All tiers exhausted → OFFLINE mode
```

---

## DataForge — Lifecycle & Access Control Enforcement

### State Machine Enforcement

All lifecycle transitions are enforced at the API level. Invalid transitions return **409 Conflict**.

**BugCheck Finding Lifecycle:**
```
NEW → TRIAGED → FIX_PROPOSED → APPROVED → APPLIED → VERIFIED → CLOSED
  ↘ DISMISSED (requires reason + scope + expiration)
```

**Run Immutability:**
After a run is FINALIZED, new findings are rejected with 409. This is enforced at the database layer.

### Access Control Violations

| Violation | Response | Side Effect |
|-----------|----------|-------------|
| BugCheck writes lifecycle transition | 403 Forbidden | Security event logged |
| VibeForge writes finding | 403 Forbidden | Security event logged |
| Invalid run_token scope | 403 Forbidden | Token nonce burned |
| Expired run_token | 401 Unauthorized | — |
| Writing to finalized run | 409 Conflict | — |

### Exception Hierarchy

```python
DataForgeError (base)
├── DataForgeUnavailableError     # Service unreachable
├── InvalidStateTransitionError   # Lifecycle violation → 409
├── UnauthorizedWriteError        # Access control violation → 403
├── DuplicateFindingError         # Fingerprint collision → 409
└── ValidationError               # Schema violation → 422
```

### Resilience

| Layer | Strategy | Recovery |
|-------|----------|----------|
| PostgreSQL | Primary-replica + automated failover | < 30s |
| Redis | Sentinel-managed failover | < 10s |
| API | Load balancer + health checks + graceful shutdown | < 5s |
| Async tasks | Celery + DLQ + exponential backoff | 3 retries, 60s max |

---

## ForgeAgents — Explicit Degradation

### Exception Hierarchy

```python
ForgeAgentsError (base)
├── AgentError
│   ├── AgentNotFoundError        # 404
│   ├── AgentBusyError            # 409
│   └── ExecutionTimeoutError     # 408
├── PolicyError
│   ├── PolicyViolationError      # 403
│   └── QuotaExceededError        # 429
├── ServiceError
│   ├── DataForgeUnavailableError # 503 (fatal for runs)
│   ├── NeuroForgeUnavailableError # Degraded (non-fatal)
│   ├── RakeUnavailableError      # Degraded (non-fatal)
│   └── ServiceTimeoutError       # 504
├── BugCheckError
│   ├── InvalidStateTransitionError # 409
│   ├── RunTokenExpiredError      # 401
│   └── RunFinalizedError         # 409
└── ToolError
    ├── ToolNotFoundError         # 404
    ├── ToolExecutionError        # 500
    └── ToolPolicyDeniedError     # 403
```

### Dependency Degradation

| Dependency | On Failure | Recovery |
|-----------|-----------|---------|
| DataForge (REQUIRED) | Run does not start; `/ready` returns 503 | Startup health check retries |
| NeuroForge | Direct LLM API fallback; memory without embeddings; flag `degraded_enrichment` | Auto-recover on next call |
| Rake | Synchronous in-process execution; flag `degraded_mode: sync_fallback` | Auto-recover on next call |
| ForgeCommand | Standalone mode (no desktop integration, no approval routing) | Operates independently |

### BugCheck Degradation

| Condition | Behavior |
|-----------|----------|
| XAI unavailable | Proceed MAID-only, flag as "degraded enrichment" |
| MAID unavailable | Report findings without fix proposals, flag as "analysis pending" |
| Both unavailable | Complete with raw findings only, alert operator |
| XAI call limit reached (50) | Remaining findings skip XAI enrichment |
| MAID proposal limit reached (20) | Remaining findings skip fix generation |

---

## Rake — Pipeline Error Handling

### Stage Failure

| Stage | On Failure | Recovery |
|-------|-----------|----------|
| FETCH | Job marked FAILED; error logged with source details | Retry via `POST /api/v1/jobs` |
| CLEAN | Documents that fail cleaning are skipped; others proceed | Partial success logged |
| CHUNK | Fallback to token-based chunking if semantic fails | Automatic |
| EMBED | Retry with exponential backoff (3 attempts) | API key rotation if provider fails |
| STORE | DataForge unavailable → job FAILED | Must restart after DataForge recovery |

### Mission Error Handling

| Condition | Behavior |
|-----------|----------|
| NeuroForge unavailable (strategy) | Mission stays in CREATED; cannot progress to STRATEGIZING |
| Discovery finds no sources | Mission moves to COMPLETED with empty results |
| Cost cap reached | Mission halted; state preserved; can be resumed with higher cap |
| Individual source fails ingestion | Source marked FAILED; other sources continue |

### Retry Configuration

```python
RETRY_ATTEMPTS = 3        # Max retries
RETRY_DELAY = 1.0         # Base delay (seconds)
RETRY_BACKOFF = 2.0       # Multiplier per attempt
# Delays: 1s → 2s → 4s
```

---

## Cross-Service Error Conventions

### HTTP Status Codes

| Code | Meaning | Used Across |
|------|---------|-------------|
| 400 | Bad Request — malformed input | All |
| 401 | Unauthorized — missing/invalid JWT | All |
| 403 | Forbidden — insufficient permissions | All |
| 404 | Not Found — resource missing | All |
| 409 | Conflict — state machine violation, run finalized, agent busy | DF, FA |
| 422 | Unprocessable — valid JSON, invalid values (Pydantic) | All |
| 429 | Too Many Requests — rate limit exceeded | All |
| 503 | Unavailable — critical dependency down | All |

### Structured Logging

All services use structured logging with mandatory context fields:

```python
import structlog
logger = structlog.get_logger()

logger.info(
    "finding_created",
    run_id=run_id,
    finding_id=finding_id,
    severity=severity,
    service="forgeagents",
)
```

**Required fields:** `run_id` (when inside a run), `service` (originating service), `event` (what happened).

---

## Per-Service Retry Contracts

### NeuroForge

| Parameter | Value |
|-----------|-------|
| Strategy | Exponential backoff |
| Base delay | 1 second |
| Progression | 1s → 2s → 4s |
| Max retries per model | 3 |
| Retry triggers | 5xx responses, network timeouts |
| Non-retryable | 4xx responses (invalid input, auth failures) |
| Circuit breaker | Trips after repeated DataForge failures; half-open probes for recovery |

### DataForge

| Parameter | Value |
|-----------|-------|
| Async strategy | Celery task retries |
| Max retries | 3 |
| Max backoff | 60 seconds |
| Dead Letter Queue | Failed tasks moved to DLQ after 3 attempts |
| DB failover | Primary-replica with < 30s automated failover |
| Redis failover | Sentinel-managed with < 10s failover |

**Dead Letter Queue (DLQ) behavior:**
1. **Write:** Failed Celery tasks are moved to DLQ after exhausting retries
2. **Inspect:** Admin API exposes DLQ contents for triage
3. **Replay:** Individual DLQ items can be replayed via admin endpoint
4. **Delete:** Admin-only operation — requires explicit confirmation

### ForgeAgents

| Parameter | Value |
|-----------|-------|
| Library | `tenacity` |
| Max retries | 3 |
| Timeout | 30 seconds per attempt |
| Strategy | Exponential backoff |
| DataForge calls | Startup health check retries; run does not start if unavailable |

### Rake

| Parameter | Value |
|-----------|-------|
| Max attempts | 3 |
| Base delay | 1 second |
| Multiplier | 2.0 |
| Progression | 1s → 2s → 4s |
| Retry scope | EMBED stage only (API failures) |
| Non-retryable | STORE stage failures (DataForge must be healthy to start) |

---

## UI Error Rendering (forge-smithy)

forge-smithy surfaces backend degradation through three visual mechanisms:

### System Rail Priority Banners

The System Rail renders priority-ordered banners based on system state:

| Priority | Condition | Banner Style | Action |
|----------|-----------|-------------|--------|
| **P0** | Orphan run detected | `--status-danger` background | Immediate attention required |
| **P1** | Session locked | `--status-warning` background | Unlock or wait |
| **P2** | Service offline | `--status-neutral` background | Degraded mode indicator |

Banners stack vertically. Higher priority (lower number) renders first.

### ServiceHealthPanel (Circuit Breaker Display)

The `ServiceHealthPanel` component in the System Rail shows per-service circuit breaker status:

| Service State | Visual | Token |
|---------------|--------|-------|
| **Closed** (healthy) | Green indicator | `--status-success` |
| **Half-Open** (probing) | Amber indicator | `--status-warning` |
| **Open** (tripped) | Red indicator | `--status-danger` |

Source: `serviceHealthStore` — tracks `ServiceId` enum (DataForge, Rake, ForgeAgents, ForgeCommand, Ollama).

### Status Footer

The persistent 28px footer displays governance metrics and pipeline state. When services degrade, the footer reflects the current operational mode.

### Consumer Error Handling Contract

What each HTTP status means for forge-smithy callers:

| Status | Meaning | UI Behavior |
|--------|---------|-------------|
| 200-299 | Success | Render response normally |
| 400 | Bad Request | Show validation errors inline |
| 401 | Unauthorized | Redirect to auth flow |
| 403 | Forbidden | Show "insufficient permissions" banner |
| 404 | Not Found | Show "resource not found" state |
| 409 | Conflict | Show state machine violation message (lifecycle, finalized run) |
| 422 | Unprocessable | Show field-level Pydantic validation errors |
| 429 | Rate Limited | Show "too many requests" with retry-after |
| 503 | Service Unavailable | Trigger System Rail P2 banner; degrade gracefully |

---

*For per-service error handling details, see each service's own `doc/system/` error handling chapter. For circuit breaker implementation, see §9. For design tokens used in error states, see §6.*
