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
