# 01 — Purpose and Ownership

## What this repo is

`forge-contract-core` is the canonical contract center for the Forge ecosystem.

It exists to prevent semantic drift before multi-repo proving-slice implementation expands. It owns shared contract meaning and enforces discipline through machine-readable schemas, validators, and a canonical gate runner.

## What this repo owns

- Shared envelope schema (canonical wire format for all admitted artifact families)
- Admitted family schemas (proving slice 01: `source_drift_finding`, `promotion_envelope`, `promotion_receipt`)
- Canonical enum vocabularies (10 enums)
- Validator Python package (`forge_contract_core`)
- Fixture corpus (valid, invalid, duplicate, restricted, read-model)
- Canonical gate runner (`python -m forge_contract_core.gates.run_all`)
- Forbidden-pattern rules
- Repo role matrix (who may emit, consume, promote)
- Reference producer and consumer examples

## What this repo does NOT own

- Transport services
- Review UI or operator control surfaces
- Durable truth persistence for runtime artifacts
- Approval, execution, recommendation, contradiction, rollback, or calibration families (future phases only)
- Any application runtime code

## Authority position in the ecosystem

`forge-contract-core` is a prerequisite for all downstream proving-slice implementation.

No cross-repo transport work may proceed until:
- schemas exist
- validator package works
- gate runner passes
- role matrix exists
- fixture corpus exists

## Role class

`contract_core`
