#!/bin/bash
# run_benchmarks.sh - Benchmark harness for fast DEFLATE decompressor
#
# Usage: ./bench/run_benchmarks.sh [corpus_dir] [iterations]
#
# Prerequisites:
#   - Build the project: make all
#   - Prepare corpus: see bench/corpus/README.md

set -euo pipefail

CORPUS_DIR="${1:-bench/corpus}"
ITERATIONS="${2:-100}"
RESULTS_FILE="results/baseline_results.json"

echo "=== Fast DEFLATE Benchmark Suite ==="
echo "Corpus directory: $CORPUS_DIR"
echo "Iterations: $ITERATIONS"
echo "Results file: $RESULTS_FILE"

# Disable frequency scaling if possible
if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
    echo "CPU governor: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)"
    echo "For best results, set to 'performance': echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
fi

# Pin to CPU 0 if taskset is available
TASKSET=""
if command -v taskset &> /dev/null; then
    TASKSET="taskset -c 0"
    echo "Pinning to CPU 0 via taskset"
fi

mkdir -p results

echo ""
echo "Running benchmarks..."
if [ -x ./bench_harness ]; then
    $TASKSET ./bench_harness "$CORPUS_DIR" "$ITERATIONS" "$RESULTS_FILE"
else
    echo "ERROR: bench_harness not built. Run 'make bench_harness' first."
    exit 1
fi

echo ""
echo "Done. Results in $RESULTS_FILE"
