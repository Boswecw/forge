# Forge Workspace

`/home/charlie/Forge` is the workspace root for the Forge ecosystem. It contains
application repos, service repos, websites, shared packages, infrastructure,
reports, evidence, and generated artifacts.

Durable workspace-level documentation lives under [`docs/`](docs/). Individual
products and nested repos should keep their own docs beside the code they govern.

## Start Here

- [Documentation index](docs/INDEX.md) - central map for workspace-level docs.
- [Docs landing page](docs/README.md) - short guide to the docs tree.
- [Authoritative context](docs/governance/CONTEXT_AUTHORITATIVE_DO_NOT_DEVIATE.txt) - preserved governance/runtime context moved out of the root.
- [Master inventory](docs/governance/FORGE_MASTER_INVENTORY.md) - generated inventory of the Forge workspace.
- [Semantic cache Rust prompt](docs/ARCHITECTURE/FORGE_SEMANTIC_CACHE_RUST_EXECUTOR_PROMPT.md) - archived architecture/executor prompt.

## Root Documentation Policy

Keep the root documentation surface intentionally small:

- `README.md` stays at the root as the human entrypoint.
- Workspace-level docs belong in `docs/`.
- Service-specific docs belong in the owning service or app directory.
- One-off or unclear ownership docs belong in `docs/archive/root-holding/` until promoted or retired.
- Reports belong in `reports/`.

The former ForgeImages package README that was sitting at the workspace root is
preserved at
[`docs/archive/root-holding/FORGEIMAGES_IMPLEMENTATION_PACKAGE_README.md`](docs/archive/root-holding/FORGEIMAGES_IMPLEMENTATION_PACKAGE_README.md).
