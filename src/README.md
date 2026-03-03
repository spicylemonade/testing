# GCD Algorithm Research — Source Code

A combined branchless binary GCD algorithm with modular reduction and lookup table acceleration, achieving 12-65% speedup over standard implementations for 64-bit integers.

## Directory Structure

```
src/
  baselines/
    gcd_baselines.h       # 4 baseline algorithms (Euclidean, Stein's, Binary+CTZ, Binary+Opt)
    test_correctness.cpp   # Correctness test suite (96,480 test cases)
    asm_analysis.cpp       # Assembly generation for inner loop analysis
  novel/
    combined_gcd.h         # THE WINNER: combined algorithm (initial mod + LUT + branchless)
    branchless_gcd.h       # Branchless variants (hybrid, fixed, unrolled)
    lut_gcd.h              # 64KB lookup table for small operands
    divstep_gcd.h          # Bernstein-Yang divstep (negative result — 3.6x slower)
    test_novel.cpp         # Novel algorithm correctness + performance tests
  bench/
    benchmark.cpp          # Initial baseline benchmark
    full_benchmark.cpp     # Full comparative benchmark (summary statistics CSV)
    raw_benchmark.cpp      # Per-trial raw data benchmark (for statistical analysis)
```

## Quick Start

```bash
# Build everything
make all

# Run correctness tests
make test

# Run full benchmark suite and generate results
make reproduce

# Just build and run the full benchmark
make full_benchmark
```

## Prerequisites

- **Compiler**: GCC 12+ with C++20 support
- **CPU**: x86-64 with BMI2 (TZCNT, SHRX) — any Intel Haswell+ or AMD Zen+
- **Python** (optional, for figures/stats): Python 3 with matplotlib, seaborn, scipy, pandas, numpy

## Using the Algorithm

The combined GCD is a single-header library:

```cpp
#include "src/novel/combined_gcd.h"

uint64_t result = gcd_novel::gcd_combined(a, b);

// 128-bit version
unsigned __int128 result128 = gcd_novel::gcd_combined_128(a128, b128);
```

## Reproduction

To reproduce all benchmark results:

```bash
make reproduce
```

This will:
1. Run correctness tests (96,480 test cases)
2. Run full benchmark (10 algorithms × 5 distributions × 2 bit-widths)
3. Run raw trial data collection (50 trials for statistical analysis)
4. Generate statistical analysis (bootstrap CIs, Wilcoxon tests)
5. Generate publication-quality figures

Results are written to `results/phase4/` and `figures/`.
