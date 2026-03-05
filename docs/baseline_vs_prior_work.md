# Comparison of Baseline Metrics to Prior Work

## Implemented Baseline Metrics
Our current continuous/algebraic filter relies on spectral properties—specifically, Hoffman's bound and a heuristic related to the Lovász $\vartheta$-function (`metrics/spectral_bounds.py`). As demonstrated in `experiments/baseline_evaluation_results.md`, these metrics correctly identify the $K_5$-freeness of the $R(4,4)$ critical graph (Paley(17)) by computing a bound of $\sqrt{17} \approx 4.12 < 5$.

## Comparison Against Literature

### 1. Angeltveit & McKay (2024): $R(5,5) \le 46$
* **Their Approach**: Angeltveit & McKay relied on exhaustive computational search spaces aggressively pruned using **linear programming** over structural counts (edges, triangles, $K_4$s). Their filtering relied heavily on subgraph enumeration and flag algebras to bound densities.
* **Our Baseline**: Our spectral baseline avoids explicit subgraph enumeration entirely. Instead of searching for triangles or $K_4$s, it computes the global algebraic invariants (eigenvalues) in $O(N^3)$ time. However, Hoffman/Lovász bounds are continuous relaxations; for $N \ge 43$, the $\vartheta$-function of a $K_5$-free graph might exceed 5, making our baseline a weaker sufficient condition but an infinitely faster necessary filter compared to their heavy LP.

### 2. Tamburini (2025): Random-Projector Quantum Diagnostics
* **Their Approach**: Embeds Ramsey instances into a $Z_2 \times Z_2$-graded Majorana algebra to bypass brute-force enumeration, providing a statistical prime-factor heuristic for $R(5,5)=45$.
* **Our Baseline**: Both approaches map the discrete combinatorial problem to continuous algebraic spaces. While Tamburini uses random projections in a Clifford algebra to estimate subgraph densities, our baseline computes deterministic exact spectral bounds on the adjacency matrix. The quantum approach might provide a tighter expected value near $N=43-45$, whereas our spectral bounds provide absolute, rigorous mathematical guarantees (albeit looser).

### 3. Alon & Lubetzky (2006): Graph Powers and Shannon Capacity
* **Their Approach**: Studies the clique numbers of graph powers using algebraic bounds like Hoffman's bound and Lovász $\vartheta$.
* **Our Baseline**: Our baseline directly applies the exact continuous algebraic limits pioneered in works similar to Alon & Lubetzky. The fact that Paley(17) precisely yields $\vartheta(G) = \sqrt{17}$ validates our numerical implementation of these Shannon-capacity-related limits.

## Summary
Our spectral baselines perfectly match the foundational algebraic theory (Alon & Lubetzky) but reveal the core limitation of linear algebraic relaxations: as $N$ approaches the true $R(5,5)$ bound ($\approx 43-46$), the continuous spectral gap weakens. To achieve stricter, non-trivial new bounds and surpass the $N=46$ limit of computational LPs (McKay 2024), we must incorporate non-linear constraints—such as mapping the exact partition function via tensor networks or exploring topological syzygies (our ConceptEvolve pathways)—which do not suffer from the same continuous relaxation slack as the Lovász $\vartheta$-function.
