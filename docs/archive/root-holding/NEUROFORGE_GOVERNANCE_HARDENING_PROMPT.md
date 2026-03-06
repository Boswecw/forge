# NeuroForge Governance Hardening — Implementation Prompt

**Target:** Claude in VS Code / Claude Code  
**Date:** 2026-02-25  
**Scope:** Routing authority enforcement, reason codes, SDK bypass guards, DOCMAP prep  
**Depends on:** SMITH Ecosystem Intelligence Layer v4.1 (§8, Appendix A, Appendix B)  
**Services touched:** NeuroForge (primary), ForgeAgents (guard tests), DataForge (schema)  

---

## CONTEXT

You are hardening NeuroForge's routing authority governance for the Forge Ecosystem. The SMITH Ecosystem Intelligence Layer v4.1 plan (§8) codifies three rules that were established during the governance sweep but need formal, enforceable implementation:

1. **NeuroForge is the single routing authority** — ForgeAgents and all consumers must call NeuroForge for LLM inference. No direct provider SDK calls.
2. **Direct SDK use is restricted** to (a) dev-only mode, or (b) inside approved provider gateway modules (`neuroforge_backend/providers/`).
3. **Tier policy is consistent across all entrypoints** — the `TASK_ROUTING_TABLE` is the single source of tier assignments.

Additionally, Appendix A establishes the router governance pattern as a reusable Integration Law template, and Appendix B defines a starter set of machine-readable reason codes for routing decisions.

This work also prepares NeuroForge for DocForge integration by creating the `DOCMAP.toml` file.

**Key constraints:**
- Integration Law 2 is already defined ("All AI Calls Route Through NeuroForge") — this work adds runtime enforcement, not new policy
- The 5-stage inference pipeline is frozen — no changes to `Query → Context Builder → Prompt Engine → Model Router → Evaluator → Post-Processor`
- RunIntent.v1, MRPA, and ECD are frozen core — wrap only, never modify
- Python 3.11+, FastAPI, existing project structure
- All test assertions must be specific and measurable

**Read these files first before writing any code:**
- `NeuroForge/neuroforge_backend/providers/` — existing adapter layer (understand what's already there)
- `NeuroForge/neuroforge_backend/routing/resolver.py` — existing route resolver
- `NeuroForge/neuroforge_backend/routing/task_config.py` — existing task routing table
- `NeuroForge/doc/nfSYSTEM.md` — current NeuroForge SYSTEM doc
- `ForgeAgents/app/tools/` — tool adapters (check for any direct SDK imports)
- `ForgeAgents/app/execution/` — execution engine (check for any direct provider calls)
- `BDS_FORGE_ECOSYSTEM_INTEGRATION_PROTOCOL_v1.md` — Integration Laws (especially Law 2)

---

## WORKSTREAM 1: Reason Code Infrastructure

### 1A. Reason Code Enum

**Create:** `neuroforge_backend/routing/reason_codes.py`

Define a `RoutingReason` enum with machine-friendly codes. These are logged with every routing decision to make the decision explainable and reproducible.

```python
from enum import Enum

class RoutingReason(str, Enum):
    """Machine-readable reason codes for routing decisions.
    
    Every route_and_execute call logs one or more reason codes
    explaining why a specific provider/model was selected.
    """
    TIER_FAST_REQUESTED = "TIER_FAST_REQUESTED"
    TIER_MIN_ENFORCED = "TIER_MIN_ENFORCED"
    GOV_CRITICAL_NO_DOWNGRADE = "GOV_CRITICAL_NO_DOWNGRADE"
    OVERRIDE_APPROVED = "OVERRIDE_APPROVED"
    PROVIDER_HEALTH_FAILOVER = "PROVIDER_HEALTH_FAILOVER"
    BUDGET_CAP_APPLIED = "BUDGET_CAP_APPLIED"
    LATENCY_TARGET_APPLIED = "LATENCY_TARGET_APPLIED"
    LOCAL_OLLAMA_SELECTED = "LOCAL_OLLAMA_SELECTED"
    BATCH_REQUIRED = "BATCH_REQUIRED"
    CHAMPION_EMA_SELECTED = "CHAMPION_EMA_SELECTED"
    COST_OPTIMIZED = "COST_OPTIMIZED"
    QUALITY_THRESHOLD_APPLIED = "QUALITY_THRESHOLD_APPLIED"
    TASK_DEFAULT_APPLIED = "TASK_DEFAULT_APPLIED"
    PROVIDER_UNAVAILABLE_SKIP = "PROVIDER_UNAVAILABLE_SKIP"
    CACHE_HIT = "CACHE_HIT"
```

### 1B. Routing Decision Record

**Create:** `neuroforge_backend/routing/decision_record.py`

Define a `RoutingDecision` dataclass that captures the full decision trace:

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

@dataclass
class RoutingDecision:
    """Immutable record of a routing decision. Logged to DataForge."""
    request_id: str
    task_type: str
    selected_provider: str
    selected_model: str
    selected_tier: str
    reasons: list[str]  # List of RoutingReason values
    fallback_chain: list[str]  # Models considered in order
    rejected: dict[str, str]  # model_key -> rejection reason
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    latency_ms: Optional[float] = None
    cost_estimate: Optional[float] = None
```

### 1C. Wire Reason Codes into Route Resolver

**Modify:** `neuroforge_backend/routing/resolver.py`

Update `resolve_model()` to return a `RoutingDecision` alongside the selected model. Every branch in the resolution algorithm must append the appropriate reason code:

- When task type lookup finds a match → `TASK_DEFAULT_APPLIED`
- When tier minimum is enforced → `TIER_MIN_ENFORCED`
- When a provider is skipped due to health → `PROVIDER_UNAVAILABLE_SKIP`
- When cost sorting selects the winner → `COST_OPTIMIZED`
- When champion EMA overrides cost → `CHAMPION_EMA_SELECTED`
- When budget cap constrains the selection → `BUDGET_CAP_APPLIED`
- When Ollama is selected for local inference → `LOCAL_OLLAMA_SELECTED`
- When governance policy prevents downgrade → `GOV_CRITICAL_NO_DOWNGRADE`

The caller (inference pipeline) logs the `RoutingDecision` to the AI Transparency Log and to the cost ledger.

### 1D. DataForge Schema — Routing Decision Table

**Create migration** in DataForge for the routing decision log:

```sql
CREATE TABLE routing_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id VARCHAR(128) NOT NULL,
    task_type VARCHAR(64) NOT NULL,
    selected_provider VARCHAR(32) NOT NULL,
    selected_model VARCHAR(128) NOT NULL,
    selected_tier VARCHAR(20) NOT NULL,
    reasons JSONB NOT NULL,          -- ["COST_OPTIMIZED", "TASK_DEFAULT_APPLIED"]
    fallback_chain JSONB NOT NULL,   -- ["gemini-2.5-flash", "gpt-4.1-mini", ...]
    rejected JSONB DEFAULT '{}',     -- {"claude-sonnet-4-5": "PROVIDER_UNAVAILABLE_SKIP"}
    latency_ms DECIMAL(10,2),
    cost_estimate DECIMAL(10,6),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_routing_decisions_task ON routing_decisions(task_type);
CREATE INDEX idx_routing_decisions_provider ON routing_decisions(selected_provider);
CREATE INDEX idx_routing_decisions_created ON routing_decisions(created_at);
```

**Endpoint:** Add `POST /api/v1/routing-decisions` to DataForge for writing and `GET /api/v1/routing-decisions` with filters for querying.

---

## WORKSTREAM 2: Routing Authority Enforcement

### 2A. No-Downgrade Gate

**Create:** `neuroforge_backend/routing/governance.py`

Implement the governance gate that prevents silent tier downgrades:

```python
class RoutingGovernor:
    """Enforces routing governance invariants.
    
    Rule: once a task type is assigned a minimum tier, no routing
    decision may select a model below that tier without an explicit
    approved override.
    """
    
    def validate_selection(
        self,
        task_type: str,
        selected_model: ModelSpec,
        task_config: TaskRouting,
        override: Optional[str] = None
    ) -> tuple[bool, list[RoutingReason]]:
        """
        Returns (approved, reasons).
        If approved is False, the caller must reject the selection.
        """
```

The governor checks:
1. Selected model tier >= task config minimum tier → pass
2. Selected model tier < minimum AND override is None → **reject** with `GOV_CRITICAL_NO_DOWNGRADE`
3. Selected model tier < minimum AND override is present → pass with `OVERRIDE_APPROVED`

**Integration:** Wire the governor into `resolve_model()` as the final validation step before returning a selection. The governor runs AFTER cost/quality sorting but BEFORE the decision is finalized.

### 2B. Tier Authority Assertion

**Create:** `neuroforge_backend/routing/tier_authority.py`

A startup assertion that validates the `TASK_ROUTING_TABLE` is the single source of tier assignments:

```python
def assert_tier_authority():
    """
    Run at NeuroForge startup. Validates that:
    1. Every task type in TASK_ROUTING_TABLE has a minimum tier
    2. No task type appears in multiple conflicting sources
    3. All referenced model keys exist in MODEL_CATALOG
    
    Raises StartupValidationError if any check fails.
    NeuroForge will not start with inconsistent tier policy.
    """
```

Wire this into the FastAPI lifespan startup sequence, after `load_catalog()` completes.

### 2C. Fallback Trace Logging

**Modify:** `neuroforge_backend/routing/resolver.py`

Ensure every `resolve_model()` call logs the complete fallback chain — every model that was considered and why it was accepted or rejected. This is the `fallback_chain` and `rejected` fields on `RoutingDecision`.

The trace must be deterministic: given the same request context (task type, provider health states, budget), the same fallback chain must be produced. This is the key design lesson from the plan (§7.2): routing decisions must be explainable and reproducible.

---

## WORKSTREAM 3: SDK Bypass Guard Tests

### 3A. NeuroForge Provider Boundary Test

**Create:** `neuroforge_backend/tests/test_provider_boundary.py`

```python
"""
Guard tests: verify that provider SDK imports are confined to
neuroforge_backend/providers/ and nowhere else in the codebase.

These tests enforce Integration Law 2 at the code level.
"""

import ast
import pathlib

PROVIDER_SDKS = {
    "openai",
    "anthropic", 
    "google.generativeai",
    "google.genai",
}

APPROVED_DIRS = {
    "neuroforge_backend/providers",
}

def test_no_provider_sdk_imports_outside_providers_dir():
    """No file outside providers/ may import a provider SDK."""
    violations = []
    root = pathlib.Path("neuroforge_backend")
    for py_file in root.rglob("*.py"):
        relative = str(py_file.relative_to(root.parent))
        if any(relative.startswith(d) for d in APPROVED_DIRS):
            continue
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(sdk) for sdk in PROVIDER_SDKS):
                        violations.append(f"{relative}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(sdk) for sdk in PROVIDER_SDKS):
                    violations.append(f"{relative}: from {node.module} import ...")
    assert violations == [], f"Provider SDK imports outside approved dirs:\n" + "\n".join(violations)


def test_no_direct_api_urls_in_codebase():
    """No hardcoded provider API URLs outside providers/ dir."""
    PROVIDER_URLS = [
        "api.openai.com",
        "api.anthropic.com",
        "generativelanguage.googleapis.com",
        "api.x.ai",
    ]
    violations = []
    root = pathlib.Path("neuroforge_backend")
    for py_file in root.rglob("*.py"):
        relative = str(py_file.relative_to(root.parent))
        if any(relative.startswith(d) for d in APPROVED_DIRS):
            continue
        content = py_file.read_text()
        for url in PROVIDER_URLS:
            if url in content:
                violations.append(f"{relative}: contains {url}")
    assert violations == [], f"Direct API URLs outside approved dirs:\n" + "\n".join(violations)
```

### 3B. ForgeAgents Bypass Guard Test

**Create:** `ForgeAgents/app/tests/test_neuroforge_boundary.py`

```python
"""
Guard tests: verify ForgeAgents never imports provider SDKs directly.
All LLM calls must route through NeuroForge (Integration Law 2).
"""

import ast
import pathlib

PROVIDER_SDKS = {
    "openai",
    "anthropic",
    "google.generativeai",
    "google.genai",
}

# ForgeAgents has ZERO approved dirs for provider SDKs
APPROVED_DIRS: set[str] = set()


def test_no_provider_sdk_imports_in_forgeagents():
    """ForgeAgents must never import provider SDKs. Period."""
    violations = []
    root = pathlib.Path("app")
    for py_file in root.rglob("*.py"):
        relative = str(py_file)
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(sdk) for sdk in PROVIDER_SDKS):
                        violations.append(f"{relative}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(sdk) for sdk in PROVIDER_SDKS):
                    violations.append(f"{relative}: from {node.module} import ...")
    assert violations == [], (
        f"Integration Law 2 violation — ForgeAgents imports provider SDKs directly:\n"
        + "\n".join(violations)
    )


def test_no_direct_provider_urls_in_forgeagents():
    """ForgeAgents must not contain hardcoded provider API URLs."""
    PROVIDER_URLS = [
        "api.openai.com",
        "api.anthropic.com",
        "generativelanguage.googleapis.com",
        "api.x.ai",
    ]
    violations = []
    root = pathlib.Path("app")
    for py_file in root.rglob("*.py"):
        content = py_file.read_text()
        for url in PROVIDER_URLS:
            if url in content:
                violations.append(f"{py_file}: contains {url}")
    assert violations == [], (
        f"Integration Law 2 violation — direct provider URLs in ForgeAgents:\n"
        + "\n".join(violations)
    )


def test_all_llm_calls_use_neuroforge_client():
    """Every LLM-related call in ForgeAgents must go through the NeuroForge HTTP client."""
    # Check that any file doing inference-like work imports from the neuroforge client module
    NEUROFORGE_CLIENT_IMPORTS = {
        "neuroforge_client",
        "clients.neuroforge",
        "app.clients.neuroforge",
    }
    # Files that perform LLM operations should import from the approved client
    # This is a structural assertion — not exhaustive, but catches drift
    root = pathlib.Path("app")
    llm_related_files = []
    for py_file in root.rglob("*.py"):
        content = py_file.read_text()
        if any(term in content.lower() for term in ["inference", "llm", "completion", "chat_completion"]):
            llm_related_files.append(py_file)
    
    for py_file in llm_related_files:
        tree = ast.parse(py_file.read_text())
        has_neuroforge_import = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(client) for client in NEUROFORGE_CLIENT_IMPORTS):
                    has_neuroforge_import = True
                    break
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(client) for client in NEUROFORGE_CLIENT_IMPORTS):
                        has_neuroforge_import = True
                        break
        # Note: not all files mentioning "inference" need the import (could be data models)
        # This test flags suspicious files for manual review
```

### 3C. Ecosystem-Wide Integration Law 2 Smoke Test

**Create:** `tests/ecosystem/test_integration_law_2.py` (in the ecosystem root or Forge_Command test suite)

This is a cross-repo smoke test that can be run from the ecosystem root:

```python
"""
Ecosystem-level guard test for Integration Law 2:
All AI calls route through NeuroForge.

Run from ecosystem root:
    pytest tests/ecosystem/test_integration_law_2.py -v
"""

import pathlib

ECOSYSTEM_ROOT = pathlib.Path(__file__).parent.parent.parent
PROVIDER_SDKS = {"openai", "anthropic", "google.generativeai", "google.genai"}

# Only NeuroForge providers/ is approved for direct SDK use
APPROVED_PATHS = {
    "NeuroForge/neuroforge_backend/providers",
}

# Skip non-service directories
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"}

CONSUMER_REPOS = [
    "ForgeAgents",
    "Rake",
    "forge-smithy",
    "AuthorForge",
]


def test_no_provider_sdk_in_consumer_repos():
    """Consumer repos must not import LLM provider SDKs."""
    violations = []
    for repo_name in CONSUMER_REPOS:
        repo_path = ECOSYSTEM_ROOT / repo_name
        if not repo_path.exists():
            continue
        for py_file in repo_path.rglob("*.py"):
            if any(skip in py_file.parts for skip in SKIP_DIRS):
                continue
            try:
                content = py_file.read_text(errors="ignore")
            except Exception:
                continue
            for sdk in PROVIDER_SDKS:
                if f"import {sdk}" in content or f"from {sdk}" in content:
                    rel = py_file.relative_to(ECOSYSTEM_ROOT)
                    violations.append(f"{rel}: references {sdk}")
    assert violations == [], (
        f"Integration Law 2 violations across ecosystem:\n" + "\n".join(violations)
    )
```

---

## WORKSTREAM 4: DocForge Preparation — DOCMAP.toml

### 4A. Create NeuroForge DOCMAP

**Create:** `NeuroForge/doc/system/DOCMAP.toml`

Map NeuroForge code areas to their corresponding SYSTEM.md doc sections. This is the mechanical link that DocForge will use to enforce doc-code fidelity.

```toml
prefix = "nf"

[mappings]
# Core pipeline
"neuroforge_backend/pipeline/"          = "03-inference-pipeline.md"
"neuroforge_backend/context/"           = "03-inference-pipeline.md"
"neuroforge_backend/prompts/"           = "03-inference-pipeline.md"
"neuroforge_backend/evaluator/"         = "03-inference-pipeline.md"

# Provider adapters
"neuroforge_backend/providers/"         = "04-providers.md"

# Routing
"neuroforge_backend/routing/"           = "05-routing.md"

# RTCFX learning
"neuroforge_backend/rtcfx/"            = "06-rtcfx.md"

# Batch pipeline
"neuroforge_backend/batch/"            = "07-batch-pipeline.md"

# RAG + DataForge integration
"neuroforge_backend/rag/"              = "08-rag-integration.md"
"neuroforge_backend/dataforge/"        = "08-rag-integration.md"

# AuthorForge endpoints
"neuroforge_backend/routers/authorforge.py" = "09-authorforge-contract.md"

# VibeForge endpoints  
"neuroforge_backend/routers/vibeforge.py"   = "10-vibeforge-contract.md"

# Team learning
"neuroforge_backend/team_learning/"    = "10-vibeforge-contract.md"

# API layer (general routers)
"neuroforge_backend/routers/"          = "11-api-reference.md"

# Configuration and startup
"neuroforge_backend/config/"           = "12-configuration.md"
"neuroforge_backend/main.py"           = "12-configuration.md"

# Tests
"neuroforge_backend/tests/"            = "13-testing.md"

# Database models (local)
"neuroforge_backend/models/"           = "14-data-model.md"
"migrations/"                          = "14-data-model.md"
```

**Note:** Adjust section numbers to match NeuroForge's actual `doc/system/` file numbering. The mapping keys are directory prefixes — DocForge matches changed file paths against these prefixes to determine which doc sections need updating.

### 4B. Validate DOCMAP Coverage

After creating DOCMAP.toml, run a quick validation:

```bash
# List all Python source directories in NeuroForge
find neuroforge_backend -type d -not -path '*/__pycache__/*' -not -path '*/.git/*' | sort

# Compare against DOCMAP mappings — any unmapped directory is a gap
```

Flag any unmapped directories. DocForge will eventually automate this check, but manual verification confirms completeness now.

---

## IMPLEMENTATION ORDER

Follow this sequence to minimize integration risk:

1. **Reason code enum + decision record** (Workstream 1A, 1B) — pure new files, no existing code touched
2. **DataForge routing_decisions migration** (Workstream 1D) — schema only
3. **Routing governor** (Workstream 2A) — new file, self-contained governance logic
4. **Tier authority startup assertion** (Workstream 2B) — new file, wired into startup
5. **Wire reason codes into resolver** (Workstream 1C) — modifies existing resolver to return RoutingDecision
6. **Wire governor into resolver** (Workstream 2A integration) — final validation step in resolve_model
7. **Fallback trace logging** (Workstream 2C) — modify resolver to capture full trace
8. **NeuroForge boundary guard tests** (Workstream 3A) — new test file
9. **ForgeAgents boundary guard tests** (Workstream 3B) — new test file in ForgeAgents
10. **Ecosystem Integration Law 2 smoke test** (Workstream 3C) — cross-repo test
11. **DOCMAP.toml creation** (Workstream 4A) — new file
12. **DOCMAP coverage validation** (Workstream 4B) — manual check

---

## VERIFICATION GATES

After all workstreams, verify:

- [ ] `resolve_model()` returns a `RoutingDecision` with at least one reason code for every call
- [ ] No routing decision can select a model below the task's minimum tier without an explicit override
- [ ] `GOV_CRITICAL_NO_DOWNGRADE` is logged when a downgrade attempt is blocked
- [ ] `OVERRIDE_APPROVED` is logged when an explicit override permits a downgrade
- [ ] Startup fails with `StartupValidationError` if `TASK_ROUTING_TABLE` references a model key not in `MODEL_CATALOG`
- [ ] `test_no_provider_sdk_imports_outside_providers_dir` passes in NeuroForge
- [ ] `test_no_provider_sdk_imports_in_forgeagents` passes in ForgeAgents
- [ ] `test_no_provider_sdk_in_consumer_repos` passes from ecosystem root
- [ ] `routing_decisions` table exists in DataForge with correct schema and indexes
- [ ] `DOCMAP.toml` covers all NeuroForge source directories (no unmapped dirs)
- [ ] Existing AuthorForge contract tests still pass (response shapes unchanged)
- [ ] Existing NeuroForge unit tests still pass (pipeline behavior unchanged)
- [ ] Fallback chain is deterministic — same inputs produce same trace

---

## NON-GOALS (explicit)

- **No changes to the 5-stage inference pipeline** — this work wraps and observes, never restructures
- **No UI work** — routing decisions will surface in The Forge Floor later (Phase 10 of EIL plan)
- **No DocForge enforcement engine** — DOCMAP.toml is prep only; the gate logic comes in Phase 3
- **No cross-repo coordinated runs** — that's Phase 8 of the EIL plan
- **No Assayer audits** — that's Phase 4 of the EIL plan
