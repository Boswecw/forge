# Forge Ecosystem — Canonical Reference

**Document Role:** Authoritative ecosystem doctrine and architectural intent for Forge.

This document defines **what Forge is**, **what it is not**, and **the invariants that must not drift** as services, models, tooling, and personnel change.

It is not a README, onboarding guide, or tutorial. Navigation, service lists, and setup instructions live in the repository README.

---

## 1. Scope and Authority

This document is **canonical**.

- If a service README conflicts with this document, **this document wins**.
- If implementation behavior conflicts with this document, the behavior is considered **defective or incomplete**.
- Changes to this document require explicit, deliberate intent.

Forge exists as **business infrastructure**, not a releasable product.

---

## 2. What Forge Is

Forge is **internal AI engineering infrastructure**.

It is a governed system for designing, operating, and verifying AI-assisted and AI-mediated systems over time.

Forge treats the following as first-class operational actors:

- Code
- Models (local and hosted)
- Prompts
- Agents
- Pipelines
- Automation

These actors are expected to evolve, drift, and interact in non-trivial ways.

Forge exists to keep those interactions **governable, inspectable, attributable, and correct** over time.

---

## 3. What Forge Is Not

Forge is not:

- A traditional software development framework
- A consumer-facing application platform
- A “move fast and fix later” environment
- A system optimized for developer convenience over correctness

Velocity is allowed. **Unbounded velocity is not.**

---

## 4. Core Operating Model

Forge operates on a **governance-first engineering model**.

### 4.1 Intent → Execution → Evidence

All meaningful system behavior follows this chain:

1. **Intent** — human-defined doctrine, rules, and contracts
2. **Execution** — code, agents, models, and pipelines performing work
3. **Evidence** — immutable artifacts proving what occurred

Evidence is the only acceptable source of truth.

---

## 5. Evidence-First Architecture

Forge systems must:

- Emit **immutable evidence artifacts**
- Prefer append-only storage
- Avoid hidden or implicit state
- Make reconstruction possible without human memory

User interfaces are **views**, not authorities.

If evidence does not exist, the event is treated as **non-existent**.

---

## 6. Determinism, Drift, and Reality

Forge assumes:

- AI systems are partially non-deterministic
- Behavior can change without code changes
- Correctness must be measured continuously

Therefore:

- Drift detection is mandatory
- Fingerprints and stable identifiers are required
- Trends matter as much as point-in-time results

Drift is not a failure by default.

**Unobserved drift is.**

---

## 7. Governance as Infrastructure

Governance in Forge is **implemented**, not aspirational.

Examples:

- Doctrine validation is enforced by tooling
- Ecosystem verification is executed by runners
- Violations and outcomes are recorded as evidence

Policy documents without enforcement mechanisms are considered **non-operational**.

---

## 8. Human Authority

Forge is explicitly **human-authoritative**.

- Humans define doctrine and constraints
- Humans approve changes
- Humans accept or reject risk

AI systems may recommend, generate, or execute — but they do not decide what is acceptable.

---

## 9. Continuity Over Individuals

Forge is designed so that:

- People can leave
- Models can be replaced
- Tools can change

…and the system remains understandable and operable.

This requires:

- Minimal tribal knowledge
- Explicit contracts
- Durable, inspectable evidence

Any design that requires “knowing how it works” from memory is considered fragile.

---

## 10. Change Discipline

Changes to core Forge behavior require:

1. Intent to be documented
2. Contracts to be updated (when applicable)
3. Evidence to be regenerated

Silent behavior changes are forbidden.

---

## 11. Service Relationship Model

Forge services are:

- Loosely coupled
- Explicitly contracted
- Continuously verified

No service is trusted implicitly.

Health, readiness, and synthetic verification exist to continuously re-earn trust.

---

## 12. Risk Posture

Forge optimizes for:

- Long-term correctness
- Explainability
- Auditability

Forge does not optimize for:

- Short-term throughput
- Maximum experimentation
- Implicit trust in automation

---

## 13. Enforcement Philosophy

Rules that cannot be enforced should:

- Be documented as advisory
- Not be treated as guarantees

Conversely:

If something is critical, it must be enforced **by code**.

---

## 14. Relationship to Other Documentation

- **Repository README** — orientation, navigation, service list
- **Service READMEs** — local behavior, workflows, constraints
- **Operating plans** — execution and continuity procedures

All services and documents inherit this canonical context.

---

## 15. Final Invariant

Forge exists to ensure that:

> **Complex AI-assisted systems remain governable by humans over time.**

Any design decision that undermines this invariant is invalid by definition.

---

**This document is authoritative until explicitly superseded.**