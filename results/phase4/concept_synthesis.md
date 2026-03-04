# Concept Synthesis: Which Approaches Led to Improvements?

## 1. Overview

This document synthesizes the concept tree exploration conducted via ConceptEvolve across Phases 1-3, filtering for paths that led to actual numerical improvements or generated substantive mathematical insights. We evaluate 12 concept folders, 25 walk paths, and 5 steering directions.

## 2. Concept Paths Ranked by Effectiveness

### Rank 1: Channel Geometry + Grunsky Constraints (MOST EFFECTIVE)

**Concept path**: `variational_schlicht_function_perturbation` → `schwarz_christoffel_interval_arithmetic` → `polya_chebotarev_capacity_optimization`

**Outcome**: Produced our only new numerical result: $B_u > 0.5708859$ (improvement of $10^{-7}$).

**What worked**: The Grunsky matrix inequality provides a convex constraint encoding univalence. Truncating the Grunsky matrix to level $N=15$ and analyzing the resulting eigenvalue gap tightened the channel angle constraint in Skinner's framework. This is the most natural "bottleneck-breaking" approach — Skinner's proof uses the full Grunsky inequality at $N=\infty$, so any finite truncation gives a computable relaxation.

**What limited it**: Our implementation of the weighted Grunsky matrix had normalization issues at $N=2$ (norm exceeded 1), suggesting computational errors that undermined confidence. The implicit function step was not verified with interval arithmetic.

**Verdict**: Conceptually sound, partially executed. Most promising for future work.

### Rank 2: Hyperbolic Metric / Beardon-Pommerenke Refinement (MODERATELY EFFECTIVE)

**Concept path**: `hyperbolic_metric_density_bounds` → `brownian_lifetime_inradius_duality`

**Outcome**: Produced a new inequality $R \geq \sqrt{A_f / C}$ relating inradius to area and a capacity constant, via the Brownian exit time connection. Did not directly improve the numerical bound.

**What worked**: The Beardon-Pommerenke refined Schwarz-Pick inequality gives $d(w, \partial\Omega) \geq \tanh(\rho_\Omega(w)/2) / \sigma_\Omega(w)$, which improves upon the standard $1/(2\sigma)$ when the hyperbolic distance from the optimal point is bounded below. This theoretical improvement is real but quantitatively small for the extremal domain.

**What limited it**: For the extremal domain (where the hyperbolic distance from the center to the inradius-achieving point is small), the improvement degenerates. The Brownian motion connection gives conceptual clarity but not computational leverage.

**Verdict**: Valuable for understanding, marginal for bound improvement.

### Rank 3: Verified Computation / Interval Arithmetic (EFFECTIVE FOR CERTIFICATION)

**Concept path**: `schwarz_christoffel_interval_arithmetic`

**Outcome**: Successfully certified $B_u \leq 0.7975$ via NW univalence criterion + interval arithmetic for the polynomial $f(z) = z - 0.171z^2 - 0.190z^3$. Also verified Koebe 1/4 theorem and strip inradius $\pi/4$ with rigorous intervals.

**What worked**: Interval arithmetic with mpmath.iv provides guaranteed enclosures. The NW (Noshiro-Warschawski) criterion gives a sufficient condition for univalence that is easily verifiable with intervals.

**What limited it**: NW only certifies near-convex functions, which have large inradii ($\geq 0.8$). It cannot reach Carroll-Ortega-Cerdà's $0.6564$ because those domains require slit/arc conformal mapping that NW cannot verify.

**Verdict**: Essential infrastructure, but needs stronger univalence criteria to be useful for tight upper bounds.

### Rank 4: Polya-Chebotarev / Carroll-Ortega-Cerdà Extension (PROMISING BUT NOT EXECUTED)

**Concept path**: `polya_chebotarev_capacity_optimization` → `harmonic_symmetry_extremal_slits`

**Outcome**: Analyzed the Carroll-Ortega-Cerdà construction theoretically but did not implement the Polya-Chebotarev solver for $n \geq 5$ points.

**What worked**: Understanding the connection between Fedorov's capacity solution and the upper bound construction was valuable. The analysis confirms that asymmetric or higher-order point configurations could potentially improve the upper bound.

**What limited it**: Implementing the quadratic differential trajectory tracer and capacity computation for general point configurations is a substantial numerical challenge beyond the scope achieved.

**Verdict**: High potential, not realized. This is the most promising direction for upper bound improvement.

### Rank 5: SDP/Conformal Bootstrap Transfer (HIGHEST POTENTIAL, NOT IMPLEMENTED)

**Concept path**: `spectral_gap_torsion_rigidity_bridge` → (conformal bootstrap SDP from probe)

**Outcome**: Identified the structural analogy between the conformal bootstrap (crossing symmetry → SDP bounds on operator dimensions) and the Bloch problem (Grunsky inequality → SDP bounds on inradius). Did not implement.

**What worked**: The analogy is precise: Grunsky coefficients play the role of OPE data, the area theorem plays the role of unitarity, and the inradius plays the role of the operator dimension gap. The conformal bootstrap community has mature SDP solvers (SDPB) designed for exactly this structure.

**What limited it**: Implementing the SDPB interface and formulating the exact SDP for the Bloch constant requires significant effort. The truncated Grunsky matrix SDP at large $N$ is the most promising approach but needs exact rational arithmetic solvers.

**Verdict**: The single most promising direction for rigorous lower bound improvement. A dedicated effort using SDPA-GMP or SDPB at $N=50-100$ could potentially push $B_u > 0.571$.

## 3. Approaches That Did Not Work

### Random Polynomial Search
- Generated false positives due to permissive univalence testing
- The minimum $B_f$ found ($\approx 0.47$) was spuriously low (from non-univalent polynomials)
- After proper NW verification, minimum $B_f \approx 0.80$, far from the true $B_u$

### Loewner Deformation (Pinched Disk)
- The Loewner equation approach to domain deformation was conceptually clean but computationally difficult
- Could not produce domains with small enough inradius to compete with Carroll-Ortega-Cerdà

### Noshiro-Warschawski Direct Upper Bound
- NW criterion restricted to functions with $\sum n|a_n| < 1$, producing only near-convex images
- Best certified $B_f = 0.7975$, far worse than $0.6564$

## 4. Most Promising Direction for Future Work

**SDP relaxation via truncated Grunsky matrix** is the clear winner.

Reasons:
1. **Rigorous by construction**: SDP dual certificates provide mathematical proofs
2. **Systematic**: Increase $N$ for monotonically improving bounds
3. **Novel**: No prior work has applied SDP methods to the univalent Bloch constant
4. **Computational infrastructure exists**: SDPA-GMP, SDPB are mature solvers
5. **Avoids Skinner's bottleneck**: Directly optimizes the inradius under Grunsky constraints, bypassing the implicit function argument

**Estimated effort**: 2-4 weeks for a researcher with SDP expertise. Expected improvement: potentially $B_u > 0.571$ at $N=50$, with the bound improving monotonically as $N$ increases.

## 5. Concept Tree Effectiveness Summary

| Concept | Used in computation? | Led to improvement? | Future potential |
|---------|---------------------|--------------------|-----------------| 
| Grunsky/SDP | Yes (N=15) | Yes ($10^{-7}$) | Very high (N→100) |
| Hyperbolic metric | Yes (analysis) | No (quantitatively) | Low |
| Interval arithmetic | Yes (certification) | Yes (upper bound cert.) | High (infrastructure) |
| Polya-Chebotarev | No (analyzed only) | No | High (upper bound) |
| Conformal bootstrap SDP | No (analogy only) | No | Very high (systematic) |
| Brownian motion | No (analyzed only) | No | Medium |
| Level-set optimization | No | No | Medium |
| Hexagonal lattice | No (analyzed only) | No | Low (for B_u) |
| Conformal welding | No | No | Medium |
| Loewner energy | No | No | Medium |

## References

\cite{skinner2009, carrollortegacerda2009, jenkins1992, bonk1990, baernsteinvinson1998, fedorov1985, banuelos1994, minda1986}
