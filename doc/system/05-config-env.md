# §5 — Configuration & Environment

The resident HTTP services use Pydantic v2 `BaseSettings` for configuration. Environment variables are the single source of truth for those services, and each provides a `.env.example` at its repository root. Forge Eval is different: it is a standalone CLI/repository subsystem with optional file-based config passed at runtime rather than a resident HTTP service with a fixed env-only control surface.

---

## Port Assignments

| Service | Production Port | Dev Port | Variable |
|---------|-----------------|----------|----------|
| NeuroForge | 8000 | 8000 | `PORT` |
| DataForge | 8001 | 8001 | `PORT` |
| Rake | 8002 | 8002 | `RAKE_PORT` |
| ForgeAgents | 8010 | 8010 | `PORT` |
| ForgeCommand Orchestrator | 8003 | 8003 | — |
| ForgeCommand API | 8004 | 8004 | `LISTEN_ADDR` |

No two services may share a port. ForgeCommand uses the canonical local pair from the port registry: the orchestrator on `8003` and the local API boundary on `8004`.

## Forge Eval — Local CLI Configuration

Forge Eval has no resident listener port in the current Pack J runtime. Its operator surface is the local CLI plus an optional JSON/YAML config file supplied per run.

| Control Surface | Form | Notes |
|-----------------|------|-------|
| `forge-eval run` | CLI command | Requires `--repo`, `--base`, `--head`, `--out`; optional `--config` |
| `forge-eval validate` | CLI command | Validates an artifact directory via `--artifacts` |
| `--config` | `.json` / `.yaml` / `.yml` file | Overrides deterministic defaults in `forge_eval.config` |

The current Forge Eval config surface governs enabled stages, risk weighting, slice limits, reviewer definitions, telemetry applicability, occupancy model selection, and Pack J capture-estimate policy. It does not expose a network API or a service port.

---

## Shared Variables (All Services)

### Database

| Variable | Service | Default | Notes |
|----------|---------|---------|-------|
| `DATABASE_URL` | NF | `sqlite+aiosqlite:///./neuroforge.db` | Dev: SQLite; Prod: PostgreSQL |
| `DATABASE_URL` | DF | _(required)_ | Must be PostgreSQL: `postgresql://user:pass@host/db` |
| `DATABASE_URL` | Rake | `postgresql+asyncpg://localhost:5432/forge` | Must use `asyncpg` driver |
| `REDIS_URL` | DF | `redis://localhost:6379/0` | Required for DF; optional for FA, Rake |
| `REDIS_URL` | FA | _(optional)_ | Falls back to in-process cache |
| `REDIS_URL` | Rake | _(optional)_ | Graceful degradation if absent |

### Authentication

| Variable | Service | Default | Notes |
|----------|---------|---------|-------|
| `SECRET_KEY` | NF, DF | _(required)_ | JWT signing + Fernet encryption derivation |
| `JWT_SECRET_KEY` | DF, FA, Rake | _(required)_ | JWT signing key |
| `JWT_ALGORITHM` | FA, Rake | `HS256` | `HS256` or `RS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | NF, DF | `1440` | 24 hours |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | FA | `30` | 30 minutes |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Rake | `60` | 1 hour |

### Server

| Variable | Service | Default | Notes |
|----------|---------|---------|-------|
| `ENVIRONMENT` | NF, Rake | `development` | `development` / `staging` / `production` |
| `HOST` | NF | `0.0.0.0` | Bind address |
| `HOST` | DF | `127.0.0.1` | Bind address |
| `LOG_LEVEL` | All | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `CORS_ORIGINS` / `ALLOWED_ORIGINS` | All | `http://localhost:5173,...` | Comma-separated |

### Embeddings

| Variable | Service | Default | Notes |
|----------|---------|---------|-------|
| `FORGE_EMBED_DIM` | All | `1536` | Ecosystem-wide embedding vector dimension. Must match pgvector column types. ForgeAgents defaults to `768` if unset (legacy). |

**Changing this value requires coordinated migration:** All pgvector indexes in DataForge must be rebuilt. See §15 Handover for the procedure.

### Rate Limiting

| Variable | Service | Default | Notes |
|----------|---------|---------|-------|
| `RATE_LIMIT_PER_MINUTE` | NF, FA | `60` | Requests per minute per client |
| `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_REQUESTS_PER_MINUTE` | DF, Rake | `100` / `60` | Per window/minute |
| `RATE_LIMIT_ENABLED` | NF, Rake | `true` | Master switch |

---

## LLM Provider Keys

### NeuroForge (5 providers)

| Variable | Provider | Notes |
|----------|---------|-------|
| `OPENAI_API_KEY` | OpenAI | GPT-4 family |
| `ANTHROPIC_API_KEY` | Anthropic | Claude family |
| `GOOGLE_API_KEY` | Google | Gemini family |
| `XAI_API_KEY` | XAI | Grok family |
| `OLLAMA_BASE_URL` | Ollama | Default: `http://localhost:11434` |

### ForgeAgents (2 providers)

| Variable | Notes |
|----------|-------|
| `LLM_PROVIDER` | `openai` or `anthropic` |
| `OPENAI_API_KEY` | Required if `LLM_PROVIDER=openai` |
| `ANTHROPIC_API_KEY` | Required if `LLM_PROVIDER=anthropic` |

### DataForge (embeddings only)

| Variable | Provider | Notes |
|----------|---------|-------|
| `VOYAGE_API_KEY` | Voyage AI | Primary embedding provider |
| `OPENAI_API_KEY` | OpenAI | Fallback embedding |
| `COHERE_API_KEY` | Cohere | Secondary fallback |
| `EMBEDDING_MODEL` | — | Default: `voyage-large-2` (1536-dim) |

### Rake (embeddings + discovery)

| Variable | Provider | Notes |
|----------|---------|-------|
| `OPENAI_API_KEY` | OpenAI | Embedding generation (`text-embedding-3-small`) |
| `TAVILY_API_KEY` | Tavily | Primary search provider |
| `SERPER_API_KEY` | Serper | Fallback search |
| `FIRECRAWL_API_KEY` | Firecrawl | JS-aware scraping |

**API keys are NEVER transmitted across IPC boundaries.** In production, keys are resolved via ForgeCommand vault → environment variable fallback.

---

## Cross-Service URLs

| Variable | In Service | Target | Default |
|----------|-----------|--------|---------|
| `DATAFORGE_BASE_URL` | NF | DataForge | `http://localhost:8001` |
| `DATAFORGE_URL` | FA | DataForge | _(required)_ |
| `DATAFORGE_BASE_URL` | Rake | DataForge | `http://localhost:8001` |
| `NEUROFORGE_URL` | FA | NeuroForge | _(optional)_ |
| `NEUROFORGE_BASE_URL` | Rake | NeuroForge | _(optional)_ |
| `RAKE_URL` | FA | Rake | _(optional)_ |
| `FORGECOMMAND_URL` | FA | ForgeCommand | _(optional)_ |

**DataForge is the only required dependency.** All others degrade gracefully when absent.

---

## Service-Specific Configuration

### NeuroForge — ForgeCommand Integration

| Variable | Default | Notes |
|----------|---------|-------|
| `FORGECOMMAND_KEYS_ENABLED` | `false` | Set `true` in prod: uses ForgeCommand vault |
| `DATAFORGE_SECRETS_ENABLED` | `false` | Set `true` in staging/prod |
| `ALLOW_X_USER_ID_HEADER` | `true` | **Set `false` in production** |

### DataForge — Chunking & Encryption

| Variable | Default | Notes |
|----------|---------|-------|
| `CHUNK_SIZE` | `500` | Tokens per chunk |
| `CHUNK_OVERLAP` | `50` | Overlapping tokens |
| `MAX_EMBEDDING_INPUT_LENGTH` | `8000` | Chars before truncation |
| `ENCRYPTION_KEY` | _(derived from SECRET_KEY)_ | AES-256 Fernet for PII |

### DataForge — OAuth2 (Optional)

| Variable | Notes |
|----------|-------|
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Google OAuth2 |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth |
| `MICROSOFT_CLIENT_ID` / `MICROSOFT_CLIENT_SECRET` | Microsoft Entra |
| `OAUTH_REDIRECT_URI` | Callback URI |

### ForgeAgents — Execution

| Variable | Default | Notes |
|----------|---------|-------|
| `DEFAULT_MAX_ITERATIONS` | `10` | Max 5-phase loop iterations |
| `DEFAULT_EXECUTION_TIMEOUT` | `300` | 5-minute wall-clock limit |
| `SHORT_TERM_MEMORY_SIZE` | `100` | FIFO capacity per agent |
| `EPISODIC_MEMORY_RETENTION_DAYS` | `90` | DataForge episodic TTL |
| `MAX_COST_PER_DAY` | `10.0` | LLM API spend cap (USD), enforced by global rate limiter |
| `SERVICE_TIMEOUT` | `30` | Outbound HTTP timeout (seconds) |
| `SERVICE_RETRIES` | `3` | Outbound retry attempts |

### ForgeAgents — Global API Rate Limiting

| Variable | Default | Notes |
|----------|---------|-------|
| `XAI_MONTHLY_CAP` | `5000` | Max XAI (Grok) API requests per month across all runs |
| `MAID_MONTHLY_CAP` | `2000` | Max MAID (Claude) API requests per month across all runs |
| `MAX_COST_PER_DAY` | `10.0` | Daily LLM API spend cap in USD |

**Alert thresholds:** 80% warning (structured log `global_budget_warning`), 95% critical (`global_budget_critical`). Per-run limits (XAI: 50 requests, MAID: 20 requests + 100k tokens) still apply within each run. Monthly window resets on calendar month boundary. Counters are in-memory; process restart resets them.

### Rake — Pipeline Tuning

| Variable | Default | Notes |
|----------|---------|-------|
| `MAX_WORKERS` | `4` | Concurrent pipeline workers (1-32) |
| `CHUNK_SIZE` | `500` | Tokens per chunk |
| `CHUNK_OVERLAP` | `50` | Must be < CHUNK_SIZE |
| `OPENAI_BATCH_SIZE` | `100` | Chunks per embedding call |
| `RESEARCH_MAX_SOURCES_PER_MISSION` | `50` | Sources per mission (1-100) |
| `RESEARCH_MISSION_COST_CAP_USD` | `2.00` | Budget per mission |

### Rake — Source-Specific

| Variable | Default | Notes |
|----------|---------|-------|
| `SEC_EDGAR_USER_AGENT` | _(required)_ | Must include contact email per SEC policy |
| `URL_SCRAPE_RESPECT_ROBOTS` | `true` | Respect robots.txt |
| `URL_SCRAPE_MAX_SIZE` | `10485760` | 10 MB max page size |
| `DB_QUERY_READ_ONLY` | `true` | Rejects non-SELECT queries |
| `DB_QUERY_MAX_ROWS` | `1000` | Max rows per query |

---

## Secrets Management

| Environment | Method |
|-------------|--------|
| Development | `.env` file (never committed) |
| Staging | ForgeCommand vault → environment variables |
| Production | ForgeCommand vault / Docker secrets / Kubernetes Secrets |

**Critical validation rules:**
1. `SECRET_KEY` / `JWT_SECRET_KEY` must be present — services fail to start without it
2. `DATABASE_URL` for DataForge must be PostgreSQL (never SQLite in production)
3. `ALLOW_X_USER_ID_HEADER=true` in production is a security misconfiguration
4. Rake validates that `OPENAI_API_KEY` and `JWT_SECRET_KEY` are non-default in production

---

*For per-service variable details, see each service's own `doc/system/` configuration chapter. For API authentication, see §8. For deployment specifics, see §15.*
