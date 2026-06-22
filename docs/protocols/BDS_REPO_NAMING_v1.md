# Repository Naming Convention Protocol

**Truth class:** canonical doctrine
**Protocol ID:** `BDS-REPO-NAMING-v1`
**Status:** active
**Applies to:** all BDS GitHub repositories, local checkouts, CI references, deployment mappings, and promotion ledgers.

## Purpose

Repository names must make ownership, system role, authority level, deployment intent, and governance boundaries obvious to both humans and agents.

A repo name is not branding decoration. It is an operational identifier.

## Naming Rule

All BDS repositories use lowercase kebab-case.

```text
<domain>-<system>-<role>
```

Optional extension:

```text
<domain>-<system>-<role>-<qualifier>
```

## Required Rules

1. Use lowercase only.
2. Use hyphens, not underscores.
3. Avoid abbreviations unless canonical.
4. Avoid vague names like `backend`, `frontend`, `core`, or `app` by themselves.
5. Do not rename a repo casually once referenced by CI, deployment, docs, or promotion ledgers.
6. Public-facing repos must clearly distinguish customer/product surfaces from internal control systems.
7. Local-first support systems must identify whether they are local, cloud, command, data, or customer-facing.

## Repository Classification Matrix

| Class | Prefix | Authority |
|------|------|------|
| Product Plane | `authorforge-*` | Customer-facing application authority |
| Local Runtime Plane | `neuronforge-*` | Local AI/runtime authority |
| Cloud Runtime Plane | `neuroforge-*` | Cloud AI/provider authority |
| Control Plane | `forge-command-*` | Governance, registry, audit, orchestration authority |
| Data Plane | `dataforge-*` | Data, memory, persistence authority |
| Customer Plane | `forgecustomer-*` | Customer, billing, entitlement authority |
| Doctrine Plane | `bds-*` | Canonical protocol and doctrine authority |

## Canonical Prefixes

```text
authorforge-*     Public author/customer product surface
neuronforge-*     Local model/runtime/support lane
neuroforge-*      Cloud reasoning/provider lane
forge-command-*   Control plane, governance, entitlement, registry
dataforge-*       Data, memory, persistence, analytics
forgecustomer-*   Customer/billing/account surface
bds-*             Company-wide protocols, doctrine, shared tooling
```

## Recommended Role Suffixes

```text
-api
-web
-desktop
-worker
-agent
-registry
-analytics
-contracts
-protocols
-support
-local
-cloud
-sdk
-cli
-tests
-docs
```

## Examples

```text
authorforge-web
authorforge-api
authorforge-support-api
neuronforge-local-operator
neuronforge-model-registry
neuroforge-provider-gateway
forge-command-registry
forge-command-analytics
forge-command-audit-agent
dataforge-local-store
dataforge-cloud-analytics
bds-protocols
bds-contracts
forgecustomer-web
forgecustomer-billing-api
```

## Forbidden Patterns

```text
AuthorForge_API
authorForgeApi
backend
frontend
main-app
test-repo
new-system
ai-agent
control
registry2
final-backend
```

## Authority Rule

A repository name must not imply authority it does not possess.

Authority is determined by:

1. Repository classification.
2. `SYSTEM.md` declarations.
3. Canonical doctrine in `doc/system/`.
4. Promotion governance records.

## Agent Rule

Agents must treat repository names as routing hints, not absolute authority.

Before modifying a repository, an agent must verify:

```text
1. repository name
2. SYSTEM.md
3. doc/system authority declarations
4. CI policy
5. promotion ledger
```

If these disagree, the agent must fail closed.

## Rename Policy

A repository may be renamed only when:

```text
1. Current name violates this protocol
2. New name has explicit canonical approval
3. GitHub references are updated
4. CI/CD references are updated
5. deployment providers are updated
6. local clone paths are updated
7. protocol/index docs are updated
8. promotion ledger records the rename
```

## Validation Regex

```regex
^[a-z0-9]+(-[a-z0-9]+)*$
```

Preferred BDS pattern:

```regex
^(authorforge|neuronforge|neuroforge|forge-command|dataforge|forgecustomer|bds)(-[a-z0-9]+)+$
```

## Compliance Levels

```text
compliant
legacy
deprecated
invalid
reserved
```

## Agent Enforcement

Agents must not create, rename, or reference repositories outside this convention unless explicitly approved by a human authority.

Unknown repositories must be classified as:

```text
unverified-repo
```

until validated.

## Summary

Repository names must be boring, explicit, durable, machine-readable, and governance-aware.

A valid repository name should tell an agent:

```text
who owns it
which plane it belongs to
what authority it possesses
what role it performs
whether it is local, cloud, public, customer, data, or control-plane
```
