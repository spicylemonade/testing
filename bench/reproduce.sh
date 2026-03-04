#!/bin/bash
# reproduce.sh - Full reproducibility script for the Fast DEFLATE project
#
# Builds everything from a clean checkout, runs all tests and benchmarks,
# and generates all figures and results.
#
# Requirements:
#   - GCC 12+ with -march=native support
#   - zlib development headers (zlib-dev / zlib1g-dev)
#   - git (for cloning third-party dependencies)
#   - Python 3 with matplotlib and numpy (for figures only)
#
# Usage:
#   bash bench/reproduce.sh [--skip-deps] [--skip-figures] [--iterations N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# Parse arguments
SKIP_DEPS=0
SKIP_FIGURES=0
ITERATIONS=100

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-deps) SKIP_DEPS=1; shift ;;
        --skip-figures) SKIP_FIGURES=1; shift ;;
        --iterations) ITERATIONS="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "============================================"
echo "  Fast DEFLATE Decompressor — Reproduction"
echo "============================================"
echo ""
echo "Project directory: $PROJECT_DIR"
echo "Iterations: $ITERATIONS"
echo ""

# ─────────────────────────────────────────────
# Step 1: Build third-party dependencies
# ─────────────────────────────────────────────
if [[ $SKIP_DEPS -eq 0 ]]; then
    echo ">>> Step 1: Building third-party dependencies..."

    mkdir -p third_party

    # zlib-ng
    if [[ ! -d third_party/zlib-ng ]]; then
        echo "    Cloning zlib-ng..."
        git clone --depth 1 https://github.com/zlib-ng/zlib-ng.git third_party/zlib-ng
    fi
    if [[ ! -f third_party/zlib-ng/libz.so ]] && [[ ! -f third_party/zlib-ng/libz.a ]]; then
        echo "    Building zlib-ng..."
        pushd third_party/zlib-ng > /dev/null
        ./configure --zlib-compat
        make -j"$(nproc)" 2>&1 | tail -3
        popd > /dev/null
    fi
    echo "    zlib-ng: OK"

    # libdeflate
    if [[ ! -d third_party/libdeflate ]]; then
        echo "    Cloning libdeflate..."
        git clone --depth 1 https://github.com/ebiggers/libdeflate.git third_party/libdeflate
    fi
    if [[ ! -f third_party/libdeflate/libdeflate.a ]]; then
        echo "    Building libdeflate..."
        pushd third_party/libdeflate > /dev/null
        make -j"$(nproc)" 2>&1 | tail -3
        popd > /dev/null
    fi
    echo "    libdeflate: OK"
    echo ""
else
    echo ">>> Step 1: Skipping dependency build (--skip-deps)"
    echo ""
fi

# ─────────────────────────────────────────────
# Step 2: Build project
# ─────────────────────────────────────────────
echo ">>> Step 2: Building project..."

# Test binaries
echo "    Building test_correctness..."
gcc -O3 -march=native -std=c11 -Wall -Wextra -g -Iinclude \
    -o test_correctness tests/test_correctness.c src/naive_inflate.c -lz

echo "    Building test_fast..."
gcc -O3 -march=native -std=c11 -Wall -Wextra -g -Iinclude \
    -o test_fast tests/test_fast.c src/fast_decode.c -lz

echo "    Building test_adversarial..."
gcc -O3 -march=native -std=c11 -Wall -Wextra -g -Iinclude \
    -o test_adversarial tests/test_adversarial.c src/fast_decode.c -lz

echo "    Building test_adversarial (ASAN)..."
gcc -O3 -march=native -std=c11 -Wall -Wextra \
    -fsanitize=address,undefined -fno-omit-frame-pointer \
    -Iinclude -o test_adversarial_asan tests/test_adversarial.c src/fast_decode.c -lz

# Benchmark binary
if [[ -f third_party/libdeflate/libdeflate.a ]]; then
    echo "    Building bench_harness..."
    gcc -O3 -march=native -std=c11 -Wall -Wextra -g \
        -Iinclude -Ithird_party/libdeflate \
        -o bench_harness bench/benchmark.c src/naive_inflate.c src/fast_decode.c \
        third_party/libdeflate/libdeflate.a \
        -lz -lm -ldl
else
    echo "    WARNING: libdeflate not built, skipping bench_harness"
fi

echo "    Build: OK"
echo ""

# ─────────────────────────────────────────────
# Step 3: Generate corpus (if not present)
# ─────────────────────────────────────────────
echo ">>> Step 3: Checking benchmark corpus..."
if [[ -d bench/corpus ]] && [[ $(find bench/corpus -name '*.z' 2>/dev/null | head -1) ]]; then
    CORPUS_COUNT=$(find bench/corpus -name '*.z' | wc -l)
    echo "    Corpus found: $CORPUS_COUNT compressed files"
else
    echo "    WARNING: Corpus not found in bench/corpus/"
    echo "    See bench/corpus/README.md for corpus generation instructions."
    echo "    Benchmarks will be skipped."
fi
echo ""

# ─────────────────────────────────────────────
# Step 4: Run tests
# ─────────────────────────────────────────────
echo ">>> Step 4: Running tests..."

echo "    test_correctness (naive decoder, 181 tests)..."
./test_correctness
echo ""

echo "    test_fast (fast decoder, 79 tests)..."
./test_fast
echo ""

echo "    test_adversarial (685 edge-case tests)..."
./test_adversarial
echo ""

echo "    test_adversarial ASAN/UBSAN..."
./test_adversarial_asan
echo ""

echo "    All tests: PASSED"
echo ""

# ─────────────────────────────────────────────
# Step 5: Run benchmarks
# ─────────────────────────────────────────────
if [[ -x ./bench_harness ]] && [[ -d bench/corpus ]]; then
    echo ">>> Step 5: Running benchmarks ($ITERATIONS iterations)..."
    mkdir -p results

    # Pin to CPU 0 if taskset available
    TASKSET=""
    if command -v taskset &> /dev/null; then
        TASKSET="taskset -c 0"
    fi

    $TASKSET ./bench_harness bench/corpus "$ITERATIONS" results/benchmark_reproduced.json
    echo "    Results written to results/benchmark_reproduced.json"
    echo ""
else
    echo ">>> Step 5: Skipping benchmarks (bench_harness or corpus not available)"
    echo ""
fi

# ─────────────────────────────────────────────
# Step 6: Generate figures
# ─────────────────────────────────────────────
if [[ $SKIP_FIGURES -eq 0 ]]; then
    echo ">>> Step 6: Generating figures..."
    if command -v python3 &> /dev/null && python3 -c "import matplotlib" 2>/dev/null; then
        python3 figures/generate_figures.py
        echo "    Figures generated in figures/"
    else
        echo "    WARNING: Python 3 with matplotlib not available; skipping figures"
    fi
    echo ""
else
    echo ">>> Step 6: Skipping figure generation (--skip-figures)"
    echo ""
fi

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
echo "============================================"
echo "  Reproduction complete!"
echo "============================================"
echo ""
echo "Artifacts:"
echo "  Tests:     test_correctness, test_fast, test_adversarial"
echo "  Benchmark: bench_harness"
echo "  Results:   results/benchmark_reproduced.json (if benchmarks ran)"
echo "  Figures:   figures/*.png, figures/*.pdf (if matplotlib available)"
echo "  Report:    results/technical_report.md"
echo ""
echo "Key files:"
echo "  src/fast_decode.c    — Optimized DEFLATE decoder"
echo "  include/bitreader.h  — 64-bit branchless bit reader"
echo "  sources.bib          — 24 BibTeX references"
