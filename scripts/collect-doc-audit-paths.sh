#!/usr/bin/env bash
set -euo pipefail

BASE_SHA=""
HEAD_SHA="HEAD"
OUTPUT_PATH=""

usage() {
  cat <<'USAGE'
Usage: bash scripts/collect-doc-audit-paths.sh --output <path> [--base <sha>] [--head <sha>]

Collect changed file paths for doc-audit scoped mode.
- If --base is provided and not all-zero, diffs the range <base>..<head>.
- If --base is empty or all-zero, falls back to the single head commit.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_SHA="${2:-}"
      shift 2
      ;;
    --head)
      HEAD_SHA="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT_PATH="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "${OUTPUT_PATH}" ]]; then
  echo "--output is required" >&2
  usage >&2
  exit 2
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "collect-doc-audit-paths.sh must run inside a git repository" >&2
  exit 1
fi

OUTPUT_DIR="$(dirname "${OUTPUT_PATH}")"
mkdir -p "${OUTPUT_DIR}"

is_zero_sha() {
  [[ -n "$1" && "$1" =~ ^0+$ ]]
}

if [[ -n "${BASE_SHA}" ]] && ! is_zero_sha "${BASE_SHA}"; then
  MODE="range"
  git diff --name-only --diff-filter=ACDMRTUXB "${BASE_SHA}" "${HEAD_SHA}" | sort -u > "${OUTPUT_PATH}"
else
  MODE="single-commit"
  if git rev-parse --verify "${HEAD_SHA}^{commit}" >/dev/null 2>&1; then
    git diff-tree --no-commit-id --name-only -r --diff-filter=ACDMRTUXB "${HEAD_SHA}" | sort -u > "${OUTPUT_PATH}"
  else
    : > "${OUTPUT_PATH}"
  fi
fi

COUNT="$(wc -l < "${OUTPUT_PATH}")"
printf 'Collected %s changed paths (%s) into %s\n' "${COUNT}" "${MODE}" "${OUTPUT_PATH}"
