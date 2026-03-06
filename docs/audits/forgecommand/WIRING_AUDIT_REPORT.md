# Forge_Command Wiring, Integration & Broken-Path Audit Report

**Date:** 2026-01-30
**Auditor:** Claude Opus 4.5
**Scope:** Complete frontend-to-backend IPC command mapping

---

## Executive Wiring Status

| Category | Count | Health |
|----------|-------|--------|
| Total Backend Commands | 84 | - |
| Frontend Wrappers | 70 | - |
| **Working Paths** | 61 | ✅ |
| **Broken Paths** | 4 | 🔴 CRITICAL |
| **Stub Commands** | 18 | ⚠️ MEDIUM |
| **Unused Backend Commands** | 19 | ℹ️ LOW |

**Overall System Health: 🟡 DEGRADED**

- 4 frontend functions call non-existent or misnamed backend commands
- 18 commands return "not implemented" errors but are wired
- 19 backend commands have no frontend consumer

---

## 1. Verified Working Paths

### Health & Monitoring (6/6 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getSystemHealth()` | `get_system_health` | `ecosystem.svelte.ts` | `+page.svelte`, `+layout.svelte` |
| `getServiceHealth()` | `get_service_health` | `healthStore` | Service pages |
| `wakeAllServices()` | `wake_all_services` | `tauri.ts` | Wake buttons |

### Telemetry - Working (6/6 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getRecentEvents()` | `get_recent_events` | `telemetry.ts` | `/recent-events` |
| `getDataForgeMetrics()` | `get_dataforge_metrics` | `ecosystem.svelte.ts` | `/dataforge` |
| `getNeuroForgeMetrics()` | `get_neuroforge_metrics` | `ecosystem.svelte.ts` | `/neuroforge` |
| `getForgeAgentsMetrics()` | `get_forgeagents_metrics` | `telemetry.ts` | `/forgeagents` |

### Local Telemetry Collector (7/7 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `telemetryIngestBatch()` | `telemetry_ingest_batch` | - | SDK internal |
| `telemetryIngestSpan()` | `telemetry_ingest_span` | - | SDK internal |
| `getTelemetryHealth()` | `telemetry_health` | `telemetry.ts` | `/telemetry` |
| `listLocalTraces()` | `telemetry_list_traces` | `telemetry.ts` | `/telemetry` |
| `getLocalTraceDetail()` | `telemetry_get_trace` | `telemetry.ts` | `/telemetry` |
| `getTelemetryStats()` | `telemetry_stats` | `telemetry.ts` | `/telemetry` |
| `clearTelemetry()` | `telemetry_clear` | `telemetry.ts` | `/telemetry` |

### API Keys (5/5 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getApiKeys()` | `list_api_keys` | `settings.ts` | `/forge-keys` |
| `saveApiKey()` | `store_api_key` | `settings.ts` | `/forge-keys` |
| `updateApiKey()` | `update_api_key` | `settings.ts` | `/forge-keys` |
| `deleteApiKey()` | `delete_api_key` | `settings.ts` | `/forge-keys` |

### Cost Tracking (7/7 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getCostSummary()` | `get_cost_summary` | `ecosystem.svelte.ts` | `/costs`, `+page.svelte` |
| `getBudgetStatus()` | `check_budget_status` | `tauri.ts` | `/costs` |
| `getRateCards()` | `get_rate_cards` | `tauri.ts` | `/costs` |
| `saveRateCard()` | `save_rate_card` | `tauri.ts` | `/costs` |
| `getBudgetThresholds()` | `get_budget_thresholds` | `tauri.ts` | `/costs` |
| `saveBudgetThreshold()` | `save_budget_threshold` | `tauri.ts` | `/costs` |
| `deleteBudgetThreshold()` | `delete_budget_threshold` | `tauri.ts` | `/costs` |

### Provider Health (3/3 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getProviderHealth()` | `get_provider_health` | `tauri.ts` | `/providers` |
| `getSingleProviderHealth()` | `get_single_provider_health` | `tauri.ts` | `/providers` |
| `getProviderStats()` | `get_provider_stats` | `tauri.ts` | `/providers` |

### Wake Tracking (3/3 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getWakeStatus()` | `get_wake_status` | `tauri.ts` | Dashboard |
| `getWakeStats()` | `get_wake_stats` | `tauri.ts` | Dashboard |
| `getWakeHistory()` | `get_wake_history` | `tauri.ts` | Dashboard |

### Distributed Tracing (3/3 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `listTraces()` | `list_traces` | `tauri.ts` | `/tracing` |
| `getTraceDetail()` | `get_trace_detail` | `tauri.ts` | `/tracing` |
| `refreshTraceViews()` | `refresh_trace_views` | `tauri.ts` | `/tracing` |

### Data Lineage (2/2 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `getLineageGraph()` | `get_lineage_graph` | `tauri.ts` | `/lineage` |
| `getLineageStats()` | `get_lineage_stats` | `tauri.ts` | `/lineage` |

### Operational Control (2/2 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `executeOperation()` | `execute_operation` | `tauri.ts` | `/operations` |
| `getAuditLog()` | `get_audit_log` | `tauri.ts` | `/operations` |

### AI Insights (6/6 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `queryInsights()` | `query_insights` | `tauri.ts` | `/insights` |
| `listAnomalies()` | `list_anomalies` | `tauri.ts` | `/insights/anomalies` |
| `detectAnomaliesNow()` | `detect_anomalies_now` | `tauri.ts` | `/insights/anomalies` |
| `acknowledgeAnomaly()` | `acknowledge_anomaly` | `tauri.ts` | `/insights/anomalies` |
| `getAnomalyStats()` | `get_anomaly_stats` | `tauri.ts` | `/insights/anomalies` |
| `getInsightHistory()` | `get_insight_history` | `tauri.ts` | `/insights` |

### ForgeAgents Run Execution (8/8 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `forgeRunStart()` | `forge_run_start` | `forgeRunStore` | `/orchestrator` |
| `forgeRunSubscribe()` | `forge_run_subscribe` | `forgeRunStore` | `/orchestrator` |
| `forgeRunUnsubscribe()` | `forge_run_unsubscribe` | `forgeRunStore` | `/orchestrator` |
| `forgeRunCancel()` | `forge_run_cancel` | `forgeRunStore` | `/orchestrator` |
| `forgeRunHistory()` | `forge_run_history` | `forgeRunStore` | `/history` |
| `forgeRunGet()` | `forge_run_get` | `forgeRunStore` | `/history` |
| `forgeRunGetEvidence()` | `forge_run_get_evidence` | `forgeRunStore` | `/history` |
| `forgeRunVerifyEvidence()` | `forge_run_verify_evidence` | `forgeRunStore` | `/history` |

### Parity Sentinel (2/2 ✅)
| Frontend Wrapper | Backend Command | Store | Route(s) |
|------------------|-----------------|-------|----------|
| `checkVocabParity()` | `check_vocab_parity` | `tauri.ts` | ParitySentinel component |
| `getParityStatus()` | `get_parity_status` | `tauri.ts` | `/orchestrator` |

---

## 2. Broken Paths 🔴

### BP-001: `get_time_series` - Command Does Not Exist
| Severity | Location | Impact |
|----------|----------|--------|
| **CRITICAL** | [tauri.ts:101-108](src/lib/utils/tauri.ts#L101-L108) | Runtime error on invocation |

**Frontend calls:**
```typescript
export async function getTimeSeries(service: string, metric: string, hours?: number): Promise<TimeSeriesData> {
  const invoke = await getInvoke();
  return invoke('get_time_series', { service, metric, hours });
}
```

**Backend:** NO SUCH COMMAND REGISTERED

**Consumers:**
- `telemetry.ts:fetchTimeSeries()` (line 164-186)
- Any chart components requesting historical data

**Fix:** Either implement `get_time_series` backend command or remove frontend wrapper.

---

### BP-002: `get_bugcheck_history` - Command Does Not Exist
| Severity | Location | Impact |
|----------|----------|--------|
| **CRITICAL** | [tauri.ts:124-130](src/lib/utils/tauri.ts#L124-L130) | BugCheck history never loads |

**Frontend calls:**
```typescript
export async function getBugCheckHistory(limit?: number, target?: string): Promise<BugCheckRunSummary[]> {
  const invoke = await getInvoke();
  return invoke('get_bugcheck_history', { limit, target });
}
```

**Backend:** Has `get_bugcheck_result` but NOT `get_bugcheck_history`

**Fix:** Either:
- Add `get_bugcheck_history` command to backend
- Or rename frontend to use `get_bugcheck_result` (different semantics)

---

### BP-003: `get_services` - Command Name Mismatch
| Severity | Location | Impact |
|----------|----------|--------|
| **CRITICAL** | [tauri.ts:141-144](src/lib/utils/tauri.ts#L141-L144) | Service list fails to load |

**Frontend calls:**
```typescript
export async function getServices(): Promise<ServiceInfo[]> {
  const invoke = await getInvoke();
  return invoke('get_services');  // WRONG NAME
}
```

**Backend:** Command is registered as `list_services` (not `get_services`)

**Fix:** Change frontend to call `list_services`:
```typescript
return invoke('list_services');
```

---

### BP-004: `send_notification` - Command Name Mismatch
| Severity | Location | Impact |
|----------|----------|--------|
| **MEDIUM** | [tauri.ts:239-242](src/lib/utils/tauri.ts#L239-L242) | Notifications fail silently |

**Frontend calls:**
```typescript
export async function sendNotification(request: NotificationRequest): Promise<void> {
  const invoke = await getInvoke();
  return invoke('send_notification', { request });  // WRONG NAME
}
```

**Backend:** Command is registered as `send_test_notification`

**Fix:** Change frontend to call `send_test_notification`:
```typescript
return invoke('send_test_notification', { request });
```

---

## 3. Stub Commands (Not Implemented) ⚠️

These commands are wired frontend-to-backend but return "not implemented" errors:

### Alert Commands (6)
| Command | File | Status |
|---------|------|--------|
| `get_alert_config` | [alerts.rs:21](src-tauri/src/commands/alerts.rs#L21) | Returns `Err(NOT_IMPLEMENTED)` |
| `update_alert_config` | [alerts.rs:29](src-tauri/src/commands/alerts.rs#L29) | Returns `Err(NOT_IMPLEMENTED)` |
| `add_alert_rule` | [alerts.rs:37](src-tauri/src/commands/alerts.rs#L37) | Returns `Err(NOT_IMPLEMENTED)` |
| `delete_alert_rule` | [alerts.rs:45](src-tauri/src/commands/alerts.rs#L45) | Returns `Err(NOT_IMPLEMENTED)` |
| `get_alert_history` | [alerts.rs:53](src-tauri/src/commands/alerts.rs#L53) | Returns `Err(NOT_IMPLEMENTED)` |
| `acknowledge_alert` | [alerts.rs:61](src-tauri/src/commands/alerts.rs#L61) | Returns `Err(NOT_IMPLEMENTED)` |

**Impact:** `/alerts` page shows "Alert management not yet implemented" error

### Service Management Commands (5)
| Command | File | Status |
|---------|------|--------|
| `list_services` | [services.rs:16](src-tauri/src/commands/services.rs#L16) | Returns `Err(NOT_IMPLEMENTED)` |
| `start_service` | [services.rs:24](src-tauri/src/commands/services.rs#L24) | Returns `Err(NOT_IMPLEMENTED)` |
| `stop_service` | [services.rs:32](src-tauri/src/commands/services.rs#L32) | Returns `Err(NOT_IMPLEMENTED)` |
| `restart_service` | [services.rs:40](src-tauri/src/commands/services.rs#L40) | Returns `Err(NOT_IMPLEMENTED)` |
| `get_service_config` | [services.rs:48](src-tauri/src/commands/services.rs#L48) | Returns `Err(NOT_IMPLEMENTED)` |

**Impact:** Service management UI non-functional

### BugCheck Commands (4)
| Command | File | Status |
|---------|------|--------|
| `start_bugcheck` | [bugcheck.rs:16](src-tauri/src/commands/bugcheck.rs#L16) | Returns `Err(NOT_IMPLEMENTED)` |
| `get_bugcheck_status` | [bugcheck.rs:24](src-tauri/src/commands/bugcheck.rs#L24) | Returns `Err(NOT_IMPLEMENTED)` |
| `get_bugcheck_result` | [bugcheck.rs:32](src-tauri/src/commands/bugcheck.rs#L32) | Returns `Err(NOT_IMPLEMENTED)` |
| `cancel_bugcheck` | [bugcheck.rs:40](src-tauri/src/commands/bugcheck.rs#L40) | Returns `Err(NOT_IMPLEMENTED)` |

**Impact:** BugCheck integration pending (per CLAUDE.md roadmap)

### Notification Commands (3)
| Command | File | Status |
|---------|------|--------|
| `get_notification_settings` | notifications.rs | Returns `Err(NOT_IMPLEMENTED)` |
| `update_notification_settings` | notifications.rs | Returns `Err(NOT_IMPLEMENTED)` |
| `send_test_notification` | notifications.rs | Returns `Err(NOT_IMPLEMENTED)` |

**Impact:** Notification system non-functional

---

## 4. Declared-but-Unused Inventory

### Backend commands with no frontend consumer (19 total):

#### Health Module (3)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `ping_service` | Single service ping | Add to UI or remove |
| `get_orchestrator_status` | Python orchestrator health | Wire to status badge |
| `restart_orchestrator` | Restart Python orchestrator | Wire to admin panel |

#### Telemetry Module (2)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `query_telemetry` | Generic telemetry query | Evaluate need vs specific endpoints |
| `get_metrics_summary` | Aggregated metrics | Wire to dashboard |

#### BugCheck Module (1)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `get_bugcheck_result` | Get completed run result | Fix BP-002 (frontend calls wrong name) |

#### API Keys Module (1)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `test_api_key` | Validate key with provider | Wire to key management UI |

#### Services Module (1)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `get_service_config` | Get service config JSON | Wire when services implemented |

#### Notification Module (2)
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `get_notification_settings` | Get notification prefs | Wire to settings page |
| `update_notification_settings` | Update notification prefs | Wire to settings page |

#### Intent/SMITH Module (9) - ENTIRE MODULE UNUSED
| Command | Purpose | Recommendation |
|---------|---------|----------------|
| `intent_register` | Register typed RunIntent | Pending SMITH integration |
| `intent_register_raw` | Register raw JSON intent | Pending SMITH integration |
| `intent_accept` | Accept pending intent | Pending SMITH integration |
| `intent_get` | Get intent by ID | Pending SMITH integration |
| `intent_list` | List intents with filters | Pending SMITH integration |
| `intent_pending_count` | Count pending intents | Pending SMITH integration |
| `pipeline_get_session` | Get pipeline session | Pending SMITH integration |
| `pipeline_update_state` | Update pipeline state | Pending SMITH integration |
| `intent_cleanup` | Clean up expired intents | Pending SMITH integration |

**Note:** Intent commands are Phase 5 SMITH integration - unused by design currently.

---

## 5. Required Fix Plan

### Priority 1: Critical Path Fixes (Blocking)

| ID | Issue | Fix | File(s) |
|----|-------|-----|---------|
| **FIX-001** | `get_services` → `list_services` | Rename invoke call | `tauri.ts:143` |
| **FIX-002** | `send_notification` → `send_test_notification` | Rename invoke call | `tauri.ts:241` |
| **FIX-003** | `get_bugcheck_history` doesn't exist | Add backend command OR remove frontend | `tauri.ts:129` + `bugcheck.rs` |
| **FIX-004** | `get_time_series` doesn't exist | Add backend command OR remove frontend | `tauri.ts:107` + new `telemetry.rs` |

### Priority 2: Medium - Wiring Completion

| ID | Issue | Fix | File(s) |
|----|-------|-----|---------|
| **WIRE-001** | `test_api_key` unwired | Add "Test Key" button to API keys UI | `/forge-keys` route |
| **WIRE-002** | `get_orchestrator_status` unwired | Add orchestrator status badge | Layout header |
| **WIRE-003** | `restart_orchestrator` unwired | Add restart button to admin | `/orchestrator` route |
| **WIRE-004** | Notification settings unwired | Wire to `/settings` | Settings page |

### Priority 3: Low - Cleanup

| ID | Issue | Fix | File(s) |
|----|-------|-----|---------|
| **CLEAN-001** | `query_telemetry` unused | Evaluate removal or document use case | `telemetry.rs` |
| **CLEAN-002** | `get_metrics_summary` unused | Wire to dashboard or remove | `telemetry.rs` |
| **CLEAN-003** | `ping_service` unused | Wire or remove | `health.rs` |

### Priority 4: Future - Intent System

| ID | Issue | Fix | File(s) |
|----|-------|-----|---------|
| **FUTURE-001** | 9 Intent commands unused | Wire when SMITH integration begins | Phase 5 |

---

## 6. Summary Statistics

```
WORKING PATHS:     61 / 70 frontend wrappers (87.1%)
BROKEN PATHS:       4 (5.7%)
STUB COMMANDS:     18 backend commands return "not implemented"
UNUSED BACKEND:    19 commands have no frontend consumer

CRITICAL FIXES:     4 (command name mismatches / missing commands)
MEDIUM FIXES:       4 (wiring incomplete)
LOW FIXES:          3 (cleanup opportunities)
FUTURE WORK:        9 (Intent/SMITH integration)
```

---

## Appendix: File References

### Backend Command Registration
- [lib.rs:202-325](src-tauri/src/lib.rs#L202-L325) - All 84 commands registered

### Frontend Wrappers
- [tauri.ts](src/lib/utils/tauri.ts) - All 70 wrapper functions

### Key Stores
- [ecosystem.svelte.ts](src/lib/stores/ecosystem.svelte.ts) - Main dashboard data
- [telemetry.ts](src/lib/stores/telemetry.ts) - Telemetry & local collector
- [settings.ts](src/lib/stores/settings.ts) - API keys, alerts, settings
- [forgeRunStore](src/lib/stores/) - ForgeAgents run management

### Route Pages Audited
- `+page.svelte` (dashboard)
- `/forgeagents/+page.svelte`
- `/orchestrator/+page.svelte`
- `/telemetry/+page.svelte`
- `/settings/+page.svelte`
- `/alerts/+page.svelte`

---

*Report generated by Wiring Audit Agent*
