"""Reference producer example: emit a source_drift_finding artifact.

THIS IS NOT PRODUCTION CODE. It is a boundary example to prevent interpretation drift.

A real producer (e.g. dataforge-Local) will:
1. Detect drift using its own detection mechanism.
2. Build the payload using admitted field names and enum values from forge_contract_core.
3. Compute the idempotency key using compute_idempotency_key().
4. Build the full envelope.
5. Sign it (signing not shown here — signing is system-specific).
6. Pass the full artifact through validate_artifact() before persisting or staging.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from forge_contract_core.enums import (
    Confidence,
    DriftClass,
    ImpactScope,
    PromotionClass,
    SensitivityClass,
    SourceScope,
    ValidationStatus,
    VisibilityClass,
)
from forge_contract_core.identity import compute_idempotency_key
from forge_contract_core.validators.artifact import validate_artifact


def build_source_drift_finding(
    system_id: str,
    drift_class: DriftClass,
    declared_truth_ref: str,
    observed_truth_ref: str,
    impact_scope: ImpactScope,
    confidence: Confidence,
    operator_summary: str,
    produced_by_system: str = "dataforge-Local",
    produced_by_component: str = "reference_producer_example",
) -> dict:
    """Build a valid source_drift_finding artifact envelope.

    Returns the artifact dict. The caller is responsible for signing before
    persisting or staging.
    """
    artifact_id = str(uuid.uuid4())
    lineage_root_id = artifact_id  # Root artifact: lineage_root_id == artifact_id
    artifact_family = "source_drift_finding"
    artifact_version = 1
    now = datetime.now(UTC).isoformat()

    idempotency_key = compute_idempotency_key(
        artifact_family, artifact_id, artifact_version, lineage_root_id
    )

    artifact = {
        "artifact_id": artifact_id,
        "artifact_family": artifact_family,
        "artifact_version": artifact_version,
        "produced_by_system": produced_by_system,
        "produced_by_component": produced_by_component,
        "source_scope": SourceScope.LOCAL,
        "lineage_root_id": lineage_root_id,
        "parent_artifact_id": None,
        "trace_id": f"trace-{artifact_id}",
        "idempotency_key": idempotency_key,
        "created_at": now,
        "recorded_at": now,
        "sensitivity_class": SensitivityClass.INTERNAL,
        "visibility_class": VisibilityClass.OPERATOR,
        "promotion_class": PromotionClass.PROMOTABLE,
        "validation_status": ValidationStatus.VALID,
        "signer_identity": f"{produced_by_system}/{produced_by_component}@proving-slice-v1",
        # signature: the real system must compute and set this
        "signature": "PLACEHOLDER_MUST_BE_SET_BY_REAL_SIGNER",
        "payload": {
            "system_id": system_id,
            "drift_class": drift_class,
            "declared_truth_ref": declared_truth_ref,
            "observed_truth_ref": observed_truth_ref,
            "impact_scope": impact_scope,
            "confidence": confidence,
            "operator_summary": operator_summary,
        },
    }

    # Validate before returning — real producers must validate before persisting
    validate_artifact(artifact, strict_idempotency=True)

    return artifact


if __name__ == "__main__":
    import json

    example = build_source_drift_finding(
        system_id="dataforge-Local",
        drift_class=DriftClass.SCHEMA_DRIFT,
        declared_truth_ref="source_drift_finding:example:v1",
        observed_truth_ref="runtime_state:dataforge-Local:example",
        impact_scope=ImpactScope.SERVICE,
        confidence=Confidence.HIGH,
        operator_summary="Reference example: schema drift detected.",
    )
    print(json.dumps(example, indent=2))
