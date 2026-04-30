# V1 Self-Healing Integration — Use Current Centipede Evidence Now

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Intent

Do not wait for future Centipede evidence contracts before improving Self-Healing.

Use the richest evidence Centipede already provides now, and build Self-Healing around that current truth surface.

## Current evidence already available from Centipede

### 1. Run provenance
- run id
- repository id
- revision anchor
- run class
- runtime mode
- producer metadata
- timestamps
- operator note

### 2. Lane admission evidence
- lane id
- admitted vs denied
- lane health state
- denial reason

### 3. Decision trace evidence
- decision stage
- decision key
- disposition
- rationale
- evidence payload JSON blob

## Correct Self-Healing posture

Self-Healing should stop treating Centipede as a shallow incident producer and instead treat it as an **evidence-bearing upstream source**.

The integration target is not:

- "a new incident exists"

The integration target is:

- "here is the current evidence package for this run, as it exists today"

## What Self-Healing should do with current Centipede evidence

### A. Build a Centipede-to-Self-Healing evidence adapter
Input:
- Centipede run detail
- lane admissions
- decision traces

Output:
- Self-Healing incident envelope enriched with current evidence

### B. Preserve raw evidence
For every Centipede-backed incident, Self-Healing should keep:

- raw decision traces
- raw evidence payload JSON
- lane admission records
- run provenance

A normalized digest can exist beside the raw evidence, but not instead of it.

### C. Add evidence-derived summaries
For each incident, compute:

- admitted lane count
- denied lane count
- degraded lane count
- decision stage list
- terminal disposition mix
- rationale digest
- confidence-posture proxy based on lane support and denial posture
- operator review posture

### D. Separate evidence from proposal
The current Centipede evidence is not yet a complete correction proposal.

So Self-Healing should distinguish:

- **evidence-backed incident**
- **proposal candidate**
- **approved proposal**
- **executed correction**

Do not collapse those into a single object.

## Immediate improvement path

### Step 1
Add an evidence adapter from current Centipede run detail into Self-Healing.

### Step 2
Store both:
- raw upstream evidence
- normalized Self-Healing digest

### Step 3
Show evidence inside existing incident and proposal surfaces.

### Step 4
Only later, layer in the more formal `CentipedeSelfHealingProjection` contract.

## Bottom line

Even before the formal next-phase contracts land, Self-Healing can become materially better by using the **current Centipede evidence surface as evidence**, not just as a queue signal.
