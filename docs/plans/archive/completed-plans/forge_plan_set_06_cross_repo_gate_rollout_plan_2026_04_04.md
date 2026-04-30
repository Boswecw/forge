# Forge Plan Set 06 — Cross-Repo Gate and Compatibility Rollout Plan

**Date:** 2026-04-04 01:19 America/New_York  
**Purpose:** Define how the actual participating repos adopt shared-family compatibility without drifting into repo-by-repo semantics.

---

# 1. Mission

This plan defines how the real ecosystem repos participate in the first shared-family proving wave.

It exists to ensure that compatibility is:
- machine-checked
- role-aware
- enforced in CI
- blocked when incomplete

It must prevent a repeat of “docs looked aligned, but runtime behavior drifted anyway.”

---

# 2. Participating repos in the first wave

## 2.1 Direct first-wave participants
- `forge-contract-core` — contract authority
- `dataforge-Local` — local truth and promoter
- `DataForge` (cloud) — shared intake and receipt authority
- `Forge_Command` — review surface

## 2.2 Indirect / later participants
- `forge-eval`
- `ForgeMath`
- `forgeHQ`
- `fa-local`
- `cortex` / CortexBDS
- `forge-local-runtime`
- `NeuronForge` / NeuronForge Local

These later systems may become producers, consumers, or execution participants later, but they should not all be pulled into the first proving wave at once.

---

# 3. Role classes for actual repos

## 3.1 `forge-contract-core`
Role class:
- `contract_core`

## 3.2 `dataforge-Local`
Role class:
- `producer_promoter`

## 3.3 `DataForge` cloud
Role class:
- `shared_truth_consumer`
- practical shared-truth owner for accepted artifacts

## 3.4 `Forge_Command`
Role class:
- `review_surface`

## 3.5 Later role classes
### `fa-local`
- `execution_consumer` (future)

### `forge-eval`
- `evaluation_producer`

### `ForgeMath`
- `evaluation_producer`
- possible later shared-truth consumer

### `forgeHQ`
- `producer_only`

### `CortexBDS`
- possible later `producer_only`

### `forge-local-runtime`
- no first-wave proving-slice ownership until more deeply authored

### `NeuronForge Local`
- possible later `producer_only` or bounded candidate producer

---

# 4. Gate profiles by real repo

## 4.1 Contract core
Required gates:
- schema verification
- fixture corpus verification
- validator correctness
- role-matrix integrity
- gate-runner integrity

## 4.2 DataForge Local
Required gates:
- all producer gates
- transport verification
- idempotency verification
- dead-letter/retry verification
- backlog observability verification
- read-model truthfulness verification for supplied queue/detail surfaces

## 4.3 DataForge Cloud
Required gates:
- consumer/intake schema verification
- signature and identity verification
- duplicate reconciliation verification
- unsupported-version rejection verification
- restricted-visibility handling verification

## 4.4 ForgeCommand
Required gates:
- supported-version read verification
- stale/incomplete handling verification
- restricted visibility handling verification
- queue/detail UI truthfulness verification

---

# 5. CI rollout rule

Every participating repo must run the canonical gate command from `forge-contract-core`.

Required standard entry point:

```bash
python -m forge_contract_core.gates.run_all
```

Each repo may wrap it, but may not weaken it.

---

# 6. Required repo onboarding checklist

Before a repo joins the shared contract surface, it must answer:
1. what role class does it have?
2. which families may it emit?
3. which families may it consume?
4. is promotion enabled?
5. what local-only truth must remain local?
6. what forbidden payload classes must it never emit?
7. what gate profile applies?
8. what version posture applies?
9. what signature/identity checks apply?
10. what review/read-model obligations apply?

No repo should be waved through this process because it is “part of the ecosystem anyway.”

---

# 7. Read-model governance rules

## 7.1 Shared rule
Derived read models must always be labeled as derived.

## 7.2 Required metadata
- source families
- derivation version
- derivation timestamp
- freshness posture
- stale/incomplete warning where applicable

## 7.3 Anti-rule
A review surface may not invent lifecycle meaning unsupported by canonical artifacts.

---

# 8. Compatibility verification matrix

## 8.1 Schema verification
Must prove:
- valid envelope path
- invalid envelope path
- valid family payload path
- missing-required-field rejection
- forbidden additional-field rejection
- enum parity validation

## 8.2 Validator correctness
Must prove:
- valid fixtures accepted
- invalid fixtures rejected
- producer output matches canonical validator expectations
- consumer rejects invalid inputs safely

## 8.3 Transport verification
For DataForge Local / Cloud path, must prove:
- accepted path
- rejection path
- retry path
- dead-letter path
- duplicate-send path
- receipt ambiguity path
- lease expiry and reclaim behavior
- backlog observability

## 8.4 Security verification
Must prove:
- blocked family cannot promote
- invalid signature blocked
- unsupported producer blocked
- oversize payload blocked
- restricted visibility not overexposed

## 8.5 Review-surface verification
Must prove:
- accepted looks accepted
- retrying looks retrying
- rejected looks rejected
- dead-letter looks dead-lettered
- stale/unknown does not look resolved
- restricted payloads remain constrained

---

# 9. Rollout order

## Step 1
Create and validate `forge-contract-core`.

## Step 2
Integrate canonical validator + gate runner into DataForge Local.

## Step 3
Integrate canonical validator + gate runner into DataForge Cloud intake.

## Step 4
Integrate read-model and UI truthfulness gates into ForgeCommand.

## Step 5
Run first full cross-repo proving-slice gate suite before enabling the end-to-end path.

---

# 10. Waiver rule

Required gate failures block readiness.

Temporary waivers:
- must be explicit
- time-bounded
- governance-approved
- visible
- never allowed to become hidden permanent compatibility paths

---

# 11. Exit criteria

Cross-repo rollout is ready only when:
- role classes are assigned honestly
- each direct participant passes its required gates
- CI fails on required gate failure
- no repo is carrying local semantic overrides for shared families
- queue/review/read-model honesty is proven end to end

Until that is true, the ecosystem is not yet compatible for proving slice 01.

