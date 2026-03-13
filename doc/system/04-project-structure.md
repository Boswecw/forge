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
