# Cross-Comparison with Prior Literature

Benchmarking our computational findings against the existing Collatz literature.

## Comparison Table

| Finding | Closest Prior Work | What's New | Significance |
|---------|-------------------|------------|--------------|
| Lyapunov exponent ≈ 0 (not 0.2027) | Kontorovich-Lagarias (2009) stochastic model | First systematic computation of finite-time Lyapunov distribution; correct theoretical value is log(2)·log(3/2)/log(6) ≈ 0, not log(3/2)/2 | KS p = 0 (non-Gaussian) |
| Non-Gaussian Lyapunov distribution | Polli et al. (2024) stochastic characteristics | First demonstration that the distribution has negative skew (~-1.55) and heavy tails (kurtosis ~3.6), ruling out Gaussian and Tracy-Widom | Survives all scales |
| R² ≈ 0.013k for n mod 2^k | Terras (1976) stopping time theorem; Wirsching (1998) | First quantitative R² decomposition showing linear growth of variance explained with 2-adic precision | Novel quantitative law |
| Modular resonance DEBUNKED | Lagarias (1985, 2021) surveys; Kontorovich-Lagarias (2009) | Demonstrated that apparent non-uniformity of stopping_time mod p (p coprime to 6) is entirely from marginal distribution, not arithmetic structure | Corrects potential misinterpretation |
| Phase transition at a≈3→5 | Lagarias (1985) generalized maps; Wirsching (1998) | First systematic phase diagram of (a,b) parameter space with convergence fractions and escape time analysis | Effect = 0.93, sharpens with scale |
| MI decays to zero | Kontorovich-Lagarias (2009) stochastic independence | First direct computation confirming stochastic independence assumption for k-bit windows up to k=8 | Supports existing theory |
| Spectral gap → 0 (Poisson spacing) | No prior spectral work on Collatz graph | First eigenvalue spacing computation; Poisson (not GOE/GUE), indicating integrable rather than chaotic structure | New characterization |
| TDA: borderline H1 persistence | No prior TDA on Collatz | First application of persistent homology; H1 feature at p=0.02 does not survive Bonferroni | Not significant |
| All forbidden patterns from "11" constraint | Wirsching (1998) parity sequences | Systematic verification that no non-trivial forbidden k-grams exist up to k=12 beyond the consecutive-odd constraint | Confirms existing understanding |

## Detailed Comparisons

### 1. Lyapunov Exponent Distribution vs. Kontorovich-Lagarias (2009)

Kontorovich and Lagarias [kontorovich2009] model the Collatz map as a stochastic process where each step independently multiplies by 3/2 (odd) or 1/2 (even) with probabilities determined by the Syracuse encoding. Their model predicts a mean "drift" of log(3)/3 + 2·log(1/2)/3 ≈ -0.098 per step (in their formulation using the Syracuse map). Our computation of the finite-time Lyapunov exponent λ(n) = (1/T)·Σ log|T'| directly measures the geometric average expansion rate along actual trajectories.

**What's new**: We find mean λ ≈ 0.0001, consistent with the marginal stability prediction but NOT with the naive log(3/2)/2 ≈ 0.2027 sometimes quoted. The distribution is strongly non-Gaussian (KS statistic > 0.11 across all scales), with negative skewness ≈ -1.55 and excess kurtosis ≈ 3.6. This non-Gaussianity is a novel finding — the Kontorovich-Lagarias model would predict a CLT-type convergence to Gaussian if steps were truly independent, which they are not at finite time scales.

### 2. R² Decomposition vs. Terras (1976) and Wirsching (1998)

Terras [terras1976] proved that the "stopping time" (time to first reach a value less than n) has density 1 among positive integers for any finite bound. Wirsching [wirsching1998] extended this to analyze how the binary structure of n influences the first k steps of the trajectory.

**What's new**: We provide the first systematic R² decomposition: the fraction of stopping time variance explained by n mod 2^k grows linearly as R² ≈ 0.013k. This means each additional bit of 2-adic information about n explains an additional 1.3% of its stopping time variance. At k=12 (4096 residue classes), 15% of the variance is explained. This quantitative law is verifiable and not stated in the literature. It provides a concrete measure of how "deterministic" vs. "random" the Collatz process appears at different levels of arithmetic resolution.

### 3. Phase Transition vs. Lagarias (1985)

Lagarias [lagarias1985] noted that generalized maps an+b with a ≥ 5 typically diverge, while a=3,b=1 is the famous convergent case. However, no systematic phase diagram existed.

**What's new**: We provide the first complete (a,b) phase diagram for odd a ∈ {1,3,...,21}, b ∈ {1,3,...,21} with convergence fractions computed from 2000 random starting values up to n=5000. The transition from a=3 (100% convergent) to a=5 (7-17% convergent depending on b) is remarkably sharp. The effect size strengthens with scale (0.83 → 0.91 → 0.93), confirming this is not a finite-size artifact.

### 4. Modular Resonance (Debunked) vs. Lagarias (2021)

Lagarias [lagarias2021] notes that stopping times have well-known dependencies on residue class modulo powers of 2 (the "2-adic" structure), but makes no claims about non-uniformity modulo primes coprime to 6.

**What's critical**: Our initial scan found 165 apparently "novel" resonances at primes coprime to 6 (e.g., mod 13 with χ²=47082). However, rigorous significance testing with the correct null model (iid draws from the empirical stopping time CDF) revealed that ALL of this non-uniformity is a property of the marginal distribution of stopping times, not of the arithmetic dependence of stopping time on starting value. The ANOVA test further confirmed: mean stopping time shows no significant dependence on residue class mod p for any prime p coprime to 6 (all F < 1.2, all p > 0.26). This is an important methodological lesson: the large chi-squared values arise because stopping times are not uniformly distributed integers, so their residues mod m are naturally non-uniform.

### 5. Mutual Information Decay vs. Kontorovich-Lagarias (2009)

The stochastic independence assumption is central to [kontorovich2009]: after sufficiently many steps, the parity of the iterate becomes essentially independent of the starting value.

**What's new**: We provide the first direct computational test by measuring I(binary_bits_of_n; parity_step_t) as a function of step t. The mutual information decays from ~0.86 bits at step 0 to null-model levels within ~20 steps for all window sizes k ∈ {4,6,8}. This supports the stochastic independence assumption and is consistent with the theoretical analysis of [kontorovich2009], but is the first direct empirical measurement.

### 6. Spectral Properties (Novel)

**No prior work exists** on the eigenvalue spacing distribution of the Collatz predecessor graph. Our finding of Poisson statistics (not GOE/GUE) indicates the graph has "integrable" structure, more akin to a tree-like graph than a random graph. The spectral gap shrinks as N^{-α} (with α ≈ 2 based on our two data points N=3000, N=10000), suggesting the graph is an expander at no finite scale.

### 7. TDA Persistent Homology (Novel but Not Significant)

**No prior work exists** applying TDA to Collatz trajectory point clouds. Our H1 feature at p=0.02 is suggestive but does not survive Bonferroni correction (corrected p=0.14). The Wasserstein distance of 13.4 between mod-4 residue classes indicates some topological differentiation, but this needs larger-scale computation to be conclusive.

### 8. Forbidden Patterns vs. Wirsching (1998)

Wirsching [wirsching1998] analyzed symbolic dynamics of parity sequences and noted the impossibility of consecutive odd steps (the "11" constraint).

**What's new**: We systematically verified for all k-grams up to k=12 that the "11" constraint is the ONLY source of forbidden patterns. All zero-frequency k-grams contain "11" as a substring. This rules out the existence of higher-order constraints on Collatz symbolic dynamics up to words of length 12, supporting the view that parity sequences are well-approximated by Bernoulli(p) with p = log(2)/log(3) subject only to the "11" exclusion.

## Summary of Advances

1. **Genuinely novel quantitative law**: R² ≈ 0.013k for 2-adic variance decomposition (not in literature)
2. **Novel characterization**: Lyapunov distribution shape (skew = -1.55, kurtosis = 3.6, non-Gaussian)
3. **First systematic phase diagram**: (a,b) parameter space with convergence fractions
4. **First spectral characterization**: Poisson spacing in Collatz predecessor graph
5. **Important negative result**: Modular resonance at primes coprime to 6 is an artifact
6. **Empirical confirmation**: MI decay supports stochastic independence assumption
7. **Systematic verification**: No non-trivial forbidden patterns up to k=12

References: [tao2019], [lagarias1985], [lagarias2021], [kontorovich2009], [terras1976], [wirsching1998], [polli2024], [mori2024], [siegel2024], [barina2020], [applegate2001], [lagarias2005]
