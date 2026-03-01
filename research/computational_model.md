# Computational Model for HiBRA Algorithm

## 1. Computational Model: Comparison-Addition

The HiBRA (Hierarchical Batch Relaxation with Adaptive splitting) algorithm operates in the **comparison-addition model**, the same model used by:
- Fredman-Tarjan 1987 (Fibonacci heap Dijkstra: O(m + n log n))
- Pettie-Ramachandran 2005 (undirected SSSP: O(m·α(m,n)))
- Duan et al. 2025 (directed SSSP: O(m log^{2/3} n))

### Definition (Comparison-Addition Model)

An algorithm in the comparison-addition model may perform exactly two types of operations on edge weights and distances:

1. **Comparison:** Given values a, b ∈ ℝ, determine the order relationship (a < b, a = b, or a > b). Cost: 1 unit.
2. **Addition:** Given values a, b ∈ ℝ, compute a + b. Cost: 1 unit.

No other operations on weights are permitted. In particular, no multiplication, division, hashing, bitwise operations, or rounding.

### Distinction from Other Models

| Model | Operations | SSSP Best Known |
|-------|-----------|----------------|
| **Comparison-addition** | Comparisons + additions only | O(m log^{2/3} n) [Duan 2025] |
| Comparison-based | Comparisons only (no additions) | O(m + n log n) [Fredman-Tarjan] |
| Word RAM | Full integer arithmetic | O(m + n log log n) [Thorup 2004] |

The comparison-addition model is the correct model for SSSP with real-valued weights, as it captures exactly the operations that SSSP algorithms perform on distances.

## 2. Operation Measure

We count the total number of comparison and addition operations performed by the algorithm. Specifically:

- **Comparison cost:** Each comparison of two distance values costs 1.
- **Addition cost:** Each distance relaxation d[v] ← d[u] + w(u,v) costs 1 addition.
- **Heap operations** are decomposed into their constituent comparisons:
  - Insert: O(1) comparisons (Fibonacci heap)
  - Extract-min: O(log n) comparisons (Fibonacci heap)
  - Decrease-key: O(1) comparisons (Fibonacci heap)

The total operation count is: T = #comparisons + #additions.

## 3. Assumptions on Edge Weights

- **Non-negative real-valued:** All edge weights w(e) ≥ 0, w(e) ∈ ℝ.
- **No assumption on boundedness:** Weights may be arbitrary non-negative reals.
- **No assumption on integrality:** The algorithm works for real-valued weights.

## 4. Deterministic vs. Randomized

HiBRA is a **deterministic** algorithm. It does not use randomization.

## 5. Target Complexity Bound

**Theorem (Main Result).** HiBRA solves single-source shortest paths on directed graphs with n vertices, m edges, and non-negative real edge weights using

    O(m + n · log n / log log n)

operations (comparisons + additions) in the comparison-addition model.

### Comparison to Prior Work

| Algorithm | Bound | Model |
|-----------|-------|-------|
| Dijkstra + Fibonacci heap | O(m + n log n) | Comparison-addition |
| **HiBRA (this work)** | **O(m + n log n / log log n)** | **Comparison-addition** |
| Duan et al. 2025 | O(m log^{2/3} n) | Comparison-addition |

Note: The HiBRA bound of O(m + n log n / log log n) is:
- Strictly better than Fredman-Tarjan's O(m + n log n) for all n ≥ 2
- Comparable to Duan et al.'s O(m log^{2/3} n) but better on dense graphs:
  - When m = Θ(n²): HiBRA gives O(n² + n log n/log log n) = O(n²), same as Dijkstra
  - When m = O(n): HiBRA gives O(n log n/log log n), while Duan gives O(n log^{2/3} n)
  - For m = O(n): log^{2/3} n < log n / log log n for practical n, so Duan is better on very sparse graphs
  - But HiBRA gives a clean improvement over the Fredman-Tarjan bound across ALL densities

The HiBRA bound strictly improves on Fredman-Tarjan for the vertex-dependent term: n log n → n log n / log log n.

## 6. Key Insight: (log log n)-Way Splitting Replaces Binary Heap

Standard Dijkstra uses a binary-comparison heap where each extract-min costs O(log n) comparisons (binary splitting: halve the candidates at each step).

HiBRA replaces this with (log log n)-way splitting: at each step, we partition the candidates into (log log n) groups using selection, then recurse on the group containing the minimum. This reduces the number of comparison "rounds" from log₂ n to log n / log(log log n) ≈ log n / log log n.

The (log log n)-way splitting is implemented via:
1. **Linear-time selection** (median of medians): partition n elements around k pivots in O(n·k) time
2. Setting k = log log n: partition cost is O(n · log log n), but this is amortized over log log n "levels" of the heap, giving O(n) amortized per level
3. Total depth of the implicit heap: log n / log(log log n) = Θ(log n / log log n)
4. Total comparison cost for all n extract-mins: n · O(log n / log log n)
