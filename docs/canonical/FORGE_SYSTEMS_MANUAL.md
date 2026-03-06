# Forge Ecosystem Systems Manual

**Version:** 1.0
**Last Updated:** December 27, 2025
**Classification:** Internal Technical Reference
**Maintainer:** Boswell Digital Solutions LLC

---

## Table of Contents

1. [Executive Overview](#1-executive-overview)
2. [System Architecture](#2-system-architecture)
3. [Security Model](#3-security-model)
4. [Core Services](#4-core-services)
5. [Desktop Applications](#5-desktop-applications)
6. [ForgeCommand Integration](#6-forgecommand-integration)
7. [Key Rotation System](#7-key-rotation-system)
8. [Operations Guide](#8-operations-guide)
9. [Deployment](#9-deployment)
10. [Troubleshooting](#10-troubleshooting)
11. [Appendices](#11-appendices)

---

## 1. Executive Overview

### 1.1 What is the Forge Ecosystem?

The Forge Ecosystem is a comprehensive AI infrastructure platform consisting of:

- **4 Backend Services**: DataForge, NeuroForge, Rake, ForgeAgents
- **3 Desktop Applications**: Forge Command, forge-smithy, Cortex BDS
- **2 Infrastructure Components**: PostgreSQL (with pgvector), Redis

Together, these components provide:

| Capability | Description |
|------------|-------------|
| **Vector Memory** | Semantic search, embeddings storage, document retrieval |
| **LLM Orchestration** | Multi-model routing across OpenAI, Anthropic, Google, xAI, Ollama |
| **Data Ingestion** | Automated fetch → clean → chunk → embed → store pipeline |
| **Agent Automation** | Autonomous AI agents with tools, policies, and memory |
| **Credential Management** | Centralized vault with 30-day key rotation |
| **Operational Control** | Mission control dashboard for monitoring and operations |

### 1.2 Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Single Source of Truth** | ForgeCommand owns all credentials; DataForge owns all telemetry |
| **Brokered Access** | UI layers never receive plaintext secrets |
| **Fail Fast** | Invalid states cause immediate rejection, not silent degradation |
| **Audit Everything** | All credential access, state transitions, and operations are logged |
| **Offline-First Desktop** | Desktop apps work without network; sync when available |

### 1.3 Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Backend Services** | Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| **Desktop Apps** | Tauri 2.0, Rust, SvelteKit 2, Svelte 5 Runes, Tailwind v4 |
| **Database** | PostgreSQL 14+ with pgvector extension |
| **Cache** | Redis 6+ |
| **AI/ML** | OpenAI, Anthropic Claude, Google Gemini, xAI Grok, Ollama |
| **Embeddings** | ONNX Runtime (local), OpenAI ada-002 (cloud) |

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATIONS                                   │
│    VibeForge · AuthorForge · TradeForge · Rail Harmony · Custom Apps        │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────────┐
│                     DESKTOP CONTROL PLANE                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │ Forge Command  │  │  forge-smithy  │  │   Cortex BDS   │                 │
│  │ (Mission Ctrl) │  │ (AI Pipeline)  │  │ (File Search)  │                 │
│  │                │  │                │  │                │                 │
│  │ ┌────────────┐ │  │ ┌────────────┐ │  │ ┌────────────┐ │                 │
│  │ │ Credential │ │  │ │ForgeCommand│ │  │ │ForgeCommand│ │                 │
│  │ │   Vault    │◄├──┤─│  Client    │ │  │ │  Client    │ │                 │
│  │ │ (SQLite)   │ │  │ └────────────┘ │  │ └────────────┘ │                 │
│  │ └────────────┘ │  └────────────────┘  └────────────────┘                 │
│  └────────────────┘                                                          │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ HTTP (Authenticated)
┌──────────────────────────────▼──────────────────────────────────────────────┐
│                     BACKEND SERVICES LAYER                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │ NeuroForge │  │ DataForge  │  │    Rake    │  │ForgeAgents │             │
│  │   :8000    │  │   :8001    │  │   :8002    │  │   :8010    │             │
│  │ LLM Router │  │Vector Mem  │  │ Ingestion  │  │   Agents   │             │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘             │
│        └───────────────┴───────────────┴───────────────┘                     │
│                               │                                              │
└───────────────────────────────┼──────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                                     │
│        ┌──────────────────┐        ┌──────────────────┐                     │
│        │   PostgreSQL     │        │      Redis       │                     │
│        │   + pgvector     │        │     (Cache)      │                     │
│        │    :5432         │        │      :6379       │                     │
│        └──────────────────┘        └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow Patterns

#### 2.2.1 Ingestion Flow (Rake → DataForge)

```
External Source → Rake Fetch → Clean → Chunk → Embed → DataForge Store
                    ↓            ↓        ↓        ↓          ↓
               [Raw Content] [Sanitized] [Chunks] [Vectors] [Indexed]
```

#### 2.2.2 Query Flow (Client → NeuroForge → DataForge)

```
User Query → NeuroForge → RAG Context Fetch → LLM Generation → Response
                 ↓               ↓                  ↓
            [Route Model]  [DataForge Query]  [Claude/GPT/Grok]
```

#### 2.2.3 Agent Execution Flow (ForgeAgents)

```
Task Request → Agent Selection → Tool Execution → Memory Update → Result
                    ↓                 ↓               ↓
              [Policy Check]   [External APIs]  [DataForge Store]
```

### 2.3 Port Assignments

| Service | Development | Production | Protocol |
|---------|-------------|------------|----------|
| NeuroForge | 8000 | 443 (Render) | HTTPS |
| DataForge | 8001 | 443 (Render) | HTTPS |
| Rake | 8002 | 443 (Render) | HTTPS |
| ForgeAgents | 8010 | 443 (Render) | HTTPS |
| PostgreSQL | 5432 | 5432 (Render) | PostgreSQL |
| Redis | 6379 | 6379 (Redis Labs) | Redis |
| Forge Command | 1420 | N/A (Desktop) | Tauri IPC |

---

## 3. Security Model

### 3.1 Credential Authority

**Forge Command is the single credential authority for the entire ecosystem.**

```
┌─────────────────────────────────────────────────────────────┐
│                    FORGE COMMAND                             │
│              (Credential Authority)                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │            Encrypted SQLite Vault                        │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │ │
│  │  │NeuroForge   │ │ DataForge   │ │    Rake     │        │ │
│  │  │  API Key    │ │  API Key    │ │  API Key    │        │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │ │
│  │  │ForgeAgents  │ │  OpenAI     │ │ Anthropic   │        │ │
│  │  │  API Key    │ │  API Key    │ │  API Key    │        │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          │                                   │
│              ┌───────────┴───────────┐                       │
│              │   Rust Backend Only   │                       │
│              │  (Never crosses IPC)  │                       │
│              └───────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Brokered Access Model

UI layers (Svelte frontends) **never receive plaintext credentials**. When an app needs to call a backend service:

1. **Frontend requests operation** via Tauri IPC (e.g., "fetch user data")
2. **Rust backend retrieves credential** from vault (internal only)
3. **Rust backend makes authenticated HTTP call** with injected headers
4. **Result (not credential) returned** to frontend via IPC

```
┌──────────────┐     IPC (invoke)      ┌──────────────┐
│   Svelte     │ ─────────────────────▶│    Rust      │
│   Frontend   │    "fetch_users"      │   Backend    │
│              │                       │              │
│  NO SECRETS  │◀───────────────────── │ + Vault Read │
│   HERE       │    [{users...}]       │ + HTTP Call  │
└──────────────┘                       └──────────────┘
```

### 3.3 IPC Boundary Enforcement

**Commands that handle credentials are internal Rust functions only.**

| Command | Crosses IPC? | Notes |
|---------|--------------|-------|
| `get_active_api_key` | NO | Internal Rust function for authenticated calls |
| `list_service_credentials` | YES | Returns metadata only (service name, status, dates) |
| `rotate_service_key` | YES | Triggers rotation; new key never returned |
| `get_scheduler_status` | YES | Returns scheduler state, not credentials |

### 3.4 Hard Rules

These rules are **non-negotiable** and enforced at the code level:

1. **No Forge UI layer ever receives, logs, or stores long-lived service credentials**
2. **All secret access is mediated by Rust backends**
3. **Credentials stored with XOR encryption** in SQLite vault
4. **Vault file location**: `~/.forge-command/local.db`
5. **Emergency bypass requires `EMERGENCY_OPS_KEY` header** (audit-logged)

### 3.5 Authentication Flow

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Desktop    │      │   Forge     │      │  Backend    │
│    App      │      │  Command    │      │  Service    │
│             │      │   Vault     │      │             │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │ 1. Need NeuroForge │                    │
       │───────────────────▶│                    │
       │                    │                    │
       │                    │ 2. Read vault      │
       │                    │    (internal)      │
       │                    │                    │
       │ 3. Credential      │                    │
       │    (Rust only)     │                    │
       │◀───────────────────│                    │
       │                    │                    │
       │ 4. HTTP + Authorization: Bearer {key}   │
       │────────────────────────────────────────▶│
       │                    │                    │
       │ 5. Response                             │
       │◀────────────────────────────────────────│
       │                    │                    │
```

---

## 4. Core Services

### 4.1 DataForge (Vector Memory Engine)

**Purpose**: Persistent vector storage, semantic search, and document management.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/collections` | GET/POST | List or create vector collections |
| `/api/v1/documents` | POST | Store documents with embeddings |
| `/api/v1/search` | POST | Semantic similarity search |
| `/api/v1/health` | GET | Service health check |
| `/api/v1/stats` | GET | Collection statistics |

**Key Features**:
- PostgreSQL + pgvector for vector storage
- Multiple embedding models (OpenAI ada-002, local ONNX)
- Metadata filtering with semantic search
- Batch document ingestion

**Environment Variables**:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dataforge
OPENAI_API_KEY=sk-...  # For ada-002 embeddings
REDIS_URL=redis://...  # Cache layer
```

### 4.2 NeuroForge (LLM Orchestration)

**Purpose**: Route AI requests to optimal models across multiple providers.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat` | POST | Chat completion with model routing |
| `/api/v1/embeddings` | POST | Generate embeddings |
| `/api/v1/models` | GET | List available models |
| `/api/v1/providers` | GET | Provider health status |
| `/api/v1/costs` | GET | Token usage and cost tracking |

**Supported Providers**:

| Provider | Models | Status |
|----------|--------|--------|
| OpenAI | GPT-4, GPT-4o, GPT-3.5-turbo | Production |
| Anthropic | Claude 3.5, Claude 3 Opus/Sonnet | Production |
| Google | Gemini Pro, Gemini Ultra | Production |
| xAI | Grok-2, Grok-2-mini | Production |
| Ollama | Llama 3, Mistral, etc. | Local Only |

**Routing Logic**:
1. Check provider circuit breaker state
2. Evaluate cost vs. capability requirements
3. Apply rate limiting and quota checks
4. Route to optimal model
5. Fallback to secondary provider if primary fails

### 4.3 Rake (Data Ingestion Pipeline)

**Purpose**: Automated data ingestion from external sources.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/jobs` | GET/POST | List or create ingestion jobs |
| `/api/v1/jobs/{id}` | GET | Job status and progress |
| `/api/v1/sources` | GET/POST | Manage data sources |
| `/api/v1/schedule` | POST | Schedule recurring jobs |

**Pipeline Phases**:

```
FETCH → CLEAN → CHUNK → EMBED → STORE → COMPLETE
  ↓        ↓       ↓       ↓       ↓        ↓
[Raw]  [Sanitize] [Split] [Vector] [Index] [Done]
```

**Supported Sources**:
- Web URLs (HTML, PDF, DOCX)
- Local files and directories
- APIs (REST, GraphQL)
- Databases (PostgreSQL, MySQL)
- Cloud storage (S3, GCS)

### 4.4 ForgeAgents (Agent Orchestration)

**Purpose**: Autonomous AI agents with tools, policies, and persistent memory.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/agents` | GET/POST | List or create agents |
| `/api/v1/agents/{id}/execute` | POST | Execute agent task |
| `/api/v1/tasks` | GET | List all tasks |
| `/api/v1/tasks/ecosystem` | POST | EcosystemAgent operations |
| `/api/v1/tools` | GET | Available tools |

**Agent Types**:

| Type | Purpose | Tools |
|------|---------|-------|
| `research` | Information gathering | web_search, document_read |
| `coding` | Code generation/review | code_write, test_run |
| `data` | Data analysis | query_database, visualize |
| `ecosystem` | Cross-service operations | All Forge APIs |

**EcosystemAgent Operations**:

| Operation | Capability | Description |
|-----------|------------|-------------|
| `ecosystem_health` | READ | Real-time health across services |
| `ecosystem_stats` | READ | Aggregate metrics |
| `ecosystem_costs` | READ | Cost tracking |
| `ecosystem_wake` | WRITE | Wake sleeping services |
| `ecosystem_cache_flush` | WRITE | Flush caches |
| `ecosystem_rollback` | DESTRUCTIVE | Rollback by correlation ID |

---

## 5. Desktop Applications

### 5.1 Forge Command (Mission Control)

**Purpose**: Operational headquarters for the Forge ecosystem.

**Location**: `/ecosystem/Forge_Command/`

**Technology**:
- Tauri 2.0 (Rust backend)
- SvelteKit 2 + Svelte 5 Runes
- Tailwind CSS v4
- SQLite (local vault)

**Key Features**:

| Feature | Description |
|---------|-------------|
| Health Monitoring | Real-time status for all services |
| Cost Tracking | Token usage, spending projections, budget alerts |
| Distributed Tracing | Request flow visualization with correlation IDs |
| API Key Management | Centralized credential vault |
| Key Rotation | 30-day automated rotation with kitchen hours blocking |
| Alerting | Configurable thresholds and notifications |
| Operations | Service controls with audit logging |

**Architecture**:
```
src/
├── lib/
│   ├── components/     # Svelte components
│   ├── stores/         # Svelte stores
│   └── services/       # API clients
├── routes/             # SvelteKit pages
└── app.html

src-tauri/
├── src/
│   ├── commands/       # Tauri IPC commands
│   ├── rotation/       # Key rotation logic
│   ├── vault/          # Credential vault
│   └── main.rs
└── Cargo.toml
```

### 5.2 forge-smithy (AI Pipeline Manager)

**Purpose**: Governed AI development pipeline with approval workflows.

**Location**: `/ecosystem/forge-smithy/`

**Technology**:
- Tauri 2.0 (Rust backend)
- SvelteKit 2 + Svelte 5 Runes
- BuildGuard governance engine
- ForgeCommand vault client

**Key Features**:

| Feature | Description |
|---------|-------------|
| Pipeline Execution | Governed step-by-step AI operations |
| Mandate System | Approval gates with override authority |
| Evidence Collection | Audit trail for all pipeline actions |
| BuildGuard | Pre-execution safety checks |
| VS Code Integration | Push deliverables to IDE |

**Pipeline States**:
```
IDLE → COORDINATING → MANDATE_GATE → EXECUTING → VERIFYING → EVALUATING → COMPLETE
                           ↓
                      BLOCKED (requires override)
```

**Architecture**:
```
src/
├── lib/
│   ├── pipeline/       # Pipeline state machine
│   ├── stores/         # Svelte stores
│   └── services/       # API clients
├── routes/
│   ├── coordinator/    # Pipeline control
│   ├── evaluator/      # Result review
│   └── execution/      # Active execution
└── tests/

src-tauri/
├── src/
│   ├── buildguard/     # Governance engine
│   ├── forgecommand/   # Vault client
│   └── grr/            # GRR engine
└── Cargo.toml
```

### 5.3 Cortex BDS (Semantic File Search)

**Purpose**: AI-powered local file search with embeddings.

**Location**: `/ecosystem/cortex_bds/`

**Technology**:
- Tauri 2.0 (Rust backend)
- SvelteKit 2 + Svelte 5 Runes
- SQLite + FTS5
- ONNX Runtime (local embeddings)
- ForgeCommand vault client

**Key Features**:

| Feature | Description |
|---------|-------------|
| File Indexing | Recursive directory scanning |
| Full-Text Search | SQLite FTS5 with ranking |
| Semantic Search | Local ONNX embeddings |
| Pattern Library | Saved search patterns |
| Collections | Smart file groupings |
| File Watching | Real-time index updates |

**Architecture**:
```
src/
├── lib/
│   ├── components/     # UI components
│   ├── stores/         # Svelte stores
│   └── services/       # Search clients
└── routes/

src-tauri/
├── src/
│   ├── ai/             # Embedding generation
│   ├── commands/       # Tauri IPC commands
│   ├── db/             # SQLite + FTS5
│   ├── forgecommand/   # Vault client
│   ├── indexer/        # File scanner
│   └── search/         # Search engine
└── Cargo.toml
```

---

## 6. ForgeCommand Integration

### 6.1 Overview

All Forge desktop applications integrate with ForgeCommand's credential vault. This provides:

- **Centralized key management**: No `.env` files with secrets
- **Automatic rotation**: 30-day key lifecycle
- **Zero-config**: Apps read from shared vault
- **Audit trail**: All key access logged

### 6.2 Vault Location

```
~/.forge-command/
├── local.db          # Encrypted SQLite vault
├── local.db-shm      # SQLite shared memory
└── local.db-wal      # Write-ahead log
```

### 6.3 Integration Pattern

Each app implements a `forgecommand` module:

```
src-tauri/src/forgecommand/
├── mod.rs            # Module exports
├── types.rs          # Credential structs
├── client.rs         # ForgeCommandClient
└── commands.rs       # Tauri IPC commands
```

**Client Implementation** (Rust):

```rust
pub struct ForgeCommandClient {
    pool: SqlitePool,
}

impl ForgeCommandClient {
    pub async fn new() -> Result<Self, Error> {
        let vault_path = dirs::home_dir()
            .ok_or(Error::HomeDirNotFound)?
            .join(".forge-command")
            .join("local.db");

        let pool = SqlitePoolOptions::new()
            .max_connections(1)
            .connect(&format!("sqlite:{}", vault_path.display()))
            .await?;

        Ok(Self { pool })
    }

    pub async fn get_service_key(&self, service: &str) -> Result<String, Error> {
        let row = sqlx::query("SELECT value FROM credentials WHERE service = ?")
            .bind(service)
            .fetch_one(&self.pool)
            .await?;

        let encrypted: Vec<u8> = row.get("value");
        Ok(self.decrypt_value(&encrypted))
    }

    fn decrypt_value(&self, encrypted: &[u8]) -> String {
        // XOR decryption matching ForgeCommand's encryption
        let key = b"forge-command-local-key";
        encrypted.iter()
            .zip(key.iter().cycle())
            .map(|(a, b)| a ^ b)
            .collect::<Vec<u8>>()
            .into_iter()
            .map(|b| b as char)
            .collect()
    }
}
```

### 6.4 Available Commands

| Command | Description |
|---------|-------------|
| `forgecommand_is_available` | Check if vault exists |
| `forgecommand_get_status` | Vault connectivity status |
| `forgecommand_list_credentials` | List configured services |
| `forgecommand_get_service_key` | Get key for service (internal) |
| `forgecommand_get_neuroforge_key` | NeuroForge API key |
| `forgecommand_get_dataforge_key` | DataForge API key |
| `forgecommand_get_rake_key` | Rake API key |
| `forgecommand_get_forgeagents_key` | ForgeAgents API key |

### 6.5 Dependency

Add to `Cargo.toml`:

```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
```

---

## 7. Key Rotation System

### 7.1 Overview

ForgeCommand implements automated 30-day key rotation for all backend services.

### 7.2 Rotation Schedule

| Phase | Duration | Description |
|-------|----------|-------------|
| Active | Days 1-23 | Current key in use |
| Overlap Start | Day 24 | New key generated, both valid |
| Overlap Period | Days 24-30 | Both keys accepted by services |
| Old Key Expires | Day 31 | Old key invalidated |

### 7.3 Kitchen Hours Blocking

Automated rotation is blocked during peak usage hours:

- **Blocked**: 10:00 - 22:00 local time
- **Allowed**: 22:00 - 10:00 local time
- **Override**: `EMERGENCY_OPS_KEY` header bypasses blocking

### 7.4 Emergency Operations

For critical situations requiring rotation during kitchen hours:

```bash
# Set emergency key in environment
export EMERGENCY_OPS_KEY="your-emergency-key"

# Emergency rotation is audit-logged with:
# - Timestamp
# - Operator identity
# - Reason (required)
# - Service affected
```

### 7.5 Rotation Flow

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│  Scheduler │────▶│   Check    │────▶│   Rotate   │
│   (Tick)   │     │Kitchen Hrs │     │    Key     │
└────────────┘     └─────┬──────┘     └─────┬──────┘
                         │                   │
                    Blocked?            New Key
                         │                   │
                         ▼                   ▼
                   ┌──────────┐       ┌──────────┐
                   │  Queue   │       │  Store   │
                   │  Retry   │       │  Vault   │
                   └──────────┘       └────┬─────┘
                                           │
                                           ▼
                                    ┌──────────┐
                                    │  Notify  │
                                    │  Apps    │
                                    └──────────┘
```

### 7.6 Monitoring

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `key_age_days` | Days since last rotation | > 25 days |
| `rotation_failures` | Failed rotation attempts | > 0 |
| `overlap_remaining` | Days until old key expires | < 3 days |

---

## 8. Operations Guide

### 8.1 Starting Services

**Development (Local)**:

```bash
# Start all backend services
cd /ecosystem/DataForge && uvicorn main:app --port 8001 &
cd /ecosystem/NeuroForge && uvicorn main:app --port 8000 &
cd /ecosystem/rake && uvicorn main:app --port 8002 &
cd /ecosystem/ForgeAgents && uvicorn main:app --port 8010 &

# Start Forge Command
cd /ecosystem/Forge_Command && pnpm tauri dev

# Start forge-smithy
cd /ecosystem/forge-smithy && pnpm tauri dev

# Start Cortex BDS
cd /ecosystem/cortex_bds && pnpm tauri dev
```

**Production (Render)**:

All backend services are deployed on Render with auto-sleep after inactivity:

| Service | Wake Time | Auto-Sleep |
|---------|-----------|------------|
| DataForge | ~30s | 15 min inactivity |
| NeuroForge | ~30s | 15 min inactivity |
| Rake | ~30s | 15 min inactivity |
| ForgeAgents | ~45s | 15 min inactivity |

Use Forge Command's "Wake All" button to spin up sleeping services.

### 8.2 Health Checks

**Manual Health Check**:

```bash
# Check individual services
curl https://dataforge-pzmo.onrender.com/api/v1/health
curl https://neuroforge-9lxc.onrender.com/api/v1/health
curl https://rake-zp35.onrender.com/api/v1/health
curl https://forgeagents.onrender.com/api/v1/health
```

**Via Forge Command**:

Forge Command polls health every 30 seconds and displays:
- **Green**: Service UP
- **Yellow**: Service DEGRADED (4xx/5xx responses)
- **Red**: Service DOWN (timeout/connection refused)

### 8.3 Log Access

**Backend Services** (Render Dashboard):
1. Navigate to service in Render dashboard
2. Click "Logs" tab
3. Filter by severity or search

**Desktop Apps** (Local):
```bash
# Forge Command logs
tail -f ~/.forge-command/logs/app.log

# forge-smithy logs
tail -f ~/.forge-smithy/logs/app.log

# Cortex BDS logs
tail -f ~/.cortex-bds/logs/app.log
```

### 8.4 Common Operations

| Operation | Forge Command Action |
|-----------|---------------------|
| Wake all services | Click "Wake All" button |
| Flush caches | Operations → Flush Cache |
| Rotate API key | Settings → Credentials → Rotate |
| View costs | Costs dashboard |
| Check alerts | Alerts dashboard |
| Trace request | Tracing → Enter correlation ID |

---

## 9. Deployment

### 9.1 Backend Services (Render)

**Deployment Configuration** (`render.yaml`):

```yaml
services:
  - type: web
    name: dataforge
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: REDIS_URL
        sync: false

  - type: web
    name: neuroforge
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Deployment Process**:
1. Push to `main` branch
2. Render auto-deploys within 5 minutes
3. Health check validates deployment
4. Rollback available if health check fails

### 9.2 Desktop Applications

**Build Commands**:

```bash
# Forge Command
cd /ecosystem/Forge_Command
pnpm install
pnpm tauri build

# forge-smithy
cd /ecosystem/forge-smithy
pnpm install
pnpm tauri build

# Cortex BDS
cd /ecosystem/cortex_bds
pnpm install
pnpm tauri build
```

**Output Locations**:

| Platform | Location |
|----------|----------|
| Windows | `src-tauri/target/release/bundle/msi/*.msi` |
| macOS | `src-tauri/target/release/bundle/dmg/*.dmg` |
| Linux | `src-tauri/target/release/bundle/deb/*.deb` |

### 9.3 Database Migrations

**DataForge/NeuroForge/Rake** (Alembic):

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Cortex BDS** (Refinery):

```bash
# Migrations are embedded and run on startup
# Located in src-tauri/migrations/
```

---

## 10. Troubleshooting

### 10.1 Service Won't Start

| Symptom | Cause | Solution |
|---------|-------|----------|
| Connection refused | Service not running | Start service, check port |
| Timeout | Render cold start | Wait 30-60s, use Wake All |
| 500 error | Internal error | Check service logs |
| 503 error | Service overloaded | Scale up or reduce load |

### 10.2 Credential Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Vault not found" | ForgeCommand not installed | Install ForgeCommand first |
| "Key expired" | Rotation overdue | Trigger manual rotation |
| "Decryption failed" | Corrupt vault | Restore from backup |
| "Service unauthorized" | Key mismatch | Verify key in vault |

### 10.3 Desktop App Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Blank screen | WebView crash | Restart app, check logs |
| IPC timeout | Rust panic | Check `src-tauri/logs/` |
| Build fails | Missing deps | Run `pnpm install`, `cargo build` |
| Icon missing | Asset not found | Verify icons in `src-tauri/icons/` |

### 10.4 Performance Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Slow queries | Missing indexes | Add database indexes |
| High latency | Cold starts | Keep services warm |
| Memory spike | Large embeddings | Batch processing |
| CPU spike | Concurrent requests | Rate limiting |

### 10.5 Emergency Procedures

**Service Outage**:
1. Check Render dashboard for errors
2. Review recent deployments
3. Rollback if deployment caused issue
4. Scale up if overloaded
5. Contact Render support if infrastructure issue

**Credential Compromise**:
1. Immediately rotate all affected keys
2. Use `EMERGENCY_OPS_KEY` to bypass kitchen hours
3. Audit access logs for unauthorized use
4. Update vault backup
5. Notify security team

**Data Loss**:
1. Stop all write operations
2. Identify last known good backup
3. Restore from backup
4. Replay transaction logs if available
5. Validate data integrity

---

## 11. Appendices

### 11.1 Environment Variables Reference

**Backend Services**:

| Variable | Service | Description |
|----------|---------|-------------|
| `DATABASE_URL` | All | PostgreSQL connection string |
| `REDIS_URL` | All | Redis connection string |
| `OPENAI_API_KEY` | NeuroForge | OpenAI API key |
| `ANTHROPIC_API_KEY` | NeuroForge | Anthropic API key |
| `GOOGLE_API_KEY` | NeuroForge | Google AI API key |
| `XAI_API_KEY` | NeuroForge | xAI API key |

**Desktop Apps**:

| Variable | App | Description |
|----------|-----|-------------|
| `FORGE_COMMAND_VAULT` | All | Override vault location |
| `EMERGENCY_OPS_KEY` | Forge Command | Emergency override key |
| `CORTEX_IPC_SOCKET` | Cortex BDS | IPC socket path |

### 11.2 API Rate Limits

| Service | Endpoint | Limit |
|---------|----------|-------|
| DataForge | `/api/v1/search` | 100/min |
| NeuroForge | `/api/v1/chat` | 60/min |
| Rake | `/api/v1/jobs` | 10/min |
| ForgeAgents | `/api/v1/agents/*/execute` | 30/min |

### 11.3 Backup Schedule

| Data | Frequency | Retention |
|------|-----------|-----------|
| PostgreSQL | Daily | 30 days |
| Redis | Hourly (AOF) | 7 days |
| Vault (`local.db`) | On rotation | 5 versions |
| Audit logs | Daily | 90 days |

### 11.4 Contact Information

| Role | Contact |
|------|---------|
| Technical Lead | tech@boswelldigital.com |
| Security Team | security@boswelldigital.com |
| Operations | ops@boswelldigital.com |
| Emergency | emergency@boswelldigital.com |

---

**Document History**:

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-27 | Forge Team | Initial release |

---

<p align="center">
  <strong>Forge Ecosystem Systems Manual</strong><br/>
  <sub>Boswell Digital Solutions LLC</sub><br/>
  <sub>© 2025 All Rights Reserved</sub>
</p>
