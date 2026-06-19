# Forge Promotion Ledger Governance

This ledger governs promotion from the local ecosystem proving repos into the
public app local-support bundle.

Source of truth:

- Proving authority: `/home/charlie/Forge/ecosystem/local-systems`
- Promoted app-support bundle: `/home/charlie/Forge/apps/public-app-local-support`

The app-support bundle is never the authority for shared doctrine, schemas,
readiness posture, degraded-state behavior, denial rules, service ownership,
runtime trust contracts, or public privacy/local-first claims. If an app-support
repo reveals a foundational need, classify it as drift, recreate or backport it
in the ecosystem proving repo, prove it there, then promote forward.

## Slice 00 Scope

Slice 00 creates governance only:

- promotion ledger scaffold
- repo registry
- promotion and drift schemas
- promotion and drift templates
- initial bootstrap promotion entry
- initial drift reports
- proof gate inventory
- no reverse authority scan
- documentation-first drift review

It must not alter runtime behavior, service logic, schemas, UI behavior, or
AuthorForge public surfaces.

## Decision Rule

The AI may draft entries, classify drift, summarize evidence, and propose
decisions. Only Charlie Boswell may make the final human acceptance decision.

Allowed promotion decisions:

- `accepted`
- `rejected`
- `rollback`
- `needs-followup`

## Drift Classification

Use exactly these classifications:

- `same`
- `intentional_app_support_adaptation`
- `missing_from_target`
- `target_only_glue`
- `dangerous_drift`
- `unknown`

Dangerous drift and unknown drift block promotion until resolved by human
decision, backport, or explicit exception.

## Commands

Validate a promotion entry:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/validate_promotion_entry.py \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/promotions/2026-06-19--slice-00--promotion-governance-bootstrap.yaml
```

Generate the initial conservative drift inventory:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/generate_drift_inventory.py
```

The scripts use Python standard library plus PyYAML. PyYAML is available in the
current environment; if it is missing in a future environment, install it before
running the scripts.
