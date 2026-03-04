# Wider Vector Amortization Analysis

## Context

SIMD vector widths have quadrupled over the past decade: SSE (128-bit, 2001) → AVX2 (256-bit, 2013) → AVX-512 (512-bit, 2017). Each generation potentially doubles Base64 decode throughput. However, real-world scaling is complicated by:

1. **Cross-lane penalties**: Wider vectors make byte-level permutations more expensive (unless VPERMB is available)
2. **Frequency throttling**: Some Intel processors reduce clock speed when using AVX-512 (up to 20% on Skylake-X)
3. **Instruction availability**: Wider widths unlock new instructions (VPERMB at VBMI, VGF2P8AFFINEQB at GFNI) that fundamentally change the algorithm
4. **Diminishing returns**: At some width, decode becomes memory-bound rather than compute-bound

Muła and Lemire (2020) showed that AVX-512 VBMI achieves near-memcpy speed, suggesting we are close to the memory bandwidth limit for single-core decode.

## Key Insight

The scaling from 256 to 512 bits is super-linear for Base64 because AVX-512 VBMI provides VPERMB (full-width byte permutation in 1 instruction), which replaces a 3-instruction VPERMD+VPSHUFB+blend sequence on AVX2. The instruction count drops from ~14 to ~7 per vector, more than compensating for any frequency throttling.

## Implementation Backlog

- [ ] Implement identical decode algorithm at 4 vector widths (SSE4.2, AVX2, AVX-512BW, AVX-512VBMI)
- [ ] Benchmark on Sapphire Rapids (no throttling), Skylake-X (throttling), Zen4 (no throttling)
- [ ] Monitor actual CPU frequency during benchmark using rdtsc + rdmsr
- [ ] Plot throughput (GB/s) vs vector width with error bars
- [ ] Identify the crossover point where decode becomes memory-bound (expected: ~6-8 GB/s single-core)
- [ ] Project scaling to hypothetical 1024-bit vectors (SVE at 1024 bits on future ARM)
