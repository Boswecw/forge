# §2 — Architecture

## Ecosystem Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    USER / OPERATOR                                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ UI actions (no secrets)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               ForgeCommand (Port 8003) — ROOT OF TRUST                  │
│               ForgeCommand API (Port 8004, local boundary)              │
│                                                                         │
│   SvelteKit UI ──IPC──▶ Rust Broker ──▶ Encrypted Vault                │
│   (no secrets)          (injects auth)   (~/.forge-command/local.db)    │
│                                                                         │
│   Orchestration · API Key Vault · Run Lifecycle · Health Monitoring     │
└──────────┬──────────────┬──────────────┬──────────────┬─────────────────┘
           │              │              │              │
           ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  NeuroForge  │ │  ForgeAgents │ │     Rake     │ │   Consumer   │
│   (8000)     │ │   (8010)     │ │   (8002)     │ │    Apps      │
│              │ │              │ │              │ │ SMITH, Vibe, │
│  5-stage     │ │  5-phase     │ │  5-stage     │ │ Author, etc  │
│  inference   │ │  agent loop  │ │  ingestion   │ │              │
│  pipeline    │ │  + BugCheck  │ │  pipeline    │ │  (no creds)  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                 ┌──────▼──────┐
                 │  DataForge  │
                 │   (8001)    │
                 │ Source of   │
                 │   Truth     │
                 └──────┬──────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
  ┌──────▼─────┐ ┌─────▼────┐ ┌──────▼─────┐
  │ PostgreSQL │ │  Redis   │ │  pgvector  │
  │   14+      │ │   6+     │ │  (ANN)     │
  └────────────┘ └──────────┘ └────────────┘
```

The diagram above covers the always-on service mesh. Forge Eval is intentionally outside that runtime topology because it is a standalone repository and CLI evaluator, not a resident network service.

### Trust Boundaries

| Boundary | Rule |
|----------|------|
| User → UI | No secrets cross this boundary |
| UI → Rust Backend | IPC operations only; Rust injects auth headers |
| ForgeCommand → Services | Authenticated HTTP; headers injected server-side |
| Services → DataForge | API key or run_token authentication |
| Consumer Apps → Services | No credential ownership; all calls brokered through ForgeCommand |
| Forge Eval → Target Repos | Read-only repository inspection for deterministic evaluation; target repos remain the evaluated subjects |
| Forge Eval → Governance / Persistence Layers | Artifact handoff only; no authority or durable-truth ownership |

---

## Forge Eval — Standalone Evaluation Plane

Forge Eval exists in its own repository at `/home/charlie/Forge/ecosystem/forge-eval`. It evaluates sibling repositories in the workspace and emits deterministic artifacts rather than serving requests.

```
Operator / CI
    │
    ▼
forge-eval CLI
    │
    ├── target repo checkout / diff range
    │
    └── canonical Pack J stage chain
         risk
           -> context slices
           -> reviewer findings
           -> telemetry matrix
           -> occupancy snapshot
           -> capture estimate
    │
    ▼
schema-locked local artifacts
```

### Forge Eval Stage Naming

The ecosystem reference uses human-readable narrative stage names for Pack J. Code-facing stage IDs and emitted artifact names remain snake_case.

| Narrative Stage | Stage / Artifact ID | Notes |
|-----------------|---------------------|-------|
| Risk | `risk_heatmap` / `risk_heatmap.json` | Canonical narrative name: `risk` |
| Context slices | `context_slices` / `context_slices.json` | Canonical narrative name: `context slices` |
| Reviewer findings | `review_findings` / `review_findings.json` | Ecosystem docs standardize on `reviewer findings`; some implementation paths may still use `reviewer_execution` naming internally |
| Telemetry matrix | `telemetry_matrix` / `telemetry_matrix.json` | Canonical narrative name: `telemetry matrix` |
| Occupancy snapshot | `occupancy_snapshot` / `occupancy_snapshot.json` | Canonical narrative name: `occupancy snapshot` |
| Capture estimate | `capture_estimate` / `capture_estimate.json` | Canonical narrative name: `capture estimate` |

### Forge Eval Boundary

- Forge Eval is standalone. It is not a child subsystem of NeuroForge, DataForge, or forge-smithy.
- Forge Eval evaluates sibling repositories and emits local evidence-oriented artifacts.
- Forge Eval does not make governance decisions. SMITH remains the authority layer for human-governed decisions.
- Forge Eval does not own durable persistence. DataForge remains the durable truth store when evaluation artifacts need to be retained beyond local execution.

### Eval Cal Node — Post-Implementation Calibration

Eval Cal Node is a separate standalone repository (`eval-cal-node/`) that operates downstream of both Forge Eval and reconciliation. It ingests three surfaces per implementation slice:

1. **Forge Eval A-M artifact chain** — what Eval said
2. **SYSTEM.md declared state** — what was documented
3. **Reconciliation findings** — what actually drifted or aligned

From these surfaces it computes bounded calibration proposals for 13 Eval parameters (hazard weights, merge thresholds, occupancy priors). The node uses a three-gate autonomy model:

- **Gate 1 (Sufficiency):** Autonomous — rejects weak or noisy signals
- **Gate 2 (Control Envelope):** Autonomous — rejects policy-violating proposals
- **Gate 3 (Math-Effect Boundary):** Human approval required

Eval Cal Node does not alter Forge Eval stage order, artifact contracts, fail-closed doctrine, or the current approved Eval parameter revision directly. It only emits candidate proposals.

---

## NeuroForge — 5-Stage Inference Pipeline

Every inference request traverses all five stages in sequence. There is no bypass.

```
Query
  │
  ▼
┌─────────────────────┐
│   Context Builder   │  ← Fetches RAG chunks from DataForge
│                     │    Circuit breaker + SQLite fallback
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Prompt Engine     │  ← Domain templates (literary|market|general)
│                     │    Task types: analysis|generation|reasoning|
└──────────┬──────────┘    classification|summarization|extraction
           │
           ▼
┌─────────────────────┐
│   Model Router      │  ← 4 strategies: CHAMPION_SELECTION, ENSEMBLE_VOTING,
│                     │    COST_OPTIMIZATION, QUALITY_OPTIMIZATION
└──────────┬──────────┘    Fallback chains: PREMIUM → STANDARD → FAST
           │
           ▼
┌─────────────────────┐
│     Evaluator       │  ← LLM-based quality scoring (0.0–1.0)
│                     │    Pass/fail gate before output release
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Post-Processor     │  ← Output normalization, DataForge persistence
└─────────────────────┘
           │
           ▼
        Response
```

### LLM Provider Hierarchy

| Tier | Models |
|------|--------|
| PREMIUM | Claude-Opus-4-6, GPT-4, Gemini 1.5 Pro, Grok-4 |
| STANDARD | Claude-Sonnet-4-6, GPT-4o, Gemini Pro, Grok-4-Fast |
| FAST | Claude-Haiku-4-5, GPT-4o-mini, Ollama/* |

Fallback chain on failure: `PREMIUM → STANDARD → FAST`. Governance-critical tasks require PREMIUM tier minimum and will not fall through to FAST.

### 3-Layer Prompt Cache

```
Incoming Request
      │
  L1: Redis (SHA-256 exact hash, ~1.5ms)
      │ miss
  L2: MinHash Pre-Screen (128 perms, Jaccard >85%)
      │ miss
  L3: Jaccard Similarity (95% token-level threshold)
      │ miss
  Full Pipeline Execution
```

Expected hit rate: 30%+. Cost reduction: 60-80% on cached prompts.

### Subsystems

| Subsystem | Purpose |
|-----------|---------|
| **RTCFX** | Real-Time Compilation & Feedback eXecution — governed learning from inference outcomes |
| **MAID** | Multi-AI Inference Deliberation — parallel multi-model consensus validation |
| **MAPO** | Multi-AI Planning Orchestration — sequential brainstorming across models |
| **Psychology** | 9 behavioral frameworks for user/team profiling |
| **Champion Model** | EMA-based empirical model selection per domain+task_type |

---

## DataForge — Hybrid Search & Persistence

Inventory counts in this section are current audited snapshot values. The storage boundary, hybrid search design, and truth ownership rules are canonical.

### Component Map

```
DataForge (port 8001)
│
├── FastAPI Application Layer
│   ├── 33 router registrations (current audited snapshot; 80+ endpoints)
│   ├── Lifespan handler (CORS, startup/shutdown)
│   └── Admin UI (Jinja2 template)
│
├── Business Logic Layer
│   ├── CRUD operations
│   ├── Hybrid search engine (semantic + BM25 + RRF)
│   ├── Embedding pipeline
│   ├── Auth (JWT, OAuth2, TOTP, API keys, scoped tokens)
│   └── Anomaly detection (6 threat patterns)
│
├── ORM Layer
│   ├── SQLAlchemy models (31+ classes)
│   └── Pydantic schemas (90+ schemas)
│
└── Storage Layer
    ├── PostgreSQL 14+ — primary relational store
    ├── pgvector — ANN index (IVFFlat, cosine)
    └── Redis 6+ — cache, rate limiting, sessions
```

### Hybrid Search Pipeline

```
Query Text
    │
    ├──► Embedding Model (Voyage AI) ──► 1536-dim vector ──► pgvector ANN (cosine)
    │
    └──► PostgreSQL TSVECTOR ──► BM25 ranking
                                      │
                Both result sets ──► Reciprocal Rank Fusion (RRF)
                                      │
                                 Merged + scored results
```

**RRF formula:** `RRF_score(d) = Σ 1/(k + rank_i(d))` where `k=60`. Measured improvement: +40% accuracy over pure semantic search.

### Execution Index Pattern

```
ForgeCommand creates run → ExecutionIndex (fast-path, no joins)
                               → RunEvidence (full JSONB blob)
                               → Domain-specific records (BugCheckRun, etc.)
```

### Resilience

| Layer | Strategy | Recovery |
|-------|----------|----------|
| PostgreSQL | Primary-replica + automated failover | < 30s |
| Redis | Sentinel-managed failover | < 10s |
| API | Load balancer + health checks | < 5s |
| Async tasks | Celery + DLQ, exponential backoff | 3 retries |

---

## Rake — 5-Stage Ingestion Pipeline

### Service Boundaries

```
ForgeCommand (orchestration) ──► Rake (port 8002) ──► DataForge (storage)
                                      │
                         ┌────────────┼────────────┐
                         │            │            │
                    NeuroForge    Tavily/Serper  Firecrawl
                    (strategy     (search)      (scraping)
                     curation)
```

### Pipeline Architecture

```
POST /api/v1/jobs → validate → create job record → queue BackgroundTask → 202

BackgroundTask:
  FETCH   → SourceAdapter (file|url|sec_edgar|api|database) → list[RawDocument]
  CLEAN   → text normalization, format conversion → list[CleanedDocument]
  CHUNK   → 3 strategies (token|semantic|hybrid) → list[Chunk]
  EMBED   → embedding model (OpenAI text-embedding-3-small) → list[Embedding]
  STORE   → DataForgeClient → persisted to DataForge → list[StoredDocument]
```

### Research Mission Lifecycle (11 states)

```
CREATED → STRATEGIZING → STRATEGY_REVIEW → APPROVED → DISCOVERING
→ CURATING → INGESTING → COMPLETING → COMPLETED
(+ FAILED, CANCELLED as terminal states)
```

Missions call NeuroForge for strategy generation and source curation. Cost is tracked per phase with budget enforcement via `cost_cap_usd`.

---

## ForgeAgents — Agent Execution Runtime

### Component Map

```
┌──────────────────────────────────────────────────────────────┐
│                     ForgeAgents :8010                         │
│                                                               │
│  FastAPI Routes  ·  Policy Engine (12 policies)               │
│  Memory Manager  ·  Tool Router (35 tools, 6 adapters)        │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         Agent Executor — 5-Phase Loop                     │ │
│  │    Plan → Act → Observe → Reflect → Decide                │ │
│  │         (max 10 iterations, 300s timeout)                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         35 Execution Nodes across 7 Tiers                  │ │
│  │  T0 Control · T1 Intelligence · T2 Specialist              │ │
│  │  T3 Verification · T4 Planning · T5 Integration · T6 Rel. │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────┬──────────────┬──────────────┬─────────────────────┘
           │              │              │
      DataForge      NeuroForge        Rake
      (SoT, mem)    (LLM, embed)    (async jobs)
```

### Policy Engine (4 categories, 12 policies)

| Category | Policies |
|----------|----------|
| **Safety** (5) | DestructiveAction, Confirmation, ContentSafety, FileSystemSafety, HealingScope |
| **Domain** (4) | ToolAccess, DataAccess, ScopeRestriction, Permission |
| **Resource** (3) | RateLimit (60/min), Quota, CostTracking ($10/day max) |

Enforcement order: Safety → Domain → Resource. All tool calls are pre-authorized.

### Memory Architecture

| Tier | Storage | Capacity | TTL |
|------|---------|----------|-----|
| Short-term | In-memory FIFO | 100 items/agent | Run lifetime |
| Long-term | DataForge PostgreSQL + pgvector | Unlimited | Indefinite |
| Episodic | DataForge timeline log | Unlimited | 90 days |

### 6 Reference Agent Archetypes

| Agent | Role | Key Tools |
|-------|------|-----------|
| Writer | General tasks | Read-only tools |
| Coder | Code generation, refactoring | `write_file` |
| Analyst | Data analysis, reporting | DataForge queries |
| Researcher | Information gathering | Semantic search |
| Coordinator | Multi-agent orchestration | All tools |
| Ecosystem | Cross-repo infrastructure | 12 specialized ecosystem tools |
| Sentinel | Health monitoring + self-healing | health_sweep, breaker_probe_reset |

### BugCheck Agent

Ecosystem-wide quality enforcement. Runs static analysis, type checks, linting, tests, security scans, and cross-service contract validation across all Forge services. Findings follow a governed lifecycle state machine (NEW → TRIAGED → FIX_PROPOSED → APPROVED → APPLIED → VERIFIED → CLOSED / DISMISSED).

### Sentinel Agent

Ecosystem-wide health monitoring and autonomous healing. Specialization of the Ecosystem archetype. Runs 6 diagnostic dimensions (D1 Liveness, D2 Connectivity, D3 Circuit Breakers, D4 Degradation, D5 Config Coherence, D6 Token Authority) in light sweeps (D1+D3+D6, every 5 min) or deep sweeps (all D1-D6, on-demand). Healing actions are tiered: A (autonomous — cache flush, breaker reset, job retry), B (supervised — requires ForgeCommand approval), C (escalation only). HealingScopePolicy enforces tier boundaries with cooldowns and frequency limits (3 autonomous actions/hour). All sweep results and healing events persisted to DataForge.

---

## Cross-Service Data Flow

### End-to-End Knowledge Ingestion

```
1. Rake FETCHES raw documents from diverse sources
2. Rake CLEANs, CHUNKs, EMBEDs documents
3. Rake STOREs embeddings to DataForge
4. NeuroForge QUERIEs DataForge for RAG context
5. NeuroForge INFERs using LLM providers
6. NeuroForge PERSISTs provenance to DataForge
7. ForgeAgents CONSUMEs inference results for agent tasks
```

### End-to-End Quality Check (BugCheck)

```
1. ForgeCommand creates run record, issues run_token
2. ForgeAgents/BugCheck detects service stacks
3. BugCheck runs checks (typecheck, lint, tests, security, contracts)
4. Findings written to DataForge (requires run_token)
5. Findings routed to XAI (context) and MAID (fix proposals) via NeuroForge
6. Enriched findings persisted to DataForge
7. ForgeCommand finalizes run (immutable after FINALIZED)
```

---

*For per-service architecture deep dives, see each service's own `doc/system/` architecture chapter. For tech stack details, see §3. For backend internals, see §9.*
