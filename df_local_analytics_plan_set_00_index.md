# ForgeCommand ↔ DataForge Local Local-Systems Analytics Plan Set

**Date:** 2026-04-17  
**Time:** America/New_York  
**Scope:** Single-person BDS business / local systems analytics, information, and operator diagnostics

## Purpose

This canvas set is the complete planning package for connecting **ForgeCommand** to **DataForge Local** so ForgeCommand becomes the operator-facing control surface and DataForge Local becomes the local systems analytics and information substrate.

This plan is intentionally framed for a **single-operator internal business system**.
It is not written as a SaaS plan, not as a customer BI plan, and not as a multi-tenant analytics platform.

## Plan set contents

### 00. Index and governance frame
This document.

### 01. Architecture and authority boundaries
Locks the ownership model, trust boundaries, runtime topology, and what each system is allowed to do.

### 02. Contracts, schemas, and data model
Locks the Phase 1 and expansion contract shapes, enums, response rules, freshness posture, and read-model doctrine.

### 03. Repository mapping and implementation sequencing
Maps the work into ForgeCommand and DataForge Local repos and breaks implementation into bounded slices.

### 04. UI, operator workflow, and analytics surfaces
Defines how the operator will consume the analytics, what pages exist, and how degraded/stale/offline posture should be rendered.

### 05. Verification, operations, and governance
Defines the proof gates, test matrix, runtime checks, failure posture, and change-control expectations.

## Core intent

The target outcome is a governed local analytics lane where:

- **ForgeCommand** owns the operator-facing cockpit
- **DataForge Local** owns local systems analytics/read-model computation
- **DataForge Cloud** remains outside the immediate Phase 1 local analytics loop except where long-lived persistence is needed later
- all local analytics are explicitly marked **derived**, **freshness-labeled**, and **non-canonical**

## Locked baseline assumptions

- single person business
- local-first runtime
- ForgeCommand remains the operator control plane
- DataForge Local is for local systems analytics and information
- no direct UI calls to DataForge Local
- Axum remains the contract gate and proxy boundary
- analytics endpoints are read-only
- freshness and degradation must be explicit
- no fake healthy state is allowed

## Recommended execution order

1. Read 01 first
2. Lock 02 before repo work
3. Use 03 to execute slice-by-slice
4. Build UI from 04 only after 02 is locked
5. Enforce 05 before calling any slice complete

## Minimum success state

The plan succeeds when:

- ForgeCommand can reach DataForge Local through a governed proxy boundary
- ForgeCommand renders trustworthy local systems analytics and information
- stale/degraded/offline states are explicit
- contracts are stable and typed
- verification is strong enough that this does not become a hidden governance burden later

