#!/usr/bin/env bash
# forge-contract-core CI gate
#
# Canonical proving-slice gate runner. All participating repos must wire
# this script (or an equivalent call to `python -m forge_contract_core.gates.run_all`)
# into their CI pipelines. This repo also runs its full pytest suite and a
# bytecode syntax gate, with pycache writes routed outside the repo.
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
LOCAL_REPORT="$REPORT_DIR/local_tests_$(date +%Y%m%d_%H%M%S).xml"

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

# Route bytecode writes away from repo-local __pycache__ directories.
BYTECODE_CACHE_ROOT="${PYTHONPYCACHEPREFIX:-}"
if [[ -z "$BYTECODE_CACHE_ROOT" ]]; then
    BYTECODE_CACHE_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/forge-contract-core-pycache.XXXXXX")"
    trap 'rm -rf "$BYTECODE_CACHE_ROOT"' EXIT
fi

# ── Gate 1: canonical contract gate runner ───────────────────────────────────
echo "=== Gate 1: canonical contract gates ==="
PYTHONPYCACHEPREFIX="$BYTECODE_CACHE_ROOT" PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON" -m forge_contract_core.gates.run_all \
    --repo "forge-contract-core" \
    --report-out "$REPORT_FILE"

echo ""
# ── Gate 2: full pytest suite ────────────────────────────────────────────────
echo "=== Gate 2: local pytest suite ==="
cd "$SCRIPT_DIR"
PYTHONPYCACHEPREFIX="$BYTECODE_CACHE_ROOT" PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON" -m pytest tests \
    --junit-xml="$LOCAL_REPORT"

echo ""
# ── Gate 3: package/test bytecode compilation ────────────────────────────────
echo "=== Gate 3: package/test bytecode compile ==="
PYTHONPYCACHEPREFIX="$BYTECODE_CACHE_ROOT" PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON" -m compileall -q forge_contract_core tests

echo ""
echo "CI gate: PASSED"
echo "  evidence: $REPORT_FILE"
echo "  local test report: $LOCAL_REPORT"
echo "  bytecode cache prefix: $BYTECODE_CACHE_ROOT"
