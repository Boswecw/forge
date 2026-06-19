# Documentation Governance

This rule applies to promotion review across the local-systems proving repos and
the app-support promotion targets.

## Placement Rule

All human-authored documentation belongs under `/docs`.

Documentation should be condensed when it is not an active plan being
implemented. Active plans may remain expanded while they are actively driving a
slice; inactive plans should be reduced to status, decision, evidence, and next
action.

## Code Mirror Rule

`/doc/system` is the canonical code mirror surface. Treat it as a generated or
maintained mirror of code/system truth, not as the home for general
documentation.

`/doc/system` changes should be reviewed against:

- the live code they claim to mirror
- the repo-local build script
- generated assembled system output, if the repo uses one
- snapshot or validation scripts, if present

Do not accept `/doc/system` drift as documentation promotion. First prove that
the mirror reflects the live source and the proving repo authority.

## Promotion Review Rule

When a drift item is documentation-related:

- `/docs/**`: review as condensed documentation or active implementation plan.
- `/doc/system/**`: review as code mirror, not general documentation.
- root `README.md`, `SYSTEM.md`, closeout files, and generated assembled docs:
  keep as short pointers or generated artifacts; move substantive narrative into
  `/docs`.
- misplaced docs such as `doc/adr/**`, `registry/*.md`, or nested
  service-level README files should move or condense into `/docs` unless they are
  generated receipts.
- evidence and run records may remain in evidence/output locations, but they
  must not become doctrine.

Unknown documentation drift still blocks promotion until Charlie reviews,
backports, or explicitly excepts it.
