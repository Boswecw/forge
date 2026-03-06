# Forge Ecosystem — Next Priorities Implementation Prompt

**Protocol:** `BDS_DOCUMENTATION_PROTOCOL_v1.md` §8 (Prompting Plans)  
**Date:** February 24, 2026  
**Version:** 1.0  
**Status:** Master Implementation Plan  
**Scope:** All Forge Ecosystem services  
**Companion Docs:** `BDS_QA_TESTING_PROTOCOL.md`, `BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md`, `FORGE_ECOSYSTEM_HEALTH_AND_HEALING_PROTOCOL.md`, `FORGEAGENTS_AGENTIC_REASONING_PROMPTING_PLAN.md`, `Forge_Gap_Closure_FollowUp_Tasks.docx`, `BDS_STANDARD_OPERATING_PROCEDURES.md`

---

## Document Purpose

This is the **master sequenced implementation plan** for all pending Forge Ecosystem priorities. It consolidates tasks from multiple source documents into a single execution order with explicit dependencies, gate criteria, and session prompts.

**Execution Rule:** Complete each phase's exit criteria before starting the next phase. P0 tasks within each phase must complete before P1 tasks. No feature work may proceed until all P0 verification tasks pass and SYSTEM.md files are rebuilt.

---

## Priority Legend

| Priority | Meaning | Gate Impact |
|----------|---------|-------------|
| **P0** | Blocker — blocks all downstream work | Must complete before any Phase 2+ work |
| **P1** | Expansion Blocker — blocks new feature development | Must complete before new capability sessions |
| **P2** | Resilience — improves reliability but not blocking | Can proceed in parallel with Phase 3+ |
| **P3** | Enhancement — future capability | Scheduled after all P0–P2 clear |

---

## Master Execution Sequence

```
PHASE 1: VERIFICATION (P0)         ← You are here
    All V-001 through V-005 pass
    All D-001, D-002 documentation rebuilt
    │
PHASE 2: TEST COVERAGE (P0/P1)
    T-003 through T-008 (P0 test gaps)
    T-001, T-002, T-005 (P1 test gaps)
    │
PHASE 3: OPERATIONAL READINESS (P1/P2)
    O-001 through O-006 operational tasks
    D-003 through D-005 documentation
    Deferred technical debt items
    │
PHASE 4: SENTINEL AGENT (P1 — New Capability)
    Health & Healing Protocol: Sessions 1–8
    │
PHASE 5: AGENTIC REASONING (P1 — New Capability)
    Agentic Reasoning Plan: Sessions 1–9
    │
PHASE 6: FORGEAGENTS MATURATION (P2)
    Test coverage to 85%
    Deep mode environment safety gate
    Global XAI rate limiting
    Trending analytics completion
    │
PHASE 7: FORGECOMMAND EVOLUTION (P3)
    Headless mode for CI/CD
    Multi-user support
    Enhanced telemetry (OTEL)
    Automated alerting
```

---

# PHASE 1 — VERIFICATION (P0)

**Gate:** No work beyond Phase 1 until all P0 verification tasks pass.  
**Estimated effort:** 1–2 focused sessions  
**Protocol reference:** `BDS_QA_TESTING_PROTOCOL.md` Phase 3 (T0 Pre-Flight)

## Session 1.1 — P0 Verification & Documentation Rebuild

**Priority:** P0  
**Services touched:** All  
**Context to load:**

```bash
# Load ecosystem overview + gap closure report
cat doc/system/01-overview-philosophy.md
cat doc/system/05-config-env.md
cat CONNECTIVITY_GAP_CLOSURE_REPORT.md
cat Forge_Gap_Closure_FollowUp_Tasks.docx  # or .md equivalent
```

**Prompt:**

```
Execute the P0 verification tasks from the Forge Ecosystem Connectivity Gap Closure Follow-Up Task Register. These are T0 pre-flight checks that must pass before any further work.

VERIFICATION TASKS (all P0):

V-001: Health check all 5 services on canonical ports.
  - curl -f http://localhost:8000/health   # NeuroForge
  - curl -f http://localhost:8001/health   # DataForge
  - curl -f http://localhost:8002/health   # Rake
  - curl -f http://localhost:8010/health   # ForgeAgents
  - curl -f http://localhost:8003/health   # ForgeCommand orchestrator
  Expected: All return 200 OK.

V-002: Verify ForgeCommand token bridge responds on port 8790 (localhost only).
  - curl -f http://127.0.0.1:8790/fc/health
  - curl -f http://127.0.0.1:8790/fc/health
  Expected: 200 OK from localhost. Connection refused from non-localhost.

V-003: grep -r '9100' across all doc/system/*.md — expect zero hits.
  - for service in NeuroForge DataForge ForgeAgents rake forge-smithy ForgeCommand; do
      echo "=== $service ===" && grep -rn '9100' $service/doc/system/ 2>/dev/null
    done
  Expected: Zero matches. Port 9100 is the legacy port and must be fully purged.

V-004: grep -r 'OPENAI_API_KEY' across AuthorForge/ — expect zero hits.
  - grep -rn 'OPENAI_API_KEY' Author-Forge/ --include='*.py' --include='*.ts' --include='*.env*'
  Expected: Zero matches. AuthorForge must route all AI through NeuroForge (Law 2).

V-005: Run AuthorForge full Integration Audit Template (Protocol §11) — zero S0/S1.
  - Execute the audit template from BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md §11
  - Check all 5 laws against AuthorForge codebase
  Expected: Zero S0 findings. Zero S1 findings.

DOCUMENTATION TASKS (P0):

D-001: Rebuild all SYSTEM.md files from part files.
  - for service in NeuroForge DataForge ForgeAgents rake forge-smithy ForgeCommand; do
      cd $service/doc/system && bash BUILD.sh && cd -
    done
  - Diff rebuilt files against current versions
  - Any divergence = documentation debt that must be reconciled

D-002: Verify Integration Protocol Service Registry has no port 9100 references.
  - Check BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md §2
  - If port 9100 appears, update to canonical port 8003
  - Update ForgeCommand entry if needed

FAILURE HANDLING:
- Any V-001 through V-005 failure is an S0 blocker
- Log the failure, identify root cause, fix before proceeding
- Do NOT proceed to Phase 2 with any verification failure

PRODUCE:
- Verification report: PASS/FAIL for each task with evidence
- If all pass: declare Phase 1 complete
- If any fail: remediation plan with specific fixes needed
```

**Acceptance criteria:**

- [ ] V-001 through V-005 all PASS
- [ ] D-001: All SYSTEM.md files rebuilt and consistent
- [ ] D-002: Integration Protocol Service Registry uses canonical ports
- [ ] Verification report produced with evidence for each check

**Post-session gate:**

```bash
# Quick verification of all gates
curl -sf http://localhost:8000/health && echo "NF: OK" || echo "NF: FAIL"
curl -sf http://localhost:8001/health && echo "DF: OK" || echo "DF: FAIL"
curl -sf http://localhost:8002/health && echo "Rake: OK" || echo "Rake: FAIL"
curl -sf http://localhost:8010/health && echo "FA: OK" || echo "FA: FAIL"
curl -sf http://localhost:8003/health && echo "FC: OK" || echo "FC: FAIL"
echo "=== Port 9100 check ==="
grep -r '9100' */doc/system/ 2>/dev/null | wc -l  # Must be 0
echo "=== OPENAI_API_KEY check ==="
grep -r 'OPENAI_API_KEY' Author-Forge/ --include='*.py' --include='*.ts' 2>/dev/null | wc -l  # Must be 0
```

---

# PHASE 2 — TEST COVERAGE (P0/P1)

**Gate:** Phase 1 must be complete. No Phase 3+ work until all P0 test tasks pass.  
**Estimated effort:** 3–4 focused sessions  
**Protocol reference:** `BDS_QA_TESTING_PROTOCOL.md` Phase 4 (BUILD)

## Session 2.1 — AuthorForge DataForge Client Tests (P0)

**Priority:** P0 (T-003, T-004)  
**Services touched:** AuthorForge  
**Context to load:**

```bash
# AuthorForge DataForge client implementations
cat Author-Forge/apps/backend/app/services/dataforge_client.py
cat Author-Forge/apps/api/src/services/dataforge.ts
```

**Prompt:**

```
Write unit tests for the AuthorForge DataForge client implementations introduced during F-003 closure.

TASK T-003: Python DataForge Client (Author-Forge/apps/backend/app/services/dataforge_client.py)
  - Test all CRUD operations (project, entity, document)
  - Test error handling (timeout, 4xx, 5xx responses)
  - Test timeout behavior and retry logic
  - Mock httpx responses — do not call real DataForge
  - Place tests in: Author-Forge/apps/backend/tests/test_dataforge_client.py

TASK T-004: TypeScript DataForge Client (Author-Forge/apps/api/src/services/dataforge.ts)
  - Test project/entity/doc CRUD operations
  - Test client-side search filtering
  - Test error propagation
  - Mock fetch/axios responses
  - Place tests in: Author-Forge/apps/api/tests/dataforge.test.ts

CONSTRAINTS:
  - Follow existing test patterns in each codebase
  - Use pytest for Python, vitest/jest for TypeScript
  - Mock all external HTTP calls
  - Each test file should have 10+ test methods minimum
  - Test both success and failure paths

ACCEPTANCE CRITERIA:
  - [ ] Python tests pass: cd Author-Forge/apps/backend && pytest tests/test_dataforge_client.py -v
  - [ ] TypeScript tests pass: cd Author-Forge/apps/api && npm test -- dataforge
  - [ ] Zero regressions in existing test suites
  - [ ] ruff check passes (Python), eslint passes (TypeScript)
```

## Session 2.2 — AuthorForge Contract Tests (P0)

**Priority:** P0 (T-006, T-007, T-008)  
**Services touched:** AuthorForge, DataForge, NeuroForge  

**Prompt:**

```
Write contract tests validating AuthorForge's integration with DataForge and NeuroForge after the F-003 remediation.

TASK T-006: AuthorForge embed.py → NeuroForge Contract Test
  - Validate POST /api/v1/embeddings payload schema matches NeuroForge's expected input
  - Validate response schema parsing
  - Test with mock NeuroForge server returning expected shapes
  - Verify NEUROFORGE_URL env var is read correctly

TASK T-007: AuthorForge Python routes → DataForge Contract Test
  - Validate namespace/tenant_id/project_id scoping in all DataForge calls
  - Verify each route sends correct DataForge path parameters
  - Test routes: projects.py, entities.py, docs.py
  - Confirm no cross-tenant data leakage in request construction

TASK T-008: AuthorForge TypeScript routes → DataForge Contract Test
  - Validate request shapes match DataForge API schemas
  - Test routes: projects.ts, entities.ts, docs.ts
  - Verify multipart upload handling in docs.ts
  - Confirm DataForge URL construction is correct

CONSTRAINTS:
  - Contract tests validate shapes and schemas, not business logic
  - Use schema validation (Pydantic for Python, Zod/Joi for TS) where possible
  - Each contract test file should validate request AND response shapes
  - Follow BDS_QA_TESTING_PROTOCOL Tier T3 (API Contract Tests)

ACCEPTANCE CRITERIA:
  - [ ] All contract tests pass
  - [ ] Request schemas match DataForge's Pydantic models
  - [ ] Response parsing handles all documented status codes
  - [ ] Zero regressions
```

## Session 2.3 — P1 Test Coverage (P1)

**Priority:** P1 (T-001, T-002, T-005)  
**Services touched:** ForgeAgents, Rake  

**Prompt:**

```
Write unit tests for three P1 test coverage gaps identified during connectivity gap closure.

TASK T-001: GlobalRateLimiter Tests (ForgeAgents)
  - Test monthly window reset behavior
  - Test daily cost cap enforcement
  - Test alert thresholds (80% warning, 95% critical)
  - Test concurrent atomicity (thread-safe counter operations)
  - Location: ForgeAgents/tests/unit/test_global_rate_limiter.py

TASK T-002: Rake Pipeline Retry Tests (Rake)
  - Test _run_stage_with_retry() exponential backoff timing
  - Test max retry per stage (verify it stops after configured max)
  - Test error propagation (transient vs. permanent errors)
  - Test stage-level retry config overrides
  - Location: rake/tests/test_pipeline_retry.py

TASK T-005: BugCheck Deep Mode Safety Gate Tests (ForgeAgents)
  - Test agent.py rejects deep mode when FORGE_ENVIRONMENT=production
  - Test cli.py rejects --deep flag in production
  - Test executor.py rejects deep mode intent in production
  - Each component must independently enforce the gate
  - Location: ForgeAgents/tests/unit/test_deep_mode_safety.py

CONSTRAINTS:
  - Follow existing test patterns in each service
  - Use pytest with pytest-asyncio where needed
  - Mock external dependencies (DataForge, NeuroForge)
  - 5+ test methods per task minimum

ACCEPTANCE CRITERIA:
  - [ ] All tests pass: pytest tests/ -v --tb=short (per service)
  - [ ] Zero regressions in existing suites
  - [ ] mypy and ruff pass with zero errors
```

---

# PHASE 3 — OPERATIONAL READINESS (P1/P2)

**Gate:** Phase 2 P0 tasks complete.  
**Estimated effort:** 2–3 focused sessions  

## Session 3.1 — P1 Verification & Documentation

**Priority:** P1  
**Services touched:** All  

**Prompt:**

```
Execute P1 verification and documentation tasks from the Gap Closure Follow-Up Register.

VERIFICATION:

V-006: Confirm FORGE_EMBED_DIM env var is read by all 5 config files at startup.
  - Check: DataForge/app/config.py
  - Check: ForgeAgents/app/core/config.py
  - Check: NeuroForge/neuroforge_backend/config.py
  - Check: rake/services/embedding_service.py
  - Check: Author-Forge/apps/backend/app/core/config.py
  - Set FORGE_EMBED_DIM=2048, start each service, verify config reads 2048
  Expected: All 5 services read from FORGE_EMBED_DIM.

V-007: Set FORGE_ENVIRONMENT=production, attempt bugcheck --deep — expect rejection.
  - FORGE_ENVIRONMENT=production python -m app.agents.bugcheck.cli --deep
  Expected: Rejected with clear error message. Non-zero exit code.

V-008: Import context_builder from NeuroForge — expect ImportError pointing to _fixed.
  - python -c "from neuroforge_backend.services.context_builder import ContextBuilder"
  Expected: ImportError with message directing to context_builder_fixed.

DOCUMENTATION:

D-003: Add AuthorForge to quarterly audit schedule in Integration Protocol.
  - Update BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md
  - Add AuthorForge to the list of applications requiring quarterly audit

D-004: Document FORGE_EMBED_DIM in AuthorForge SYSTEM.md env var reference.
  - Update AuthorForge doc/system/ configuration chapter
  - Add FORGE_EMBED_DIM with description, default, and relationship to ecosystem config

D-005: Update ForgeAgents SYSTEM.md §11 to include GlobalRateLimiter test files.
  - Add test file references to the testing section
  - Rebuild SYSTEM.md: cd ForgeAgents/doc/system && bash BUILD.sh

ACCEPTANCE CRITERIA:
  - [ ] V-006, V-007, V-008 all PASS
  - [ ] D-003, D-004, D-005 documentation updated
  - [ ] All SYSTEM.md files rebuilt
```

## Session 3.2 — P2 Verification & Technical Debt

**Priority:** P2  
**Services touched:** ForgeAgents, Rake  

**Prompt:**

```
Execute P2 verification tasks and address deferred technical debt items.

VERIFICATION:

V-009: Trigger Rake pipeline with simulated EMBED stage timeout — confirm retry + backoff.
  - Create a test job that triggers the EMBED stage
  - Mock the embedding service to timeout on first 2 calls, succeed on 3rd
  - Verify exponential backoff timing in logs
  - Verify job completes successfully after retries
  Expected: Job completes with retry_count=2 logged.

V-010: Simulate concurrent XAI calls exceeding XAI_MONTHLY_CAP — confirm global limiter fires.
  - Set XAI_MONTHLY_CAP to a low value (e.g., 5)
  - Fire 10 concurrent XAI call requests
  - Verify calls 6-10 are rate limited
  Expected: Rate limiter rejects excess calls with structured error.

TECHNICAL DEBT:

TD-001: AuthorForge read-only pool usage documentation.
  - Add inline comments to exempted files (rag.ts, continuity.py, gen.py, embed.py)
  - Comments should explain the Law 3 exception: "Read-only vector similarity compute,
    not authoritative data persistence. Exempt per F-003 closure audit."
  - Track DataForge vector search API development for future migration

TD-002: ForgeAgents embedding dimension legacy default.
  - Document the 768 vs 1536 divergence in ForgeAgents SYSTEM.md
  - Add migration plan note: re-embed at 1536 when legacy data is refreshed
  - Add TODO comment in ForgeAgents/app/core/config.py

TD-003: GlobalRateLimiter persistence evaluation.
  - Add monitoring hook to log rate limiter resets (for production observation)
  - Document decision to defer DataForge-backed persistence
  - Note in SYSTEM.md: "Evaluate restart-resilient rate limiting after 30 days production"

ACCEPTANCE CRITERIA:
  - [ ] V-009, V-010 PASS
  - [ ] TD-001: Inline comments added to all 4 exempted AuthorForge files
  - [ ] TD-002: Migration plan documented
  - [ ] TD-003: Monitoring hook added, decision documented
```

---

# PHASE 4 — SENTINEL AGENT (P1 — New Capability)

**Gate:** Phase 2 P0 tasks complete. Phase 1 fully clear.  
**Estimated effort:** 6–8 focused sessions  
**Protocol reference:** `FORGE_ECOSYSTEM_HEALTH_AND_HEALING_PROTOCOL.md`

> **Note:** This phase has its own detailed 8-session prompting plan in `FORGE_ECOSYSTEM_HEALTH_AND_HEALING_PROTOCOL.md` Part 3. The sessions below are summaries. Use the full protocol document for session execution.

## Dependency Graph

```
Session 4.1 (Doc: SYSTEM.md updates with [PLANNED] markers)
    │
    ├──► Session 4.2 (Doc: Module Spec + DataForge Schema Plan)
    │        │
    │        ├──► Session 4.3 (Code: DataForge schema migration + CRUD)
    │        │        │
    │        │        ├──► Session 4.4 (Code: Health Sweep tooling — light + deep)
    │        │        │        │
    │        │        │        └──► Session 4.5 (Code: Sentinel agent + 5-phase loop)
    │        │        │                 │
    │        │        │                 └──► Session 4.6 (Code: Healing playbooks — 3 playbooks)
    │        │        │                          │
    │        │        │                          └──► Session 4.7 (Code: HealingScope policy)
    │        │        │
    │        │        └──► Session 4.8 (Code: SMITH UI integration)
```

## Session 4.1 — Documentation: SYSTEM.md Updates

**Prompt summary:** Update ForgeAgents, DataForge, and Forge:SMITH SYSTEM.md files with [PLANNED] markers for the Sentinel subsystem. Add new sections for health sweep dimensions, healing actions, and Sentinel agent archetype.

## Session 4.2 — Documentation: Module Spec + Schema Plan

**Prompt summary:** Create `ForgeAgents/docs/sentinel/SENTINEL_MODULE_SPEC.md` with full module specification. Create DataForge schema plan for `health_sweep_reports` and `healing_actions` tables.

## Session 4.3 — Code: DataForge Schema + API

**Prompt summary:** Create Alembic migration for Sentinel tables. Implement SQLAlchemy models, Pydantic schemas, and CRUD router (`app/routers/sentinel.py`). Full test coverage.

## Session 4.4 — Code: Health Sweep Tooling

**Prompt summary:** Implement `app/tools/health.py` with `health_sweep` and `breaker_probe_reset` tools. Register in Tool Router. Implement light sweep (D1+D3+D6) and deep sweep (D1-D6) across all 6 health dimensions.

## Session 4.5 — Code: Sentinel Agent

**Prompt summary:** Create `app/agents/reference/sentinel.py`. Implement sentinel_light and sentinel_deep execution modes. 5-phase loop (Plan→Act→Observe→Reflect→Decide). Register in agent registry.

## Session 4.6 — Code: Healing Playbooks

**Prompt summary:** Implement 3 healing playbooks: H-001 (Cache Flush), H-002 (Circuit Breaker Reset), H-003 (Rake Job Retry). Each with preconditions, cooldowns, and rollback behavior.

## Session 4.7 — Code: HealingScope Policy

**Prompt summary:** Create `HealingScope` policy. Register as Safety policy #5 in Policy Engine (total: 13 policies). Enforce autonomy tier boundaries (Tier A auto, Tier B requires approval, Tier C manual only).

## Session 4.8 — Code: SMITH UI Integration

**Prompt summary:** Add Sentinel state to ServiceHealthPanel, ForgeHUD indicators, and System Rail in Forge:SMITH. Display sweep results, healing status, and escalation queue.

**Phase 4 Exit Criteria:**

```bash
# Verify all components
cd DataForge && pytest tests/test_sentinel_router.py -v --tb=short
cd ForgeAgents && pytest tests/unit/test_health_sweep.py tests/unit/test_sentinel_agent.py tests/unit/test_healing_playbooks.py tests/test_policies/test_healing_scope.py -v --tb=short
# Verify policy count = 13
grep -c "policy" ForgeAgents/app/policies/engine.py
# Verify tool count = 37
grep -c "register\|tool_name" ForgeAgents/app/tools/router.py
# Rebuild all SYSTEM.md files
for service in ForgeAgents DataForge forge-smithy; do
  cd $service/doc/system && bash BUILD.sh && cd -
done
# Remove [PLANNED] markers
grep -r '\[PLANNED\]' */doc/system/ | wc -l  # Must be 0
```

---

# PHASE 5 — AGENTIC REASONING (P1 — New Capability)

**Gate:** Phase 2 P0 tasks complete. Can run in parallel with Phase 4 if different developers.  
**Estimated effort:** 6–8 focused sessions for P0/P1, 2–3 for P2  
**Protocol reference:** `FORGEAGENTS_AGENTIC_REASONING_PROMPTING_PLAN.md`

> **Note:** This phase has its own detailed 9-session prompting plan. The sessions below are summaries.

## Dependency Graph

```
Session 5.1 (Doc: SYSTEM.md updates)
    │
    ├──► Session 5.2 (Doc: Module Spec + Schema)
    │        │
    │        ├──► Session 5.3 (Code: Experience Store — DataForge schema + API)
    │        │        │
    │        │        ├──► Session 5.4 (Code: Plan Phase memory retrieval)
    │        │        │
    │        │        └──► Session 5.5 (Code: Gate Analytics aggregation)
    │        │                 │
    │        │                 └──► Session 5.6 (Code: SMITH Assist narrator integration)
    │        │
    │        ├──► Session 5.7 (Code: Skill Nomination pipeline)
    │        │
    │        └──► Session 5.8 (Code: Governed Broadcast adapter)
    │
    └──► Session 5.9 (Code: Metacognitive monitor — SMITH only)
```

## Key Extensions

| Extension | Phase Integration | DataForge Tables | Description |
|-----------|-------------------|------------------|-------------|
| Experience Store | Plan (read), Reflect (write) | `execution_experiences` | Agents learn from past executions via pgvector similarity search |
| Gate Analytics | Read-only aggregation | Existing `gate_results` | Statistical analysis of gate pass/fail patterns |
| Skill Nomination | Reflect phase | `nominated_skills` | Agents detect and propose reusable skill patterns |
| Governed Broadcast | Tool #36 | None (routing only) | Agents communicate findings across agent boundaries via ForgeCommand |

**Architecture Invariants:**
1. All four extensions operate within the existing Policy Engine — no governance bypass
2. DataForge is the single source of truth for all persisted state
3. All cost caps remain enforced (embedding calls count against CostTracking)
4. Memory writes happen at Reflect phase, not end-of-run

---

# PHASE 6 — FORGEAGENTS MATURATION (P2)

**Gate:** Phase 4 or Phase 5 substantially complete.  
**Estimated effort:** 4–6 focused sessions  

## Session 6.1 — Test Coverage to 85%

**Priority:** P1 (per ForgeAgents roadmap)  
**Focus areas:** `app/nodes/` (35 execution nodes), `app/capabilities/`, `app/cortex/`

**Prompt:**

```
Bring ForgeAgents test coverage from current level to 85%+.

FOCUS AREAS (ordered by coverage gap):
1. app/nodes/ — 35 execution nodes across 7 tiers. Each node needs at minimum:
   - Input validation test
   - Happy path execution test
   - Error handling test
   - Policy compliance test (verify policy check is called)

2. app/capabilities/ — Capability registry and matching. Test:
   - Capability registration
   - Archetype-to-capability mapping
   - Unknown capability handling

3. app/cortex/ — Agent reasoning layer. Test:
   - Phase transitions (Plan→Act→Observe→Reflect→Decide)
   - Max iteration enforcement (10 iterations)
   - Timeout enforcement (300s)
   - Memory read/write during Reflect phase

CONSTRAINTS:
  - Use pytest with pytest-asyncio
  - Mock DataForge, NeuroForge, Rake clients
  - Each node test file: tests/unit/nodes/test_{node_name}.py
  - Follow existing test patterns in ForgeAgents/tests/

MEASUREMENT:
  - Run: pytest tests/ --cov=app --cov-report=term-missing
  - Target: 85%+ overall, 80%+ per module

ACCEPTANCE CRITERIA:
  - [ ] Coverage ≥ 85%
  - [ ] Zero regressions
  - [ ] All new tests pass
  - [ ] mypy and ruff clean
```

## Session 6.2 — Deep Mode Environment Safety Gate

**Priority:** P2

**Prompt:**

```
Implement a production environment safety gate for BugCheck deep mode.

REQUIREMENT: When FORGE_ENVIRONMENT=production (or unset), deep mode checks must be
rejected before execution begins. Deep mode runs static analysis that could be
disruptive or resource-intensive in production environments.

IMPLEMENTATION:
1. In app/agents/bugcheck/agent.py:
   - Check FORGE_ENVIRONMENT at run initialization
   - If "production" and mode is "deep": raise DeepModeProductionError
   - Log security event

2. In app/agents/bugcheck/cli.py:
   - Check FORGE_ENVIRONMENT before parsing --deep flag
   - Exit with code 1 and clear message if production

3. In app/agents/bugcheck/executor.py:
   - Validate RunIntent mode against environment
   - Reject before any tool calls are made

4. Allow override via ALLOW_DEEP_MODE_PRODUCTION=true (must be explicitly set)
   - Log warning when override is used
   - Include override status in run metadata

TESTS:
  - Test each enforcement point independently
  - Test override behavior
  - Test that non-deep modes still work in production
  - Location: ForgeAgents/tests/unit/test_deep_mode_safety.py

ACCEPTANCE CRITERIA:
  - [ ] Deep mode rejected in production (all 3 enforcement points)
  - [ ] Override works when explicitly enabled
  - [ ] Standard/light modes unaffected
  - [ ] Security event logged on rejection
  - [ ] Tests pass
```

## Session 6.3 — Global XAI Rate Limiting

**Priority:** P3

**Prompt:**

```
Implement a global XAI/MAID rate limiter backed by DataForge for cross-run rate limiting.

PROBLEM: The current 50 XAI calls/run cap is per-run only. Concurrent ecosystem runs
could exceed XAI provider rate limits. The current GlobalRateLimiter is a process-wide
singleton that resets on restart.

IMPLEMENTATION:
1. DataForge schema (new table: global_rate_limits):
   - provider (varchar, indexed)
   - window_start (timestamp)
   - window_duration_seconds (int)
   - current_count (int)
   - max_count (int)
   - Row-level locking for atomic increment

2. DataForge endpoint:
   - POST /api/v1/rate-limits/check — atomically increment and return allow/deny
   - Uses SELECT FOR UPDATE for atomicity
   - Sliding window (not fixed intervals)

3. ForgeAgents integration:
   - Check global limit before each XAI call
   - If denied: queue with backpressure (wait up to 30s for slot)
   - If still denied: skip XAI enrichment, flag finding as xai_rate_limited: true
   - Graceful degradation to per-run limits if DataForge endpoint unavailable

ACCEPTANCE CRITERIA:
  - [ ] global_rate_limits table exists with Alembic migration
  - [ ] Atomic increment endpoint works under concurrent load
  - [ ] ForgeAgents checks global limit before XAI calls
  - [ ] Backpressure queues requests when within wait threshold
  - [ ] Findings flagged when XAI skipped due to rate limit
  - [ ] Graceful degradation if DataForge unavailable
  - [ ] Tests pass (both DataForge and ForgeAgents)
```

## Session 6.4 — Trending Analytics

**Priority:** P3

**Prompt:**

```
Complete the ForgeAgents trending analytics system for BugCheck findings.

FEATURES:
1. Historical severity trends — track severity distribution over time
   - Per-service severity breakdown (S0-S4 counts per run)
   - Trend direction (improving/stable/degrading) per service

2. Flaky test detection — identify tests that alternate pass/fail
   - Track test results across runs
   - Flag tests with >20% flip rate as "flaky"
   - Surface in BugCheck reports

3. Finding recurrence rates — detect findings that keep coming back
   - Hash-based matching of similar findings across runs
   - Recurrence count and first/last seen timestamps
   - Flag chronic findings (>3 recurrences) for escalation

STORAGE: All trending data persists to DataForge via existing BugCheck finding endpoints.

ACCEPTANCE CRITERIA:
  - [ ] Severity trend data computed and available via API
  - [ ] Flaky test detection working with configurable threshold
  - [ ] Finding recurrence tracking with hash matching
  - [ ] All data persisted to DataForge
  - [ ] SYSTEM.md updated
```

---

# PHASE 7 — FORGECOMMAND EVOLUTION (P3)

**Gate:** Phases 1–3 complete. Phases 4–6 substantially complete.  
**Estimated effort:** 8–12 focused sessions (major feature work)

## Session 7.1 — Headless Mode Design

**Priority:** P3

**Prompt:**

```
Design and implement a headless (CLI-driven) operation mode for ForgeCommand
to enable CI/CD automation.

REQUIREMENTS:
1. ForgeCommand must be invokable from command line without GUI
2. All orchestration capabilities available via CLI subcommands:
   - forge health — ecosystem health check
   - forge run bugcheck --targets=NeuroForge,DataForge — trigger BugCheck run
   - forge status — current ecosystem status
   - forge costs — cost summary
3. Output formats: JSON (machine), table (human), quiet (exit codes only)
4. Configuration via env vars and config file (no interactive prompts)
5. Credential access via the same encrypted vault (no new credential paths)

DESIGN CONSTRAINTS:
  - Reuse existing Rust backend services — do not duplicate business logic
  - CLI is a thin layer over the existing service modules
  - All ForgeCommand invariants still apply (credential isolation, audit logging)
  - Output must be parseable by CI/CD tools (GitHub Actions, GitLab CI)

DELIVERABLES:
  - Architecture design document
  - CLI subcommand specification with input/output schemas
  - Implementation plan with phased approach
```

## Session 7.2 — Multi-User Support Design

**Priority:** P3

**Prompt:**

```
Design a shared authority model for ForgeCommand to support team operation.

REQUIREMENTS:
1. Multiple operators can use ForgeCommand (currently single-operator only)
2. Role-based access:
   - Admin: full access, credential management, run approval
   - Operator: can trigger runs, view dashboards, cannot manage credentials
   - Viewer: read-only access to dashboards and reports
3. Credential isolation maintained — operators never see plaintext API keys
4. Audit trail attributes actions to specific operators
5. Concurrent operation safety — no conflicting run triggers

DESIGN CONSTRAINTS:
  - ForgeCommand remains a desktop application (not web-served)
  - DataForge manages user accounts and roles (existing auth stack)
  - ForgeCommand vault adds role-based access control layer
  - Must work offline (role cache with sync)

DELIVERABLES:
  - Feature Specification (per BDS_STANDARD_OPERATING_PROCEDURES §3)
  - Contract Impact Assessment
  - Data model changes
  - Phased implementation plan
```

---

# ARCHITECTURE INVARIANTS (Apply to ALL Phases)

These are non-negotiable. Every session, every implementation must respect them. If a design conflicts, stop and escalate.

1. **DataForge is the single source of truth.** All durable state writes go to DataForge. No local truth caches.
2. **ForgeCommand is the root of trust.** All credentials brokered through ForgeCommand vault.
3. **The Five Integration Laws are inviolable.** No direct frontend-to-service calls. All AI through NeuroForge. All persistence through DataForge. ForgeCommand is sole token issuer. Health reporting mandatory.
4. **Policy evaluation order: Safety → Domain → Resource.** No bypasses.
5. **All cost caps are enforced, not advisory.** XAI: max 50 calls/run. MAID: max 20 fixes/run.
6. **Fail fast, degrade explicitly.** Silent fallbacks are banned. All degradation is declared and logged.
7. **Human authority.** AI systems recommend, generate, execute — but do not decide what is acceptable.
8. **Evidence-first.** If evidence does not exist, the event is treated as non-existent.
9. **Svelte 5 runes only. Rust 2024 edition only. Pydantic v2 only. FastAPI exclusively.**
10. **BugCheck may never write lifecycle transitions. Only ForgeCommand owns lifecycle state.**

---

# COMPLETION GATE

After all phases are complete, run the full ecosystem verification:

```bash
# 1. Rebuild all SYSTEM.md files
for service in NeuroForge DataForge ForgeAgents rake forge-smithy ForgeCommand; do
  cd $service/doc/system && bash BUILD.sh && cd -
done

# 2. Verify health endpoints
for port in 8000 8001 8002 8010 8003; do
  curl -sf http://localhost:$port/health && echo "$port: OK" || echo "$port: FAIL"
done

# 3. Run all test suites
cd NeuroForge && pytest tests/ -v --tb=short && cd -
cd DataForge && pytest tests/ -v --tb=short && cd -
cd rake && pytest tests/ -v --tb=short && cd -
cd ForgeAgents && pytest tests/ -v --tb=short && cd -

# 4. Integration audit
# Run BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md §11 template against all apps

# 5. Verify no remaining violations
grep -r '9100' */doc/system/                    # Zero hits
grep -r 'OPENAI_API_KEY' Author-Forge/          # Zero hits
grep -r '\[PLANNED\]' */doc/system/             # Zero hits
```

---

*Per BDS_DOCUMENTATION_PROTOCOL_v1.md §7.1 — this prompting plan is a session-level tactical guide. It does not supersede SYSTEM.md or Architecture Specs. All changes made during these sessions must be reflected back into the relevant SYSTEM.md part files and rebuilt.*

*Last updated: February 24, 2026*
