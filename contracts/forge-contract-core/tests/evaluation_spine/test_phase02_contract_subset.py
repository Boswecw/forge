"""Evaluation Spine phase 02 contract subset tests."""

from __future__ import annotations

import pytest

from forge_contract_core.enums import ADMITTED_FAMILIES, ADMITTED_VERSIONS
from forge_contract_core.validators.families import FamilyValidationError, validate_family_payload
from forge_contract_core.validators.role_matrix import check_producer_admitted


SHA = "sha256:" + ("a" * 64)

REFS = {
    "forge_eval_evidence_bundle": "forge_eval_evidence_bundle:11111111-1111-1111-1111-111111111111:v1",
    "eval_calibration_report": "eval_calibration_report:22222222-2222-2222-2222-222222222222:v1",
    "forgemath_lane_evaluation_ref": "forgemath_lane_evaluation_ref:33333333-3333-3333-3333-333333333333:v1",
    "forgehq_upstream_evidence_refs": "forgehq_upstream_evidence_refs:44444444-4444-4444-4444-444444444444:v1",
}


def test_phase02_families_are_admitted_v1() -> None:
    expected = {
        "forge_eval_evidence_bundle",
        "eval_calibration_report",
        "forgemath_lane_evaluation_ref",
        "forgehq_upstream_evidence_refs",
        "evaluation_spine_detail_model",
    }

    assert expected.issubset(ADMITTED_FAMILIES)

    for family in expected:
        assert ADMITTED_VERSIONS[family] == frozenset({1})


def test_valid_forge_eval_evidence_bundle_payload_passes() -> None:
    validate_family_payload(
        "forge_eval_evidence_bundle",
        1,
        {
            "schema_version": "forge_eval.evidence_bundle.v1",
            "forge_eval_run_id": "run-phase02-001",
            "source_projection_id": "centipede-projection-001",
            "source_fused_bundle_id": "centipede-fused-bundle-001",
            "repository_id": "Forge_Command",
            "base_ref": "base-sha",
            "head_ref": "head-sha",
            "artifact_refs": [
                {
                    "artifact_kind": "risk_heatmap",
                    "artifact_path": "risk_heatmap.json",
                    "artifact_hash": SHA,
                },
                {
                    "artifact_kind": "context_slices",
                    "artifact_path": "context_slices.json",
                    "artifact_hash": SHA,
                },
            ],
            "deterministic": True,
            "validation_state": "passed",
        },
    )


def test_valid_eval_calibration_report_payload_passes() -> None:
    validate_family_payload(
        "eval_calibration_report",
        1,
        {
            "schema_version": "eval_cal_node.calibration_report.v1",
            "calibration_report_id": "cal-report-001",
            "source_forge_eval_evidence_bundle_ref": REFS["forge_eval_evidence_bundle"],
            "source_artifact_hash": SHA,
            "repository_id": "Forge_Command",
            "score_normalization_version": "phase02.v1",
            "calibrated_scores": [
                {
                    "metric_name": "risk_heatmap_pressure",
                    "raw_score": 17.0,
                    "calibrated_score": 0.72,
                    "weight": 0.50,
                },
                {
                    "metric_name": "context_slice_density",
                    "raw_score": 6.0,
                    "calibrated_score": 0.41,
                    "weight": 0.50,
                },
            ],
            "confidence_band_candidate": "medium_confidence",
            "threshold_crossings": [
                {
                    "threshold_id": "self_healing_candidate_confidence_v1.review",
                    "crossed": True,
                    "direction": "above",
                }
            ],
            "validation_state": "passed",
        },
    )


def test_valid_forgemath_lane_evaluation_ref_payload_passes() -> None:
    validate_family_payload(
        "forgemath_lane_evaluation_ref",
        1,
        {
            "schema_version": "forgemath.lane_evaluation_ref.v1",
            "lane_id": "self_healing_candidate_confidence_v1",
            "lane_version": 1,
            "source_eval_calibration_report_ref": REFS["eval_calibration_report"],
            "source_artifact_hash": SHA,
            "canonical_evaluation_ref": "forgemath://lanes/self_healing_candidate_confidence_v1/evaluations/phase02-001",
            "canonical_score_ref": "forgemath://scores/phase02-001",
            "threshold_decision_ref": "forgemath://threshold-decisions/phase02-001",
            "proposal_candidate_allowed": True,
            "rollback_required": False,
            "non_recalculation_notice": "Downstream systems must reference this ForgeMath result and must not recalculate canonical confidence, band, threshold, proposal allowance, or rollback decision.",
        },
    )


def test_valid_forgehq_upstream_evidence_refs_payload_passes() -> None:
    validate_family_payload(
        "forgehq_upstream_evidence_refs",
        1,
        {
            "schema_version": "forgehq.upstream_evidence_refs.v1",
            "forgehq_evidence_ref_id": "forgehq-upstream-001",
            "source_forge_eval_evidence_bundle_ref": REFS["forge_eval_evidence_bundle"],
            "source_eval_calibration_report_ref": REFS["eval_calibration_report"],
            "source_forgemath_lane_evaluation_ref": REFS["forgemath_lane_evaluation_ref"],
            "upstream_artifact_hashes": [
                {
                    "artifact_family": "forge_eval_evidence_bundle",
                    "artifact_ref": REFS["forge_eval_evidence_bundle"],
                    "artifact_hash": SHA,
                },
                {
                    "artifact_family": "eval_calibration_report",
                    "artifact_ref": REFS["eval_calibration_report"],
                    "artifact_hash": SHA,
                },
                {
                    "artifact_family": "forgemath_lane_evaluation_ref",
                    "artifact_ref": REFS["forgemath_lane_evaluation_ref"],
                    "artifact_hash": SHA,
                },
            ],
            "non_authoritative_notice": "ForgeHQ may reference upstream evidence for proposal shaping but is not mathematical authority and is not operator decision authority.",
        },
    )


def test_valid_evaluation_spine_detail_model_payload_passes() -> None:
    validate_family_payload(
        "evaluation_spine_detail_model",
        1,
        {
            "schema_version": "forgecommand.evaluation_spine_detail_model.v1",
            "detail_model_id": "detail-001",
            "repository_id": "Forge_Command",
            "forge_eval_evidence_bundle_ref": REFS["forge_eval_evidence_bundle"],
            "eval_calibration_report_ref": REFS["eval_calibration_report"],
            "forgemath_lane_evaluation_ref": REFS["forgemath_lane_evaluation_ref"],
            "forgehq_upstream_evidence_refs_ref": REFS["forgehq_upstream_evidence_refs"],
            "display_layers": [
                "centipede_evidence",
                "forge_eval_artifacts",
                "eval_calibration",
                "forgemath_canonical_result",
                "forgehq_proposal",
                "operator_action",
            ],
            "operator_action_available": True,
            "operator_decision_ref": None,
            "read_model_hash": SHA,
        },
    )


def test_forgehq_upstream_refs_requires_non_authoritative_notice() -> None:
    payload = {
        "schema_version": "forgehq.upstream_evidence_refs.v1",
        "forgehq_evidence_ref_id": "forgehq-upstream-001",
        "source_forge_eval_evidence_bundle_ref": REFS["forge_eval_evidence_bundle"],
        "source_eval_calibration_report_ref": REFS["eval_calibration_report"],
        "source_forgemath_lane_evaluation_ref": REFS["forgemath_lane_evaluation_ref"],
        "upstream_artifact_hashes": [
            {
                "artifact_family": "forge_eval_evidence_bundle",
                "artifact_ref": REFS["forge_eval_evidence_bundle"],
                "artifact_hash": SHA,
            }
        ],
    }

    with pytest.raises(FamilyValidationError):
        validate_family_payload("forgehq_upstream_evidence_refs", 1, payload)


def test_forgemath_lane_ref_rejects_wrong_lane_id() -> None:
    payload = {
        "schema_version": "forgemath.lane_evaluation_ref.v1",
        "lane_id": "not_the_canonical_lane",
        "lane_version": 1,
        "source_eval_calibration_report_ref": REFS["eval_calibration_report"],
        "source_artifact_hash": SHA,
        "canonical_evaluation_ref": "forgemath://lanes/other/evaluations/phase02-001",
        "canonical_score_ref": "forgemath://scores/phase02-001",
        "threshold_decision_ref": "forgemath://threshold-decisions/phase02-001",
        "proposal_candidate_allowed": True,
        "rollback_required": False,
    }

    with pytest.raises(FamilyValidationError):
        validate_family_payload("forgemath_lane_evaluation_ref", 1, payload)


def test_role_matrix_admits_phase02_producers() -> None:
    check_producer_admitted("forge-eval", "forge_eval_evidence_bundle")
    check_producer_admitted("eval-cal-node", "eval_calibration_report")
    check_producer_admitted("ForgeMath", "forgemath_lane_evaluation_ref")
    check_producer_admitted("forgeHQ", "forgehq_upstream_evidence_refs")
    check_producer_admitted("Forge_Command", "evaluation_spine_detail_model")
