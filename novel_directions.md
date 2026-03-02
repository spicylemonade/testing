# Novel Algorithmic Directions for SSSP

## Synthesis of ConceptEvolve and Literature Analysis

This document identifies 3 concrete algorithmic ideas inspired by cross-domain analogies discovered through the ConceptEvolve framework.

## Direction 1: Epsilon-Scaling Multi-Scale SSSP

**Cross-domain insight:** From auction algorithms (Bertsekas 1992) and the ConceptEvolve forced bridge between epsilon-scaling and multi-scale distance computation.

**How it maps to SSSP:** Start with a coarse approximation of all distances (rounded to multiples of Δ). Use these as Johnson-style vertex potentials to reduce all edge weights to [0, Δ). Then run a simplified Dijkstra on the reduced-weight graph (since weights are small, a bucket-based PQ with O(Δ/β) buckets suffices). Halve Δ and repeat. After O(√(log n)) scales, distances are exact.

**Potential complexity improvement:** O(m · √(log n)) — matches Duan et al. 2026 with simpler algorithm structure. The key advantage is the direct connection to the well-studied epsilon-scaling framework, enabling transfer of optimization techniques.

**Feasibility:** HIGH — This is the core of our DAMS-SSSP algorithm. Implemented and tested successfully.

## Direction 2: Adaptive Mesh Refinement-Inspired Interval Decomposition

**Cross-domain insight:** From computational fluid dynamics (AMR) via the ConceptEvolve forced bridge between AMR and SSSP interval decomposition.

**How it maps to SSSP:** Instead of using fixed-width distance intervals (as in Duan et al.'s BMSSP), adaptively choose interval widths based on vertex density. Intervals with many vertices are split further; sparse intervals are processed directly. This reduces the total number of recursive calls.

**Potential complexity improvement:** Could reduce the constant factor in the O(m · log^{2/3} n) bound by a factor proportional to the "distance entropy" of the graph. For structured graphs (road networks, grids), the constant factor could be significantly smaller.

**Feasibility:** MEDIUM-HIGH — Requires an efficient density estimation step, but the basic idea is straightforward. Partially incorporated into DAMS-SSSP via the adaptive bucket width.

## Direction 3: Binned/Sketched Priority Queue for SSSP

**Cross-domain insight:** From streaming algorithms and data compression via the ConceptEvolve bridge between sketches and PQ overhead reduction, and between Huffman coding run-length and batch vertex processing.

**How it maps to SSSP:** Replace the comparison-based priority queue with a histogram-based structure. Maintain O(√n) bins covering the range of active distances. Each bin operation is O(1) (no comparisons needed — just compute the bin index via integer arithmetic on distances). Finding the minimum non-empty bin is O(1) amortized (scan forward from the last emptied bin).

**Potential complexity improvement:** Eliminates the O(log n) per-operation PQ overhead. Total PQ overhead becomes O(n + m) instead of O(n log n + m). The total algorithm complexity becomes dominated by edge relaxations: O(m × num_scales) = O(m · √(log n)).

**Feasibility:** HIGH — This is the BucketPQ data structure implemented in `src/datastructures/bucket_pq.py`. It achieves O(1) insert, O(1) decrease-key, and O(batch_size) extract-min-batch.
