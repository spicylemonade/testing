# Research Questions: Novel Computational Investigation of the Collatz Conjecture

## Question 1: Information-Theoretic Memory in Collatz Trajectories

**Domain**: Information theory × number theory

**Precise mathematical statement**: Define X_k(n) as the k-bit window starting at bit position 0 of the binary representation of n, and Y_t(n) as the parity (odd=1, even=0) of the t-th iterate T^t(n). Compute the mutual information I(X_k; Y_t) = H(Y_t) - H(Y_t | X_k) for all n in {1, ..., N}, as a function of trajectory step t, for k = 4, 6, 8.

**Falsifiable hypothesis**: H₁: The mutual information I(X_k; Y_t) does NOT decay to zero as t → ∞ but instead plateaus at a value I∞(k) > 0 that increases with k. The null hypothesis H₀ is that I(X_k; Y_t) → 0 as t → ∞ for all k, consistent with the stochastic independence assumption of Kontorovich-Lagarias \cite{kontorovich2009}.

**Computational test**: For N = 200,000 and k ∈ {4, 6, 8}, compute I(X_k; Y_t) at each step t = 1, ..., 200. Plot I vs t with bootstrap confidence intervals. If I plateaus significantly above zero (p < 0.001 against shuffled null model), H₁ is supported.

**Why not in literature**: The web search and Semantic Scholar review found no prior work computing mutual information between binary structure of n and trajectory parity at specific steps. The closest work (Kontorovich-Lagarias) assumes independence without testing it directly. Charton-Narayanan (2025) trained transformers that implicitly learn these correlations but did not measure MI explicitly.

---

## Question 2: Modular Resonance in Stopping Times

**Domain**: Modular arithmetic × signal processing

**Precise mathematical statement**: For modulus m ∈ {2, ..., 500}, define the empirical distribution D_m(r) = |{n ≤ N : σ(n) ≡ r (mod m)}| / N where σ(n) is the total stopping time. Under the null hypothesis that stopping times are uniformly distributed mod m for m coprime to 6, the chi-squared statistic χ²(m) = Σ_r m(D_m(r) - 1/m)² · N follows χ²(m-1).

**Falsifiable hypothesis**: H₁: There exist prime moduli p > 3 with gcd(p, 6) = 1 where χ²(p) indicates significant non-uniformity (p-value < 10⁻¹⁰ after Bonferroni correction). H₀: Only moduli of the form 2^a · 3^b show significant resonance.

**Computational test**: For N = 500,000, compute σ(n) for all n, then compute χ²(m) for each m = 2..500. Rank by effect size. If any prime p > 3 coprime to 6 shows χ² with p-value < 10⁻¹⁰/500 (Bonferroni), this is a novel arithmetic constraint.

**Why not in literature**: Winkler (2017) studied stopping time determinism for specific residue classes mod 2^k. Individual modular results exist, but no systematic scan across hundreds of moduli has been published. The question of whether non-trivial resonances exist at primes coprime to 6 has not been addressed.

---

## Question 3: Spectral Statistics of the Collatz Predecessor Graph

**Domain**: Spectral graph theory × random matrix theory

**Precise mathematical statement**: Construct the Collatz predecessor graph G_N = (V, E) where V = {1, ..., N} and (a, b) ∈ E iff T(a) = b. Compute the normalized graph Laplacian L = I - D^{-1/2}AD^{-1/2} and its eigenvalues λ₁ ≤ λ₂ ≤ ... ≤ λ_N. Define the spectral gap Δ = λ₂ and the nearest-neighbor spacing distribution P(s) where s_i = (λ_{i+1} - λ_i) / ⟨λ_{i+1} - λ_i⟩.

**Falsifiable hypothesis**: H₁: The nearest-neighbor spacing distribution P(s) matches the GOE (Gaussian Orthogonal Ensemble) Wigner surmise P_GOE(s) = (π/2)s exp(-πs²/4) rather than the Poisson distribution P_Poisson(s) = exp(-s). H₀: P(s) is Poisson (uncorrelated eigenvalues).

**Computational test**: For N = 10,000, 50,000, 100,000, compute the top 500 eigenvalues of L. Compare P(s) against GOE and Poisson using KS test. If P(s) matches GOE, this connects Collatz to quantum chaos (Berry-Tabor conjecture).

**Why not in literature**: The matricial approach (2024) studies nilpotency of adjacency matrices but does not compute eigenvalue spacing statistics. No work compares Collatz graph spectra to random matrix ensembles. The spectral gap scaling with N has not been characterized.

---

## Question 4: Forbidden Patterns in Parity Sequences

**Domain**: Symbolic dynamics × combinatorics on words

**Precise mathematical statement**: For the standard Collatz map, define the parity sequence π(n) = (p_1, p_2, ..., p_T) where p_i = T^i(n) mod 2. For word length k, define F_k = {w ∈ {0,1}^k : w does not appear as a contiguous substring in π(n) for any n ∈ {1, ..., N}}. Under an iid Bernoulli(q) null model with q = log₂(3)/(1+log₂(3)) ≈ 0.387, the expected count of each k-gram across all sequences is computable.

**Falsifiable hypothesis**: H₁: There exist binary words of length k ≥ 6 that are provably forbidden (never appear for any n) or appear with frequency < 1% of the iid Bernoulli prediction, and these cannot be explained by trivial parity constraints. H₀: All 2^k words appear with approximately the expected frequency for k ≤ 12.

**Computational test**: For N = 500,000, collect all parity sequences and count every k-gram for k = 4, ..., 16. Identify k-grams absent or rare (< 1% of expected frequency). Verify forbidden patterns via modular arithmetic analysis.

**Why not in literature**: Symbolic dynamics formulations of Collatz exist (2024), but no systematic enumeration of forbidden words has been published. The connection between forbidden patterns and subshift entropy has not been explored computationally.

---

## Question 5: Phase Transition and Fractal Boundary in Generalized Collatz Family

**Domain**: Statistical mechanics × fractal geometry × dynamical systems

**Precise mathematical statement**: For the generalized map T_a,b(n) = n/2 (even), T_a,b(n) = an+b (odd) with a ∈ {1, 3, 5, ..., 21} and b ∈ {1, 3, 5, ..., 21}, define the convergence fraction F(a,b) = |{n ≤ N : T_a,b reaches a cycle within 10^6 steps}| / N. The critical boundary ∂C = {(a,b) : F(a,b) transitions from ~1 to ~0}.

**Falsifiable hypothesis**: H₁: The critical boundary ∂C has box-counting dimension d_B > 1 (fractal), and the mean escape time τ(a,b) diverges as a power law τ ~ |a - a_c|^{-γ} near the boundary with γ > 0. H₀: The boundary is smooth (d_B = 1) with exponential escape time scaling.

**Computational test**: For each (a,b) pair (a odd, 1-21; b odd, 1-21), test n = 1..100,000 for convergence. Create phase diagram. Zoom into boundary regions to estimate box-counting dimension via log-log plot of box count vs. box size. Measure escape time scaling near critical (a,b) pairs.

**Why not in literature**: Wegner (2021) studied 3x+k for specific k values. Individual generalized maps have been studied, but no comprehensive phase diagram with fractal boundary analysis exists. The connection to critical phenomena in statistical mechanics (power-law divergence, universality) has not been explored.
