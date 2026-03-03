# Optimization Strategy Selection

**Date:** 2026-03-03  
**Rubric Item:** item_014  
**Source:** concept_evolve probe on "N-body simulation performance bottleneck"

## Problem Statement

Our pure-Python Barnes-Hut implementation has O(N log N) algorithmic complexity but cannot outperform NumPy's vectorized O(N^2) for N < 5000 due to Python loop overhead in tree traversal. The per-body tree walk involves ~O(log N) Python function calls, each with ~1 microsecond overhead, while NumPy's vectorized operations execute the entire N^2 computation in optimized C/BLAS.

## Concept Cards from Probe

### 1. Morton-Ordered Interaction List Precomputation
Sort bodies by Morton (Z-order) code. Bodies nearby in physical space are nearby in memory. Precompute interaction lists for groups of bodies sharing the same tree path. Vectorize the actual force computation over these lists.

### 2. Hybrid Adaptive Depth-Switching
Use the tree only for far-field approximation. For leaves below a threshold size, switch to direct vectorized N^2 over bodies within the leaf and its neighbors. This reduces the number of Python-level tree walk steps.

### 3. Implicit Octree via Sorted Morton Codes ("Treeless Tree Code")
Replace the explicit tree with sorted Morton-coded indices. The tree structure is implicit in the sorted order. Range queries on Morton codes find neighbors without pointer chasing.

## Selected Approach

**Hybrid Adaptive Depth-Switching** — for the following reasons:

1. **Directly addresses the bottleneck:** The problem is Python loop overhead per tree node visit. By stopping tree recursion early (at a coarser level) and computing forces within groups using NumPy vectorized operations, we reduce the number of Python-level iterations from O(N * log N) to O(N * log(N/k) + k^2 * N/k) where k is the leaf group size.

2. **Implementation simplicity:** Requires only a minor modification to the existing tree code — add a threshold parameter for minimum leaf size, and batch all bodies within large leaves for vectorized computation.

3. **Literature support:** This approach is used in production N-body codes. Efstathiou et al. \cite{efstathiou1985} describe the PM-tree hybrid where particle-mesh handles long-range forces and direct summation handles short-range. The Abacus code \cite{garrison2021} uses a similar near-field/far-field split with vectorized near-field computation.

## Expected Impact

For N=500 with leaf group size k=20, we expect:
- ~25 leaf groups × vectorized k^2 = 400 computations each
- ~25 far-field tree approximations per group
- Total Python iterations: ~25*25 = 625 (vs 500*15 = 7500 for per-body tree walk)
- Expected speedup: ~10x over current pure-Python Barnes-Hut

## Deferred Approaches

- Morton-ordered interaction lists: more complex, similar benefit
- GNN surrogate: requires training infrastructure, orthogonal to this project
- Traversal splicing: requires SIMD intrinsics, not available in pure Python

## References

- \cite{efstathiou1985} Efstathiou et al. (1985). Near-field/far-field force splitting for N-body.
- \cite{garrison2021} Garrison et al. (2021). Abacus code: hybrid multipole + direct.
