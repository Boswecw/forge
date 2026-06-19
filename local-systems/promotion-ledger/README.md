# Forge Promotion Ledger

Short index for the promotion ledger scaffold.

Canonical documentation lives in:

- `docs/promotion-ledger-governance.md`
- `docs/documentation-governance.md`
- `docs/slice-00/documentation-drift-review.md`
- `docs/slice-00/source-local-hold-resolution-proof.md`
- `docs/slice-01/support-promotion-candidate-queue.md`
- `docs/slice-01/cortex-gnat-target-role-opening.md`
- `docs/slice-01/fa-local-gnat-dispatch-target-role-opening.md`
- `docs/slice-01/neuronforge-cor-gnat-semantic-handoff-target-role-opening.md`

Machine-readable registry, schemas, scripts, promotions, drift reports, and
evidence receipts remain in their named ledger directories.

Current Slice 00 closeout status: generated drift has zero `unknown`, zero
`dangerous_drift`, and zero `missing_from_target`. Reviewed source-only
artifacts are held as `source_local_hold` until a named support promotion slice
opens an explicit app-support target role.

Current Slice 01 intake queue: `source_local_hold` artifacts are grouped by
candidate type before any support promotion slice is opened.

Current Slice 01 target-role status: Cortex GNAT, FA Local GNAT dispatch, and
NeuronForge COR GNAT semantic handoff have support target-role documents, but
runtime, route, schema, model execution, and durable behavior remain held
source-local until later promotion slices name exact files and proof commands.
