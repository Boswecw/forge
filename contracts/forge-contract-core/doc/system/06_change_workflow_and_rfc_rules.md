# 06 — Change Workflow and RFC Rules

## When an RFC is required

An RFC (Request for Contract Change) is required for:
- Adding a new admitted artifact family
- Making a breaking change to an existing admitted family schema
- Adding a new major version of an admitted family
- Admitting a new promotable family
- Adding a new restricted payload class
- Adding contradiction, execution, or approval families
- Changing the repo role matrix for a direct proving-slice participant

## When an RFC is NOT required

No RFC needed for:
- Adding optional fields to a family schema (non-breaking)
- Adding new valid fixtures
- Bug fixes to the validator that do not change behavior
- Documentation improvements
- Adding new gate checks that do not fail existing passing repos

## RFC process

1. Open a PR with a description of the proposed change.
2. Label it `rfc`.
3. Assign a contract owner reviewer, a compatibility reviewer, and (for promotable families) a security reviewer.
4. The RFC must document:
   - What is changing and why
   - Which repos are affected
   - What migration path exists for existing consumers
   - Whether backward compatibility is preserved
5. RFC must be approved before implementation merges.

## Breaking change policy

A breaking change to an admitted family requires a new major version (v2, v3...). v1 consumers must never be silently broken.

## Deprecation process

To deprecate a family version:
1. Add an entry to `registry/deprecation_registry.json`.
2. Set `deprecated_at` in `registry/version_registry.json`.
3. Set `sunset_at` to give consumers a migration window.
4. After sunset, the version may be removed from `ADMITTED_VERSIONS` in `enums.py`.

## Role class changes

Changes to admitted emit or consume families in the role matrix require an RFC because they affect proving-slice security boundaries.
