# BugCheck Agent - Claude Code Context

## Project Overview

You are implementing **BugCheck Agent**, an ecosystem-wide quality enforcement system for the Forge platform. This agent detects issues across all Forge services (NeuroForge, DataForge, Rake, VibeForge, ForgeAgents, AuthorForge), routes findings through AI intelligence layers (MAID/Claude, XAI/Grok) for analysis and fix generation, and persists all state to DataForge as the single source of truth.

**Repository:** `forgeagents`  
**Language:** Python 3.11+  
**Framework:** FastAPI  
**Location:** `src/agents/bugcheck/`

---

## Canonical Rules (NON-NEGOTIABLE)

### DataForge as Source of Truth
- **DataForge owns all durable state.** No other service persists truth.
- ForgeAgents (including BugCheck) are stateless beyond a run.
- All findings, runs, enrichments, and lifecycle events write to DataForge.
- If DataForge is unavailable, runs do not start. Period.

### Invariant Violations = System Fault
- Any attempt to bypass DataForge, violate lifecycle transitions, or write unauthorized data is a **system fault**, not a user error.
- Fail fast. Log as security event. No exceptions.

### API Boundary Enforcement
| Component | Authorized Writes |
|-----------|-------------------|
| ForgeCommand | run records, lifecycle transitions, run finalization |
| BugCheck | findings, progress events, check telemetry (requires run_token) |
| XAI/MAID | enrichment artifacts only (requires run_token) |
| VibeForge | user decisions only (requires user_token) |

**BugCheck may NEVER write lifecycle transitions.**  
**VibeForge may NEVER write findings.**

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ForgeCommand                          │
│              (Orchestration / Control Plane)             │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
   ┌────▼─────┐              ┌─────▼─────┐
   │ BugCheck │              │ DataForge │
   │  Agent   │─────────────▶│   (SoT)   │
   └────┬─────┘              └───────────┘
        │
   ┌────┴────┐
   │         │
┌──▼──┐   ┌──▼──┐
│ XAI │   │MAID │
│(Grok)│   │(Claude)│
└─────┘   └─────┘
```

---

## File Structure

```
forgeagents/
├── src/
│   ├── agents/
│   │   └── bugcheck/
│   │       ├── __init__.py
│   │       ├── agent.py              # Main BugCheckAgent class
│   │       ├── executor.py           # Parallel execution engine
│   │       ├── topology.py           # Service topology from DataForge
│   │       ├── lifecycle.py          # State machine enforcement
│   │       ├── audit.py              # Append-only event logging
│   │       ├── correlation.py        # Root cause correlation
│   │       ├── trending.py           # Historical analysis
│   │       ├── dataforge_client.py   # DataForge API client
│   │       ├── forgecommand.py       # ForgeCommand operation
│   │       ├── cli.py                # CLI interface
│   │       │
│   │       ├── schemas/
│   │       │   ├── __init__.py
│   │       │   └── models.py         # Pydantic models from JSON schemas
│   │       │
│   │       ├── checks/
│   │       │   ├── __init__.py
│   │       │   ├── base.py           # Check interface
│   │       │   ├── registry.py       # Check registry
│   │       │   ├── stack_detector.py # Stack detection
│   │       │   │
│   │       │   ├── python/
│   │       │   │   ├── typecheck.py  # mypy/pyright
│   │       │   │   ├── lint.py       # ruff
│   │       │   │   └── tests.py      # pytest
│   │       │   │
│   │       │   ├── typescript/
│   │       │   │   ├── typecheck.py  # tsc
│   │       │   │   ├── lint.py       # eslint
│   │       │   │   └── tests.py      # vitest/jest
│   │       │   │
│   │       │   ├── rust/
│   │       │   │   ├── check.py      # cargo check
│   │       │   │   ├── clippy.py     # cargo clippy
│   │       │   │   └── tests.py      # cargo test
│   │       │   │
│   │       │   ├── security/
│   │       │   │   ├── gitleaks.py   # Secret scanning
│   │       │   │   └── dependency_audit.py
│   │       │   │
│   │       │   ├── cross_service/
│   │       │   │   ├── contract_drift.py
│   │       │   │   ├── dependency_alignment.py
│   │       │   │   └── config_coherence.py
│   │       │   │
│   │       │   └── deep/
│   │       │       ├── failure_sim.py
│   │       │       ├── fuzzer.py
│   │       │       └── flake_detector.py
│   │       │
│   │       ├── routing/
│   │       │   ├── __init__.py
│   │       │   ├── xai_router.py     # XAI routing logic
│   │       │   └── maid_router.py    # MAID routing logic
│   │       │
│   │       ├── xai/
│   │       │   ├── __init__.py
│   │       │   ├── client.py         # XAI API client
│   │       │   └── cache.py          # Caching layer
│   │       │
│   │       ├── maid/
│   │       │   ├── __init__.py
│   │       │   ├── fix_generator.py  # Fix proposal generation
│   │       │   └── changeset.py      # Multi-repo changesets
│   │       │
│   │       └── reports/
│   │           ├── __init__.py
│   │           └── generator.py      # JSON/Markdown reports
│   │
│   └── api/
│       └── routes/
│           ├── bugcheck.py           # REST endpoints
│           └── bugcheck_ws.py        # WebSocket endpoint
│
├── tests/
│   └── agents/
│       └── bugcheck/
│           ├── test_agent.py
│           ├── test_checks.py
│           ├── test_lifecycle.py
│           └── test_routing.py
│
└── schemas/
    └── bugcheck/
        ├── service.manifest.schema.json
        ├── bugcheck_run.schema.json
        ├── finding.schema.json
        ├── enrichment.schema.json
        ├── lifecycle_event.schema.json
        ├── run_token.schema.json
        └── user_token.schema.json
```

---

## Key Data Models

### BugCheckRun
```python
class BugCheckRun(BaseModel):
    run_id: UUID
    run_type: Literal["service_run", "ecosystem_run", "workflow_run"]
    targets: list[str]
    mode: Literal["quick", "standard", "deep"]
    scope: Literal["changed_files", "package", "full_repo"]
    commit_sha: str
    status: Literal["pending", "running", "finalizing", "finalized", "failed"]
    started_at: datetime
    completed_at: datetime | None
    severity_counts: SeverityCounts
    gating_result: Literal["pass", "block"]
    is_baseline: bool = False
```

### Finding
```python
class Finding(BaseModel):
    finding_id: UUID
    run_id: UUID
    fingerprint: str  # Stable across runs
    correlation_id: UUID | None
    severity: Literal["S0", "S1", "S2", "S3", "S4"]
    category: Literal["security", "performance", "test", "contract", "lint", "dependency", "migration"]
    confidence: float  # 0.0-1.0
    title: str
    description: str
    location: FindingLocation
    lifecycle_state: LifecycleState
    autofix_available: bool
    provenance: str  # Which check produced this
    created_at: datetime
```

### LifecycleState
```python
class LifecycleState(str, Enum):
    NEW = "NEW"
    TRIAGED = "TRIAGED"
    FIX_PROPOSED = "FIX_PROPOSED"
    APPROVED = "APPROVED"
    APPLIED = "APPLIED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    DISMISSED = "DISMISSED"
```

### Severity Levels
| Level | Name | Behavior |
|-------|------|----------|
| S0 | Release Blocker | Blocks all merges and deployments |
| S1 | High | Blocks PR merge |
| S2 | Medium | Warning, no block |
| S3 | Low | Informational |
| S4 | Info | Advisory only |

---

## Check Interface

Every check implements this interface:

```python
from abc import ABC, abstractmethod
from typing import Literal

class Check(ABC):
    id: str
    description: str
    cost: Literal["low", "med", "high"]
    categories: list[str]
    stacks: list[StackProfile]
    
    @abstractmethod
    async def run(self, ctx: CheckContext) -> list[Finding]:
        """Execute the check and return findings."""
        pass

class CheckContext:
    repo_path: Path
    mode: Mode
    scope: Scope
    run_token: str
    stack_profile: StackProfile
    changed_files: list[Path] | None
    env: dict[str, str]
```

---

## Fingerprinting Rules

### Default Fingerprint
```python
fingerprint = hash(f"{category}:{rule_id}:{file_path}:{line_range}:{normalized_message}")
```

### Category-Specific Fingerprints
| Category | Fingerprint Composition |
|----------|------------------------|
| API Contract Drift | `hash(service + schema_path + field_name + change_type)` |
| Dependency CVE | `hash(package_name + version_range + cve_id)` |
| Endpoint Failure | `hash(service + endpoint + method + status_class)` |
| Flaky Test | `hash(test_file + test_name + failure_signature)` |

---

## Intelligence Routing

### XAI Routing Thresholds
| Condition | Action |
|-----------|--------|
| Category = security | Always route to XAI |
| Category = dependency | Route if severity ≥ S2 |
| Category = deprecation | Route for doc lookup |
| Confidence < 0.6 | Route for context |
| Category = lint/format | Skip XAI |

### Caching Policy
| Source | TTL |
|--------|-----|
| CVE lookups | 24 hours |
| Documentation | 7 days |
| Stack Overflow | 48 hours |

### Fallback Behavior
- **XAI unavailable:** Proceed with MAID-only, flag as "degraded enrichment"
- **MAID unavailable:** Report findings without fix proposals, flag as "analysis pending"
- **Both unavailable:** Complete with raw findings only, alert operator

---

## Token Semantics

### run_token
- **TTL:** 30 minutes (max 60)
- **Scope:** Bound to `{run_id, targets, mode, scope, commit_sha}`
- **Replay protection:** Includes nonce
- **Allowed operations:** Write findings, progress events, enrichment

### user_token
- **Used for:** Lifecycle transitions (triage, approve, dismiss)
- **Never used for:** Writing findings or enrichment

---

## State Machine Transitions

```
NEW → TRIAGED → FIX_PROPOSED → APPROVED → APPLIED → VERIFIED → CLOSED
    ↘ DISMISSED (requires reason + scope + expiration)
```

**Enforce at API level.** Invalid transitions return 409 Conflict.

**Run immutability:** After FINALIZED, reject new findings with 409.

---

## Performance Budgets

| Mode | Max Runtime | Concurrency |
|------|-------------|-------------|
| --quick | 60 seconds | Sequential |
| --standard | 10 minutes | Parallel services |
| --deep | 30 minutes | Full parallel |
| --ecosystem | 45 minutes | Full parallel + deps |

### API Cost Controls
- XAI: Max 50 calls per run
- MAID: Max 20 fix proposals per run
- Monthly cap with 80% alerting

---

## Code Style

### Svelte 5 Runes (MANDATORY)

All Svelte code MUST use Svelte 5 runes. Never write Svelte 4 patterns.

| Svelte 4 (BANNED) | Svelte 5 (REQUIRED) |
|-------------------|---------------------|
| `export let prop` | `let { prop } = $props()` |
| `let x = value` (reactive) | `let x = $state(value)` |
| `$: derived = ...` | `const derived = $derived(...)` |
| `$: { sideEffect }` | `$effect(() => { sideEffect })` |
| `<slot />` | `{@render children()}` with `Snippet` type |
| `<slot name="x" />` | `{@render x()}` with named `Snippet` props |
| `on:click={handler}` | `onclick={handler}` |
| `on:input={handler}` | `oninput={handler}` |
| `createEventDispatcher()` | Callback props: `onSave?: (data) => void` |
| `bind:value` (two-way) | `$bindable()` in props definition |

```svelte
<!-- CORRECT: Svelte 5 -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = {
    title: string;
    count?: number;
    onSave?: (data: string) => void;
    children?: Snippet;
  };

  const { title, count = 0, onSave, children }: Props = $props();
  let localCount = $state(count);
  const doubled = $derived(localCount * 2);

  $effect(() => {
    console.log('count changed:', localCount);
  });
</script>

<button onclick={() => onSave?.(title)}>Save</button>
{#if children}{@render children()}{/if}
```

### Rust 2024 Edition (MANDATORY)

All Rust code MUST target Rust 2024 edition. Set in `Cargo.toml`:

```toml
[package]
edition = "2024"
```

Key Rust 2024 patterns:

- Use `gen` blocks for generators when stable
- Prefer `async fn` in traits (now stable)
- Use new `unsafe_op_in_unsafe_fn` lint (warn by default)
- Lifetime elision in more positions
- `impl Trait` in more positions

### Python Standards
- Python 3.11+
- Type hints everywhere
- Pydantic v2 for models
- async/await for I/O
- ruff for linting
- pytest for testing

### Naming Conventions
- Classes: PascalCase
- Functions/variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Files: snake_case.py

### Error Handling
```python
# Always use specific exceptions
class BugCheckError(Exception):
    """Base exception for BugCheck."""
    pass

class DataForgeUnavailableError(BugCheckError):
    """Raised when DataForge is not accessible."""
    pass

class InvalidStateTransitionError(BugCheckError):
    """Raised when lifecycle transition is invalid."""
    pass
```

### Logging
```python
import structlog
logger = structlog.get_logger()

# Include run_id in all logs
logger.info("finding_created", run_id=run_id, finding_id=finding_id, severity=severity)
```

---

## Testing Requirements

- **Unit tests:** All check modules, state machine, token handling
- **Integration tests:** DataForge persistence, API endpoints
- **Coverage target:** 85%+

```python
# Example test structure
class TestLifecycleTransitions:
    def test_valid_transition_new_to_triaged(self):
        ...
    
    def test_invalid_transition_new_to_approved(self):
        with pytest.raises(InvalidStateTransitionError):
            ...
    
    def test_finalized_run_rejects_new_findings(self):
        ...
```

---

## Git Workflow

- Feature branches for all changes
- Commit frequently with descriptive messages
- Run linting before commit
- Never push directly to main

---

## Commands Reference

```bash
# Run BugCheck locally
forge bugcheck --quick
forge bugcheck --standard --service neuroforge
forge bugcheck --deep --fuzz
forge bugcheck --ecosystem

# Run tests
pytest tests/agents/bugcheck/ -v

# Type checking
mypy src/agents/bugcheck/

# Linting
ruff check src/agents/bugcheck/
ruff format src/agents/bugcheck/
```

---

## Implementation Order

1. **Phase 0:** JSON Schemas in `schemas/bugcheck/`
2. **Phase 1:** Pydantic models, stack detector, check registry, basic checks, DataForge client
3. **Phase 2:** ForgeCommand integration, parallel executor, cross-service checks
4. **Phase 2.5:** Lifecycle enforcement, audit logging
5. **Phase 3:** WebSocket streaming, query endpoints
6. **Phase 4:** MAID integration, correlation engine
7. **Phase 5:** XAI integration, caching
8. **Phase 6:** Deep mode, fuzzing, trending

---

## What NOT to Do

❌ **No local truth caches** - All state goes to DataForge  
❌ **No agent-side persistence** - BugCheck is stateless beyond a run  
❌ **No MAID/XAI authority** - They produce proposals, never final truth  
❌ **No partial runs** - If DataForge is down, runs don't start  
❌ **No silent fallbacks** - All degraded states are explicit and logged  
❌ **No bypassing lifecycle** - State machine is enforced, not suggested

---

## Questions?

If you're unsure about any architectural decision, refer to:
1. This CLAUDE.md file (canonical)
2. BugCheck_Agent_Plan_v1.2.1_FINAL.docx (full specification)
3. Ask for clarification rather than guessing

**When in doubt: fail fast, log everything, write to DataForge.**

---

## Forge:SMITH (forge-smithy)

Forge:SMITH is the Authority Layer for the Forge Ecosystem - a governance-enforced AI engineering workbench.

**Repository:** `forge-smithy`
**Language:** Rust (Tauri 2.0 backend) + TypeScript/Svelte 5 (frontend)
**Location:** `/home/charlie/Forge/ecosystem/forge-smithy`

### Command Organization (219 Commands)

Commands are organized into domain-specific modules under `src-tauri/src/`:

| Domain | Commands | Location |
|--------|----------|----------|
| Runtime | 3 | `commands/runtime.rs` |
| Signals | 2 | `signals.rs` |
| Images | 11 | `images/commands.rs` |
| Branding | 8 | `images/branding/commands.rs` |
| BuildGuard | 36 | `buildguard/commands.rs` |
| IPC | 3 | `commands/ipc_commands.rs` |
| Smithy | 28 | `smithy/*.rs` |
| Repos | 3 | `repos/mod.rs` |
| Smelter | 9 | `smelter/commands.rs` |
| Cache | 1 | `cache_v1/commands.rs` |
| ForgeCommand | 4 | `forgecommand/commands.rs` |
| ForgeAgents | 4 | `forgeagents_proxy.rs` |
| Generative | 9 | `generative_nodes/*.rs` |
| Audit | 7 | `audit/commands.rs` |
| SMITH Assist | 18 | `assist/*.rs` |
| SMITH Authority | 14 | `smith/*.rs` |
| Governance | 26 | `governance/*.rs` |
| MRPA | 12 | `mrpa/commands.rs` |
| Evidence | 5 | `evidence/*.rs` |
| Attestation | 7 | `attestation/*.rs` |
| SAS | 5 | `sas/*.rs` |
| Telemetry | 2 | `telemetry/*.rs` |
| Research | 2 | `research/*.rs` |

### Key Modules

- **commands/** - Centralized command registry with domain re-exports
- **smith/** - RTCFX Authority Layer (cryptographic signing, run intents, evidence packets)
- **buildguard/** - Quality gate enforcement, ledger, patchset operations, verification ladder
- **smithy/** - Release governance, encyclopedia, evidence bundles
- **assist/** - SMITH Assist narrator (read-only governance chatbot)
- **mrpa/** - Minimal Rust Patch Applier (deterministic patch execution with governance)

### Documentation Requirement (MANDATORY)

**`/docs/smith` is the mirror of the code.** Any changes to forge-smithy code MUST include corresponding updates to the documentation in `/docs/smith/`.

When you add, modify, or remove:

- **Components** → Update `docs/smith/COMPONENTS.md` (counts, categories, component lists)
- **Stores** → Update `docs/smith/STORES.md` (store table, file summary)
- **Routes** → Update `docs/smith/UI_ROUTES.md` (route tables)
- **Tauri Commands** → Update `docs/smith/COMMANDS.md` (command tables)
- **Any of the above** → Update `docs/smith/README.md` (system metrics table)

The documentation files track:

| File | Tracks |
|------|--------|
| `README.md` | System metrics (routes, commands, stores, components), quick links |
| `COMPONENTS.md` | All 243 Svelte components by category |
| `STORES.md` | All 44 Svelte stores with state descriptions |
| `UI_ROUTES.md` | All 64 routes with state dependencies |
| `COMMANDS.md` | All 219 Tauri commands by domain |

**Failure to update documentation is a task failure.** The docs must always reflect the current code state.
