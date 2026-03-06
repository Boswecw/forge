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
