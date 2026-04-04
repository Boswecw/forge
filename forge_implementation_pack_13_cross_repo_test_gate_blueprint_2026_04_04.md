# Forge Implementation Pack 13 — Cross-Repo Test and Gate Blueprint

**Date:** 2026-04-04 01:35 America/New_York  
**Purpose:** Give VSCode Opus 4.6 an implementation-ready test and CI gate plan for the proving slice across the real participating repos.

---

# 1. Mission

Build the proving-slice verification spine so that compatibility is proven, not assumed.

The first-wave repos are:
- `forge-contract-core`
- `dataforge-Local`
- `DataForge` cloud
- `Forge_Command`

This blueprint defines the gate structure Opus should implement around them.

---

# 2. Required gate principle

A proving-slice repo is not ready because its code compiles.
It is ready only when its role-class gates pass.

Gate failures are blocking, not advisory.

---

# 3. First-wave gate matrix

## 3.1 forge-contract-core
Required gates:
- schema verification
- fixture corpus verification
- validator correctness
- role matrix integrity
- forbidden-pattern gate
- gate runner self-test

## 3.2 DataForge Local
Required gates:
- producer validation gate
- promotion admission gate
- queue/lease behavior gate
- retry/reconciliation gate
- dead-letter gate
- duplicate/idempotency gate
- read-model truthfulness gate

## 3.3 DataForge Cloud
Required gates:
- intake validation gate
- signature/identity gate
- acceptance/rejection gate
- duplicate reconciliation gate
- restricted visibility gate
- unsupported-version gate

## 3.4 ForgeCommand
Required gates:
- supported read-model gate
- stale/incomplete truthfulness gate
- restricted visibility rendering gate
- queue/detail lifecycle honesty gate
- changed-since-last-view behavior gate

---

# 4. Canonical gate runner integration

Every participating repo must run the contract-core gate entry point:

```bash
python -m forge_contract_core.gates.run_all
```

Opus should wire repo-local wrappers if needed, but the canonical gate runner must remain authoritative.

---

# 5. Test artifact strategy

## 5.1 Shared fixtures should come from contract core
Contract-core owns:
- valid fixtures
- invalid fixtures
- duplicate fixtures
- restricted fixtures
- stale/incomplete read-model fixtures where appropriate

## 5.2 Repo-local tests should consume shared fixtures
Repos may add local tests, but they must use shared fixtures wherever contract compatibility is being tested.

---

# 6. Cross-repo proving-slice scenarios Opus must cover

## Scenario 1 — valid accepted path
`source_drift_finding` emitted -> DataForge Local persists -> staging -> cloud accepts -> receipt exists -> ForgeCommand shows accepted truthfully.

## Scenario 2 — local blocked path
Artifact invalid or blocked before staging -> durable local blocked outcome -> ForgeCommand shows blocked/dead-letter truthfully.

## Scenario 3 — retryable transport failure path
Queue item sent -> retryable failure -> next retry computed -> no false acceptance -> ForgeCommand shows retrying truthfully.

## Scenario 4 — explicit rejection path
Cloud rejects -> rejection durable -> local reconciliation updates -> ForgeCommand shows rejected truthfully.

## Scenario 5 — duplicate/idempotent path
Same effective artifact sent again -> no duplicate shared truth -> duplicate-safe reconciliation -> local side resolves truthfully.

## Scenario 6 — receipt ambiguity path
Send outcome uncertain -> local state becomes awaiting reconciliation -> eventual resolve to accepted, rejected, retry, or dead-letter.

## Scenario 7 — dead-letter path
Retries exhausted or non-retryable resolution requires stop -> dead-letter durable -> ForgeCommand surfaces dead-letter honestly.

---

# 7. Required automated test layers

## 7.1 Contract-core tests
- schema tests
- validator tests
- registry tests
- property tests
- gate-runner tests

## 7.2 DataForge Local tests
- unit tests for admission and queue services
- integration tests for persistence + staging + reconciliation
- property tests for queue state invariants and lease reclaim

## 7.3 DataForge Cloud tests
- unit tests for intake classification
- integration tests for receipt/rejection persistence
- adversarial tests for duplicate and tamper behavior

## 7.4 ForgeCommand tests
- component tests for queue/detail rendering
- state truthfulness tests
- workflow tests for changed-since-last-view behavior

---

# 8. Suggested CI structure Opus should implement

## 8.1 Contract-core CI job
- install package
- run schema and validator tests
- run gate-runner self-test

## 8.2 DataForge Local CI job
- install contract-core dependency
- run contract-core gate command
- run local proving-slice unit/integration tests

## 8.3 DataForge Cloud CI job
- install contract-core dependency
- run contract-core gate command
- run intake/reconciliation tests

## 8.4 ForgeCommand CI job
- consume canonical read-model fixtures and/or generated test payloads
- run truthfulness UI tests
- run changed-since-last-view tests

---

# 9. Required failure behavior

If a required gate fails:
- CI must fail
- the repo is not proving-slice ready
- no manual “close enough” interpretation is allowed

Temporary waivers must be:
- explicit
- time-bounded
- documented
- exceptional

---

# 10. Adversarial tests Opus must prioritize

## 10.1 Duplicate send with same idempotency key
Must not create duplicate shared truth.

## 10.2 Duplicate send with altered metadata
Must not silently reconcile as safe duplicate if body meaning changed.

## 10.3 Lease expiration mid-send
Must not leave permanent limbo.

## 10.4 Receipt loss
Must not mark accepted without proof.

## 10.5 Invalid signature
Must not become retryable happy-path noise.

## 10.6 Restricted payload overexposure
Must not leak into broad review surface summaries.

---

# 11. Reporting and evidence

Opus should make each repo emit a proving-slice test report artifact that records:
- commit sha
- gate set run
- pass/fail by category
- failing scenario names
- generated timestamps

This can be lightweight, but the test evidence should not live only in terminal output.

---

# 12. Anti-scope statement for Opus

Do not:
- build an oversized general-purpose QA framework
- widen the gate suite to later-family behavior
- rely on prose-only compatibility claims
- treat UI smoke tests as enough for truthfulness

Keep the gate spine narrow and hard.

---

# 13. Implementation completion checklist

Opus should not declare the gate blueprint complete until:
- contract-core gates exist
- all first-wave repos are wired to them
- required scenario tests exist
- adversarial tests exist
- CI fails on required gate failure
- test evidence is retained in a reviewable form

If CI can still pass while required compatibility is broken, the proving-slice verification spine is not done.

