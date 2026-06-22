# BDS Repository Naming Compliance Report

Generated: `2026-06-22T15:13:15+00:00`

Root: `/home/charlie/Forge/ecosystem`

Protocol: [`docs/protocols/BDS_REPO_NAMING_v1.md`](../docs/protocols/BDS_REPO_NAMING_v1.md)

No repositories were renamed by this audit. Non-compliant names require the protocol rename policy: explicit canonical approval, GitHub reference updates, CI/CD updates, deployment-provider updates, local clone path updates, protocol/index updates, and promotion-ledger evidence.

## Summary

- Total repositories discovered: `36`
- Overall status uses the stricter result across the local checkout name and GitHub origin repository name.
- compliant: `1`
- legacy: `18`
- deprecated: `0`
- invalid: `16`
- reserved: `1`

Local checkout counts: compliant `1`, legacy `22`, deprecated `0`, invalid `12`, reserved `1`
GitHub origin counts: compliant `1`, legacy `19`, deprecated `0`, invalid `14`, reserved `1`

## Repository Inventory

| Status | Local repository | Origin repository | Path | Plane | Evidence | Rename candidate / action |
|---|---|---|---|---|---|---|
| legacy | `ecosystem` | `forge` | `.` | Doctrine Plane | SYSTEM, doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `DoppelCore` | `DoppelCore` | `DoppelCore` | Doctrine Plane | none | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `ERA` | `ERA` | `ERA` | Doctrine Plane | none | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `Forge_Command` | `Forge_Command` | `Forge_Command` | Control Plane | doc/system, CI, manifest | `forge-command-<role>` - Normalize casing/separators and add an approved role suffix. |
| invalid | `canebrake_press` | `canebrake_press` | `canebrake_press` | Doctrine Plane | SYSTEM, doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `checkly` | `none` | `checkly` | Doctrine Plane | doc/system | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `DataForge` | `DataForge` | `cloud-systems/DataForge` | Data Plane | SYSTEM, doc/system, CI | `dataforge-<role>` - Normalize casing/separators and add an approved role suffix. |
| invalid | `ForgeAgents` | `Forge-Agents` | `cloud-systems/ForgeAgents` | Control Plane | doc/system, CI | `forge-command-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `NeuroForge` | `NeuroForge` | `cloud-systems/NeuroForge` | Cloud Runtime Plane | SYSTEM, doc/system, CI | `neuroforge-<role>` - Normalize casing/separators and add an approved role suffix. |
| reserved | `forgecustomer` | `forgecustomer` | `cloud-systems/forgecustomer` | Customer Plane | SYSTEM, doc/system, CI | `forgecustomer-<role>` - Add an explicit role suffix after human approval. |
| legacy | `forgesentinel` | `forgesentinel` | `cloud-systems/forgesentinel` | Cloud Runtime Plane | none | `neuroforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `rake` | `rake` | `cloud-systems/rake` | Cloud Runtime Plane | doc/system, CI | `neuroforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `forge-contract-core` | `forge_contract_core` | `contracts/forge-contract-core` | Doctrine Plane | SYSTEM, doc/system | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `forge_lineage` | `forge_lineage` | `contracts/forge_lineage` | Doctrine Plane | none | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `failureforge` | `failureforge` | `failureforge` | Doctrine Plane | doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `forge-smithy` | `forge-smithy` | `forge-smithy` | Doctrine Plane | SYSTEM, doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `ForgeImages` | `forgeimages` | `local-systems/ForgeImages` | Local Runtime Plane | SYSTEM, doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `ForgeMath` | `forgemath` | `local-systems/ForgeMath` | Local Runtime Plane | doc/system, CI | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `context-runtime` | `context-runtime` | `local-systems/context-runtime` | Local Runtime Plane | doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `cortex` | `COR` | `local-systems/cortex` | Local Runtime Plane | SYSTEM, doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `dataforge-Local` | `dataforge-Local` | `local-systems/dataforge-Local` | Data Plane | doc/system | `dataforge-local` - Mechanical local/GitHub rename may be enough, but still requires rename-policy approval. |
| legacy | `eval-cal-node` | `eval-cal-node` | `local-systems/eval-cal-node` | Local Runtime Plane | doc/system, CI | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `fa-local-operator` | `fa-local-operator` | `local-systems/fa-local-operator` | Local Runtime Plane | doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `repo` | `forge-eval` | `local-systems/forge-eval/repo` | Local Runtime Plane | doc/system, CI | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `forge-local-systems-runtime` | `forge-local-systems-runtime` | `local-systems/forge-local-systems-runtime` | Local Runtime Plane | SYSTEM, doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `forge-smithy` | `forge-smithy` | `local-systems/forge-smithy` | Local Runtime Plane | SYSTEM, doc/system, CI | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `forgeHQ` | `forgeHQ` | `local-systems/forgeHQ` | Local Runtime Plane | SYSTEM, doc/system | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| compliant | `neuronforge-local-operator` | `neuronforge-local-operator` | `local-systems/neuronforge-local-operator` | Local Runtime Plane | doc/system | `neuronforge-local-operator` - No rename needed. |
| legacy | `yellowjacket` | `yellowjacket` | `local-systems/yellowjacket` | Local Runtime Plane | none | `neuronforge-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `pact` | `PACT` | `pact` | Doctrine Plane | doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `precomputed-context-core` | `precomputed-context-core` | `precomputed-context-core` | Doctrine Plane | doc/system | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `rak-adatsik` | `rak-adatsik` | `rak-adatsik` | Doctrine Plane | none | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| invalid | `smithy` | `Smithy` | `smithy` | Doctrine Plane | SYSTEM, doc/system, CI | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `tarcie` | `tarcie` | `tarcie` | Doctrine Plane | SYSTEM, doc/system | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `yellowjacket` | `yellowjacket` | `yellowjacket` | Doctrine Plane | none | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |
| legacy | `zfss` | `zfss` | `zfss` | Doctrine Plane | SYSTEM, doc/system | `bds-<approved-role>` - Classify authority, approve a canonical BDS name, then update references. |

## Non-Compliant Repositories

### `.`

- Current name: `ecosystem`
- Origin repository: `forge`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `DoppelCore`

- Current name: `DoppelCore`
- Origin repository: `DoppelCore`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `ERA`

- Current name: `ERA`
- Origin repository: `ERA`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `Forge_Command`

- Current name: `Forge_Command`
- Origin repository: `Forge_Command`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `forge-command`
- Candidate: `forge-command-<role>`
- Required action: Normalize casing/separators and add an approved role suffix.

### `canebrake_press`

- Current name: `canebrake_press`
- Origin repository: `canebrake_press`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `checkly`

- Current name: `checkly`
- Origin repository: `none`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `unverified-repo`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `cloud-systems/DataForge`

- Current name: `DataForge`
- Origin repository: `DataForge`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `dataforge`
- Candidate: `dataforge-<role>`
- Required action: Normalize casing/separators and add an approved role suffix.

### `cloud-systems/ForgeAgents`

- Current name: `ForgeAgents`
- Origin repository: `Forge-Agents`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `forge-command`
- Candidate: `forge-command-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `cloud-systems/NeuroForge`

- Current name: `NeuroForge`
- Origin repository: `NeuroForge`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `neuroforge`
- Candidate: `neuroforge-<role>`
- Required action: Normalize casing/separators and add an approved role suffix.

### `cloud-systems/forgecustomer`

- Current name: `forgecustomer`
- Origin repository: `forgecustomer`
- Status: `reserved`
- Reason: local checkout: uses a reserved canonical prefix without a role suffix; origin repository: uses a reserved canonical prefix without a role suffix
- Local name status: `reserved`
- Origin name status: `reserved`
- Preferred prefix: `forgecustomer`
- Candidate: `forgecustomer-<role>`
- Required action: Add an explicit role suffix after human approval.

### `cloud-systems/forgesentinel`

- Current name: `forgesentinel`
- Origin repository: `forgesentinel`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuroforge`
- Candidate: `neuroforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `cloud-systems/rake`

- Current name: `rake`
- Origin repository: `rake`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuroforge`
- Candidate: `neuroforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `contracts/forge-contract-core`

- Current name: `forge-contract-core`
- Origin repository: `forge_contract_core`
- Status: `invalid`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: fails lowercase kebab-case validation regex
- Local name status: `legacy`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `contracts/forge_lineage`

- Current name: `forge_lineage`
- Origin repository: `forge_lineage`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `failureforge`

- Current name: `failureforge`
- Origin repository: `failureforge`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `forge-smithy`

- Current name: `forge-smithy`
- Origin repository: `forge-smithy`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/ForgeImages`

- Current name: `ForgeImages`
- Origin repository: `forgeimages`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `invalid`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/ForgeMath`

- Current name: `ForgeMath`
- Origin repository: `forgemath`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `invalid`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/context-runtime`

- Current name: `context-runtime`
- Origin repository: `context-runtime`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/cortex`

- Current name: `cortex`
- Origin repository: `COR`
- Status: `invalid`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: fails lowercase kebab-case validation regex
- Local name status: `legacy`
- Origin name status: `invalid`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/dataforge-Local`

- Current name: `dataforge-Local`
- Origin repository: `dataforge-Local`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `dataforge`
- Candidate: `dataforge-local`
- Required action: Mechanical local/GitHub rename may be enough, but still requires rename-policy approval.

### `local-systems/eval-cal-node`

- Current name: `eval-cal-node`
- Origin repository: `eval-cal-node`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/fa-local-operator`

- Current name: `fa-local-operator`
- Origin repository: `fa-local-operator`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/forge-eval/repo`

- Current name: `repo`
- Origin repository: `forge-eval`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/forge-local-systems-runtime`

- Current name: `forge-local-systems-runtime`
- Origin repository: `forge-local-systems-runtime`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/forge-smithy`

- Current name: `forge-smithy`
- Origin repository: `forge-smithy`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/forgeHQ`

- Current name: `forgeHQ`
- Origin repository: `forgeHQ`
- Status: `invalid`
- Reason: local checkout: fails lowercase kebab-case validation regex; origin repository: fails lowercase kebab-case validation regex
- Local name status: `invalid`
- Origin name status: `invalid`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `local-systems/yellowjacket`

- Current name: `yellowjacket`
- Origin repository: `yellowjacket`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `neuronforge`
- Candidate: `neuronforge-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `pact`

- Current name: `pact`
- Origin repository: `PACT`
- Status: `invalid`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: fails lowercase kebab-case validation regex
- Local name status: `legacy`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `precomputed-context-core`

- Current name: `precomputed-context-core`
- Origin repository: `precomputed-context-core`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `rak-adatsik`

- Current name: `rak-adatsik`
- Origin repository: `rak-adatsik`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `smithy`

- Current name: `smithy`
- Origin repository: `Smithy`
- Status: `invalid`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: fails lowercase kebab-case validation regex
- Local name status: `legacy`
- Origin name status: `invalid`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `tarcie`

- Current name: `tarcie`
- Origin repository: `tarcie`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `yellowjacket`

- Current name: `yellowjacket`
- Origin repository: `yellowjacket`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.

### `zfss`

- Current name: `zfss`
- Origin repository: `zfss`
- Status: `legacy`
- Reason: local checkout: valid lowercase kebab-case but not a preferred BDS pattern; origin repository: valid lowercase kebab-case but not a preferred BDS pattern
- Local name status: `legacy`
- Origin name status: `legacy`
- Preferred prefix: `bds`
- Candidate: `bds-<approved-role>`
- Required action: Classify authority, approve a canonical BDS name, then update references.
