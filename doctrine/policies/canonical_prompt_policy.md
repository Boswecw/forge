# Canonical Prompt Policy

## Overview
Canonical prompts under `doctrine/prompts/canonical/` define governance-critical
verification workflows. Changes to these prompts must be reviewed and anchored
to an ADR.

## Policy
- Any change to a file under `doctrine/prompts/canonical/` must include an ADR
  update in the same change set.
- ADRs live under `docs/adr/` and must follow the `ADR-####-*.md` naming pattern.
- The canonical prompt registry (`doctrine/prompts/canonical/registry.json`)
  is the source of truth for canonical prompt IDs and ownership.

## Enforcement Notes
- CI enforcement should verify that any diff touching canonical prompts also
  touches at least one ADR file under `docs/adr/`.
- If CI enforcement is unavailable, reviewers must enforce the rule manually.
