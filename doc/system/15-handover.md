# §15 — Handover: Critical Constraints, Known Issues & Maintenance Guide

This section is the first thing a new developer or AI agent working on the Forge ecosystem should read after the overview. It contains facts that, if ignored, will cause subtle bugs, data corruption, or security violations.

Architectural invariants in this chapter are canonical. Operational counts, implementation phase tallies, and other measured status lines are audit-derived snapshot values unless they are explicitly framed as invariants.

---

## Ecosystem-Wide Invariants — Non-Negotiable

These are architectural invariants, not guidelines. Violating any of them is a **system fault**.

### 1. DataForge Is the Only Source of Truth

No service maintains authoritative state outside DataForge. There is no "eventually consistent" model. There is no "local cache that syncs later." If DataForge is unavailable, the operation does not happen.

```
WRONG: Service stores data locally, syncs to DataForge later
RIGHT: Service attempts DataForge write; if it fails, the operation fails
```

**NeuroForge** `neuroforge.db` and `neuroforge_fallback.db` are operational caches, NOT truth stores.
**Rake** runs on Render's ephemeral filesystem — all state is PostgreSQL JSONB, never local files.
**ForgeAgents** holds no durable state. Agent registry is in-memory only, reconstituted from DataForge on restart.

### 2. API Boundary Enforcement

Every service has strictly defined write permissions. Violations are treated as **security events**, not user errors.

| Actor | Authorized Writes | Prohibited |
|-------|------------------|------------|
| ForgeCommand (admin token) | Run records, lifecycle transitions, finalization, API keys, tokens | Findings, enrichments |
| BugCheck Agent (run_token) | Findings, progress events, check telemetry | Lifecycle transitions, run records |
| XAI/MAID (run_token) | Enrichment artifacts | Findings, lifecycle, run records |
| VibeForge (user_token) | User decisions (lifecycle transitions) | Findings, run records, enrichments |
| NeuroForge (API key) | Inference records, performance metrics | BugCheck data |
| AuthorForge (API key) | Project content hierarchy | BugCheck data, run records |
| SMITH (API key) | Planning sessions, portfolio, governance events | BugCheck findings |

**BugCheck may NEVER write lifecycle transitions. VibeForge may NEVER write findings.**

### 3. Lifecycle Transitions Are One-Way

Terminal states (`CLOSED`, `DISMISSED`, `FINALIZED`, `COMPLETED`, `FAILED`, `CANCELLED`) are irreversible. The only "reset" is to create a new run or mission — not to modify the state of existing ones.

### 4. Audit Log Is Append-Only Forever

DataForge's audit log is HMAC-SHA256 signed and append-only. There is no admin endpoint to delete entries. No SQL DELETE on the events table. Code attempting to DELETE from the audit log is a security incident.

### 5. No Silent Fallbacks

Every degradation across every service must be:
- **Logged** at `warning` or higher
- **Reflected** in responses (`degraded_mode`, `degraded_enrichment`, etc.)
- **Visible** to callers

Silent fallbacks that hide degradation are bugs.

### 6. Policy Evaluation Is Mandatory (ForgeAgents)

The tool router always calls the policy engine (Safety → Domain → Resource) before every tool invocation. No "fast path" bypasses. This is non-configurable.

### 7. Forge Eval Is a Standalone Subsystem

Forge Eval lives in `/home/charlie/Forge/ecosystem/forge-eval` and must be documented and operated as its own subsystem. It is not a child module of NeuroForge, DataForge, or forge-smithy.

```
WRONG: Forge Eval is a helper module inside SMITH or DataForge
RIGHT: Forge Eval is a standalone repository that evaluates sibling repos
```

Forge Eval currently implements a deterministic Pack J pipeline:

```text
risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate
```

It emits local schema-locked artifacts, but it does not own governance authority and it does not replace DataForge as the durable truth store.

---

## Per-Service Critical Warnings

### NeuroForge

**Guard file — `context_builder.py`:**
```
FILE:  neuroforge_backend/services/context_builder.py
STATE: Guard stub — raises ImportError if imported
USE:   neuroforge_backend/services/context_builder_fixed.py

The original corrupted file was deleted. A guard stub now
prevents accidental re-creation or import. All 26+ modules
import from context_builder_fixed.
```

**RTCFX invariants (4 hard rules):**
1. Compiler NEVER asserts truth about outputs
2. Compiler NEVER signs learning ledger entries (only Significance Gate does)
3. Compiler NEVER auto-promotes models
4. All learning is append-only, versioned, gated

If a PR adds auto-promotion logic to `rtcfx/compiler.py`, reject it.

**AuthorForge endpoint contract:** All `/api/v1/authorforge/*` endpoints MUST return safe empty responses on LLM failure — never 5xx. Breaking this breaks AuthorForge's degraded-mode user experience.

**`main.py` is large (63.5KB):** Use search to locate specific sections. Consider dedicated router modules for new functionality.

**Ollama batch is simulated:** Sequential calls, no cost savings. Use for local/private inference only.

**Redis is optional but strongly recommended:** Without Redis, L1 cache drops from 30%+ hit rate to MinHash/Jaccard layer only. Significant cost impact in production.

**EMA champion state is in-memory until persisted:** One data point loss possible on crash. Tolerable but means champion state briefly lags after restart.

### DataForge

**run_token scope cannot be widened:** A token for `run_id=abc` cannot write to `run_id=xyz`. Validated per request.

**Encryption key rotation requires migration:** Changing `SECRET_KEY` without running `scripts/rotate_encryption_key.py` first makes all encrypted PII fields unreadable. Never rotate without the re-encryption migration.

**FINALIZED runs are immutable:** `status = "finalized"` is one-way. Nothing can unset it. Attempts to write findings to a finalized run return 409.

**Duplicate fingerprints are correlated:** Existing findings with the same fingerprint are linked via `correlation_id` for deduplication across runs.

### ForgeAgents

**Coverage gap:** ~70% actual vs 85% target. Gaps in `app/nodes/`, `app/capabilities/`, `app/cortex/`, `app/runner/`.

**Deep mode is gated in production:** Fuzzer and failure simulator have side effects. `FORGE_ENVIRONMENT=production` blocks deep mode at agent, executor, and CLI layers with a clear error. Run deep mode in staging only.

**XAI/MAID global rate limiter:** `GlobalRateLimiter` in `routing/global_rate_limiter.py` enforces monthly caps across concurrent runs. XAI default: 5000/month, MAID default: 2000/month, daily cost cap: $10 USD. Thresholds: 80% warning, 95% critical. Configurable via `XAI_MONTHLY_CAP`, `MAID_MONTHLY_CAP`, `MAX_COST_PER_DAY` env vars. Per-run limits (XAI: 50, MAID: 20 requests + 100k tokens) still apply within each run. State is in-memory (resets on process restart).

**Global limiter operations:**

- **Monitoring:** Watch for structured log events `global_budget_warning` (80%) and `global_budget_critical` (95%). When budget exhausted, XAI/MAID calls return graceful degradation (None/empty results) — never exceptions.
- **Capacity planning:** With defaults, ~167 XAI calls/day and ~67 MAID calls/day are sustainable across all runs. Adjust caps if running more concurrent BugCheck sessions.
- **Reset:** Monthly counters reset on calendar month boundary. Daily cost resets at midnight UTC. Process restart also resets all counters (in-memory only).
- **Emergency override:** To temporarily lift limits, set `XAI_MONTHLY_CAP=999999` and restart. Monitor costs manually.

**Short-term memory lost on restart:** 100-item FIFO buffer is in-memory only. Agents mid-execution lose working context on restart. Long-term and episodic memory are durable.

**Embedding dimension hardcoded at 768:** NeuroForge model changes require coordinated migration — all pgvector indexes in DataForge must be rebuilt.

### Rake

**Render ephemeral filesystem:** Evidence bundles and mission state are PostgreSQL JSONB only — never local files.

**Orchestrator retry logic:** `PipelineOrchestrator._run_stage_with_retry()` provides per-stage exponential backoff. Default retries: FETCH=1, CLEAN=1, CHUNK=1, EMBED=2, STORE=2. Override via `max_stage_retries` constructor parameter. After all retries exhausted, `PipelineError` propagates to caller.

**Embedding validation hardcoded to 1536 dims:** If switching to `text-embedding-3-large` (3072 dims), update `models/document.py`.

**SQLite default is dev only:** Production must use `postgresql+asyncpg://` DSN.

### Forge Eval

**Standalone repo boundary:** Keep Forge Eval documented as a first-class repository in the ecosystem workspace. Do not bury it under SMITH, DataForge, or NeuroForge diagrams.

**Deterministic pipeline through Pack J:** The current implemented path is `risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate`. If ecosystem docs claim less than this, they are stale. If they claim governance authority or durable truth ownership, they are wrong.

**Artifact posture:** Forge Eval generates local schema-valid artifacts and verifies byte stability on identical input. Fail-closed behavior is part of the contract, not an optimization.

**Boundary discipline:** SMITH remains the human-authoritative governance surface. DataForge remains the durable record when artifacts need persistence beyond local execution. Target repositories remain the evaluated subjects.

---

## Environment Variable Security Checklist

Before deploying any service to staging or production:

| Variable | Requirement | Service |
|----------|------------|---------|
| `ALLOW_X_USER_ID_HEADER` | Must be `false` | NeuroForge |
| `SKIP_RATE_LIMIT` | Must be absent or `false` | NeuroForge |
| `SECRET_KEY` | 32+ byte random hex, unique per environment | NF, DF |
| `JWT_SECRET_KEY` | Strong random value, unique per environment | DF, FA, Rake |
| `DATAFORGE_SECRETS_ENABLED` | Must be `true` | NeuroForge |
| `FORGECOMMAND_KEYS_ENABLED` | Must be `true` in production | NeuroForge |
| `DATABASE_URL` | Must be PostgreSQL (never SQLite) | DF, Rake |
| `ALLOWED_ORIGINS` | No wildcards in production | DataForge |
| `ENVIRONMENT` | Set to `production` | NF, Rake |
| LLM API keys | Never in source control; inject via vault | All |

---

## Failure Cascade Analysis

When diagnosing ecosystem-wide issues, understand the dependency chain:

### DataForge Down (Most Severe)

| Affected Service | Impact |
|-----------------|--------|
| NeuroForge | Enters CACHE_ONLY or MODEL_ONLY mode. No live RAG. Inference degrades. |
| ForgeAgents | `/ready` returns 503. BugCheck runs cannot start. All writes fail. |
| Rake | STORE stage fails. Jobs marked FAILED. Missions cannot persist state. |
| ForgeCommand | Cannot create run records. Dashboard data stale. |

**Recovery:** Restore DataForge first. All services auto-recover on next successful DataForge call.

### NeuroForge Down

| Affected Service | Impact |
|-----------------|--------|
| ForgeAgents | Falls back to direct LLM API. Memory writes lack embeddings. Flag `degraded_enrichment`. |
| Rake | Cannot progress missions to STRATEGIZING. Strategy/curation blocked. |

**Recovery:** Non-critical. Services continue degraded. Auto-recover on NeuroForge return.

### Rake Down

| Affected Service | Impact |
|-----------------|--------|
| ForgeAgents | BugCheck falls back to synchronous in-process execution. Parallel modes serialize. Flag `degraded_mode: sync_fallback`. |

**Recovery:** Non-critical. ForgeAgents continues degraded. Auto-recover on Rake return.

### ForgeCommand Down

| Affected Service | Impact |
|-----------------|--------|
| All | Standalone mode. No desktop integration, no approval routing, no new run_token issuance. |

**Recovery:** Services operate independently. No data loss. Resume on ForgeCommand return.

---

## Diagnosing Degraded State

### Step 1: Check health endpoints

```bash
# All services at once
curl -s http://localhost:8000/health   # NeuroForge
curl -s http://localhost:8001/health   # DataForge
curl -s http://localhost:8002/health   # Rake
curl -s http://localhost:8010/health   # ForgeAgents
curl -s http://localhost:8003/health   # ForgeCommand Orchestrator
curl -s http://localhost:8004/health   # ForgeCommand API
```

### Step 2: Check NeuroForge degraded mode

```bash
curl -s http://localhost:8000/degraded
# Returns: { "mode": "FULL|CACHE_ONLY|MODEL_ONLY|DEGRADED_NO_RAG|OFFLINE", "reasons": [...] }
```

### Step 3: Check circuit breaker state (NeuroForge)

The context builder circuit breaker state indicates DataForge connectivity:
- `CLOSED` — Normal operation
- `OPEN` — DataForge unreachable; using fallback
- `HALF_OPEN` — Probing DataForge recovery

### Step 4: Check service readiness

```bash
curl -s http://localhost:8010/ready    # ForgeAgents — 503 if DataForge down
curl -s http://localhost:8002/ready    # Rake — 503 if critical deps down
```

---

## Migration & Deployment Runbook

### Standard Post-Pull Procedure (All Services)

```bash
cd <service_directory>

# 1. Activate virtualenv
source venv/bin/activate   # or: source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (DataForge, Rake)
alembic upgrade head

# 4. Verify
alembic current

# 5. Run tests
pytest tests/ -v --tb=short

# 6. Start service
uvicorn app.main:app --host <host> --port <port> --reload
```

### Service Startup Ports

| Service | Dev Command |
|---------|------------|
| NeuroForge | `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| DataForge | `uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload` |
| Rake | `uvicorn main:app --host 0.0.0.0 --port 8002 --reload` |
| ForgeAgents | `uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload` |
| ForgeCommand Orchestrator | Canonical local port `8003` |
| ForgeCommand API | Canonical local port `8004` |

### Database Migrations (DataForge & Rake)

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View history
alembic history --verbose
```

**Caution:** Alembic autogenerate does not detect: column renames, computed columns, custom constraints, pgvector index creation, or TSVECTOR triggers. These require manual migration steps. Review generated migrations before applying.

### DataForge First-Time Setup

```bash
cd DataForge

# Create admin user
python scripts/create_admin.py

# Or non-interactive:
ADMIN_USERNAME=admin ADMIN_PASSWORD=<strong-password> ADMIN_EMAIL=admin@forge.local \
  python scripts/create_admin.py --non-interactive
```

---

## Production Deployment Checklist

### Infrastructure Requirements

- [ ] PostgreSQL 14+ primary + at least one replica
- [ ] Redis 6+ with Sentinel (3 sentinels minimum)
- [ ] pgvector extension installed
- [ ] ForgeCommand vault configured with all API keys

### Per-Service Checks

- [ ] `SECRET_KEY` / `JWT_SECRET_KEY` generated and stored in vault
- [ ] All LLM API keys in vault (never in `.env` or source control)
- [ ] `ALLOWED_ORIGINS` lists only production origins (no wildcards)
- [ ] `LOG_LEVEL=INFO` (not DEBUG)
- [ ] `alembic upgrade head` run against production DB
- [ ] Health check endpoints registered with load balancer
- [ ] Prometheus scrape jobs configured for `/metrics`
- [ ] Backup schedule confirmed

### Smoke Tests

```bash
# Liveness
curl -f http://<host>:<port>/health

# Readiness
curl -f http://<host>:<port>/ready

# Version
curl -f http://<host>:<port>/version
```

---

## Performance Tuning Notes

### pgvector Index (DataForge)

For >100,000 chunks, tune the IVFFlat index:
```sql
-- lists = sqrt(row_count)
CREATE INDEX CONCURRENTLY ON chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 300);

-- Tune probes at query time
SET ivfflat.probes = 10;
```

### Connection Pooling (DataForge)

For high-concurrency production, add PgBouncer:
```
uvicorn (N workers) → PgBouncer (pool_size=20) → PostgreSQL
```

### Redis Memory (DataForge)

Monitor usage. If Redis memory exceeds 80% of limit, reduce TTLs or increase allocation.

---

## Key Files Quick Reference

| File | Service | Purpose |
|------|---------|---------|
| `neuroforge_backend/services/context_builder_fixed.py` | NF | RAG context builder (`context_builder.py` is a guard stub) |
| `neuroforge_backend/services/model_router.py` | NF | LLM provider selection + fallback chains |
| `neuroforge_backend/rtcfx/compiler.py` | NF | RTCFX learning pipeline |
| `app/main.py` | DF | FastAPI app, router registration, lifespan |
| `app/models/models.py` | DF | All ORM models (31+ classes) |
| `app/api/search.py` | DF | Hybrid search implementation |
| `app/utils/auth.py` | DF | JWT + bcrypt + token scoping |
| `scripts/rotate_encryption_key.py` | DF | Fernet key rotation migration |
| `app/agents/bugcheck/agent.py` | FA | BugCheck main agent class |
| `app/agents/bugcheck/lifecycle.py` | FA | State machine enforcement |
| `app/tools/router.py` | FA | Tool dispatch with mandatory policy check |
| `pipeline/orchestrator.py` | Rake | 5-stage pipeline coordinator |
| `services/mission_orchestrator.py` | Rake | Research mission state machine |
| `services/evidence_bundle.py` | Rake | SHA-256 evidence bundles |

---

## Connectivity Gap Closure (2026-02-23)

Seven connectivity gaps (F-001 through F-007) were identified and remediated across 5 repos. Changes include: port canonicalization, AuthorForge S0/S1 violation fixes (NeuroForge proxy, DataForge clients), shared `FORGE_EMBED_DIM`, deep mode production safety gates, `context_builder.py` guard stub, Rake pipeline retry logic, and global XAI/MAID rate limiter.

Full details: `CONNECTIVITY_GAP_CLOSURE_REPORT.md` (ecosystem root).

---

## Implementation Phase Status (Current Audited Snapshot)

| Service | Status |
|---------|--------|
| NeuroForge | Production ready. 5-stage pipeline, RTCFX, MAID, MAPO, AuthorForge, psychology |
| DataForge | v5.2, 18/18 phases complete. 296 tests, 82% coverage, 42,732 LOC |
| ForgeAgents | Phases 0-5 complete, Phase 6 partial (deep mode + trending in progress) |
| Rake | v1.0.0 production ready. Phases 0-4 complete (pipeline, discovery, missions, evidence) |

---

## Ecosystem Documentation Maintenance

This `doc/system/` directory is the ecosystem-level compilation of all four services' documentation. To keep it current:

1. When a service's `doc/system/` is updated, review whether the ecosystem-level chapter needs updating
2. Run `bash doc/system/BUILD.sh` to regenerate `doc/SYSTEM.md` after any chapter changes
3. Per-service docs remain the authoritative source for service-specific detail
4. `docs/canonical/ecosystem_canonical.md` has authority over all service-level documentation for ecosystem-wide principles
5. Cross-reference links to per-service docs use the pattern `<Service>/doc/system/<chapter>.md`
6. Update §16 when a code audit changes how snapshot facts should be labeled or maintained

---

## Precedence of Authority

When documentation conflicts:

1. `docs/canonical/ecosystem_canonical.md` — Canonical doctrine (highest authority)
2. `doc/system/` (this directory) — Ecosystem-level compilation
3. `<Service>/doc/system/` — Per-service documentation
4. `CLAUDE.md` — Repository-specific instructions

---

*Forge Documentation Protocol v1 — Forge Ecosystem — Last updated: 2026-03-06*
