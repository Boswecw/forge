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
- **Current implemented path runs through Pack J.** `risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate`

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
| **Forge Eval** | None in current Pack J runtime; emits local schema-locked artifacts | — |

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
