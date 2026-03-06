# Slice 1: Deterministic Policy Envelope

Slice 1 adds static, fail-closed governance around ForgeAgents LLM execution.

## Policy Source

Policies are loaded from DataForge, which remains the source of truth.

- Policy fetch: `GET /api/v1/policy-envelopes/{policy_key}`
- Run state hydrate: `GET /api/v1/policy-runs/{run_id}/state`
- Ledger append: `POST /api/v1/policy-runs/ledger`
- Finalization: `POST /api/v1/policy-runs/finalize`
- Pricing lookup for cap checks: `GET /api/v1/models`

The runtime loader is `ForgeAgents/app/llm/policy_envelope.py`. Missing or invalid policy data raises a hard failure before any model call.

Seed the required baseline envelopes with:

```bash
cd /home/charlie/Forge/ecosystem/DataForge
.venv/bin/python -m scripts.seed_policy_envelopes
```

The seed script creates:

- `forgeagents.assist.v1`
- `forgeagents.skills.v1`
- `forgeagents.agent.<agent_type>.v1` for the wired ForgeAgents agent types

## Enforcement Boundary

Enforcement lives in `ForgeAgents/app/llm/manager.py`, which is the active LLM execution boundary used by:

- `ForgeAgents/app/api/assist.py`
- `ForgeAgents/app/api/skills.py`
- `ForgeAgents/app/agents/llm_helper.py`

Each governed request must carry explicit metadata:

- `policy_run_id`
- `policy_envelope_key`

Current entrypoints set those keys explicitly and opt into `auto_start_policy_run`. Agent helper calls also auto-finalize per chat call unless a caller provides a longer-lived run id.

## Gates

The manager enforces these checks before provider execution:

- policy metadata present, otherwise fail closed
- run state known or explicitly auto-started
- run not already finalized
- requested model is in the whitelist
- current call count is below `max_calls_per_run`
- `observed_tokens + estimated_tokens` stays within `max_tokens_per_run`
- `observed_cost + estimated_cost` stays within `max_cost_usd_per_run`
- elapsed wall time stays within `total_run_seconds`

Each provider call is wrapped in `asyncio.wait_for(...)` using `per_call_seconds`.

## Cap Computation

Prompt-token estimates come from the registered provider `count_tokens(...)`.

Completion-token estimates use `request.max_tokens` when present. Slice 1 keeps this static and deterministic; it does not add learned estimation.

Cost is computed from the DataForge model catalog using `input_cost_per_mtok` and `output_cost_per_mtok`:

- estimated pre-call cost uses estimated prompt tokens plus estimated completion tokens
- observed post-call cost uses provider-reported `prompt_tokens` and `completion_tokens`

If pricing is missing for a model, the run is denied with `price_not_configured`.

## Ledger And Finalization

Every observed call appends an immutable `LedgerEntryV1` to DataForge and updates an in-memory run accumulator for fast gate checks.

Finalization writes a single `RunFinalizationV1` record with:

- `success`
- `terminated`
- `error`

After finalization:

- DataForge rejects additional ledger writes with `409`
- ForgeAgents marks the run locally as finalized
- any later call using the same run id is blocked with `run_already_finalized`

Slice 1 also defines deterministic `RunScoreV1`. Threshold enforcement is applied when a caller supplies an explicit score payload; otherwise the runtime emits the fixed schema with placeholder values.
