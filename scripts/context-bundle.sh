#!/usr/bin/env bash
# BDS Documentation Protocol v1.0 — Ecosystem context-bundle.sh
# Generates a focused context bundle for AI sessions from the ecosystem-level SYSTEM.md.
#
# Usage:
#   ./scripts/context-bundle.sh              # Full bundle (all 15 chapters)
#   ./scripts/context-bundle.sh architecture # Architecture focus
#   ./scripts/context-bundle.sh backend      # Backend internals focus
#   ./scripts/context-bundle.sh frontend     # Design system + frontend focus
#   ./scripts/context-bundle.sh integration  # API + integration + schema + errors
#   ./scripts/context-bundle.sh testing      # Testing + handover
#   ./scripts/context-bundle.sh config       # Config + API layer
#   ./scripts/context-bundle.sh handover     # Overview + errors + testing + handover
#
# Minimum 3 presets required by BDS Protocol; we provide 8.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."
DOC_DIR="$ROOT/doc/system"
OUT="$ROOT/context-bundle.md"
PRESET="${1:-full}"

echo "Forge Ecosystem context-bundle.sh — preset: $PRESET"

write_header() {
  echo "# Forge Ecosystem — Context Bundle ($PRESET)" > "$OUT"
  echo "_Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ) | Preset: ${PRESET}_" >> "$OUT"
  echo "" >> "$OUT"
}

append_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    echo "" >> "$OUT"
    echo "---" >> "$OUT"
    echo "" >> "$OUT"
    cat "$file" >> "$OUT"
  else
    echo "Warning: $file not found, skipping" >&2
  fi
}

write_header

case "$PRESET" in
  full)
    # All 15 chapters
    for f in "$DOC_DIR"/[0-1][0-9]-*.md; do
      append_file "$f"
    done
    ;;

  architecture)
    # Overview + architecture + API + integration
    append_file "$DOC_DIR/01-overview-philosophy.md"
    append_file "$DOC_DIR/02-architecture.md"
    append_file "$DOC_DIR/08-api-layer.md"
    append_file "$DOC_DIR/10-ecosystem-integration.md"
    ;;

  backend)
    # Overview + backend internals + schema + AI integration + errors
    append_file "$DOC_DIR/01-overview-philosophy.md"
    append_file "$DOC_DIR/09-backend-internals.md"
    append_file "$DOC_DIR/11-database-schema.md"
    append_file "$DOC_DIR/12-ai-integration.md"
    append_file "$DOC_DIR/13-error-handling.md"
    ;;

  frontend)
    # Overview + design system + frontend
    append_file "$DOC_DIR/01-overview-philosophy.md"
    append_file "$DOC_DIR/06-design-system.md"
    append_file "$DOC_DIR/07-frontend.md"
    ;;

  integration)
    # Overview + API + integration + schema + errors
    append_file "$DOC_DIR/01-overview-philosophy.md"
    append_file "$DOC_DIR/08-api-layer.md"
    append_file "$DOC_DIR/10-ecosystem-integration.md"
    append_file "$DOC_DIR/11-database-schema.md"
    append_file "$DOC_DIR/13-error-handling.md"
    ;;

  testing)
    # Testing + handover
    append_file "$DOC_DIR/14-testing.md"
    append_file "$DOC_DIR/15-handover.md"
    ;;

  config)
    # Config/env + API layer
    append_file "$DOC_DIR/05-config-env.md"
    append_file "$DOC_DIR/08-api-layer.md"
    ;;

  handover)
    # Overview + errors + testing + handover
    append_file "$DOC_DIR/01-overview-philosophy.md"
    append_file "$DOC_DIR/13-error-handling.md"
    append_file "$DOC_DIR/14-testing.md"
    append_file "$DOC_DIR/15-handover.md"
    ;;

  *)
    echo "Unknown preset: $PRESET" >&2
    echo "Available presets: full, architecture, backend, frontend, integration, testing, config, handover" >&2
    exit 1
    ;;
esac

LINE_COUNT=$(wc -l < "$OUT")
echo ""
echo "Context bundle written: $OUT"
echo "  $LINE_COUNT lines | preset: $PRESET"
echo ""
echo "To use with Claude: copy $OUT content into your session."
