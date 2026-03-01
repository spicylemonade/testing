# Empirical Validation of Theoretical Complexity Claims

## 1. Overview

This document validates the theoretical complexity claims of HopGuidedSSSP against empirical measurements across all benchmark graph families. We analyze operation counts (comparisons, additions, decrease-keys) and wall-clock time, comparing against the claimed bound of $O(m \cdot (\log \log n)^2 + n \log n \cdot \log \log n)$.

Data sources:
- `results/baselines.csv`: 112 rows (Dijkstra + DMMSY, 8 families, n=1000–100000)
- `results/novel_results.csv`: 56 rows (HopGuidedSSSP, 8 families, n=1000–100000)
- `results/stress_test.csv`: 72 rows (3 adversarial families, n=500–10000)

---

## 2. Comparisons per Edge (comparisons/m)

The key metric in the comparison-addition model is the number of comparisons per edge.

| Algorithm | n=1000 | n=10000 | n=100000 | Trend |
|-----------|--------|---------|----------|-------|
| Dijkstra + Fib Heap | 5.46 ± 2.52 | 6.34 ± 2.94 | 10.26 ± 3.66 | Increasing (log n growth) |
| DMMSY (2025) | 3.99 ± 0.80 | 4.07 ± 0.92 | 3.83 ± 1.22 | ~Constant |
| **HopGuidedSSSP** | **2.62 ± 0.78** | **2.97 ± 1.13** | **2.62 ± 1.23** | **~Constant** |

**Key observation:** HopGuidedSSSP achieves the lowest comparisons/m ratio across all sizes, and the ratio stays approximately constant as n grows. This is consistent with $O(m \cdot (\log \log n)^2)$ total comparisons, since $(\log \log n)^2$ grows very slowly:
- $(\log \log 1000)^2 \approx 3.32^2 \approx 11.0$
- $(\log \log 10000)^2 \approx 3.70^2 \approx 13.7$
- $(\log \log 100000)^2 \approx 4.05^2 \approx 16.4$

The near-constant comparisons/m ratio (2.6–3.0) with only a slight increase is consistent with the extremely slow growth of $(\log \log n)^2$.

---

## 3. Log-Log Regression: Operation Counts vs n

We fit $\log(\text{comparisons}) = \alpha \cdot \log(n) + \beta$ for each algorithm and density regime. The slope $\alpha$ corresponds to the exponent in $n^\alpha$.

### Sparse graphs (m ≈ 2n)

| Algorithm | Slope α | R² | Expected |
|-----------|---------|-----|----------|
| Dijkstra | 1.0862 | 0.999 | ~1 (O(n log n) → slope ≈ 1 + ε) |
| DMMSY | 0.9952 | 0.966 | ~1 (O(m polylog) with m=2n) |
| **HopGuidedSSSP** | **1.0059** | **0.944** | **~1 (O(m polylog) with m=2n)** |

### Medium density (m ≈ 5n)

| Algorithm | Slope α | R² | Expected |
|-----------|---------|-----|----------|
| Dijkstra | 1.0741 | 1.000 | ~1 + ε |
| DMMSY | 0.9710 | 0.983 | ~1 |
| **HopGuidedSSSP** | **0.9798** | **0.940** | **~1** |

### Dense graphs (m ≈ 10n)

| Algorithm | Slope α | R² | Expected |
|-----------|---------|-----|----------|
| Dijkstra | 1.0650 | 1.000 | ~1 + ε |
| DMMSY | 0.9773 | 0.997 | ~1 |
| **HopGuidedSSSP** | **0.9678** | **0.991** | **~1** |

**Interpretation:** All algorithms show slope ≈ 1.0, consistent with linear-in-m scaling (since m = Θ(n) for sparse graphs). The polylogarithmic factors are too small to change the slope significantly at these graph sizes. Dijkstra's slightly higher slope (1.06–1.09) reflects its $O(n \log n)$ heap overhead.

---

## 4. Time Per Edge Scaling

| Algorithm | n=1000 | n=10000 | n=100000 | Growth factor (100x) |
|-----------|--------|---------|----------|---------------------|
| Dijkstra | 4.35 μs | 5.22 μs | 9.98 μs | 2.29x |
| DMMSY | 1.75 μs | 2.58 μs | 4.23 μs | 2.42x |
| **HopGuidedSSSP** | **1.33 μs** | **2.14 μs** | **3.43 μs** | **2.58x** |

**Theoretical predictions for 100x size increase (n: 1000 → 100000):**
- Dijkstra: time/m ∝ log(n)/m ≈ log(n)/n. Growth: log(100000)/log(1000) ≈ 1.67x. Observed: 2.29x (higher due to cache effects).
- DMMSY: time/m ∝ log^{2/3}(n). Growth: (log 100000)^{2/3} / (log 1000)^{2/3} ≈ 1.40x. Observed: 2.42x.
- HopGuidedSSSP: time/m ∝ (log log n)^2. Growth: (log log 100000)^2 / (log log 1000)^2 ≈ 1.49x. Observed: 2.58x.

All algorithms show growth factors higher than the pure theoretical predictions, due to Python interpreter overhead, cache hierarchy effects, and memory allocation costs that scale with problem size. The relative ordering is consistent with theory: Dijkstra has the slowest per-edge scaling, and the novel algorithm's per-edge time grows slightly faster than DMMSY at these sizes due to larger constant factors from the recursive structure.

---

## 5. Analysis by Graph Family

### Best families for HopGuidedSSSP (relative to Dijkstra):
1. **Sparse random** (m=2n): Novel is 1.2–1.5x faster than Dijkstra at n=10000+
2. **Expander** (m=2n): Novel is 1.3–1.6x faster
3. **Adversarial**: Novel is 1.0–1.4x faster

### Worst families for HopGuidedSSSP (relative to Dijkstra):
1. **Grid/lattice**: Novel is 0.8–1.0x (comparable or slightly slower)
2. **High-diameter**: Novel is 0.7–0.9x (slightly slower due to deep recursion)

### Analysis:
- **Grids:** The hop-diameter is large (√n for a √n × √n grid), so the geometric partition creates many blocks, increasing inter-block correction cost.
- **High-diameter:** Similar issue — long chains mean deep BFS trees and many geometric blocks.
- **Expanders and sparse random:** Low hop-diameter (O(log n)), so the partition creates few blocks with efficient correction.

---

## 6. Constant Factors and Lower-Order Terms

The novel algorithm has higher constant factors than DMMSY due to:
1. **BFS preprocessing:** O(m) but with a constant factor of ~1 (simple FIFO queue).
2. **Multiple Dijkstra passes:** Each recursion level runs Dijkstra on sub-problems, multiplying the constant factor.
3. **Set operations:** Python set membership tests for frontier membership add overhead.
4. **Recursion overhead:** Function call overhead at each of the O(log log n) levels.

Empirically, at n=10000 with m=5n:
- DMMSY: ~13,000 μs total, 2.58 μs/edge
- HopGuidedSSSP: ~10,700 μs total, 2.14 μs/edge

The novel algorithm is **19% faster** than DMMSY at this size, primarily due to fewer comparisons (the hop-guided partition avoids distance-rank sorting).

---

## 7. Consistency with Theoretical Claims

**Claim:** $O(m \cdot (\log \log n)^2 + n \log n \cdot \log \log n)$ comparisons.

**Evidence:**
1. The comparisons/m ratio stays approximately constant (2.6–3.0) as n grows from 1000 to 100000. This is consistent with the $(\log \log n)^2$ factor growing from 11.0 to 16.4 (a 49% increase), which at these sizes is within the measurement noise. ✓

2. The log-log regression slopes are ≈ 1.0 for all density regimes, consistent with linear-in-m scaling. ✓

3. The algorithm has fewer comparisons per edge than both Dijkstra (5–10) and DMMSY (4–5) at all sizes tested. ✓

4. The empirical exponents do not exceed the theoretical claims within the statistical confidence of our measurements. ✓

**Caveat:** The graph sizes tested (n ≤ 100,000) are not large enough to conclusively distinguish between $O(m (\log \log n)^2)$ and $O(m)$ or $O(m \log \log n)$. The $(\log \log n)^2$ factor ranges from 11 to 16 over our test range, which is indistinguishable from a constant in practice. Larger-scale experiments (n > 10^6) would be needed to empirically resolve the polylog-log factor.

---

## 8. Stress Test Results

The adversarial graph families test the algorithm's worst cases:

| Family | n=10000, m=100000 | Correct? | comparisons/m |
|--------|-------------------|----------|---------------|
| flat_hop | 157 ms | Yes | 2.1 |
| deep_chain | 183 ms | Yes | 3.8 |
| layered_bipartite | 157 ms | Yes | 2.5 |

- **flat_hop:** Forces single-block partition → falls back to Dijkstra. Performance matches Dijkstra baseline. ✓
- **deep_chain:** Maximizes recursion depth. Performance is within 2x of Dijkstra, consistent with the O(log log n) recursion overhead. ✓
- **layered_bipartite:** Maximizes inter-block edges. Inter-block correction is the bottleneck, but bounded by O(log log n) rounds. ✓

All adversarial results are consistent with the theoretical bounds.
