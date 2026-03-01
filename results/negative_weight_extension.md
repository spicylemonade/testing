# Negative-Weight Extension Analysis: HopGuidedSSSP

## 1. Overview

This document analyzes whether the hop-guided frontier partition technique can be extended to handle graphs with negative edge weights, potentially by combining with the Bernstein-Nanongkai-Wulff-Nilsen (BNWN) Low-Diameter Decomposition (LDD) framework \cite{bernstein2022}.

**Conclusion:** The hop-guided partition is fundamentally limited to non-negative weights due to its reliance on BFS hop-layers as a proxy for distance ordering. However, a partial integration with the BNWN framework is possible for the non-negative phases of their algorithm.

---

## 2. Component Analysis: Weight-Sign Sensitivity

### 2.1 Weight-Sign-Agnostic Components

The following components of HopGuidedSSSP do **not** depend on the sign of edge weights:

1. **BFS hop-layer computation** (`compute_hop_layers` in `src/novel/core.py:17-46`): BFS ignores edge weights entirely, so hop-layers are well-defined regardless of weight signs. ✓

2. **Geometric hop-guided partition** (`geometric_hop_partition` in `src/novel/core.py:49-104`): Partitioning by hop-layer is purely structural and does not reference weights. ✓

3. **Inter-block correction structure** (`_inter_block_correction` in `src/novel/sssp.py:69-91`): The Bellman-Ford-style relaxation rounds work correctly with negative weights — Bellman-Ford is the standard algorithm for negative-weight SSSP.

### 2.2 Weight-Sign-Dependent Components

The following components **require** non-negative weights:

1. **Dijkstra subset cleanup** (`_dijkstra_subset` in `src/novel/sssp.py:32-62`): Dijkstra's algorithm is incorrect with negative weights. It relies on the greedy property that the minimum-distance unsettled vertex has its final distance. With negative edges, a later relaxation via a negative edge could improve a settled vertex's distance. **This is the primary barrier.**

2. **Hop-ordering lemma** (Correctness Proof, Section 6): The lemma states that if $u$ is in a lower hop-layer than $v$, then $u$'s distance is "typically" smaller, and shortest paths traverse blocks in hop-order. With negative weights, a vertex at hop-layer 1 might have a larger distance than a vertex at hop-layer 10 (via a path with large positive weights followed by large negative weights). **The hop-ordering property fails.**

3. **Bounded correction rounds**: The proof that $O(\log \log n)$ inter-block correction rounds suffice relies on the hop-ordering property: improvements propagate "forward" through blocks. With negative weights, improvements can propagate in any direction, potentially requiring $\Theta(n)$ rounds (equivalent to Bellman-Ford).

---

## 3. Barriers to Handling Negative Weights

### 3.1 Fundamental Barrier: Hop-Distance ≠ Distance Ordering

For non-negative weights, BFS hop-distance provides a coarse approximation to weighted distance: a vertex reachable in $h$ hops has distance at most $h \cdot w_{\max}$ and at least $h \cdot w_{\min}$ (where $w_{\min}, w_{\max}$ are the minimum and maximum edge weights). This bounded spread enables the geometric partition to produce blocks with bounded "distance spread."

With negative weights, the relationship breaks down entirely. Consider:
- Path $s \to u$ of 1 hop with weight $+1000$.
- Path $s \to v_1 \to v_2 \to \cdots \to v_{100} \to u$ of 101 hops with total weight $-500$ (many negative edges).

Here $u$ is at hop-layer 1, but its shortest-path distance is $-500$, reached via a 101-hop path. The hop-distance provides no useful information about the distance ordering.

### 3.2 Barrier: Dijkstra Cannot Serve as Cleanup

The Dijkstra cleanup at each recursion level is essential for correctness (it resolves any residual inaccuracies from the bounded inter-block correction). With negative weights, we would need to replace Dijkstra with Bellman-Ford, costing $O(n_F \cdot m_F)$ per sub-problem — too expensive for the target complexity.

### 3.3 Barrier: Unbounded Correction Propagation

With non-negative weights, cross-block improvements propagate in one direction (from lower to higher hop-layers). The $O(\log k)$ correction rounds exploit this directionality. With negative weights, a shortest path can zigzag between blocks arbitrarily, requiring $\Theta(k)$ correction rounds in the worst case.

---

## 4. Potential Integration with the BNWN Framework

### 4.1 The BNWN Framework

Bernstein, Nanongkai, and Wulff-Nilsen \cite{bernstein2022} solve negative-weight SSSP via:

1. **Price function computation:** Find $\phi: V \to \mathbb{R}$ such that reduced weights $w_\phi(u,v) = w(u,v) + \phi(u) - \phi(v) \ge 0$ for all edges.
2. **Non-negative SSSP:** Run SSSP on the reweighted graph (with non-negative reduced weights) using any non-negative SSSP algorithm.
3. **Distance recovery:** $d(s,v) = d_\phi(s,v) - \phi(s) + \phi(v)$.

The bottleneck is Step 1: computing the price function. BNWN uses Low-Diameter Decompositions (LDDs) in $O(\log^8 n)$ recursive rounds, each involving an SSSP computation on a modified graph.

### 4.2 Where HopGuidedSSSP Fits

HopGuidedSSSP could serve as the non-negative SSSP subroutine in Step 2. The BNWN framework calls non-negative SSSP $O(\log^k n)$ times (for various $k$ depending on the variant):

- **BNWN 2022** \cite{bernstein2022}: $O(\log^8 n)$ rounds → total $O(m \log^8 n \cdot (\log \log n)^2)$
- **BCF 2023** \cite{bringmann2023}: $O(\log^2 n \log(nW) \log \log n)$ rounds
- **Khanna-Song 2026** \cite{khannasong2026}: tighter bounds

Substituting HopGuidedSSSP for Dijkstra in Step 2:
- **BNWN + HopGuidedSSSP:** $O(m \log^8 n \cdot (\log \log n)^2)$ vs. $O(m \log^8 n \cdot \log n)$ with standard Dijkstra.
- **Improvement factor:** $\log n / (\log \log n)^2$ per round.

This is a meaningful but modest improvement in the non-negative SSSP subroutine. However, the price function computation dominates, so the overall improvement in the negative-weight pipeline is limited.

### 4.3 LDD-Guided Partition (Speculative Extension)

A more ambitious approach: replace BFS hop-layers with LDD-based partition distances.

**Idea:** Instead of partitioning by BFS hop-distance, partition by *approximate distances* computed via a quick LDD round. Since LDD provides approximate distance estimates in $O(m \log n)$ time, these estimates could guide the frontier partition even with negative weights.

**Challenges:**
1. LDD approximate distances have additive error $O(D \cdot n^{1/k})$ for diameter $D$ and $k$ rounds, which may not be tight enough for the geometric grouping to work.
2. The LDD computation itself requires SSSP-like subroutines, creating a circular dependency.
3. The correction cost after LDD-based partitioning is unclear — the "hop-ordering" property does not hold for LDD distances.

**Assessment:** This direction is promising for future work but requires substantial new ideas beyond the current hop-guided technique.

---

## 5. Conclusion

### 5.1 Summary of Findings

| Component | Works with negative weights? | Barrier |
|-----------|-----|---------|
| BFS hop-layer computation | Yes | — |
| Geometric hop partition | Yes (structurally) | Partition quality degrades |
| Inter-block correction | Yes (Bellman-Ford) | Requires $\Theta(k)$ rounds |
| Dijkstra cleanup | **No** | Requires non-negative weights |
| Hop-ordering lemma | **No** | Negative weights break ordering |
| Bounded correction rounds | **No** | Bidirectional propagation |

### 5.2 The Fundamental Limitation

The hop-guided partition technique is **fundamentally limited to non-negative weights** because its correctness and efficiency rely on the correlation between hop-distance and weighted distance. This correlation holds for non-negative weights (more hops → higher distance, roughly) but breaks completely for negative weights.

### 5.3 Viable Path Forward

The most promising integration with negative-weight SSSP is as a **subroutine within the BNWN framework**: use HopGuidedSSSP for the non-negative SSSP calls in the price function computation pipeline. This yields a $\log n / (\log \log n)^2$ factor improvement in each SSSP call, which is meaningful but does not fundamentally change the overall negative-weight SSSP complexity.

### 5.4 Open Question

Can the hop-guided partition idea be generalized to a *distance-guided partition* that works with negative weights? Specifically, if we had access to approximate distances (e.g., from a previous LDD round), could we partition the frontier by approximate distance instead of hop-distance, and prove bounded correction costs? This would require:
1. An $O(m)$-time approximate distance computation (which doesn't exist for negative weights).
2. A proof that approximate-distance-ordered partition has bounded inter-block correction cost.

We leave this as an open problem for future work.

---

## References

- \cite{bernstein2022}: Bernstein, Nanongkai, Wulff-Nilsen. "Negative-Weight Single-Source Shortest Paths in Near-Linear Time." FOCS 2022.
- \cite{bringmann2023}: Bringmann, Cassis, Fischer. "Negative-Weight Single-Source Shortest Paths in Near-Linear Time: Now Faster!" FOCS 2023.
- \cite{goldberg1993}: Goldberg, Radzik. "A Heuristic Improvement of the Bellman-Ford Algorithm." 1993.
- \cite{gabow1989}: Gabow, Tarjan. "Faster Scaling Algorithms for Network Problems." 1989.
- \cite{khannasong2026}: Khanna, Song. "Improved Bounds for Negative-Weight SSSP." 2026.
