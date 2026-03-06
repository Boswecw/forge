#!/usr/bin/env bash
set -euo pipefail

# Requires: ImageMagick (convert)
# Ubuntu: sudo apt-get install -y imagemagick
# macOS:  brew install imagemagick

if ! command -v convert >/dev/null 2>&1; then
  echo "ERROR: ImageMagick 'convert' not found. Install ImageMagick and re-run." >&2
  exit 1
fi

SVG_SOURCE="forge-brand/assets/anvil-seal.svg"
SVG_16="forge-brand/assets/anvil-seal-16px.svg"
SVG_TAGLINE="forge-brand/assets/anvil-seal-with-tagline.svg"

OUTPUT_DIR="forge-brand/assets/exports"
mkdir -p "$OUTPUT_DIR"

# Base mark exports (use simplified version for 16px)
convert -background none -density 300 "$SVG_16"     -resize 16x16     "$OUTPUT_DIR/anvil-seal_16.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 32x32     "$OUTPUT_DIR/anvil-seal_32.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 64x64     "$OUTPUT_DIR/anvil-seal_64.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 128x128   "$OUTPUT_DIR/anvil-seal_128.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 256x256   "$OUTPUT_DIR/anvil-seal_256.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 512x512   "$OUTPUT_DIR/anvil-seal_512.png"
convert -background none -density 300 "$SVG_SOURCE" -resize 1024x1024 "$OUTPUT_DIR/anvil-seal_1024.png"

# Dark background variants (light mark on dark bg)
convert -size 512x512 xc:"#0a0a0a" \
        \( -background none -density 300 "$SVG_SOURCE" -resize 512x512 -fill "#e0e0e0" -colorize 100 \) \
        -composite "$OUTPUT_DIR/anvil-seal-darkbg_512.png"

convert -size 1024x1024 xc:"#0a0a0a" \
        \( -background none -density 300 "$SVG_SOURCE" -resize 1024x1024 -fill "#e0e0e0" -colorize 100 \) \
        -composite "$OUTPUT_DIR/anvil-seal-darkbg_1024.png"

# Tagline exports (after text → paths conversion)
convert -background none -density 300 "$SVG_TAGLINE" -resize 400x96   "$OUTPUT_DIR/anvil-seal-tagline_400x96.png"
convert -background none -density 300 "$SVG_TAGLINE" -resize 800x192  "$OUTPUT_DIR/anvil-seal-tagline_800x192.png"
convert -background none -density 300 "$SVG_TAGLINE" -resize 1200x288 "$OUTPUT_DIR/anvil-seal-tagline_1200x288.png"

echo "✓ PNG exports complete in $OUTPUT_DIR/"
