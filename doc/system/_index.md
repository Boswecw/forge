        # Forge Ecosystem - Compiled System Reference

        **Designation:** ECO
        **Document role:** Canonical compiled technical reference for the Forge ecosystem parent repo
        **Source:** `doc/system/`
        **Build command:** `bash doc/system/BUILD.sh`
        **Document version:** 2.0 (2026-06-22) - canonical compliance migration
        **Protocol:** BDS Documentation Protocol v2.0; BDS Repo Documentation System Canonical Compliance Standard

        > **Generated artifact warning:** `doc/ECOSYSTEM.md` is assembled output. Edit
        > the source modules under `doc/system/` and rebuild. Hand edits to the
        > compiled artifact are overwritten by the next build.

        Assembly contract:

        - Command: `bash doc/system/BUILD.sh`
        - Validation: `bash doc/system/validate_snapshots.sh` runs during assembly
        - Primary output: `doc/ECOSYSTEM.md`

        This `doc/system/` tree is the canonical source of truth for the Forge ecosystem parent repo. It uses
        explicit **truth classes**: canonical facts define ecosystem role, service
        boundaries, contract behavior, runtime behavior, and verification doctrine;
        snapshot facts are dated, audit-derived counts and current implementation
        inventory that may drift between audits.

        | Part | File | Contents |
        | --- | --- | --- |
        | §1 | `00_overview/00-overview.md` | §1 — Overview & Philosophy |
| §2 | `00_overview/01-architecture.md` | §2 — Architecture |
| §3 | `10_service-contract/10-product-surface.md` | Product Surface |
| §4 | `20_runtime/20-runtime.md` | Runtime |
| §5 | `20_runtime/30-data.md` | §11 — Database Schema |
| §6 | `30_dependencies/40-integrations.md` | Integrations |
| §7 | `40_governance/40-governance.md` | Governance |
| §8 | `50_operations/50-operations.md` | Operations |
| §9 | `99_appendices/90-appendices.md` | Appendices |

        ## Quick Assembly

        ```bash
        bash doc/system/BUILD.sh
        ```
