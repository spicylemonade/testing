# ConceptEvolve Steering Notes

## Steering Direction 1: TZCNT-before-ABS Reordering (PRIORITIZED)

**Direction**: Optimize the scalar branchless binary GCD inner loop by reordering operations so that TZCNT computes on the raw signed difference (before absolute value), allowing TZCNT and ABS-via-CMOV to execute in parallel on separate execution ports.

**Informs rubric items**: item_005 (bottleneck analysis), item_007 (baseline implementation), item_012 (branchless inner loop)

**Why prioritized**: This is the lowest-risk, highest-impact optimization. It requires no new data structures or algorithmic changes -- just instruction reordering. The theoretical payoff is 1-2 cycles off the critical path, which at ~64 iterations per 64-bit GCD translates to a 15-30% latency reduction. It also provides the foundation for all other optimizations.

**Key insight**: TZCNT(x) == TZCNT(-x) == TZCNT(|x|) for all x != 0. Therefore, we can compute TZCNT on the raw (possibly negative) difference before computing the absolute value. This breaks the serial dependency: instead of SUB -> ABS -> TZCNT -> SARX, we get SUB -> {TZCNT || ABS} -> SARX (parallel execution of TZCNT and ABS).

## Steering Direction 2: LUT-Hybrid for Tail Elimination

**Direction**: Combine the branchless inner loop with a 64KB lookup table that terminates the algorithm in O(1) when both operands shrink below 256. This eliminates the ~8 most variable-length final iterations.

**Informs rubric items**: item_016 (LUT GCD), item_018 (combined algorithm), item_019 (benchmarks)

**Why second priority**: The LUT approach adds complexity (cache footprint) but addresses a real bottleneck: the tail iterations have the highest relative overhead because the operands are small and the loop overhead dominates. The 64KB table fits comfortably in L1 cache (which is typically 32-48KB per core, but the table is only accessed at the end, allowing L1 evictions to be amortized).

## Steering Direction 3: SIMD Batch GCD for Throughput

**Direction**: Implement AVX2 batch processing of 4 independent 64-bit GCD pairs simultaneously, using masked blend operations in place of scalar CMOV and emulated TZCNT via bit isolation.

**Informs rubric items**: item_013 (SIMD GCD), item_018 (combined algorithm), item_019 (benchmarks), item_021 (figures)

**Why third priority**: SIMD provides the clearest path to "strict outperformance" on throughput metrics, but it only applies when multiple independent GCD pairs are available. The lack of native SIMD TZCNT is a significant implementation challenge. This direction is the most novel but also the most likely to produce a negative result for single-pair latency.

## Summary

| Priority | Direction | Key Rubric Items | Risk | Expected Improvement |
|----------|-----------|------------------|------|---------------------|
| 1 (HIGH) | TZCNT-before-ABS reordering | 005, 007, 012 | Low | 15-30% latency |
| 2 (MED) | LUT-hybrid tail elimination | 016, 018, 019 | Medium | 8-12% additional |
| 3 (LOW) | SIMD batch throughput | 013, 018, 019 | High | 2-3x throughput (batch) |
