# ForgeAgents 120 Capabilities — Claude Code Build Prompt

**Project:** ForgeAgents  
**Location:** `/Forge/ForgeAgents/`  
**Port:** 8787  
**Stack:** Python 3.11+, FastAPI, Pydantic

---

## Mission

Build the 120 capabilities that power Forge:SMITH. These are internal BDS engineering capabilities, not customer features. Every capability must be:

- **Governance-first** — Authority checks before execution
- **Evidence-producing** — Audit-grade records of what happened
- **Fail-closed** — Uncertainty = escalation, not autonomous action
- **Authority-aware** — Respects Ring 0/1/2 boundaries

---

## Current ForgeAgents Structure

```
ForgeAgents/
├── app/
│   ├── api.py                    # FastAPI endpoints
│   ├── server.py                 # Uvicorn entrypoint
│   │
│   ├── agents/                   # Agent implementations (2,216 lines)
│   │   ├── base.py               # Base agent class
│   │   ├── registry.py           # Agent type registration
│   │   ├── lifecycle.py          # 5-phase execution engine
│   │   ├── assistant.py          # Writer agent (629 lines)
│   │   ├── developer.py          # Coder agent (582 lines)
│   │   ├── analyst.py            # Analyst agent (312 lines)
│   │   ├── research.py           # Researcher agent (385 lines)
│   │   └── coordinator.py        # Orchestrator agent (380 lines)
│   │
│   ├── policies/                 # Policy engine (2,409 lines)
│   │   ├── base.py               # Policy types (379 lines)
│   │   ├── engine.py             # Evaluation (357 lines)
│   │   ├── safety.py             # Safety policies (474 lines)
│   │   ├── domain.py             # Domain policies (415 lines)
│   │   └── resource.py           # Resource policies (567 lines)
│   │
│   ├── memory/                   # Memory system (2,322 lines)
│   │   ├── base.py               # Memory types (413 lines)
│   │   ├── manager.py            # Memory manager (783 lines)
│   │   ├── shortterm.py          # Short-term (289 lines)
│   │   ├── longterm.py           # Long-term (441 lines)
│   │   └── episodic.py           # Episodic (396 lines)
│   │
│   ├── tools/                    # Tool adapters (3,549 lines)
│   │   ├── base.py               # Adapter interface (301 lines)
│   │   ├── router.py             # Tool routing (397 lines)
│   │   ├── rake.py               # Rake adapter (833 lines, 9 tools)
│   │   ├── neuroforge.py         # NeuroForge adapter (740 lines, 6 tools)
│   │   ├── dataforge.py          # DataForge adapter (663 lines, 5 tools)
│   │   └── filesystem.py         # Filesystem adapter (615 lines, 3 tools)
│   │
│   └── evidence/                 # Evidence system
│       ├── __init__.py
│       ├── exporter.py           # Bundle creation with SHA-256
│       └── verifier.py           # Bundle integrity verification
│
├── tests/                        # Test suite
├── requirements.txt
└── README.md
```

---

## The 120 Capabilities to Build

### A. Authority & Governance (1–20)
**Location:** `app/policies/` + new `app/capabilities/authority/`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 1 | Authority boundary enforcement | Extend PolicyEngine |
| 2 | Human-in-the-loop gating | New HumanApprovalGate class |
| 3 | Read-only vs write-capable execution enforcement | Add execution_mode to context |
| 4 | Scope containment validation | Compare plan scope vs granted scope |
| 5 | Intent declaration validation | Validate intent hash matches plan |
| 6 | Issuer identity verification | JWT claim validation |
| 7 | Context class enforcement (GOVERNED/UNGOVERNED) | Context decorator |
| 8 | Privilege escalation detection | Compare requested vs held privileges |
| 9 | Authority ring validation | Ring 0/1/2 checks |
| 10 | Unsafe autonomy rejection | Block AI-initiated writes without approval |
| 11 | Execution veto handling | Veto state machine |
| 12 | Doctrine-based decision blocking | Load doctrine rules, evaluate |
| 13 | Mandatory human approval capture | Signature + timestamp recording |
| 14 | Governance state locking | Mutex on governance operations |
| 15 | Unauthorized execution prevention | Hard block on policy failure |
| 16 | Policy version enforcement | Version pinning check |
| 17 | Cross-service authority isolation | Service-scoped tokens |
| 18 | Authority provenance recording | Append-only authority log |
| 19 | Governance override audit logging | Log all override attempts |
| 20 | Authority revocation handling | Revocation propagation |

---

### B. Planning & Intent (21–35)
**Location:** New `app/capabilities/planning/`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 21 | Structured plan parsing | Pydantic models for plan schema |
| 22 | Goal extraction | NLP or structured field extraction |
| 23 | Constraint extraction | Parse constraint blocks |
| 24 | Deliverable identification | Extract deliverable list |
| 25 | Ambiguity detection | Flag unclear requirements |
| 26 | Incomplete plan detection | Required field validation |
| 27 | Multi-step plan normalization | Canonical step format |
| 28 | Deterministic plan canonicalization | RFC 8785 JSON |
| 29 | Planning request hashing | SHA-256 of canonical plan |
| 30 | Intent vs execution separation | Phase state machine |
| 31 | Multi-deliverable disambiguation | Conflict resolution |
| 32 | Plan scope risk scoring | Risk rubric evaluation |
| 33 | Unsafe plan rejection | Doctrine rule matching |
| 34 | Plan revision request generation | Structured feedback |
| 35 | Plan-to-pipeline mapping | Route to MAPO/MAID/Single |

---

### C. ETCOS Execution (36–55)
**Location:** New `app/capabilities/execution/` + extend `app/agents/lifecycle.py`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 36 | MAPO lane execution | Parallel lane orchestrator |
| 37 | MAID consensus orchestration | Voting/consensus logic |
| 38 | Cross-provider validation routing | Multi-LLM dispatch |
| 39 | Lane-specific risk handling | Per-lane policy binding |
| 40 | Red-team veto enforcement | Lane E veto check |
| 41 | Safety veto supremacy | Lane C always wins |
| 42 | Evidence-weighted routing (EARL) | Route by evidence strength |
| 43 | EVDR authorization enforcement | Evidence→Validate→Decide→Route |
| 44 | Fail-closed execution logic | Default to escalation |
| 45 | Execution pause & resume | Checkpoint/resume state |
| 46 | Execution abort handling | Clean abort with evidence |
| 47 | Partial execution containment | Isolate incomplete work |
| 48 | Multi-model disagreement detection | Compare model outputs |
| 49 | Execution confidence scoring | ECG calculation |
| 50 | Execution trace generation | Structured trace log |
| 51 | Token usage accounting | Per-operation token tracking |
| 52 | Latency measurement per stage | Timing instrumentation |
| 53 | Provider failure fallback | Fallback chain |
| 54 | Execution drift detection | Plan vs actual comparison |
| 55 | Execution reproducibility enforcement | Determinism checks |

---

### D. Evidence & Provenance (56–75)
**Location:** Extend `app/evidence/`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 56 | Evidence bundle generation | Already exists, extend |
| 57 | Evidence sufficiency validation | Minimum evidence rules |
| 58 | Evidence artifact typing | Type enum + validation |
| 59 | Cryptographic hashing (SHA-256) | Already exists |
| 60 | Canonical JSON generation (RFC 8785) | json-canonicalize library |
| 61 | Evidence immutability enforcement | Write-once storage |
| 62 | Evidence chain linking | Parent hash reference |
| 63 | Provenance header injection | Standard headers |
| 64 | Evidence timestamp normalization (UTC) | datetime.utcnow() |
| 65 | Evidence replay validation | Replay test harness |
| 66 | Evidence completeness checks | Required artifact list |
| 67 | Evidence rejection reasoning | Structured rejection |
| 68 | Evidence storage delegation (DataForge) | DataForge client call |
| 69 | Evidence lifecycle state tracking | State machine |
| 70 | Evidence corruption detection | Hash verification |
| 71 | Evidence verification tooling | CLI verify command |
| 72 | Manifest hash verification | Manifest integrity |
| 73 | Trust tier classification | Tier enum assignment |
| 74 | Evidence expiry handling | TTL enforcement |
| 75 | Evidence audit export | ZIP export with manifest |

---

### E. BuildGuard & Verification (76–95)
**Location:** New `app/capabilities/buildguard/`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 76 | BuildGuard invariant enforcement | Invariant registry + checks |
| 77 | Canonical reason code emission | Error code enum |
| 78 | Verification block orchestration | Verification pipeline |
| 79 | Test sufficiency analysis | Coverage threshold check |
| 80 | Dry-run execution validation | Dry-run flag + simulation |
| 81 | Release readiness checking | Release gate checklist |
| 82 | Quality gate evaluation | Quality metric thresholds |
| 83 | Invariant regression detection | Before/after comparison |
| 84 | Verification failure categorization | Failure type enum |
| 85 | Required-action generation | Remediation suggestions |
| 86 | Waiver detection & logging | Waiver registry |
| 87 | Block vs revise classification | Decision tree |
| 88 | Completeness validation | Required element check |
| 89 | Assumption detection | Assumption flagging |
| 90 | Risk tier escalation | Escalation rules |
| 91 | Post-execution verification | Outcome validation |
| 92 | Artifact consistency validation | Expected vs actual |
| 93 | Verification artifact hashing | Hash verification outputs |
| 94 | Verification replay checks | Replay capability |
| 95 | Verification summary generation | Human-readable summary |

---

### F. Repository & Identity (96–105)
**Location:** New `app/capabilities/repository/`

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 96 | Repo identity hashing | Git SHA + path hash |
| 97 | Deterministic tree capture | git ls-tree snapshot |
| 98 | Drift state detection | Live/Stale/Dirty/Detached enum |
| 99 | Drift-at-use recording | Snapshot at operation time |
| 100 | Repo context pack generation | SMELTER pack creation |
| 101 | Repo mutation detection | Before/after comparison |
| 102 | Evidence-repo binding | Link evidence to commit |
| 103 | Repo trust tier evaluation | Trust scoring |
| 104 | Repo integrity verification | Hash verification |
| 105 | Repo state provenance logging | State change log |

---

### G. Observability & Operator (106–120)
**Location:** New `app/capabilities/observability/` + extend existing

| # | Capability | Implementation Notes |
|---|------------|---------------------|
| 106 | Correlation ID propagation | Middleware + context |
| 107 | Distributed trace stitching | OpenTelemetry integration |
| 108 | Operator-legible error reporting | Error message formatting |
| 109 | Execution timeline visualization support | Timeline data structure |
| 110 | Structured log emission | JSON logging |
| 111 | Telemetry safety filtering | PII/secret redaction |
| 112 | Cache decision logging | Cache hit/miss logging |
| 113 | Performance metric emission | Prometheus metrics |
| 114 | Token cost attribution | Cost tracking per operation |
| 115 | Execution history querying | History search API |
| 116 | Operator intervention hooks | Manual override endpoints |
| 117 | State machine visibility | State introspection API |
| 118 | Audit-grade export formatting | Compliance export format |
| 119 | Incident replay support | Replay from evidence |
| 120 | Institutional memory persistence | Encyclopedia integration |

---

## Implementation Approach

### Phase 1: Foundation (Week 1)
Create the capability framework:

```python
# app/capabilities/base.py
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

class CapabilityContext(BaseModel):
    """Context passed to every capability."""
    correlation_id: str
    authority_ring: int  # 0, 1, or 2
    execution_mode: str  # "read_only" or "write"
    issuer_id: str
    policy_version: str

class CapabilityResult(BaseModel):
    """Standard result from capability execution."""
    success: bool
    evidence: dict | None = None
    error_code: str | None = None
    error_message: str | None = None

class Capability(ABC):
    """Base class for all 120 capabilities."""
    
    capability_id: int
    capability_name: str
    category: str  # A, B, C, D, E, F, or G
    requires_authority_ring: int = 2  # Minimum ring required
    produces_evidence: bool = True
    
    @abstractmethod
    async def execute(self, context: CapabilityContext, **kwargs) -> CapabilityResult:
        """Execute the capability."""
        pass
    
    @abstractmethod
    def validate_preconditions(self, context: CapabilityContext, **kwargs) -> bool:
        """Check if capability can execute."""
        pass
```

### Phase 2: Authority & Governance (Week 2)
Build capabilities 1–20 in `app/capabilities/authority/`

### Phase 3: Planning & Execution (Week 3)
Build capabilities 21–55 in `app/capabilities/planning/` and `app/capabilities/execution/`

### Phase 4: Evidence & Verification (Week 4)
Build capabilities 56–95 in `app/evidence/` and `app/capabilities/buildguard/`

### Phase 5: Repository & Observability (Week 5)
Build capabilities 96–120 in `app/capabilities/repository/` and `app/capabilities/observability/`

---

## Non-Negotiable Requirements

1. **Every capability must produce evidence** — No silent execution
2. **Authority checks before execution** — Ring validation mandatory
3. **Fail-closed on uncertainty** — Escalate, don't assume
4. **Correlation ID on everything** — Full traceability
5. **Pydantic models for all data** — Type safety enforced
6. **Tests for every capability** — Minimum 2 tests per capability

---

## Integration Points

| Service | Port | Used By Capabilities |
|---------|------|---------------------|
| DataForge | 8001 | 68, 115, 120 (evidence storage, history, memory) |
| NeuroForge | 8000 | 36–55 (all execution capabilities) |
| Rake | 8002 | Job processing |
| Forge:SMITH | 3001 | Calls all capabilities via API |

---

## File Naming Convention

```
app/capabilities/
├── __init__.py
├── base.py                      # Base classes
├── registry.py                  # Capability registry
├── authority/
│   ├── __init__.py
│   ├── cap_001_boundary.py      # Capability 1
│   ├── cap_002_human_gate.py    # Capability 2
│   └── ...
├── planning/
│   ├── __init__.py
│   ├── cap_021_plan_parse.py    # Capability 21
│   └── ...
├── execution/
├── evidence/
├── buildguard/
├── repository/
└── observability/
```

---

## Start Here

1. Create `app/capabilities/base.py` with the base classes above
2. Create `app/capabilities/registry.py` to register and discover capabilities
3. Implement Capability 1 (Authority boundary enforcement) as the template
4. Build out from there

**Do not proceed without explicit human approval on the architecture.**
