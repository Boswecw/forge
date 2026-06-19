# Slice 00 Evidence Reproduction

Generated: `2026-06-19T07:04:12Z`

## Validate Bootstrap Promotion Entry

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/validate_promotion_entry.py \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/promotions/2026-06-19--slice-00--promotion-governance-bootstrap.yaml
```

Expected result: pass output and exit code `0`.

## Generate Drift Inventory

Initial generation, when the target report files do not already exist:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/generate_drift_inventory.py
```

Expected result: one `.md` and one `.drift.yaml` report for each registered
repo pair under:

```text
/home/charlie/Forge/ecosystem/local-systems/promotion-ledger/drift-reports
```

For a non-destructive re-run after reports already exist, write to a temporary
output directory:

```bash
python3 /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/scripts/generate_drift_inventory.py \
  --out-dir /tmp/forge-promotion-drift-reports
```

## Inspect Reports

```bash
find /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/drift-reports \
  -maxdepth 1 -type f | sort
```

```bash
rg -n "dangerous_drift|unknown|missing_from_target" \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/drift-reports
```

Inspect the Slice 00 unknown drift type addendum:

```bash
sed -n '1,120p' \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/evidence/slice-00/unknown-drift-type-inventory.md
```

Inspect the documentation-first drift review:

```bash
sed -n '1,160p' \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/docs/slice-00/documentation-drift-review.md
```

Inspect `/doc/system` mirror proof:

```bash
sed -n '1,120p' \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/docs/slice-00/doc-system-mirror-proof.md
```

Inspect root documentation condensation proof:

```bash
sed -n '1,120p' \
  /home/charlie/Forge/ecosystem/local-systems/promotion-ledger/docs/slice-00/root-doc-condensation-proof.md
```

## Known Limitations

- The drift generator is intentionally conservative.
- Same-file matches are counted but not listed as item rows.
- Source-only files are classified as `missing_from_target` by default and can
  move to `source_local_hold` only through explicit resolution evidence.
- Target-only files and modified files are classified as `unknown` by default.
- Unknown and dangerous drift block promotion until human decision, backport, or
  explicit exception.
- The no reverse authority scan is evidence for review, not an acceptance
  decision.

## Recommended Human Review Steps

1. Review all `unknown` items in the generated drift reports.
2. Reclassify legitimate app-only target files as `target_only_glue`.
3. Reclassify legitimate target adaptations as `intentional_app_support_adaptation`.
4. Backport or recreate foundational target-only authority claims in the
   proving repos before future promotion.
5. Decide whether Slice 00 itself should remain `needs-followup`, be accepted,
   or be revised.
