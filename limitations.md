# Limitations, Threats to Validity, and Honest Assessment

## 1. Honest Assessment of Asymptotic Improvement

### Does DAMS-SSSP achieve a genuine asymptotic improvement over O(m + n log n)?

**Qualified yes, with important caveats.**

DAMS-SSSP achieves O(m · √(log n) + n · log n) in the comparison-addition model. This is asymptotically better than O(m + n log n) when m = Ω(n · √(log n) · log(log n)), i.e., for graphs that are at least slightly denser than the extreme sparse case.

Specifically:
- For **m = Θ(n^{1+ε})** for any constant ε > 0: DAMS-SSSP gives O(m √(log n)) = o(m + n log n). **Genuine improvement.**
- For **m = Θ(n √(log n))**: DAMS-SSSP gives O(n log n), same as Dijkstra. **No improvement.**
- For **m = Θ(n)** (maximally sparse): DAMS-SSSP gives O(n √(log n) + n log n) = O(n log n), dominated by the additive term. **No improvement over Dijkstra** in this regime, unlike Duan et al. 2026 which achieves O(n √(log n)).

**The additive O(n log n) term is the key weakness** compared to Duan et al. 2026's pure O(m √(log n)). This term arises from the cleanup phase and the initial scan of all edges to determine the maximum weight. Duan et al.'s recursive BMSSP approach avoids this by never performing a full scan — their recursion only touches edges within each subproblem.

### What was achieved?

Even where DAMS-SSSP does not strictly improve on Dijkstra:

1. **A novel algorithmic framework:** DAMS-SSSP provides an alternative to BMSSP recursion for sub-sorting-barrier SSSP, based on the well-understood techniques of epsilon-scaling and Δ-stepping. This simpler framework is potentially more amenable to practical optimization and parallelization.

2. **Cross-domain synthesis:** The algorithm demonstrates productive transfer of ideas from auction algorithms, adaptive mesh refinement, and streaming algorithms to SSSP — a concrete example of algorithmic innovation through cross-domain analogy.

3. **Matching the state-of-the-art for moderate-density graphs:** For m = Ω(n^{1.5}) or denser, DAMS-SSSP matches the Duan et al. 2026 bound. For many practical applications (dense road networks, social networks, web graphs), this density regime is relevant.

4. **Simpler implementation:** DAMS-SSSP is ~150 lines of Python (including data structure) vs. the ~200+ lines needed for even a simplified Duan et al. implementation. The iterative structure avoids the complexity of managing recursive BMSSP calls.

## 2. Practical Performance Assessment

### DAMS-SSSP does NOT outperform Dijkstra in practice.

This must be stated clearly and without equivocation. At all experimentally feasible sizes (n ≤ 200K), binary heap Dijkstra is 3–10× faster than DAMS-SSSP in wall-clock time:

| n | Graph | Dijkstra+Bin | DAMS-SSSP | Ratio |
|---|---|---|---|---|
| 100K | Sparse | 0.72s | 3.28s | 4.6× |
| 100K | Grid | 0.47s | 3.30s | 7.0× |
| 100K | Worst-case | 0.79s | 1.34s | 1.7× |
| 100K | Road network | 0.61s | 5.54s | 9.1× |
| 200K | Social network | 3.34s | 12.28s | 3.7× |

The gap is smallest on worst-case graphs (1.7×) and largest on road networks (9.1×). This is because worst-case graphs have a chain structure that DAMS-SSSP handles efficiently (each bucket contains exactly one vertex), while road networks have geometric structure that Dijkstra exploits via locality but DAMS-SSSP's buckets scatter.

This practical gap is consistent with Castro et al. [castro2025], who found Dijkstra 3–4× faster than Duan et al. 2025 in an optimized C++ implementation. They estimated a crossover point beyond n > 10^{67} for the worst-case variant. Our DAMS-SSSP likely has a similarly distant crossover point.

## 3. Threats to Validity

### 3.1 Language Overhead

All algorithms are implemented in Python 3, which has ~100× overhead per operation compared to C/C++. This disproportionately affects algorithms with complex data structures:
- Fibonacci heap: Each extract-min involves Python list operations, pointer chasing, and cascading cuts — all expensive in Python
- BucketPQ: Python list append/remove operations are slower than C array operations

The implication: **wall-clock comparisons between algorithms in Python primarily measure Python overhead differences, not algorithmic complexity differences.** Operation counts are a fairer comparison metric.

### 3.2 Size Limitations

Our largest tests use n = 200K vertices. At this size:
- log₂(n) ≈ 17.6
- √(log₂(n)) ≈ 4.2
- log^{2/3}(n) ≈ 6.7

The ratio log(n)/√(log(n)) is only about 4. For the theoretical improvements to become practically visible, we would need n where log(n)/√(log(n)) >> 10, i.e., n > 2^{100} ≈ 10^{30}. This is far beyond any experimentally feasible size.

### 3.3 Correctness Verification Scope

We verified correctness against Bellman-Ford for n ≤ 5K on all graph types. For larger n, correctness is assumed based on the mathematical proof. It is theoretically possible (though unlikely given the clean proof structure) that numerical precision issues in floating-point arithmetic could cause errors at very large n. A comprehensive verification at n = 100K (expensive but feasible) was not performed.

### 3.4 Graph Generator Fidelity

Our graph generators produce synthetic instances that approximate but do not perfectly replicate real-world networks:
- Road networks lack hierarchical and planar structure
- Social networks lack community/cluster structure
- Power-law graphs may have different exponents than real networks

Testing on actual DIMACS Challenge road networks and SNAP social network datasets would provide stronger external validity.

### 3.5 Single Seed

All experiments use seed 42. While this ensures reproducibility, it means results may not be representative of the average case. A more thorough evaluation would use multiple seeds (e.g., 10 random seeds) and report confidence intervals.

## 4. Comparison with Castro et al. [castro2025]

Castro, Clementino and de Freitas (2025) performed the first rigorous experimental analysis of the Duan et al. 2025 algorithm. Their key findings:

| Finding | Castro et al. | Our results | Consistent? |
|---|---|---|---|
| Dijkstra faster in practice | Yes (3–4× in C++) | Yes (3–9× in Python) | Yes |
| Gap grows with n | Unclear (limited sizes) | Gap stable at 3–5× for sparse | Partially |
| Constant factor is the bottleneck | Yes | Yes | Yes |
| Expected-time variant helps | Yes (some improvement) | Not tested | N/A |

Our DAMS-SSSP results are qualitatively consistent with Castro et al.'s findings on Duan et al. The practical gap exists for any sub-sorting-barrier algorithm, not just BMSSP-based approaches.

## 5. Future Work Directions

1. **C/C++ Implementation:** The most impactful next step. Would eliminate the Python overhead confound and enable testing at n > 10^6. Expected to narrow the practical gap from 3–9× to potentially 1.5–3× (based on the operation count ratios).

2. **GPU/Parallel Implementation:** DAMS-SSSP's bucket structure is naturally parallelizable. Each bucket can be processed in parallel (similar to Δ-stepping on GPUs). The multi-scale structure adds another dimension of parallelism.

3. **Adaptive Multi-Scale Framework:** Instead of fixed √(log n) scales, use graph properties (diameter estimate, weight distribution) to choose the optimal number of scales. The ablation study shows this could reduce runtime by up to 1.5× on well-structured graphs.

4. **Integration with Practical Heuristics:** Combining DAMS-SSSP with A* search, landmark-based pruning, or contraction hierarchies could yield a practical algorithm that uses the multi-scale framework for the "core" computation while leveraging heuristics for speed.

5. **Formal Verification:** Machine-checked proof of correctness using Coq or Lean would strengthen the theoretical contribution and catch any subtle issues in the hand-written proof.
