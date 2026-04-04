"""Reference consumer example: receive and validate a promotion_receipt artifact.

THIS IS NOT PRODUCTION CODE. It is a boundary example to prevent interpretation drift.

A real consumer (e.g. dataforge-Local receiving a receipt from DataForge) will:
1. Receive the raw receipt artifact over its transport.
2. Validate it using validate_artifact().
3. Inspect intake_outcome to determine accepted / rejected / duplicate_reconciled.
4. Update its local queue state accordingly (never write lifecycle truth from the read model).
5. Never blur accepted and duplicate_reconciled outcomes.
"""

from __future__ import annotations

import json
from typing import Any

from forge_contract_core.enums import IntakeOutcome
from forge_contract_core.validators.artifact import ArtifactValidationError, validate_artifact


class ReceiptProcessingError(Exception):
    """Raised when a received promotion_receipt cannot be processed."""


def receive_promotion_receipt(raw_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate and process an inbound promotion_receipt artifact.

    Returns a structured outcome dict. Raises ReceiptProcessingError if the
    artifact is invalid or the outcome is ambiguous.
    """
    # Step 1: validate the full artifact
    try:
        validate_artifact(raw_artifact, strict_idempotency=False)
    except ArtifactValidationError as exc:
        raise ReceiptProcessingError(f"Invalid promotion_receipt: {exc}") from exc

    payload = raw_artifact["payload"]
    intake_outcome = payload["intake_outcome"]

    # Step 2: map to explicit outcome — never blur accepted and duplicate_reconciled
    if intake_outcome == IntakeOutcome.ACCEPTED:
        return {
            "outcome": IntakeOutcome.ACCEPTED,
            "shared_record_ref": payload["shared_record_ref"],
            "receipt_id": payload["receipt_id"],
            "received_at": payload["received_at"],
            "idempotency_key": payload["idempotency_key"],
            "summary": payload["outcome_summary"],
            "action": "mark_queue_item_accepted",
        }
    elif intake_outcome == IntakeOutcome.REJECTED:
        return {
            "outcome": IntakeOutcome.REJECTED,
            "rejection_class": payload.get("rejection_class"),
            "retry_allowed": payload.get("retry_allowed", False),
            "receipt_id": payload["receipt_id"],
            "received_at": payload["received_at"],
            "idempotency_key": payload["idempotency_key"],
            "summary": payload["outcome_summary"],
            "action": "mark_queue_item_rejected" if not payload.get("retry_allowed") else "mark_queue_item_retryable",
        }
    elif intake_outcome == IntakeOutcome.DUPLICATE_RECONCILED:
        # Duplicate: item was already accepted. Link to existing shared record.
        return {
            "outcome": IntakeOutcome.DUPLICATE_RECONCILED,
            "shared_record_ref": payload["shared_record_ref"],
            "receipt_id": payload["receipt_id"],
            "received_at": payload["received_at"],
            "idempotency_key": payload["idempotency_key"],
            "summary": payload["outcome_summary"],
            "action": "mark_queue_item_accepted_via_duplicate_reconciliation",
        }
    else:
        raise ReceiptProcessingError(
            f"Unrecognized intake_outcome: {intake_outcome!r}. "
            f"Must be one of: {[o.value for o in IntakeOutcome]}"
        )


if __name__ == "__main__":
    # Load a valid receipt fixture to demonstrate consumption
    import pathlib
    fixture_path = (
        pathlib.Path(__file__).parent.parent.parent
        / "fixtures" / "valid" / "promotion_receipt.v1.valid.json"
    )
    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    raw_clean = {k: v for k, v in raw.items() if not k.startswith("_")}

    result = receive_promotion_receipt(raw_clean)
    print(json.dumps(result, indent=2))
