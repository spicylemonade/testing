# Limitations, Open Questions, and Future Research Directions

## 1. Computational Limitations

### 1.1 Search Bound Constraints

Our exhaustive search methods (brute force and modular sieve) reached a maximum edge bound of 5,000 — many orders of magnitude below published frontiers:

| Method | Our Bound | Published Frontier | Gap Factor |
|--------|-----------|-------------------|------------|
| Exhaustive (brute force) | 5,000 | 2.325×10^10 (Rathbun) | ~5×10^6 |
| Exhaustive (modular sieve) | 5,000 | 2.5×10^13 (Matson) | ~5×10^9 |
| Novel search (triple intersection) | 5,000 | — | — |
| Parametric families | ~10^10 edges | ~10^13 (Butler) | ~10^3 |

The primary bottleneck is algorithmic: our methods scale as O(n^2) or worse, while published algorithms exploit number-theoretic structure (even-edge factorization, elliptic curve methods) to achieve sub-quadratic scaling. A secondary bottleneck is implementation: single-threaded Python is ~100x slower than optimized C/C++ for integer arithmetic.

### 1.2 Time Budget

All experiments were conducted within a single session with a practical time budget of minutes per method per bound. At bound=5,000:
- Brute force: 16.1 seconds
- Modular sieve: 3.6 seconds
- Novel search: 0.02 seconds

Extrapolation shows that reaching bound=10^6 would require ~2 days for the modular sieve and ~12 days for brute force. Reaching bound=10^10 is infeasible with any of our methods (~500,000 years for the sieve).

### 1.3 Incomplete Coverage of Novel Search

The Pythagorean triple intersection method found only 24 of 69 Euler bricks (35% coverage) at bound=5,000. It misses bricks where no two faces share a common Pythagorean leg via the indexed lookup structure. This is an inherent limitation of the shared-leg triangle-finding approach, not a bug.

## 2. Mathematical Limitations

### 2.1 What Our Methods Cannot Prove

Our computational search can only establish non-existence below a finite bound. Even if we searched to 10^100, this would not constitute a proof of non-existence — a perfect cuboid could still exist with larger edges. Computational evidence, no matter how extensive, cannot settle the existence question definitively.

### 2.2 Statistical Analysis Limitations

Our chi-squared test of the near-miss gap distribution (χ² = 4.45, 9 dof) shows consistency with random behavior, but:
- The test has limited statistical power with only 620 Euler bricks.
- Uniformity of gaps does not prove non-existence; it merely fails to detect a pattern.
- The space diagonal values are not truly random — they are constrained by Pythagorean structure — so the uniform null hypothesis is only an approximation.
- Subtle arithmetic biases (e.g., from specific residue class correlations) could be masked by the coarse binning of the chi-squared test.

### 2.3 Parametric Family Limitations

Our parametric families (Saunderson, Euler, Bremner) produce infinite Euler bricks but are known to never yield a perfect cuboid. Saunderson's family produces bricks where the space diagonal squared has the form a²+b²+c² = u²v²(4v²-w²)² + v²u²(4u²-w²)² + 16u²v²w², which factors in a way that prevents it from being a perfect square for generic Pythagorean triples (u,v,w). Thus, our parametric near-misses, while useful for studying gap distributions, cannot converge to a solution.

### 2.4 Modular Sieve Ceiling

The modular sieve eliminates candidates mod p for individual primes, but the Chinese Remainder Theorem guarantees that for any finite set of primes, some candidates will survive all filters. The sieve achieves 100% filtering at bound=5,000 with 10+ primes only because the search space is small enough. At larger bounds, more candidates will survive, and the sieve's speedup factor will plateau. The sieve cannot, in principle, prove non-existence — it can only reduce the number of exact checks.

## 3. Open Questions

### 3.1 Does the Pythagorean Graph Have Triangle Density Bounds?

Our novel search algorithm finds Euler bricks as triangles in the Pythagorean graph. A natural question: what is the asymptotic density of triangles in this graph? If T(N) denotes the number of triangles with all vertices ≤ N, what is the growth rate of T(N)? Our data suggests T(N) grows roughly as N^1.3, but the theoretical bound is unknown. Understanding triangle density could inform whether perfect cuboids are "expected" to exist from a graph-theoretic perspective.

### 3.2 Are Sharipov's Three Cuboid Conjectures True?

Sharipov (2012) formulated three conjectures about the irreducibility of certain polynomials in the cuboid factor equations. If all three hold, no perfect cuboid exists. The conjectures remain unproven. A resolution — either proving them via commutative algebra/algebraic geometry or finding a counterexample — would be a major advance.

### 3.3 Is There a Brauer-Manin Obstruction?

The algebraic variety V defined by the four cuboid equations is a subvariety of projective space. Van Luijk (2000) showed it is related to a K3 surface. If V has a non-trivial Brauer group element that obstructs rational points (despite having real and p-adic points for all primes p), this would constitute a proof of non-existence. Computing the Brauer group of V appears feasible with modern computational algebra (Magma, SageMath) but has not been attempted.

### 3.4 What Is the Optimal Sieve Prime Set?

Our ablation study tested primes in natural order (2, 3, 5, 7, ...). But the optimal sieve may use a different set of primes — those maximizing the combined filtering rate for the specific Pythagorean structure of the cuboid problem. Are there "special" primes (perhaps related to Leech's divisibility conditions) that provide disproportionate filtering power?

## 4. Future Research Directions

### 4.1 GPU-Parallelized Modular Sieve

The modular sieve's vectorized structure is naturally suited to GPU computation. The QR mask lookups for all candidate c values at a given (a,b) pair are independent and can be executed in parallel on GPU threads. A CUDA implementation could achieve 100-1000x speedup over our NumPy version, potentially pushing the exhaustive search bound to ~10^7 in hours. This would still fall short of published frontiers but would provide a much larger Euler brick catalog for statistical analysis.

**Justification**: The NumPy vectorized sieve already demonstrates the parallelism inherent in the approach. Modern GPUs (e.g., NVIDIA A100) have thousands of cores and high memory bandwidth ideal for the bulk modular arithmetic operations.

### 4.2 Elliptic Curve Parameterization Search

Following De Grey, Gibbs, and Helm (2024), parameterize Euler bricks via families of elliptic curves. For each rational point on an appropriate elliptic curve, check whether the resulting space diagonal is an integer. The Mordell-Weil group structure of these curves determines the density of rational points, and 2-descent or 4-descent techniques can enumerate generators. This approach fundamentally changes the search strategy from "iterate over edges" to "iterate over elliptic curve points," which is vastly more efficient for large edge bounds.

**Justification**: De Grey et al. demonstrated that this approach discovers new structural constraints (e.g., excluded aspect ratios) and enables search at scales unreachable by brute force. Implementing their algorithm would bring our methods closer to the state of the art.

### 4.3 Algebraic Geometry: Computing the Brauer Group of V

Use computational algebra systems (SageMath/Magma) to compute the Brauer group Br(V)/Br(k) of the cuboid variety V over Q. If a non-trivial element exists, evaluate the Brauer-Manin pairing at all places of Q. A non-trivial obstruction would prove non-existence unconditionally, resolving the 300-year-old problem.

**Justification**: The Brauer-Manin obstruction has successfully explained the absence of rational points on other algebraic varieties (e.g., Skorobogatov's bielliptic surfaces). The cuboid variety's structure as a K3 surface (van Luijk 2000) places it in a class where Brauer group computations are feasible with existing algorithms. This is arguably the most promising path to a theoretical resolution.

### 4.4 Machine Learning-Guided Search Prioritization

Train a neural network on the features of known near-misses (edge ratios, prime factorizations, Pythagorean parameter values) to predict which regions of the search space are most likely to contain close near-misses or a perfect cuboid. Use the model to prioritize candidates, effectively replacing the uniform search with an adaptive one. Even a modest improvement in search efficiency (2-5x) could be valuable when combined with other optimizations.

**Justification**: The near-miss analysis reveals that the Saunderson family dominates the closest near-misses. Understanding which parametric families and parameter ranges produce the smallest gaps could focus computational resources more effectively.

## 5. Honest Assessment: Existence vs. Non-Existence

Based on our analysis and the broader literature, the weight of evidence **leans toward non-existence**, but not conclusively:

**Evidence favoring non-existence:**
- Over 300 years of searching with no solution found.
- Computational searches up to 2.5×10^13 have found no perfect cuboid (Matson 2015).
- The near-miss gap distribution is consistent with random behavior (no clustering near zero).
- Multiple structural constraints (Leech's divisibility, Sharipov's conjectures, De Grey et al.'s aspect ratio exclusions) progressively restrict the solution space.
- Several non-existence claims have been made (Lloyd 2022, Agbanwa 2025), though none peer-reviewed.

**Evidence favoring existence (or at least non-impossibility):**
- No universally accepted proof of non-existence exists.
- The algebraic variety has local points (real solutions and p-adic solutions for all primes), so there is no simple local obstruction.
- Analogous problems (e.g., finding rational points on specific K3 surfaces) sometimes have solutions at surprisingly large heights.
- The Hasse principle, while not always valid, does hold for many families of varieties, and its failure would require a non-trivial Brauer-Manin obstruction that has not been computed.

**Our assessment**: The problem is likely to be resolved by a **theoretical proof of non-existence** (most plausibly via a Brauer-Manin obstruction or a proof of Sharipov's conjectures) rather than by finding an actual solution. However, until such a proof exists, the question remains genuinely open.
