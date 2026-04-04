#!/usr/bin/env bash
# forge-contract-core CI gate
#
# Canonical proving-slice gate runner. All participating repos must wire
# this script (or an equivalent call to `python -m forge_contract_core.gates.run_all`)
# into their CI pipelines.
#
# Exit codes:
#   0 — all gates pass
#   1 — one or more gates failed
#
# Usage (from the forge-contract-core root):
#   bash ci_gate.sh
#
# Usage (from a participating repo, with CONTRACT_CORE_PATH set):
#   CONTRACT_CORE_PATH=/path/to/forge-contract-core bash ci_gate.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACT_CORE_PATH="${CONTRACT_CORE_PATH:-$SCRIPT_DIR}"
REPORT_DIR="$SCRIPT_DIR/reports"
REPORT_FILE="$REPORT_DIR/proving_slice_gate_$(date +%Y%m%d_%H%M%S).json"

echo "forge-contract-core CI gate"
echo "  contract core path: $CONTRACT_CORE_PATH"
echo ""

# Determine the Python executable — prefer the venv if present
PYTHON="$CONTRACT_CORE_PATH/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="python3"
fi

echo "  python: $PYTHON"
echo ""

mkdir -p "$REPORT_DIR"

# Run the canonical gate suite and emit a JSON evidence report
PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON" -m forge_contract_core.gates.run_all \
    --repo "forge-contract-core" \
    --report-out "$REPORT_FILE"

echo ""
echo "CI gate: PASSED"
echo "  evidence: $REPORT_FILE"
