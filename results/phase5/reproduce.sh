#!/usr/bin/env bash
# reproduce.sh - Reproduce all computations for the Univalent Bloch Constant study
# Usage: bash results/phase5/reproduce.sh
# Requires: Python 3.10+, packages listed in requirements.txt
#
# This script re-runs all Phase 2-4 computations and regenerates figures.
# All Python scripts use deterministic seeds (42) for reproducibility.
# Expected runtime: ~10-15 minutes depending on hardware.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=============================================="
echo " Univalent Bloch Constant - Reproducibility"
echo "=============================================="
echo ""
echo "Repository root: $REPO_ROOT"
echo "Python: $(python3 --version 2>&1)"
echo ""

# Check dependencies
echo "[1/8] Checking dependencies..."
python3 -c "import numpy, scipy, matplotlib, seaborn; print('All dependencies available.')"
echo ""

# Phase 2: Core computations
echo "[2/8] Phase 2: Computing B_f for parametric families..."
python3 results/phase2/compute_Bf.py
echo ""

echo "[3/8] Phase 2: Running Skinner reproduction..."
python3 results/phase2/reproduce_skinner.py
echo ""

echo "[4/8] Phase 2: Running benchmark suite..."
python3 results/phase2/benchmark.py
echo ""

echo "[5/8] Phase 2: Computing upper bounds..."
python3 results/phase2/upper_bounds.py
echo ""

# Phase 3: Coefficient optimization
echo "[6/8] Phase 3: Running coefficient optimization..."
python3 results/phase3/coefficient_optimization.py
echo ""

# Phase 4: Optimization campaigns
echo "[7/8] Phase 4: Running optimization campaign (1500+ evaluations)..."
python3 results/phase4/optimization_campaign.py
echo ""

echo "[7b/8] Phase 4: Running slit mapping search (1200+ configurations)..."
python3 results/phase4/slit_mapping_search.py
echo ""

# Phase 4: Figures
echo "[8/8] Phase 4: Generating publication-quality figures..."
python3 results/phase4/generate_figures.py
echo ""

# Phase 5: Verification
echo "[VERIFY] Phase 5: Running independent verification..."
python3 results/phase5/verification.py
echo ""

echo "=============================================="
echo " Reproduction complete!"
echo "=============================================="
echo ""
echo "Key outputs:"
echo "  results/phase2/benchmark_results.json"
echo "  results/phase2/upper_bound_results.json"
echo "  results/phase3/coefficient_results.json"
echo "  results/phase4/optimization_results.json"
echo "  results/phase4/upper_bound_search.json"
echo "  results/phase5/verification_report.json"
echo "  figures/*.png, figures/*.pdf"
echo ""
echo "Final bounds: see results/phase5/final_bounds.json"
echo "Main report:  see results/phase5/main_report.md"
