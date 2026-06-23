# §7 — Frontend

UI conventions, IPC boundaries, and required Svelte/Tauri patterns in this chapter are canonical. Counts of components, routes, stores, and commands are current audited snapshot values.

## Framework Overview

The Forge ecosystem's primary frontend is **forge-smithy** (SMITH) — a desktop application built with **Tauri 2.0** (Rust backend) + **SvelteKit** (Svelte 5 frontend). It serves as the governance-enforced authority layer for the entire ecosystem.

| Aspect | Technology |
|--------|-----------|
| Desktop framework | Tauri 2.0 (Rust 2024 edition) |
| Frontend framework | SvelteKit + Svelte 5 (runes) |
| Package manager | pnpm |
| Styling | CSS custom properties (forge-tokens.css) + Tailwind v4 |
| IPC | `@tauri-apps/api/core` → `invoke<T>()` |
| State management | Svelte 5 `$state()` runes + exported singletons |

### Key Metrics

Current code snapshot:

| Metric | Count |
|--------|-------|
| Total `.svelte` files | 330 |
| Reusable components | 218 (34 categories) |
| Route files | 71 pages + 10 API endpoints |
| Store modules | 55 |
| Tauri commands | 444 |

---

## Svelte 5 Runes — Mandatory Patterns

All Svelte code MUST use Svelte 5 runes. Svelte 4 patterns are banned.

| Svelte 4 (BANNED) | Svelte 5 (REQUIRED) |
|-------------------|---------------------|
| `export let prop` | `let { prop } = $props()` |
| `let x = value` (reactive) | `let x = $state(value)` |
| `$: derived = ...` | `const derived = $derived(...)` |
| `$: { sideEffect }` | `$effect(() => { sideEffect })` |
| `<slot />` | `{@render children()}` with `Snippet` type |
| `<slot name="x" />` | `{@render x()}` with named `Snippet` props |
| `on:click={handler}` | `onclick={handler}` |
| `createEventDispatcher()` | Callback props: `onSave?: (data) => void` |
| `bind:value` (two-way) | `$bindable()` in props definition |

---

## Component Patterns

### Standard Component Structure

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = {
    title?: string;
    variant?: 'default' | 'elevated' | 'bordered';
    children?: Snippet;
    header?: Snippet;
    actions?: Snippet;
    onSave?: (data: string) => void;
  };

  let {
    title = '',
    variant = 'default',
    children,
    header,
    actions,
    onSave,
    ...rest
  }: Props = $props();

  let localState = $state(0);
  const computed = $derived(localState * 2);
  const classes = $derived.by(() =>
    ['panel', `panel-${variant}`].filter(Boolean).join(' ')
  );

  $effect(() => {
    console.log('state changed:', localState);
  });
</script>

<div class={classes} {...rest}>
  {#if header}{@render header()}{/if}
  {#if children}{@render children()}{/if}
  {#if actions}{@render actions()}{/if}
</div>
```

### Two-Way Binding (with `$bindable`)

```svelte
<script lang="ts">
  let {
    value = $bindable(''),
    error = '',
  }: { value: string; error?: string } = $props();
</script>

<input bind:value class:error={!!error} />
```

### Component Categories (Representative Snapshot Breakdown)

The table below is a representative snapshot breakdown. The audited top-line component total appears in the Key Metrics table above.

| Category | Count | Examples |
|----------|-------|---------|
| Layout | 6 | AppShell, Header, Sidebar, PageHeader, TriPaneLayout, Icon |
| Form | 3 | FormField, FormGroup, SubmitButton |
| Input | 4 | Button, Input, Select, Textarea |
| Container | 2 | Panel, Modal |
| Feedback | 6 | Badge, Alert, MetaRow, StateBanner, Notifications |
| Evidence | 6 | EvidenceViewer, EvidenceBundleList, PacketDetail |
| Assist | 15 | AssistPanel, AssistThread, NarrationBanner, ModeSelector |
| Research | 15 | ClaimMaturationBadge, ClaimTimeline, TrendingClaims |
| Knowledge | 14 | MissionCard, PipelineProgress, KpiCard, ActivityFeed |
| SCAFA | 6 | ScafaPanel, ScafaFindingCard, ScafaProofGateResult |
| RAG Eval | 4 | RagEvalGauge, RagEvalBreakdown, CragChunkGrid |
| SAS | 15 | SASDashboard, SASViolationTable, CdiGauge |
| Governance | 4 | GateDetailCard, SmelterProofPanel, GovernanceGlossary |

---

## Routing

### Global Layout Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Top Bar (48px)                               Command Palette │
├────────┬───────────────────────────────┬────────────────────┤
│        │                               │                    │
│ Side   │    Center Content Area        │  Right Context     │
│ Nav    │    (page routes)              │  Panel             │
│ (56-   │                               │  (collapsible)     │
│ 240px) │                               │                    │
│        │                               │                    │
├────────┴───────────────────────────────┴────────────────────┤
│  Status Footer (28px) — governance metrics, pipeline state   │
├─────────────────────────────────────────────────────────────┤
│  System Rail — priority banners (P0 orphan, P1 locked, P2)  │
└─────────────────────────────────────────────────────────────┘
```

### Global Layout Components

| Component | Purpose |
|-----------|---------|
| AppShell | Root layout container |
| Tri-Pane Layout | Left nav + center content + right context (all collapsible) |
| System Rail | Priority-based banners (P0: orphan run, P1: locked session, P2: offline service) |
| Status Footer | Persistent 28px footer with governance metrics |
| Command Palette | Global search + action dispatch (`--z-command-palette: 800`) |
| SMITH Assist | Governance narrator chatbot panel |
| Pipeline HUD | Step chevrons, lock badge, session context |
| Patch Cart | Staged file changes preview |

### Route Organization (Representative Snapshot Breakdown)

The table below summarizes major route groups. It is a breakdown view, not a second canonical total.

| Route Group | Pages | Purpose |
|-------------|-------|---------|
| `/` | 1 | Dashboard |
| `/admin` | 1 | Administrative panel |
| `/agents` | 1 | Agent management |
| `/analytics` | 1 | Usage analytics |
| `/architecture` | 1 | Architecture studio |
| `/audit` | 1 | Governance audit |
| `/code-review` | 1 | Code review sessions |
| `/encyclopedia` | 1 | Encyclopedia browse |
| `/evidence` | 1 | Evidence bundles |
| `/governance` | 1 | Governance dashboard |
| `/knowledge/*` | 8 | War Room, Mission Control, New Mission, Theater, Source Vault, Ledger, Archive, Evidence Detail |
| `/research/*` | 5 | Sessions, New, [id], Analytics, Search |
| `/planning` | 1 | Planning sessions |
| `/repos` | 1 | Repository management |
| Other routes | ~44 | Evaluator, execution, history, models, orchestration, etc. |
| API routes | 10 | Server-side data endpoints |

---

## Store Pattern

Stores use **plain objects with `$state()` runes** — not Svelte stores (`writable()`) — to avoid production build issues.

### Standard Store Structure

```typescript
// Internal reactive state (not exported directly)
let state = $state<{
  data: SomeType | null;
  status: 'idle' | 'loading' | 'ready' | 'error';
  message: string;
}>({
  data: null,
  status: 'idle',
  message: '',
});

// Exported singleton with getters + actions
export const myStore = {
  // Read-only getters
  get data() { return state.data; },
  get status() { return state.status; },
  get message() { return state.message; },

  // Actions
  async hydrate(): Promise<void> {
    state.status = 'loading';
    const result = await invoke<SomeType>('my_command');
    state.data = result;
    state.status = 'ready';
  },

  // Test helper
  _reset(): void {
    state.data = null;
    state.status = 'idle';
    state.message = '';
  },
};

// Optional class export for unit test instantiation
export class MyStore { /* mirrors singleton */ }
```

### Key Stores by Domain

| Store | Domain | State |
|-------|--------|-------|
| `pipeline` | Core | Step, sessionId, blueprint, lock state |
| `assistStore` | SMITH Assist | Messages, context, failurePatterns, fixProposals |
| `knowledgeStore` | Knowledge | Missions, search, cost tracking, pipeline progress |
| `researchStore` | Research | Claims, sources, MCP validation, enrichment, telemetry |
| `scafaStore` | SCAFA | Findings, proposals, proofGateResult, workflowPhase |
| `ragEvalStore` | RAG | Composite score, decision, remediation |
| `retrievalRouterStore` | RAG | Query complexity, retrieval strategy |
| `serviceHealthStore` | System | Circuit breaker status per service |
| `smelterDriftStore` | Governance | Drift reports, trust posture (T0-T4) |
| `trustDebtBiStore` | Governance | GFI report, operational patterns |
| `patchCartStore` | MRPA | Patch set, status, contract |
| `wizardStore` | Governance | Decision wizard steps, rationale |

---

## Tauri IPC Bridge

### Communication Pattern

Frontend → Rust backend communication uses `invoke()` from `@tauri-apps/api/core`:

```typescript
import { invoke } from '@tauri-apps/api/core';

// Query with typed response
const context = await invoke<AssistContext>('smith_assist_context_get', {
  sessionId: 'abc123',
});

// Mutation
await invoke('smith_assist_apply_fix', {
  fixId: 'fix-123',
  runId: 'run-456',
});
```

### IPC Principles

1. **No API keys cross the IPC boundary** — all credentials injected server-side from ForgeCommand vault
2. **Response types are generic** — `invoke<ResponseType>(command, payload)`
3. **Errors bubble as exceptions** — caught in try-catch blocks
4. **Token semantics handled in Rust** — `run_token`, `user_token` validated server-side
5. **Terminal states explicit** — `COMPLETED`, `FAILED`, `CANCELLED`

### Command Organization (Representative Domain Breakdown)

The table below highlights major command domains. The audited top-line command total appears in the Key Metrics table above.

| Domain | Count | Purpose |
|--------|-------|---------|
| Governance | 108 | Stop-ship, packaging, compliance, evidence, SBOM |
| BuildGuard | 39 | Quality gates, ledger, analytics, verification |
| Research | 36 | Rake API, MCP-v5.0, sessions, verification, telemetry |
| Smithy | 28 | Release governance, encyclopedia, evidence bundles |
| SMITH Assist | 18 | Narrator, incidents, fixes, context assembly |
| MRPA | 15 | Minimal Rust Patch Applier, deterministic patching |
| Knowledge | 13 | Knowledge retrieval, research missions |
| Generative | 9 | ForgeImages integration |
| Images | 11 | Image generation + branding |
| Smelter | 9 | Drift analysis, trust posture |
| SCAFA | 8 | Structural analysis + Proof Gate |
| RAG Eval | 7 | RAG quality gate + CRAG evaluation |
| Attestation | 7 | Cryptographic attestation |
| Audit | 7 | Governance audit trail |
| Molting | 7 | Policy molting proposals |
| Learning | 6 | Track B policy learning |
| SAS | 5 | Self-Assessment System |
| Evidence | 5 | Evidence packet management |
| MAID | 4 | CDI-aware validation routing |
| ForgeCommand | 4 | Desktop orchestration proxy |
| ForgeAgents | 6 | Agent proxy, gate analytics |
| Runtime | 3 | Token management, health ping |
| Service Client | 3 | Circuit breaker status |
| Replay Cache | 3 | Deterministic replay cache |
| Repos | 3 | Repository management |
| IPC | 3 | Low-level IPC |
| Signals | 2 | System signals |
| Research (Tauri) | 2 | Research-specific commands |
| Telemetry | 2 | Telemetry bridge |
| Cache | 1 | Cache management |

---

## SMITH Assist — Situational Awareness Engine (SAE)

SMITH Assist is a read-only governance chatbot that provides context-aware guidance. It uses a Situational Awareness Engine with these client-side modules:

| Module | File | Purpose |
|--------|------|---------|
| Context Assembler | `contextAssembler.ts` | Reads all frontend stores → builds SAEContext |
| Query Classifier | `queryClassifier.ts` | 8 intent types + BRIEFING/GOVERNED tiering |
| Route Prompt Registry | `routePromptRegistry.ts` | 25+ route-specific context prompts |
| Narrator Language | `narratorLanguage.ts` | Plain-English translations for pipeline/readiness/drift |
| Conversation Memory | `conversationMemory.ts` | Ring buffer (max 10), clean slate on mode switch |
| Narration Engine | `narrationEngine.ts` | State transition detection, rate-limited (5s) |
| Mode Suggester | `modeSuggester.ts` | Context-aware mode recommendations |

---

## Documentation Sync Requirement

Any changes to forge-smithy code MUST include corresponding documentation updates:

| Change | Update |
|--------|--------|
| Add/modify components | `docs/smith/COMPONENTS.md` |
| Add/modify stores | `docs/smith/STORES.md` |
| Add/modify routes | `docs/smith/UI_ROUTES.md` |
| Add/modify Tauri commands | `docs/smith/COMMANDS.md` |
| Any of the above | `docs/smith/README.md` (system metrics) |

---

*For design token definitions, see §6. For Tauri command backend details, see §9. For IPC security boundaries, see §10.*
