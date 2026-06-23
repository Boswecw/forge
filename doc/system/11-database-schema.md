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
