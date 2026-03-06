# §8 — API Layer

The four resident HTTP services use FastAPI with JSON request/response bodies. All write endpoints require authentication. Health probes are unauthenticated. Forge Eval is outside this API surface: it is a local CLI evaluator with no resident HTTP API in the current Pack J runtime.

Router and endpoint totals in this chapter are audit-derived snapshot values. Paths, auth semantics, and HTTP-versus-CLI boundaries are canonical.

---

## Authentication Matrix

| Auth Type | Used By | Scope |
|-----------|---------|-------|
| JWT Bearer token | All services | User-facing endpoints, admin operations |
| API Key header | DF, Rake | Service-to-service calls |
| run_token | DF (BugCheck) | Finding writes, enrichment writes, progress events |
| user_token | DF (BugCheck) | Lifecycle transitions (triage, approve, dismiss) |
| No auth | All | `/health`, `/ready`, `/version`, `/metrics` |

---

## Health & Observability (All Services)

Every service exposes these standard endpoints:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | None | Liveness probe — 200 if process is alive (NeuroForge also exposes `patch_tasks_enabled`) |
| GET | `/ready` | None | Readiness probe — checks dependency connectivity (NeuroForge also exposes `patch_tasks_enabled`) |
| GET | `/version` | None | Service version, commit, build metadata |
| GET | `/metrics` | None | Prometheus metrics (DF, FA) |

NeuroForge additionally exposes:
- `GET /degraded` — Current degraded mode and active degradation reasons

## Forge Eval CLI Surface (No HTTP API)

Forge Eval does not publish HTTP endpoints in the ecosystem runtime. Its current operator surface is local CLI invocation against a target repository checkout.

| Command | Required Inputs | Output |
|---------|------------------|--------|
| `forge-eval run` | `--repo`, `--base`, `--head`, `--out` | Deterministic artifact set for the enabled stage chain |
| `forge-eval validate` | `--artifacts` | Schema validation result for an artifact directory |

Optional runtime config is supplied with `--config` (`.json`, `.yaml`, `.yml`). This boundary is intentional: Forge Eval evaluates sibling repositories and emits local artifacts, but it is not a resident network service.

---

## NeuroForge API (Port 8000)

### Core Inference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/inference/run` | Primary NeuroForge 5-stage inference endpoint (supports patch-task governance contract) |
| POST | `/api/v1/inference` | Single inference through 5-stage pipeline |
| GET | `/api/v1/inference/{id}` | Get inference status/result |
| GET | `/api/v1/inference/history` | Filtered inference history |
| POST | `/api/v1/inference/batch` | Batch inference (async, returns batch_id) |

### MAID Consensus

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/maid/validate` | Multi-model consensus validation |
| GET | `/api/v1/maid/status/{id}` | Validation status |
| POST | `/api/v1/maid/estimate-cost` | Cost estimation |

### RAG & Context

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/rag/query` | Fetch RAG context chunks from DataForge |

### Research, Analytics, ML

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/research/sessions` | Create research session |
| POST | `/api/v1/orchestration/execute-planning` | MAPO execution |
| POST | `/api/v1/evaluation/submit` | Quality evaluation |
| GET | `/api/v1/analytics/dashboard` | Aggregated performance metrics |
| GET | `/api/v1/models/list` | Available models across providers |
| GET | `/api/v1/models/performance` | Per-model metrics |

### AuthorForge Proxy

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/authorforge/suggest` | RAG-grounded literary suggestions |
| POST | `/api/v1/authorforge/style-analysis` | 4-dimension style analysis |
| POST | `/api/v1/authorforge/analyze-consistency` | Contradiction detection |
| POST | `/api/v1/authorforge/extract-entities` | Entity extraction |

**Failure contract:** All AuthorForge endpoints return empty arrays on LLM failure — never 5xx.

### Psychology & Team Learning

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/infer` | Psychology profile inference (9 frameworks) |
| POST | `/api/v1/team-learning/aggregate/{team_id}` | Team learning aggregation |
| GET | `/api/v1/team-learning/insights/{team_id}` | Team learning insights |

---

## DataForge API (Port 8001)

**Current audited snapshot: 33 router registrations supporting 80+ endpoints.** Organized by domain.

### Search

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/search` | Hybrid search (semantic + BM25 + RRF) |
| GET | `/api/search/stats` | Search usage statistics |

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/login` | JWT login |
| POST | `/auth/logout` | Session invalidation |
| GET | `/auth/oauth/{provider}` | OAuth2 flow (Google, GitHub, Microsoft) |
| POST | `/auth/mfa/setup` | Initialize TOTP 2FA |
| POST | `/auth/mfa/verify` | Verify TOTP code |

### Document Management

| Method | Path | Description |
|--------|------|-------------|
| POST | `/admin/documents` | Create document + auto-chunk + embed |
| GET | `/admin/documents` | List documents (paginated, filterable) |
| PATCH | `/admin/documents/{id}` | Update document + re-chunk |
| DELETE | `/admin/documents/{id}` | Delete + cascade chunks |

### Service Integration Endpoints

| Prefix | Consumer | Key Operations |
|--------|----------|---------------|
| `/api/neuroforge` | NeuroForge | Run logging, inference records, performance metrics, context retrieval |
| `/api/vibeforge` | VibeForge | Projects, sessions, stack outcomes, code analysis |
| `/api/projects` | AuthorForge | Books, chapters, scenes, characters, arcs, manuscripts |
| `/api/bugcheck` | BugCheck | Runs, findings, lifecycle transitions, enrichments |
| `/api/agents-registry` | ForgeAgents | Agent registration and configuration |
| `/forge-runs` | ForgeCommand | Execution index (fast status lookups), evidence storage |
| `/api/v1/smithy` | SMITH | Planning sessions, portfolio projects, evaluations |
| `/api/teams` | VibeForge | Team CRUD, membership, insights |

### BugCheck API (via DataForge)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/bugcheck/runs` | admin token | Create run record (ForgeCommand only) |
| POST | `/api/bugcheck/runs/{id}/findings` | run_token | Ingest finding |
| POST | `/api/bugcheck/findings/{id}/lifecycle` | user_token | Transition lifecycle state |
| POST | `/api/bugcheck/findings/{id}/enrichments` | run_token | Store enrichment |
| POST | `/api/bugcheck/runs/{id}/finalize` | admin token | Finalize run (immutable after) |

### Infrastructure

| Prefix | Purpose |
|--------|---------|
| `/api/events` | Append-only HMAC-signed audit log |
| `/api/tracing` | OpenTelemetry span ingestion |
| `/secrets` | LLM API key vault (synced from ForgeCommand) |
| `/cache` | Redis cache operations |
| `/dlq` | Dead letter queue inspection + replay |
| `/admin-ui` | Browser-based admin interface |

---

## Rake API (Port 8002)

### Ingestion Jobs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/jobs` | Submit ingestion job (returns 202) |
| GET | `/api/v1/jobs/{id}` | Poll job status |
| GET | `/api/v1/jobs` | List jobs (paginated, filterable) |
| DELETE | `/api/v1/jobs/{id}` | Cancel pending job |

**Source types:** `file_upload`, `url_scrape`, `sec_edgar`, `api_fetch`, `database_query`

### Research Missions

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/missions` | Create research mission |
| GET | `/api/v1/missions/{id}` | Get mission status |
| POST | `/api/v1/missions/{id}/approve` | Approve strategy |
| POST | `/api/v1/missions/{id}/cancel` | Cancel mission |
| GET | `/api/v1/missions/{id}/pipeline-status` | Ingestion progress |
| GET | `/api/v1/missions/{id}/evidence-bundle` | Evidence bundle |

### Discovery

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/discover` | Web discovery job (search without full pipeline) |
| GET | `/api/v1/discover/{id}` | Discovery results |

---

## ForgeAgents API (Port 8010)

### Agent Management

| Method | Path | Description |
|--------|------|-------------|
| POST | `/agents` | Create agent |
| GET | `/agents` | List agents |
| GET | `/agents/{id}` | Get agent details |
| PUT | `/agents/{id}` | Update agent config |
| DELETE | `/agents/{id}` | Delete agent (409 if executing) |

### Execution

| Method | Path | Description |
|--------|------|-------------|
| POST | `/agents/{id}/execute` | Start async execution (returns 202) |
| GET | `/agents/{id}/executions/{exec_id}` | Poll execution status |
| GET | `/agents/{id}/executions/{exec_id}/result` | Fetch result (409 if not complete) |
| POST | `/agents/{id}/executions/{exec_id}/cancel` | Cancel execution |
| WS | `/ws/agents/{id}/execute` | Real-time execution streaming |

### Memory

| Method | Path | Description |
|--------|------|-------------|
| POST | `/agents/{id}/memory` | Insert memory entry |
| GET | `/agents/{id}/memory` | Query memory (supports semantic search) |
| DELETE | `/agents/{id}/memory` | Clear memory |

### BugCheck

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/bugcheck/run-service` | Start BugCheck run against a service |
| GET | `/api/bugcheck/checks` | List available checks |
| GET | `/api/bugcheck/runs` | List BugCheck runs |

### Sentinel (Health Monitoring + Healing)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/sentinel/sweep` | Trigger light or deep health sweep |
| GET | `/api/v1/sentinel/sweep/{id}` | Get sweep results by ID |
| GET | `/api/v1/sentinel/sweeps` | List recent sweeps (filterable by mode, paginated) |
| POST | `/api/v1/sentinel/heal` | Trigger healing playbook (cache_flush, breaker_reset, job_retry) |
| GET | `/api/v1/sentinel/status` | Current Sentinel status (last sweep, 24h counts) |

### Tools, Policies, Skills

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tools` | List tools with metadata |
| POST | `/policies/evaluate` | Dry-run policy evaluation |
| GET | `/api/v1/skills` | List skills catalog |
| POST | `/api/v1/approvals/request` | Request human approval |

### Forge-Run (DAG Execution)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/forge-run` | Submit DAG execution plan |
| GET | `/forge-run/events/{id}` | SSE stream of execution events |

---

## Cross-Service API Call Map

Which services call which:

| Caller | Target | Endpoint(s) | Purpose |
|--------|--------|-------------|---------|
| NF | DF | `POST /context/fetch` | RAG context retrieval |
| NF | DF | `POST /api/neuroforge/inferences` | Provenance write |
| FA | DF | `/api/bugcheck/*` | Finding persistence |
| FA | DF | `/api/v1/sentinel/*` | Sweep + healing event persistence |
| FA | NF | `POST /api/v1/maid/validate` | MAID consensus |
| FA | Rake | Job submission APIs | Async task execution |
| Rake | DF | DataForge REST API | Document storage |
| Rake | NF | Strategy/curation endpoints | Research mission AI |

---

## Error Response Convention

All services use a consistent error envelope:

```json
{
  "detail": "Human-readable error message",
  "error_code": "SERVICE_ERROR_CODE"
}
```

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Malformed input |
| 401 | Unauthorized | Missing/invalid JWT |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | State machine violation, run finalized, agent busy |
| 422 | Unprocessable | Valid JSON, invalid values (Pydantic) |
| 429 | Too Many Requests | Rate limit exceeded |
| 503 | Unavailable | Critical dependency down |

---

*For per-service API deep dives, see each service's own `doc/system/` API layer chapter. For backend internals, see §9. For ecosystem integration, see §10.*
