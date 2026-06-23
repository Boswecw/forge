# §3 — Tech Stack

## Shared Core Stack

The four HTTP backend services share a common Python foundation:

| Component | Version | Used By |
|-----------|---------|---------|
| Python | 3.11+ | NF, DF, FA, Rake |
| FastAPI | 0.104+ | NF, DF, FA, Rake |
| Uvicorn | 0.24+ | NF, DF, FA, Rake |
| Pydantic | v2 (2.5+) | NF, DF, FA, Rake |
| pydantic-settings | v2 | NF, FA, Rake |
| httpx | 0.25+ | NF, DF, FA, Rake |
| structlog | 23.2+ | NF, FA (DF uses stdlib logging) |
| pytest | 7.4+ | NF, DF, FA, Rake |
| pytest-asyncio | 0.21+ | NF, DF, FA, Rake |
| ruff | 0.1.7+ | NF, DF, FA, Rake |
| mypy | 1.7+ | NF, FA, Rake |

**Mandatory patterns:** Pydantic v2 API only (`.model_validate()`, `.model_dump()`). FastAPI exclusively — no Flask, Django, or raw Starlette. `httpx.AsyncClient` for all outbound calls — no `requests` or `aiohttp`.

---

## Standalone Subsystem Stacks

| Subsystem | Core Stack | Role |
|-----------|------------|------|
| **forge-smithy** | Tauri 2.0, Rust, SvelteKit / Svelte 5 | Desktop authority layer and governance workbench |
| **Forge Eval** | Python 3.12, stable Rust, `jsonschema`, `PyYAML`, stdlib-first stage orchestration | Standalone deterministic evaluation pipeline over sibling repositories |

---

## Database & Storage

| Component | Version | Role | Used By |
|-----------|---------|------|---------|
| PostgreSQL | 14+ | Primary relational store | DF (direct), Rake (direct), NF (via DF), FA (via DF) |
| pgvector | 0.2.4 | Vector similarity (IVFFlat ANN, cosine) | DF |
| Redis | 6+ | Cache, rate limiting, sessions | DF, NF (L1 cache) |
| SQLite | (built-in) | Dev databases, fallback caches | NF, Rake (dev mode) |

### ORM & Migrations

| Component | Version | Used By |
|-----------|---------|---------|
| SQLAlchemy | 2.0.23+ | DF, Rake |
| Alembic | 1.13+ | DF (11 versions), Rake |
| asyncpg | 0.29+ | NF, Rake |
| psycopg2-binary | 2.9.10 | DF |
| aiosqlite | (via SQLAlchemy) | NF, Rake (dev) |

**Note:** ForgeAgents does not hold a direct database connection. All PostgreSQL interactions go through the DataForge HTTP API.

---

## Authentication & Cryptography

| Component | Version | Role | Used By |
|-----------|---------|------|---------|
| python-jose | 3.3.0 | JWT encode/decode (HS256, RS256) | DF, FA, Rake |
| PyJWT | 2.8+ | JWT generation/validation | NF |
| passlib | 1.7.4+ | Password hashing (bcrypt backend) | NF, DF, FA, Rake |
| bcrypt | 4.1.2+ | Bcrypt backend for passlib | DF |
| cryptography | (latest) | AES-256 Fernet field-level encryption | DF, FA |

---

## AI / LLM Providers

### NeuroForge — 5 Providers

| Provider | Models | Key Capability |
|----------|--------|---------------|
| OpenAI | GPT-4, GPT-4o, GPT-4o-mini | Batch API (/v1/batches), 50% cost savings |
| Anthropic | Claude-Opus-4-6, Claude-Sonnet-4-6, Claude-Haiku-4-5 | Native batch, cached prompts (60-80% reduction), 200K context |
| Google | Gemini Pro, Gemini 1.5 Pro | Multimodal, gRPC batching |
| XAI | Grok-4, Grok-4-Fast | Real-time knowledge, reasoning |
| Ollama | Mistral, Llama 2, Neural Chat | Local/private inference, zero API cost |

### ForgeAgents — 2 Providers

| Provider | Env Var | Notes |
|----------|---------|-------|
| OpenAI | `OPENAI_API_KEY` | `LLM_PROVIDER=openai` |
| Anthropic | `ANTHROPIC_API_KEY` | `LLM_PROVIDER=anthropic` |

### Embedding Providers

| Provider | Dimensions | Used By |
|----------|-----------|---------|
| Voyage AI (`voyage-large-2`) | 1536 | DF (primary) |
| OpenAI (`text-embedding-3-small`) | 1536 | Rake (primary) |
| Voyage AI (`voyage-2`) | 1024 | DF (alternate) |
| Cohere | varies | DF (fallback) |

---

## Rake — Document Processing

| Format | Library | Notes |
|--------|---------|-------|
| PDF | `pdfplumber`, `pypdf` | pdfplumber preferred; pypdf fallback |
| DOCX | `python-docx` | Full text + table extraction |
| PPTX | `python-pptx` | Slide text extraction |
| HTML | `beautifulsoup4` | Content extraction from scraped pages |
| XML | `lxml` | API responses in XML format |
| Tokenization | `tiktoken` | cl100k_base encoding |
| Chunking | `sentence-transformers` | Local model for semantic boundary detection |

### Web Discovery Providers

| Provider | Purpose | Priority |
|----------|---------|---------|
| Tavily | AI-optimized search | Primary (if `TAVILY_API_KEY` set) |
| Serper | Google SERP | Fallback (if `SERPER_API_KEY` set) |
| Firecrawl | JS-aware scraping | Primary scraper (if `FIRECRAWL_API_KEY` set) |
| `aiohttp` | Direct HTTP scraping | Fallback when Firecrawl unavailable |

---

## ForgeAgents — BugCheck Tool Dependencies

BugCheck requires external tools installed in the runtime environment:

| Stack | Tools |
|-------|-------|
| Python | `mypy` (typecheck), `ruff` (lint), `pytest` (test) |
| TypeScript | `tsc` (typecheck), `eslint` (lint), `vitest`/`jest` (test) |
| Rust | `cargo check`, `cargo clippy`, `cargo test` |
| Security | `gitleaks` (secret scanning), dependency audit tools |

---

## Resilience & Networking

| Component | Version | Role | Used By |
|-----------|---------|------|---------|
| tenacity | 8.2.3+ | Retry with exponential backoff | NF, FA |
| cachetools | 5.3.2+ | In-process LRU/TTL caches | NF |
| websockets | — | WebSocket support (agent streaming) | FA |
| Celery | — | Async task queue + DLQ | DF |
| APScheduler | — | Scheduled tasks (disabled by default) | Rake |

---

## Observability

| Component | Role | Used By |
|-----------|------|---------|
| structlog | Structured JSON logging | NF, FA |
| stdlib logging | Structured logging with `extra={}` | DF, Rake |
| prometheus-client | Metrics at `/metrics` | DF, FA |
| OpenTelemetry | Distributed tracing | DF |
| X-Correlation-ID | Request correlation header | Rake |

---

## Testing & Quality

| Tool | Role | Used By |
|------|------|---------|
| pytest | Test runner | All |
| pytest-asyncio | Async test support | All |
| pytest-cov | Coverage reporting | DF, FA, Rake |
| pytest-mock | Mocking utilities | DF |
| ruff | Lint + format | All |
| mypy | Static type checking | NF, FA, Rake |
| black | Code formatting | NF, Rake |
| Locust | Load testing | NF |

---

## Deployment

| Environment | DF | NF | FA | Rake |
|-------------|----|----|-----|------|
| Dev DB | PostgreSQL | SQLite | (via DF) | SQLite |
| Prod DB | PostgreSQL | PostgreSQL | (via DF) | PostgreSQL |
| Container | Docker | Docker | Docker | Docker (multi-stage) |
| Orchestration | Docker Compose / K8s | Docker Compose | uvicorn | Docker Compose |
| Production | Render / K8s | Render | Render | Render |

---

## Dependency Files

| Service | Location |
|---------|----------|
| NeuroForge | `NeuroForge/requirements.txt` |
| DataForge | `DataForge/requirements.txt` |
| ForgeAgents | `ForgeAgents/requirements.txt` |
| Rake | `rake/requirements.txt` |
| Forge Eval | `forge-eval/repo/pyproject.toml`, `forge-eval/repo/rust/forge-evidence/Cargo.toml` |

Always consult the service-specific `requirements.txt` for pinned production versions. The versions in this document are minimum bounds.
