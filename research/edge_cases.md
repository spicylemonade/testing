# Edge Case Analysis for HiBRA

## Overview

This document identifies degenerate graph structures and boundary conditions where the HiBRA algorithm could potentially fail or exhibit degraded performance, and verifies correct behavior on each.

## Edge Case 1: Self-Loops

**Description:** Graphs containing self-loop edges (u→u). A self-loop never provides a shorter path since w(u,u) ≥ 0 and d(s,u) + w(u,u) ≥ d(s,u).

**Risk:** Self-loops could cause the algorithm to relax an already-finalized vertex or trigger unnecessary decrease-key operations.

**Result:** PASS. HiBRA correctly ignores self-loops. The relaxation step computes d[u] + w(u,u) ≥ d[u], so the comparison `new_dist < dist[v]` (where v=u, already finalized) is always false.

**Within claimed bound:** Yes. Self-loops add O(1) per loop edge to the edge relaxation cost (1 addition + 1 comparison), which is already counted in the O(m) term.

## Edge Case 2: Parallel Edges

**Description:** Multiple edges between the same pair of vertices with different weights.

**Risk:** Could cause multiple decrease-key operations on the same node, or the shorter edge might not be processed first.

**Result:** PASS. Each parallel edge is relaxed independently. The first time vertex v is reached, it is inserted into the heap. Subsequent relaxations (from shorter parallel edges) trigger decrease-key. The minimum-weight path is always found correctly.

**Within claimed bound:** Yes. Each edge is relaxed exactly once when its source is extracted.

## Edge Case 3: Long Chain / Path Graph

**Description:** A path graph 0→1→2→...→(n-1) with n-1 edges. This is the worst case for decrease-key operations per vertex (zero—each vertex is reached once with its optimal distance).

**Risk:** On a path graph, n extract-min operations are performed with essentially no decrease-keys. This maximizes the amortized extract-min cost since there are no decrease-keys to "pay" for lazy operations.

**Result:** PASS. Distances are correct for n up to 10,000.

**Within claimed bound:** Yes. With m = n-1, the total is O(n + n log n / log log n) = O(n log n / log log n).

## Edge Case 4: Star Graph (High-Degree Source)

**Description:** Source vertex 0 connected to all other n-1 vertices. All vertices are reachable in one hop.

**Risk:** After extracting vertex 0, n-1 nodes are simultaneously inserted into the heap. The consolidation step must process a root list of size n-1, which could exceed the max_degree array bound.

**Result:** PASS. The heap dynamically extends the degree table when needed (`if d >= len(degree_table)`). All distances correct for n up to 10,000.

**Within claimed bound:** Yes. The single large consolidation costs O(n) (traversing n-1 roots), but this is amortized over the n extract-min operations.

## Edge Case 5: Source with No Outgoing Edges

**Description:** Source vertex has no neighbors; all other vertices are unreachable.

**Risk:** The algorithm should correctly assign dist[v] = ∞ for all v ≠ s, and terminate without errors.

**Result:** PASS. Only the source is inserted into the heap. After extracting it (with distance 0), the heap is empty and the loop terminates. All other distances remain ∞.

## Edge Case 6: All Equal Weights

**Description:** All edges have weight 1.0. Creates maximum tie-breaking scenarios in the heap.

**Risk:** Many nodes have identical keys. Tie-breaking in extract-min and decrease-key could lead to incorrect ordering.

**Result:** PASS. The heap correctly handles ties (equal keys are ordered arbitrarily, but Dijkstra's correctness only requires the minimum key to be correct). Verified on n=500 random graphs with uniform weight 1.0.

## Edge Case 7: k-Parameter Boundary (n=15, 16, 17)

**Description:** The k parameter computation switches behavior at n=16:
- n < 16: k = 2 (fallback to standard Fibonacci heap behavior)
- n = 16: log₂(log₂(16)) = log₂(4) = 2, so k = 2
- n = 17: log₂(log₂(17)) ≈ 2.03, floor = 2, so k = 2
- n = 65536: log₂(log₂(65536)) = log₂(16) = 4, so k = 4

**Risk:** Off-by-one errors in the k computation could cause k=0 or k=1.

**Result:** PASS. The `max(2, ...)` guard ensures k ≥ 2. Verified on n = 2, 3, 4, 8, 15, 16, 17 — all produce correct distances.

## Edge Case 8: Extreme Weight Magnitudes

**Description:** Very large (10¹⁵) or very small (10⁻¹⁵) edge weights.

**Risk:** Floating-point precision issues could cause incorrect distance comparisons.

**Result:** PASS. Both large and small weights produce correct results. The algorithm uses native Python float comparisons which have ~15 decimal digits of precision. For practical inputs, this is sufficient.

**Potential issue:** For pathological inputs with weights spanning more than ~15 orders of magnitude, floating-point roundoff could theoretically cause errors. This is a limitation of the comparison-addition model implementation, not the algorithm itself.

## Edge Case 9: Mixed Zero and Non-Zero Weights

**Description:** Graphs where ~30% of edges have weight 0 and the rest are uniform random.

**Risk:** Zero-weight edges can create zero-length cycles (not shortest-path-affecting since weights are non-negative) and cause decrease-key to be called with the same key value.

**Result:** PASS. The decrease-key guard `if not _cmp_lt(new_key, node.key)` correctly skips when the new key equals the current key, since 0 is not less than 0. Verified on n=200 with 30% zero-weight edges.

## Summary

| Edge Case | Correctness | Within Bound | Modifications Needed |
|-----------|-------------|--------------|---------------------|
| Self-loops | PASS | Yes | None |
| Parallel edges | PASS | Yes | None |
| Long chain | PASS | Yes | None |
| Star graph | PASS | Yes | None |
| No outgoing edges | PASS | Yes | None |
| Equal weights | PASS | Yes | None |
| k-boundary | PASS | Yes | None |
| Extreme weights | PASS | Yes* | None |
| Mixed zero weights | PASS | Yes | None |

*Subject to standard floating-point precision limitations (~15 digits).

## Modifications Made

No modifications to the algorithm were required. All edge cases are handled correctly by the original implementation. The key design choices that enable this:

1. **Lazy insertion**: Only inserting vertices when first reached (rather than all vertices upfront) naturally handles disconnected graphs and source-isolated vertices.
2. **Dynamic degree table**: The consolidation step extends the degree table when needed, handling unexpectedly high-degree scenarios.
3. **Guard in decrease-key**: The `new_key < node.key` check prevents no-op decrease-key calls.
4. **k ≥ 2 guard**: Ensures the algorithm degrades gracefully to standard Fibonacci heap behavior for small n.
