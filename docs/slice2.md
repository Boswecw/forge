# Slice 2: Bandit Routing and Preference Vector

Slice 2 adds adaptive model selection on top of the Slice 1 policy envelope. Slice 1 remains authoritative: routing can only choose from allowed actions, and every selected action still passes the existing hard gates before execution.

## Routing Algorithm

The live router is `ForgeAgents/app/llm/bandit_routing.py` and is invoked from `ForgeAgents/app/llm/manager.py` before each governed LLM call.

Slice 2 ships exactly one routing policy:

- Thompson Sampling with `bandit_policy_id = "ts_v1"`

Execution flow:

1. Load `PolicyEnvelopeV1`
2. Build a routable action set from the policy whitelist and the DataForge model catalog
3. Derive `RouterContextV1` from the request
4. Normalize `PreferenceVectorV1`
5. Load tenant-scoped `BanditStateV1` from DataForge
6. Select an allowed action
7. Run the existing Slice 1 pre-call gates
8. Execute the call
9. Compute deterministic reward
10. Atomically persist updated bandit state plus reward record

If the bandit state is missing or corrupt, the router falls back to a deterministic baseline action and marks `router_degraded = true`. Degraded mode still stays inside the whitelist.

## Reward Definition

Reward is versioned as `RewardV1` and bounded to `[0, 1]`.

Inputs:

- observed cost
- observed latency
- `RunScoreV1.quality_score`
- `RunScoreV1.safety_score`
- `RunScoreV1.invariant_pass`
- `RunScoreV1.unit_tests_pass`

Weighted components:

- quality uses `quality_score`
- safety uses `safety_score` only when invariants and unit tests pass
- cost is normalized against the candidate action set
- latency uses a deterministic inverse-time score

The final reward is the normalized weighted sum of those components using `PreferenceVectorV1`.

If Slice 1 terminates the run on a hard cap before or immediately after the call, no bandit update is written.

## State Storage

DataForge remains the source of truth.

Schemas:

- `BanditStateV1`
- `RewardRecordV1`
- `ActionV1`
- `RouterContextV1`
- `PreferenceVectorV1`

Persistence tables:

- `llm_policy_bandit_states`
- `llm_policy_reward_records`

Endpoints:

- `GET /api/v1/policy-routing/bandit-states/{tenant_id}/{policy_key}`
- `PUT /api/v1/policy-routing/bandit-states/{tenant_id}/{policy_key}`
- `POST /api/v1/policy-routing/rewards`
- `POST /api/v1/policy-routing/outcomes`

`POST /api/v1/policy-routing/outcomes` is the authoritative write path for normal execution. It updates `BanditStateV1` and appends `RewardRecordV1` in one transaction with optimistic version checks so partial writes are rejected.

## Preference Vector Behavior

Operators can supply `PreferenceVectorV1` in request metadata under `preference_vector`.

Weights:

- `w_quality`
- `w_cost`
- `w_latency`
- `w_safety`

The router normalizes the vector with `sum_to_one`.

Practical effect:

- cost-heavy vectors bias toward cheaper actions
- quality-heavy vectors bias toward higher-tier actions
- latency-heavy vectors bias toward faster actions
- safety-heavy vectors bias toward safer tiers

Every ledger entry now records routing audit metadata:

- `action_id`
- `action_mode`
- `router_context`
- `preference_vector`
- `bandit_policy_id`
- `bandit_state_hash`
- `router_degraded`
- `high_cost_action`

Those fields make each decision auditable without weakening Slice 1 finalization or cap enforcement.
