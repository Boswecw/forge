#!/usr/bin/env bash
# Assemble SYSTEM.md from doc/system/ section files.
# Run from repo root: bash doc/system/BUILD.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT="$REPO_ROOT/SYSTEM.md"

echo "# forge-contract-core — System Reference" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "> Assembled from \`doc/system/\`. Edit the section files, then run \`bash doc/system/BUILD.sh\`." >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "**Document version:** $(date -u +%Y-%m-%d)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "" >> "$OUTPUT"

for section in "$SCRIPT_DIR"/0*.md; do
    echo "" >> "$OUTPUT"
    cat "$section" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
done

echo "SYSTEM.md assembled at $OUTPUT"
