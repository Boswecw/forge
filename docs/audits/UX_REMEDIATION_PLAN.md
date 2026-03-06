# UX/UI Remediation Implementation Plan

**Based on:** UX_UI_AUDIT_REPORT.md
**Created:** 2026-01-29
**Status:** In Progress

---

## Phase 1: Critical Fixes (Immediate)

### R1: Form Validation Library
**Systems:** Both
**Effort:** Medium | **Impact:** High

**Implementation:**
1. Create shared form validation utilities in `forge-smithy/src/lib/utils/validation.ts`
2. Build form components: `FormField`, `FormError`, `FormGroup`
3. Implement validation rules: required, email, minLength, maxLength, pattern, custom
4. Add inline validation on blur
5. Add focus management (focus first invalid field on submit)
6. Port to Forge Command or create shared package

**Files to Create/Modify:**
- `forge-smithy/src/lib/utils/validation.ts` (new)
- `forge-smithy/src/lib/components/form/FormField.svelte` (new)
- `forge-smithy/src/lib/components/form/FormError.svelte` (new)
- `forge-smithy/src/lib/components/form/FormGroup.svelte` (new)
- `forge-smithy/src/lib/components/form/index.ts` (new)

---

### R2: Fix Event Listener Memory Leaks
**System:** Forge Command
**Effort:** Low | **Impact:** High

**Implementation:**
1. Add `onDestroy` cleanup to all components using `forge-run.svelte.ts`
2. Create store-level lifecycle management with subscriber counting
3. Ensure `cleanupEventListeners()` called on component unmount

**Files to Modify:**
- `Forge_Command/src/lib/stores/forge-run.svelte.ts`
- `Forge_Command/src/routes/orchestrator/+page.svelte`
- `Forge_Command/src/routes/history/+page.svelte`

**Code Pattern:**
```typescript
// In store
let subscriberCount = 0;
export function subscribe() {
  if (++subscriberCount === 1) initEventListeners();
  return () => {
    if (--subscriberCount === 0) cleanupEventListeners();
  };
}

// In component
onDestroy(() => forgeRunStore.cleanup());
```

---

### R3: Persist Filter State in URL
**Systems:** Both
**Effort:** Medium | **Impact:** High

**Implementation:**
1. Create `useUrlState` utility hook for syncing state with URL params
2. Update `/library` to use URL params for search, section, category
3. Update `/encyclopedia` to use URL params for query, mode, status
4. Update `/governance/proposals` to use URL params for filters
5. Update Forge Command `/history` to use URL params

**Files to Create/Modify:**
- `forge-smithy/src/lib/utils/urlState.ts` (new)
- `forge-smithy/src/routes/library/+page.svelte`
- `forge-smithy/src/routes/encyclopedia/+page.svelte`
- `forge-smithy/src/routes/governance/proposals/+page.svelte`
- `Forge_Command/src/routes/history/+page.svelte`

**Code Pattern:**
```typescript
import { page } from '$app/stores';
import { goto } from '$app/navigation';

function updateUrlParam(key: string, value: string | null) {
  const url = new URL($page.url);
  if (value) url.searchParams.set(key, value);
  else url.searchParams.delete(key);
  goto(url, { replaceState: true, noScroll: true });
}

// Initialize from URL
let search = $page.url.searchParams.get('search') ?? '';
```

---

### R4: Add Back-Button Protection
**System:** Forge:SMITH
**Effort:** Low | **Impact:** High

**Implementation:**
1. Add `beforeNavigate` guard in pipeline routes
2. Check for unsaved work or in-progress operations
3. Show confirmation dialog before allowing navigation away
4. Track "dirty" state in pipeline store

**Files to Modify:**
- `forge-smithy/src/lib/stores/pipeline.svelte.ts` (add hasPendingWork getter)
- `forge-smithy/src/routes/+layout.svelte` (add beforeNavigate with confirm)

**Code Pattern:**
```typescript
import { beforeNavigate } from '$app/navigation';

beforeNavigate(({ cancel, to, from }) => {
  if (pipelineStore.hasPendingWork) {
    const confirmed = confirm('You have unsaved work. Leave anyway?');
    if (!confirmed) cancel();
  }
});
```

---

### R5: Standardize API Response Format
**System:** Forge:SMITH
**Effort:** Medium | **Impact:** High

**Implementation:**
1. Define canonical `ApiResponse<T>` type
2. Create response helper functions: `successResponse()`, `errorResponse()`
3. Update all server routes to use standard format
4. Update client code to expect standard format

**Files to Create/Modify:**
- `forge-smithy/src/lib/types/api.ts` (new)
- `forge-smithy/src/routes/governed/*/+server.ts` (all)
- `forge-smithy/src/routes/api/smithy/*/+server.ts` (all)

**Type Definition:**
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    timestamp: string;
    requestId?: string;
  };
}
```

---

### R6: Fix Dynamic Tailwind Classes
**System:** Forge Command
**Effort:** Low | **Impact:** Medium

**Implementation:**
1. Replace dynamic class construction with explicit class mapping
2. Add safelist to tailwind.config.js if dynamic classes still needed
3. Audit all components for dynamic class patterns

**Files to Modify:**
- `Forge_Command/src/lib/components/Sidebar.svelte`
- `Forge_Command/tailwind.config.js` (if needed)

**Code Pattern:**
```typescript
// BEFORE (broken)
const bgColor = `bg-${item.color}/20`;

// AFTER (working)
const BG_COLORS: Record<string, string> = {
  dataforge: 'bg-dataforge/20',
  neuroforge: 'bg-neuroforge/20',
  rake: 'bg-rake/20',
  forgeagents: 'bg-forgeagents/20',
};
const bgColor = BG_COLORS[item.color] ?? 'bg-forge-slate';
```

---

## Phase 2: High Priority (Next Sprint)

### R7: Migrate to Unified Store Pattern
**System:** Forge Command
**Effort:** High | **Impact:** High

**Implementation:**
1. Audit all stores for pattern (runes vs writable)
2. Create migration guide
3. Convert writable stores to runes pattern one at a time
4. Update all consuming components

**Files to Migrate:**
- `Forge_Command/src/lib/stores/telemetry.ts` → runes
- `Forge_Command/src/lib/stores/settings.ts` → runes
- `Forge_Command/src/lib/stores/toast.ts` → runes

---

### R8: Add Pipeline Progress Indicator
**System:** Forge:SMITH
**Effort:** Low | **Impact:** Medium

**Implementation:**
1. Create `PipelineStepper` component showing steps
2. Add to pipeline route layouts
3. Highlight current step, show completed/pending

**Files to Create:**
- `forge-smithy/src/lib/components/pipeline/PipelineStepper.svelte`

---

### R9: Implement Request Deduplication
**Systems:** Both
**Effort:** Medium | **Impact:** Medium

**Implementation:**
1. Create request cache with TTL
2. Deduplicate identical requests within 1s window
3. Add to Tauri command wrapper

---

### R10: Add Emergency Stop UI Button
**Systems:** Both
**Effort:** Low | **Impact:** High

**Implementation:**
1. Add prominent red button in header
2. Wire to emergency stop API
3. Show confirmation before triggering
4. Display banner when active

**Files to Create/Modify:**
- `forge-smithy/src/lib/components/EmergencyStopButton.svelte` (new)
- `forge-smithy/src/routes/+layout.svelte`
- `Forge_Command/src/lib/components/EmergencyStopButton.svelte` (new)
- `Forge_Command/src/routes/+layout.svelte`

---

### R11: Create Shared Error Components
**Systems:** Both
**Effort:** Medium | **Impact:** Medium

**Implementation:**
1. Create `LoadingState`, `ErrorState`, `EmptyState` components
2. Standardize usage across all pages
3. Port Forge:SMITH error system to Forge Command

---

### R12: Fix Polling Accumulation
**System:** Forge Command
**Effort:** Medium | **Impact:** Medium

**Implementation:**
1. Add reference counting to polling stores
2. Only start polling when first subscriber
3. Stop polling when last subscriber leaves
4. Prevent duplicate intervals

---

## Phase 3: Medium Priority (Scheduled)

### R13: Group Navigation Items
- Collapse 22+ items into logical groups
- Add collapsible sections

### R14: Add Breadcrumb Navigation
- Create `Breadcrumb` component
- Add to nested routes

### R15: Standardize Toast Positioning
- Align both systems to top-right
- Standardize z-index (9999)

### R16: Add Loading Skeletons
- Create skeleton components for Forge Command
- Replace spinners with contextual skeletons

### R17: Implement Undo for Destructive Actions
- Add 30-second undo window
- Show undo toast after destructive actions

### R18: Add Token Expiry Countdown
- Display TTL in session context
- Warn at 5 minutes remaining

---

## Phase 4: Low Priority (Backlog)

### R19: Add Recent Pages to Navigation
### R20: Implement Dark Mode Toggle
### R21: Add Keyboard Shortcuts
### R22: Virtualize Encyclopedia Results

---

## Implementation Order

```
Week 1: R1 (Form Validation) + R2 (Event Listeners) + R6 (Tailwind)
Week 2: R3 (URL State) + R4 (Back Button) + R10 (Emergency Stop)
Week 3: R5 (API Response) + R8 (Stepper) + R11 (Error Components)
Week 4: R7 (Store Migration) + R12 (Polling)
Week 5+: R9, R13-R22
```

---

## Success Criteria

- [ ] All forms have inline validation with error messages
- [ ] No memory leaks from event listeners
- [ ] Filter state survives page refresh
- [ ] Users warned before losing unsaved work
- [ ] Consistent API response format across all endpoints
- [ ] All Tailwind classes render correctly in production
- [ ] Emergency stop accessible from UI
- [ ] Unified store pattern in Forge Command
