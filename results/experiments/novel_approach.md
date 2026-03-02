# Novel Optimization: Vectorized Pairwise Force with Symmetric Pair Indexing

**Date**: 2026-03-02  
**Item**: item_015  
**Concept path**: `09_vectorized_computation -> 10_force_decomposition -> 05_barnes_hut_tree`

## Selected Approach: Vectorized Symmetric Pair Computation

From the concept cards NEWTONS_THIRD_EXPLOIT and SOA_STATE, combined with the walk path
through vectorized computation:

**Idea**: Replace the O(N^2) full pairwise computation with an O(N(N-1)/2) upper-triangle
computation using numpy advanced indexing. Instead of computing all N^2 displacement vectors
(including redundant pairs and self-interactions), pre-compute the upper-triangular pair
indices and vectorize only over those pairs.

**Why this is novel for our codebase**: Our current vectorized approach (`compute_forces_vectorized`)
computes the full N x N displacement matrix (including the wasted lower triangle and diagonal),
using O(N^2 * d) memory. The optimized approach:
1. Pre-computes pair indices (i, j) with j > i: N(N-1)/2 pairs
2. Vectorizes force computation over pairs only
3. Uses `np.add.at` for scatter-accumulation (applies Newton's third law)
4. Reduces memory from O(N^2 * d) to O(N(N-1)/2 * d) — exactly 2x savings

**Expected improvement**:
- ~2x speed improvement for force computation (compute each pair once)
- ~2x memory reduction (half the displacement vectors)
- Exact numerical equivalence with brute-force (no approximation)

## Implementation Plan

1. Create `src/forces_optimized.py` with `compute_forces_symmetric()`
2. Pre-compute pair indices using `np.triu_indices(N, k=1)`
3. Vectorize displacement, distance, and force computation over pairs
4. Use `np.add.at` for accumulating forces (handles Newton's third law)
5. Unit tests verifying exact equivalence with brute-force
6. Benchmark against brute-force and Barnes-Hut

## Rationale

This optimization is the "lowest-hanging fruit" identified by the concept tree:
- Zero algorithmic complexity (still O(N^2) but with half the constant)
- Zero approximation error (exact)
- Complements Barnes-Hut (useful for the N < 300 regime where tree overhead dominates)
- Demonstrates Newton's third law exploitation in vectorized code
