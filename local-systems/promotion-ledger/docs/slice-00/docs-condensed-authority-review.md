# Slice 00 `/docs` Authority Review

Generated: `2026-06-19T08:09:06Z`

This continuation reviews the 17 `docs_condensed_documentation` items from the
documentation drift review. It applies the local-system promotion rule:

- `/docs` is the documentation home.
- Condensed inactive plans may remain in `/docs`.
- Target-only support docs are not source authority.
- Foundational doctrine, contracts, routing rules, and integration contracts must
  exist in the local-system proving repo before they can be promoted to the
  app-support copy.

## Result

No remaining `/docs` item needs a placement move. The remaining problem is
authority direction.

| Decision | Count | Meaning |
| --- | ---: | --- |
| `source_intake_required_before_promotion` | 11 | Target doc defines doctrine, contract, registry, privacy, migration, visibility, or routing authority. It must be backported or re-authored in the proving repo before support promotion. |
| `source_diff_reconciliation_required` | 3 | A source-side doc exists, but target drift must be reconciled before promotion. |
| `target_support_only_or_receipt` | 2 | Target-side operation note or closeout receipt; keep in target `/docs`, but do not treat as promoted source authority. |
| `source_equivalent_condensed` | 1 | Source already has an equivalent condensed roadmap; reconcile naming only if needed. |

## Decisions By Item

| Repo pair | Path | Decision | Next action |
| --- | --- | --- | --- |
| `cortex__cortex` | `docs/service/authorforge-service.md` | `target_support_only_or_receipt` | Keep as app-support service operation doc unless the Cortex proving repo adds the AuthorForge service wrapper. |
| `dataforge-Local__df-local-foundation` | `docs/app-integration-contract.md` | `source_intake_required_before_promotion` | Add source-side DF Local app attachment contract, then prove against schema/runtime surfaces. |
| `dataforge-Local__df-local-foundation` | `docs/architecture.md` | `source_intake_required_before_promotion` | Backport as source-side architecture doctrine or merge into the source architecture spec. |
| `dataforge-Local__df-local-foundation` | `docs/backup-export-restore.md` | `source_intake_required_before_promotion` | Backport as source-side backup/export/restore doctrine before support promotion. |
| `dataforge-Local__df-local-foundation` | `docs/closeout-initial-governed-implementation.md` | `target_support_only_or_receipt` | Keep as target closeout receipt; link from source only if the source repo has matching proof. |
| `dataforge-Local__df-local-foundation` | `docs/df-local-foundation_extended_roadmap.md` | `source_equivalent_condensed` | Source has `docs/dataforge-local_extended_roadmap.md`; reconcile naming only after source proof. |
| `dataforge-Local__df-local-foundation` | `docs/migration-doctrine.md` | `source_intake_required_before_promotion` | Backport migration doctrine and validate against migration tooling. |
| `dataforge-Local__df-local-foundation` | `docs/operational-visibility.md` | `source_intake_required_before_promotion` | Backport status/visibility contract and prove no content-bearing fields leak. |
| `dataforge-Local__df-local-foundation` | `docs/privacy-doctrine.md` | `source_intake_required_before_promotion` | Backport privacy doctrine and tie it to source validation. |
| `neuronforge-local-operator__neuronforge` | `docs/adr/ADR-2026-04-18-promotion-truth-upstream.md` | `source_diff_reconciliation_required` | Source has `docs/adr/ADR-001-promotion-truth-upstream-of-pact.md`; reconcile target paths and mirror claims to source truth. |
| `neuronforge-local-operator__neuronforge` | `docs/authorforge-task-envelope-contract.md` | `source_intake_required_before_promotion` | Backport/re-author in NeuronForge proving repo before treating the support contract as promoted. |
| `neuronforge-local-operator__neuronforge` | `docs/authorforge-task-router-plan.md` | `source_intake_required_before_promotion` | Keep active-plan status, then backport into source planning docs before support promotion. |
| `neuronforge-local-operator__neuronforge` | `docs/local-first-cloud-assist-boundary.md` | `source_intake_required_before_promotion` | Backport as source doctrine and prove degraded/entitlement boundaries. |
| `neuronforge-local-operator__neuronforge` | `docs/model-routing-doctrine.md` | `source_intake_required_before_promotion` | Backport only after verifying source runtime claims for local-first/cloud escalation. |
| `neuronforge-local-operator__neuronforge` | `docs/neuronforge_architecture_spec.md` | `source_diff_reconciliation_required` | Source doc exists; compare target drift and prefer source-code-backed claims. |
| `neuronforge-local-operator__neuronforge` | `docs/neuronforge_extended_roadmap.md` | `source_diff_reconciliation_required` | Source doc exists; reconcile support wording after source roadmap is current. |
| `neuronforge-local-operator__neuronforge` | `docs/registries/task-lanes.md` | `source_intake_required_before_promotion` | Backport the task lane registry to source before support promotion. |

## Next Slice

1. Backport or re-author the 11 source-intake docs in the local-system proving
   repos.
2. Reconcile the 3 source/target drift docs by preferring source-code-backed
   truth.
3. Regenerate drift reports from the promotion ledger and verify the
   `docs_condensed_documentation` lane shrinks to support-only receipts or
   source-backed deltas.

Continuation: `source-authority-intake-proof.md` records the completed
source-intake pass and the refreshed drift shape.
