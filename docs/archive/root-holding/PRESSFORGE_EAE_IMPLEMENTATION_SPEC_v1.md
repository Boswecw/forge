# PressForge — Evidence Assembly Engine (EAE) Implementation Spec

**Version:** 1.0  
**Date:** 2026-02-25  
**Owner:** Boswell Digital Solutions  
**Status:** Implementation-Ready  
**Depends On:** NeuroForge, DataForge, Rake, ForgeCommand  
**Companion To:** PRESSFORGE_PRODUCT_SPEC_v0.2  
**Supersedes:** press_forge_eae_refactor_plan_v1.md (planning draft)  
**Internal Label:** RAG 2.0

---

# §1 — Purpose & Scope

## 1.1 What This Document Is

This is the implementation spec for the Evidence Assembly Engine (EAE) — a governed retrieval pipeline that supplies grounded, auditable evidence bundles to PressForge AI tasks. EAE is a **NeuroForge library module**, not a PressForge UI feature. PressForge consumes its output read-only.

## 1.2 What EAE Solves

Without EAE, PressForge AI tasks (pitch generation, GEO optimization, disinfo scanning) operate on zero grounding. The model receives a task and generates text from parametric memory alone. This produces:

- Generic pitches indistinguishable from every other AI-generated email
- Claims with no traceable source
- No way to prove what informed an output
- No way to detect when evidence was insufficient

EAE eliminates this by inserting a governed evidence supply chain between "PressForge needs output" and "NeuroForge generates output."

## 1.3 What EAE Does NOT Do

- Execute anything (retrieval only — RunIntent remains the execution gate)
- Auto-approve any output
- Score humanity, run compliance logic, or compute velocity math
- Replace the NeuroForge 5-stage inference pipeline (it feeds Stage 1: Context Builder)
- Grant PressForge any write authority over evidence

## 1.4 Governance Invariants (Non-Negotiable)

| Invariant | Enforcement |
|-----------|-------------|
| DataForge is source of truth (Law 3) | All evidence, retrieval logs, and audit records persist to DataForge Postgres. Redis is speed-only. |
| ForgeCommand is root of trust (Law 1) | API keys for embedding providers injected from ForgeCommand vault. Never cross IPC. |
| Services communicate via defined contracts (Law 2) | EvidenceQuery.v1 / EvidenceBundle.v1 are the only input/output contracts. No ad-hoc payloads. |
| Evidence proves what happened (Law 5) | Every retrieval run logged. No silent fallbacks. Coverage gaps reported explicitly. |
| Humans decide intent | PressForge operator triggers retrieval. EAE never auto-initiates. |

---

# §2 — Architecture

## 2.1 Service Ownership

```
PressForge (UI)                    NeuroForge (AI)                    DataForge (Storage)
─────────────────                  ────────────────                   ───────────────────
Requests outputs                   Owns EAE pipeline                  Stores evidence items
Displays evidence (read-only)      Calls DataForge for retrieval      Stores retrieval run logs
Shows coverage warnings            Writes audit records                Stores AI audit records
Manual "refresh evidence" trigger  Manages Redis cache                 Hybrid search engine
                                   Packages bundles with citations     Embedding pipeline

                                   Redis Cloud (Cache)
                                   ──────────────────
                                   Caches bundles (short TTL)
                                   Caches rerank intermediates
                                   NOT authoritative
```

## 2.2 Call Flow

```
PressForge UI
    │
    │  POST /api/v1/pressforge/evidence/assemble
    │  (EvidenceQuery.v1 payload)
    │
    ▼
NeuroForge — EAE Pipeline
    │
    ├── D1: Query Planner ──► Maps task → evidence requirements
    │
    ├── D2: Hybrid Retrieval ──► DataForge hybrid search
    │       │                    (tsvector BM25 + pgvector cosine + RRF)
    │       │                    + metadata filters (trust, time, kind, entity)
    │       │
    │       ├── Cache check (Redis) ──► hit? return cached bundle
    │       └── miss? execute retrieval
    │
    ├── D3: Re-ranking ──► Deterministic scoring (no LLM call)
    │       trust_tier × 0.35 + freshness × 0.25 + entity_match × 0.25 + rrf_score × 0.15
    │
    ├── D4: Bundle Packaging ──► Cap items, cap excerpts, citation_map, bundle_hash
    │
    └── D5: Audit Logging ──► pf_retrieval_runs + pf_ai_audit_log (DataForge)
    │
    ▼
EvidenceBundle.v1 returned to caller
    │
    ├── NeuroForge inference pipeline (Stage 1 context) → generates grounded output
    │
    └── PressForge UI displays evidence + citations + coverage warnings
```

## 2.3 Where EAE Fits in NeuroForge

EAE is a **library module** imported by NeuroForge, not a standalone service. It lives alongside the existing 5-stage inference pipeline:

```
NeuroForge/
├── app/
│   ├── eae/                          # NEW — Evidence Assembly Engine
│   │   ├── __init__.py
│   │   ├── contracts.py              # EvidenceQuery.v1, EvidenceBundle.v1 (Pydantic v2)
│   │   ├── query_planner.py          # D1: Task → evidence requirements
│   │   ├── retriever.py              # D2: Hybrid retrieval via DataForge
│   │   ├── reranker.py               # D3: Deterministic scoring
│   │   ├── bundler.py                # D4: Packaging + citation mapping
│   │   ├── auditor.py                # D5: Log writer
│   │   ├── cache.py                  # Redis bundle cache
│   │   └── pipeline.py               # Orchestrates D1–D5
│   │
│   ├── context_builder_fixed.py      # EXISTING — gains EAE integration point
│   ├── prompt_engine.py              # EXISTING — unchanged
│   ├── model_router.py               # EXISTING — unchanged
│   ├── evaluator.py                  # EXISTING — unchanged
│   └── post_processor.py             # EXISTING — unchanged
```

**Integration point:** `context_builder_fixed.py` gains an optional code path: when an `EvidenceQuery.v1` is attached to an inference request, the context builder delegates to `eae/pipeline.py` instead of running the default RAG fetch. This preserves backward compatibility — all existing NeuroForge consumers continue to work unchanged.

---

# §3 — Contracts

## 3.1 EvidenceQuery.v1 (Input)

```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime
from typing import Optional

class EAETaskType(str, Enum):
    GEO_CITATION_OPT = "geo_citation_opt"
    DISINFO_SCAN = "disinfo_scan"
    NARRATIVE_FORECAST = "narrative_forecast"
    ALIGNMENT_FORECAST = "alignment_forecast"
    PITCH_GENERATION = "pitch_generation"
    JOURNALIST_MATCH = "journalist_match"

class EntityRef(BaseModel):
    """Structured entity reference for targeted retrieval."""
    kind: str = Field(..., pattern=r"^(book|author|journalist|outlet|campaign|topic|person)$")
    name: str = Field(..., min_length=1, max_length=500)
    id: Optional[str] = None  # DataForge entity ID if known

class EvidenceKind(str, Enum):
    JOURNALIST_ARTICLE = "journalist_article"
    JOURNALIST_PROFILE = "journalist_profile"
    BOOK_METADATA = "book_metadata"
    AUTHOR_BIO = "author_bio"
    PRESS_RELEASE = "press_release"
    INDUSTRY_SIGNAL = "industry_signal"
    PRIOR_COVERAGE = "prior_coverage"
    SOCIAL_SIGNAL = "social_signal"
    AUTHORITATIVE_REF = "authoritative_ref"

class RiskMode(str, Enum):
    NORMAL = "normal"
    HIGH_RISK = "high_risk"  # Stricter trust_floor, wider retrieval

class EvidenceQuery(BaseModel):
    """EvidenceQuery.v1 — Canonical input contract for EAE pipeline."""
    
    model_config = {"json_schema_extra": {"version": "1"}}
    
    task: EAETaskType
    entities: list[EntityRef] = Field(..., min_length=1, max_length=10)
    time_window: Optional[dict] = Field(
        default=None,
        description="{'min': ISO datetime, 'max': ISO datetime}. Defaults per task if omitted."
    )
    required_kinds: list[EvidenceKind] = Field(default_factory=list, max_length=8)
    risk_mode: RiskMode = RiskMode.NORMAL
    trust_floor: int = Field(default=1, ge=1, le=5, description="Minimum trust tier (1=unvetted, 5=authoritative)")
    max_items: int = Field(default=20, ge=5, le=50)
    max_excerpt_tokens: int = Field(default=200, ge=50, le=500)
    max_tokens_budget: int = Field(default=4000, ge=500, le=16000, description="Total token budget for assembled bundle")
    campaign_id: Optional[str] = None  # Links retrieval to a PressForge campaign
    
    @field_validator("time_window")
    @classmethod
    def validate_time_window(cls, v):
        if v is not None:
            if "min" not in v and "max" not in v:
                raise ValueError("time_window must have at least 'min' or 'max'")
        return v
    
    def canonical_json(self) -> str:
        """Deterministic JSON for cache keying and hash computation."""
        import json
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
```

## 3.2 EvidenceBundle.v1 (Output)

```python
import hashlib
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from typing import Optional

class EvidenceItem(BaseModel):
    """Single evidence item in a bundle."""
    evidence_id: str  # DataForge chunk/document ID
    kind: EvidenceKind
    title: str
    excerpt: str = Field(..., max_length=2000)  # Bounded excerpt
    url: Optional[str] = None
    source: Optional[str] = None  # Publication name, database name, etc.
    published_at: Optional[datetime] = None
    trust_tier: int = Field(..., ge=1, le=5)
    entity_tags: list[str] = Field(default_factory=list)
    content_hash: str  # SHA-256 of full source content
    rank_score: float = Field(..., ge=0.0, le=1.0)
    retrieval_method: str = Field(..., pattern=r"^(semantic|keyword|hybrid|metadata)$")

class CoverageReport(BaseModel):
    """What was found vs. what was requested."""
    requested_kinds: list[str]
    found_kinds: list[str]
    missing_kinds: list[str]
    entity_coverage: dict[str, bool]  # entity_name → found?
    coverage_score: float = Field(..., ge=0.0, le=1.0)
    warnings: list[str] = Field(default_factory=list)

class EvidenceBundle(BaseModel):
    """EvidenceBundle.v1 — Canonical output contract for EAE pipeline."""
    
    model_config = {"json_schema_extra": {"version": "1"}}
    
    bundle_id: str  # UUID
    created_at: datetime
    task: EAETaskType
    query_hash: str  # SHA-256 of EvidenceQuery.canonical_json()
    items: list[EvidenceItem] = Field(..., max_length=50)
    citation_map: dict[str, str]  # citation_key (e.g. "[1]") → evidence_id
    coverage: CoverageReport
    total_tokens: int  # Estimated token count of assembled bundle
    cache_hit: bool = False
    
    @computed_field
    @property
    def bundle_hash(self) -> str:
        """Canonical hash of bundle contents for audit integrity."""
        import json
        payload = json.dumps(
            [item.model_dump(mode="json") for item in self.items],
            sort_keys=True, separators=(",", ":")
        )
        return f"sha256:{hashlib.sha256(payload.encode()).hexdigest()}"
    
    @computed_field
    @property
    def item_count(self) -> int:
        return len(self.items)
```

## 3.3 Contract Invariants

| Rule | Enforcement |
|------|-------------|
| `items` length ≤ `max_items` from query | Bundler enforces hard cap |
| Each `excerpt` ≤ `max_excerpt_tokens` | Bundler truncates with `…` marker |
| `total_tokens` ≤ `max_tokens_budget` | Bundler drops lowest-ranked items until within budget |
| `citation_map` keys are sequential `[1]`, `[2]`, etc. | Bundler generates in rank order |
| `bundle_hash` is deterministic | Same items in same order → same hash |
| `coverage.missing_kinds` is never suppressed | If a required kind has zero results, it appears here |
| `coverage.warnings` includes thin-coverage alerts | < 3 items for a required kind triggers warning |

---

# §4 — DataForge Schema Additions

## 4.1 `pf_retrieval_runs` (New Table)

Every EAE pipeline execution writes one row. Append-only.

```sql
CREATE TABLE pf_retrieval_runs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- What was asked
    task            VARCHAR(50) NOT NULL,
    campaign_id     UUID REFERENCES pf_campaigns(id) ON DELETE SET NULL,
    query_spec      JSONB NOT NULL,           -- Full EvidenceQuery.v1 JSON
    query_hash      VARCHAR(71) NOT NULL,     -- sha256: prefix
    
    -- What was searched
    filters_applied JSONB NOT NULL,           -- trust_floor, time_window, kinds, entities
    sub_query_count INT NOT NULL DEFAULT 1,   -- How many sub-queries were planned (max 3)
    
    -- What was found
    candidate_count INT NOT NULL,             -- Pre-rerank count
    candidate_ids   JSONB NOT NULL,           -- Array of evidence IDs considered
    topk_ids        JSONB NOT NULL,           -- Array of evidence IDs in final bundle
    topk_hashes     JSONB NOT NULL,           -- Array of content hashes for integrity
    rerank_scores   JSONB NOT NULL,           -- {evidence_id: {trust: x, freshness: x, entity: x, rrf: x, final: x}}
    
    -- Bundle output
    bundle_id       UUID NOT NULL,
    bundle_hash     VARCHAR(71) NOT NULL,     -- sha256: prefix
    item_count      INT NOT NULL,
    total_tokens    INT NOT NULL,
    
    -- Performance
    cache_hit       BOOLEAN NOT NULL DEFAULT false,
    latency_ms      INT NOT NULL,
    
    -- Coverage quality
    coverage_score  FLOAT NOT NULL,           -- 0.0–1.0
    missing_kinds   JSONB DEFAULT '[]'::jsonb,
    warnings        JSONB DEFAULT '[]'::jsonb
);

CREATE INDEX idx_pf_retrieval_runs_task ON pf_retrieval_runs(task);
CREATE INDEX idx_pf_retrieval_runs_campaign ON pf_retrieval_runs(campaign_id);
CREATE INDEX idx_pf_retrieval_runs_created ON pf_retrieval_runs(created_at DESC);
CREATE INDEX idx_pf_retrieval_runs_query_hash ON pf_retrieval_runs(query_hash);
CREATE INDEX idx_pf_retrieval_runs_bundle ON pf_retrieval_runs(bundle_id);
```

## 4.2 `pf_ai_audit_log` (Extend Existing)

The `pf_ai_audit_log` table already exists in the PressForge schema. Add columns to link inference outputs to evidence bundles:

```sql
ALTER TABLE pf_ai_audit_log
    ADD COLUMN IF NOT EXISTS evidence_bundle_id UUID,
    ADD COLUMN IF NOT EXISTS bundle_hash VARCHAR(71),
    ADD COLUMN IF NOT EXISTS model_route VARCHAR(100),       -- e.g. "anthropic/claude-sonnet-4-6"
    ADD COLUMN IF NOT EXISTS output_payload JSONB,           -- Generated draft content
    ADD COLUMN IF NOT EXISTS cited_evidence_ids JSONB,       -- Array of evidence IDs actually cited
    ADD COLUMN IF NOT EXISTS uncited_evidence_ids JSONB,     -- Evidence provided but not used
    ADD COLUMN IF NOT EXISTS missing_evidence_warnings JSONB;

CREATE INDEX idx_pf_ai_audit_bundle ON pf_ai_audit_log(evidence_bundle_id);
CREATE INDEX idx_pf_ai_audit_bundle_hash ON pf_ai_audit_log(bundle_hash);
```

## 4.3 `pf_evidence_items` (New Table — Evidence Registry)

Dedicated registry for PressForge evidence items. This augments DataForge's generic `documents`/`chunks` tables with PressForge-specific metadata. Evidence items may reference underlying DataForge chunks or be standalone entries (e.g., manually added journalist profiles).

```sql
CREATE TABLE pf_evidence_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- Classification
    kind            VARCHAR(50) NOT NULL,     -- Maps to EvidenceKind enum
    title           VARCHAR(500) NOT NULL,
    source          VARCHAR(500),             -- Publication, database, URL domain
    url             VARCHAR(2000),
    published_at    TIMESTAMPTZ,
    
    -- Content
    content         TEXT NOT NULL,            -- Full text
    content_hash    VARCHAR(71) NOT NULL,     -- sha256: prefix for integrity
    excerpt         TEXT,                     -- Pre-computed excerpt (optional)
    
    -- Trust & classification
    trust_tier      INT NOT NULL DEFAULT 1 CHECK (trust_tier BETWEEN 1 AND 5),
    entity_tags     JSONB DEFAULT '[]'::jsonb,  -- ["author:Charles", "book:Title", "outlet:NYT"]
    metadata        JSONB DEFAULT '{}'::jsonb,  -- Extensible metadata
    
    -- Search
    embedding       VECTOR(1536),            -- Voyage AI embedding
    search_vector   TSVECTOR,                -- Auto-maintained by trigger
    
    -- Provenance
    source_chunk_id INT REFERENCES chunks(id) ON DELETE SET NULL,  -- Link to DataForge chunk if applicable
    ingested_by     VARCHAR(50),             -- "rake", "manual", "journalist_refresh_agent"
    
    -- Lifecycle
    is_active       BOOLEAN NOT NULL DEFAULT true,
    stale_at        TIMESTAMPTZ              -- When this evidence should be re-verified
);

CREATE INDEX idx_pf_evidence_kind ON pf_evidence_items(kind);
CREATE INDEX idx_pf_evidence_trust ON pf_evidence_items(trust_tier);
CREATE INDEX idx_pf_evidence_published ON pf_evidence_items(published_at DESC);
CREATE INDEX idx_pf_evidence_active ON pf_evidence_items(is_active) WHERE is_active = true;
CREATE INDEX idx_pf_evidence_entity_tags ON pf_evidence_items USING GIN(entity_tags);
CREATE INDEX idx_pf_evidence_embedding ON pf_evidence_items USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_pf_evidence_tsvector ON pf_evidence_items USING GIN(search_vector);
CREATE INDEX idx_pf_evidence_stale ON pf_evidence_items(stale_at) WHERE stale_at IS NOT NULL;

-- Auto-maintain tsvector
CREATE TRIGGER pf_evidence_tsvector_update
    BEFORE INSERT OR UPDATE ON pf_evidence_items
    FOR EACH ROW EXECUTE FUNCTION
    tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);
```

## 4.4 Trust Tier Definitions

| Tier | Label | Examples | Retrieval Behavior |
|------|-------|---------|-------------------|
| 5 | Authoritative | Publisher databases, ISBN registries, SEC filings, official press releases | Always included when available |
| 4 | Verified | Major publication articles, verified journalist profiles, established media databases | Default trust_floor for high_risk mode |
| 3 | Credible | Trade publications, industry blogs with editorial oversight, curated RSS feeds | Default trust_floor for normal mode |
| 2 | Community | Social media posts, forum discussions, unvetted blog content | Included only if higher-tier evidence is insufficient |
| 1 | Unvetted | Raw web scrapes, unverified claims, anonymous sources | Excluded by default; requires explicit trust_floor=1 |

---

# §5 — EAE Pipeline Implementation

## 5.1 D1: Query Planner

Maps task type + entities to concrete retrieval requirements. Bounded to max 3 sub-queries.

```python
# eae/query_planner.py

TASK_EVIDENCE_MAP: dict[EAETaskType, list[EvidenceKind]] = {
    EAETaskType.PITCH_GENERATION: [
        EvidenceKind.JOURNALIST_PROFILE,
        EvidenceKind.JOURNALIST_ARTICLE,
        EvidenceKind.BOOK_METADATA,
        EvidenceKind.AUTHOR_BIO,
        EvidenceKind.PRIOR_COVERAGE,
        EvidenceKind.INDUSTRY_SIGNAL,
    ],
    EAETaskType.GEO_CITATION_OPT: [
        EvidenceKind.AUTHOR_BIO,
        EvidenceKind.BOOK_METADATA,
        EvidenceKind.PRIOR_COVERAGE,
        EvidenceKind.AUTHORITATIVE_REF,
    ],
    EAETaskType.DISINFO_SCAN: [
        EvidenceKind.SOCIAL_SIGNAL,
        EvidenceKind.JOURNALIST_ARTICLE,
        EvidenceKind.AUTHORITATIVE_REF,
        EvidenceKind.INDUSTRY_SIGNAL,
    ],
    EAETaskType.JOURNALIST_MATCH: [
        EvidenceKind.JOURNALIST_PROFILE,
        EvidenceKind.JOURNALIST_ARTICLE,
        EvidenceKind.BOOK_METADATA,
    ],
    EAETaskType.NARRATIVE_FORECAST: [
        EvidenceKind.SOCIAL_SIGNAL,
        EvidenceKind.INDUSTRY_SIGNAL,
        EvidenceKind.PRIOR_COVERAGE,
        EvidenceKind.JOURNALIST_ARTICLE,
    ],
    EAETaskType.ALIGNMENT_FORECAST: [
        EvidenceKind.JOURNALIST_PROFILE,
        EvidenceKind.JOURNALIST_ARTICLE,
        EvidenceKind.SOCIAL_SIGNAL,
        EvidenceKind.INDUSTRY_SIGNAL,
    ],
}

TASK_DEFAULT_TIME_WINDOWS: dict[EAETaskType, dict] = {
    EAETaskType.PITCH_GENERATION: {"days_back": 90},
    EAETaskType.GEO_CITATION_OPT: {"days_back": 365},
    EAETaskType.DISINFO_SCAN: {"days_back": 30},
    EAETaskType.JOURNALIST_MATCH: {"days_back": 180},
    EAETaskType.NARRATIVE_FORECAST: {"days_back": 60},
    EAETaskType.ALIGNMENT_FORECAST: {"days_back": 90},
}

TASK_DEFAULT_TRUST_FLOORS: dict[EAETaskType, int] = {
    EAETaskType.PITCH_GENERATION: 3,
    EAETaskType.GEO_CITATION_OPT: 4,    # Higher bar — public-facing content
    EAETaskType.DISINFO_SCAN: 2,          # Need to see low-trust signals
    EAETaskType.JOURNALIST_MATCH: 3,
    EAETaskType.NARRATIVE_FORECAST: 2,
    EAETaskType.ALIGNMENT_FORECAST: 3,
}
```

**Sub-query decomposition rules:**
1. If entities span multiple kinds (e.g., journalist + book), split into entity-focused sub-queries (max 3).
2. Each sub-query targets a subset of required_kinds relevant to that entity.
3. Results from all sub-queries merge before reranking.

## 5.2 D2: Hybrid Retrieval

Delegates to DataForge's existing hybrid search engine with PressForge-specific filters layered on top.

```python
# eae/retriever.py — Pseudocode

async def retrieve(plan: RetrievalPlan, dataforge_client: DataForgeClient) -> list[CandidateItem]:
    """Execute hybrid retrieval against pf_evidence_items + DataForge chunks."""
    
    candidates = []
    
    for sub_query in plan.sub_queries:
        # Build query text from entity names + required kinds
        query_text = build_query_text(sub_query.entities, sub_query.target_kinds)
        
        # Call DataForge hybrid search with PressForge filters
        results = await dataforge_client.hybrid_search(
            query=query_text,
            table="pf_evidence_items",        # PressForge evidence registry
            filters={
                "kind__in": [k.value for k in sub_query.target_kinds],
                "trust_tier__gte": sub_query.trust_floor,
                "is_active": True,
                "published_at__gte": sub_query.time_min,
                "published_at__lte": sub_query.time_max,
                "entity_tags__overlap": sub_query.entity_tag_filters,  # GIN index
            },
            limit=plan.query.max_items * 3,   # Over-fetch for reranking (matches DataForge pattern)
            similarity_threshold=0.5,          # Lower than default 0.7 — reranker handles quality
        )
        
        candidates.extend(results)
    
    # Deduplicate by evidence_id
    seen = set()
    unique = []
    for c in candidates:
        if c.evidence_id not in seen:
            seen.add(c.evidence_id)
            unique.append(c)
    
    return unique
```

**Key design decision:** The retrieval threshold is intentionally lower than DataForge's default (0.5 vs 0.7) because D3 reranking handles quality filtering. This prevents premature exclusion of evidence that might score well on trust or entity match despite moderate semantic similarity.

## 5.3 D3: Deterministic Re-ranking

No LLM calls. Fully deterministic scoring with configurable weights.

```python
# eae/reranker.py

from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class RerankWeights:
    """Weights for each scoring dimension. Must sum to 1.0."""
    trust: float = 0.35
    freshness: float = 0.25
    entity_match: float = 0.25
    rrf_base: float = 0.15
    
    def __post_init__(self):
        total = self.trust + self.freshness + self.entity_match + self.rrf_base
        assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"

# Per-task weight overrides
TASK_WEIGHT_OVERRIDES: dict[EAETaskType, RerankWeights] = {
    EAETaskType.DISINFO_SCAN: RerankWeights(
        trust=0.20,       # Lower — need to see unvetted signals
        freshness=0.40,   # Higher — recency critical for disinfo
        entity_match=0.25,
        rrf_base=0.15,
    ),
    EAETaskType.GEO_CITATION_OPT: RerankWeights(
        trust=0.45,       # Higher — authoritative refs matter most
        freshness=0.15,   # Lower — evergreen content acceptable
        entity_match=0.25,
        rrf_base=0.15,
    ),
}

def freshness_score(published_at: datetime | None, decay_halflife_days: int = 90) -> float:
    """Exponential decay: 1.0 at t=0, 0.5 at halflife, approaches 0 asymptotically.
    Returns 0.5 if published_at is None (unknown recency → neutral)."""
    if published_at is None:
        return 0.5
    age_days = (datetime.utcnow() - published_at).days
    if age_days < 0:
        return 1.0  # Future-dated (shouldn't happen, but safe)
    import math
    return math.exp(-0.693 * age_days / decay_halflife_days)

def trust_score(tier: int) -> float:
    """Linear normalization: tier 1→0.2, tier 5→1.0."""
    return 0.2 + (tier - 1) * 0.2

def entity_match_score(item_tags: list[str], query_entities: list[EntityRef]) -> float:
    """Fraction of query entities matched by item tags."""
    if not query_entities:
        return 0.5
    query_names = {e.name.lower() for e in query_entities}
    item_names = set()
    for tag in item_tags:
        # Tags are formatted as "kind:name"
        if ":" in tag:
            item_names.add(tag.split(":", 1)[1].lower())
        else:
            item_names.add(tag.lower())
    matches = len(query_names & item_names)
    return matches / len(query_names)

def rerank(
    candidates: list[CandidateItem],
    query: EvidenceQuery,
    weights: RerankWeights | None = None,
) -> list[ScoredItem]:
    """Deterministic reranking. Returns items sorted by final score descending."""
    
    if weights is None:
        weights = TASK_WEIGHT_OVERRIDES.get(query.task, RerankWeights())
    
    scored = []
    for item in candidates:
        ts = trust_score(item.trust_tier)
        fs = freshness_score(item.published_at)
        em = entity_match_score(item.entity_tags, query.entities)
        rrf = item.rrf_score  # From DataForge hybrid search
        
        final = (
            weights.trust * ts
            + weights.freshness * fs
            + weights.entity_match * em
            + weights.rrf_base * rrf
        )
        
        scored.append(ScoredItem(
            item=item,
            scores={"trust": ts, "freshness": fs, "entity_match": em, "rrf": rrf, "final": final},
        ))
    
    scored.sort(key=lambda s: s.scores["final"], reverse=True)
    return scored
```

**Implementation note — phased approach:** For the initial implementation (Phase D, first pass), use a simplified reranker: `trust_floor` filter + sort by `published_at DESC`. This gets EAE producing bundles immediately. Swap in the full weighted reranker once you have real retrieval data to validate the weight tuning against.

## 5.4 D4: Bundle Packaging

```python
# eae/bundler.py — Key logic

def package_bundle(
    scored_items: list[ScoredItem],
    query: EvidenceQuery,
) -> EvidenceBundle:
    """Package scored items into a bounded, hashable bundle."""
    
    # 1. Apply hard caps
    items = scored_items[:query.max_items]
    
    # 2. Truncate excerpts
    for item in items:
        item.excerpt = truncate_to_tokens(item.excerpt, query.max_excerpt_tokens)
    
    # 3. Enforce token budget — drop lowest-ranked items until within budget
    total_tokens = estimate_tokens(items)
    while total_tokens > query.max_tokens_budget and len(items) > 1:
        items.pop()  # Remove lowest-ranked (last in sorted list)
        total_tokens = estimate_tokens(items)
    
    # 4. Generate citation map
    citation_map = {}
    for i, item in enumerate(items, 1):
        citation_map[f"[{i}]"] = item.evidence_id
    
    # 5. Build coverage report
    coverage = build_coverage_report(items, query)
    
    # 6. Assemble bundle
    return EvidenceBundle(
        bundle_id=str(uuid4()),
        created_at=datetime.utcnow(),
        task=query.task,
        query_hash=f"sha256:{hashlib.sha256(query.canonical_json().encode()).hexdigest()}",
        items=[to_evidence_item(s) for s in items],
        citation_map=citation_map,
        coverage=coverage,
        total_tokens=total_tokens,
        cache_hit=False,
    )

def build_coverage_report(items: list, query: EvidenceQuery) -> CoverageReport:
    """Honest coverage assessment — never suppress gaps."""
    
    found_kinds = list(set(item.kind for item in items))
    
    # Determine what was required
    requested = query.required_kinds or TASK_EVIDENCE_MAP.get(query.task, [])
    requested_strs = [k.value if isinstance(k, EvidenceKind) else k for k in requested]
    found_strs = [k.value if isinstance(k, EvidenceKind) else k for k in found_kinds]
    missing = [k for k in requested_strs if k not in found_strs]
    
    # Entity coverage
    entity_coverage = {}
    item_entity_names = set()
    for item in items:
        for tag in item.entity_tags:
            if ":" in tag:
                item_entity_names.add(tag.split(":", 1)[1].lower())
    for entity in query.entities:
        entity_coverage[entity.name] = entity.name.lower() in item_entity_names
    
    # Coverage score
    if not requested_strs:
        coverage_score = 1.0 if items else 0.0
    else:
        coverage_score = len([k for k in requested_strs if k in found_strs]) / len(requested_strs)
    
    # Warnings
    warnings = []
    for kind in requested_strs:
        kind_count = sum(1 for item in items if (item.kind.value if isinstance(item.kind, EvidenceKind) else item.kind) == kind)
        if kind_count == 0:
            warnings.append(f"MISSING: No evidence found for kind '{kind}'")
        elif kind_count < 3:
            warnings.append(f"THIN: Only {kind_count} item(s) for kind '{kind}' (recommend ≥3)")
    
    for name, found in entity_coverage.items():
        if not found:
            warnings.append(f"ENTITY_GAP: No evidence tagged for entity '{name}'")
    
    return CoverageReport(
        requested_kinds=requested_strs,
        found_kinds=found_strs,
        missing_kinds=missing,
        entity_coverage=entity_coverage,
        coverage_score=coverage_score,
        warnings=warnings,
    )
```

## 5.5 D5: Audit Logging

Every EAE pipeline execution writes to DataForge. No exceptions. No silent fallbacks.

```python
# eae/auditor.py

async def log_retrieval_run(
    query: EvidenceQuery,
    candidates: list[CandidateItem],
    scored: list[ScoredItem],
    bundle: EvidenceBundle,
    latency_ms: int,
    dataforge_client: DataForgeClient,
) -> None:
    """Write retrieval run to pf_retrieval_runs. Mandatory — failure here is a pipeline error."""
    
    await dataforge_client.insert("pf_retrieval_runs", {
        "task": query.task.value,
        "campaign_id": query.campaign_id,
        "query_spec": query.model_dump(mode="json"),
        "query_hash": bundle.query_hash,
        "filters_applied": {
            "trust_floor": query.trust_floor,
            "time_window": query.time_window,
            "required_kinds": [k.value for k in query.required_kinds],
            "entity_refs": [e.model_dump() for e in query.entities],
        },
        "sub_query_count": len(query.entities),  # Simplified — refine with actual planner output
        "candidate_count": len(candidates),
        "candidate_ids": [c.evidence_id for c in candidates],
        "topk_ids": [s.item.evidence_id for s in scored[:bundle.item_count]],
        "topk_hashes": [s.item.content_hash for s in scored[:bundle.item_count]],
        "rerank_scores": {s.item.evidence_id: s.scores for s in scored[:bundle.item_count]},
        "bundle_id": bundle.bundle_id,
        "bundle_hash": bundle.bundle_hash,
        "item_count": bundle.item_count,
        "total_tokens": bundle.total_tokens,
        "cache_hit": bundle.cache_hit,
        "latency_ms": latency_ms,
        "coverage_score": bundle.coverage.coverage_score,
        "missing_kinds": bundle.coverage.missing_kinds,
        "warnings": bundle.coverage.warnings,
    })
```

**Failure behavior:** If the DataForge write fails, the EAE pipeline returns an error to the caller. An unlogged retrieval run is treated as a pipeline failure, not a degraded success. This is a hard invariant — you cannot use evidence that wasn't audited.

---

# §6 — Redis Cache Layer

## 6.1 Cache Keys

```
eae:bundle:{sha256_of_canonical_query}  →  EvidenceBundle.v1 JSON
eae:meta:{sha256_of_canonical_query}    →  {created_at, item_count, coverage_score}
```

## 6.2 TTL Strategy

| Condition | TTL |
|-----------|-----|
| Default | 15 minutes |
| High-risk mode | 5 minutes |
| Disinfo scan tasks | 5 minutes (freshness critical) |
| GEO citation tasks | 30 minutes (slower-changing content) |

## 6.3 Invalidation Triggers

| Event | Action |
|-------|--------|
| New evidence ingested (Rake job completes) | Flush all `eae:bundle:*` keys matching affected entity tags |
| Trust tier change on any `pf_evidence_items` row | Flush all `eae:bundle:*` |
| EvidenceBundle schema version bump | Flush all `eae:*` |
| Manual "Refresh Evidence" from PressForge UI | Bypass cache for that specific query |

## 6.4 Cache-Aside Pattern

```python
# eae/cache.py

async def get_or_assemble(
    query: EvidenceQuery,
    redis: Redis,
    pipeline: EAEPipeline,
) -> EvidenceBundle:
    """Cache-aside: check Redis first, assemble on miss."""
    
    cache_key = f"eae:bundle:{hashlib.sha256(query.canonical_json().encode()).hexdigest()}"
    
    cached = await redis.get(cache_key)
    if cached is not None:
        bundle = EvidenceBundle.model_validate_json(cached)
        bundle.cache_hit = True
        # Still log retrieval run even for cache hits (audit completeness)
        await pipeline.auditor.log_cache_hit(query, bundle)
        return bundle
    
    bundle = await pipeline.assemble(query)
    
    ttl = resolve_ttl(query)
    await redis.setex(cache_key, ttl, bundle.model_dump_json())
    
    return bundle
```

**Invariant:** Audit logging happens for both cache hits and misses. A cache hit writes a lightweight `pf_retrieval_runs` entry with `cache_hit=true` so audit trail is unbroken.

---

# §7 — NeuroForge API Surface

## 7.1 New Endpoint

```
POST /api/v1/pressforge/evidence/assemble
```

**Request:** `EvidenceQuery.v1` JSON body  
**Response:** `EvidenceBundle.v1` JSON  
**Auth:** Bearer token (ForgeCommand-issued)  
**Rate limit:** 10 req/min per campaign_id  

**Error responses:**

| Status | Condition | Body |
|--------|-----------|------|
| 400 | Invalid EvidenceQuery | Pydantic validation errors |
| 404 | No evidence found at all | `{"error": "no_evidence", "warnings": [...]}` |
| 422 | Evidence found but coverage critically insufficient | `{"error": "insufficient_coverage", "bundle": partial_bundle, "warnings": [...]}` |
| 500 | DataForge unreachable or audit write failed | `{"error": "pipeline_failure", "stage": "retrieval|audit"}` |
| 503 | Redis unavailable (non-fatal — proceeds without cache) | N/A — degrades silently to uncached |

## 7.2 Integration with Existing Inference Pipeline

When a PressForge inference request includes an `evidence_query` field, the 5-stage pipeline adapts:

```python
# context_builder_fixed.py — Modified flow

async def build_context(request: InferenceRequest) -> Context:
    if request.evidence_query is not None:
        # EAE path — governed evidence assembly
        bundle = await eae_pipeline.assemble(request.evidence_query)
        return Context(
            chunks=bundle_to_chunks(bundle),      # Convert to existing Chunk format
            evidence_bundle=bundle,                 # Attach full bundle for audit
            source="eae",
        )
    else:
        # Default path — existing RAG fetch (unchanged)
        return await default_rag_fetch(request)
```

This means existing NeuroForge consumers (AuthorForge, VibeForge, Rake, BugCheck) are completely unaffected.

---

# §8 — PressForge UI Integration

## 8.1 Evidence Panel (New Component)

Read-only evidence display component, shown alongside draft outputs.

```
┌─────────────────────────────────────────────────────┐
│  Evidence Bundle                     [Refresh ↻]     │
│  ─────────────────────────────────────────────────── │
│  Coverage: 85% ████████░░  (12 items, 3 kinds)       │
│                                                       │
│  ⚠ THIN: Only 1 item for kind 'prior_coverage'       │
│  ⚠ ENTITY_GAP: No evidence for entity 'Book Title'   │
│                                                       │
│  [1] "Interview: Fantasy Genre in 2026" — PW         │
│      Tier 4 · Jan 2026 · journalist_article           │
│      "The indie fantasy market has seen a 40%..."     │
│                                                       │
│  [2] "Journalist Profile: Jane Smith" — Verified DB   │
│      Tier 4 · journalist_profile                      │
│      "Covers: indie publishing, BookTok, SFF..."      │
│                                                       │
│  [3] ...                                              │
│                                                       │
│  Bundle: sha256:a1b2c3... · 3,200 tokens · 45ms      │
└─────────────────────────────────────────────────────┘
```

## 8.2 What PressForge UI Can Do

- Display evidence items with citation keys, trust tier badges, kind labels
- Display coverage report (score bar, missing kinds, warnings)
- Display bundle metadata (hash, token count, latency, cache hit status)
- Trigger "Refresh Evidence" (re-runs EAE pipeline with cache bypass)
- Link citation keys in draft output back to evidence panel items

## 8.3 What PressForge UI Must NOT Do

- Perform retrieval directly
- Modify evidence items or rankings
- Suppress or hide coverage warnings
- Override trust tier filters
- Execute any action based on evidence (execution remains gated by RunIntent)

---

# §9 — Degraded Mode Behavior

| Failure | EAE Behavior | PressForge Behavior |
|---------|-------------|-------------------|
| DataForge unreachable | Pipeline fails with 500. No silent fallback. | Shows error: "Evidence unavailable — DataForge offline" |
| Redis unreachable | Pipeline continues without cache. Latency increases. | No visible change (cache is transparent to UI) |
| Embedding provider down | Falls back through provider chain (Voyage AI → OpenAI → Cohere). If all fail, returns keyword-only results with warning. | Shows warning: "Semantic search degraded — keyword results only" |
| Zero evidence found | Returns 404 with empty bundle + coverage report | Shows: "No evidence found. Seed evidence via Rake before generating." |
| Thin coverage (< 3 items per required kind) | Returns 200 with bundle + warnings | Shows warnings inline. Operator decides whether to proceed. |
| Audit write fails | Pipeline fails with 500. Evidence is discarded. | Shows error: "Evidence audit failed — cannot proceed" |

---

# §10 — Phase Plan (Implementation Order)

## Phase A — Confirm Current Reality (Day 1)

**Work:** Write a short AS-BUILT note documenting:
1. Where PressForge evidence currently lives (answer: it doesn't — no evidence items exist yet)
2. Which embedding pipeline is available (answer: DataForge Voyage AI 1536-dim + tsvector)
3. Current PressForge → NeuroForge call path (answer: none for evidence; pitch generation not implemented)
4. Existing `pf_ai_audit_log` table schema and current usage

**Exit gate:** AS-BUILT note committed to docs. Known unknowns documented.

## Phase B — Contracts (Days 2–3)

**Work:**
1. Implement `EvidenceQuery.v1` and `EvidenceBundle.v1` as Pydantic v2 models in `NeuroForge/app/eae/contracts.py`
2. Implement canonical JSON serialization and SHA-256 hashing
3. Write contract tests: required fields, defaults, bounds, hash stability

**Exit gate:** `pytest tests/eae/test_contracts.py` passes. Hash determinism verified across 100 random inputs.

## Phase C — DataForge Schema (Days 4–5)

**Work:**
1. Create Alembic migration for `pf_evidence_items` table
2. Create Alembic migration for `pf_retrieval_runs` table
3. Create Alembic migration for `pf_ai_audit_log` column additions
4. Verify all indexes, triggers, and constraints
5. Write integration test: insert evidence item → insert retrieval run → insert audit log → read back

**Exit gate:** Migrations apply cleanly. Round-trip test passes.

## Phase D — EAE Pipeline, First Pass (Days 6–10)

**Implementation strategy — two sub-phases:**

**D-alpha (Days 6–8): Minimal viable pipeline**
- Query planner: task → evidence kinds mapping (static, no sub-query decomposition)
- Retriever: single hybrid search call against `pf_evidence_items`
- Reranker: **simplified** — trust_floor filter + sort by `published_at DESC` (no weighted scoring yet)
- Bundler: cap items, cap excerpts, generate citation map, compute hash
- Auditor: write `pf_retrieval_runs` and `pf_ai_audit_log`
- Wire up as `POST /api/v1/pressforge/evidence/assemble`
- **Target task:** `pitch_generation` (most immediately useful)

**D-beta (Days 9–10): Full reranker + sub-queries**
- Implement weighted reranker with per-task weight overrides
- Implement sub-query decomposition (max 3) for multi-entity queries
- Implement freshness decay math
- Validate reranker outputs against D-alpha results to confirm scoring improves relevance

**Exit gate:** `pitch_generation` task runs E2E: query → retrieval → bundle → audit log. Coverage report accurately reflects what was found/missing.

## Phase E — Redis Cache (Days 11–12)

**Work:**
1. Implement cache-aside pattern in `eae/cache.py`
2. Implement TTL strategy per task type
3. Implement invalidation on evidence ingest (Rake job webhook)
4. Verify audit logging for cache hits
5. Benchmark: p95 latency with cache on vs. off

**Exit gate:** p95 latency improves ≥ 50% on cache hits. Audit records identical with cache on/off.

## Phase F — PressForge UI (Days 13–15)

**Work:**
1. Create `EvidencePanel.svelte` component (read-only evidence display)
2. Create `CoverageBar.svelte` component (visual coverage indicator)
3. Wire "Refresh Evidence" button to re-trigger EAE with cache bypass
4. Link citation keys in draft output to evidence panel scroll targets
5. Add evidence panel to campaign detail page and pitch generation flow

**Exit gate:** PressForge can display EvidenceBundle + coverage warnings. No write operations possible.

## Phase G — Tests (Days 16–18)

**Work:**
1. **T1 Unit:** query planner mapping, filter construction, freshness decay, trust normalization, entity match, budget enforcement
2. **T2 Reranker:** deterministic ordering verified with fixtures, weight override correctness, tie-breaking stability
3. **T3 Contract:** schema validation, canonical hash stability, serialization round-trip
4. **T4 E2E:** `pitch_generation` and `geo_citation_opt` full pipeline (seed test evidence → query → bundle → verify citations present)
5. **T5 Coverage:** coverage report accuracy (seeded gaps → verify warnings generated)
6. **T6 Perf:** latency thresholds (< 500ms uncached, < 50ms cached), bundle size thresholds

**Exit gate:** All tests pass. Tests gate merges in CI.

---

# §11 — Evidence Seeding Strategy

EAE is useless without evidence in `pf_evidence_items`. This section defines how evidence gets there.

## 11.1 Rake Integration (Primary)

Existing Rake research missions already ingest documents, chunk them, and embed them in DataForge. Add a post-ingest hook that:

1. Checks if the document matches PressForge evidence kinds (journalist article, industry signal, etc.)
2. If yes, creates a `pf_evidence_items` row with appropriate `kind`, `trust_tier`, and `entity_tags`
3. Links back to the source `chunks.id` via `source_chunk_id`

This means evidence seeding happens automatically as Rake ingests journalist-related content.

## 11.2 Agent-Driven Enrichment

The existing `pressforge-journalist-refresh-agent` and `pressforge-monitor-agent` (defined in PRESSFORGE_PRODUCT_SPEC_v0.2 §5) gain evidence-writing capabilities:

- Journalist refresh agent: creates/updates `journalist_profile` evidence items
- Monitor agent: creates `prior_coverage` and `social_signal` evidence items from discovered media mentions

## 11.3 Manual Entry

PressForge settings page (Phase 2+) allows manual evidence entry for:
- Author bios
- Book metadata
- Press releases
- Authoritative references

These get `ingested_by: "manual"` and default `trust_tier: 3` (operator can override).

---

# §12 — GraphRAG Appendix (Phase H — Deferred)

## 12.1 Why Defer

GraphRAG adds entity extraction, relationship graph maintenance, and traversal logic. Implementing it before baseline EAE is stable creates:
- Unclear correctness ("is it retrieval or graph traversal that broke?")
- Schema sprawl (3+ additional tables, batch extraction jobs)
- Single-operator debugging overload

**Decision criterion:** Implement GraphRAG when retrieval run logs show repeated misses where the missing information is "relationship context" — i.e., EAE finds individual evidence items but cannot connect them (journalist X covers beat Y at outlet Z which recently covered topic W).

## 12.2 GraphLite Schema (Postgres-Native)

When triggered, implements in Supabase Postgres (no new database):

```sql
-- Future: pf_entities (graph nodes)
-- Future: pf_relations (graph edges)  
-- Future: pf_communities (derived cluster summaries)
```

**Bounded traversal:** max depth 2, max 50 nodes per request, every traversal logged in `pf_retrieval_runs`.

## 12.3 EAE Integration Point

GraphRAG inserts as a post-retrieval expansion step between D2 (Hybrid Retrieval) and D3 (Re-ranking):

```
D2: Hybrid Retrieval → [D2.5: Graph Expansion (1–2 hops)] → D3: Re-ranking
```

The expansion step takes top-k entity IDs from D2 results, traverses 1–2 hops in the relationship graph, and adds related evidence items to the candidate pool. These additional items still pass through D3 reranking and D4 budget enforcement — graph expansion cannot bypass the bundle caps.

---

# §13 — Success Metrics

| Metric | Baseline (No EAE) | Target (With EAE) | Measurement |
|--------|-------------------|-------------------|-------------|
| Pitch grounding | 0 cited sources | ≥ 3 cited sources per pitch | Count `cited_evidence_ids` in `pf_ai_audit_log` |
| Coverage score | N/A | ≥ 0.7 average across tasks | Mean `coverage_score` in `pf_retrieval_runs` |
| Audit completeness | Partial (existing audit log) | 100% of inference runs linked to evidence bundles | `pf_ai_audit_log` rows with non-null `evidence_bundle_id` / total rows |
| Retrieval latency (uncached) | N/A | p95 < 500ms | `latency_ms` in `pf_retrieval_runs` where `cache_hit=false` |
| Retrieval latency (cached) | N/A | p95 < 50ms | `latency_ms` in `pf_retrieval_runs` where `cache_hit=true` |
| Cache hit rate (steady state) | N/A | ≥ 30% | Ratio of `cache_hit=true` in `pf_retrieval_runs` |
| Coverage warnings addressed | N/A | Track over time | Count of warnings per retrieval run (should decrease as evidence grows) |

---

# §14 — Open Questions

| # | Question | Impact | Owner |
|---|----------|--------|-------|
| 1 | Should `pf_evidence_items` use DataForge's existing `documents`/`chunks` tables with a `pf_` domain filter, or a dedicated table? | Schema simplicity vs. query isolation. Spec assumes dedicated table. Revisit in Phase A. | Charles |
| 2 | Should evidence seeding from Rake run synchronously (in-pipeline) or as a post-ingest background job? | Latency vs. consistency. Background job recommended to avoid slowing Rake pipeline. | Charles |
| 3 | What is the minimum viable evidence corpus needed before EAE produces useful bundles? | Determines when to start testing with real tasks vs. fixtures. Estimate: 50+ evidence items spanning ≥ 3 kinds. | Charles |
| 4 | Should the 422 "insufficient coverage" response block pitch generation, or return a partial bundle with warnings and let the operator decide? | UX vs. safety. Spec recommends: return partial bundle + warnings, let operator decide. | Charles |
| 5 | Redis Cloud instance: new dedicated instance or shared with existing Rake/DataForge cache? | Cost vs. isolation. Shared is fine if key prefixes are enforced (`eae:*`). | Charles |

---

# Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-25 | Initial implementation spec. Incorporates improvements from planning review: phased D-alpha/D-beta reranker approach, explicit degraded mode behavior, evidence seeding strategy, success metrics, trust tier definitions, per-task weight overrides, simplified first-pass reranker recommendation. |
