# Branch-Free Predicated Fixup for Base64

## Context

Branch misprediction is one of the most expensive penalties in modern CPUs: 15-20 wasted cycles on x86, 10-15 on ARM. For short Base64 inputs (JWT tokens, HTTP headers), the branch predictor has limited history, making mispredictions more likely. Even in the SIMD decode loop, a single branch (e.g., "if error detected, break") can cause mispredictions.

Branchless programming replaces all conditional jumps with predicated operations: compare → mask → select. On x86 SIMD, this is natural (PCMPEQ produces a mask, AND/BLEND select values). On ARM SVE, every instruction can be predicated.

## Key Insight

The Muła PSHUFB-bitmask lookup is already branchless for character-to-value mapping. The remaining branches are: (1) error check per iteration (can be deferred to end), (2) loop termination (unavoidable but predictable), and (3) padding handling (last 4 bytes only). By deferring error checks and handling padding outside the main loop, the hot loop becomes entirely branch-free.

## Implementation Backlog

- [ ] Audit existing implementations for remaining branches in the hot loop
- [ ] Replace per-iteration error check with OR-accumulated flag (deferred to end)
- [ ] Implement branchless padding detection for last 4 input bytes
- [ ] Benchmark on short inputs (16, 32, 64, 128, 256 bytes)
- [ ] Compare branch-miss rates between branching and branchless versions
- [ ] Test on ARM NEON and SVE where predication model differs from x86
- [ ] Verify constant-time behavior for security-sensitive applications (no timing side-channels)
