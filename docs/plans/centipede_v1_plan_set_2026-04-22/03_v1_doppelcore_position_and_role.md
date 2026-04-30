# V1 DoppelCore Position and Role

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Core decision

DoppelCore should live as its **own internal ecosystem component**.

It should **not** live inside:
- Centipede
- Self-Healing
- Registry UI code
- Cortex

## Recommended placement

### Primary placement
A standalone internal ecosystem repo, for example:

`~/Forge/ecosystem/DoppelCore`

## Why this placement is correct

DoppelCore is not a crawler.
DoppelCore is not a fixer.
DoppelCore is not a UI page.
DoppelCore is not a bounded file-intelligence parser like Cortex.

DoppelCore is the governed **truth-core** layer for:

- machine-readable truth structures
- human-readable projection rules
- schema and ontology for claim-targets and truth surfaces
- parity and consistency validation rules
- deterministic projection and build rules
- evidence-linked document/twin primitives
- correction-ready deltas and proof obligations

That makes it a shared internal substrate, not a feature of one consumer.

## What DoppelCore should consume

Upstream evidence producers include:

- Centipede
- Registry scans
- other evidence-producing systems

These producers generate:
- observations
- mismatches
- parity failures
- evidence bundles

DoppelCore normalizes those into governed truth surfaces and correction-relevant deltas.

## What DoppelCore should produce

DoppelCore should not produce code changes directly.
It should produce **correction-ready artifacts**.

### 1. Twin truth records
Canonical machine-readable representation of governed truth surfaces.

### 2. Drift and mismatch records
Structured declarations of divergence across code, docs, config, and contracts.

### 3. Correction opportunities
Bounded descriptions of:
- what is wrong
- where it is wrong
- what class of correction would address it
- what evidence supports that conclusion
- whether operator review is required

### 4. Proof obligations
Requirements every downstream correction proposal must satisfy.

Examples:
- preserve required invariants
- maintain contract compatibility
- not violate documentation truth
- not degrade authority posture

### 5. Evaluation packets
Structured inputs for downstream evaluation systems containing:
- target identity
- mismatch class
- evidence lineage
- candidate metadata
- proof obligations
- acceptance criteria

### 6. Lineage bundles
Traceable linkage back to:
- originating evidence
- crawl/run ids
- truth-surface projections
- prior decisions

## Downstream stack position

The correct order is:

1. **Evidence producers**
   - Centipede
   - Registry scans
   - other evidence sources
2. **Truth-core**
   - DoppelCore
3. **Correction fabric**
   - forgeHQ
   - ForgeMath
   - forge-eval
   - eval-cal-node
4. **Operator governance**
   - Self-Healing
5. **Execution**
   - FA-Local-Operator
   - ForgeAgents

## What should consume DoppelCore

### Registry
Registry is the main operator and governance consumer for documentation truth.
It should use DoppelCore to:
- understand governed truth surfaces
- validate documentation parity
- materialize remediation proposals for doc/system drift
- drive its autonomous worker flows using governed truth

### Centipede
Centipede should use DoppelCore as a target ontology and truth schema.
It should **not** own DoppelCore.

### Self-Healing
Self-Healing should consume DoppelCore-derived findings when they become actionable correction incidents or proposal candidates.
It should **not** own the truth-core.

### ForgeCommand
ForgeCommand should host operator surfaces for Registry and other consumers, but it should not be the canonical home of DoppelCore semantics.

### DataForge
DataForge can store cloud-side lineage, long-term records, and history of DoppelCore artifacts, but it should not be the authoring home of DoppelCore semantics.

## Explicit non-owners

### Not Cortex
Cortex is intentionally bounded and anti-semantic-authority.
DoppelCore is semantic and governance heavy.
That is the wrong fit.

### Not Self-Healing
Self-Healing is downstream proposal and execution governance.
DoppelCore is upstream truth infrastructure.

### Not Centipede
Centipede is an evidence producer and reconciler.
DoppelCore is the truth-core.
Those roles must remain separate.

## Bottom line

If the correcting side of the system is driven by what DoppelCore produces, then DoppelCore is **upstream of the correction fabric**.

That is exactly where it should be.
