# forge-contract-core

Canonical contract center for the Forge ecosystem.

This repo owns:
- shared envelope schemas
- admitted family schemas (proving slice: `source_drift_finding`, `promotion_envelope`, `promotion_receipt`)
- enum vocabularies
- validator library
- fixtures
- compatibility notes
- version registry
- repo role-class registry
- canonical gate runner
- forbidden-pattern rules
- reference producer and consumer examples

It does **not** own:
- transport services
- review UI
- durable truth persistence for runtime artifacts
- approval, execution, recommendation, contradiction, rollback, or calibration families (future phases only)

## Quick start

```bash
pip install -e ".[test]"
python -m forge_contract_core.gates.run_all
pytest
```

## Contract governance

Changes to admitted families require an RFC. See `doc/system/06_change_workflow_and_rfc_rules.md`.

## Exit criteria for proving slice 01

This repo is ready when:
- three admitted family schemas exist
- validator package works
- canonical gate runner exits green on correct fixture corpus
- repo role matrix exists
- reference producer and consumer examples exist
- SYSTEM.md is assembled and truthful
