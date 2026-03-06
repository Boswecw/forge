# Contract Utilities

All `contracts/` modules are pure helpers that express deterministic validation and hashing for
`NodeEnvelope.v1` and `RunEvidence.v1`. The entry points are:

- `canonicalizeJson(value)` and `sha256Prefixed(bytes)` produce RFC 8785-style canonical bytes and `sha256:<hex>` digests.
- `validateNodeEnvelope(envelope)` / `finalizeNodeEnvelope(envelope)` enforce the envelope schema, fail-closed invariants, and compute `envelope_hash`.
- `validateRunEvidence(evidence)` / `finalizeRunEvidence(evidence)` enforce the run-evidence ledger and recompute `run_evidence_hash`.
- `verifyEnvelopeAgainstEvidence(envelope, evidence)` ties both artifacts together (including replay windows and hash cross-checks).

Controlled vocabularies live in `contracts/vocab.ts` and are referenced throughout validation helpers.

### Running the contract tests

Install dependencies if needed and then run:

```
npm run contracts:test
```

The test harness covers the gating rules, replay-window protection, and the canonical hash invariants documented in the spec.
