# Fast DEFLATE Decompressor

A high-performance, RFC 1951-compliant DEFLATE decompressor written in portable C, targeting modern x86-64 hardware.

## Results Summary

| Decoder | Geomean Throughput (MB/s) | vs. System zlib |
|---------|--------------------------|-----------------|
| Naive baseline | 349 | 0.25x |
| System zlib 1.2.x | 1,380 | 1.00x |
| **Our fast decoder** | **2,307** | **1.67x** |
| **Our fast decoder + PGO** | **2,497** | **1.81x** |
| zlib-ng 2.x | 2,848 | 2.06x |
| libdeflate 1.x | 2,993 | 2.17x |

Measured on 20-file corpus × 3 compression levels, 100 iterations per data point. See [Technical Report](results/technical_report.md) for full analysis.

### Key Optimizations

1. **11-bit primary Huffman table** (8 KB) — fits entirely in L1 cache; 4.9x over naive
2. **Packed 32-bit table entries** with saved_bitbuf — eliminates 4 dependent array lookups; +32%
3. **Multi-literal decode** — up to 3 literals per bit-buffer refill; +5%
4. **64-bit branchless bit reader** — unaligned 8-byte loads, no refill branches
5. **SSE2/AVX2 SIMD match copy** — tiered by distance for overlapping-safe copies
6. **Pre-computed fixed Huffman tables** — zero overhead for BTYPE=01 blocks

## Building

### Requirements

- GCC 12+ (or compatible compiler with `-march=native` and SSE2/AVX2 support)
- zlib development headers (`zlib-dev` or `zlib1g-dev`)
- GNU Make
- Python 3 + matplotlib + numpy (for figure generation only)

### Quick Build

```bash
# Build tests
make test_fast
make test_correctness

# Run correctness tests
./test_correctness
./test_fast

# Build with third-party dependencies (for benchmarking)
make deps           # Clone zlib-ng and libdeflate
# Then manually build zlib-ng and libdeflate (see below)
make bench_harness  # Build benchmark harness
```

### Building Third-Party Dependencies

```bash
# zlib-ng (with zlib-compat mode)
cd third_party/zlib-ng
./configure --zlib-compat --prefix=$(pwd)/install
make -j$(nproc) && make install
cd ../..

# libdeflate
cd third_party/libdeflate
make -j$(nproc)
cd ../..
```

### Building with PGO

```bash
# Step 1: Instrumented build
gcc -O3 -march=native -std=c11 -fprofile-generate -Iinclude \
    -o bench_pgo bench/benchmark.c src/fast_decode.c src/naive_inflate.c \
    third_party/libdeflate/libdeflate.a -lz -lm -ldl

# Step 2: Run with corpus to generate profile data
./bench_pgo bench/corpus 10

# Step 3: Optimized build using profile
gcc -O3 -march=native -std=c11 -fprofile-use -Iinclude \
    -o fast_pgo bench/benchmark.c src/fast_decode.c src/naive_inflate.c \
    third_party/libdeflate/libdeflate.a -lz -lm -ldl
```

## Running Benchmarks

```bash
# Using the benchmark harness directly
./bench_harness bench/corpus 100 results/benchmark_output.json

# Using the wrapper script
bash bench/run_benchmarks.sh bench/corpus 100
```

The benchmark harness compares 5 decoders: naive, system zlib, zlib-ng (via dlopen), libdeflate, and our fast decoder. Output is JSON with per-file statistics (median, mean, p5, p95, stddev, min, max).

## Running Tests

```bash
# Correctness tests (naive decoder, 181 tests)
make test_correctness && ./test_correctness

# Fast decoder tests (79 tests)
make test_fast && ./test_fast

# Adversarial tests (685 tests)
gcc -O3 -march=native -std=c11 -Iinclude -o test_adversarial \
    tests/test_adversarial.c src/fast_decode.c -lz
./test_adversarial

# With AddressSanitizer
gcc -O3 -march=native -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer \
    -Iinclude -o test_adversarial_asan tests/test_adversarial.c src/fast_decode.c -lz
./test_adversarial_asan
```

## Project Structure

```
include/
  fast_deflate.h          # Public API
  bitreader.h             # 64-bit branchless bit reader (static inline)

src/
  fast_decode.c           # Optimized DEFLATE decoder (~870 lines)
  naive_inflate.c         # Reference decoder for correctness validation

tests/
  test_correctness.c      # 181 tests (naive decoder)
  test_fast.c             # 79 tests (fast decoder)
  test_adversarial.c      # 685 adversarial/edge-case tests

bench/
  benchmark.c             # 5-decoder comparison harness
  corpus/                 # 20 test files × 3 compression levels
  run_benchmarks.sh       # Benchmark runner script

results/
  technical_report.md     # Full research report (4600+ words)
  benchmark_final.json    # 100-iteration benchmark data
  ablation_study.json     # 6-stage optimization progression
  cross_arch_analysis.md  # x86-64 microarchitecture analysis
  prior_work_comparison.md # Comparison with libdeflate, zlib-ng, ISA-L

figures/
  throughput_comparison.png/pdf
  speedup_heatmap.png/pdf
  throughput_by_level.png/pdf
  ablation_chart.png/pdf

sources.bib               # 24 BibTeX references
```

## API

```c
#include "fast_deflate.h"

// Naive (reference) decoder
int fd_inflate(const uint8_t *src, size_t src_len,
               uint8_t *dst, size_t dst_len,
               size_t *out_len);

// Fast (optimized) decoder
int fd_inflate_fast(const uint8_t *src, size_t src_len,
                    uint8_t *dst, size_t dst_len,
                    size_t *out_len);

// Returns FD_OK (0) on success, FD_ERROR_* on failure
```

## Reproducibility

To reproduce all results from a clean checkout:

```bash
bash bench/reproduce.sh
```

This script builds all dependencies, compiles the project, runs tests, executes benchmarks, and generates figures. See the script for details.

## License

Research project. See individual source files for attribution.
