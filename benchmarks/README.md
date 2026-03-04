# Benchmark Framework

## Measurement Methodology

- **Timing:** `clock_gettime(CLOCK_MONOTONIC)` for wall-clock nanoseconds. `rdtsc` (x86) or `cntvct_el0` (ARM) for cycle-accurate measurements.
- **Iterations:** 10000 for small payloads (<64KB), 1000 for medium (64KB-1MB), 100 for large (>1MB).
- **Warmup:** 10% of iteration count before measurement begins.
- **Statistics:** Sorted timings; report median, p95, p99 latency.
- **Throughput:** `input_bytes / median_nanoseconds` = GB/s.

## Payload Sizes

| Size | Bytes | Cache Level |
|------|-------|-------------|
| 64B | 64 | L1 |
| 256B | 256 | L1 |
| 1KB | 1,024 | L1 |
| 4KB | 4,096 | L1 |
| 16KB | 16,384 | L1/L2 boundary |
| 64KB | 65,536 | L2 |
| 256KB | 262,144 | L2/L3 boundary |
| 1MB | 1,048,576 | L3 |
| 10MB | 10,485,760 | Main memory |

## Reproducibility Setup

### Pin to single core (Linux):
```bash
taskset -c 0 ./build/bench_base64
```

### Disable turbo boost (Intel):
```bash
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
# Or for older kernels:
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

### Disable turbo boost (AMD):
```bash
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

### Set performance governor:
```bash
sudo cpupower frequency-set -g performance
```

## Building

```bash
gcc -std=c99 -O3 -march=native -o build/bench_base64 benchmarks/bench_main.c src/scalar/base64_scalar.c -Isrc/common -lm
```

For specific ISA targets:
```bash
# AVX2 only
gcc -std=c99 -O3 -mavx2 -o build/bench_avx2 ...

# AVX-512 VBMI
gcc -std=c99 -O3 -mavx512bw -mavx512vbmi -o build/bench_avx512 ...
```

## Output Format

JSON output with per-decoder, per-payload-size results including:
- `input_bytes`, `output_bytes`
- `median_ns`, `p95_ns`, `p99_ns`
- `throughput_gbps`
- `iterations`
