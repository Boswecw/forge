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

# Run the canonical gate suite
PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON" -m forge_contract_core.gates.run_all

echo ""
echo "CI gate: PASSED"
