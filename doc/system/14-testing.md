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
