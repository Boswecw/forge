# V1 Correction Fabric Process Diagrams

Date: 2026-04-22
Time: 2026-04-23 00:36 UTC

## Purpose

This document gives a Mermaid-safe view of the correction flow so the stack can be reviewed visually.

## 1. Full correction loop

```mermaid
flowchart LR
    A["Centipede / Registry / Other Evidence Sources"] --> B["DoppelCore: Truth-Core + Correction-Ready Artifacts"]
    B --> C["forgeHQ: Routing + Workflow"]
    C --> D["ForgeMath: Scoring + Weighting + Priority"]
    D --> E["forge-eval: Proposal Evaluation"]
    E --> F["eval-cal-node: Calibration + Threshold Stability"]
    F --> G["Self-Healing: Review + Approval + Tracking"]
    G --> H["FA-Local-Operator: Local Execution"]
    G --> I["ForgeAgents: Cloud Execution"]
    H --> J["Execution Receipts + Post-Change Evidence"]
    I --> J
    J --> K["Registry / DoppelCore / Self-Healing Updates"]
```

## 2. Evidence-to-proposal path

```mermaid
flowchart TD
    A["Findings + Evidence from Centipede / Registry"] --> B["DoppelCore"]
    B --> C["Correction Opportunity"]
    B --> D["Proof Obligations"]
    B --> E["Evaluation Packet"]
    C --> F["forgeHQ"]
    D --> G["forge-eval"]
    E --> G
    F --> H["Proposal Candidate"]
    G --> I["Evaluated Proposal"]
    I --> J["Self-Healing"]
```

## 3. Approval-to-execution split

```mermaid
flowchart TD
    A["Self-Healing Approved Proposal"] --> BExecution Domain
    B -->|Local| C["FA-Local-Operator"]
    B -->|Cloud| D["ForgeAgents"]
    C --> E["Local Execution Receipt"]
    D --> F["Cloud Execution Receipt"]
    E --> G["Post-Change Verification"]
    F --> G
    G --> H["DoppelCore / Registry / Self-Healing Refresh"]
```

## 4. Why the split matters

### Centipede is upstream evidence
Centipede should stop at:
- finding
- evidence
- contradiction preservation
- projection emission

### DoppelCore is truth and correction-readiness
DoppelCore should stop at:
- truth normalization
- mismatch formalization
- proof obligations
- correction-ready packets

### Correction fabric is proposal work
The correction-fabric stack should:
- route
- score
- evaluate
- calibrate

### Self-Healing is governance
Self-Healing should:
- review
- approve
- track
- hold posture
- hand off approved execution packets

### Execution lanes mutate state
Execution lanes should:
- execute bounded actions
- produce receipts
- feed verification back upstream
