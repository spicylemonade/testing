# Open Problems and Future Research Directions

## Problem 1: Can the technique yield a truly linear-time SSSP algorithm?

**Question:** Is there a comparison-addition model algorithm for SSSP on directed graphs with non-negative real weights running in $O(m + n)$ time?

**Current state:** Our algorithm achieves $O(m (\log \log n)^2 + n \log n \log \log n)$. The lower bound is $\Omega(m + n)$ \cite{karger1999}. The gap is $(\log \log n)^2$ on the $m$ term and $\log n \log \log n$ on the $n$ term.

**Barriers:**
- The $n \log n$ term comes from Dijkstra cleanup at each recursion level. Eliminating it requires a sub-$O(n \log n)$ SSSP subroutine, which is exactly what we are trying to build — a circular dependency.
- The $(\log \log n)^2$ factor comes from $O(\log \log n)$ recursion levels × $O(\log \log n)$ correction rounds per level. Reducing either factor requires fundamentally new ideas.

**Potential approaches:**
- Amortize Dijkstra cleanup across levels (only pay $O(n \log n)$ once, not per level).
- Use a non-comparison-based cleanup step (e.g., radix-sort-like for approximate distances, as suggested by Thorup \cite{thorup2004} for integer weights).
- Reduce correction rounds via a tighter hop-ordering analysis.

## Problem 2: Can the approach handle negative weights deterministically in near-linear time?

**Question:** Can hop-guided partitioning be extended to handle graphs with negative edge weights, achieving near-linear deterministic SSSP?

**Current state:** The best negative-weight SSSP algorithms \cite{bernstein2022, bringmann2023} are randomized and run in $O(m \log^{O(1)} n)$ time. Deterministic algorithms remain far from near-linear.

**Barriers:**
- BFS hop-layers do not correlate with weighted distances when negative edges exist (see `results/negative_weight_extension.md`).
- Dijkstra cannot serve as a cleanup subroutine with negative weights.
- Inter-block correction requires $\Theta(k)$ rounds instead of $O(\log k)$ with negative weights.

**Potential approaches:**
- Use LDD-based approximate distances instead of hop-distances for partitioning.
- Combine with the price function framework of Johnson's algorithm \cite{gabow1989}: first compute prices to make all weights non-negative, then apply HopGuidedSSSP.
- Design a "negative-weight-aware" hop metric that accounts for potential negative shortcuts.

## Problem 3: What is the practical crossover point where the novel algorithm outperforms Dijkstra?

**Question:** For what values of $n$ and $m$ does HopGuidedSSSP become faster than Dijkstra + Fibonacci heap in practice?

**Current empirical evidence:** At $n = 100,000$ with $m = 5n$, HopGuidedSSSP is approximately 19% faster than DMMSY and 2.4x faster than Dijkstra in our Python implementation. However, constant factors vary significantly between implementations.

**Barriers:**
- The theoretical advantage of $(\log \log n)^2$ vs. $\log n$ is tiny for practical sizes. At $n = 10^6$: $(\log \log n)^2 \approx 17.6$ vs. $\log n \approx 20$, a ratio of only 1.14.
- Python implementation overhead dominates at small sizes. A C/C++ implementation would have different crossover characteristics.
- Dijkstra's simplicity (no recursion, no BFS preprocessing) gives it an inherent constant-factor advantage.

**Recommended experiments:**
- Implement in C++ with optimized data structures.
- Test at $n = 10^6, 10^7, 10^8$.
- Profile memory access patterns (cache performance is crucial).

## Problem 4: Can the technique be parallelized or distributed?

**Question:** Can HopGuidedSSSP be efficiently parallelized on shared-memory or distributed architectures?

**Current state:** The recursive structure naturally decomposes into independent sub-problems (blocks), but the inter-block correction creates sequential dependencies.

**Barriers:**
- The inter-block correction (Bellman-Ford rounds) is inherently sequential: each round depends on the previous round's results.
- The final Dijkstra cleanup is hard to parallelize efficiently.
- Load balancing across blocks is difficult when block sizes vary.

**Potential approaches:**
- Process independent blocks in parallel at each recursion level (embarrassingly parallel).
- Use delta-stepping \cite{meyer2003} instead of Dijkstra for the cleanup (supports batched parallelism).
- Replace Bellman-Ford correction with a parallel BFS-like propagation, exploiting the hop-ordering property to determine safe-to-update vertices.
- Distribute blocks across processors in a bulk-synchronous model, with one synchronization per correction round.

## Problem 5: Does the approach generalize to all-pairs shortest paths?

**Question:** Can the hop-guided partition idea improve APSP (all-pairs shortest paths) beyond the naive application of $n$ single-source instances?

**Current state:** Running HopGuidedSSSP from each source gives $O(nm (\log \log n)^2)$ for APSP. The best known general APSP is $O(mn + n^2 \log \log n)$ for non-negative weights \cite{pettie2004}, and $O(n^3 / 2^{\Omega(\sqrt{\log n})})$ by Williams \cite{williams2014}.

**Key insight:** Different sources produce different BFS hop-layers, but the *graph structure* (adjacency) is shared. Can we precompute a universal partition that works well for all sources?

**Potential approaches:**
- Compute a *multi-source hop decomposition*: for each vertex $v$, store hop-distances from a set of $O(\sqrt{n})$ landmark vertices. Use these to guide a universal partition.
- Exploit the relationship between APSP and matrix multiplication: the hop-guided partition induces a block structure on the distance matrix.
- Combine with Seidel's algorithm \cite{seidel1995} or other algebraic APSP methods.

## Problem 6: Can the constant factors be reduced?

**Question:** Can the algorithm be redesigned to reduce the large constant factors that arise from multiple Dijkstra passes and recursive overhead?

**Practical significance:** Even if the asymptotic complexity is optimal, large constants limit practical applicability.

**Potential approaches:**
- Replace the final Dijkstra cleanup with a single global Dijkstra pass after all recursion completes (amortized cleanup).
- Use a Fibonacci heap-based Dijkstra subset that shares state across recursion levels.
- Implement "lazy" inter-block correction that only processes edges incident to vertices whose distances changed.
- Use iterative deepening instead of full recursion to reduce overhead.

---

## Summary

| Problem | Difficulty | Impact | Current Gap |
|---------|-----------|--------|-------------|
| 1. Linear-time SSSP | Very Hard | Breakthrough | $(\log \log n)^2$ |
| 2. Negative-weight extension | Hard | High | Fundamental barrier |
| 3. Practical crossover | Medium | High (engineering) | Implementation-dependent |
| 4. Parallelization | Medium | High | Sequential correction |
| 5. APSP generalization | Hard | Medium | $n$ factor overhead |
| 6. Constant factor reduction | Medium | Medium | 2-3x overhead |
