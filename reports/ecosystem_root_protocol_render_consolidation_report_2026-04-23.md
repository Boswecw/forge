# Ecosystem Root Protocol And Render Consolidation Report

Date: 2026-04-23
Scope: `/home/charlie/Forge/ecosystem` repo root protocol files and Render blueprint YAML files.

## Goal

Remove loose protocol documents and ecosystem-level Render blueprints from the
ecosystem repo root while preserving all content and updating navigation.

## Files Moved

| Original root path | New path | Classification |
|--------------------|----------|----------------|
| `BDS_DOCUMENTATION_PROTOCOL_v1.md` | `docs/protocols/BDS_DOCUMENTATION_PROTOCOL_v1.md` | BDS documentation protocol reference |
| `bds_ai_assisted_development_operations_protocol.md` | `docs/protocols/bds_ai_assisted_development_operations_protocol.md` | AI-assisted development operations protocol |
| `render-dataforge-only.yaml` | `cloud-systems/render-blueprints/render-dataforge-only.yaml` | DataForge-first Render blueprint |
| `render-testing-phase.yaml` | `cloud-systems/render-blueprints/render-testing-phase.yaml` | Testing-phase Render blueprint |
| `render-consolidated.yaml` | `cloud-systems/render-blueprints/render-consolidated.yaml` | Consolidated Render blueprint |

## Files Added Or Updated

| Path | Purpose |
|------|---------|
| `docs/protocols/README.md` | Protocol directory guide |
| `cloud-systems/render-blueprints/README.md` | Render blueprint directory guide |
| `docs/README.md` | Added protocol docs and Render blueprint locations |
| `docs/DOCUMENTATION_INDEX.md` | Added protocol docs and Render blueprint locations |
| `docs/render-deployment/00_MASTER_INDEX.md` | Added ecosystem blueprint location |
| `doc/system/04-project-structure.md` | Updated ecosystem layout map |
| `doc/SYSTEM.md`, `SYSTEM.md` | Rebuilt ecosystem system docs |
| `scripts/ecosystem-documentation-protocol-sync.sh` | Updated generated audit source path |

## Final Root Surface

The ecosystem repo root no longer contains:

- `BDS_DOCUMENTATION_PROTOCOL_v1.md`
- `bds_ai_assisted_development_operations_protocol.md`
- `render-dataforge-only.yaml`
- `render-testing-phase.yaml`
- `render-consolidated.yaml`

## Verification

- Confirmed moved files exist at their new locations.
- Confirmed root-level protocol and `render*.yaml` files no longer exist.
- Left service-local `cloud-systems/*/render.yaml` files in place.
