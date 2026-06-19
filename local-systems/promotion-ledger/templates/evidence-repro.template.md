# Evidence Reproduction

## Commands

Validate a promotion entry:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/validate_promotion_entry.py \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/promotions/<promotion-entry>.yaml
```

Generate drift inventory:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/generate_drift_inventory.py
```

Inspect reports:

```bash
find /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/drift-reports -maxdepth 1 -type f | sort
```

## Known Limitations

- Drift classification is conservative.
- Unknown and dangerous drift block promotion.
- Human review is required before accepting any promotion decision.
