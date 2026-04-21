# Canvas 01 — Promotion Contract and Admission Model
**Date:** 2026-04-17  
**Time:** 10:32 PM America/New_York

## Purpose

Lock the cross-repo promotion contract so neuronforge/neuroforge and ForgeCommand consume a single governed truth instead of reinterpreting the proved PACT output.

---

## System rule

PACT is the upstream serialization authority for TOON wave-1.

That means PACT owns:
- allowed wave-1 packet classes
- requested profile names
- used profile names
- fallback rules
- strict success hash
- non-strict canonical digest definitions
- manifest version
- promotion packet contents

The downstream repos may:
- carry promoted evidence
- validate presence and compatibility
- display operator-facing summaries
- route or gate work using the promoted evidence

The downstream repos may not:
- redefine the TOON wave-1 rendering contract
- silently substitute different fallback rules
- recalculate admission truth differently from PACT
- present locally invented promotion state as canonical truth

---

## Promotion unit

The promotion unit for next-repo work is the **wave-1 promotion envelope**.

### Required fields

The envelope should include:

- `promotion_packet_version`
- `source_repo`
- `source_commit`
- `wave_manifest_path`
- `wave_manifest_hash`
- `strict_success_hash`
- `non_strict_canonical_digests`
- `allowed_packet_classes`
- `supported_requested_profiles`
- `supported_used_profiles`
- `fallback_reason_codes`
- `feature_flag_name`
- `admission_stage`
- `generated_at`

### Optional but recommended fields

- `operator_evidence_paths`
- `repo_gate_report_path`
- `promotion_notes`
- `source_schema_versions`

---

## Canonical ownership model

### PACT owns
- serialization profile semantics
- replay truth
- canonical success hash lock
- canonical non-strict digest lock
- promotion packet assembly
- manifest issuance

### neuronforge / NeuroForge own
- intake acceptance of promoted envelope
- carriage of packet-level connectivity identifiers
- run-level storage of promotion lineage
- model execution provenance linked to the promotion envelope
- bounded emission of consumer evidence

### ForgeCommand owns
- operator visualization
- approval state recording
- repo/comparison posture
- promotion readiness summary
- drift and mismatch surfacing

---

## Required cross-repo lineage fields

These fields must move intact through the next seam whenever applicable:

- `task_intent_id`
- `context_bundle_id`
- `context_bundle_hash`
- `promotion_manifest_hash`
- `promotion_packet_version`
- `serialization_profile_requested`
- `serialization_profile_used`
- `artifact_kind`
- `fallback_used`
- `fallback_reason`
- `strict_success_hash` when applicable
- `non_strict_canonical_digest` when applicable

Do not rename these casually once admission work begins.
If renaming is ever needed, do it through an explicit contract revision with version bump and compatibility plan.

---

## Admission classes

### Class A — strict admitted result
Used when:
- PACT strict success case matches the locked success hash
- profile usage is exactly the admitted wave-1 profile
- packet class is allowed

### Class B — non-strict admitted result
Used when:
- result is intentionally non-strict
- canonical projection matches the locked digest
- public outcome meaning remains compatible

### Class C — not admitted
Used when:
- manifest missing
- hash/digest mismatch
- unsupported packet class
- unsupported profile
- local repo produced output without a valid upstream promotion envelope

---

## Required operator states

Use explicit operator states, not vague language:

- `not_promoted`
- `promotion_loaded`
- `promotion_compatible`
- `promotion_mismatch`
- `promotion_blocked`
- `approved_for_local_use`
- `approved_for_cloud_use`
- `rolled_back`

---

## Initial architectural constraint

The next-repo seam must start as **promotion carriage first, behavioral change second**.

That means first proving:
1. manifest loads
2. compatibility is checked
3. lineage fields are preserved
4. operator evidence is emitted

Only after that should any repo start making runtime decisions conditioned on promotion state.
