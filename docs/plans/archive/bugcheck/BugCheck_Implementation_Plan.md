# BugCheck Agent Implementation Plan
## Development Task Breakdown for VS Code Claude

**Version:** 1.0  
**Date:** December 2025  
**Target:** ForgeAgents repository (Python/FastAPI)  
**Estimated Duration:** 12.5 weeks

---

## Overview

This document provides a phase-by-phase implementation breakdown for BugCheck Agent, designed for systematic development using VS Code Claude. Each phase includes specific tasks, file structures, dependencies, and acceptance criteria.

**Repository Structure:**
```
forgeagents/
├── src/
│   ├── agents/
│   │   └── bugcheck/           # BugCheck agent implementation
│   │       ├── __init__.py
│   │       ├── agent.py        # Main BugCheckAgent class
│   │       ├── checks/         # Individual check modules
│   │       ├── schemas/        # Pydantic models
│   │       ├── routing/        # Intelligence routing
│   │       └── reports/        # Report generation
│   ├── api/
│   │   └── routes/
│   │       └── bugcheck.py     # API endpoints
│   └── core/
│       └── tokens.py           # Token management
├── tests/
│   └── agents/
│       └── bugcheck/           # Test suite
└── schemas/                    # JSON Schema files (Phase 0)
```

---

## Phase 0: Runtime Contract (Week 1)

### Objective
Lock all specifications before building. Create JSON Schema files that become the contract between services.

### Tasks

#### 0.1 Create Schema Directory Structure
```
forgeagents/schemas/bugcheck/
├── service.manifest.schema.json
├── bugcheck_run.schema.json
├── finding.schema.json
├── enrichment.schema.json
├── lifecycle_event.schema.json
├── run_token.schema.json
└── user_token.schema.json
```

#### 0.2 service.manifest.schema.json
Define the service manifest format:
- `name` (string, required): Service identifier
- `version` (string, required): Semantic version
- `stack` (enum): python-fastapi | typescript-sveltekit | rust-tauri | mixed
- `port` (integer, required): Default port
- `health_endpoints` (array of strings): Health check paths
- `dependencies` (array of strings): Required services
- `required_env_vars` (array of strings): Environment variables
- `api_contract` (string): Path to OpenAPI spec
- `client_package` (string): Generated client package name
- `fuzz_endpoints` (array of strings, optional): Designated fuzz test endpoints

#### 0.3 bugcheck_run.schema.json
Define the run record format:
- `run_id` (string, uuid, required)
- `run_type` (enum): service_run | ecosystem_run | workflow_run
- `targets` (array of strings, required): Service names
- `mode` (enum): quick | standard | deep
- `scope` (enum): changed_files | package | full_repo
- `commit_sha` (string, required)
- `status` (enum): pending | running | finalizing | finalized | failed
- `started_at` (datetime)
- `completed_at` (datetime, nullable)
- `severity_counts` (object): { s0: int, s1: int, s2: int, s3: int, s4: int }
- `gating_result` (enum): pass | block
- `is_baseline` (boolean, default false)

#### 0.4 finding.schema.json
Define the finding format:
- `finding_id` (string, uuid, required)
- `run_id` (string, uuid, required)
- `fingerprint` (string, required): Stable identifier
- `correlation_id` (string, uuid, nullable): Groups related findings
- `severity` (enum): S0 | S1 | S2 | S3 | S4
- `category` (enum): security | performance | test | contract | lint | dependency | migration
- `confidence` (number, 0.0-1.0)
- `title` (string, required)
- `description` (string, required)
- `location` (object): { service, file_path, line_start, line_end }
- `lifecycle_state` (enum): NEW | TRIAGED | FIX_PROPOSED | APPROVED | APPLIED | VERIFIED | CLOSED | DISMISSED
- `autofix_available` (boolean)
- `provenance` (string): Which check produced this
- `created_at` (datetime)

#### 0.5 enrichment.schema.json
Define enrichment artifact format:
- `enrichment_id` (string, uuid)
- `finding_id` (string, uuid, required)
- `source` (enum): xai | maid
- `version` (integer): Enrichment version for this finding
- `content` (object): Source-specific payload
- `status` (enum): pending | accepted | rejected
- `created_at` (datetime)

#### 0.6 lifecycle_event.schema.json
Define append-only audit trail:
- `event_id` (string, uuid)
- `finding_id` (string, uuid, required)
- `from_state` (string, required)
- `to_state` (string, required)
- `actor` (string, required): user_id or system
- `reason` (string, nullable)
- `scope` (enum, nullable): local | branch | global (for dismissals)
- `expires_at` (datetime, nullable): For dismissals
- `timestamp` (datetime, required)

#### 0.7 run_token.schema.json
Define run token structure:
- `token` (string, required)
- `run_id` (string, uuid, required)
- `targets` (array of strings)
- `mode` (string)
- `scope` (string)
- `commit_sha` (string)
- `nonce` (string): Replay protection
- `issued_at` (datetime)
- `expires_at` (datetime)
- `revoked` (boolean, default false)

#### 0.8 user_token.schema.json
Define user-scoped token:
- `token` (string, required)
- `user_id` (string, required)
- `roles` (array of strings)
- `allowed_services` (array of strings)
- `issued_at` (datetime)
- `expires_at` (datetime)

### Acceptance Criteria
- [ ] All 7 JSON Schema files created and valid
- [ ] Schemas pass JSON Schema Draft 2020-12 validation
- [ ] Pydantic models generated from schemas
- [ ] Schema documentation generated

---

## Phase 1: MVP Foundation (Weeks 2-3)

### Objective
Core detection pipeline with basic checks and DataForge persistence.

### Tasks

#### 1.1 Create Pydantic Models
**File:** `src/agents/bugcheck/schemas/models.py`
- Generate from JSON schemas
- Add validation methods
- Include serialization helpers

#### 1.2 Stack Detection Module
**File:** `src/agents/bugcheck/checks/stack_detector.py`
- Detect Python (pyproject.toml, requirements.txt, setup.py)
- Detect TypeScript (package.json with typescript)
- Detect Rust (Cargo.toml)
- Return `StackProfile` enum

#### 1.3 Check Interface
**File:** `src/agents/bugcheck/checks/base.py`
```python
class Check(ABC):
    id: str
    description: str
    cost: Literal["low", "med", "high"]
    categories: list[str]
    stacks: list[StackProfile]
    
    @abstractmethod
    async def run(self, ctx: CheckContext) -> list[Finding]:
        pass
```

#### 1.4 Check Registry
**File:** `src/agents/bugcheck/checks/registry.py`
- Register checks by ID
- Filter by stack, cost, category
- Support mode-based selection (quick/standard/deep)

#### 1.5 Basic Checks Implementation

**Python Checks:**
- `src/agents/bugcheck/checks/python/typecheck.py` - mypy/pyright
- `src/agents/bugcheck/checks/python/lint.py` - ruff
- `src/agents/bugcheck/checks/python/tests.py` - pytest

**TypeScript Checks:**
- `src/agents/bugcheck/checks/typescript/typecheck.py` - tsc --noEmit
- `src/agents/bugcheck/checks/typescript/lint.py` - eslint
- `src/agents/bugcheck/checks/typescript/tests.py` - vitest/jest

**Rust Checks:**
- `src/agents/bugcheck/checks/rust/check.py` - cargo check
- `src/agents/bugcheck/checks/rust/clippy.py` - cargo clippy
- `src/agents/bugcheck/checks/rust/tests.py` - cargo test

#### 1.6 Security Checks
- `src/agents/bugcheck/checks/security/gitleaks.py` - Secret scanning
- `src/agents/bugcheck/checks/security/dependency_audit.py` - pip-audit, npm audit, cargo audit

#### 1.7 DataForge Client
**File:** `src/agents/bugcheck/dataforge_client.py`
- `write_run(run: BugCheckRun) -> str`
- `write_finding(finding: Finding) -> str`
- `write_progress_event(run_id: str, event: dict)`
- `get_service_manifests() -> list[ServiceManifest]`

#### 1.8 BugCheckAgent Core
**File:** `src/agents/bugcheck/agent.py`
```python
class BugCheckAgent:
    async def run(
        self,
        repo_path: Path,
        mode: Mode,
        scope: Scope,
        run_token: str
    ) -> BugCheckReport
```

#### 1.9 CLI Interface
**File:** `src/agents/bugcheck/cli.py`
- `forge bugcheck --quick`
- `forge bugcheck --standard`
- `forge bugcheck --service <name>`

#### 1.10 Report Generator
**File:** `src/agents/bugcheck/reports/generator.py`
- Generate JSON report
- Generate Markdown report
- Calculate health score (0-100)

### Acceptance Criteria
- [ ] Stack detection works for Python, TypeScript, Rust
- [ ] At least 9 checks implemented (3 per stack)
- [ ] Security checks (gitleaks, dependency audit) working
- [ ] Findings persist to DataForge
- [ ] CLI commands functional
- [ ] Health score calculation correct
- [ ] 80%+ test coverage for Phase 1 code

---

## Phase 2: ForgeCommand Integration (Weeks 4-5)

### Objective
Register BugCheck as ForgeCommand operation with ecosystem-aware orchestration.

### Tasks

#### 2.1 ForgeCommand Operation Registration
**File:** `src/agents/bugcheck/forgecommand.py`
- Register as operation type `bugcheck`
- Define operation schema
- Implement operation handler

#### 2.2 Service Topology Integration
**File:** `src/agents/bugcheck/topology.py`
- Fetch manifests from DataForge
- Build dependency graph
- Determine execution order

#### 2.3 Parallel Execution Engine
**File:** `src/agents/bugcheck/executor.py`
- Execute independent services in parallel
- Respect dependency ordering
- Aggregate results

#### 2.4 Cross-Service Checks

**Contract Validation:**
- `src/agents/bugcheck/checks/cross_service/contract_drift.py`
- Fetch OpenAPI specs
- Generate clients
- Compile and detect breaking changes

**Dependency Alignment:**
- `src/agents/bugcheck/checks/cross_service/dependency_alignment.py`
- Compare shared library versions across services

**Config Coherence:**
- `src/agents/bugcheck/checks/cross_service/config_coherence.py`
- Validate env vars, ports, connection strings

#### 2.5 Ephemeral Container Execution
**File:** `src/agents/bugcheck/isolation.py`
- Docker/Compose environment setup
- Resource limits (CPU, memory, time)
- Cleanup after run

#### 2.6 API Endpoints
**File:** `src/api/routes/bugcheck.py`
```python
POST /bugcheck/runs          # Start a run
GET  /bugcheck/runs/{id}     # Get run status
GET  /bugcheck/runs/{id}/findings  # Get findings
POST /bugcheck/runs/{id}/cancel    # Cancel run
```

### Acceptance Criteria
- [ ] ForgeCommand integration complete
- [ ] Parallel execution with dependency awareness
- [ ] Cross-service checks detecting real issues
- [ ] Container isolation working
- [ ] API endpoints functional
- [ ] 80%+ test coverage

---

## Phase 2.5: Lifecycle + Audit Enforcement (Week 6)

### Objective
Protect state machine before UI and AI integration.

### Tasks

#### 2.5.1 State Machine Enforcement
**File:** `src/agents/bugcheck/lifecycle.py`
- Define valid transitions
- Reject invalid transitions at API level
- Return clear error messages

#### 2.5.2 Append-Only Event Log
**File:** `src/agents/bugcheck/audit.py`
- Write lifecycle events to DataForge
- Include actor, timestamp, reason
- Never delete or modify

#### 2.5.3 Dismissal Requirements
- Require reason for all dismissals
- Require scope (local/branch/global)
- Require expiration for non-permanent dismissals

#### 2.5.4 Run Immutability
- After FINALIZED, reject new findings
- Return 409 Conflict with clear message

#### 2.5.5 Anomaly Detection Hooks
**File:** `src/agents/bugcheck/anomaly.py`
- Track dismissal patterns
- Alert on suspicious activity (bulk dismissals, repeated S0 dismissals)

#### 2.5.6 API Boundary Enforcement
- Validate write operations against component type
- Reject unauthorized writes with 403

### Acceptance Criteria
- [ ] State machine rejects invalid transitions
- [ ] All transitions logged as events
- [ ] Dismissals require reason/scope/expiry
- [ ] Finalized runs reject new findings
- [ ] Anomaly hooks in place
- [ ] API boundary tests passing

---

## Phase 3: VibeForge Panel (Weeks 7-8)

### Objective
Developer interface integration (VibeForge side, documented here for context).

### Tasks (Backend Support)

#### 3.1 WebSocket Endpoint
**File:** `src/api/routes/bugcheck_ws.py`
- Real-time run progress
- Finding stream
- Status updates

#### 3.2 Query Endpoints
```python
GET  /bugcheck/findings?service=X&severity=S1,S2&state=NEW
GET  /bugcheck/findings/{id}
GET  /bugcheck/findings/{id}/enrichments
GET  /bugcheck/health  # Ecosystem health score
```

#### 3.3 Lifecycle Action Endpoints
```python
POST /bugcheck/findings/{id}/triage
POST /bugcheck/findings/{id}/dismiss
POST /bugcheck/findings/{id}/approve
```

### Acceptance Criteria
- [ ] WebSocket streaming working
- [ ] Query endpoints with filtering
- [ ] Lifecycle endpoints functional
- [ ] User token validation

---

## Phase 4: MAID Integration (Weeks 9-10)

### Objective
Intelligent fix generation with Claude.

### Tasks

#### 4.1 MAID Router
**File:** `src/agents/bugcheck/routing/maid_router.py`
- Determine which findings need MAID
- Prioritize by severity
- Respect budget limits

#### 4.2 Correlation Engine
**File:** `src/agents/bugcheck/correlation.py`
- Group related findings
- Identify root causes
- Assign correlation_id

#### 4.3 Fix Proposal Generator
**File:** `src/agents/bugcheck/maid/fix_generator.py`
- Send finding context to MAID
- Receive fix proposal
- Score confidence
- Store enrichment in DataForge

#### 4.4 Multi-Repo Changeset
**File:** `src/agents/bugcheck/maid/changeset.py`
- When fix spans multiple repos
- Generate unified diff
- Track affected services

#### 4.5 Diff Viewer Support
- Generate unified diff format
- Include context lines
- Support multi-file changes

### Acceptance Criteria
- [ ] MAID routing respects thresholds
- [ ] Correlation engine grouping correctly
- [ ] Fix proposals generated with confidence
- [ ] Enrichments stored in DataForge
- [ ] Multi-repo changesets working

---

## Phase 5: XAI Integration (Week 11)

### Objective
Real-time external intelligence with Grok.

### Tasks

#### 5.1 XAI Client
**File:** `src/agents/bugcheck/xai/client.py`
- CVE lookup
- Documentation lookup
- Error pattern search

#### 5.2 XAI Router
**File:** `src/agents/bugcheck/routing/xai_router.py`
- Route security findings
- Route deprecation warnings
- Route low-confidence findings

#### 5.3 Caching Layer
**File:** `src/agents/bugcheck/xai/cache.py`
- CVE cache (24h TTL)
- Documentation cache (7d TTL)
- Stack Overflow cache (48h TTL)
- Cache key: hash(query + source + version)

#### 5.4 Fallback Behavior
- XAI unavailable: proceed with MAID-only, flag as degraded
- Log degraded state
- Retry logic for transient failures

### Acceptance Criteria
- [ ] XAI client functional
- [ ] Routing respects thresholds
- [ ] Caching working with correct TTLs
- [ ] Fallback behavior tested

---

## Phase 6: Deep Mode & Polish (Weeks 12-13)

### Objective
Comprehensive validation and hardening.

### Tasks

#### 6.1 Failure Simulation
**File:** `src/agents/bugcheck/checks/deep/failure_sim.py`
- Service kill/restart
- Latency injection
- Connection drops

#### 6.2 Fuzz Mode
**File:** `src/agents/bugcheck/checks/deep/fuzzer.py`
- Input fuzzing on designated endpoints
- Invalid payloads
- Edge cases

#### 6.3 Flake Detection
**File:** `src/agents/bugcheck/checks/deep/flake_detector.py`
- Run tests N times
- Flag unstable tests
- Calculate flake rate

#### 6.4 Baseline Support
- Mark runs as baseline
- Compare against baseline instead of previous run
- `--baseline <run_id>` flag

#### 6.5 Historical Trending
**File:** `src/agents/bugcheck/trending.py`
- Query historical data from DataForge
- Calculate trend metrics
- Identify recurring issues

#### 6.6 CI/CD Integration
- GitHub Actions workflow
- PR gate configuration
- Nightly run setup

#### 6.7 Runbooks
- Document all runbook procedures
- Implement alerting hooks

### Acceptance Criteria
- [ ] Deep mode failure simulation working
- [ ] Fuzz mode with designated endpoints
- [ ] Flake detection accurate
- [ ] Baseline comparison functional
- [ ] CI/CD workflows created
- [ ] Runbooks documented
- [ ] Overall test coverage 85%+

---

## Testing Strategy

### Unit Tests
- Each check module
- Schema validation
- State machine transitions
- Token handling

### Integration Tests
- DataForge persistence
- ForgeCommand operations
- API endpoints
- WebSocket streaming

### End-to-End Tests
- Full run lifecycle
- Cross-service validation
- MAID/XAI integration

### Performance Tests
- Mode runtime budgets
- Parallel execution efficiency
- Memory limits

---

## Dependencies

### Python Packages
```
fastapi>=0.109.0
pydantic>=2.5.0
httpx>=0.26.0
asyncio
docker
pyyaml
jsonschema
```

### External Tools
```
mypy, pyright (Python type checking)
ruff (Python linting)
pytest (Python testing)
tsc (TypeScript)
eslint (TypeScript linting)
vitest, jest (TypeScript testing)
cargo (Rust)
gitleaks (secret scanning)
pip-audit, npm audit, cargo audit (dependency scanning)
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Test Coverage | 85%+ |
| Quick Mode Runtime | <60s |
| Standard Mode Runtime | <10min |
| Deep Mode Runtime | <30min |
| False Positive Rate | <5% |
| Finding Accuracy | >95% |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| DataForge unavailability | Queue runs as PENDING, explicit operator messaging |
| XAI/MAID rate limits | Budget controls, caching, fallback modes |
| Container isolation failures | Resource limits, cleanup hooks, health checks |
| Schema drift | Phase 0 lock, schema versioning |
| Performance regression | Runtime budgets, parallel execution |

---

## Next Steps

1. Review and approve Phase 0 schemas
2. Set up development environment
3. Begin Phase 1 implementation
4. Weekly progress reviews

