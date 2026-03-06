# §16 — Documentation Truth Policy

This section defines how the ecosystem reference distinguishes canonical doctrine from audit-derived snapshot facts.

## Definitions

### Canonical Fact

A canonical fact is stable, normative, and architecture-defining. Examples include:

- subsystem roles and ownership
- authority boundaries
- durable truth rules
- port assignments from the canonical registry
- HTTP versus CLI boundaries
- authentication semantics
- lifecycle rules
- fail-closed doctrine
- canonical Pack J stage ordering: `risk -> context slices -> reviewer findings -> telemetry matrix -> occupancy snapshot -> capture estimate`

### Snapshot Fact

A snapshot fact is measured from the current codebase or runtime surface and may change after future audits. Examples include:

- router or endpoint totals
- file counts and LOC
- command, route, component, or store totals
- test totals and coverage percentages
- schema, table, or model tallies
- phase/status summaries that include measured counts

## Labeling Rules

Use canonical wording for canonical facts:

- "Forge Eval is a standalone subsystem."
- "DataForge is the durable truth store."
- "Forge Eval has no resident HTTP API in the current Pack J runtime."

Label snapshot facts visibly with language such as:

- "Current audited snapshot"
- "Current code snapshot"
- "Audit-derived count"
- "As of this document version"

Do not present snapshot counts as timeless doctrine.

## Update Rules For Future Audits

1. Update canonical facts only when architecture, doctrine, ports, boundaries, or enforced stage order actually change.
2. Update snapshot facts when a code audit re-measures counts, coverage, or inventory totals.
3. If a chapter mixes doctrine and inventory, add a local note stating which content is canonical and which content is snapshot-derived.
4. When narrative stage names differ from internal IDs, document both:
   - narrative name for ecosystem doctrine
   - stage or artifact ID for code-facing references
5. If two sections disagree, resolve the conflict by:
   - correcting the stale value,
   - converting a measured value into snapshot-labeled wording,
   - or removing the lower-value duplicate.
6. After changes, rebuild `doc/SYSTEM.md` and verify that no old contradictory values remain.

## Maintainer Checklist

- Check canonical ports against `PORT_REGISTRY.md`
- Keep Forge Eval described as standalone CLI/runtime-local evaluation unless the codebase gains a resident service API
- Keep the Pack J narrative chain consistent across overview, architecture, integration, testing, and handover
- Treat counts as volatile unless a protocol or invariant explicitly fixes them
- Rebuild the compiled reference after every source-chapter edit
