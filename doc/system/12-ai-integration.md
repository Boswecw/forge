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
