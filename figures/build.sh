#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT_DIR/figures/src"
BUILD_DIR="$ROOT_DIR/figures/build"
OUT_DIR="$ROOT_DIR/figures"

mkdir -p "$BUILD_DIR" "$OUT_DIR"

for tex in "$SRC_DIR"/*.tex; do
  base="$(basename "$tex" .tex)"
  if [[ "$base" == "style" ]]; then
    continue
  fi
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory "$BUILD_DIR" \
    "$tex" >/dev/null
  cp "$BUILD_DIR/$base.pdf" "$OUT_DIR/$base.pdf"
  mutool draw -q -F png -r 600 -o "$OUT_DIR/$base.png" "$OUT_DIR/$base.pdf" 1 >/dev/null
done
