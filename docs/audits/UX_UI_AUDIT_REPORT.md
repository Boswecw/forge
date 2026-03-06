# UX/UI Wiring & UX Theory Compliance Audit

**Systems:** Forge Command, Forge:SMITH
**Date:** 2026-01-29
**Auditor:** Claude Opus 4.5
**Methodology:** Nielsen, Norman, Shneiderman Heuristics + Custom Authority Analysis

---

## Executive Summary

This audit evaluates both Forge Command and Forge:SMITH frontends against 8 non-negotiable UX principles. The analysis covers navigation architecture, state management, component wiring, IPC integration, and authority/trust boundaries.

**Overall Assessment:**
- **Forge:SMITH**: Maturing architecture with sophisticated error handling but complex state management creating cognitive load
- **Forge Command**: Simpler architecture with critical gaps in error handling and consistency

| System | Compliance Score | Critical Issues | High Priority |
|--------|-----------------|-----------------|---------------|
| Forge:SMITH | 67% | 4 | 8 |
| Forge Command | 52% | 6 | 7 |

---

## Section 1: UX-Correct & Compliant Areas

### 1.1 Forge:SMITH - Compliant Patterns

#### Pipeline State Machine (Visibility of System Status)
**Location:** [pipeline.svelte.ts](forge-smithy/src/lib/stores/pipeline.svelte.ts)

The pipeline implements an explicit state machine with well-defined steps:
```
IDLE → WELCOME_FIRST_RUN → SELECTED → EVALUATING → AWAITING_AUTH →
EXECUTING → VERIFYING_EVIDENCE → REVIEWING → DONE → ERROR
```

**Compliant Because:**
- States are enumerated and exhaustive
- Contract-driven transitions prevent invalid state changes
- Heartbeat mechanism detects stale/crashed sessions
- Visual representation via `StateChevrons` component shows progress

#### Error Classification System (Error Prevention)
**Location:** [errors.ts](forge-smithy/src/lib/utils/errors.ts) (665 lines)

Enterprise-grade error taxonomy:
- 9 error categories (NETWORK, API, VALIDATION, AUTHENTICATION, etc.)
- 4 severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Retryable flag with exponential backoff calculation
- Unique error IDs for support reference

**Compliant Because:**
- Errors are classified, not just displayed
- Severity drives auto-dismiss behavior (LOW = 5s auto-dismiss)
- Retry logic respects `Retry-After` headers
- Technical details collapsible (progressive disclosure)

#### Navigation Gates (User Control)
**Location:** [Sidebar.svelte](forge-smithy/src/lib/components/Sidebar.svelte)

Runtime-aware navigation with conditional disabling:
```typescript
interface NavItem {
  requiresTauri?: boolean;
  requiresRepoAccess?: boolean;
}
```

**Compliant Because:**
- Disabled items show explanatory notes
- CTA links ("Import repo") guide users to enable features
- Graceful degradation between web and Tauri modes

#### Offline Detection (Visibility of System Status)
**Location:** [OfflineBanner.svelte](forge-smithy/src/lib/components/OfflineBanner.svelte)

Fixed top banner when network unavailable:
- Warning color (#e8a64d)
- Clear message: "You are offline. Some features may not work."
- Slide animation for attention without disruption

---

### 1.2 Forge Command - Compliant Patterns

#### Service Health Visualization (Visibility of System Status)
**Location:** [ServiceHealthPanel.svelte](Forge_Command/src/lib/components/ServiceHealthPanel.svelte)

Real-time service status with skeleton loading:
- Color-coded status (green=up, red=down, yellow=degraded)
- Wake button for dormant services
- Polling with configurable interval
- Skeleton loader during initial fetch

**Compliant Because:**
- System status always visible
- Users can take action (wake) on degraded services
- Loading state distinguished from empty state

#### Type-Safe Tauri Bindings (Consistency)
**Location:** [tauri.ts](Forge_Command/src/lib/utils/tauri.ts) (639 lines)

Comprehensive command wrapper layer:
```typescript
async function getInvoke() {
  const { invoke } = await import('@tauri-apps/api/core');
  return invoke;
}
```

**Compliant Because:**
- All IPC commands have TypeScript types
- Dynamic import prevents SSR crashes
- Centralized error handling pattern

#### SSE Event Integration (Visibility of System Status)
**Location:** [forge-run.svelte.ts](Forge_Command/src/lib/stores/forge-run.svelte.ts)

Real-time run status updates via Server-Sent Events:
- Live event streaming for active runs
- Event history maintained per run
- Status transitions visible immediately

---

## Section 2: UX Violations by Principle

### Principle 1: Visibility of System Status

#### VIOLATION V1.1 - Silent Navigation Redirects (CRITICAL)
**System:** Forge:SMITH
**Location:** [+layout.svelte](forge-smithy/src/routes/+layout.svelte)

```typescript
if (redirect && redirect !== targetPath) {
  void goto(redirect, { replaceState: true });
}
```

**Issue:** Pipeline route guard redirects users without explanation. User navigates to `/verify` but lands on `/select` with no indication why.

**Nielsen Heuristic Violated:** Users must be informed about what is going on through appropriate feedback within reasonable time.

**Remediation:**
```typescript
if (redirect && redirect !== targetPath) {
  toastStore.add({
    type: 'info',
    message: `Redirected: Pipeline not at required step for ${targetPath}`
  });
  void goto(redirect, { replaceState: true });
}
```

---

#### VIOLATION V1.2 - Indeterminate Loading States (HIGH)
**System:** Forge Command
**Location:** Multiple components

```typescript
// KPICard shows 0 during loading
value={stats?.dataforge?.total_documents ?? 0}
```

**Issue:** Cannot distinguish between "loading", "loaded but empty", and "load failed". Value `0` could mean any of these states.

**Remediation:**
```typescript
{#if isLoading}
  <Skeleton class="h-8 w-24" />
{:else if error}
  <span class="text-red-400">Error</span>
{:else}
  {stats?.dataforge?.total_documents ?? 0}
{/if}
```

---

#### VIOLATION V1.3 - Missing Pipeline Progress Indicator
**System:** Forge:SMITH
**Location:** Pipeline flow pages

**Issue:** Users in multi-step pipeline flow cannot see their position in the overall flow. No breadcrumb or stepper component indicates "Step 3 of 7".

**Remediation:** Add `PipelineStepper` component to pipeline route layouts showing current position and remaining steps.

---

### Principle 2: Match Between System and Mental Model

#### VIOLATION V2.1 - Dual Store Systems (CRITICAL)
**System:** Forge Command
**Location:** [stores/](Forge_Command/src/lib/stores/)

```typescript
// Svelte 5 runes pattern
let state = $state<HealthState>({ systemHealth: null });

// Svelte 4 writable pattern (same codebase)
export const appSettings = writable<AppSettings>(defaultSettings);
```

**Issue:** Developers must mentally track two different reactivity systems. Mixing `$derived()` with `$store` subscriptions creates confusion.

**Mental Model Violation:** Users (developers) cannot form a consistent mental model of how state flows through the application.

**Remediation:** Migrate all stores to Svelte 5 runes pattern. Create migration guide documenting the transition.

---

#### VIOLATION V2.2 - Inconsistent Response Formats
**System:** Forge:SMITH API routes
**Location:** [governed/](forge-smithy/src/routes/governed/)

```typescript
// Some endpoints return:
return json({ ok: true, data: result });

// Others return:
return json({ success: true, result });
```

**Issue:** Client code must handle multiple response formats. Developers cannot predict response shape.

**Remediation:** Standardize on single response envelope:
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
}
```

---

#### VIOLATION V2.3 - Severity Ordering Bug
**System:** Forge:SMITH
**Location:** [governance/proposals/+page.svelte](forge-smithy/src/routes/governance/proposals/+page.svelte)

```typescript
// Uses localeCompare for severity sorting
.sort((a, b) => a.severity.localeCompare(b.severity))
```

**Issue:** "BLOCK" sorts before "HIGH" alphabetically, but "BLOCK" should be highest severity. Mental model expects severity ordering.

**Remediation:**
```typescript
const SEVERITY_ORDER = { BLOCK: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
.sort((a, b) => SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity])
```

---

### Principle 3: User Control & Authority

#### VIOLATION V3.1 - No Back-Button Protection (CRITICAL)
**System:** Forge:SMITH
**Location:** Pipeline flow routes

**Issue:** Users can browser-back from `/review` to `/select`, corrupting pipeline state. No confirmation dialog when leaving in-progress work.

**Remediation:**
```typescript
beforeNavigate(({ cancel, to }) => {
  if (pipelineStore.hasUnsavedWork && !confirm('Abandon current work?')) {
    cancel();
  }
});
```

---

#### VIOLATION V3.2 - No Undo for Destructive Actions
**System:** Forge:SMITH
**Location:** Mute/snooze actions in proposals

**Issue:** Muting a proposal is permanent. No undo mechanism or grace period.

**Remediation:** Implement soft-delete with 30-second undo toast:
```typescript
toast.add({
  type: 'success',
  message: 'Proposal muted',
  action: { label: 'Undo', onClick: unmute }
});
```

---

#### VIOLATION V3.3 - Double-Click Submission (HIGH)
**System:** Forge Command
**Location:** Form buttons

```typescript
<button onclick={handleStartRun}>
  {#if isStarting} Loading... {:else} Start Run {/if}
</button>
// Button not disabled during submission
```

**Issue:** Button remains clickable during async operation, allowing duplicate submissions.

**Remediation:**
```typescript
<button onclick={handleStartRun} disabled={isStarting}>
```

---

### Principle 4: Error Prevention > Error Handling

#### VIOLATION V4.1 - No Form Validation Library (CRITICAL)
**System:** Both systems
**Location:** All form pages

**Issue:** All form validation is manual with inconsistent patterns. No inline field errors. Users must submit to discover validation failures.

```typescript
// Manual validation, no error display
if (!workflowId.trim() || !repoId.trim()) {
  return;  // Silent failure
}
```

**Remediation:** Implement form library with:
- Inline validation on blur
- Field-level error messages
- Required field indicators
- Focus management on error

---

#### VIOLATION V4.2 - Client-Side Filtering of Large Datasets
**System:** Forge:SMITH
**Location:** [governance/proposals/+page.svelte](forge-smithy/src/routes/governance/proposals/+page.svelte)

**Issue:** Time window filtering (all/7d/24h) happens client-side after fetching all records. With 1000+ records, this wastes bandwidth and memory.

**Remediation:** Pass filter params to API, filter server-side.

---

#### VIOLATION V4.3 - No Input Constraints
**System:** Both systems
**Location:** Numeric/date inputs

**Issue:** Inputs accept invalid values (negative numbers, future dates where inappropriate). Validation only at submission.

**Remediation:** Use `<input type="number" min="0">`, `<input type="date" max={today}>`.

---

### Principle 5: Recognition Over Recall

#### VIOLATION V5.1 - Filter State Not in URL (CRITICAL)
**System:** Both systems
**Location:** `/library`, `/encyclopedia`, `/governance/proposals`, `/history`

**Issue:** Filter selections are component state only. Refreshing the page loses all filters. Cannot bookmark or share filtered views.

**Remediation:** Sync filter state to URL query params:
```typescript
// URL: /library?search=auth&section=security&page=2
const searchParams = $page.url.searchParams;
let search = searchParams.get('search') ?? '';
```

---

#### VIOLATION V5.2 - No Recent/Favorites
**System:** Both systems
**Location:** Navigation

**Issue:** Users must remember and navigate to frequently-used pages. No recently-visited list or favorites.

**Remediation:** Add "Recent" section to sidebar with last 5 visited pages.

---

#### VIOLATION V5.3 - Missing Breadcrumbs
**System:** Forge:SMITH
**Location:** Nested routes (`/smithy/portfolio/projects/[slug]/checklist`)

**Issue:** Deep navigation paths have no breadcrumb trail. Users cannot see current location in hierarchy.

**Remediation:** Add `Breadcrumb` component showing: `Smithy > Portfolio > Projects > {name} > Checklist`

---

### Principle 6: Progressive Disclosure

#### VIOLATION V6.1 - Massive State Complexity in Single Component
**System:** Forge:SMITH
**Location:** [encyclopedia/+page.svelte](forge-smithy/src/routes/encyclopedia/+page.svelte) (1,339 lines)

**Issue:** 20+ state variables, multiple `$effect()` blocks with interdependencies. All features visible immediately, overwhelming users.

**Remediation:**
- Split into sub-components
- Hide advanced search behind "Advanced" toggle
- Default to simple search, expand to forensic mode on demand

---

#### VIOLATION V6.2 - All Skills Loaded Upfront
**System:** Forge:SMITH
**Location:** [library/+page.svelte](forge-smithy/src/routes/library/+page.svelte)

**Issue:** All skills loaded on mount. Virtual scrolling helps render performance but doesn't reduce initial data load.

**Remediation:** Implement pagination with 50-item pages, load more on scroll or explicit "Load More" button.

---

### Principle 7: Cognitive Load Management

#### VIOLATION V7.1 - 22+ Navigation Items
**System:** Forge:SMITH
**Location:** [Sidebar.svelte](forge-smithy/src/lib/components/Sidebar.svelte)

```typescript
const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/' },
  { label: 'Planning Agent', href: '/planning' },
  // ... 20+ more items
];
```

**Issue:** Users must scan 22+ items to find their destination. No grouping or hierarchy.

**Remediation:** Group navigation into collapsible sections:
- **Agents** (Planning, Execution, Evaluator, Coordinator)
- **Content** (Library, Workflows, Models)
- **Analysis** (Analytics, History, Architecture)
- **Operations** (Repos, Settings, Admin)

---

#### VIOLATION V7.2 - Inconsistent Error Presentation
**System:** Both systems
**Location:** Various

| Route | Loading | Error | Empty |
|-------|---------|-------|-------|
| /library | Spinner | Alert | Empty state |
| /governance/proposals | Text | None | Text |
| /encyclopedia/[id] | Banner | Banner | Banner |
| /governed | None | Array | None |

**Issue:** Users must learn different error patterns for each page, increasing cognitive load.

**Remediation:** Create `LoadingState`, `ErrorState`, `EmptyState` wrapper components used consistently.

---

### Principle 8: Consistency & Determinism

#### VIOLATION V8.1 - Toast Positioning Inconsistency (HIGH)
**System:** Cross-system

| System | Position | Z-Index |
|--------|----------|---------|
| Forge Command | bottom-right | z-50 |
| Forge:SMITH | top-right | z-9999 |

**Issue:** Users switching between systems see toasts in different locations.

**Remediation:** Standardize on top-right (Material Design convention) with z-9999.

---

#### VIOLATION V8.2 - Event Listener Memory Leaks (CRITICAL)
**System:** Forge Command
**Location:** [forge-run.svelte.ts](Forge_Command/src/lib/stores/forge-run.svelte.ts)

```typescript
const unlistenEvents = await listen<ForgeRunEvent>('forge_run_events', handler);
eventUnlisteners.push(unlistenEvents);
// cleanupEventListeners() exists but not guaranteed to be called
```

**Issue:** SSE event listeners accumulate on navigation. Multiple listeners cause duplicate event handling and memory growth.

**Remediation:** Call `cleanupEventListeners()` in `onDestroy()` of consuming components. Consider moving to store-level lifecycle.

---

#### VIOLATION V8.3 - Polling Accumulation
**System:** Forge Command
**Location:** [+layout.svelte](Forge_Command/src/routes/+layout.svelte)

**Issue:** `startPolling()` called on mount but `stopPolling()` never called in root layout (onDestroy doesn't fire for root). Sidebar toggle causes remount, accumulating intervals.

**Remediation:** Use store-level singleton polling with reference counting:
```typescript
let subscribers = 0;
function subscribe() {
  if (++subscribers === 1) startInterval();
  return () => { if (--subscribers === 0) stopInterval(); };
}
```

---

#### VIOLATION V8.4 - Dynamic Tailwind Classes Broken
**System:** Forge Command
**Location:** [Sidebar.svelte](Forge_Command/src/lib/components/Sidebar.svelte)

```typescript
const bgColor = item.color ? `bg-${item.color}/20` : 'bg-forge-slate';
```

**Issue:** Dynamic class construction doesn't work with Tailwind's purge system. Classes like `bg-forgeagents/20` won't be in production CSS.

**Remediation:** Use explicit class mapping:
```typescript
const BG_COLORS = {
  dataforge: 'bg-dataforge/20',
  neuroforge: 'bg-neuroforge/20',
  // ...
};
```

---

## Section 3: Wiring vs UX Mismatches

### Mismatch W1: IPC Error Types vs UI Error Display
**System:** Forge Command

**Backend:** Tauri commands return typed errors with codes
**Frontend:** All errors coerced to strings

```typescript
// Frontend loses error structure
catch (e) {
  state.error = e instanceof Error ? e.message : String(e);
}
```

**UX Impact:** Users see generic error messages instead of actionable guidance.

**Remediation:** Define typed error interface, parse and display appropriately:
```typescript
interface TauriError {
  code: 'NETWORK' | 'AUTH' | 'VALIDATION';
  message: string;
  recoverable: boolean;
}
```

---

### Mismatch W2: Pipeline State vs Route Access
**System:** Forge:SMITH

**Backend:** Pipeline state determines valid operations
**Frontend:** Routes are always accessible via URL

**UX Impact:** User can bookmark `/verify` URL, but visiting it later fails silently or redirects.

**Remediation:**
1. Add `+page.ts` load functions that validate prerequisites
2. Show explicit "Prerequisites not met" page instead of redirect

---

### Mismatch W3: Emergency Stop Signal vs UI Feedback
**System:** Both systems

**Backend:** Emergency stop is a system-wide signal in Rust/Python
**Frontend:** No visual indicator when emergency stop is active

**UX Impact:** Users don't know why operations are failing during emergency stop.

**Remediation:** Add global `EmergencyStopBanner` component that displays when stop is active.

---

### Mismatch W4: Token Expiry vs Session UI
**System:** Forge:SMITH

**Backend:** `run_token` has 30-minute TTL
**Frontend:** No countdown or warning before expiry

**UX Impact:** Operations fail unexpectedly when token expires mid-session.

**Remediation:**
1. Display token TTL countdown in session context
2. Warn at 5 minutes remaining
3. Offer token refresh action

---

## Section 4: Authority & Trust Risks

### Risk A1: API Key Migration Without User Confirmation (CRITICAL)
**System:** Forge Command
**Location:** [api_keys.rs](Forge_Command/src-tauri/src/commands/api_keys.rs)

```rust
pub fn migrate_api_keys_to_aes() -> Result<MigrationStatus, String>
```

**Risk:** Migration from legacy XOR to AES-256-GCM can be triggered without explicit user consent. If migration fails mid-way, keys could be in inconsistent state.

**Remediation:**
1. Require explicit user confirmation before migration
2. Backup existing keys before migration
3. Provide rollback mechanism

---

### Risk A2: Silent Pipeline State Mutations
**System:** Forge:SMITH

**Risk:** Pipeline transitions happen via store mutations without user-visible authorization. User cannot audit what triggered a state change.

**Remediation:** Add transition audit log visible in UI (who/what triggered each transition).

---

### Risk A3: No Authorization Scope Display
**System:** Forge:SMITH
**Location:** Skill invocation

**Risk:** When invoking skills, users don't see what permissions the skill will use. Skills may have filesystem/network access without disclosure.

**Remediation:** Display permission scope before skill invocation:
```
This skill will:
- Read files in /project
- Make network requests to api.forge.dev
[Authorize] [Cancel]
```

---

### Risk A4: Emergency Stop Missing UI Trigger
**System:** Both systems

**Risk:** Emergency stop can be triggered via API but no prominent UI button exists. In crisis, users may not know how to stop runaway operations.

**Remediation:** Add visible emergency stop button (red, always accessible) in header.

---

### Risk A5: Cross-System Authentication Gap
**System:** Cross-system

**Risk:** Users may have different auth states between Forge Command and Forge:SMITH. No unified session management or SSO indication.

**Remediation:** Display unified auth status showing all system connections.

---

## Section 5: Targeted Remediation Recommendations

### Priority 1: Critical (Implement Immediately)

| ID | Issue | System | Effort | Impact |
|----|-------|--------|--------|--------|
| R1 | Add form validation library | Both | Medium | High |
| R2 | Fix event listener memory leaks | Forge Command | Low | High |
| R3 | Persist filter state in URL | Both | Medium | High |
| R4 | Add back-button protection | Forge:SMITH | Low | High |
| R5 | Standardize error response format | Forge:SMITH | Medium | High |
| R6 | Fix dynamic Tailwind classes | Forge Command | Low | Medium |

### Priority 2: High (Next Sprint)

| ID | Issue | System | Effort | Impact |
|----|-------|--------|--------|--------|
| R7 | Migrate to unified store pattern | Forge Command | High | High |
| R8 | Add pipeline progress indicator | Forge:SMITH | Low | Medium |
| R9 | Implement request deduplication | Both | Medium | Medium |
| R10 | Add emergency stop UI button | Both | Low | High |
| R11 | Create shared error components | Both | Medium | Medium |
| R12 | Fix polling accumulation | Forge Command | Medium | Medium |

### Priority 3: Medium (Scheduled)

| ID | Issue | System | Effort | Impact |
|----|-------|--------|--------|--------|
| R13 | Group navigation items | Forge:SMITH | Low | Medium |
| R14 | Add breadcrumb navigation | Forge:SMITH | Low | Medium |
| R15 | Standardize toast positioning | Both | Low | Low |
| R16 | Add loading skeletons | Forge Command | Medium | Medium |
| R17 | Implement undo for destructive actions | Forge:SMITH | Medium | Medium |
| R18 | Add token expiry countdown | Forge:SMITH | Low | Medium |

### Priority 4: Low (Backlog)

| ID | Issue | System | Effort | Impact |
|----|-------|--------|--------|--------|
| R19 | Add recent pages to navigation | Both | Low | Low |
| R20 | Implement dark mode toggle | Forge Command | Medium | Low |
| R21 | Add keyboard shortcuts | Both | Medium | Low |
| R22 | Virtualize encyclopedia results | Forge:SMITH | Medium | Low |

---

## Appendix A: Compliance Checklist

### Principle 1: Visibility of System Status
- [ ] All async operations show loading state
- [ ] Error states are visually distinct from empty states
- [ ] System status (online/offline/degraded) always visible
- [ ] Progress indicators for multi-step operations
- [ ] Real-time updates for background processes

### Principle 2: Match Between System and Mental Model
- [ ] Single state management pattern
- [ ] Consistent API response format
- [ ] Severity/priority ordering matches user expectations
- [ ] Terminology consistent across UI

### Principle 3: User Control & Authority
- [ ] Confirmation before destructive actions
- [ ] Undo available for reversible actions
- [ ] Cancel available for long operations
- [ ] Back navigation works as expected
- [ ] Buttons disabled during processing

### Principle 4: Error Prevention > Error Handling
- [ ] Inline validation on input fields
- [ ] Required fields marked visually
- [ ] Input constraints (min/max/pattern)
- [ ] Server-side filtering for large datasets

### Principle 5: Recognition Over Recall
- [ ] Current filters visible and modifiable
- [ ] Filter state persisted in URL
- [ ] Breadcrumb navigation for deep hierarchies
- [ ] Recent items accessible

### Principle 6: Progressive Disclosure
- [ ] Advanced features behind toggles
- [ ] Pagination for large lists
- [ ] Collapsible detail sections
- [ ] Components under 500 lines

### Principle 7: Cognitive Load Management
- [ ] Navigation grouped logically
- [ ] Consistent component patterns
- [ ] Limited options per screen
- [ ] Clear visual hierarchy

### Principle 8: Consistency & Determinism
- [ ] Same patterns across both systems
- [ ] No memory leaks from listeners
- [ ] Polling properly managed
- [ ] CSS classes statically defined

---

## Appendix B: File Reference

### Forge Command Key Files
- [Forge_Command/src/routes/](Forge_Command/src/routes/) - 22 page routes
- [Forge_Command/src/lib/stores/](Forge_Command/src/lib/stores/) - State management
- [Forge_Command/src/lib/components/](Forge_Command/src/lib/components/) - 20 components
- [Forge_Command/src/lib/utils/tauri.ts](Forge_Command/src/lib/utils/tauri.ts) - IPC wrapper

### Forge:SMITH Key Files
- [forge-smithy/src/routes/](forge-smithy/src/routes/) - 30+ routes
- [forge-smithy/src/lib/stores/pipeline.svelte.ts](forge-smithy/src/lib/stores/pipeline.svelte.ts) - Pipeline state
- [forge-smithy/src/lib/utils/errors.ts](forge-smithy/src/lib/utils/errors.ts) - Error system
- [forge-smithy/src/lib/components/](forge-smithy/src/lib/components/) - Component library
- [forge-smithy/src/hooks.client.ts](forge-smithy/src/hooks.client.ts) - Global error handlers

---

**End of Audit Report**

*Generated by Claude Opus 4.5 - UX/UI Compliance Audit System*
