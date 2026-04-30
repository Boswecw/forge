# Canvas 05 — Rollout, Security, and Governance
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Lock the rollout posture so promotion integration stays governed, reversible, and fail-closed.

---

## Rollout stages

### Stage 0 — passive visibility
- manifest can be loaded
- no runtime behavior changes yet
- compatibility and mismatch states visible only

### Stage 1 — local carriage admitted
- neuronforge can accept and record admitted envelopes
- no cloud dependency required
- operator can approve local use

### Stage 2 — cloud intake admitted
- NeuroForge accepts only compatible promotion envelopes
- operator can separately approve cloud use

### Stage 3 — control-plane governed
- ForgeCommand becomes the working approval and mismatch surface
- rollback state visible across repos

### Stage 4 — active runtime dependence
- only after all lower stages are green
- runtime decisions may depend on admitted promotion state

---

## Security posture

Treat promotion metadata as governance-sensitive.

Protect against:
- partial envelope spoofing
- stale manifest reuse
- unsupported packet class claims
- digest substitution
- operator UI masking of blocked states
- local repo emitting “admitted” without proof artifacts

---

## Fail-closed rules

Fail closed when:
- manifest hash missing
- manifest version unsupported
- packet class unsupported
- requested/used profile pair unsupported
- strict hash missing for strict case
- non-strict canonical digest missing for non-strict case
- lineage identifiers absent where required by the seam
- evidence report cannot be loaded

Fail closed means:
- mark blocked
- do not silently downgrade to admitted
- do not infer missing truth
- make the reason visible to the operator

---

## Drift doctrine

There are three drift classes:

### Class 1 — source drift
PACT manifest or digest package changed.
Action:
- downstream repos must re-verify before being treated as compatible again

### Class 2 — consumer drift
A downstream repo changed its local schema or carrier fields.
Action:
- compatibility becomes mismatch until re-proved

### Class 3 — operator-state drift
Approval records exist for an older manifest.
Action:
- approval state becomes stale and cannot count as current approval

---

## Rollback doctrine

Rollback is required when:
- source manifest replaced without downstream proof
- consumer mismatch persists
- operator evidence missing or contradictory
- replay classification no longer matches admitted expectations

Rollback target should record:
- repo name
- manifest hash being exited
- reason code
- time of rollback
- operator note

---

## Explicit non-goals for this wave

Do not include in this promotion wave:
- new TOON segment shapes
- generalized multi-packet admission
- silent auto-upgrade to wave 2
- mutation of source digests from consumer repos
- broad agentic orchestration work

This wave is about **promotion integrity**, not feature expansion.
