# 02. Contracts, Schemas, and Data Model

**Date:** 2026-04-17  
**Time:** America/New_York

## Objective

Lock the contracts and schema posture for the ForgeCommand ↔ DataForge Local local-systems analytics lane.

## Contract doctrine

Every analytics payload must be:

- derived
- schema-versioned
- freshness-labeled
- read-only
- bounded to local systems analytics/information

## Phase 1 endpoints

### `GET /api/v1/analytics/overview`
Top-level dashboard summary.

### `GET /api/v1/analytics/systems`
Per-system operational posture.

### `GET /api/v1/analytics/queue`
Queue posture summary.

### `GET /api/v1/analytics/freshness`
Freshness and source age posture.

## ForgeCommand proxy routes

### `GET /fc/local/analytics/overview`
### `GET /fc/local/analytics/systems`
### `GET /fc/local/analytics/queue`
### `GET /fc/local/analytics/freshness`

## Common response envelope

All responses should include:

```json
{
  "_derived": true,
  "schema_version": "v1",
  "computed_at": "2026-04-17T18:00:00Z"
}
```

## Locked enums

### `SystemStatus`

- `healthy`
- `degraded`
- `offline`
- `unknown`

### `StalenessPosture`

- `fresh`
- `aging`
- `stale`
- `unknown`

## Overview response model

```json
{
  "_derived": true,
  "schema_version": "v1",
  "computed_at": "2026-04-17T18:00:00Z",
  "window_start": "2026-04-17T17:45:00Z",
  "window_end": "2026-04-17T18:00:00Z",
  "staleness_posture": "fresh",
  "degradation_flags": [],
  "systems_summary": {
    "total": 5,
    "healthy": 4,
    "degraded": 1,
    "offline": 0,
    "unknown": 0
  },
  "queue_summary": {
    "queued": 8,
    "claimed": 1,
    "retryable": 2,
    "dead_letter": 0,
    "oldest_item_age_seconds": 94
  },
  "freshness_summary": {
    "fresh": 4,
    "aging": 1,
    "stale": 0,
    "unknown": 0,
    "max_source_age_seconds": 212
  }
}
```

## Systems response model

```json
{
  "_derived": true,
  "schema_version": "v1",
  "computed_at": "2026-04-17T18:00:00Z",
  "staleness_posture": "fresh",
  "systems": [
    {
      "system_id": "forgecommand",
      "system_name": "ForgeCommand",
      "system_role": "operator_control_surface",
      "enabled": true,
      "status": "healthy",
      "freshness_posture": "fresh",
      "last_ok_at": "2026-04-17T17:59:42Z",
      "last_error_at": null,
      "endpoint": "http://127.0.0.1:8004",
      "notes": null
    }
  ]
}
```

## Queue response model

```json
{
  "_derived": true,
  "schema_version": "v1",
  "computed_at": "2026-04-17T18:00:00Z",
  "staleness_posture": "fresh",
  "status_counts": {
    "queued": 8,
    "claimed": 1,
    "retryable": 2,
    "dead_letter": 0
  },
  "stale_leases": 0,
  "oldest_item_age_seconds": 94,
  "average_queue_dwell_seconds": 28,
  "degradation_flags": []
}
```

## Freshness response model

```json
{
  "_derived": true,
  "schema_version": "v1",
  "computed_at": "2026-04-17T18:00:00Z",
  "overall_staleness_posture": "aging",
  "max_source_age_seconds": 212,
  "sources": [
    {
      "source_id": "neuronforge-local",
      "source_name": "NeuronForge Local",
      "freshness_posture": "aging",
      "age_seconds": 212,
      "last_updated_at": "2026-04-17T17:56:28Z",
      "degraded_reason": null
    }
  ]
}
```

## Data-model rules

### Systems inventory rules

- `system_id` must be stable and machine-safe
- `system_name` is presentation-facing
- `system_role` should use a locked vocabulary later if it grows
- `enabled` is config/state visibility, not health
- `status` is operational posture

### Freshness rules

- freshness must be computed at source granularity
- freshness thresholds must be centrally configurable
- a source with missing timestamps must return `unknown`, not `fresh`

### Queue rules

- queue metrics must be derived from real queue truth, not guessed counters
- stale lease logic must be deterministic and threshold-based

## Expansion candidates after Phase 1

Only after Phase 1 is stable:

- artifact analytics
- validation analytics
- lineage anomaly rollups
- historical trend windows
- export/report packet schemas

## Contract locking decisions before repo work

The following must be treated as locked before implementation starts:

- endpoint names
- envelope fields
- enum values
- read-only posture
- schema version handling
- fail-closed behavior on schema mismatch

## Acceptance criteria

Contracts are ready only when:

- both repos have typed models for the same shapes
- proxy behavior is deterministic
- schema mismatch behavior is explicit
- stale/unknown/degraded states are represented distinctly
- no UI page depends on ad hoc field guessing

