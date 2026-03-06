# Forge Ecosystem - Service Catalog

**Document Version:** 1.0.1
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Service Overview](#service-overview)
2. [DataForge - Core Data Layer](#dataforge---core-data-layer)
3. [NeuroForge - AI Orchestration](#neuroforge---ai-orchestration)
4. [ForgeAgents - Agent Coordination](#forgeagents---agent-coordination)
5. [Rake - Data Ingestion](#rake---data-ingestion)
6. [Forge Command - Mission Control](#forge-command---mission-control)
7. [Forge:SMITH - AI Governance](#forgesmith---ai-governance)
8. [Service Comparison Matrix](#service-comparison-matrix)

---

## Service Overview

The Forge Ecosystem consists of 8 services: 4 deployed on Render.com (cloud) and 4 running locally (desktop apps).

### Cloud Services (Render.com)

| Service | Port | Role | Technology | Production URL |
|---------|------|------|------------|----------------|
| **DataForge** | 8001 | Data/Memory Layer | Python + FastAPI | `https://dataforge.onrender.com` |
| **NeuroForge** | 8000 | AI Orchestration | Python + FastAPI | `https://neuroforge.onrender.com` |
| **ForgeAgents** | 8010 | Agent Execution | Python + FastAPI | `https://forgeagents.onrender.com` |
| **Rake** | 8002 | Data Ingestion | Python + FastAPI | `https://rake.onrender.com` |

### Local Services (Desktop)

| Service | Port | Role | Technology | Type |
|---------|------|------|------------|------|
| **Forge Command** | 1420 | Mission Control | Rust + Tauri 2.0 | Desktop App |
| **Forge:SMITH** | 3001 | AI Governance | Rust + Tauri 2.0 | Desktop App |
| **Cortex BDS** | - | Semantic File Search | Rust + Tauri | Desktop App |
| **AuthorForge** | - | Story Operating System | Bun + React | In Development |

---

## DataForge - Core Data Layer

### Purpose

DataForge is the **single source of truth** for the entire Forge ecosystem. It owns all durable state, persistent data, and knowledge management. All other services are stateless and write their state to DataForge.

### Repository
- **GitHub**: `https://github.com/Boswecw/DataForge.git`
- **Branch**: `master`
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+

### Key Capabilities

#### 1. Knowledge Base Management
- **Document Storage**: Hierarchical domain-based organization
- **Tag System**: Many-to-many tagging with flexible categorization
- **Full-Text Search**: PostgreSQL `tsvector` with trigram indexing
- **Document Types**: Guides, patterns, examples, references

#### 2. Vector Embeddings (Semantic Search)
- **Embedding Providers**: Voyage AI (primary), OpenAI, Cohere
- **Vector Database**: pgvector extension (1536-dimensional embeddings)
- **Chunking Strategy**: 500-token chunks with 50-token overlap
- **Similarity Search**: Cosine similarity with configurable thresholds

#### 3. Project Management (VibeForge Integration)
- **Session Tracking**: Multi-day project sessions with state persistence
- **Conversation History**: Full thread persistence with branching support
- **Resource Management**: Attached files, URLs, code snippets
- **Collaboration**: Multi-user projects with real-time sync

#### 4. Run Provenance (NeuroForge Integration)
- **Execution Logging**: Complete LLM execution history
- **Model Tracking**: Champion model performance metrics
- **Cost Attribution**: Token usage and cost per execution
- **Context Snapshots**: Retrieved context at inference time

#### 5. Agent Execution Persistence (ForgeAgents Integration)
- **Execution Index**: Fast `/history` queries with denormalized fields
- **Memory Management**: Long-term, short-term, episodic memory storage
- **Tool Call Logs**: Complete tool execution history
- **State Snapshots**: Checkpointing for long-running agents

#### 6. Security & Compliance
- **Audit Logs**: Immutable, HMAC-SHA256 signed event logs
- **Anomaly Detection**: 6 detector types (impossible travel, brute force, etc.)
- **Encryption**: AES-256 for sensitive fields (LLM API keys)
- **Access Control**: JWT authentication with role-based permissions

#### 7. Admin Operations
- **API Key Management**: Rotation, revocation, scoped permissions
- **Secret Sync**: LLM provider keys synced from Forge Command desktop app
- **Health Monitoring**: Dependency validation, latency tracking
- **Telemetry**: Ecosystem-wide event ingestion

### API Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| **Authentication** | `/api/v1/auth/*` | 5 |
| **Search** | `/api/v1/search/*` | 4 |
| **Projects** | `/api/v1/projects/*` | 8 |
| **Runs** | `/api/v1/runs/*` | 6 |
| **Learning** | `/api/v1/learning/*` | 5 |
| **Admin** | `/admin/*` | 12 |
| **Audit** | `/api/v1/audit/*` | 3 |
| **Secrets** | `/api/v1/secrets/*` | 4 |
| **ForgeAgents** | `/api/v1/forge-run/*` | 7 |
| **BugCheck** | `/api/v1/bugcheck/*` | 9 |
| **Smithy** | `/api/v1/smithy/*` | 6 |
| **FPVS** | `/api/v1/fpvs/*` | 4 |
| **Total** | - | **73** |

### Dependencies

- **PostgreSQL 13+**: Primary database with `pgvector` extension
- **Redis 6+**: Query caching and session storage (optional but recommended)
- **Voyage AI / OpenAI / Cohere**: Embedding generation (at least one required)

### Technology Stack

```python
# Core
FastAPI==0.104+
SQLAlchemy==2.0+
Alembic==1.13+
Pydantic==2.5+

# Database
asyncpg==0.29+
pgvector==0.2.4+
redis==5.0+

# Security
python-jose==3.3+  # JWT
passlib==1.7+      # Password hashing
cryptography==41+  # AES-256 encryption

# Observability
structlog==24.1+
prometheus-client==0.20+
opentelemetry-api==1.21+
```

### Deployment Configuration

```yaml
# render.yaml
services:
  - type: web
    name: dataforge
    runtime: python
    plan: free
    buildCommand: |
      python --version
      pip install --upgrade pip
      pip install -e ./forge-telemetry
      pip install --no-cache-dir -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: dataforge-db
          property: connectionString
      - key: OPENAI_API_KEY
        sync: false
      - key: VOYAGE_API_KEY
        sync: false
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | No | - | Redis cache (degrades gracefully if absent) |
| `SECRET_KEY` | Yes | - | JWT signing key |
| `VOYAGE_API_KEY` | Yes* | - | Voyage AI embeddings |
| `OPENAI_API_KEY` | Yes* | - | OpenAI embeddings |
| `COHERE_API_KEY` | Yes* | - | Cohere embeddings |
| `ALLOWED_ORIGINS` | No | `*` | CORS allowed origins |
| `LOG_LEVEL` | No | `INFO` | Logging level |

*At least one embedding provider required.

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Average Response Time** | <100ms (p95) |
| **Throughput** | 1,000+ RPS sustained |
| **Concurrent Connections** | 50 (default pool size) |
| **Cache Hit Rate** | 95% (with Redis) |
| **Cold Start Time** | 60-90 seconds (Render Free Tier) |

---

## NeuroForge - AI Orchestration

### Purpose

NeuroForge is the **LLM orchestration pipeline** for the Forge ecosystem. It routes AI requests through a multi-stage pipeline: context building → prompt engineering → model routing → evaluation → post-processing.

### Repository
- **GitHub**: `https://github.com/Boswecw/NeuroForge.git`
- **Branch**: `master`
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+

### Key Capabilities

#### 1. Model Routing
- **Supported Providers**: OpenAI, Anthropic, Google AI, XAI (Grok), Ollama (local)
- **Champion Model Tracking**: Automatically routes to best-performing model per task
- **Fallback Chains**: Graceful degradation if primary model unavailable
- **Cost Optimization**: Intelligent routing to minimize token costs

#### 2. Context Management
- **Composite Context Provider**: Pulls from DataForge, local memory, and external sources
- **Circuit Breaker**: Automatic retry with exponential backoff
- **Context Window Management**: Automatic truncation to fit model limits
- **Semantic Compression**: Remove redundant information while preserving meaning

#### 3. Prompt Engineering
- **Template System**: Jinja2-based prompt templates
- **Few-Shot Learning**: Dynamic example injection
- **Chain-of-Thought**: Automatic CoT prompt augmentation
- **Psychology Layer**: Personality profiling for consistent character voices

#### 4. Evaluation & Quality
- **Response Scoring**: Automatic quality assessment
- **Hallucination Detection**: Fact-checking against context
- **Sentiment Analysis**: Emotional tone tracking
- **Toxicity Filtering**: Safety guardrails

#### 5. Caching & Performance
- **Prompt Caching**: MinHash-based deduplication (60-80% cost savings)
- **Redis Integration**: Distributed cache across instances
- **Response Streaming**: Server-sent events for real-time output
- **Batch Processing**: MAID batch APIs for bulk operations

#### 6. MAID Integration
- **Multi-Agent Consensus**: Routes to 3+ models for critical decisions
- **Disagreement Detection**: Flags low-consensus responses
- **Fix Proposals**: Automatic code fix generation
- **Changesets**: Multi-repo patch generation

#### 7. RTCFX Compiler System
- **Evidence Packets**: Cryptographically signed execution records
- **Run Intents**: Secure agent invocation contracts
- **Attestation**: Verifiable proof of agent actions

### API Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| **Inference** | `/process`, `/stream`, `/batch` | 3 |
| **Orchestration** | `/orchestration/*` | 5 |
| **Psychology** | `/psychology/*` | 4 |
| **Research** | `/research/*` | 3 |
| **MAID** | `/maid/*` | 2 |
| **RTCFX** | `/rtcfx/*` | 6 |
| **Admin** | `/admin/*` | 8 |
| **Analytics** | `/analytics/*` | 4 |
| **Execution** | `/execution/*` | 3 |
| **Evaluation** | `/evaluation/*` | 3 |
| **Total** | - | **41** |

### Dependencies

- **DataForge**: Context retrieval, provenance storage
- **PostgreSQL 13+**: Shared database for inference logs
- **Redis 6+**: Prompt caching (required for production)
- **OpenAI / Anthropic / Google AI / XAI**: At least one LLM provider

### Technology Stack

```python
# Core
FastAPI==0.104+
Pydantic==2.5+
SQLAlchemy==2.0+

# LLM Providers
openai==1.10+
anthropic==0.18+
google-generativeai==0.3+

# Caching & Performance
redis==5.0+
datasketch==1.6+  # MinHash caching
aiohttp==3.9+

# Observability
prometheus-fastapi-instrumentator==6.1+
opentelemetry-sdk==1.21+
structlog==24.1+
```

### Deployment Configuration

```yaml
# render.yaml
services:
  - type: web
    name: neuroforge
    runtime: python
    plan: free
    buildCommand: bash scripts/render_build.sh
    startCommand: uvicorn neuroforge_backend.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        sync: false  # Manually set to DataForge DB
      - key: OPENAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | - | Shared PostgreSQL (same as DataForge) |
| `DATAFORGE_BASE_URL` | Yes | - | DataForge API URL |
| `OPENAI_API_KEY` | Yes* | - | OpenAI models |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic Claude models |
| `GOOGLE_API_KEY` | No | - | Google Gemini models |
| `XAI_API_KEY` | No | - | XAI Grok models |
| `REDIS_URL` | Recommended | - | Prompt caching |
| `ADMIN_API_KEY` | Yes | - | Admin operations |

*At least one LLM provider required.

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Inference Latency** | 500ms - 5s (model-dependent) |
| **Cache Hit Rate** | 70-80% (with MinHash) |
| **Cost Savings** | 60-80% (with caching) |
| **Concurrent Requests** | 100+ (async architecture) |
| **Model Timeout** | 60 seconds (configurable) |

---

## ForgeAgents - Agent Coordination

### Purpose

ForgeAgents is the **AI agent orchestration layer** for the Forge ecosystem. It manages autonomous agent lifecycles, tool execution, memory management, and policy enforcement.

### Repository
- **GitHub**: `https://github.com/Boswecw/Forge-Agents.git`
- **Branch**: `master`
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+

### Key Capabilities

#### 1. Agent Management
- **Agent Registry**: Persistent agent definitions with versioning
- **Lifecycle Management**: Create, configure, execute, pause, resume, terminate
- **Multi-Agent Coordination**: Agent-to-agent communication
- **Agent Types**: Researcher, coder, analyst, orchestrator

#### 2. Memory System
- **Short-Term Memory**: In-execution context (100 items default)
- **Long-Term Memory**: Persistent knowledge with embeddings
- **Episodic Memory**: Experience replay for learning
- **Memory Quotas**: Configurable limits per agent (500MB default)

#### 3. Tool Execution
- **Tool Adapters**: Rake, NeuroForge, DataForge, Filesystem, Ecosystem, Health, Rake Scrape
- **Tool Registry**: Dynamic tool discovery and registration
- **Timeout Handling**: Per-tool timeout configuration
- **Error Recovery**: Automatic retry with exponential backoff
- **Rake Scrape Adapter**: Registered as `"rake_scrape"` in `app/main.py` lifespan -- provides `scrape_pricing_page`, `extract_pricing_data`, and `compare_catalog_prices` tools for the Pricing Monitor agent. Scrapes provider pricing pages via Rake, extracts structured data via NeuroForge, and compares against the DataForge model catalog.

#### 4. Policy Enforcement
- **Safety Policies**: Prevent harmful actions
- **Domain Policies**: Business rule enforcement
- **Resource Policies**: Rate limits, cost caps, quotas
- **Ring-Based Authorization**: 3-tier access control (0=owner, 1=operator, 2=read-only)

#### 5. BugCheck Agent (Ecosystem Quality)
- **Cross-Service Checks**: API contract drift, dependency alignment
- **Security Scanning**: Gitleaks, dependency audits
- **Test Coverage**: Pytest, vitest, cargo test integration
- **Fix Proposals**: MAID-powered automatic fixes

#### 6. Execution Persistence
- **Run Evidence**: Complete execution traces to DataForge
- **Tool Call Logs**: Full audit trail of tool usage
- **State Snapshots**: Checkpointing for long-running tasks
- **Correlation IDs**: Distributed tracing across services

#### 7. Real-Time Monitoring
- **WebSocket Streaming**: Live execution updates
- **Server-Sent Events**: Progress notifications
- **Health Checks**: Agent availability status
- **Metrics**: Execution success rate, average duration, tool usage

### API Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| **Agents** | `/api/v1/agents/*` | 12 |
| **Execution** | `/api/v1/execute/*` | 5 |
| **Memory** | `/api/v1/memory/*` | 6 |
| **Tools** | `/api/v1/tools/*` | 4 |
| **BugCheck** | `/api/v1/bugcheck/*` | 8 |
| **BugCheck WS** | `/api/v1/bugcheck/ws` | 1 |
| **BDS Execution** | `/api/v1/bds/execution/*` | 4 |
| **BDS Evaluation** | `/api/v1/bds/evaluation/*` | 3 |
| **BDS Planning** | `/api/v1/bds/planning/*` | 3 |
| **BDS Workflow** | `/api/v1/bds/workflow/*` | 3 |
| **Approvals** | `/api/v1/approvals/*` | 2 |
| **Skills** | `/api/v1/skills/*` | 3 |
| **Total** | - | **54** |

### Dependencies

- **DataForge**: Agent state, execution persistence, memory storage
- **NeuroForge**: AI operations (LLM calls)
- **Rake**: Document ingestion jobs
- **PostgreSQL 13+**: Shared database
- **Redis 6+**: Agent state caching (recommended)

### Technology Stack

```python
# Core
FastAPI==0.104+
Pydantic==2.5+
structlog==24.1+

# Agent Framework
langchain==0.1+
langchain-core==0.1+
langchain-community==0.0.13+

# Tool Adapters
httpx==0.26+
aiohttp==3.9+

# Memory & State
redis==5.0+
msgpack==1.0+

# Testing & Quality
pytest==7.4+
mypy==1.8+
ruff==0.1+
```

### Deployment Configuration

```yaml
# render.yaml
services:
  - type: web
    name: forgeagents
    runtime: python
    plan: free
    buildCommand: chmod +x render-build.sh && ./render-build.sh
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health/render
    envVars:
      - key: DATABASE_URL
        sync: false  # Manually set to DataForge DB
      - key: DATAFORGE_URL
        sync: false
      - key: NEUROFORGE_URL
        sync: false
      - key: RAKE_URL
        sync: false
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | - | Shared PostgreSQL (same as DataForge) |
| `DATAFORGE_URL` | Yes | - | DataForge API URL |
| `NEUROFORGE_URL` | Yes | - | NeuroForge API URL |
| `RAKE_URL` | Yes | - | Rake API URL |
| `REDIS_URL` | Recommended | - | Agent state caching |
| `JWT_SECRET_KEY` | Yes | - | Authentication |
| `LLM_PROVIDER` | No | `openai` | Default LLM provider |
| `OPENAI_API_KEY` | Yes* | - | OpenAI access |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic access |

*At least one LLM provider required.

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Agent Startup Time** | <500ms |
| **Execution Timeout** | 300 seconds (default) |
| **Max Iterations** | 10 (default, configurable) |
| **Memory Quota** | 500MB per agent |
| **Concurrent Agents** | 50+ (async architecture) |

---

## Rake - Data Ingestion

### Purpose

Rake is the **document ingestion pipeline** for the Forge ecosystem. It fetches, cleans, chunks, and embeds documents from various sources, then stores them in DataForge for semantic search.

### Repository
- **GitHub**: `https://github.com/Boswecw/rake.git`
- **Branch**: `master`
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+

### Key Capabilities

#### 1. Document Fetching
- **URL Scraping**: Extract content from web pages
- **File Upload**: Direct file ingestion (PDF, TXT, MD, DOCX)
- **API Integration**: Firecrawl, Tavily, Serper for web discovery
- **Batch Processing**: Process multiple documents concurrently

#### 2. Content Cleaning
- **HTML Stripping**: Remove HTML tags, scripts, styles
- **Text Normalization**: Unicode normalization, whitespace cleanup
- **Markdown Extraction**: Preserve markdown structure
- **Metadata Extraction**: Title, author, date, language detection

#### 3. Chunking Strategy
- **Token-Based Chunking**: 500-token chunks (configurable)
- **Overlap**: 50-token overlap for context continuity
- **Semantic Boundaries**: Respect paragraph/section breaks
- **Chunk Metadata**: Preserve source, position, relationships

#### 4. Embedding Generation
- **Provider Integration**: OpenAI, Voyage AI, Cohere
- **Batch Embedding**: Process up to 100 chunks per batch
- **Rate Limiting**: Respect provider rate limits
- **Error Recovery**: Retry failed embeddings with backoff

#### 5. Research Orchestration (Phase 1 - Web Discovery)

- **Web Discovery**: Async job-based discovery via `/api/v1/discover`
- **Primary Search**: Tavily AI-optimized search (advanced depth, 2 credits/query)
- **Fallback Search**: Serper.dev Google SERP API (1000x cheaper at $0.001/search)
- **Web Scraping**: Firecrawl intelligent scraper (handles JS, returns markdown)
- **Provider Fallback**: Automatic Tavily → Serper fallback chain
- **Cost Tracking**: Mission-level cost caps ($2 default), credit calculation
- **Quality Scoring**: Relevance scoring, URL deduplication by fingerprint
- **Error Handling**: Graceful degradation, detailed error reporting per query

#### 6. Job Management
- **Job Queue**: Async job processing with status tracking
- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Detailed error reporting
- **Job History**: Complete audit trail in DataForge

### API Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| **Jobs** | `/api/v1/jobs/*` | 8 |
| **Ingestion** | `/api/v1/ingest/*` | 4 |
| **Discovery** | `/api/v1/discover/*` | 2 |
| **Health** | `/health/*` | 2 |
| **Admin** | `/api/v1/admin/*` | 2 |
| **Total** | - | **18** |

#### Discovery Endpoints (Phase 1)

- **POST `/api/v1/discover`** - Submit web discovery job
  - Accepts `WebSearchParams` with multiple queries
  - Returns 202 with `discovery_id` and poll URL
  - Queues background task for async execution

- **GET `/api/v1/discover/{discovery_id}`** - Poll discovery results
  - Returns `DiscoveryResult` with discovered URLs
  - Includes status, errors, duration, cost tracking

### Dependencies

- **DataForge**: Store processed documents and embeddings
- **PostgreSQL 13+**: Shared database for job tracking
- **Redis 6+**: Job queue (optional, degrades gracefully)
- **OpenAI / Voyage AI / Cohere**: Embedding generation

### Technology Stack

```python
# Core
FastAPI==0.104+
Pydantic==2.5+
SQLAlchemy==2.0+

# Document Processing
beautifulsoup4==4.12+
markdown==3.5+
python-magic==0.4+
PyPDF2==3.0+

# Embeddings
openai==1.10+
tiktoken==0.5+

# Web Discovery (Phase 1)
tavily-python>=0.3.0      # Primary search (AI-optimized)
firecrawl-py>=0.1.0       # Primary scraper (JS-aware)
httpx>=0.24.0             # Used by Serper provider

# Task Queue
celery==5.3+  # Optional
redis==5.0+   # Optional
```

### Deployment Configuration

```yaml
# render.yaml
services:
  - type: web
    name: rake
    runtime: python
    plan: free
    buildCommand: pip install --upgrade pip && pip install -e ./forge-telemetry && pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health/render
    envVars:
      - key: DATABASE_URL
        sync: false  # Manually set to DataForge DB
      - key: DATAFORGE_BASE_URL
        sync: false
      - key: OPENAI_API_KEY
        sync: false
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | - | Shared PostgreSQL (same as DataForge) |
| `DATAFORGE_BASE_URL` | Yes | - | DataForge API URL |
| `OPENAI_API_KEY` | Yes | - | Embedding generation |
| `TAVILY_API_KEY` | No | - | Primary search provider (Phase 1) |
| `SERPER_API_KEY` | No | - | Fallback search provider (Phase 1) |
| `FIRECRAWL_API_KEY` | No | - | Primary scrape provider (Phase 1) |
| `RESEARCH_DEFAULT_PROVIDER` | No | `tavily` | Default search provider |
| `RESEARCH_MAX_SOURCES_PER_MISSION` | No | `50` | Max URLs per discovery job |
| `RESEARCH_MISSION_COST_CAP_USD` | No | `2.00` | Max cost per mission |
| `CHUNK_SIZE` | No | `500` | Chunk size in tokens |
| `CHUNK_OVERLAP` | No | `50` | Token overlap |
| `MAX_WORKERS` | No | `4` | Concurrent workers |
| `REDIS_URL` | No | - | Optional caching (graceful degradation) |

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Processing Speed** | 10-50 docs/minute (size-dependent) |
| **Chunking Speed** | 1000 tokens/second |
| **Embedding Latency** | 100-500ms per batch |
| **Max Document Size** | 10MB (configurable) |
| **Concurrent Jobs** | 4 workers (default) |

---

## Forge Command - Mission Control

### Purpose

Forge Command is the **mission control dashboard** for the Forge ecosystem. It provides real-time monitoring, health checks, service orchestration, and operational dashboards. Runs locally as a Tauri 2.0 desktop application.

### Repository
- **GitHub**: Private (Boswell Digital Solutions)
- **Language**: Rust 2024 Edition (backend) + Svelte 5 (frontend)
- **Framework**: Tauri 2.0
- **Port**: 1420 (Tauri app), 8003 (orchestrator backend)

### Key Capabilities

#### 1. Real-Time Monitoring
- **Service Health**: Live status of all Forge services
- **Latency Tracking**: P50/P90/P99 latency metrics
- **Throughput**: Requests per second across services
- **Error Rates**: 4xx/5xx error tracking

#### 2. Cost Tracking
- **Token Usage**: Per-service, per-model token consumption
- **Cost Attribution**: Real-time cost calculations
- **Budget Alerts**: Configurable spending caps
- **Projections**: Monthly cost forecasts

#### 3. Service Orchestration
- **Wake All**: Ping all services to prevent cold starts
- **Health Checks**: Manual health check triggers
- **Log Aggregation**: Centralized log viewing
- **Trace Visualization**: Distributed trace inspection

#### 4. API Key Management
- **Secret Vault**: Encrypted storage for LLM API keys
- **Key Rotation**: Sync keys to DataForge
- **Provider Management**: Enable/disable LLM providers
- **Quota Tracking**: API key usage limits

#### 5. Telemetry Ingestion
- **Event Streaming**: WebSocket-based telemetry
- **Metric Aggregation**: Real-time metric rollups
- **Alert Routing**: Anomaly notifications
- **Dashboard Updates**: Live UI refresh

#### 6. Developer Tools
- **API Playground**: Test API endpoints
- **Schema Inspector**: View database schemas
- **Query Builder**: Generate API requests
- **Log Streaming**: Tail service logs

### Technology Stack

```rust
// Backend (Rust)
tauri = "2.0"
tokio = "1.35"
serde = "1.0"
sqlx = "0.7"
axum = "0.7"
prometheus = "0.13"
```

```typescript
// Frontend (Svelte 5)
svelte = "5.x"
chart.js = "4.4"
@tauri-apps/api = "2.0"
```

### Configuration

Forge Command runs entirely locally - it is NOT deployed to Render. Configuration is stored in:
- **Linux**: `~/.config/forge_command/config.json`
- **macOS**: `~/Library/Application Support/forge_command/config.json`
- **Windows**: `%APPDATA%\forge_command\config.json`

---

## Forge:SMITH - AI Governance

### Purpose

Forge:SMITH is the **AI governance workbench** for the Forge ecosystem. It provides cryptographic authority layers, build guards, quality gates, and release governance. Runs locally as a Tauri 2.0 desktop application.

### Repository
- **GitHub**: Private (`forge-smithy`)
- **Language**: Rust 2024 Edition (backend) + TypeScript/Svelte 5 (frontend)
- **Framework**: Tauri 2.0
- **Port**: 3001

### Key Capabilities

#### 1. RTCFX Authority Layer
- **Run Intents**: Cryptographically signed agent invocation contracts
- **Evidence Packets**: Tamper-proof execution records (Ed25519 signatures)
- **Attestation**: Verifiable proof of agent actions
- **Authority Rings**: 3-tier governance (Ring 0/1/2)

#### 2. BuildGuard Quality Gates
- **Verification Ladder**: 7-tier quality checks (L0-L6)
- **Patchset Operations**: Git-based patch management
- **Pre-Commit Hooks**: Automatic quality enforcement
- **Ledger**: Immutable build history

#### 3. Smithy Release Governance
- **Release Encyclopedia**: Complete release metadata
- **Evidence Bundles**: Aggregated proof of quality
- **Approval Workflows**: Multi-stakeholder sign-off
- **Rollback Procedures**: Automated rollback on failure

#### 4. SMITH Assist (Governance Chatbot)
- **Read-Only Narrator**: Answer questions about governance state
- **Context-Aware**: Query build status, evidence, approvals
- **Natural Language**: Conversational interface
- **Audit Trail**: All queries logged

#### 5. MRPA (Minimal Rust Patch Applier)
- **Deterministic Patching**: Apply patches with governance
- **Conflict Detection**: Automatic merge conflict resolution
- **Rollback Support**: Undo patches safely
- **Audit Trail**: Complete patch history

### Technology Stack

```rust
// Backend (219 Tauri Commands)
tauri = "2.0"
ed25519-dalek = "2.1"  // Cryptographic signing
git2 = "0.18"          // Git integration
serde = "1.0"
tokio = "1.35"
```

```typescript
// Frontend (243 Svelte Components, 44 Stores)
svelte = "5.x"
@tauri-apps/api = "2.0"
```

### Configuration

Forge:SMITH runs entirely locally - it is NOT deployed to Render. Configuration is stored in:
- **Linux**: `~/.config/forge-smithy/config.json`

---

## Service Comparison Matrix

### Responsibilities

| Service | Primary Responsibility | Writes to DataForge? | Stateless? |
|---------|------------------------|----------------------|------------|
| **DataForge** | Single source of truth | Yes (owns DB) | No |
| **NeuroForge** | LLM orchestration | Yes (provenance) | Yes |
| **ForgeAgents** | Agent coordination | Yes (executions) | Yes |
| **Rake** | Data ingestion | Yes (documents) | Yes |
| **Forge Command** | Monitoring/orchestration | No (read-only) | No (local) |
| **Forge:SMITH** | AI governance | No (local authority) | No (local) |

### Technology Comparison

| Service | Language | Framework | Database | Cache |
|---------|----------|-----------|----------|-------|
| **DataForge** | Python 3.11+ | FastAPI | PostgreSQL (owner) | Redis |
| **NeuroForge** | Python 3.11+ | FastAPI | PostgreSQL (shared) | Redis |
| **ForgeAgents** | Python 3.11+ | FastAPI | PostgreSQL (shared) | Redis |
| **Rake** | Python 3.11+ | FastAPI | PostgreSQL (shared) | Redis |
| **Forge Command** | Rust 2024 | Tauri 2.0 | SQLite (local) | - |
| **Forge:SMITH** | Rust 2024 | Tauri 2.0 | SQLite (local) | - |

### Deployment Comparison

| Service | Deployment | Port | Uptime | Cold Start |
|---------|------------|------|--------|------------|
| **DataForge** | Render Free | 8001 | 99%+ | 60-90s |
| **NeuroForge** | Render Free | 8000 | 99%+ | 60-90s |
| **ForgeAgents** | Render Free | 8010 | 99%+ | 60-90s |
| **Rake** | Render Free | 8002 | 99%+ | 60-90s |
| **Forge Command** | Local Only | 1420 | N/A | <1s |
| **Forge:SMITH** | Local Only | 3001 | N/A | <1s |

### API Endpoint Count

| Service | Total Endpoints | Authentication Required | WebSocket Support |
|---------|----------------|------------------------|-------------------|
| **DataForge** | 73 | Yes (except `/health`) | No |
| **NeuroForge** | 41 | Yes (except `/health`) | Yes (`/stream`) |
| **ForgeAgents** | 54 | Yes (except `/health`) | Yes (BugCheck) |
| **Rake** | 17 | Yes (except `/health`) | No |
| **Forge Command** | 219 (Tauri commands) | N/A (local) | Yes (internal) |
| **Forge:SMITH** | 219 (Tauri commands) | N/A (local) | No |

---

## Summary

The Forge ecosystem services are designed with clear boundaries, minimal coupling, and a single source of truth (DataForge). All cloud services share a PostgreSQL database and Redis cache, enabling cost-effective deployment on Render's Free Tier while maintaining production-grade functionality.

**Key Takeaways**:
1. **DataForge** owns all durable state - other services are stateless
2. **NeuroForge** handles all LLM operations - no other service calls LLMs directly
3. **ForgeAgents** coordinates agents but delegates AI to NeuroForge and storage to DataForge
4. **Rake** ingests documents but stores everything in DataForge
5. **Forge Command** monitors everything but doesn't modify state
6. **Forge:SMITH** governs AI but runs entirely locally

This architecture enables independent scaling, clear ownership, and operational excellence.

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
