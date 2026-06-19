# Updated Plan: NeuroForge -> NeuronForge Ollama Delegation Boundary

Generated: 2026-06-19
Status: active plan; initial NeuroForge implementation slices committed

## Executive Ruling

The original finding still holds, but the implementation order should be tighter:

NeuroForge must stop owning direct Ollama execution. Ollama should be a NeuronForge-managed local/private runtime. NeuroForge should own route policy, governance, cloud fallback decisions, and route receipts, then delegate private runtime execution to NeuronForge through a stable contract.

This is not an "Ollama cloud provider" slice. It is a boundary correction.

Clean work package name:

```text
NF-BRIDGE-01 - NeuronForge Local/Private Runtime Delegation
```

## Implementation Progress

Initial NeuroForge-only implementation slices were committed on branch:

```text
/home/charlie/Forge/ecosystem/cloud-systems/NeuroForge
feat/provider-health-provisioning
```

Committed slices:

```text
237804c7 Delegate local route execution to NeuronForge
b61f2e33 Route model router local compatibility through NeuronForge
945765f7 Delegate chat local lane through NeuronForge
```

Current completed scope:

```text
- Added NeuronForgeDelegationClient and NEURONFORGE_* config.
- Canonical RouteResolver local/private lane delegates to NeuronForge.
- Legacy route_and_infer, _execute_on_provider, and direct execute local paths
  delegate to the same NeuronForge helper.
- ChatCompletionGateway local/private chat execution delegates to NeuronForge.
- Provider-health local/private reachability probe calls NeuronForge health,
  not Ollama /api/tags.
- ChatCompletionGateway no longer depends on ollama_client.base_url.
```

Proof run during implementation:

```text
venv/bin/python -m pytest neuroforge_backend/tests/test_model_router_provider_unification.py -q
venv/bin/python -m pytest neuroforge_backend/tests/test_chat_gateway_all_providers.py -q
venv/bin/python -m pytest neuroforge_backend/tests/test_governance_critical_no_fast_downgrade.py -q
git diff --check
```

Remaining direct-Ollama surfaces still need classification or migration:

```text
neuroforge_backend/clients/batch_ollama.py
neuroforge_backend/llm_service.py
neuroforge_backend/services/http_optimizer.py
neuroforge_backend/routers/authorforge.py
neuroforge_backend/services/providers/ollama_client.py
neuroforge_backend/config.py
docs and archived docs with OLLAMA_BASE_URL / localhost:11434 language
```

## Live-State Evidence

This section captures the baseline evidence that triggered the plan. Some
model-router and chat-gateway items have now been remediated by the commits
listed above; keep the remaining entries as the migration inventory.

### NeuroForge direct Ollama ownership remains present

Verified source root:

```text
/home/charlie/Forge/ecosystem/cloud-systems/NeuroForge
```

Current branch observed locally:

```text
feat/provider-health-provisioning...origin/feat/provider-health-provisioning
```

Direct or policy-level Ollama anchors:

```text
neuroforge_backend/services/model_router.py
  - imports OllamaClient
  - initializes self.ollama_client
  - initializes ChatCompletionGateway with self.ollama_client.base_url
  - route_and_infer calls self.ollama_client.generate(...)
  - _execute_on_provider calls self.ollama_client.generate(...)
  - _execute_route_decision calls self.ollama_client.generate(...) for local lane

neuroforge_backend/services/providers/ollama_client.py
  - owns local Ollama base_url
  - owns retry/circuit-breaker behavior
  - POSTs directly to {base_url}/api/generate

neuroforge_backend/clients/batch_ollama.py
  - owns OLLAMA_BASE_URL / localhost:11434
  - POSTs directly to /api/chat
  - exposes get_ollama_batch_client()

neuroforge_backend/config.py
  - defines OllamaConfig(default http://localhost:11434)
  - adds "ollama" to available providers when local models are enabled

neuroforge_backend/routing/policy.py
  - binds Ollama models under FAST tier
  - infer_provider_tier("ollama") returns FAST

neuroforge_backend/providers/identity.py
  - defines ollama as the local/private inference lane
```

Important nuance: the newer resolver path already has useful governance machinery. `RouteResolver` handles data-class firewall constraints, provider health, fail-closed unknown providers, and governance-critical downgrade rules. The migration should preserve that path and replace only the local execution branch.

### NeuronForge already has usable local runtime pieces

Verified likely app-local service root:

```text
/home/charlie/Forge/apps/public-app-local-support/neuronforge
```

Current branch observed locally:

```text
master...origin/master
```

Existing assets to reuse:

```text
service/main.py
  - GET /health
  - GET /api/v1/authorforge/health
  - GET /api/v1/authorforge/local-status
  - POST /api/v1/authorforge/tasks

service/local_runtime.py
  - the intended single local runtime adapter
  - POSTs to Ollama /api/generate
  - classifies unreachable/model_unavailable/timeout/bad_response

service/authorforge_task_contract.py
  - nf-task-envelope-v1
  - nf-task-response-v1
  - task/routing/provider/model/quota receipts

service/authorforge_task_service.py
  - validates task envelopes
  - dispatches local-first
  - preserves no-fake-output and manual-review-required invariants

service/cloud_escalation.py
  - local-can't-serve escalation hook
  - currently defaults to a neuroforge-named Render URL, which is a naming/boundary smell
```

There is also an operator-oriented checkout:

```text
/home/charlie/Forge/ecosystem/local-systems/neuronforge-local-operator
```

That repo contains route-class docs, scripts, local Ollama execution, and operator records. It may be the canonical long-term local operator, but the app-local support clone has the HTTP/service skeleton that best matches this bridge.

## Updated Target Shape

```text
NeuroForge
  - route policy
  - data-class firewall
  - governance-critical downgrade rules
  - cloud provider execution
  - cloud fallback authorization
  - RouteDecisionReceipt
  - NeuronForgeDelegationClient

NeuronForge
  - node profile
  - local/private capability snapshot
  - Ollama base URL and runtime health
  - /nf-node/health
  - /nf-node/capabilities
  - /nf-node/execute
  - local/private execution receipts
```

NeuroForge should not know how to call:

```text
/api/generate
/api/chat
OLLAMA_BASE_URL
localhost:11434
```

Those details belong behind NeuronForge.

## Contract Placement

Primary contract owner should be:

```text
/home/charlie/Forge/ecosystem/contracts/forge-contract-core
```

Use temporary local schemas only if forge-contract-core intake blocks the first proof slice. If temporary schemas are used, the plan must include a follow-up migration to forge-contract-core before broad rollout.

Minimum contract families:

```text
NeuronForgeNodeProfile.v1
NeuronForgeCapabilitySnapshot.v1
NeuronForgeExecutionDelegation.v1
NeuronForgeExecutionReceipt.v1
RouteDecisionReceipt.v1 extension for delegated_runtime_receipt
```

These should not be AuthorForge-only. The existing `nf-task-envelope-v1` can remain an app-specific adapter, but NeuroForge needs a general runtime delegation envelope.

## Implementation Sequence

### Slice 0 - Repo and boundary lock

Purpose: prevent work from landing in the wrong checkout or preserving stale assumptions.

Actions:

1. Fetch and compare the target branches for NeuroForge, app-local NeuronForge, neuronforge-local-operator, and forge-contract-core.
2. Choose the canonical NeuronForge service repo for the bridge. Default recommendation: start with `apps/public-app-local-support/neuronforge` because it already has a FastAPI service and local runtime adapter, then reconcile with `ecosystem/local-systems/neuronforge-local-operator`.
3. Produce a boundary audit file listing every active NeuroForge direct-Ollama touchpoint and classify each as migrate, compatibility shim, test-only, generated artifact, or delete-later.

Output:

```text
reports/neuronforge-ollama-boundary/<timestamp>/summary.md
```

Acceptance:

```text
rg -n "OllamaClient|OLLAMA_BASE_URL|/api/generate|/api/chat|localhost:11434" \
  neuroforge_backend \
  --glob '!**/__pycache__/**'
```

The report must explain every match.

### Slice 1 - Contract-first bridge

Purpose: make the boundary explicit before moving runtime behavior.

Actions:

1. Add NeuronForge delegation contracts to forge-contract-core or a clearly marked staging location.
2. Add valid and invalid fixtures.
3. Include semantic checks that enforce:
   - local/private execution cannot silently become cloud execution
   - data sensitivity is required
   - fallback policy is explicit
   - receipts are required
   - prompt/body logging policy is explicit
4. Add a compatibility map from existing AuthorForge `nf-task-*` receipts to the general NeuronForge receipt vocabulary.

Acceptance:

```text
bash ci_gate.sh
```

or the repo-local equivalent gate if contracts are staged outside forge-contract-core.

### Slice 2 - NeuronForge node API

Purpose: expose local/private runtime execution through NeuronForge, not direct NeuroForge clients.

Actions in the chosen NeuronForge service repo:

1. Add general endpoints alongside the AuthorForge-specific task API:

```text
GET  /nf-node/health
GET  /nf-node/capabilities
POST /nf-node/execute
```

2. Implement `/nf-node/execute` by wrapping `service/local_runtime.py`.
3. Return `NeuronForgeExecutionReceipt.v1` for every accepted request.
4. Fail closed when:
   - node disabled
   - model unavailable
   - data policy disallows local/private handling
   - request asks NeuronForge to perform cloud fallback
5. Keep AuthorForge `/api/v1/authorforge/tasks` working.

Acceptance tests:

```text
POST /nf-node/execute with valid local delegation -> succeeded receipt
POST /nf-node/execute with unavailable runtime -> failed receipt, no fake output
POST /nf-node/execute with disallowed sensitivity -> rejected_by_policy
GET /nf-node/capabilities -> available models and supported task flags
```

### Slice 3 - NeuroForge NeuronForgeDelegationClient

Purpose: create the bridge without changing the router all at once.

Actions in NeuroForge:

1. Add:

```text
neuroforge_backend/services/providers/neuronforge_client.py
```

2. Add config:

```text
NEURONFORGE_BASE_URL
NEURONFORGE_ENABLED
NEURONFORGE_TIMEOUT_SECONDS
NEURONFORGE_CLOUD_FALLBACK_DEFAULT=false
```

3. The client should call:

```text
GET  /nf-node/health
GET  /nf-node/capabilities
POST /nf-node/execute
```

4. It should return the current `ModelResult`-compatible shape plus receipt metadata:

```text
metadata.neuronforge_execution_receipt
metadata.delegation_id
metadata.node_id
metadata.node_mode
```

5. It must not import or instantiate `OllamaClient`.

Acceptance:

```text
NeuronForgeClient.execute() succeeds with mocked /nf-node/execute
NeuronForgeClient.execute() maps timeout/unreachable to explicit failure
NeuronForgeClient never calls /api/generate or /api/chat
```

### Slice 4 - Route-class compatibility

Purpose: avoid overloading FAST/STANDARD/PREMIUM with runtime location.

Actions:

1. Keep `ModelTier` as quality/governance tier:

```text
FAST
STANDARD
PREMIUM
```

2. Add a separate runtime route classification:

```text
NEURONFORGE_LOCAL
NEURONFORGE_PRIVATE_REMOTE
NEURONFORGE_CUSTOMER_REMOTE
CLOUD_FAST
CLOUD_STANDARD
CLOUD_PREMIUM
```

3. Map legacy behavior:

```text
FAST + provider=ollama -> NEURONFORGE_LOCAL
STANDARD/PREMIUM + external provider -> CLOUD_STANDARD/CLOUD_PREMIUM
governance-critical + FAST local -> blocked unless explicit approved downgrade
```

4. Update reason codes and route receipts to include both:

```text
quality_tier=FAST
runtime_route_class=NEURONFORGE_LOCAL
```

Acceptance:

```text
Existing governance-critical no-fast-downgrade tests still pass.
New local runtime tests assert runtime_route_class=NEURONFORGE_LOCAL.
```

### Slice 5 - Switch NeuroForge router local execution

Purpose: remove direct Ollama execution from live NeuroForge routes.

Actions:

1. Update `_execute_route_decision` so local/private decisions call `NeuronForgeDelegationClient.execute(...)`.
2. Update `route_and_infer` and `_execute_on_provider` legacy paths so their Ollama branch delegates through the same client or is explicitly deprecated behind tests.
3. Remove `ChatCompletionGateway(self.ollama_client.base_url)` coupling. Gateway initialization must not depend on an Ollama client.
4. Keep `OllamaClient` only as a compatibility shim during this slice, with no live router ownership.
5. Update `test_model_router_provider_unification.py`:
   - replace "executes local ollama lane" with "delegates local lane to NeuronForge"
   - assert `router.ollama_client.generate` is not called
   - assert receipt metadata is preserved

Acceptance:

```text
Given provider=ollama/local lane
When ModelRouter executes the route decision
Then NeuroForge calls NeuronForgeDelegationClient
And does not instantiate/call direct Ollama execution
And returns provider/runtime metadata honestly
```

### Slice 6 - Batch and MAID migration

Purpose: direct `/api/chat` in `batch_ollama.py` is a second execution authority.

Actions:

1. Reclassify `OllamaBatchClient` as legacy-only.
2. Add a NeuronForge batch/delegation wrapper for local/private MAID participation, or explicitly block local batch until NeuronForge exposes the required batch semantics.
3. Update `clients/__init__.py` so public batch routing does not hand new callers a direct NeuroForge-owned Ollama batch client.
4. Add MAID tests proving local/private participation goes through NeuronForge receipts.

Acceptance:

```text
No live MAID path in NeuroForge calls /api/chat directly.
Local/private MAID responses carry NeuronForgeExecutionReceipt metadata.
```

### Slice 7 - Capability ingestion

Purpose: route local/private tasks based on NeuronForge capability snapshots, not hardcoded Ollama assumptions.

Actions:

1. Teach NeuroForge to read `/nf-node/capabilities`.
2. Merge capability snapshots into route eligibility without promoting NeuronForge into the external provider set.
3. Treat missing/stale capability snapshots as degraded and ineligible unless a test explicitly injects a healthy snapshot.
4. Decide whether DataForge should store capability snapshots or only route receipts. Default recommendation: DataForge stores durable truth; NeuroForge keeps short-lived cache.

Acceptance:

```text
Healthy snapshot + eligible task -> NeuronForge route eligible
Offline/stale snapshot -> local/private route ineligible
Customer-private data + no eligible private node + cloud fallback false -> fail closed
```

### Slice 8 - Fail-closed fallback rules

Purpose: prevent private data from silently crossing boundaries.

Rules:

```text
NeuronForge failure never silently becomes cloud.
Cloud escalation requires explicit policy and data-class permission.
Governance-critical tasks still require PREMIUM unless explicitly downgraded.
Unknown runtime/provider names fail closed.
Local/private receipt failure is visible in route metadata.
```

Acceptance tests:

```text
customer_private + NeuronForge offline + cloud_fallback_allowed=false -> fail closed
customer_private + cloud fallback true but firewall denies cloud -> fail closed
internal + NeuronForge offline + cloud fallback true + firewall allows -> approved cloud route
governance_critical + NeuronForge FAST/local + no override -> GovernanceRoutingError
```

### Slice 9 - Documentation and naming cleanup

Purpose: remove stale authority language.

Update:

```text
NeuroForge README.md
NeuroForge doc/system/00_overview/02-architecture.md
NeuroForge doc/system/20_runtime/05-backend-internals.md
NeuroForge doc/system/40_governance/14-scope.md
NeuroForge doc/system/40_governance/16-change-control.md
NeuronForge service README/docs
```

Replace:

```text
Ollama is the local/private inference lane inside NeuroForge.
```

with:

```text
Ollama is a NeuronForge-managed local/private runtime. NeuroForge may delegate
to NeuronForge when route policy, capability, data-class, and fallback rules permit.
```

Also clean up `service/cloud_escalation.py` naming drift. A NeuronForge cloud URL should not default to a neuroforge-named deployment unless the operational reality is documented and intentionally transitional.

## First Proof Slice

Recommended first implementation target:

```text
NF-BRIDGE-01A - Replace canonical local route execution with NeuronForge delegation
```

Scope:

```text
NeuroForge route_via_resolver/_execute_route_decision only
mocked NeuronForgeClient only
no live Ollama
no live NeuronForge service dependency
no batch migration yet
```

Acceptance tests:

```text
1. Given a RouteDecision(provider="ollama", tier=FAST)
   When _execute_route_decision runs
   Then NeuronForgeDelegationClient.execute is awaited
   And OllamaClient.generate is not awaited
   And ModelResult.metadata contains NeuronForge receipt fields

2. Given NeuronForgeDelegationClient returns unavailable and cloud fallback is false
   Then the route fails closed with explicit error metadata
   And no cloud adapter is called

3. Given governance_critical task with local/private route and no override
   Then existing GovernanceRoutingError behavior still holds

4. Given an external provider decision for xai/deepseek
   Then execution still uses get_adapter(provider)
   And no NeuronForge or Ollama path is called
```

Proof command candidates:

```text
python -m pytest neuroforge_backend/tests/test_model_router_provider_unification.py -q
python -m pytest neuroforge_backend/tests/test_governance_critical_no_fast_downgrade.py -q
rg -n "/api/generate|/api/chat|OLLAMA_BASE_URL|localhost:11434" neuroforge_backend \
  --glob '!clients/batch_ollama.py' \
  --glob '!services/providers/ollama_client.py' \
  --glob '!tests/**'
```

The final `rg` is allowed to keep legacy shim matches during the first proof slice, but no canonical router execution path should depend on them.

## Non-Goals

```text
Do not add Ollama as a cloud provider.
Do not promote NeuronForge/Ollama into the five external provider set.
Do not silently use cloud fallback when private runtime fails.
Do not delete the old Ollama clients before compatibility tests are migrated.
Do not let AuthorForge-specific task envelopes become the only NeuroForge delegation contract.
Do not treat generated/deb copies as live source authority.
```

## Final Done Criteria

The boundary correction is done when:

```text
1. NeuroForge live router and batch paths no longer call Ollama /api/generate or /api/chat.
2. NeuroForge local/private route decisions delegate to NeuronForge.
3. NeuronForge owns Ollama base URL, local runtime health, execution, and local receipts.
4. Route receipts include both NeuroForge route decision metadata and NeuronForge execution receipt references.
5. Data-class/firewall and governance-critical downgrade tests still pass.
6. Docs no longer say NeuroForge owns the local/private Ollama lane.
7. A source guard catches future direct Ollama execution reintroduction in NeuroForge.
```
