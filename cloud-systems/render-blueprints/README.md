# Render Blueprints

This directory holds ecosystem-level Render blueprint YAML files that were
formerly stored at the ecosystem repo root.

## Files

| File | Purpose |
|------|---------|
| [render-dataforge-only.yaml](render-dataforge-only.yaml) | DataForge-first deployment blueprint that provisions the shared database and deploys DataForge |
| [render-testing-phase.yaml](render-testing-phase.yaml) | Testing-phase multi-service Render blueprint using one PostgreSQL database and shared Redis |
| [render-consolidated.yaml](render-consolidated.yaml) | Consolidated backend ecosystem blueprint with DataForge/Rake shared database and separate NeuroForge database |

Service-local `render.yaml` files remain inside the owning service directories.
Use this directory only for ecosystem-level blueprints.
