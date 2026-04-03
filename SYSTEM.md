# Forge Ecosystem — Complete System Reference

**Document version:** 1.4 (2026-03-06) — Normalized canonical vs snapshot facts, resolved cross-section contradictions, and added documentation truth policy
**Protocol:** Forge Documentation Protocol v1

This document is the **ecosystem-level compilation** of the Forge core backend services, the forge-smithy desktop authority layer, and Forge Eval as the standalone deterministic evaluation subsystem. It combines and clarifies the relationships between NeuroForge, DataForge, ForgeAgents, Rake, forge-smithy, Forge Eval, and the surrounding workspace into a unified reference. Each subsystem maintains its own `doc/system/` for deep detail; this layer provides the cross-cutting view.

Documentation truth classes in this reference are explicit:
- Canonical facts define subsystem roles, ports, boundaries, authority, stage ordering, and failure doctrine.
- Snapshot facts record audit-derived counts such as routers, commands, files, tests, coverage, or schema totals as of this document version.

Assembly contract:
- Command: `bash doc/system/BUILD.sh`
- Output: `doc/SYSTEM.md`

| Part | File | Contents |
|------|------|----------|
| §1 | [01-overview-philosophy.md](01-overview-philosophy.md) | Ecosystem identity, canonical doctrine, service roles, design principles |
| §2 | [02-architecture.md](02-architecture.md) | System architecture, data flow, per-service pipelines, infrastructure |
| §3 | [03-tech-stack.md](03-tech-stack.md) | Unified dependency matrix, shared and per-service stacks |
| §4 | [04-project-structure.md](04-project-structure.md) | Repository layout, per-service structure, shared patterns |
| §5 | [05-config-env.md](05-config-env.md) | Master environment variable registry, secret management |
| §6 | [06-design-system.md](06-design-system.md) | Design tokens, colors, typography, spacing, component conventions |
| §7 | [07-frontend.md](07-frontend.md) | Svelte 5, Tauri IPC, routing, stores, component patterns |
| §8 | [08-api-layer.md](08-api-layer.md) | Unified API reference, authentication matrix, endpoint registry |
| §9 | [09-backend-internals.md](09-backend-internals.md) | Key subsystems: inference, search, ingestion, agents, state machines |
| §10 | [10-ecosystem-integration.md](10-ecosystem-integration.md) | Master integration map, contracts, access control, data lifecycle |
| §11 | [11-database-schema.md](11-database-schema.md) | All ORM models, table definitions, indexes, constraints |
| §12 | [12-ai-integration.md](12-ai-integration.md) | LLM providers, prompt routing, MAID, RTCFX, cost controls |
| §13 | [13-error-handling.md](13-error-handling.md) | Failure modes, degradation, circuit breakers, retry contracts |
| §14 | [14-testing.md](14-testing.md) | Testing infrastructure, QA tiers T0-T6, severity gates S0-S4 |
| §15 | [15-handover.md](15-handover.md) | Critical constraints, known issues, maintenance, sync workflow |
| §16 | [16-documentation-truth-policy.md](16-documentation-truth-policy.md) | Canonical vs snapshot labeling rules for future audits |

## Per-Service Documentation

For deep detail on individual services, see their own `doc/system/` directories:

| Service | Location | Port | Role |
|---------|----------|------|------|
| NeuroForge | [NeuroForge/doc/system/](../../NeuroForge/doc/system/_index.md) | 8000 | AI inference orchestration |
| DataForge | [DataForge/doc/system/](../../DataForge/doc/system/_index.md) | 8001 | Source of truth — data persistence |
| ForgeAgents | [ForgeAgents/doc/system/](../../ForgeAgents/doc/system/_index.md) | 8010 | Agent execution runtime |
| Rake | [rake/doc/system/](../../rake/doc/system/_index.md) | 8002 | Data ingestion pipeline |
| forge-smithy | [forge-smithy/docs/smith/](../../forge-smithy/docs/smith/README.md) | — | Desktop authority layer (Tauri 2.0 + Svelte 5) |
| Forge Eval | [forge-eval/repo/doc/system/](../../forge-eval/repo/doc/system/_index.md) | — | Standalone deterministic evaluation subsystem (Packs A-J) |

## Quick Assembly

```bash
./BUILD.sh                              # Assembles all parts into ../SYSTEM.md
../scripts/context-bundle.sh full       # Full context bundle
../scripts/context-bundle.sh frontend   # Frontend-focused bundle
```

*Last updated: 2026-03-06*

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

---

# §4 — Project Structure

Directory names, subsystem boundaries, and ownership lines in this chapter are canonical. File counts, route/module tallies, migration totals, LOC notes, and test-suite counts are current audited snapshot values unless the number is part of an explicit protocol.

## Ecosystem Repository Layout

```
/home/charlie/Forge/ecosystem/
├── NeuroForge/              # AI inference orchestration (port 8000)
├── DataForge/               # Source of truth — data persistence (port 8001)
├── rake/                    # Data ingestion pipeline (port 8002)
├── ForgeAgents/             # Agent execution runtime (port 8010)
├── Forge_Command/           # Desktop orchestration (port 8003)
├── forge-smithy/            # Desktop governance workbench (Tauri + Svelte 5)
├── forge-eval/              # Standalone deterministic evaluation subsystem (Packs A-M)
├── eval-cal-node/           # Post-implementation calibration node for Forge Eval
├── Author-Forge/            # Literary AI application
├── cortex_bds/              # Multi-AI orchestration desktop app (Tauri 2.0 + SvelteKit)
├── zfss/                    # Zero-trust file storage service (internal tooling)
├── checkly/                 # Monitoring infrastructure
│
├── doc/                     # Ecosystem-level documentation
│   └── system/              # ← THIS DIRECTORY (Forge Documentation Protocol v1)
│
├── docs/                    # Cross-cutting documentation
│   ├── canonical/           # Authoritative doctrine
│   ├── architecture/        # Security diagrams
│   ├── contracts/           # API contracts & JSON schemas
│   ├── implementation/      # Implementation plans (bugcheck, fpvs, doctrine)
│   ├── audits/              # Quality & compliance audits
│   ├── changelog/           # Release notes
│   ├── smith/               # SMITH ecosystem-level summary
│   ├── qa/                  # QA protocols
│   └── render-deployment/   # Deployment configs
│
├── schemas/                 # Shared JSON schemas
├── CLAUDE.md                # AI assistant context (BugCheck canonical)
└── README.md                # Main ecosystem README
```

---

## NeuroForge — `NeuroForge/`

**Root:** `/home/charlie/Forge/ecosystem/NeuroForge/`
**Application package:** `neuroforge_backend/`

```
NeuroForge/
├── neuroforge_backend/
│   ├── main.py                    # FastAPI app (63.5KB), 13 routers
│   ├── config.py                  # Pydantic settings
│   ├── services/                  # 5-stage pipeline: context_builder_fixed.py,
│   │                              #   prompt_engine.py, model_router.py,
│   │                              #   evaluator.py, post_processor.py
│   ├── routers/                   # 13 route modules (inference, maid, rtcfx,
│   │                              #   research, orchestration, authorforge, etc.)
│   ├── rtcfx/                     # Learning subsystem (compiler, ledger, gate)
│   ├── psychology/                # 9 behavioral frameworks
│   ├── clients/                   # 5 provider API clients (openai, anthropic,
│   │                              #   google, ollama, xai)
│   ├── rag/                       # RAG orchestration + fallback store
│   ├── cache/                     # Redis L1 cache client
│   ├── models/                    # Champion model EMA tracking
│   ├── analysis/                  # Pattern + trend analysis
│   └── database/                  # SQLAlchemy ORM (Inference, ModelMetric)
├── tests/
├── doc/system/                    # Forge Documentation Protocol v1 (§1-§11)
├── docs/                          # Supplementary guides
└── requirements.txt
```

**NOTE:** `context_builder.py` is a guard stub (raises `ImportError`). Always use `context_builder_fixed.py`.

---

## DataForge — `DataForge/`

**Root:** `/home/charlie/Forge/ecosystem/DataForge/`
**Application package:** `app/`

```
DataForge/
├── app/
│   ├── main.py                    # FastAPI app, 33 router registrations (current audited snapshot)
│   ├── database.py                # SQLAlchemy engine, SessionLocal, pgvector init
│   ├── models/
│   │   ├── models.py              # 31+ ORM models (User, Document, Chunk,
│   │   │                          #   ExecutionIndex, BugCheck*, NeuroForge*,
│   │   │                          #   VibeForge*, AuthorForge*, Smithy*, etc.)
│   │   └── schemas.py             # 90+ Pydantic v2 schemas
│   ├── api/
│   │   ├── search_router.py       # Hybrid search endpoints
│   │   ├── admin_router.py        # Admin CRUD
│   │   ├── auth_router.py         # JWT, OAuth2, TOTP 2FA
│   │   ├── crud.py                # Database operations (no business logic)
│   │   └── search.py              # Hybrid vector + BM25 + RRF engine
│   └── utils/
│       ├── embeddings.py          # Chunking + Voyage AI embedding
│       └── auth.py                # JWT creation/validation + bcrypt
├── alembic/                       # 11 migration files
├── templates/admin.html           # Self-contained admin UI
├── tests/                         # Current audited snapshot: 32 files, 296 tests, 82% coverage
├── doc/system/                    # Forge Documentation Protocol v1 (§1-§11)
├── docs/                          # Supplementary guides
└── requirements.txt
```

---

## Rake — `rake/`

**Root:** `/home/charlie/Forge/ecosystem/rake/`
**Application:** root-level `main.py`

```
rake/
├── main.py                        # FastAPI app, middleware, router mounts
├── config.py                      # Pydantic Settings v2
├── research_models.py             # Research mission models
├── forge_keys.py                  # API key resolution (ForgeCommand → env)
│
├── api/                           # REST routes
│   ├── routes.py                  # /api/v1/jobs
│   ├── mission_routes.py          # /api/v1/missions
│   ├── discovery_routes.py        # /api/v1/discover
│   ├── fpvs.py                    # /ready, /version
│   └── admin_keys.py              # /admin/api-keys
│
├── pipeline/                      # 5-stage ingestion
│   ├── orchestrator.py            # PipelineOrchestrator
│   ├── fetch.py, clean.py         # Stages 1-2
│   ├── chunk.py, semantic_chunker.py  # Stage 3
│   ├── embed.py                   # Stage 4
│   └── store.py                   # Stage 5
│
├── sources/                       # Data source adapters
│   ├── file_upload.py             # PDF/DOCX/TXT/PPTX/Markdown
│   ├── url_scrape.py              # Web scraping (robots.txt compliant)
│   ├── api_fetch.py               # External REST APIs
│   ├── database_query.py          # SQL SELECT (read-only)
│   ├── sec_edgar.py               # SEC EDGAR filings
│   └── providers/                 # Tavily, Serper, Firecrawl
│
├── services/                      # External clients
│   ├── dataforge_client.py        # DataForge REST client
│   ├── neuroforge_client.py       # NeuroForge strategy + curation
│   ├── embedding_service.py       # OpenAI embeddings
│   ├── mission_orchestrator.py    # Mission state machine
│   ├── budget_enforcer.py         # Cost tracking
│   └── evidence_bundle.py         # Evidence generation
│
├── models/                        # ORM + pipeline types
├── auth/                          # JWT, API keys, rate limiting, tenant
├── alembic/                       # 3 migration files
├── tests/                         # unit/ + integration/
├── doc/system/                    # Forge Documentation Protocol v1 (§1-§16)
├── docs/                          # Supplementary guides
└── requirements.txt
```

---

## ForgeAgents — `ForgeAgents/`

**Root:** `/home/charlie/Forge/ecosystem/ForgeAgents/`
**Application package:** `app/` (current snapshot: ~385 files, ~124k lines)

```
ForgeAgents/
├── app/
│   ├── main.py                    # FastAPI app, lifespan handler
│   ├── core/
│   │   ├── config.py              # All configuration (408 lines)
│   │   ├── types.py               # Core domain types (1,019 lines)
│   │   └── exceptions.py          # Exception hierarchy (290 lines)
│   │
│   ├── api/                       # Route handlers (thin controllers)
│   │   ├── agents.py              # Agent CRUD + execution
│   │   ├── health.py              # /health, /ready, /version, /metrics
│   │   ├── bugcheck.py            # BugCheck endpoints
│   │   ├── sentinel.py            # Sentinel sweep + healing REST endpoints
│   │   └── bds_*.py               # BDS stream endpoints
│   │
│   ├── agents/                    # Agent runtime
│   │   ├── base.py                # Base class, execution loop
│   │   ├── lifecycle.py           # State machine
│   │   ├── registry.py            # Agent registry
│   │   ├── startup.py             # Agent system initialization + policy registration
│   │   ├── reference/             # 6 archetypes (Writer, Coder, Analyst,
│   │   │                          #   Researcher, Coordinator, Ecosystem)
│   │   ├── bugcheck/              # BugCheck agent (checks/, routing/, schemas/)
│   │   └── sentinel/              # Sentinel health monitor + self-healing agent
│   │       ├── agent.py           # SentinelAgent class (Ecosystem specialization)
│   │       └── playbooks.py       # Healing playbooks (cache_flush, breaker_reset, etc.)
│   │
│   ├── policies/                  # 12 policies across 4 categories
│   │   ├── engine.py              # Orchestration
│   │   ├── safety.py              # 4 safety policies
│   │   ├── domain.py              # 4 domain policies
│   │   ├── resource.py            # 3 resource policies
│   │   └── healing.py             # HealingScopePolicy (tier enforcement, cooldowns)
│   │
│   ├── memory/                    # 3-tier memory
│   │   ├── manager.py             # Coordination (783 lines)
│   │   ├── shortterm.py           # In-memory FIFO
│   │   ├── longterm.py            # DataForge + pgvector
│   │   └── episodic.py            # DataForge timeline
│   │
│   ├── tools/                     # 35 tools, 6 adapters
│   │   ├── router.py              # Dispatch + policy pre-auth
│   │   ├── rake.py                # 9 Rake tools
│   │   ├── neuroforge.py          # 6 NeuroForge tools
│   │   ├── dataforge.py           # 5 DataForge tools
│   │   ├── filesystem.py          # 3 filesystem tools
│   │   └── health_sweep.py        # HealthAdapter: health_sweep + breaker_probe_reset
│   │
│   ├── capabilities/              # 120 capabilities (A-G)
│   ├── nodes/                     # 35 execution nodes (7 tiers)
│   ├── llm/                       # OpenAI + Anthropic providers
│   ├── services/                  # Outbound HTTP clients
│   ├── evidence/                  # Evidence bundle construction
│   ├── contracts/                 # Canonical JSON, node envelopes
│   ├── runner/                    # DAG execution engine
│   ├── cortex/                    # Multi-AI planning
│   └── auth/                      # JWT, RBAC, rate limiting
│
├── schemas/bugcheck/              # JSON Schema definitions
├── tests/                         # Contract tests + BugCheck tests
├── doc/system/                    # Forge Documentation Protocol v1 (§1-§11)
├── docs/                          # Supplementary guides
└── requirements.txt
```

---

## Forge Eval — `forge-eval/`

**Root:** `/home/charlie/Forge/ecosystem/forge-eval/`
**Implementation root:** `repo/`

```
forge-eval/
├── repo/
│   ├── src/forge_eval/
│   │   ├── cli.py                 # `forge-eval run|validate`
│   │   ├── stage_runner.py        # Deterministic stage orchestration
│   │   ├── stages/                # risk_heatmap -> context_slices ->
│   │   │                          #   review_findings -> telemetry_matrix ->
│   │   │                          #   occupancy_snapshot -> capture_estimate
│   │   ├── services/              # Diff parsing, range ops, reviewer logic,
│   │   │                          #   telemetry, occupancy, hidden-defect estimation
│   │   ├── schemas/               # Strict JSON schemas for emitted artifacts
│   │   └── validation/            # Schema loader + artifact validation
│   ├── rust/forge-evidence/       # Canonical JSON, hashing, artifact identity, hashchain
│   ├── tests/                     # Unit, integration, determinism, fail-closed tests
│   ├── doc/system/                # Forge Eval subsystem reference
│   └── README.md
└── implementation_pack_*.md       # Historical implementation prompts / planning docs
```

Forge Eval is a first-class subsystem, not a child module of NeuroForge, DataForge, or forge-smithy. It evaluates sibling repositories in the workspace and currently implements the deterministic Pack J path:

```text
risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate
```

---

## Eval Cal Node — `eval-cal-node/`

**Root:** `/home/charlie/Forge/ecosystem/eval-cal-node/`

```
eval-cal-node/
├── src/eval_cal_node/
│   ├── cli.py                     # `eval-cal-node record|status|review`
│   ├── config.py                  # Config loader + parameter validation
│   ├── errors.py                  # CalNodeError hierarchy
│   ├── schemas/                   # 7 JSON schemas (record, config, 5 output artifacts)
│   ├── services/                  # Pattern extraction, calibration math, gates,
│   │                              #   artifact writers, status reporting
│   └── validation/                # Schema loader + record validation
├── config/
│   └── cal_node_config.json       # Per-parameter policy bounds (13 allowed targets)
├── records/                       # Runtime: ingested calibration records (gitignored)
├── proposals/                     # Runtime: emitted proposal artifacts (gitignored)
├── reports/                       # Summary reports
├── tests/                         # 51 tests across 6 test files
└── README.md
```

Eval Cal Node is a standalone post-implementation calibration node. It studies the gap between Forge Eval outputs, SYSTEM.md declarations, and reconciliation findings. It produces bounded, reviewable calibration proposals for 13 Eval parameters but never directly alters the approved parameter revision.

---

## Shared Patterns

### Directory Convention

The four HTTP services follow a consistent internal structure:

| Directory | Purpose | Present In |
|-----------|---------|-----------|
| `api/` or `routers/` | REST route handlers | All |
| `models/` | ORM models + Pydantic schemas | All |
| `services/` | External HTTP clients | All |
| `auth/` | JWT, API keys, rate limiting | All |
| `tests/` | pytest test suite | All |
| `doc/system/` | Forge Documentation Protocol v1 docs | All |
| `docs/` | Supplementary guides | All |
| `alembic/` | Database migrations | DF, Rake |

Forge Eval follows the same `tests/`, `doc/system/`, and modular `services/`/`schemas/` discipline, but its repository shape is stage-oriented rather than HTTP-router-oriented.

### Config Pattern

The resident HTTP services use Pydantic v2 `BaseSettings` for configuration:
- Environment variables are the source of truth
- `.env` files supported via `python-dotenv`
- Each service has a `.env.example` documenting all variables

Forge Eval is the exception in this chapter: it is CLI-driven and accepts optional file-based runtime config rather than a resident `BaseSettings` service surface.

### Naming Conventions

| Pattern | Convention |
|---------|-----------|
| Python modules | `snake_case.py` |
| Test files | `test_{module}.py` |
| Alembic migrations | `YYYYMMDD_HHMM_description.py` (Rake) or `0001_description.py` (DataForge) |
| Doc parts | `NN-slug.md` |

---

*For per-service structure deep dives, see each service's own `doc/system/` project structure chapter. For configuration, see §5. For frontend structure, see §7.*

---

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

---

# §6 — Design System

## Design Philosophy

Forge's visual identity is a **dark-mode HUD** inspired by Bloomberg Terminal aesthetics — information-dense, low-distraction, and purpose-built for governance-critical workflows. There is no light mode. Every pixel earns its place.

**Guiding rules:**
- Dark-mode only — `--forge-void` (#07080c) is the canvas
- No rounded corners > 8px — "this is a HUD, not a toy"
- Transitions 150-250ms — never slower (HUD speed)
- Service identity colors are immutable across all Forge apps
- Budget thresholds: 80% warning (amber), 95% critical (red)

---

## Surface Hierarchy

Five surface layers create depth without shadows:

| Token | Hex | Role |
|-------|-----|------|
| `--forge-void` | `#07080c` | Page canvas — deepest background |
| `--forge-obsidian` | `#0e1018` | Primary card/panel surface |
| `--forge-slate` | `#161a24` | Elevated surfaces, sidebars |
| `--forge-steel` | `#1e2330` | Hover states, active panels |
| `--forge-edge` | `#2a3040` | Borders, dividers |

---

## Service Identity Colors

Each Forge service has an immutable color pair. These are non-negotiable — they identify services across all consumer apps, dashboards, and documentation.

| Service | Token | Hex | Glow Variant |
|---------|-------|-----|-------------|
| DataForge | `--dataforge-blue` | `#3b82f6` | `--dataforge-glow`: `#60a5fa` |
| NeuroForge | `--neuroforge-violet` | `#8b5cf6` | `--neuroforge-glow`: `#a78bfa` |
| Rake | `--rake-bronze` | `#d97706` | `--rake-glow`: `#f59e0b` |
| SMITH | `--smith-emerald` | `#10b981` | `--smith-glow`: `#34d399` |

---

## Ember Accent System

The primary accent is **ember** — the visual metaphor for the forge's fire. Used for CTAs, focus rings, and primary actions.

| Token | Hex | Usage |
|-------|-----|-------|
| `--ember-core` | `#f97316` | Primary CTA color |
| `--ember-hot` | `#fb923c` | Hover state |
| `--ember-dim` | `#9a3412` | Pressed/active |
| `--ember-glow` | `rgba(249, 115, 22, 0.15)` | Background glow |

---

## Semantic Status Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--status-active` | `#3b82f6` | Running, in progress |
| `--status-success` | `#10b981` | Completed, healthy |
| `--status-warning` | `#f59e0b` | Needs attention, budget 80% |
| `--status-danger` | `#ef4444` | Failed, error, budget 95% |
| `--status-neutral` | `#6b7280` | Inactive, cancelled |

**Budget threshold conventions:**
- < 80% of cap: normal (no status indicator)
- 80-94%: `--status-warning` with amber badge
- 95%+: `--status-danger` with red badge + alert

---

## Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--font-ui` | `'Inter', -apple-system, sans-serif` | Body text, labels, UI elements |
| `--font-mono` | `'JetBrains Mono', 'Fira Code', monospace` | Code blocks, terminal output, IDs |
| `--font-display` | `'Inter', sans-serif` | Page titles, hero metrics |

### Type Scale

| Token | Size | Usage |
|-------|------|-------|
| `--text-xs` | 0.75rem (12px) | Badges, timestamps |
| `--text-sm` | 0.875rem (14px) | Table cells, metadata |
| `--text-base` | 1rem (16px) | Body text |
| `--text-lg` | 1.125rem (18px) | Section headers |
| `--text-xl` | 1.25rem (20px) | Page titles |
| `--text-2xl` | 1.5rem (24px) | Page section titles |
| `--text-3xl` | 1.875rem (30px) | Hero metrics, KPIs |

---

## Spacing

4px increment system:

| Token | Value | Token | Value |
|-------|-------|-------|-------|
| `--space-1` | 0.25rem (4px) | `--space-8` | 2rem (32px) |
| `--space-2` | 0.5rem (8px) | `--space-10` | 2.5rem (40px) |
| `--space-3` | 0.75rem (12px) | `--space-12` | 3rem (48px) |
| `--space-4` | 1rem (16px) | `--space-16` | 4rem (64px) |
| `--space-5` | 1.25rem (20px) | `--space-20` | 5rem (80px) |
| `--space-6` | 1.5rem (24px) | `--space-24` | 6rem (96px) |

---

## Borders & Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-xs` | 2px | Badges |
| `--radius-sm` | 4px | Inputs, buttons |
| `--radius-md` | 6px | Cards |
| `--radius-lg` | 8px | Modals, panels (maximum allowed) |
| `--border-subtle` | `1px solid var(--forge-edge)` | Standard divider |
| `--border-focus` | `1px solid rgba(249, 115, 22, 0.4)` | Ember focus ring |

---

## Shadows & Glows

Subtle depth — no floating-card effects.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-inset` | `inset 0 1px 0 rgba(255,255,255,0.03)` | Subtle top highlight |
| `--shadow-glow-ember` | `0 0 20px rgba(249,115,22,0.08)` | Active/focused ember elements |
| `--shadow-glow-blue` | `0 0 20px rgba(59,130,246,0.08)` | DataForge-associated elements |
| `--shadow-glow-violet` | `0 0 20px rgba(139,92,246,0.08)` | NeuroForge-associated elements |
| `--shadow-glow-emerald` | `0 0 20px rgba(16,185,129,0.08)` | SMITH-associated elements |

---

## Transitions

| Token | Duration | Usage |
|-------|----------|-------|
| `--duration-fast` | 150ms | Hover, focus, small toggles |
| `--duration-normal` | 200ms | Panel transitions, dropdowns |
| `--duration-slow` | 250ms | Modal open/close (maximum allowed) |

Easing functions:

| Token | Curve |
|-------|-------|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--ease-in` | `cubic-bezier(0.7, 0, 0.84, 0)` |
| `--ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` |

---

## Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--z-base` | 0 | Normal flow |
| `--z-dropdown` | 100 | Dropdowns, menus |
| `--z-sticky` | 200 | Sticky headers |
| `--z-overlay` | 300 | Overlays |
| `--z-modal` | 400 | Modals |
| `--z-popover` | 500 | Popovers |
| `--z-toast` | 600 | Toasts |
| `--z-tooltip` | 700 | Tooltips |
| `--z-command-palette` | 800 | Command palette (highest) |

---

## Layout Dimensions

| Token | Value | Usage |
|-------|-------|-------|
| `--sidebar-width-collapsed` | 56px | Nav sidebar (collapsed) |
| `--sidebar-width-expanded` | 240px | Nav sidebar (expanded) |
| `--topbar-height` | 48px | Top navigation bar |
| `--statusbar-height` | 28px | Bottom status bar |
| `--gutter` | 16px | Column gutter |
| `--page-padding` | 24px | Page content padding |
| `--card-padding` | 16px | Card internal padding |

---

## Component Conventions

All UI components follow these patterns (see §7 for implementation details):

### Variant Props

Components expose a `variant` prop for visual variants:

```
variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
size?: 'sm' | 'md' | 'lg'
```

### Slot Pattern

Components use Svelte 5 `Snippet` type for composable content:

```
children?: Snippet          — Main content area
header?: Snippet            — Custom header
actions?: Snippet           — Action buttons
footer?: Snippet            — Custom footer
```

### Event Pattern

Components use callback props (not dispatchers):

```
onclick?: () => void
onSave?: (data: T) => void
onCancel?: () => void
```

---

## Token Source File

All tokens are defined in a single source of truth:

```
forge-smithy/src/styles/forge-tokens.css
```

Consumer apps and services should reference these tokens. No hardcoded color values.

---

*For component implementation patterns, see §7. For service identity usage in API responses, see §8.*

---

# §7 — Frontend

UI conventions, IPC boundaries, and required Svelte/Tauri patterns in this chapter are canonical. Counts of components, routes, stores, and commands are current audited snapshot values.

## Framework Overview

The Forge ecosystem's primary frontend is **forge-smithy** (SMITH) — a desktop application built with **Tauri 2.0** (Rust backend) + **SvelteKit** (Svelte 5 frontend). It serves as the governance-enforced authority layer for the entire ecosystem.

| Aspect | Technology |
|--------|-----------|
| Desktop framework | Tauri 2.0 (Rust 2024 edition) |
| Frontend framework | SvelteKit + Svelte 5 (runes) |
| Package manager | pnpm |
| Styling | CSS custom properties (forge-tokens.css) + Tailwind v4 |
| IPC | `@tauri-apps/api/core` → `invoke<T>()` |
| State management | Svelte 5 `$state()` runes + exported singletons |

### Key Metrics

Current code snapshot:

| Metric | Count |
|--------|-------|
| Total `.svelte` files | 330 |
| Reusable components | 218 (34 categories) |
| Route files | 71 pages + 10 API endpoints |
| Store modules | 55 |
| Tauri commands | 444 |

---

## Svelte 5 Runes — Mandatory Patterns

All Svelte code MUST use Svelte 5 runes. Svelte 4 patterns are banned.

| Svelte 4 (BANNED) | Svelte 5 (REQUIRED) |
|-------------------|---------------------|
| `export let prop` | `let { prop } = $props()` |
| `let x = value` (reactive) | `let x = $state(value)` |
| `$: derived = ...` | `const derived = $derived(...)` |
| `$: { sideEffect }` | `$effect(() => { sideEffect })` |
| `<slot />` | `{@render children()}` with `Snippet` type |
| `<slot name="x" />` | `{@render x()}` with named `Snippet` props |
| `on:click={handler}` | `onclick={handler}` |
| `createEventDispatcher()` | Callback props: `onSave?: (data) => void` |
| `bind:value` (two-way) | `$bindable()` in props definition |

---

## Component Patterns

### Standard Component Structure

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = {
    title?: string;
    variant?: 'default' | 'elevated' | 'bordered';
    children?: Snippet;
    header?: Snippet;
    actions?: Snippet;
    onSave?: (data: string) => void;
  };

  let {
    title = '',
    variant = 'default',
    children,
    header,
    actions,
    onSave,
    ...rest
  }: Props = $props();

  let localState = $state(0);
  const computed = $derived(localState * 2);
  const classes = $derived.by(() =>
    ['panel', `panel-${variant}`].filter(Boolean).join(' ')
  );

  $effect(() => {
    console.log('state changed:', localState);
  });
</script>

<div class={classes} {...rest}>
  {#if header}{@render header()}{/if}
  {#if children}{@render children()}{/if}
  {#if actions}{@render actions()}{/if}
</div>
```

### Two-Way Binding (with `$bindable`)

```svelte
<script lang="ts">
  let {
    value = $bindable(''),
    error = '',
  }: { value: string; error?: string } = $props();
</script>

<input bind:value class:error={!!error} />
```

### Component Categories (Representative Snapshot Breakdown)

The table below is a representative snapshot breakdown. The audited top-line component total appears in the Key Metrics table above.

| Category | Count | Examples |
|----------|-------|---------|
| Layout | 6 | AppShell, Header, Sidebar, PageHeader, TriPaneLayout, Icon |
| Form | 3 | FormField, FormGroup, SubmitButton |
| Input | 4 | Button, Input, Select, Textarea |
| Container | 2 | Panel, Modal |
| Feedback | 6 | Badge, Alert, MetaRow, StateBanner, Notifications |
| Evidence | 6 | EvidenceViewer, EvidenceBundleList, PacketDetail |
| Assist | 15 | AssistPanel, AssistThread, NarrationBanner, ModeSelector |
| Research | 15 | ClaimMaturationBadge, ClaimTimeline, TrendingClaims |
| Knowledge | 14 | MissionCard, PipelineProgress, KpiCard, ActivityFeed |
| SCAFA | 6 | ScafaPanel, ScafaFindingCard, ScafaProofGateResult |
| RAG Eval | 4 | RagEvalGauge, RagEvalBreakdown, CragChunkGrid |
| SAS | 15 | SASDashboard, SASViolationTable, CdiGauge |
| Governance | 4 | GateDetailCard, SmelterProofPanel, GovernanceGlossary |

---

## Routing

### Global Layout Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Top Bar (48px)                               Command Palette │
├────────┬───────────────────────────────┬────────────────────┤
│        │                               │                    │
│ Side   │    Center Content Area        │  Right Context     │
│ Nav    │    (page routes)              │  Panel             │
│ (56-   │                               │  (collapsible)     │
│ 240px) │                               │                    │
│        │                               │                    │
├────────┴───────────────────────────────┴────────────────────┤
│  Status Footer (28px) — governance metrics, pipeline state   │
├─────────────────────────────────────────────────────────────┤
│  System Rail — priority banners (P0 orphan, P1 locked, P2)  │
└─────────────────────────────────────────────────────────────┘
```

### Global Layout Components

| Component | Purpose |
|-----------|---------|
| AppShell | Root layout container |
| Tri-Pane Layout | Left nav + center content + right context (all collapsible) |
| System Rail | Priority-based banners (P0: orphan run, P1: locked session, P2: offline service) |
| Status Footer | Persistent 28px footer with governance metrics |
| Command Palette | Global search + action dispatch (`--z-command-palette: 800`) |
| SMITH Assist | Governance narrator chatbot panel |
| Pipeline HUD | Step chevrons, lock badge, session context |
| Patch Cart | Staged file changes preview |

### Route Organization (Representative Snapshot Breakdown)

The table below summarizes major route groups. It is a breakdown view, not a second canonical total.

| Route Group | Pages | Purpose |
|-------------|-------|---------|
| `/` | 1 | Dashboard |
| `/admin` | 1 | Administrative panel |
| `/agents` | 1 | Agent management |
| `/analytics` | 1 | Usage analytics |
| `/architecture` | 1 | Architecture studio |
| `/audit` | 1 | Governance audit |
| `/code-review` | 1 | Code review sessions |
| `/encyclopedia` | 1 | Encyclopedia browse |
| `/evidence` | 1 | Evidence bundles |
| `/governance` | 1 | Governance dashboard |
| `/knowledge/*` | 8 | War Room, Mission Control, New Mission, Theater, Source Vault, Ledger, Archive, Evidence Detail |
| `/research/*` | 5 | Sessions, New, [id], Analytics, Search |
| `/planning` | 1 | Planning sessions |
| `/repos` | 1 | Repository management |
| Other routes | ~44 | Evaluator, execution, history, models, orchestration, etc. |
| API routes | 10 | Server-side data endpoints |

---

## Store Pattern

Stores use **plain objects with `$state()` runes** — not Svelte stores (`writable()`) — to avoid production build issues.

### Standard Store Structure

```typescript
// Internal reactive state (not exported directly)
let state = $state<{
  data: SomeType | null;
  status: 'idle' | 'loading' | 'ready' | 'error';
  message: string;
}>({
  data: null,
  status: 'idle',
  message: '',
});

// Exported singleton with getters + actions
export const myStore = {
  // Read-only getters
  get data() { return state.data; },
  get status() { return state.status; },
  get message() { return state.message; },

  // Actions
  async hydrate(): Promise<void> {
    state.status = 'loading';
    const result = await invoke<SomeType>('my_command');
    state.data = result;
    state.status = 'ready';
  },

  // Test helper
  _reset(): void {
    state.data = null;
    state.status = 'idle';
    state.message = '';
  },
};

// Optional class export for unit test instantiation
export class MyStore { /* mirrors singleton */ }
```

### Key Stores by Domain

| Store | Domain | State |
|-------|--------|-------|
| `pipeline` | Core | Step, sessionId, blueprint, lock state |
| `assistStore` | SMITH Assist | Messages, context, failurePatterns, fixProposals |
| `knowledgeStore` | Knowledge | Missions, search, cost tracking, pipeline progress |
| `researchStore` | Research | Claims, sources, MCP validation, enrichment, telemetry |
| `scafaStore` | SCAFA | Findings, proposals, proofGateResult, workflowPhase |
| `ragEvalStore` | RAG | Composite score, decision, remediation |
| `retrievalRouterStore` | RAG | Query complexity, retrieval strategy |
| `serviceHealthStore` | System | Circuit breaker status per service |
| `smelterDriftStore` | Governance | Drift reports, trust posture (T0-T4) |
| `trustDebtBiStore` | Governance | GFI report, operational patterns |
| `patchCartStore` | MRPA | Patch set, status, contract |
| `wizardStore` | Governance | Decision wizard steps, rationale |

---

## Tauri IPC Bridge

### Communication Pattern

Frontend → Rust backend communication uses `invoke()` from `@tauri-apps/api/core`:

```typescript
import { invoke } from '@tauri-apps/api/core';

// Query with typed response
const context = await invoke<AssistContext>('smith_assist_context_get', {
  sessionId: 'abc123',
});

// Mutation
await invoke('smith_assist_apply_fix', {
  fixId: 'fix-123',
  runId: 'run-456',
});
```

### IPC Principles

1. **No API keys cross the IPC boundary** — all credentials injected server-side from ForgeCommand vault
2. **Response types are generic** — `invoke<ResponseType>(command, payload)`
3. **Errors bubble as exceptions** — caught in try-catch blocks
4. **Token semantics handled in Rust** — `run_token`, `user_token` validated server-side
5. **Terminal states explicit** — `COMPLETED`, `FAILED`, `CANCELLED`

### Command Organization (Representative Domain Breakdown)

The table below highlights major command domains. The audited top-line command total appears in the Key Metrics table above.

| Domain | Count | Purpose |
|--------|-------|---------|
| Governance | 108 | Stop-ship, packaging, compliance, evidence, SBOM |
| BuildGuard | 39 | Quality gates, ledger, analytics, verification |
| Research | 36 | Rake API, MCP-v5.0, sessions, verification, telemetry |
| Smithy | 28 | Release governance, encyclopedia, evidence bundles |
| SMITH Assist | 18 | Narrator, incidents, fixes, context assembly |
| MRPA | 15 | Minimal Rust Patch Applier, deterministic patching |
| Knowledge | 13 | Knowledge retrieval, research missions |
| Generative | 9 | ForgeImages integration |
| Images | 11 | Image generation + branding |
| Smelter | 9 | Drift analysis, trust posture |
| SCAFA | 8 | Structural analysis + Proof Gate |
| RAG Eval | 7 | RAG quality gate + CRAG evaluation |
| Attestation | 7 | Cryptographic attestation |
| Audit | 7 | Governance audit trail |
| Molting | 7 | Policy molting proposals |
| Learning | 6 | Track B policy learning |
| SAS | 5 | Self-Assessment System |
| Evidence | 5 | Evidence packet management |
| MAID | 4 | CDI-aware validation routing |
| ForgeCommand | 4 | Desktop orchestration proxy |
| ForgeAgents | 6 | Agent proxy, gate analytics |
| Runtime | 3 | Token management, health ping |
| Service Client | 3 | Circuit breaker status |
| Replay Cache | 3 | Deterministic replay cache |
| Repos | 3 | Repository management |
| IPC | 3 | Low-level IPC |
| Signals | 2 | System signals |
| Research (Tauri) | 2 | Research-specific commands |
| Telemetry | 2 | Telemetry bridge |
| Cache | 1 | Cache management |

---

## SMITH Assist — Situational Awareness Engine (SAE)

SMITH Assist is a read-only governance chatbot that provides context-aware guidance. It uses a Situational Awareness Engine with these client-side modules:

| Module | File | Purpose |
|--------|------|---------|
| Context Assembler | `contextAssembler.ts` | Reads all frontend stores → builds SAEContext |
| Query Classifier | `queryClassifier.ts` | 8 intent types + BRIEFING/GOVERNED tiering |
| Route Prompt Registry | `routePromptRegistry.ts` | 25+ route-specific context prompts |
| Narrator Language | `narratorLanguage.ts` | Plain-English translations for pipeline/readiness/drift |
| Conversation Memory | `conversationMemory.ts` | Ring buffer (max 10), clean slate on mode switch |
| Narration Engine | `narrationEngine.ts` | State transition detection, rate-limited (5s) |
| Mode Suggester | `modeSuggester.ts` | Context-aware mode recommendations |

---

## Documentation Sync Requirement

Any changes to forge-smithy code MUST include corresponding documentation updates:

| Change | Update |
|--------|--------|
| Add/modify components | `docs/smith/COMPONENTS.md` |
| Add/modify stores | `docs/smith/STORES.md` |
| Add/modify routes | `docs/smith/UI_ROUTES.md` |
| Add/modify Tauri commands | `docs/smith/COMMANDS.md` |
| Any of the above | `docs/smith/README.md` (system metrics) |

---

*For design token definitions, see §6. For Tauri command backend details, see §9. For IPC security boundaries, see §10.*

---

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

---

# §9 — Backend Internals

This chapter covers the key subsystems inside each service — the pipelines, state machines, and engines that define how Forge processes data.

---

## NeuroForge — Inference Pipeline

### 5-Stage Pipeline

Every inference request traverses all five stages in sequence. No bypass.

| Stage | File | Input | Output | Dependencies |
|-------|------|-------|--------|-------------|
| Context Builder | `context_builder_fixed.py` | Query text | RAG chunks | DataForge (primary), SQLite (fallback) |
| Prompt Engine | `prompt_engine.py` | Query + context + domain | Rendered prompt | Domain templates |
| Model Router | `model_router.py` | Prompt + strategy | LLM response | 5 providers |
| Evaluator | `evaluator.py` | LLM output | Quality score (0.0-1.0) | LLM (evaluation model) |
| Post-Processor | `post_processor.py` | Evaluated output | Normalized response | DataForge (provenance) |

### Model Router Strategies

| Strategy | Behavior |
|----------|----------|
| CHAMPION_SELECTION | Pick the model with highest EMA score for domain+task_type |
| ENSEMBLE_VOTING | Run multiple models, consensus scoring |
| COST_OPTIMIZATION | Cheapest model that meets quality threshold |
| QUALITY_OPTIMIZATION | Best-performing model regardless of cost |

Fallback chain: `PREMIUM → STANDARD → FAST`. Governance-critical tasks require PREMIUM minimum.

### RTCFX (Real-Time Compilation & Feedback eXecution)

Governs how NeuroForge learns from inference outcomes:

```
Inference Result → Anti-Gaming Check → Significance Gate → Learning Ledger → Shadow Compiler
```

**Invariants (NON-NEGOTIABLE):**
1. The compiler NEVER asserts truth about outputs
2. The compiler NEVER signs learning entries
3. The compiler NEVER auto-promotes a model or prompt variant
4. All learning is versioned and gated — no silent updates

### MAID (Multi-AI Inference Deliberation)

Parallel multi-model consensus validation for high-stakes outputs:
- Runs parallel batches across providers (OpenAI, Anthropic, Google, XAI, Ollama)
- Statistical consensus scoring
- Low-consensus → escalation; high-consensus → return
- 50% cost savings via batch API parallelism

### Patch-Task Governance Contract (MAPO → NeuroForge → MRPA)

Patch tasks are governed by explicit MAPO bindings:
- request must include `mapo_root_hash`, `workspace_root`, and `patch_targets` (inline) or `patch_targets_ref`
- `generated_from.root_hash` must match request `mapo_root_hash`
- `workspace_root` and resolved `patch_targets_ref` must stay under trusted roots
- evaluator rejects out-of-range patch output with non-recoverable governance codes (`MAPO-TGT-GATE-*`)

Capability status:
- NeuroForge exposes `patch_tasks_enabled` on `/health`, `/health/ready`, and `/ready`
- `true` only when trusted workspace roots are configured and valid

Current integration note:
- ForgeHUD has a deterministic `category + error_code` routing utility for patch-contract failures
  (`forge-smithy/src/lib/errors/patchContractRouting.ts`), but broad runtime adoption in all
  pipeline error surfaces is still in progress.

### MAPO (Multi-AI Planning Orchestration)

Sequential brainstorming across models for planning tasks. Uses SSE streaming for real-time progress.

### 3-Layer Prompt Cache

| Layer | Mechanism | Threshold | Avg Latency |
|-------|-----------|-----------|-------------|
| L1 | Redis SHA-256 exact hash | Exact match | ~1.5ms |
| L2 | MinHash pre-screen (128 perms) | Jaccard >85% | ms range |
| L3 | Jaccard similarity (token-level) | 95% threshold | ms range |

### Psychology System

9 behavioral frameworks (Big 5 OCEAN, Self-Determination Theory, Learning Modalities, Decision Styles, Flow Theory, Growth/Fixed Mindset, Cognitive Load Theory, Behavioral Economics, Habit Formation) for user/team profiling.

---

## DataForge — Search & Persistence Engine

### Hybrid Search Pipeline

```
Query → Embedding (Voyage AI, 1536-dim) → pgvector ANN (cosine)
     → PostgreSQL TSVECTOR → BM25 ranking
     → Both sets merged via Reciprocal Rank Fusion (RRF)
     → Filtered by similarity threshold (default 0.7)
```

**RRF formula:** `RRF_score(d) = Σ 1/(k + rank_i(d))` where `k=60`
**Measured improvement:** +40% accuracy over pure semantic search

### Document-to-Chunk Pipeline

```
Document (full text) → Text Splitter (500 tokens, 50 overlap)
→ Chunk records → Embedding generation (Voyage AI, batch)
→ pgvector column update (1536-dim) → TSVECTOR column update
```

Runs synchronously for small documents; deferred via Celery for large batches.

### Execution Index Pattern

Two-layer fast-path for run queries:
- `ExecutionIndex` — denormalized, sub-millisecond status lookups (no joins)
- `RunEvidence` — full JSONB evidence blobs for deep inspection

### Authentication Stack

| Layer | Implementation |
|-------|---------------|
| JWT (HS256) | Token issuance + validation |
| OAuth2/OIDC | Google, GitHub, Microsoft providers |
| TOTP 2FA | QR setup + 10 backup codes |
| API Keys | Service-to-service authentication |
| Field Encryption | AES-256 Fernet for PII columns |

### Anomaly Detection

6 threat pattern detectors run inline with authentication:
- Brute force detection
- Account enumeration
- Privilege escalation attempts
- Unusual access patterns
- Geographic anomalies
- Temporal anomalies

### Audit Log

Append-only, HMAC-SHA256-signed event log. No update or delete operations exist. Tamper detection via signature verification.

---

## Rake — Ingestion Pipeline

### 5-Stage Pipeline

| Stage | File | Input | Output |
|-------|------|-------|--------|
| FETCH | `fetch.py` + source adapters | Job params | `list[RawDocument]` |
| CLEAN | `clean.py` | `RawDocument` | `list[CleanedDocument]` |
| CHUNK | `chunk.py` / `semantic_chunker.py` | `CleanedDocument` | `list[Chunk]` |
| EMBED | `embed.py` | `Chunk` | `list[Embedding]` |
| STORE | `store.py` | `Embedding` | `list[StoredDocument]` (in DataForge) |

### Source Adapters

| Adapter | Sources | Key Behavior |
|---------|---------|-------------|
| `file_upload.py` | PDF, DOCX, PPTX, TXT, Markdown | pdfplumber preferred, pypdf fallback |
| `url_scrape.py` | Web pages | robots.txt compliance, rate limiting |
| `sec_edgar.py` | SEC filings | 10-K, 10-Q, 8-K; SEC user-agent required |
| `api_fetch.py` | REST APIs | GET/POST, auth types (api_key/bearer/basic) |
| `database_query.py` | SQL databases | SELECT only, read-only enforcement |

### Chunking Strategies

| Strategy | Method | Best For |
|----------|--------|---------|
| Token-based | Fixed token window + overlap | General documents |
| Semantic | sentence-transformers boundary detection | Technical content |
| Hybrid | Token with semantic boundary adjustment | Mixed content |

### Research Mission Lifecycle (11 states)

```
CREATED → STRATEGIZING → STRATEGY_REVIEW → APPROVED → DISCOVERING
→ CURATING → INGESTING → COMPLETING → COMPLETED
(+ FAILED, CANCELLED as terminal states)
```

- **STRATEGIZING:** Calls NeuroForge to generate search strategy
- **DISCOVERING:** Searches via Tavily/Serper for source URLs
- **CURATING:** Calls NeuroForge to evaluate and rank sources
- **INGESTING:** Runs full 5-stage pipeline per approved source
- **Cost tracking:** Per-phase budget enforcement via `budget_enforcer.py`

---

## ForgeAgents — Agent Execution Engine

### 5-Phase Execution Loop

```
PLAN → ACT → OBSERVE → REFLECT → DECIDE (→ loop / stop / escalate)
```

| Phase | Responsibility |
|-------|----------------|
| Plan | Decompose task, select tools, apply constraints |
| Act | Invoke tools via Tool Router (each pre-authorized by policy) |
| Observe | Collect tool outputs, detect errors |
| Reflect | Evaluate progress, update working memory, assess risk |
| Decide | Loop for another iteration, emit result, or escalate |

Default: max 10 iterations, 300-second timeout.

### Policy Engine (4-Category Enforcement)

Evaluation order: **Safety → Domain → Resource**. All tool calls are pre-authorized.

| Category | Policies | Examples |
|----------|----------|---------|
| Safety (5) | DestructiveAction, Confirmation, ContentSafety, FileSystemSafety, HealingScope | Block unauthorized writes, enforce healing tiers |
| Domain (4) | ToolAccess, DataAccess, ScopeRestriction, Permission | Role-based tool access |
| Resource (3) | RateLimit, Quota, CostTracking | 60 calls/min, $10/day cap |

### Deterministic Policy Envelope (Slices 1-3)

ForgeAgents now has an explicit split between runtime governance and offline learning prep.

| Slice | Status | Scope |
|-------|--------|-------|
| Slice 1 | Active | Deterministic hard gates (fail-closed policy load, call/token/cost/time caps, immutable run finalization) |
| Slice 2 | Active | Bandit routing + preference vector within Slice 1 guardrails |
| Slice 3 | Active (offline job only) | Deterministic offline proposal job that trains per-fingerprint updates from records and emits a proposed snapshot |

Slice 3 implementation lives in:
- `ForgeAgents/app/llm/policy_update_job.py` (core algorithm and schemas)
- `ForgeAgents/scripts/policy_update_job.py` (CLI entrypoint)
- `ForgeAgents/tests/unit/test_policy_update_job.py` (determinism/guardrail tests)

Offline job contract:
- Inputs: `current_policy_snapshot.json`, `strategy_records.jsonl`, deterministic `seed`, bounded/tripwire config.
- Outputs: `proposed_policy_snapshot.json`, `update_report.json`.
- Tripwires fail closed: quality regression, cost blowup, latency blowup, coverage gaps, and canonical hash instability reject the proposal.
- Job does not change live routing. Activation/promotion remains out of scope for this slice.

### BugCheck Finding Lifecycle State Machine

```
NEW → TRIAGED → FIX_PROPOSED → APPROVED → APPLIED → VERIFIED → CLOSED
  ↘ DISMISSED (requires reason + scope + expiration)
```

Enforced at the DataForge API level. Invalid transitions return 409 Conflict. After FINALIZED, no new findings accepted.

### Finding Fingerprinting

| Category | Fingerprint Composition |
|----------|------------------------|
| Default | `hash(category:rule_id:file_path:line_range:normalized_message)` |
| API Contract Drift | `hash(service + schema_path + field_name + change_type)` |
| Dependency CVE | `hash(package_name + version_range + cve_id)` |
| Endpoint Failure | `hash(service + endpoint + method + status_class)` |
| Flaky Test | `hash(test_file + test_name + failure_signature)` |

### Finding Severity Levels

| Level | Name | Gating Behavior |
|-------|------|----------------|
| S0 | Release Blocker | Blocks all merges and deployments |
| S1 | High | Blocks PR merge |
| S2 | Medium | Warning only |
| S3 | Low | Informational |
| S4 | Info | Advisory only |

### 35 Execution Nodes (7 Tiers)

| Tier | Name | Nodes | Purpose |
|------|------|-------|---------|
| T0 | Control | 5 | Authority gates, scope fences, token validation |
| T1 | Intelligence | 5 | Code analysis, pattern detection, risk assessment |
| T2 | Specialist | 8 | Language/domain-specific (TS, Python, Rust, Build, Test, Docs, Migration, Config) |
| T3 | Verification | 5 | BuildGuard, test, security, quality gate, contract verification |
| T4 | Planning | 4 | Plan construction, validation, constraint compilation, rollback |
| T5 | Integration | 4 | DataForge, NeuroForge, Rake, external service bridges |
| T6 | Release | 4 | Deployment, rollback, environment promotion, release validation |

### Intelligence Routing (XAI/MAID)

**XAI routing thresholds:**
- Category = security → Always route
- Category = dependency and severity ≥ S2 → Route
- Confidence < 0.6 → Route for context
- Category = lint/format → Never route

**Cost limits per run:**
- XAI: max 50 API calls
- MAID: max 20 fix proposals
- Monthly cap with 80% alerting

### Sentinel Agent — Health Monitoring & Self-Healing

Sentinel is an Ecosystem archetype specialization that monitors ecosystem health and performs tiered healing.

#### 6 Diagnostic Dimensions

| Dimension | ID | Checks | Sweep Type |
|-----------|----|--------|------------|
| Service Liveness | D1 | HTTP health endpoints across 5 services | Light + Deep |
| Connectivity | D2 | Inter-service connectivity verification | Deep only |
| Circuit Breakers | D3 | Open/half-open breaker detection | Light + Deep |
| Degradation Consistency | D4 | Cross-service degradation correlation | Deep only |
| Config Coherence | D5 | Environment variables, feature flags | Deep only |
| Token Authority | D6 | Token issuance and validation health | Light + Deep |

**Sweep schedules:** Light sweeps (D1+D3+D6) every 5 minutes (<10s). Deep sweeps (D1-D6) on-demand or anomaly-triggered (30-60s).

#### 3 Autonomy Tiers

| Tier | Label | Actions | Approval |
|------|-------|---------|----------|
| A | Autonomous | cache_flush, breaker_reset, job_retry | None (rate-limited: 3/hour) |
| B | Supervised | config_sync, schema_sync, multi_repo_edit | ForgeCommand approval required |
| C | Escalation | Critical incidents, unresolvable degradation | Human operator only |

**HealingScopePolicy** enforces tier boundaries with cooldowns (15 min cache flush, 10 min breaker reset) and frequency limits (3 autonomous actions/hour). All sweep results and healing events persist to DataForge.

---

*For per-service internals deep dives, see each service's own `doc/system/` backend internals chapter. For AI integration details, see §12. For database schemas, see §11.*

---

# §10 — Ecosystem Integration

This is the most critical chapter. It defines how the core services connect, what each subsystem is authorized to do, and how data and authority flow across the ecosystem.

---

## Master Integration Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ForgeCommand (8003)                               │
│                ForgeCommand API (8004, local boundary)                    │
│              Orchestration · API Key Vault · Run Lifecycle                │
│   Creates runs · Issues run_tokens · Finalizes runs · Syncs secrets      │
└───────┬──────────────┬──────────────┬──────────────┬─────────────────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│  NeuroForge  │ │ ForgeAgents  │ │     Rake     │ │   Consumer Apps      │
│   (8000)     │ │   (8010)     │ │   (8002)     │ │ SMITH · VibeForge    │
│              │ │              │ │              │ │ AuthorForge · Cortex  │
│ Inference    │ │ Agents +     │ │ Ingestion    │ │                      │
│ MAID · MAPO  │ │ BugCheck +   │ │ Research     │ │ (No credential own.) │
│              │ │ Sentinel     │ │              │ │                      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────────────────────┘
       │                │                │
       │         ┌──────┘                │
       │         │   ┌───────────────────┘
       ▼         ▼   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        DataForge (8001)                                    │
│                   SINGLE SOURCE OF TRUTH                                  │
│                                                                           │
│  29 Routers · 80+ Endpoints · 31+ ORM Models · Hybrid Search             │
│  PostgreSQL + pgvector + Redis · Audit Log · Lifecycle Enforcement        │
└──────────────────────────────────────────────────────────────────────────┘
```

---

The map above is the live service integration mesh. Forge Eval is deliberately separate from that mesh because it evaluates sibling repositories as a standalone CLI/repository subsystem rather than participating as a long-running network service.

## Integration Principles

1. **Every service authenticates.** No endpoint accepts unauthenticated writes.
2. **Scope is enforced, not suggested.** A service writing outside its scope receives 403 Forbidden.
3. **DataForge is the record.** Services may cache reads locally but must never treat cache as authoritative.
4. **Fail loudly.** When DataForge is unavailable, services must fail — not degrade silently.
5. **API keys never cross IPC boundaries.** Keys are injected server-side from ForgeCommand vault.

### Forge Eval Boundary in the Ecosystem

- **Forge Eval owns evaluation computation.** It computes deterministic eval artifacts from sibling repository state.
- **SMITH owns authority.** Governance decisions, approvals, and final human-authoritative calls remain outside Forge Eval.
- **DataForge owns durable persistence.** Forge Eval does not currently act as the ecosystem truth store.
- **Target repositories remain subjects.** Forge Eval evaluates them; it does not become part of their runtime ownership boundary.
- **Current implemented path runs through Pack M.** `risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate -> hazard map -> merge decision -> evidence bundle`

### Eval Cal Node Boundary in the Ecosystem

- **Eval Cal Node is post-implementation and post-reconciliation.** It never operates on in-flight implementation state.
- **Eval Cal Node does not alter Forge Eval.** It does not change stage order, artifact contracts, fail-closed doctrine, or approved parameter revisions directly.
- **Eval Cal Node only emits proposals.** Candidate calibration proposals require explicit human approval at the Gate 3 math-effect boundary before any approved Eval parameter revision changes.
- **Eval Cal Node uses local structured JSON.** No DataForge write contract required for v0. Persistence is append-only for records; proposals are immutable once written.

---

## Access Control Matrix

| Component | Authorized Writes to DataForge | Auth Token |
|-----------|-------------------------------|------------|
| **ForgeCommand** | Run records, lifecycle transitions, run finalization, token rotation, secrets sync | admin token |
| **BugCheck** | Findings, progress events, check telemetry | run_token (scoped to run) |
| **XAI/MAID** | Enrichment artifacts only | run_token |
| **VibeForge** | User decisions (lifecycle transitions), projects, sessions | user_token / API key |
| **NeuroForge** | Inference records, run logs, model performance | API key |
| **AuthorForge** | Books, chapters, scenes, characters, arcs, manuscripts | API key |
| **Rake** | Job records (local DB), documents via DataForge client | API key |
| **SMITH** | Planning sessions, portfolio, evaluation snapshots, governance events | API key |
| **ForgeAgents** | Agent registry, execution records, evidence | admin token / API key |
| **Sentinel** | Sweep results, healing events (via ForgeAgents) | API key |
| **Forge Eval** | None in current Pack M runtime; emits local schema-locked artifacts | — |
| **Eval Cal Node** | None; emits local calibration proposals and evidence artifacts | — |

**Violations are security events.** Unauthorized write attempts are rejected, logged as security events, and the caller receives no helpful error message.

### Forge Eval Integration Doctrine

Forge Eval sits beside the runtime services and evaluates sibling repositories through local git/file inspection. Its emitted artifacts may later be consumed by SMITH for governance workflows or stored by DataForge for historical analysis, but those downstream responsibilities do not move into Forge Eval itself.

---

## Integration Contract Registry

### NeuroForge → DataForge

| Operation | Endpoint | Purpose |
|-----------|----------|---------|
| RAG context fetch | `POST /context/fetch` | Retrieve top-k knowledge chunks |
| Log run start | `POST /api/neuroforge/runs` | Create run record |
| Log model results | `POST /api/neuroforge/runs/{id}/results` | Store per-model output |
| Log inference | `POST /api/neuroforge/inferences` | Individual inference record |
| Retrieve context | `GET /api/neuroforge/context` | Hybrid search for query context |

**Fallback:** SQLite cache (`neuroforge_fallback.db`) when DataForge unreachable. Circuit breaker in `context_builder_fixed.py`.

### NeuroForge ← Consumer Services

| Caller | Endpoint | Purpose |
|--------|----------|---------|
| AuthorForge | `/api/v1/authorforge/*` | Literary suggestions, style analysis, entity extraction |
| VibeForge | `/api/v1/infer`, `/api/v1/team-learning/*` | Psychology profiling, team learning |
| Rake | `/api/v1/research/sessions`, `/api/v1/inference` | Research strategy, claim analysis |
| ForgeAgents/BugCheck | `/api/v1/maid/validate` | Multi-model consensus for finding enrichment |
| SMITH Assist | MAID consensus (via ForgeAgents proxy) | Governance query validation |

### ForgeAgents → DataForge

| Operation | Endpoint | Auth |
|-----------|----------|------|
| Register agent | `POST /api/agents-registry` | admin token |
| Log execution | `POST /forge-runs` | API key |
| Store evidence | `POST /forge-runs/{id}/evidence` | API key |
| BugCheck findings | `POST /api/bugcheck/runs/{id}/findings` | run_token |
| BugCheck progress | `POST /api/bugcheck/runs/{id}/progress` | run_token |
| Sentinel sweeps | `POST /api/v1/sentinel/sweeps` | API key |
| Sentinel healing | `POST /api/v1/sentinel/healing` | API key |
| Memory (read/write) | Via DataForge tool adapter | API key |

### ForgeAgents → NeuroForge

| Operation | Purpose |
|-----------|---------|
| `generate_embedding` | Memory indexing (768-dim vectors) |
| `infer_model` | Agent planning (Plan phase) |
| `semantic_similarity` | Memory retrieval ranking |

### Rake → DataForge

| Operation | Purpose |
|-----------|---------|
| Document storage | Persist ingested documents + chunks + embeddings |
| Job record sync | Pipeline status and metrics |

### Rake → NeuroForge

| Operation | Purpose |
|-----------|---------|
| Strategy generation | AI-driven research strategy creation |
| Source curation | AI evaluation and ranking of discovered sources |

### AuthorForge → DataForge

| Operation | Endpoint | Purpose |
|-----------|----------|---------|
| List/create/update projects | `/api/projects` | Project CRUD (AuthorForge v2) |
| List/create/update docs | `/api/projects/{id}/chapters` | Document persistence (chapters) |
| List/create/delete entities | `/api/projects/{id}/entities` | Lore entity persistence |
| Health check | `/health` | DataForge availability |

**Fallback:** If DataForge is unavailable, writes fail — AuthorForge does not maintain its own authoritative store.

### AuthorForge → NeuroForge

| Operation | Endpoint | Purpose |
|-----------|----------|---------|
| Text generation | `/api/v1/inference` | Scene drafting, literary suggestions |
| Embedding | `/api/v1/embeddings` | Text vectorization for RAG |
| Entity extraction | `/api/v1/authorforge/extract-entities` | NLP-based lore extraction |
| Style analysis | `/api/v1/authorforge/style-analysis` | Writing style profiling |

**Fallback:** Generation returns `[DRAFT PLACEHOLDER]`. Embedding falls back to zero vectors. Entity extraction silently skips.

---

## Cross-Service Data Lifecycle

### Knowledge Ingestion Flow

```
1. ForgeCommand initiates mission via Rake
2. Rake STRATEGIZES → calls NeuroForge for strategy generation
3. Rake DISCOVERS → searches via Tavily/Serper
4. Rake CURATES → calls NeuroForge to evaluate sources
5. Rake INGESTS → runs 5-stage pipeline (FETCH→CLEAN→CHUNK→EMBED→STORE)
6. Rake STOREs → persists to DataForge
7. NeuroForge QUERIEs → retrieves chunks for RAG context
8. Consumer apps CONSUME → use enriched inference results
```

### Quality Check Flow (BugCheck)

```
1. ForgeCommand creates run record in DataForge, issues run_token
2. ForgeAgents/BugCheck detects service stacks via topology
3. BugCheck runs checks (typecheck, lint, tests, security, contracts)
4. Findings written to DataForge (requires run_token)
5. Eligible findings routed to XAI (external context enrichment)
6. Enriched findings routed to MAID (fix proposal generation)
7. All enrichments persisted to DataForge
8. ForgeCommand finalizes run — immutable after FINALIZED
9. VibeForge users triage/approve/dismiss via user_token
```

### Health Sweep Flow (Sentinel)

```
1. Sentinel triggered (scheduled light sweep or manual deep sweep)
2. HealthAdapter runs diagnostic dimensions (D1-D6) across services
3. Dimension results aggregated → overall_status (healthy/degraded/critical)
4. Sweep results persisted to DataForge (sentinel_sweeps)
5. If degraded/critical → healing playbook selected based on findings
6. HealingScopePolicy checks tier + cooldowns + frequency limits
7. Tier A: autonomous execution → outcome to DataForge
8. Tier B: request ForgeCommand approval → execute on approval
9. Tier C: escalate to human operator (no autonomous action)
```

### API Key Flow

```
ForgeCommand vault (~/.forge-command/local.db)
  │
  ├── Rust Broker (injects auth headers, keys never reach UI)
  │     │
  │     ├──► NeuroForge (authenticated HTTP)
  │     ├──► DataForge (authenticated HTTP)
  │     ├──► ForgeAgents (authenticated HTTP)
  │     └──► Rake (authenticated HTTP)
  │
  └── /secrets sync endpoint → DataForge vault
        └──► Services retrieve keys at runtime
```

---

## Token Semantics

### run_token

| Property | Value |
|----------|-------|
| Issuer | ForgeCommand |
| TTL | 30 minutes (max 60) |
| Scope | Bound to `{run_id, targets, mode, scope, commit_sha}` |
| Replay protection | Includes nonce (single-use for writes) |
| Authorized operations | Write findings, progress events, enrichment |

A run_token for run A cannot write findings to run B.

### user_token

| Property | Value |
|----------|-------|
| Issuer | VibeForge (on behalf of authenticated user) |
| Operations | Triage, approve, dismiss findings |
| Prohibited | Writing findings, writing enrichment |

Neither token grants lifecycle transition authority to BugCheck or ForgeAgents. That authority belongs exclusively to ForgeCommand.

---

## Dependency Availability Matrix

| Service | DataForge | NeuroForge | Rake | ForgeCommand |
|---------|-----------|------------|------|-------------|
| **NeuroForge** | REQUIRED (RAG) | — | — | Optional (keys) |
| **DataForge** | — | — | — | Optional (secrets) |
| **ForgeAgents** | **REQUIRED** | Optional | Optional | Optional |
| **Rake** | REQUIRED (storage) | Optional (strategy) | — | Optional (keys) |

**REQUIRED = run does not start without it.** Optional = graceful degradation with explicit flagging.

---

## Failure Cascade Analysis

### DataForge Down

| Affected Service | Impact |
|-----------------|--------|
| NeuroForge | Falls to SQLite fallback (CACHE_ONLY mode), no new knowledge |
| ForgeAgents | Refuses to start runs, returns 503 on `/ready` |
| Rake | Cannot store documents, pipeline fails at STORE stage |
| All | No durable state persistence — ecosystem halted |

### NeuroForge Down

| Affected Service | Impact |
|-----------------|--------|
| ForgeAgents | Direct LLM API fallback, memory without embeddings, "degraded enrichment" flag |
| Rake | Research missions cannot generate strategy/curate sources; standard ingestion unaffected |
| AuthorForge | All endpoints return empty arrays (hardened failure contract) |
| Consumer Apps | No AI inference available |

### ForgeCommand Down

| Affected Service | Impact |
|-----------------|--------|
| All backend services | Continue operating with local env var keys |
| ForgeAgents | Standalone mode (no approval routing, no desktop integration) |
| BugCheck | Cannot start new runs (no run_token issuance) |
| Sentinel | Tier B healing blocked (no approval authority); Tier A continues |

---

*For per-service integration details, see each service's own `doc/system/` integration chapter. For API contracts, see §8. For error handling, see §13.*

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

# §12 — AI Integration

## LLM Provider Matrix

NeuroForge orchestrates access to 5 LLM providers across 3 performance tiers.

### Providers

| Provider | API | Models | Primary Use |
|----------|-----|--------|-------------|
| **OpenAI** | Chat Completions v1 | GPT-4o, GPT-4o-mini | General inference, embeddings (fallback) |
| **Anthropic** | Messages v1 | Claude 3.5 Sonnet, Claude 3 Haiku | MAID consensus, planning, code analysis |
| **Google** | Gemini v1 | Gemini 1.5 Pro, Gemini 1.5 Flash | MAID consensus, ensemble voting |
| **xAI** | Chat Completions v1 | Grok-2 | BugCheck XAI enrichment, context lookup |
| **Ollama** | OpenAI-compatible | Llama 3, Mistral, CodeLlama | Local/offline fallback, development |

### Model Tiers

| Tier | Capability | Examples | Fallback |
|------|-----------|----------|----------|
| **PREMIUM** | Highest quality, highest cost | GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro | → STANDARD |
| **STANDARD** | Balanced quality/cost | GPT-4o-mini, Claude 3 Haiku, Gemini 1.5 Flash | → FAST |
| **FAST** | Lowest latency, lowest cost | Ollama local models | → OFFLINE mode |

Governance-critical tasks (evidence signing, run finalization) require PREMIUM minimum.

---

## NeuroForge 5-Stage Inference Pipeline

Every inference request traverses all five stages in sequence. No bypass allowed.

```
Query → Context Builder → Prompt Engine → Model Router → Evaluator → Post-Processor → Response
```

| Stage | File | Input | Output |
|-------|------|-------|--------|
| **Context Builder** | `context_builder_fixed.py` | Query text | RAG chunks from DataForge |
| **Prompt Engine** | `prompt_engine.py` | Query + context + domain | Rendered prompt |
| **Model Router** | `model_router.py` | Prompt + strategy | LLM response |
| **Evaluator** | `evaluator.py` | LLM output | Quality score (0.0-1.0) |
| **Post-Processor** | `post_processor.py` | Evaluated output | Normalized response |

**NOTE:** `context_builder.py` is a guard stub (raises `ImportError`). Always use `context_builder_fixed.py`.

---

## Model Routing Strategies

The Model Router selects models using one of four strategies per request:

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| **CHAMPION_SELECTION** | Pick the model with highest EMA score for domain+task_type | Default — best historical performer |
| **ENSEMBLE_VOTING** | Run multiple models, consensus scoring | High-stakes decisions |
| **COST_OPTIMIZATION** | Cheapest model that meets quality threshold | Budget-constrained tasks |
| **QUALITY_OPTIMIZATION** | Best-performing model regardless of cost | Governance-critical tasks |

### Champion Model Selection

Each `(domain, task_type)` pair maintains an Exponential Moving Average (EMA) quality score per model. The champion is the model with the highest EMA. Updated after every inference via RTCFX (see below).

### Fallback Chain

```
Provider failure → Try next model in tier by EMA score
All models in tier fail → Drop to next tier: PREMIUM → STANDARD → FAST
All tiers exhausted → OFFLINE mode (see §13)
```

---

## Prompt Engineering

### Domain Templates

NeuroForge uses domain-specific prompt templates that inject context, constraints, and style guidance:

| Domain | Template Focus |
|--------|---------------|
| Literary | Narrative craft, character development, genre conventions |
| Market analysis | Financial data, trend analysis, investment thesis |
| Technical | Code analysis, architecture, documentation |
| Research | Source evaluation, claim verification, evidence synthesis |
| General | Balanced general-purpose template |

### Task Types (6)

| Task Type | Description |
|-----------|-------------|
| `generation` | Create new content |
| `analysis` | Analyze existing content |
| `evaluation` | Score or judge content quality |
| `summarization` | Condense content |
| `extraction` | Pull structured data from text |
| `classification` | Categorize content |

---

## MAID — Multi-AI Inference Deliberation

Parallel multi-model consensus validation for high-stakes outputs.

### How It Works

1. **Fan-out:** Send the same prompt to multiple providers simultaneously (batch API)
2. **Collect:** Gather all responses with token counts and latency
3. **Score:** Statistical consensus scoring across responses
4. **Decide:** High consensus → return; low consensus → escalation

### Configuration

| Parameter | Value |
|-----------|-------|
| Max parallel providers | 5 |
| Min consensus threshold | Configurable per domain |
| Budget cap per run | 20 fix proposals |
| Batch API savings | ~50% cost reduction |
| Monthly aggregate cap | With 80% alerting threshold |

### Consensus Escalation

- **High consensus** → Return response directly
- **Low consensus** → Flag for human review or additional provider pass
- **Contradictory responses** → Route to governance for adjudication

---

## MAPO — Multi-AI Planning Orchestration

Sequential brainstorming across models for planning tasks (distinct from MAID's parallel consensus).

1. **Initial plan** — First model generates a plan
2. **Review** — Second model critiques and refines
3. **Refinement** — Additional models iterate
4. **Final synthesis** — Coordinator model produces final plan

Uses SSE streaming for real-time progress delivery to forge-smithy.

---

## RTCFX — Real-Time Compilation & Feedback eXecution

Governs how NeuroForge learns from inference outcomes. This is the ecosystem's governed learning loop.

### Pipeline

```
Inference Result → Anti-Gaming Check → Significance Gate → Learning Ledger → Shadow Compiler
```

| Stage | Purpose |
|-------|---------|
| **Anti-Gaming Check** | Detects manipulation attempts (feedback spam, synthetic scores) |
| **Significance Gate** | Filters noise — only meaningful signal passes through |
| **Learning Ledger** | Append-only, versioned record of all learning events |
| **Shadow Compiler** | Updates model scores and routing weights |

### Invariants (NON-NEGOTIABLE)

1. The compiler **NEVER asserts truth** about outputs
2. The compiler **NEVER signs** learning entries
3. The compiler **NEVER auto-promotes** a model or prompt variant
4. All learning is **versioned and gated** — no silent updates

---

## XAI Integration (BugCheck)

External context enrichment for BugCheck findings via xAI (Grok).

### Routing Thresholds

| Condition | Action |
|-----------|--------|
| Category = security | Always route to XAI |
| Category = dependency AND severity ≥ S2 | Route to XAI |
| Category = deprecation | Route for doc lookup |
| Confidence < 0.6 | Route for additional context |
| Category = lint/format | Never route (skip XAI) |

### Caching Policy

| Source | TTL |
|--------|-----|
| CVE lookups | 24 hours |
| Documentation | 7 days |
| Stack Overflow | 48 hours |

Cache is stored in DataForge (durable, queryable, auditable) — not Redis.

### Degradation

| Condition | Behavior |
|-----------|----------|
| XAI unavailable | Proceed MAID-only, flag as "degraded enrichment" |
| MAID unavailable | Report findings without fix proposals, flag as "analysis pending" |
| Both unavailable | Complete with raw findings only, alert operator |

---

## Embedding Models

### Primary: Voyage AI

| Parameter | Value |
|-----------|-------|
| Model | `voyage-large-2` |
| Dimensions | 1536 |
| Distance metric | Cosine similarity |
| Index type | IVFFlat (pgvector) |
| Batch size | Configurable |

### Fallback: OpenAI

| Parameter | Value |
|-----------|-------|
| Model | `text-embedding-3-small` |
| Dimensions | 1536 |
| Fallback trigger | Voyage AI unavailable |

### Where Embeddings Are Used

| Service | Purpose | Store |
|---------|---------|-------|
| DataForge | Document chunk embeddings for hybrid search | `chunks.embedding` (pgvector) |
| Rake | Pipeline EMBED stage — generates embeddings for ingested content | Writes to DataForge |
| ForgeAgents | Long-term memory storage — episodic and semantic recall | DataForge via pgvector |

**Constraint:** Embedding dimension (1536) is hardcoded in multiple locations. Changing the embedding model requires a coordinated migration: rebuild pgvector indexes in DataForge, re-embed all existing chunks.

---

## 3-Layer Prompt Cache

NeuroForge caches prompt-response pairs in three layers for latency reduction:

| Layer | Mechanism | Match Threshold | Avg Latency |
|-------|-----------|----------------|-------------|
| **L1** | Redis SHA-256 exact hash | Exact match | ~1.5ms |
| **L2** | MinHash pre-screen (128 perms) | Jaccard > 85% | ms range |
| **L3** | Jaccard similarity (token-level) | 95% threshold | ms range |

L1 is a Redis key-value lookup. L2/L3 detect near-duplicate prompts to avoid re-computing similar requests.

---

## Psychology System

9 behavioral frameworks for user and team profiling, used to personalize inference outputs:

| Framework | Application |
|-----------|------------|
| Big 5 OCEAN | Personality-aware response framing |
| Self-Determination Theory | Motivation alignment |
| Learning Modalities | Presentation format optimization |
| Decision Styles | Recommendation structuring |
| Flow Theory | Complexity calibration |
| Growth/Fixed Mindset | Feedback framing |
| Cognitive Load Theory | Information density management |
| Behavioral Economics | Choice architecture |
| Habit Formation | Workflow suggestions |

---

## Cost Controls

### Per-Run Limits

| Resource | Cap |
|----------|-----|
| XAI API calls per BugCheck run | 50 |
| MAID fix proposals per BugCheck run | 20 |
| Monthly aggregate cost | Configurable with 80% alerting |

### Research Mission Budgets

| Parameter | Range |
|-----------|-------|
| Cost cap per mission | $0.01 - $50.00 (default: $2.00) |
| Warning threshold | 80% of cap |
| Critical threshold | 95% of cap |
| Budget exceeded | Mission halted; state preserved; can resume with higher cap |

Cost tracking is per-phase: search, scrape, embedding, LLM — each tracked independently.

---

## Consumer Integration Pattern

How downstream services consume NeuroForge AI capabilities (using SMITH Assist as the reference implementation):

### 1. Assemble Context (Client-Side)

```typescript
// forge-smithy: contextAssembler.ts
const context: SAEContext = {
  pipeline: pipelineStore.state,
  readiness: governanceStore.readiness,
  drift: smelterDriftStore.report,
  route: currentRoute,
};
```

### 2. Classify Intent (Client-Side)

```typescript
// forge-smithy: queryClassifier.ts
const classification: QueryClassification = classifyQuery(userMessage);
// → { intent: 'STATUS_CHECK', tier: 'BRIEFING', confidence: 0.92 }
```

### 3. Invoke via Tauri IPC (No API Keys Cross Boundary)

```typescript
// forge-smithy → Rust → NeuroForge
const response = await invoke<AssistResponse>('smith_assist_query', {
  message: userMessage,
  frontendContext: flattenContext(context),
  classification,
});
```

### 4. Rust Backend Calls NeuroForge

API keys are injected server-side from ForgeCommand vault. The frontend never sees credentials.

---

*For inference pipeline internals, see §9. For LLM provider degradation modes, see §13. For embedding schema details, see §11. For SMITH Assist SAE modules, see §7.*

---

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

---

# §14 — Testing

Test posture, QA tiers, severity gates, and fail-closed expectations are canonical in this chapter. Test totals, coverage percentages, load-test tallies, and suite counts are audit-derived snapshot values unless the number is part of the QA model itself (for example `T0-T6` or `S0-S4`).

## Ecosystem Testing Snapshot

| Service | Framework | Tests | Coverage | Target |
|---------|-----------|-------|----------|--------|
| NeuroForge | pytest + Locust | 100+ | 89%+ | 89%+ |
| DataForge | pytest + k6 | 296 | 82% | 85%+ |
| ForgeAgents | pytest | 62 contract + unit | ~70% | 85% |
| Rake | pytest | unit + integration | 80%+ | 80%+ |
| Forge Eval | pytest + CLI smoke verification | unit + integration + deterministic real-run checks | Byte-stable artifacts on identical input | Deterministic Pack J pipeline |

All Python services use **pytest** with **pytest-asyncio** (`asyncio_mode = auto`). All Python codebases use **ruff** for linting and **mypy** where type checking is part of the local contract. Forge Eval extends this posture with artifact schema validation, explicit fail-closed checks, and byte-stability assertions across repeated runs.

---

## Test Categories Across the Ecosystem

### Unit Tests

Every service isolates unit tests from external dependencies. All I/O is mocked.

| Service | Key Areas Tested |
|---------|-----------------|
| NeuroForge | Pipeline stages (context builder, prompt engine, model router, evaluator, post-processor), champion model EMA, RTCFX compiler + significance gate + anti-gaming, psychology frameworks, circuit breaker state machine, token validation |
| DataForge | JWT creation/validation, Fernet encryption/decryption, rate limiting token bucket, anomaly detection (6 types), chunking + embedding logic, RRF merge correctness, fingerprint stability, lifecycle transitions, Pydantic schema validation |
| ForgeAgents | Policy engine evaluation order, tool router dispatch, memory tiers (short-term FIFO, long-term, episodic), lifecycle transitions (all valid + invalid), check fingerprint stability, XAI/MAID routing decisions |
| Rake | Source adapters (API fetch, URL scrape, SEC Edgar, database query), text processing, JWT auth, rate limiting |

### Integration Tests

| Service | Scope | External Dependencies |
|---------|-------|-----------------------|
| NeuroForge | Full 5-stage pipeline with mocked LLMs, DataForge client, RAG + fallback cache, MAID consensus, AuthorForge endpoint hardening | Mocked at HTTP boundary |
| DataForge | Hybrid search pipeline, admin API + auto-chunking, BugCheck router, NeuroForge/VibeForge/AuthorForge routers, teams API, cache failover, DB failover, DLQ replay | Live PostgreSQL + Redis (test DB) |
| ForgeAgents | Agent creation/execution/result retrieval, DataForge persistence, BugCheck run workflows | Mocked DataForge + NeuroForge |
| Rake | All `/api/v1/jobs` and `/api/v1/missions` endpoints, full mission lifecycle (create → approve → complete → evidence bundle) | Mocked services |
| Forge Eval | Real git-diff-driven stage execution, schema validation, deterministic reruns, controlled fail-closed scenarios | Tiny temp repos + real local sibling repo smoke runs |

### Security & Compliance Tests (DataForge)

DataForge has dedicated test categories that apply ecosystem-wide:

| Category | Tests |
|----------|-------|
| Security | OAuth2 flows, TOTP 2FA, run_token scope enforcement, API key security, JWT forgery/expiry/algorithm confusion |
| Compliance | GDPR erasure flow, PII field encryption, audit log HMAC integrity + append-only enforcement |

### Contract Tests (ForgeAgents)

62 contract tests in `tests/contracts/` verify cross-service payload conformance:
- Finding writes include all required DataForge fields
- `run_token` always present in finding requests
- API boundary enforcement (BugCheck cannot write lifecycle transitions)

### E2E Tests (DataForge)

Full workflow tests exercising multiple routers in sequence:
- BugCheck: create run → ingest findings → lifecycle transitions → finalize
- NeuroForge: inference → results → performance → context retrieval
- AuthorForge: book → chapters → scenes → manuscript compilation

### Load Tests

| Service | Tool | Scenarios |
|---------|------|-----------|
| NeuroForge | Locust 2.20 | Baseline inference (10 users, p95 < 2s), concurrent batch, RAG degraded mode, rate limit verification |
| DataForge | k6 | Search (1,000 RPS target, p95 < 100ms with 100K chunks), document ingestion |

---

## Running Tests — Per Service

### Forge Eval

```bash
cd forge-eval/repo

# Full test suite
pytest -q

# Determinism / stage coverage
pytest tests/ -q

# Build evidence binary
cd rust/forge-evidence && cargo build --offline

# Real local smoke run against a sibling repo
cd /home/charlie/Forge/ecosystem/forge-eval/repo
python3 -m forge_eval.cli run --repo /path/to/target-repo --base <base> --head <head> --config <config> --out <artifacts-dir>
python3 -m forge_eval.cli validate --artifacts <artifacts-dir>
```

Forge Eval testing is artifact-oriented rather than service-latency-oriented. The critical acceptance checks are deterministic artifact generation, strict schema validation, byte-identical reruns on identical input, fail-closed behavior under governed error cases, and smoke-run verification against sibling repositories through Pack J (`risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate`).

### NeuroForge

```bash
cd NeuroForge

# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=neuroforge_backend --cov-report=term-missing --cov-fail-under=89

# Skip rate limiting (CI)
SKIP_RATE_LIMIT=true pytest tests/

# Integration only
pytest tests/ -v -m integration

# API tests only
pytest tests/ -v -m api

# Load tests
locust -f tests/load/locustfile.py --headless -u 10 -r 2 --run-time 5m

# Type checking + linting
mypy src/
ruff check neuroforge_backend/
```

### DataForge

```bash
cd DataForge

# All tests
pytest tests/ -v

# With coverage
pytest --cov=app tests/ --cov-report=term-missing

# Security tests only
pytest tests/test_auth_security.py tests/test_run_token.py tests/test_jwt_security.py -v

# Compliance tests only
pytest tests/test_compliance_gdpr.py tests/test_audit_log.py -v

# BugCheck domain
pytest tests/test_bugcheck_api.py tests/test_bugcheck_access_control.py -v

# Load tests
k6 run scripts/load_test_search.js
```

**Test database setup:**
```bash
createdb dataforge_test
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dataforge_test \
  alembic upgrade head
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dataforge_test \
  pytest tests/ -m integration -v
```

### ForgeAgents

```bash
cd ForgeAgents

# All tests
pytest tests/ -v

# BugCheck tests only
pytest tests/agents/bugcheck/ -v

# Contract tests only
pytest tests/contracts/ -v

# With coverage
pytest tests/ --cov=app --cov-report=term-missing

# CI gate (85% minimum)
pytest tests/ --cov=app --cov-fail-under=85

# Type checking + linting
mypy app/
ruff check app/
ruff format app/
```

### Rake

```bash
cd rake

# All tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Skip external dependencies
pytest -m "not requires_openai and not requires_dataforge"
```

---

## Test Markers

| Marker | Service | Meaning |
|--------|---------|---------|
| `unit` | All | Fast, isolated, no external dependencies |
| `integration` | All | Requires DB or service mocks |
| `api` | NF | FastAPI endpoint tests |
| `security` | DF | Auth, token, and access control tests |
| `compliance` | DF | GDPR, encryption, audit tests |
| `e2e` | DF | Full workflow tests |
| `contract` | FA | Cross-service payload conformance |
| `slow` | All | Tests taking > 1 second |
| `requires_openai` | Rake | Needs `OPENAI_API_KEY` |
| `requires_dataforge` | Rake | Needs live DataForge |
| `requires_database` | Rake | Needs live PostgreSQL |

### Forge Eval Verification Truth

- Deterministic JSON artifact generation with stable ordering
- JSON schema validation for each emitted artifact
- Byte-stability comparisons across identical reruns
- Explicit fail-closed verification for invalid config, cap overflow, schema failure, and identity collisions
- Real smoke runs against sibling repositories in the Forge workspace
- Hidden-defect estimation coverage through Pack J (`capture_estimate.json`)

---

## Mocking Strategy

### LLM Provider Mocks

All services mock LLM providers at the HTTP boundary using `respx`, `pytest-httpx`, or `unittest.mock.patch`. Mock responses include realistic token counts, latency simulation, and structured outputs matching provider schemas.

### DataForge Mocks

DataForge is mocked at the HTTP boundary for upstream services:
- **Happy path:** Ranked chunk list with scores
- **Unavailable:** Connection refused (triggers circuit breaker in NeuroForge, prevents run start in ForgeAgents)
- **Partial:** Subset of expected chunks (tests score filtering)

### Redis Mocks

NeuroForge uses `fakeredis` for unit tests. Integration tests use a real Redis instance if available, skipping L1 cache tests if not.

---

## Key Test Fixtures

### NeuroForge
- Mock LLM providers (via `respx`/`pytest-httpx`)
- DataForge mock (happy path, unavailable, partial)
- Redis mock (`fakeredis`)

### DataForge
- `db_session` — Rollback-isolated database session (no state leaks between tests)
- `client` — FastAPI `TestClient` with overridden DB dependency
- `admin_token` — Valid admin JWT
- `run_token` — Scoped run_token for BugCheck tests

### ForgeAgents
- `app_client` — FastAPI `AsyncClient` with auth headers
- `mock_dataforge` — Patched DataForge service client
- `mock_neuroforge` — Patched NeuroForge service client
- `bugcheck_run` — Valid `BugCheckRun` in RUNNING state

### Rake
- `mock_telemetry` — TelemetryClient mock
- `mock_dataforge` — DataForgeClient mock
- `mock_embedding_service` — EmbeddingService mock
- `client` — FastAPI `TestClient`
- `sample_text`, `sample_html`, `sample_pdf_path`, `sample_chunks` — Test data

---

## Test Invariants (Non-Negotiable Coverage)

These scenarios **must** have test coverage across the ecosystem:

1. **Lifecycle transitions** — All valid and invalid transitions for `LifecycleState` (ForgeAgents, DataForge)
2. **Post-finalization rejection** — FINALIZED runs reject new findings with 409 (DataForge, ForgeAgents)
3. **XAI routing decisions** — Every category × severity combination (ForgeAgents)
4. **Policy evaluation order** — Safety before domain before resource (ForgeAgents)
5. **DataForge unavailability** — Run start rejection, circuit breaker trips (ForgeAgents, NeuroForge)
6. **run_token expiry** — 401 rejection on expired tokens (DataForge, ForgeAgents)
7. **API boundary violations** — BugCheck attempting lifecycle writes (DataForge, ForgeAgents)
8. **Fingerprint stability** — Same error at same location produces same fingerprint across runs (ForgeAgents)
9. **Rate limit enforcement** — 429 on excess requests (all services)
10. **AuthorForge hardening** — Empty response on LLM failure, never 5xx (NeuroForge)
11. **Audit log integrity** — HMAC verification, append-only enforcement (DataForge)
12. **Encryption round-trip** — PII encrypt/decrypt with Fernet (DataForge)

---

## CI/CD Requirements

### Pre-Merge Gates (All Services)

| Check | NeuroForge | DataForge | ForgeAgents | Rake |
|-------|-----------|-----------|-------------|------|
| `pytest` — 0 failures | Yes | Yes | Yes | Yes |
| Coverage minimum | 89% | 82%* | 85%* | 80% |
| `mypy` — 0 errors | Yes | Yes | Yes | Yes |
| `ruff check` — 0 violations | Yes | Yes | Yes | Yes |
| `ruff format --check` — no diffs | Yes | Yes | Yes | Yes |

\* Target; DataForge and ForgeAgents have known coverage gaps being actively closed.

### CI Tiers (Rake)

| Trigger | Tests Run |
|---------|-----------|
| Every commit | Unit tests only (exclude slow + external deps) |
| Pull request | Unit + integration (exclude external API deps) |
| Nightly | All tests including external service tests |

---

## Coverage Gaps & Priorities

| Service | Gap Area | Current | Target |
|---------|----------|---------|--------|
| DataForge | Admin router | 78% | 85%+ |
| DataForge | Domain-specific routers | 74% | 80%+ |
| ForgeAgents | `app/nodes/` (35 execution nodes) | Low | 80%+ |
| ForgeAgents | `app/capabilities/` registry | Minimal | 80%+ |
| ForgeAgents | `app/cortex/` multi-AI planning | Limited | Integration tests |
| ForgeAgents | `app/runner/` DAG execution | Limited | Integration tests |

---

## Test File Organization

### NeuroForge
```
tests/
├── unit/           # Pipeline stages, champion model, RTCFX, psychology
├── integration/    # Full pipeline, DataForge client, MAID, AuthorForge
├── api/            # FastAPI endpoint tests
└── load/           # Locust scenarios
```

### DataForge
```
tests/
├── test_auth.py, test_encryption.py, ...      # Unit tests
├── test_search_integration.py, ...            # Integration tests
├── test_auth_security.py, ...                 # Security tests
├── test_compliance_gdpr.py, ...               # Compliance tests
└── test_e2e_bugcheck_run.py, ...              # E2E workflow tests
```

### ForgeAgents
```
tests/
├── agents/bugcheck/    # BugCheck agent, checks, lifecycle, routing
├── contracts/          # 62 cross-service contract tests
├── test_api/           # API endpoint tests
├── test_policies/      # Policy engine tests
├── test_memory/        # Memory tier tests
└── test_tools/         # Tool adapter tests
```

### Rake
```
tests/
├── conftest.py         # Shared fixtures
├── unit/               # Source adapter tests, auth, text processing
└── integration/        # API endpoint tests, mission lifecycle
```

---

## Execution Tiers (ForgeAgents T0-T6)

ForgeAgents organizes its 35 execution nodes into 7 QA tiers. Each tier represents a layer of the agent execution pipeline, and test coverage must reflect the tier's criticality.

| Tier | Name | Nodes | Purpose | Test Priority |
|------|------|-------|---------|---------------|
| **T0** | Control | 5 | Authority gates, scope fences, token validation | Critical — must be 100% covered |
| **T1** | Intelligence | 5 | Code analysis, pattern detection, risk assessment | High — drives finding quality |
| **T2** | Specialist | 8 | Language/domain-specific (TS, Python, Rust, Build, Test, Docs, Migration, Config) | Medium — per-language coverage |
| **T3** | Verification | 5 | BuildGuard, test, security, quality gate, contract verification | High — gating decisions |
| **T4** | Planning | 4 | Plan construction, validation, constraint compilation, rollback | Medium — planning correctness |
| **T5** | Integration | 4 | DataForge, NeuroForge, Rake, external service bridges | High — service contract conformance |
| **T6** | Release | 4 | Deployment, rollback, environment promotion, release validation | Critical — irreversible actions |

**Tier test requirements:**
- T0 and T6 require 100% branch coverage (irreversible/security-critical)
- T1, T3, T5 require 80%+ coverage (high impact)
- T2, T4 require 70%+ coverage (domain-specific)

---

## Severity Gates (BugCheck S0-S4)

BugCheck finding severity levels map directly to CI/CD gating decisions:

| Level | Name | Gate Behavior | CI/CD Impact |
|-------|------|--------------|-------------|
| **S0** | Release Blocker | Blocks all merges and deployments | Pipeline fails; no override possible |
| **S1** | High | Blocks PR merge | PR cannot merge until resolved or dismissed with reason |
| **S2** | Medium | Warning only | Pipeline succeeds with warnings; tracked for trending |
| **S3** | Low | Informational | Logged; no pipeline impact |
| **S4** | Info | Advisory only | Visible in reports; zero enforcement |

### Gating Rules

1. **Pre-merge gate:** Any S0 or S1 finding with `lifecycle_state=NEW` → merge blocked
2. **Deployment gate:** Any S0 finding across any run in the release window → deploy blocked
3. **Dismissed findings:** Require `reason` + `scope` + `expires_at` — time-boxed, not permanent
4. **Baseline comparison:** New findings compared against baseline run; only net-new findings count toward gating

---

## CI/CD Pipeline Integration

### Stage-to-Tier Mapping

| CI Stage | QA Tiers Exercised | Blocking Severity |
|----------|-------------------|-------------------|
| Pre-commit hooks | T0 (token validation, scope) | S0 only |
| PR checks | T0-T3 (all checks through verification) | S0, S1 |
| Merge gate | T0-T5 (full pipeline minus release) | S0, S1 |
| Deploy gate | T0-T6 (complete pipeline) | S0 |
| Post-deploy validation | T6 (release validation) | S0 (rollback trigger) |

### Test-to-Spec Alignment

The §11 database schemas and §8 API contracts feed directly into spec-first QA:

1. **Schema-driven tests:** Pydantic models in §11 generate validation test cases automatically
2. **Contract tests:** ForgeAgents' 62 contract tests verify payload conformance against DataForge schemas
3. **Lifecycle tests:** State machine transitions defined in §9 map 1:1 to test assertions
4. **Fingerprint stability:** Same error at same location must produce same fingerprint — tested across synthetic runs

---

*For per-service test details and execution instructions, see each service's own `doc/system/` testing chapter. For finding severity definitions, see §9. For database schemas that drive spec-first tests, see §11.*

---

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

---

# §16 — Documentation Truth Policy

This section defines how the ecosystem reference distinguishes canonical doctrine from audit-derived snapshot facts.

## Definitions

### Canonical Fact

A canonical fact is stable, normative, and architecture-defining. Examples include:

- subsystem roles and ownership
- authority boundaries
- durable truth rules
- port assignments from the canonical registry
- HTTP versus CLI boundaries
- authentication semantics
- lifecycle rules
- fail-closed doctrine
- canonical Pack J stage ordering: `risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate`

### Snapshot Fact

A snapshot fact is measured from the current codebase or runtime surface and may change after future audits. Examples include:

- router or endpoint totals
- file counts and LOC
- command, route, component, or store totals
- test totals and coverage percentages
- schema, table, or model tallies
- phase/status summaries that include measured counts

## Labeling Rules

Use canonical wording for canonical facts:

- "Forge Eval is a standalone subsystem."
- "DataForge is the durable truth store."
- "Forge Eval has no resident HTTP API in the current Pack J runtime."

Label snapshot facts visibly with language such as:

- "Current audited snapshot"
- "Current code snapshot"
- "Audit-derived count"
- "As of this document version"

Do not present snapshot counts as timeless doctrine.

## Update Rules For Future Audits

1. Update canonical facts only when architecture, doctrine, ports, boundaries, or enforced stage order actually change.
2. Update snapshot facts when a code audit re-measures counts, coverage, or inventory totals.
3. If a chapter mixes doctrine and inventory, add a local note stating which content is canonical and which content is snapshot-derived.
4. When narrative stage names differ from internal IDs, document both:
   - narrative name for ecosystem doctrine
   - stage or artifact ID for code-facing references
5. If two sections disagree, resolve the conflict by:
   - correcting the stale value,
   - converting a measured value into snapshot-labeled wording,
   - or removing the lower-value duplicate.
6. After changes, rebuild `doc/SYSTEM.md` and verify that no old contradictory values remain.

## Maintainer Checklist

- Check canonical ports against `PORT_REGISTRY.md`
- Keep Forge Eval described as standalone CLI/runtime-local evaluation unless the codebase gains a resident service API
- Keep the Pack J narrative chain consistent across overview, architecture, integration, testing, and handover
- Treat counts as volatile unless a protocol or invariant explicitly fixes them
- Rebuild the compiled reference after every source-chapter edit
