# forge-contract-core — Claude Code Context

## What this repo is

This is the canonical contract center for the Forge ecosystem proving slice.

It is a Python library and schema corpus. It is NOT a runtime service, UI, or persistence layer.

## Admitted families (proving slice 01 only)

1. `source_drift_finding`
2. `promotion_envelope`
3. `promotion_receipt`

Do NOT add approval, execution, recommendation, contradiction, rollback, or calibration families until proving slice 01 is green.

## Where things live

- `contracts/` — JSON schemas (envelope, family payloads, enums, compatibility notes)
- `registry/` — family registry, version registry, deprecation registry, repo role matrix
- `forbidden_patterns/` — machine-readable forbidden-pattern rules
- `fixtures/` — valid, invalid, duplicate, restricted, read_model fixture corpus
- `examples/` — reference producer and consumer scripts (not production code)
- `forge_contract_core/` — Python package: validators, gates, canonical_json, refs, identity, enums
- `tests/` — schema tests, validator tests, property tests, gate tests
- `doc/system/` — modular documentation sections assembled into `SYSTEM.md`

## Running gates

```bash
python -m forge_contract_core.gates.run_all
```

This is the canonical gate command. Participating repos must run it. They may wrap it but not weaken it.

## Idempotency key algorithm

```
sha256(artifact_family + "|" + artifact_id + "|" + artifact_version + "|" + lineage_root_id)
```

## Reference grammar

```
<artifact_family>:<artifact_id>:v<artifact_version>
```

## Adding a new family

Requires RFC. See `doc/system/06_change_workflow_and_rfc_rules.md`. Never add a new family by bypassing the RFC process.

## Testing

```bash
pytest tests/ -v
```

## Documentation

Edit the modular files in `doc/system/`, then run `bash doc/system/BUILD.sh` to rebuild `SYSTEM.md`. Never edit `SYSTEM.md` directly.
