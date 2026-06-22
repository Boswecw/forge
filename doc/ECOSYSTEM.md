        # Forge Ecosystem - Compiled System Reference

        **Designation:** ECO
        **Document role:** Canonical compiled technical reference for the Forge ecosystem parent repo
        **Source:** `doc/system/`
        **Build command:** `bash doc/system/BUILD.sh`
        **Document version:** 2.0 (2026-06-22) - canonical compliance migration
        **Protocol:** BDS Documentation Protocol v2.0; BDS Repo Documentation System Canonical Compliance Standard

        > **Generated artifact warning:** `doc/ECOSYSTEM.md` is assembled output. Edit
        > the source modules under `doc/system/` and rebuild. Hand edits to the
        > compiled artifact are overwritten by the next build.

        Assembly contract:

        - Command: `bash doc/system/BUILD.sh`
        - Validation: `bash doc/system/validate_snapshots.sh` runs during assembly
        - Primary output: `doc/ECOSYSTEM.md`

        This `doc/system/` tree is the canonical source of truth for the Forge ecosystem parent repo. It uses
        explicit **truth classes**: canonical facts define ecosystem role, service
        boundaries, contract behavior, runtime behavior, and verification doctrine;
        snapshot facts are dated, audit-derived counts and current implementation
        inventory that may drift between audits.

        | Part | File | Contents |
        | --- | --- | --- |
        | §1 | `00_overview/00-overview.md` | §1 — Overview & Philosophy |
| §2 | `00_overview/01-architecture.md` | §2 — Architecture |
| §3 | `10_service-contract/10-product-surface.md` | Product Surface |
| §4 | `20_runtime/20-runtime.md` | Runtime |
| §5 | `20_runtime/30-data.md` | §11 — Database Schema |
| §6 | `30_dependencies/40-integrations.md` | Integrations |
| §7 | `40_governance/40-governance.md` | Governance |
| §8 | `50_operations/50-operations.md` | Operations |
| §9 | `99_appendices/90-appendices.md` | Appendices |

        ## Quick Assembly

        ```bash
        bash doc/system/BUILD.sh
        ```

---

# §1 — Overview & Philosophy

## Ecosystem Identity

The **Forge Ecosystem** is internal AI engineering infrastructure. It is a governed system for designing, operating, and verifying AI-assisted and AI-mediated systems over time.

Forge treats the following as first-class operational actors: code, models (local and hosted), prompts, agents, pipelines, and automation. These actors are expected to evolve, drift, and interact in non-trivial ways. Forge exists to keep those interactions **governable, inspectable, attributable, and correct** over time.

---

## Core Operational Subsystems

| Subsystem | Port / Mode | Language | Role | Durable State |
|-----------|-------------|----------|------|---------------|
| **NeuroForge** | 8000 | Python 3.11+ / FastAPI | AI inference orchestration — LLM intelligence layer | None — processing node only |
| **DataForge** | 8001 | Python 3.11+ / FastAPI | Single source of truth — all durable state persistence | PostgreSQL + pgvector + Redis |
| **Rake** | 8002 | Python 3.11+ / FastAPI | Data ingestion pipeline — fetch, clean, chunk, embed, store | None — pipeline processor only |
| **ForgeAgents** | 8010 | Python 3.11+ / FastAPI | AI agent runtime — stateless agent orchestration | None — ephemeral execution only |
| **forge-smithy** | Desktop application | Tauri 2.0 + Svelte 5 | Governance workbench and authority UI | Local workstation state only; not canonical truth |
| **Forge Eval** | CLI / local repo execution | Python 3.12 + stable Rust | Standalone deterministic evaluation of sibling repositories through Pack J | Local schema-locked artifacts only; not canonical truth |

### Supporting Infrastructure

| Component | Role |
|-----------|------|
| **ForgeCommand** (8003) | Desktop orchestration layer — API key vault, run lifecycle management |
| **PostgreSQL 14+** | Primary relational store with pgvector extension for ANN search |
| **Redis 6+** | Caching layer (L1 prompt cache, session store, task queues) |

---

## Canonical Doctrine

The following principles are drawn from the [Forge Ecosystem Canonical Reference](../../docs/canonical/ecosystem_canonical.md) and have authority over all service-level documentation.

### DataForge is the Single Source of Truth

Every service that produces durable state writes to DataForge. This is a non-negotiable architectural invariant:

- **NeuroForge** writes inference records, model performance metrics, and provenance.
- **ForgeAgents / BugCheck** writes findings, lifecycle events, enrichment artifacts, and progress events.
- **Rake** writes job records, mission state, stored documents, and embeddings (via DataForge).
- **ForgeCommand** writes run records, lifecycle transitions, and finalization states.

No service maintains a local truth cache. No service treats its own database as canonical. **If DataForge is unavailable, runs do not start. This is by design.**

Forge Eval is the current exception by design because it is not a durable truth owner or an always-on service. It emits local deterministic evaluation artifacts such as `risk_heatmap.json`, `context_slices.json`, `review_findings.json`, `telemetry_matrix.json`, `occupancy_snapshot.json`, and `capture_estimate.json`. Those artifacts may later be reviewed by SMITH or persisted by DataForge, but Forge Eval itself is not the record.

### Intent → Execution → Evidence

All meaningful system behavior follows this chain:

1. **Intent** — human-defined doctrine, rules, and contracts
2. **Execution** — code, agents, models, and pipelines performing work
3. **Evidence** — immutable artifacts proving what occurred

Evidence is the only acceptable source of truth. If evidence does not exist, the event is treated as non-existent.

### Governance is Infrastructure

Governance in Forge is **implemented**, not aspirational. Doctrine validation is enforced by tooling. Ecosystem verification is executed by runners. Violations and outcomes are recorded as evidence. Policy documents without enforcement mechanisms are considered non-operational.

### Human Authority

Forge is explicitly **human-authoritative**. Humans define doctrine and constraints, approve changes, and accept or reject risk. AI systems may recommend, generate, or execute — but they do not decide what is acceptable.

### Fail Fast, Degrade Explicitly

Ambiguous states are not tolerated. When an invariant is violated, the system faults immediately and logs a structured security event. When external dependencies are unavailable, the system continues with reduced functionality but annotates all affected outputs with a degradation flag. Silent fallbacks are banned.

---

## Service Philosophies

### NeuroForge — Inference Pipeline First

Every request follows the same 5-stage pipeline: Context Builder → Prompt Engine → Model Router → Evaluator → Post-Processor. No endpoint bypasses the pipeline. NeuroForge supports five LLM providers (OpenAI, Anthropic, Google, XAI, Ollama) with empirical champion selection and automatic fallback chains. Cost is a first-class constraint — batch APIs, prompt caching, and a 3-layer semantic cache are core to the design.

NeuroForge does not store knowledge. It fetches, contextualizes, infers, evaluates, and returns.

### DataForge — The Truth Engine

DataForge is not a cache, not a secondary store, not a convenience API. It exposes a broad multi-router API surface for persistence, search, authentication, and domain services. It provides hybrid search combining cosine similarity with BM25 keyword scoring via Reciprocal Rank Fusion (+40% accuracy over pure semantic search). It manages the full auth stack (JWT, OAuth2/OIDC, TOTP 2FA, API keys, scoped tokens). An append-only, HMAC-SHA256-signed audit log captures all significant events.

DataForge enforces lifecycle state machines at the API level. Invalid transitions return 409 Conflict. These are invariants, not policies.

### Rake — Pipeline Clarity

Every document follows a strict 5-stage path: FETCH → CLEAN → CHUNK → EMBED → STORE. Each stage has an explicit input type, output type, and failure mode. There are no short-circuit paths. After the FETCH stage, all sources are treated uniformly — whether a document came from a PDF, a website, an SEC filing, an API, or a database query. Rake also orchestrates multi-phase research missions with cost-capped budgets.

Rake does not own vector storage, does not generate AI responses, and does not manage API keys.

### ForgeAgents — Stateless Agents, Governed Execution

ForgeAgents holds no durable truth. Every piece of state that must survive beyond the lifetime of an execution is written to DataForge. The system ships six reference agent archetypes (Writer, Coder, Analyst, Researcher, Coordinator, Ecosystem) and the BugCheck quality enforcement agent. Every agent execution flows through a policy engine before a single tool call is made — safety policies before domain policies, domain policies before resource policies.

ForgeAgents may never write lifecycle transitions. Only ForgeCommand owns lifecycle state.

### Forge Eval — Deterministic Evaluation Substrate

Forge Eval is a standalone repository under `/home/charlie/Forge/ecosystem/forge-eval`. It evaluates sibling repositories rather than serving traffic. Its current implemented pipeline runs through Pack J:

```text
risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate
```

Forge Eval is intentionally narrow. It computes deterministic, schema-locked, fail-closed evaluation artifacts with byte-stable output on identical input. It does not own governance authority, and it does not replace DataForge as the durable record.

---

## What Forge Is Not

- Not a traditional software development framework
- Not a consumer-facing application platform
- Not a "move fast and fix later" environment
- Not a system optimized for developer convenience over correctness

Velocity is allowed. **Unbounded velocity is not.**

---

## Ecosystem Data Flow

```
                         ForgeCommand (8003)
                    Orchestration + API Key Vault
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
     ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
     │ ForgeAgents│     │ NeuroForge│     │   Rake    │
     │   (8010)   │     │  (8000)   │     │  (8002)   │
     │  Agents +  │     │ Inference │     │ Ingestion │
     │  BugCheck  │     │ + MAID    │     │ Pipeline  │
     └─────┬──────┘     └─────┬─────┘     └─────┬─────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                       ┌──────▼──────┐
                       │  DataForge  │
                       │   (8001)    │
                       │   Source    │
                       │  of Truth   │
                       └──────┬──────┘
                              │
               ┌──────────────┼──────────────┐
               │              │              │
        ┌──────▼─────┐ ┌─────▼────┐ ┌──────▼─────┐
        │ PostgreSQL  │ │  Redis   │ │  pgvector  │
        │  (primary)  │ │ (cache)  │ │   (ANN)    │
        └─────────────┘ └──────────┘ └────────────┘
```

### Ecosystem Evaluation Flow (Forge Eval)

```
Operator / CI
      │
      ▼
forge-eval (standalone repo / CLI)
      │
      ├── reads sibling target repo state (git diff + file content)
      ├── computes: risk -> slices -> findings -> telemetry -> occupancy -> capture
      └── emits schema-locked local artifacts
              │
              ├── may later inform SMITH governance decisions
              └── may later be persisted by DataForge if governance/runtime wiring requires it
```

---

## Quality Commitments

Canonical targets:

| Metric | Service | Target |
|--------|---------|--------|
| Prompt cache hit rate | NeuroForge | 30%+ |
| Cost reduction (batch + cache) | NeuroForge | 50-80% |
| API latency (p95) | DataForge | < 100ms |
| Throughput | DataForge | 1,000+ RPS |
| Uptime SLA | DataForge | 99.99% |
| Artifact repeatability | Forge Eval | Byte-identical outputs on identical inputs |
| Artifact validation | Forge Eval | Schema-valid, fail-closed stage outputs |

Current audited coverage and test totals are snapshot facts rather than doctrine. They are tracked in §14.

---

*For canonical doctrine details, see the [Forge Ecosystem Canonical Reference](../../docs/canonical/ecosystem_canonical.md).*

*For per-service deep dives, see each service's own `doc/system/` overview chapter. For architecture, see §2. For project structure, see §4.*

---

---

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

---

---

# Product Surface

**Document version:** 1.0 (bootstrap scaffold)

User-facing product surface: routes, flows, and entry points.

> This chapter is a registry-generated bootstrap scaffold for a
> `application` class documentation system. Replace this placeholder with
> real authored content. Registry will not invent repo truth that is not
> already present in the repo.

---

# Runtime

**Document version:** 1.0 (bootstrap scaffold)

Runtime topology, process boundaries, and managed state.

> This chapter is a registry-generated bootstrap scaffold for a
> `application` class documentation system. Replace this placeholder with
> real authored content. Registry will not invent repo truth that is not
> already present in the repo.

---

# §11 — Database Schema

## Schema Overview

The Forge ecosystem stores all durable state in **PostgreSQL** (DataForge, production) with **SQLite** as a development fallback (Rake). DataForge is the single source of truth — no other service persists authoritative data.

Snapshot counts below reflect the current checked-in model/schema surface and will evolve with the codebase.

| Metric | Count |
|--------|-------|
| ORM-mapped tables | 118 |
| Association tables | 3 |
| Pydantic pipeline DTOs | 30+ (Rake) |
| ForgeAgents JSON schemas | 23 |
| Model source files | 47 (DataForge) + 6 (Rake) |

### Database Stack

| Layer | Technology |
|-------|-----------|
| RDBMS | PostgreSQL 16 (production) |
| Vector search | pgvector (IVFFlat index, cosine distance) |
| Full-text search | PostgreSQL TSVECTOR + GIN index |
| ORM | SQLAlchemy 2.0 (async: `asyncpg` for PG, `aiosqlite` for SQLite) |
| Migrations | Alembic |
| Schema validation | Pydantic v2 |
| JSON storage | JSONB (indexed) and JSON (unindexed) columns |

---

## DataForge — Core Tables

### `users`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | PK |
| `username` | String(50) | NOT NULL, UNIQUE |
| `email` | String(255) | NOT NULL, UNIQUE |
| `hashed_password` | String(255) | NOT NULL |
| `is_active` | Boolean | default=True |
| `is_admin` | Boolean | default=False |
| `created_at` | DateTime(tz) | server_default=now() |
| `updated_at` | DateTime(tz) | onupdate=now() |

### `domains`

Self-referential hierarchy for knowledge organization.

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | String(100) | PK (e.g., "writing_craft") |
| `label` | String(255) | NOT NULL |
| `description` | Text | nullable |
| `parent_id` | String(100) | FK → domains.id ON DELETE SET NULL |
| `created_at` / `updated_at` | DateTime(tz) | auto-managed |

### `documents`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | PK |
| `domain_id` | String(100) | FK → domains.id ON DELETE CASCADE, indexed |
| `title` | String(500) | NOT NULL |
| `doc_type` | String(50) | NOT NULL (guide/pattern/example/reference), indexed |
| `content` | Text | NOT NULL |
| `doc_metadata` | Text | nullable (JSON string) |
| `is_published` | Boolean | default=True, indexed |
| `created_at` / `updated_at` | DateTime(tz) | auto-managed |

### `chunks` — Vector + Full-Text Search

The only table with both **pgvector** and **TSVECTOR** columns. This is the core of DataForge's hybrid search engine (see §9).

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | PK |
| `document_id` | Integer | FK → documents.id ON DELETE CASCADE |
| `content` | Text | NOT NULL |
| `chunk_index` | Integer | NOT NULL (order within document) |
| `embedding` | **Vector(1536)** | nullable — pgvector, 1536-dim (Voyage AI / OpenAI) |
| `search_vector` | **TSVECTOR** | nullable — maintained by DB trigger for BM25 search |
| `created_at` | DateTime(tz) | server_default=now() |

**Indexes:** IVFFlat on `embedding` (cosine distance), GIN on `search_vector`.

### `tags` + `document_tags`

| Table | Columns | Notes |
|-------|---------|-------|
| `tags` | `id` (PK), `name` (UNIQUE) | Tag vocabulary |
| `document_tags` | `document_id` FK, `tag_id` FK | M2M join table, CASCADE delete |

---

## DataForge — Execution & Evidence

### `execution_index`

Denormalized run index for sub-millisecond status lookups (no joins required).

| Column | Type | Constraints |
|--------|------|-------------|
| `run_id` | String(64) | PK |
| `trace_id` | String(64) | NOT NULL, indexed |
| `workflow_id` | String(64) | NOT NULL, indexed |
| `session_id` | String(64) | NOT NULL, indexed |
| `repo_id` | String(255) | NOT NULL, indexed |
| `repo_sha` | String(64) | NOT NULL |
| `branch` | String(255) | NOT NULL, indexed |
| `mode` | String(20) | NOT NULL (batch/interactive) |
| `final_status` | String(20) | NOT NULL, indexed (CHECK constraint: 4-value vocabulary) |
| `promotion_ready` | Boolean | default=False, indexed |
| `confidence_floor` | Float | default=0.0 |
| `evidence_hash` | String(71) | nullable (sha256:... prefix) |
| `run_metadata` | **JSONB** | nullable — extensible metadata |
| `created_at` | DateTime(tz) | server_default=now(), indexed |
| `completed_at` | DateTime(tz) | nullable |

**Composite indexes:** `(repo_id, branch)`, `(workflow_id, final_status)`, `(session_id, created_at)`.

### `run_evidence`

| Column | Type | Constraints |
|--------|------|-------------|
| `run_id` | String(64) | PK, FK → execution_index.run_id ON DELETE CASCADE |
| `evidence_version` | String(20) | NOT NULL, default="RunEvidence.v1" |
| `evidence_hash` | String(71) | NOT NULL (SHA-256 integrity hash) |
| `evidence` | **JSONB** | NOT NULL — full RunEvidence.v1 document |
| `created_at` | DateTime(tz) | server_default=now() |

### `agent_registry`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | String(36) | PK (UUID) |
| `name` | String(100) | NOT NULL, UNIQUE |
| `agent_type` | String(20) | NOT NULL (researcher/analyst/writer/etc.), indexed |
| `status` | String(20) | NOT NULL, default="idle", indexed |
| `agent_data` | **JSONB** | NOT NULL — full agent definition (config, memory, policy, stats) |
| `created_at` / `updated_at` | DateTime(tz) | auto-managed |

---

## DataForge — BugCheck Tables

5 tables for the BugCheck quality enforcement subsystem. All use native PostgreSQL UUID primary keys.

### `bugcheck_runs`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | UUID | PK, default=uuid4 |
| `run_type` | String(50) | NOT NULL (service_run/ecosystem_run/workflow_run) |
| `targets` | JSON | NOT NULL (list of service names) |
| `mode` | String(20) | NOT NULL (quick/standard/deep) |
| `scope` | String(30) | NOT NULL (changed_files/package/full_repo) |
| `commit_sha` | String(40) | NOT NULL |
| `status` | String(20) | NOT NULL, default="pending" |
| `severity_counts` | JSON | NOT NULL |
| `gating_result` | String(20) | NOT NULL, default="pending" |
| `is_baseline` | Boolean | default=False |
| `started_at` | DateTime | NOT NULL |
| `completed_at` | DateTime | nullable |

**Key constraint:** After status=FINALIZED, no new findings accepted (enforced at API level — 409 Conflict).

### `bugcheck_findings`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | UUID | PK |
| `run_id` | UUID | FK → bugcheck_runs.id ON DELETE CASCADE |
| `fingerprint` | String(64) | NOT NULL, indexed (stable across runs) |
| `severity` | String(5) | NOT NULL (S0/S1/S2/S3/S4) |
| `category` | String(30) | NOT NULL (security/performance/test/contract/lint/dependency/migration) |
| `confidence` | Float | NOT NULL (0.0-1.0) |
| `title` | String(200) | NOT NULL |
| `description` | Text | NOT NULL |
| `location` | JSON | NOT NULL (service, file_path, line_start, line_end, function) |
| `lifecycle_state` | String(20) | NOT NULL, default="NEW" |
| `provenance` | String(100) | NOT NULL (which check produced this) |
| `created_at` | DateTime | NOT NULL |

### `bugcheck_enrichments`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | UUID | PK |
| `finding_id` | UUID | FK → bugcheck_findings.id ON DELETE CASCADE |
| `source` | String(20) | NOT NULL (maid/xai) |
| `enrichment_type` | String(50) | nullable |
| `content` | JSON | NOT NULL |
| `confidence` | Float | nullable |
| `status` | String(20) | NOT NULL, default="pending" |
| `model_used` | String(100) | nullable |
| `tokens_used` | Integer | nullable |

### `bugcheck_lifecycle_events`

Append-only audit trail for finding state transitions.

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | UUID | PK |
| `finding_id` | UUID | FK → bugcheck_findings.id ON DELETE CASCADE |
| `from_state` / `to_state` | String(20) | NOT NULL |
| `actor_type` | String(20) | NOT NULL (user/system/agent/automation) |
| `actor_id` | String(255) | NOT NULL |
| `reason` | Text | nullable |
| `scope` | String(30) | nullable (for dismissals) |
| `expires_at` | DateTime | nullable (for dismissals) |
| `timestamp` | DateTime | NOT NULL |

### `bugcheck_progress`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | UUID | PK |
| `run_id` | UUID | FK → bugcheck_runs.id ON DELETE CASCADE |
| `event_type` | String(50) | NOT NULL |
| `message` | Text | NOT NULL |
| `timestamp` | DateTime | NOT NULL |

---

## DataForge — Domain-Specific Tables

### AuthorForge v1 (6 tables)

| Table | PK | Key Columns | Notable |
|-------|----|-------------|---------|
| `projects` | Integer | user_id FK, name, status (enum), word_count, settings (JSON) | Cascades to 10+ child tables |
| `manuscripts` | Integer | project_id FK, chapter_number, scene_number, content, status | Draft/revision/final lifecycle |
| `characters` | Integer | project_id FK, name, role, profile (JSON), personality (JSON), arc_data (JSON) | Rich JSON payload per character |
| `locations` | Integer | project_id FK, name, location_type, details (JSON) | Geography, climate, culture |
| `story_arcs` | Integer | project_id FK, name, arc_type, beats (JSON), graph_data (JSON) | Tension curve data |
| `brainstorm_sessions` | Integer | user_id FK, project_id FK, genre (enum), ideas (JSON) | AI-generated story ideas |

Plus `project_genres` association table (project_id + GenreEnum composite PK).

### AuthorForge v2 / Spec v3 (21 tables)

Extends v1 with structured chapters, knowledge graph, world maps, collaboration, and style profiles.

| Table Group | Tables | Key Features |
|-------------|--------|-------------|
| **Narrative** | `chapters`, `scenes` | sort_order, content_html, SceneStatus enum |
| **Knowledge Graph** | `lore_entities`, `lore_edges` | EntityKind enum (8 types), EdgeType enum (6 types) |
| **Story Structure** | `arcs`, `beats` | Beat intensity (0.0-1.0), scene links |
| **World Maps** | `map_nodes`, `map_edges`, `map_edge_modifiers`, `map_regions`, `map_settings`, `map_viewports`, `map_exports` | x/y coords, biome, SVG path data, viewport crops |
| **Lore** | `lore_pins`, `character_knowledge`, `journeys` | Knowledge types (visited/heard_of/rumored), proof_hash |
| **Collaboration** | `collab_rooms`, `collab_snapshots`, `collab_tokens` | Y.js binary snapshots (`LargeBinary`), token_hash |
| **Style** | `style_profiles` | Self-referential hierarchy, JSON rules |
| **Assets** | `assets` | AssetSourceType (upload/ai_generated/url), cdn_url |
| **Quality** | `consistency_alerts`, `factions`, `covers` | Tier 1-3 alerts, print specs (trim, spine, layers) |

### VibeForge (5 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `vibeforge_projects` | project_type (enum), selected_stack, complexity_score | Tech stack selection projects |
| `project_sessions` | 15+ JSON tracking columns, llm_queries/tokens, feedback_rating | Session-level analytics |
| `stack_outcomes` | outcome_status (enum), build/test/deploy booleans, satisfaction | Stack performance tracking |
| `model_performance` | provider, model_name, prompt_type, experiment_id, variant | A/B test tracking |
| `language_preferences` | times_selected/viewed/considered, paired_with_* (JSON) | Per-user language affinity |

### Teams (7 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `teams` | slug (UNIQUE), organization_type, denormalized member/project counts | Team identity |
| `team_members` | team_id + user_id (UNIQUE composite), role (enum), is_active | M2M with metadata |
| `team_invites` | invite_token (UNIQUE), role, status (enum), expires_at | Invitation flow |
| `team_projects` | team_id + project_id (UNIQUE composite), visibility | Project-team linkage |
| `team_learning_aggregates` | 20+ JSON/Float aggregate columns, period_start/end | Analytics rollups |
| `team_insights` | insight_type, priority, confidence_score, actionable_steps (JSON) | AI-generated insights |

### Due Diligence (3 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `diligence_projects` | git_url, current_health_status (enum) | Code review targets |
| `diligence_reviews` | 5 score columns (code/security/architecture/operations/docs), overall_rating | Multi-dimension scoring |
| `diligence_findings` | severity (enum), status (enum), file_path, line_number, remediation | Actionable findings |

### Multi-AI Planning (3 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `planning_outcomes` | stages (JSON array), total_cost_cents, execution_success | Planning session outcomes |
| `planning_model_performance` | model, provider, stage_type, EMA columns | Champion model tracking |
| `ai_estimation_feedback` | estimated_minutes, actual_minutes, accuracy_ratio | Estimation calibration |

### Prompt Run History (2 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `runs` | workspace_id, prompt_snapshot, total_cost_usd, tags (JSON) | Inference run history |
| `model_results` | run_id FK, model_id, provider, cost_usd, latency_ms | Per-model results |

**Note:** `runs` table is documented for potential TimescaleDB hypertable conversion in production.

### BuildGuard (2 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `buildguard_events` | verdict_id (UNIQUE), pass_status, severity counts, profile_hash | Quality gate verdicts |
| `buildguard_profile_stats` | profile_hash (PK), pass/fail counts, avg_triage_lag | Profile-level aggregates |

### NeuroForge (1 table)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `inferences` | domain, task_type, model_id, evaluation_score, latency_ms | Inference telemetry |

### Smithy Portfolio (3 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `smithy_portfolio_projects` | slug (UNIQUE), stack (`ARRAY(String)`) | Portfolio projects |
| `smithy_evaluation_snapshots` | template_snapshot (JSONB), answers (JSONB), evidence (JSONB) | Evaluation checkpoints |
| `smithy_evidence_items` | kind (link/file/image/snippet), url, snippet | Evidence artifacts |

### Smithy Planning (3 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `smithy_planning_sessions` | status (enum), current_stage (PAORTStage), stage_*_output (JSONB) | PAORT planning sessions |
| `smithy_planning_deliverables` | plan_title, execution_prompt, plan_risks (`ARRAY(String)`) | Session deliverables |
| `smithy_planning_steps` | step_order, dependencies (`ARRAY(String)`), acceptance_criteria | Plan steps |

### Tarcie (1 table)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `tarcie_events` | device_id (UUID), event_type (Note/Marker), content | Append-only event log |

### Sentinel (2 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `sentinel_sweeps` | sweep_type (light/deep), status (running/completed/failed), overall_status (healthy/degraded/critical/unknown), dimensions_checked (JSONB), findings (JSONB), trigger (scheduled/manual/anomaly), duration_ms | Health sweep records |
| `sentinel_healing_events` | sweep_id FK, playbook, tier (A/B/C), action, target_service, outcome (pending/success/failure/escalated/skipped), governed (bool), approval_id, details (JSONB), duration_ms | Healing action records with autonomy tier |

Both tables use PostgreSQL native UUID primary keys. `sentinel_healing_events` cascades on `sentinel_sweeps` deletion. Check constraints enforce enum values for `sweep_type`, `status`, `overall_status`, `tier`, and `outcome`.

### Multi-Provider Pipeline (6 tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `model_catalog` | provider, model_id, tier (budget/workhorse/flagship), costs, capabilities | 14-model registry |
| `pricing_snapshots` | model_id FK, input/output/batch costs, captured_at, source | Point-in-time pricing |
| `pricing_alerts` | model_id FK, alert_type, severity, acknowledged | Price change alerts |
| `pricing_monitor_runs` | status, models_checked, alerts_generated | Monitor agent runs |
| `cost_ledger` | run_id, model_id, provider, input/output tokens, cost_usd | Per-inference cost records |
| `batch_queue` | batch_id, provider, model_id, status, items_count, cost_usd | Batch inference tracking |

---

## Rake — ORM Tables

Rake uses 2 SQLAlchemy ORM tables plus extensive Pydantic pipeline DTOs.

### `jobs`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | PK, autoincrement |
| `job_id` | String(64) | UNIQUE, NOT NULL, indexed |
| `correlation_id` | String(64) | nullable, indexed |
| `source` | String(50) | NOT NULL, indexed |
| `status` | Enum(JobStatus) | NOT NULL, default=PENDING, indexed |
| `tenant_id` | String(64) | nullable, indexed |
| `documents_stored` | Integer | nullable |
| `chunks_created` | Integer | nullable |
| `embeddings_generated` | Integer | nullable |
| `stages_completed` | JSON | nullable, default=[] |
| `source_params` | JSON | nullable, default={} |
| `created_at` | DateTime | NOT NULL, indexed |
| `completed_at` | DateTime | nullable |

**Composite indexes:** `(tenant_id, status)`, `(tenant_id, created_at)`, `(status, created_at)`.

**JobStatus enum:** PENDING → FETCHING → CLEANING → CHUNKING → EMBEDDING → STORING → COMPLETED / FAILED / CANCELLED.

### `missions`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | PK, autoincrement |
| `mission_id` | String(64) | UNIQUE, NOT NULL, indexed |
| `correlation_id` | String(64) | NOT NULL, indexed |
| `topic` | Text | NOT NULL |
| `state` | Enum(MissionState) | NOT NULL, default=CREATED, indexed |
| `tenant_id` | String(64) | NOT NULL, indexed |
| `strategy_data` | JSON | nullable |
| `discovered_urls` | JSON | nullable, default=[] |
| `curation_data` | JSON | nullable |
| `ingestion_job_ids` | JSON | nullable, default=[] |
| `constraints_data` | JSON | NOT NULL |
| `cost_search_usd` / `cost_scrape_usd` / `cost_embedding_usd` / `cost_llm_usd` | Float | NOT NULL, default=0.0 |
| `evidence_bundle` | JSON | nullable |
| `source_pipeline_status` | JSON | nullable, default=[] |
| `budget_exceeded` | Boolean | NOT NULL, default=False |
| `created_at` / `updated_at` | DateTime | NOT NULL, auto-managed |

**MissionState enum:** CREATED → STRATEGIZING → STRATEGY_REVIEW → APPROVED → DISCOVERING → CURATING → INGESTING → COMPLETING → COMPLETED (+ FAILED, CANCELLED).

**Composite indexes:** `(tenant_id, state)`, `(tenant_id, created_at)`, `(state, created_at)`.

---

## Rake — Pipeline DTOs (Pydantic)

Rake's 5-stage pipeline uses Pydantic models as stage-to-stage data transfer objects. These are not persisted to Rake's own database — the final output (embeddings + chunks) is written to **DataForge**.

```
RawDocument → CleanedDocument → Chunk → Embedding → StoredDocument
  (FETCH)       (CLEAN)        (CHUNK)  (EMBED)      (STORE → DataForge)
```

| DTO | Stage Output | Key Fields |
|-----|-------------|------------|
| `RawDocument` | FETCH | id, source (enum), url, content, metadata, tenant_id |
| `CleanedDocument` | CLEAN | id, content, word_count, char_count |
| `Chunk` | CHUNK | id, document_id, content, position, token_count, start_char/end_char |
| `Embedding` | EMBED | id, chunk_id, vector (List[float], 1536-dim), model |
| `StoredDocument` | STORE | id, chunk_count, embedding_count, status |
| `PipelineJob` | Tracker | job_id, document_id, status, current_stage, retry_count |

### Research Contract Models (`research_models.py`)

Canonical contract shared between Rake and NeuroForge for research missions:

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `ResearchStrategy` | NeuroForge-generated search plan | search_queries[], quality_rubric, domain_strategy, estimated_cost_usd |
| `CurationResult` | NeuroForge source evaluation | curated_urls[], rejected_urls[], duplicates_found |
| `MissionConstraints` | User-defined mission bounds | max_sources, cost_cap_usd (0.01-50.0), depth (enum), recency |
| `SourcePipelineStatus` | Per-source progress tracking | source_url, stage (enum), chunks_created, error_message |
| `MissionEvidenceBundle` | SHA-256 integrity bundle | strategy_hash, discovery_hash, curation_hash, sources_hash |

---

## ForgeAgents — JSON Schema Definitions

ForgeAgents uses JSON Schema files (not ORM tables) for cross-service contract enforcement. Stored in `schemas/bugcheck/`.

| Schema | Purpose | Key Properties |
|--------|---------|---------------|
| `bugcheck_run.schema.json` | Run definition contract | run_id, run_type, targets[], mode, scope, commit_sha, status |
| `finding.schema.json` | Finding payload contract | finding_id, fingerprint, severity (S0-S4), category, confidence, location |
| `enrichment.schema.json` | AI enrichment contract | source (maid/xai), content, confidence, model_used |
| `lifecycle_event.schema.json` | State transition contract | from_state, to_state, actor_type, reason |
| `run_token.schema.json` | Run authorization token | run_id, targets[], mode, scope, nonce, expires_at |
| `user_token.schema.json` | User authorization token | user_id, permissions[], expires_at |
| `service.manifest.schema.json` | Service topology | service_name, health_url, stacks[], dependencies[] |

---

## Shared Schema Patterns

### Multi-Tenancy

All tables with external-facing data include `tenant_id` columns. Composite indexes on `(tenant_id, status)` and `(tenant_id, created_at)` are standard.

### Audit Timestamps

Every table includes `created_at` (server_default=now()). Mutable tables add `updated_at` (onupdate=now()). Append-only tables (lifecycle events, telemetry, audit log) have no `updated_at`.

### JSONB vs JSON

| Type | Used For | Indexable |
|------|----------|-----------|
| **JSONB** | Evidence blobs, agent definitions, evaluation snapshots, planning stage outputs | Yes (GIN index) |
| **JSON** | Configuration, metadata, lists, settings | No |

Rule: Use JSONB when the data will be queried directly. Use JSON for opaque payloads.

### Special Column Types

| Type | Table(s) | Notes |
|------|----------|-------|
| `Vector(1536)` | `chunks.embedding` | pgvector — Voyage AI / OpenAI embedding dimensions |
| `TSVECTOR` | `chunks.search_vector` | PostgreSQL full-text search, GIN-indexed |
| `JSONB` | execution_index, run_evidence, agent_registry, smithy_evaluation_*, smithy_planning_* | Queryable JSON |
| `ARRAY(String)` | smithy_portfolio (stack), smithy_planning (risks, dependencies, criteria) | PostgreSQL native arrays |
| `LargeBinary` | collab_snapshots.snapshot | Y.js binary document |
| `UUID` (native PG) | All bugcheck_* tables, buildguard_events, tarcie_events | PostgreSQL native UUID |

### Key Invariants

1. **FINALIZED runs are immutable** — new findings rejected with 409 after finalization
2. **Lifecycle transitions are one-way** — enforced at API level; invalid transitions return 409
3. **Audit events are append-only** — no UPDATE or DELETE operations exist
4. **Fingerprints must be stable** — same error at same location produces same fingerprint across runs
5. **Evidence hashes are SHA-256** — `sha256:` prefix convention, 71-character string
6. **Embedding dimensions are fixed at 1536** — changing the embedding model requires index rebuild and full re-embedding

---

*For DataForge ORM source: `DataForge/app/models/`. For Rake pipeline models: `rake/models/` and `rake/research_models.py`. For ForgeAgents schemas: `ForgeAgents/schemas/bugcheck/`. For hybrid search internals, see §9. For migration workflows, see §15.*

---

---

# Integrations

**Document version:** 1.0 (bootstrap scaffold)

External integrations, upstream services, and wire contracts.

> This chapter is a registry-generated bootstrap scaffold for a
> `application` class documentation system. Replace this placeholder with
> real authored content. Registry will not invent repo truth that is not
> already present in the repo.

---

# Governance

**Document version:** 2.0 (2026-06-22) - canonical compliance migration

Ecosystem governance is implemented infrastructure, not aspirational policy. Parent-level documentation defines cross-repo role boundaries, service authority, evidence requirements, and failure doctrine.

Individual repos keep their deep service truth in their own `doc/system/` trees. The parent repo owns the ecosystem-level map, audit gates, naming protocols, and cross-cutting documentation standards.

---

# Operations

**Document version:** 1.0 (bootstrap scaffold)

Deployment, observability, incident response, and bounded repair.

> This chapter is a registry-generated bootstrap scaffold for a
> `application` class documentation system. Replace this placeholder with
> real authored content. Registry will not invent repo truth that is not
> already present in the repo.

---

# Appendices

**Document version:** 1.0 (carry-forward)

Appendices, glossary, and cross-references.

## Unmapped legacy chapters

The following legacy chapters were carried forward but could not be
deterministically mapped to a class-aware slot. Review and place them by
hand:

- `Forge Ecosystem — Complete System Reference`
- `§3 — Tech Stack`
- `§4 — Project Structure`
- `§5 — Configuration & Environment`
- `§6 — Design System`
- `§7 — Frontend`
- `§8 — API Layer`
- `§9 — Backend Internals`
- `§10 — Ecosystem Integration`
- `§12 — AI Integration`
- `§13 — Error Handling`
- `Delays: 1s → 2s → 4s`
- `§14 — Testing`
- `Full test suite`
- `Determinism / stage coverage`
- `Build evidence binary`
- `Real local smoke run against a sibling repo`
- `All tests`
- `With coverage`
- `Skip rate limiting (CI)`
- `Integration only`
- `API tests only`
- `Load tests`
- `Type checking + linting`
- `All tests`
- `With coverage`
- `Security tests only`
- `Compliance tests only`
- `BugCheck domain`
- `Load tests`
- `All tests`
- `BugCheck tests only`
- `Contract tests only`
- `With coverage`
- `CI gate (85% minimum)`
- `Type checking + linting`
- `All tests`
- `With coverage`
- `Unit tests only`
- `Integration tests only`
- `Skip external dependencies`
- `§15 — Handover: Critical Constraints, Known Issues & Maintenance Guide`
- `All services at once`
- `Returns: { "mode": "FULL|CACHE_ONLY|MODEL_ONLY|DEGRADED_NO_RAG|OFFLINE", "reasons": [...] }`
- `1. Activate virtualenv`
- `2. Install dependencies`
- `3. Run migrations (DataForge, Rake)`
- `4. Verify`
- `5. Run tests`
- `6. Start service`
- `Create new migration`
- `Apply`
- `Rollback one step`
- `View history`
- `Create admin user`
- `Or non-interactive:`
- `Liveness`
- `Readiness`
- `Version`
- `§16 — Documentation Truth Policy`
