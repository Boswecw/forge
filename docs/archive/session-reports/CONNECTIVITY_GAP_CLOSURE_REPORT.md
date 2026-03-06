# Forge Ecosystem — Connectivity Gap Closure Report

**Executed:** 2026-02-23
**Scope:** 7 findings (F-001 through F-007), 7 sessions, P0–P2 priority

---

## Session 1 — F-001: ForgeCommand Port Canonicalization (P0, docs only)

**Problem:** Documentation inconsistently listed ForgeAgents on ports 8003 and 8787. ForgeCommand REST server port was undocumented.

**Changes:**
- `doc/system/05-config-env.md` — Corrected port table: ForgeAgents production=8787, dev=8003. Added ForgeCommand REST Server (8790, localhost-only).
- `doc/system/15-handover.md` — Updated startup command table to match corrected ports.
- `doc/SYSTEM.md` — Regenerated.

**Files touched:** 3 (docs only, no code changes)

---

## Session 2 — F-003: AuthorForge S0/S1 Violation Remediation (P0)

**Problem:** AuthorForge violated two ecosystem laws:
- **S0 (Release Blocker):** Direct OpenAI API calls from `apps/backend/app/routers/embed.py` bypassed NeuroForge (Law 2).
- **S1 (Blocks PR):** Six route files used direct PostgreSQL pool/SQLAlchemy instead of DataForge (Law 3).

**S0 Fix:**
- `Author-Forge/apps/backend/app/routers/embed.py` — Replaced direct `openai.embeddings.create()` call with NeuroForge HTTP proxy (`POST /api/v1/embeddings`). Added `NEUROFORGE_URL` env var support. OpenAI API key no longer needed in AuthorForge.

**S1 Fix — TypeScript API routes (3 files):**
- `Author-Forge/apps/api/src/services/dataforge.ts` — Created/expanded DataForge HTTP client with project CRUD, entity CRUD, and doc (chapter) CRUD operations.
- `Author-Forge/apps/api/src/routes/projects.ts` — Rewrote from direct pool queries to DataForge client.
- `Author-Forge/apps/api/src/routes/entities.ts` — Rewrote from direct pool queries to DataForge client (client-side search filtering).
- `Author-Forge/apps/api/src/routes/docs.ts` — Rewrote: multipart upload parsing stays local, all persistence through DataForge.

**S1 Fix — Python backend routes (3 files):**
- `Author-Forge/apps/backend/app/services/dataforge_client.py` — New Python DataForge HTTP client (httpx) mirroring the TS client.
- `Author-Forge/apps/backend/app/routers/projects.py` — Rewrote from SQLAlchemy to DataForge client.
- `Author-Forge/apps/backend/app/routers/entities.py` — Rewrote from SQLAlchemy to DataForge client.
- `Author-Forge/apps/backend/app/routers/docs.py` — Rewrote: file parsing stays local, persistence through DataForge, entity extraction uses DataForge for both read and write.

**Acceptable remaining pool usage:** `rag.ts`, `continuity.py`, `gen.py`, `embed.py` — read-only vector similarity compute, not authoritative data persistence.

**Docs:**
- `doc/system/10-ecosystem-integration.md` — Added AuthorForge integration contract tables.

**Files touched:** 11 code + 2 docs

---

## Session 3 — F-002: Shared Embedding Dimension Config (P1)

**Problem:** Embedding dimension was hardcoded differently across services (ForgeAgents=768, all others=1536). No single config knob to change it ecosystem-wide.

**Changes:**
- `DataForge/app/config.py` — `EMBEDDING_DIMENSION` now reads `FORGE_EMBED_DIM` env var (default 1536).
- `ForgeAgents/app/core/config.py` — `embedding_dimension` now reads `FORGE_EMBED_DIM` (default 768 for legacy compat). Max raised from 2048 to 4096.
- `NeuroForge/neuroforge_backend/config.py` — `embedding_dimension` now reads `FORGE_EMBED_DIM` (default 1536).
- `rake/services/embedding_service.py` — `get_dimensions()` fallback reads `FORGE_EMBED_DIM`.
- `Author-Forge/apps/backend/app/core/config.py` — `EMBED_DIM` checks `FORGE_EMBED_DIM` first, then `EMBED_DIM`, then defaults to 1536.
- `doc/system/05-config-env.md` — Added Embeddings section documenting `FORGE_EMBED_DIM`.

**Files touched:** 5 code + 1 doc

---

## Session 4 — F-006: Deep Mode Production Safety Gate (P1)

**Problem:** BugCheck deep mode (fuzzer, failure simulator) has side effects but had no production guard. Running `--deep` in production could cause damage.

**Changes:**
- `ForgeAgents/app/agents/bugcheck/agent.py` — Added safety gate in `run()`: checks `FORGE_ENVIRONMENT`/`ENVIRONMENT`, raises `BugCheckError` if `production`.
- `ForgeAgents/bugcheck/app/cli.py` — Added safety gate in `_run_async()`: prints error and returns early.
- `ForgeAgents/bugcheck/app/executor.py` — Added safety gate in `EcosystemExecutor.run()`: raises `ExecutionError`.
- `doc/system/15-handover.md` — Updated from "not safe for production" to "gated in production".

**Files touched:** 3 code + 1 doc

---

## Session 5 — F-007: NeuroForge context_builder.py Cleanup (P1)

**Problem:** The corrupted `context_builder.py` was deleted but could be accidentally re-created. All 26+ modules import from `context_builder_fixed.py` but there was no guard preventing re-introduction of the old filename.

**Changes:**
- `NeuroForge/neuroforge_backend/services/context_builder.py` — Created guard stub that raises `ImportError` with clear message pointing to `context_builder_fixed`.
- `doc/system/15-handover.md` — Updated from "CORRUPTED" to "guard stub" (2 edits).
- `doc/system/04-project-structure.md` — Updated from "CRITICAL" to "NOTE".
- `doc/system/12-ai-integration.md` — Same change.

**Files touched:** 1 code + 3 docs

---

## Session 6 — F-004: Rake Pipeline Retry Logic (P2)

**Problem:** Rake pipeline had retry logic only for FETCH stage (via `fetch_with_retry`). EMBED and STORE stages (external API calls to OpenAI and DataForge) had no retry, causing spurious failures on transient errors.

**Changes:**
- `rake/pipeline/orchestrator.py`:
  - Added `STAGE_RETRY_CONFIG` class variable: FETCH=1/2s, CLEAN=1/1s, CHUNK=1/1s, EMBED=2/2s, STORE=2/3s.
  - Added `max_stage_retries` constructor parameter for overrides.
  - Added `_run_stage_with_retry()` method with exponential backoff.
  - Wrapped all 5 stage executions with the retry helper.
- `doc/system/15-handover.md` — Documented the new retry logic with defaults.

**Files touched:** 1 code + 1 doc

---

## Session 7 — F-005: Global XAI Rate Limiter (P2)

**Problem:** XAI rate limit was per-run only (50 requests). MAID had per-run limits (20 requests + 100k tokens). No global cap across concurrent runs — multiple simultaneous ecosystem runs could exceed provider limits and rack up costs.

**Changes:**
- `ForgeAgents/app/agents/bugcheck/routing/global_rate_limiter.py` — **New module.** Process-wide singleton `GlobalRateLimiter` with:
  - Separate `ProviderBudget` tracking for XAI and MAID
  - Monthly rolling window (resets on calendar month boundary)
  - Daily cost cap in USD
  - `check_and_increment()` — atomic check + increment (for API call gates)
  - `check_budget()` — read-only budget query
  - Alert thresholds: 80% warning, 95% critical (structured log events)
  - Configurable via `XAI_MONTHLY_CAP`, `MAID_MONTHLY_CAP`, `MAX_COST_PER_DAY` env vars
- `ForgeAgents/app/agents/bugcheck/xai/client.py` — Global budget check before per-run check in `lookup()`.
- `ForgeAgents/app/agents/bugcheck/maid/client.py` — Global budget check in `analyze_finding()`, `propose_fix()`, `validate_fix()`.
- `ForgeAgents/app/agents/bugcheck/routing/maid_router.py` — Added `check_global_budget()` and `increment_global_usage()` async methods.
- `ForgeAgents/app/agents/bugcheck/routing/__init__.py` — Exports `APIProvider`, `GlobalRateLimiter`, `GlobalRateLimitResult`, `get_global_rate_limiter`.
- `ForgeAgents/app/core/config.py` — Added `xai_monthly_cap` (5000), `maid_monthly_cap` (2000), `max_cost_per_day` ($10) settings.
- `doc/system/15-handover.md` — Updated ForgeAgents section with global limiter details.
- `doc/system/05-config-env.md` — Added "ForgeAgents — Global API Rate Limiting" section.

**Defaults:**

| Variable | Default | Purpose |
|---|---|---|
| `XAI_MONTHLY_CAP` | 5000 | Max XAI requests/month across all runs |
| `MAID_MONTHLY_CAP` | 2000 | Max MAID requests/month across all runs |
| `MAX_COST_PER_DAY` | $10.00 | Daily LLM API spend cap |

**Files touched:** 5 code + 2 docs

---

## Aggregate Impact

| Metric | Count |
|---|---|
| Total files created | 4 |
| Total files modified | ~30 |
| Ecosystem laws enforced | 2 (Law 2: AI through NeuroForge, Law 3: DataForge as SoT) |
| S0 violations fixed | 1 (AuthorForge direct OpenAI) |
| S1 violations fixed | 6 (AuthorForge direct DB routes) |
| New env vars introduced | 4 (`FORGE_EMBED_DIM`, `XAI_MONTHLY_CAP`, `MAID_MONTHLY_CAP`, `MAX_COST_PER_DAY`) |
| Safety gates added | 3 (deep mode: agent, CLI, executor) |
| Guard stubs created | 1 (context_builder.py) |
| Doc chapters updated | 5 (04, 05, 10, 12, 15) |
| SYSTEM.md regenerations | 7 |
