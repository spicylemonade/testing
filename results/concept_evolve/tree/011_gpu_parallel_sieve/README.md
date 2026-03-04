# 011: GPU Parallel Sieve

## Overview

The Collatz sieve computation is embarrassingly parallel, making it an ideal candidate for GPU acceleration. Each surviving residue class can be processed independently, and the sieve lookup table fits comfortably in GPU shared memory.

## Performance Targets

| Platform | Raw Throughput | With Sieve (2^32) | Effective Search Rate |
|----------|---------------|-------------------|----------------------|
| Intel i9 | 4e9 nums/sec | 99.2% eliminated | ~3e7 candidates/sec |
| RTX 4090 | 5e11 nums/sec | 99.2% eliminated | ~4e9 candidates/sec |
| Speedup | | | ~130x |

## Architecture

1. **Host**: Generate candidate blocks, manage sieve table
2. **Device**: Per-thread Collatz iteration on surviving candidates
3. **Reduction**: AtomicMax for delay record, path record, completeness record
4. **Communication**: Asynchronous result transfer, pipeline next block

## Implementation Backlog

1. [ ] Design CUDA kernel for shortcut Collatz iteration
2. [ ] Implement shared memory sieve lookup (2^16 fits in 64KB shared memory)
3. [ ] Add 128-bit integer support (using uint2 or custom)
4. [ ] Benchmark vs CPU baseline
5. [ ] Profile memory bandwidth and compute utilization
6. [ ] Optimize for coalesced memory access patterns
7. [ ] Add multi-GPU support for even higher throughput
