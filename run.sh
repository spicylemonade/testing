#!/usr/bin/env bash
# Full pipeline: generate Euler bricks, search, analyze, and produce figures/report.
set -euo pipefail

echo "=== Perfect Cuboid Research Pipeline ==="
echo ""

# Step 1: Baseline search (brute-force with modular filter)
echo "[1/6] Running baseline brute-force search..."
python3 src/baseline_search.py

# Step 2: Triple decomposition search
echo "[2/6] Running triple decomposition search..."
python3 src/triple_decomposition.py

# Step 3: Combined search (all methods)
echo "[3/6] Running combined search..."
python3 src/combined_search.py

# Step 4: Near-miss statistical analysis
echo "[4/6] Running near-miss analysis..."
python3 src/near_miss_analysis.py

# Step 5: Generate publication figures
echo "[5/6] Generating figures..."
python3 src/generate_figures.py

# Step 6: Summary
echo "[6/6] Pipeline complete."
echo ""
echo "Results:"
ls -la results/*.md results/*.csv results/*.json 2>/dev/null || true
echo ""
echo "Figures:"
ls -la figures/*.png figures/*.pdf 2>/dev/null || true
echo ""
echo "Done. See results/research_report.md for the full report."
