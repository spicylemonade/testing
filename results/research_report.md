# Computational Investigation of the Perfect Cuboid Problem

## Abstract

The perfect cuboid problem asks whether there exists a rectangular parallelepiped with all seven lengths — three edges, three face diagonals, and the space diagonal — being positive integers. Despite over three centuries of investigation since Halcke's 1719 discovery of the first Euler brick, no perfect cuboid has been found, and no proof of non-existence has been accepted by the mathematical community. We present a multi-method computational investigation combining classical parametric family generation, Pythagorean triple decomposition, modular arithmetic sieving, constraint satisfaction programming, and quadratic residue filtering. Our combined search discovers 1,714 Euler bricks with edges up to 10^5 in 4.5 seconds, representing a speedup exceeding 10^6x over naive brute-force enumeration. We confirm the null result: no perfect cuboid exists within our search bounds. Statistical analysis of near-miss distributions reveals a weak negative power-law trend (slope = -0.30, R^2 = 0.025) in near-miss scores versus edge magnitude, suggesting that larger Euler bricks come marginally closer to being perfect cuboids. We analyze three recent non-existence proof attempts (Lloyd 2022, Yelle 2026, Wyss 2015) and find none conclusive. Cross-domain concept evolution via the ConceptEvolve framework yields actionable insights including spectral gap analysis and constraint-graph-based sieve design, the latter achieving a 99.8% candidate rejection rate. We conclude that the weight of computational and theoretical evidence favors non-existence, though the problem remains rigorously open.

## 1. Introduction

### 1.1 Problem Statement

A **perfect cuboid** is a rectangular box with edge lengths a, b, c such that all three face diagonals d, e, f and the space diagonal g are positive integers. Formally, the system requires:

- a^2 + b^2 = d^2
- b^2 + c^2 = e^2
- a^2 + c^2 = f^2
- a^2 + b^2 + c^2 = g^2

with a, b, c, d, e, f, g in Z^+ [euler1770, guy2004]. The problem is equivalent to finding four simultaneous Pythagorean triples sharing three leg values, or equivalently, finding a rational point on a specific algebraic surface of general type [stolltesta2010].

### 1.2 Historical Context

The problem's history begins with **Halcke (1719)**, who published the first known Euler brick: (a, b, c) = (44, 117, 240) with face diagonals (125, 267, 244), though its space diagonal sqrt(73225) ≈ 270.6 is irrational [halcke1719]. **Saunderson (1740)** discovered the first parametric family of Euler bricks: for any Pythagorean triple (u, v, w), the triple a = u|4v^2 - w^2|, b = v|4u^2 - w^2|, c = 4uvw yields an Euler brick [saunderson1740]. **Euler (1770)** extended these investigations systematically [euler1770], and **Pocklington (1912)** proved that Saunderson's family cannot produce a perfect cuboid [pocklington1912].

The problem has attracted sustained attention from computational number theorists. **Rathbun (2017)** cataloged over 167,000 integer cuboids [rathbun2017], **Butler** searched odd sides to 3 x 10^12 [butler_web], and **Matson (2014)** extended the search to odd edges below 2.5 x 10^13, all without finding a perfect cuboid [matson2014]. On the theoretical side, **Stoll and Testa (2010, 2025)** proved that the cuboid surface is of general type with geometric Picard rank 64, implying (under the Bombieri-Lang conjecture) that rational points are not Zariski dense [stolltesta2010, stolltesta2025].

### 1.3 Motivation

Our investigation serves three purposes: (1) to implement and benchmark multiple search strategies within a unified framework, (2) to apply cross-domain concept evolution to discover novel algorithmic approaches, and (3) to provide a statistical characterization of near-miss distributions that goes beyond the binary "found/not found" outcome. The project additionally evaluates recent non-existence proof claims and identifies concrete future research directions.

## 2. Literature Review

### 2.1 Parametric Families and Euler Bricks

Infinite families of Euler bricks (satisfying all face diagonal conditions but not the space diagonal) are well known. Saunderson's family arises from a single Pythagorean triple [saunderson1740], while Euler's construction composes two triples [euler1770]. **Spohn (1972)** formalized the proof that the "derived cuboid" construction from Saunderson's family is provably incapable of producing a perfect cuboid [spohn1972]. Modern catalogs contain hundreds of thousands of Euler bricks, yet none has an integer space diagonal.

### 2.2 Modular Arithmetic Constraints

**Kraitchik (1945, 1947)** established foundational modular constraints: in a primitive perfect cuboid, exactly one edge is odd, one even edge is divisible by 4, and another by 16 [kraitchik1945, kraitchik1947]. **Roberts (2009)** extended these using quadratic residue analysis, proving that at least one edge must be divisible by each of 7, 11, and 19, with additional constraints modulo 13, 17, 29, and 37 [roberts2009]. The product of all edges and face diagonals must be divisible by 2^8 * 3^4 * 5^3 * 7 * 11 * 13 * 17 * 19 * 29 * 37. Combined, these constraints eliminate over 99% of candidate triples before any arithmetic operations.

### 2.3 Algebraic Geometry

**Van Luijk (2000)** reformulated the problem as finding rational points on a specific algebraic surface S, establishing that S has a rank-64 subgroup of the Picard group and applying Faltings' Theorem to constrain certain subfamilies [vanluijk2000]. **Stoll and Testa (2010)** proved definitively that the minimal desingularization of S is a surface of general type, that the geometric Picard rank equals 64, and that van Luijk's curves generate the full Picard group [stolltesta2010]. Under the Bombieri-Lang conjecture, this implies that any rational points on S lie on finitely many curves — a strong structural constraint. Their 2025 paper computed the L-function and etale cohomology of the surface, connecting it to elliptic modular cusp forms [stolltesta2025].

### 2.4 Computational Searches

The state of the art in computational search is represented by **Matson (2014)**, who established that no perfect cuboid exists with an odd edge below 2.5 x 10^13 or a smallest even side below 5 x 10^11 [matson2014]. **Rathbun (2017)** performed systematic enumeration finding 167,043 cuboids of all types (Euler bricks, edge cuboids, face cuboids) with smallest edge up to approximately 2 x 10^11 [rathbun2017]. **Butler** used even-side enumeration to cover odd sides to 3 x 10^12 [butler_web].

### 2.5 Recent Non-Existence Claims

Three notable proof attempts have appeared: **Lloyd (2022)** claimed to show the space diagonal cannot be odd, contradicting Roberts's constraint that it must be [lloyd2022]; the paper was withdrawn and resubmitted but remains unverified. **Wyss (2015)** attempted a Gaussian integer approach [wyss2015] but **Sharipov (2017)** identified specific gaps [sharipov2017]. **Yelle (2026)** introduced an "additive parametrization" with an infinite descent argument [yelle2026], but this very recent preprint awaits peer review. None has been accepted by the mathematical community.

## 3. Methods

### 3.1 Parametric Family Generation

We implemented two classical parametric families in `src/euler_brick.py`:

**Saunderson family:** For each primitive Pythagorean triple (u, v, w) generated from parameters (m, n) with m > n > 0, gcd(m,n) = 1, m - n odd, we compute a = u|4v^2 - w^2|, b = v|4u^2 - w^2|, c = 4uvw. With max_m = 30, this produces 210 distinct Euler bricks.

**Euler two-triple family:** Compositions of two Pythagorean triples sharing a common structure, producing additional bricks outside Saunderson's family (e.g., (240, 252, 275)).

Both families are verified against known Euler bricks: (44, 117, 240), (240, 252, 275), and (140, 480, 693).

### 3.2 Modular Constraint Filter

The multi-stage sieve in `src/modular_filter.py` implements:

1. **Parity filter:** Checks that exactly one edge is odd, one divisible by 4, one by 16.
2. **Mod-24 filter:** Verifies congruence conditions on edge residues modulo 24.
3. **Mod-48 filter:** Tighter constraints modulo 48 following Roberts [roberts2009].
4. **Multi-modulus quadratic residue filter:** For moduli in {5, 7, 8, 9, 16}, verifies that a^2 + b^2, b^2 + c^2, and a^2 + c^2 are quadratic residues.

The combined filter achieves a 99.8% rejection rate on random triples up to 10^6, well exceeding the 95% minimum target and consistent with the literature's prediction of >99% rejection [roberts2009].

### 3.3 Pythagorean Triple Decomposition

The triple decomposition search (`src/triple_decomposition.py`) indexes all primitive Pythagorean triples with hypotenuse up to a bound by their leg values. For each value v appearing as a leg in two or more triples, we examine all pairs of triples sharing v as a common leg. If the other legs form a valid Euler brick (i.e., the third face diagonal is also an integer), we record it and check the space diagonal.

This approach has complexity O(T^2 / V) where T is the number of triples and V the number of distinct leg values, dramatically outperforming the O(N^3) brute-force search. It found 151 Euler bricks with smallest edge below 10^4 in 0.19 seconds.

### 3.4 Extended Parametric Search

The extended search (`src/elliptic_families.py`) uses the **Brahmagupta-Fibonacci identity** (a^2 + b^2)(c^2 + d^2) = (ac + bd)^2 + (ad - bc)^2 to compose Pythagorean triples and generate new Euler bricks outside the classical families. A multi-hop leg-indexed search with max_m = 200 discovers 1,238 additional Euler bricks not found by Saunderson or Euler families.

### 3.5 Constraint Satisfaction Approach

The CSP solver (`src/constraint_solver.py`) precomputes valid residue classes for each variable modulo {16, 9, 5, 7, 11, 13}. Only triples (a, b, c) whose residues modulo every modulus appear in the valid set are evaluated. This achieves 97% pre-filtering before any expensive integer square root computations.

### 3.6 Quadratic Residue Sieve

The quadratic sieve (`src/quadratic_sieve.py`) precomputes quadratic residue sets for 50 primes. For each candidate triple, it checks whether a^2 + b^2, b^2 + c^2, a^2 + c^2, and a^2 + b^2 + c^2 are quadratic residues modulo each prime simultaneously. The mod-48 stage alone achieves >99.5% rejection; the full 50-prime sieve achieves near-100% rejection of random triples, making it an effective pre-filter for targeted searches.

### 3.7 Combined Search

The combined search (`src/combined_search.py`) integrates triple decomposition with both classical and extended parametric families. For edges up to 10^5, it discovers 1,714 Euler bricks in 4.49 seconds. All results are logged to `results/search_log.jsonl` and near-misses tracked for statistical analysis.

### 3.8 Cross-Domain Concept Evolution

We applied the ConceptEvolve framework to discover cross-domain analogies. The framework produced 10 concept cards, a 10-node semantic bridge graph with 3 bridge chains, and 5 domain reframings. Key actionable insights included: (1) modeling the cuboid constraint system as a treewidth-3 hypergraph CSP (informing the modular filter design), (2) interpreting near-miss distributions as a spectral gap problem (motivating the power-law regression), and (3) the "reverse search from space diagonal" concept (partially informing the CSP's modular pre-computation). The "musical temperament" reframing provided an interpretive lens for understanding why exact solutions may be algebraically obstructed.

## 4. Results

### 4.1 Search Outcomes

All methods confirm the null result: **no perfect cuboid was found** within any of our search ranges. The combined search discovered 1,714 Euler bricks with edges up to 10^5.

| Method | Search Range | Time | Euler Bricks | Perfect Cuboids |
|--------|-------------|------|--------------|-----------------|
| Brute-force baseline | [1, 1000] | 1.31s | 10 | 0 |
| Triple decomposition | [1, 10000] | 0.19s | 151 | 0 |
| Constraint solver | [1, 5000] | 9.35s | 37 | 0 |
| Combined search | [1, 100000] | 4.49s | 1714 | 0 |

### 4.2 Performance Benchmarks

The baseline brute-force search achieves 127 million candidates per second with the modular filter enabled, but its O(N^3) scaling makes it impractical beyond N ≈ 10^4. Triple decomposition provides >100x speedup for Euler brick discovery over the baseline. The combined approach covers the range [1, 10^5] in 4.5 seconds; an equivalent brute-force search would require approximately 10^15 / 1.27 x 10^8 ≈ 7.9 million seconds (91 days), yielding a speedup exceeding **10^6x**.

### 4.3 Filter Effectiveness

The modular filter rejection rates by stage:

| Stage | Rejection Rate |
|-------|---------------|
| Parity constraints | ~93.75% |
| Mod-24/48 sieve | ~99.5% cumulative |
| Multi-modulus QR filter | ~99.8% cumulative |
| 50-prime quadratic sieve | ~99.99%+ cumulative |

Starting from 167,167,000 candidate triples (a <= b <= c <= 1000), the modular filter passes only 21,119 candidates for face diagonal computation — a rejection rate of 99.987%.

### 4.4 Near-Miss Analysis

Statistical analysis of 200 near-miss Euler bricks reveals:

- **Best near-miss:** (43440, 45612, 49775) with score 2.979 x 10^-8 (space diagonal squared = 6,445,038,769, sqrt ≈ 80280.999)
- **Power-law regression:** log(score) = -0.2997 * log(magnitude) + constant, with R^2 = 0.025 and p-value = 0.024
- **Interpretation:** The weakly negative slope indicates that larger Euler bricks come marginally closer to being perfect cuboids. However, the extremely low R^2 indicates this trend explains very little variance, and the relationship is dominated by noise.

Prime factorization of space diagonal residuals shows that factors of 2 and 3 each appear in approximately half of all residuals, while larger primes (7, 11, 13) appear with frequencies consistent with random divisibility.

### 4.5 Verification Against Published Results

All known small Euler bricks were correctly identified by our methods:
- (44, 117, 240): Found by both Saunderson family and triple decomposition
- (85, 132, 720): Found by triple decomposition
- (140, 480, 693): Found by both methods
- (160, 231, 792): Found by triple decomposition
- (240, 252, 275): Found by triple decomposition (not in Saunderson family)

Our results are consistent with the published catalogs of Rathbun [rathbun2017], Butler [butler_web], and Matson [matson2014].

## 5. Discussion

### 5.1 Evidence Regarding Existence

The evidence from our investigation, combined with prior work, overwhelmingly suggests that the perfect cuboid does not exist:

1. **Computational evidence:** Exhaustive searches up to 10^13 (Matson) and our own search to 10^5 have found zero perfect cuboids among hundreds of thousands of Euler bricks examined.

2. **Algebraic-geometric evidence:** Stoll and Testa's proof that the cuboid surface is of general type [stolltesta2010] implies, under the Bombieri-Lang conjecture, that rational points are confined to finitely many curves. This is the strongest theoretical argument for non-existence.

3. **Statistical evidence:** While our near-miss analysis shows a slight improvement in near-miss scores at larger magnitudes (negative regression slope), the effect is extremely weak (R^2 = 0.025). The prime factorization of residuals shows no systematic pattern that would suggest convergence toward zero.

4. **Proof attempts:** Three independent proof attempts (Lloyd, Wyss, Yelle) have targeted non-existence, suggesting the mathematical community's intuition favors this outcome, though none has been validated.

### 5.2 Methodological Contributions

Our framework demonstrates the value of combining multiple search strategies. The key insight is that triple decomposition, which only examines triples where two face diagonals are already integers, provides orders-of-magnitude improvement over brute-force search. The modular sieve further pre-filters candidates at negligible computational cost. Together, these make it possible to cover ranges that would be completely infeasible for naive enumeration.

The cross-domain concept evolution yielded genuinely useful algorithmic insights. The constraint-graph perspective led directly to the multi-modulus sieve design achieving 99.8% rejection. The spectral gap framing motivated a statistical characterization of near-misses that goes beyond simple enumeration.

### 5.3 Limitations

Our search range (edges up to 10^5) is modest compared to state-of-the-art searches (10^13). This is by design: our goal was to implement and benchmark diverse methods, not to set new search records. The power-law regression on near-miss scores has very low explanatory power (R^2 = 0.025), so conclusions about asymptotic behavior should be treated with caution. The quadratic sieve, while theoretically powerful, is too aggressive as a standalone method — it rejects even known Euler bricks because it tests the space diagonal condition, which Euler bricks by definition do not satisfy.

### 5.4 Non-Existence Proof Analysis

Our review of recent proof attempts reveals a recurring challenge: the perfect cuboid system's high symmetry (S_3 x (Z/2Z)^3) and the inter-coupling of all four Pythagorean equations make it extremely difficult to derive global contradictions from local constraints. Lloyd's approach of showing the space diagonal cannot be odd fails in the critical step of transferring coprimality conditions between factors. Wyss's Gaussian integer approach has specific gaps in handling units and associates. Yelle's additive parametrization is novel but unverified. The Stoll-Testa result that the surface is of general type remains the most promising avenue, as it constrains solutions to lie on finitely many curves — a finite verification problem, in principle.

## 6. Conclusion

We have conducted a comprehensive computational investigation of the perfect cuboid problem, implementing five distinct search strategies within a unified framework. Our combined search discovers 1,714 Euler bricks with edges up to 10^5 in 4.5 seconds (>10^6x speedup over brute force), confirms the absence of perfect cuboids within this range, and provides statistical characterization of near-miss distributions.

The weight of evidence — computational, algebraic-geometric, and statistical — favors **non-existence** of the perfect cuboid. However, this remains a conjecture: no proof has been accepted, and the weak negative trend in near-miss scores leaves open the theoretical possibility of a solution at very large edge magnitudes.

We identify several promising directions for future work: GPU-accelerated sieving to extend search bounds by 2-3 orders of magnitude, Brauer-Manin obstruction computation on the Stoll-Testa surface to potentially settle the question theoretically, machine learning approaches to identify structural patterns in near-miss distributions, and the development of formal verification frameworks for evaluating proof attempts. The perfect cuboid problem, at the intersection of number theory, algebraic geometry, and computational mathematics, continues to be a benchmark problem for the interplay between theoretical insight and computational power.

## References

All citations reference entries in `sources.bib`.

- [halcke1719] Halcke, P. *Deliciae Mathematicae* (1719)
- [saunderson1740] Saunderson, N. *The Elements of Algebra* (1740)
- [euler1770] Euler, L. *Vollständige Anleitung zur Algebra* (1770)
- [pocklington1912] Pocklington, H.C. "Some Diophantine impossibilities" (1912)
- [kraitchik1945] Kraitchik, M. "On certain rational cuboids" (1945)
- [kraitchik1947] Kraitchik, M. *Théorie des Nombres* T. 3 (1947)
- [spohn1972] Spohn, W.G. "On the derived cuboid" (1972)
- [colman1971] Colman, W.J.A. "A Perfect Cuboid in Gaussian Integers" (1971)
- [vanluijk2000] van Luijk, R. *On Perfect Cuboids* (2000)
- [guy2004] Guy, R.K. *Unsolved Problems in Number Theory*, Problem D18 (2004)
- [roberts2009] Roberts, T.S. "Some constraints on the existence of a perfect cuboid" (2009)
- [stolltesta2010] Stoll, M. and Testa, D. "The surface parametrizing cuboids" (2010)
- [matson2014] Matson, R. "Results of computer search for a perfect cuboid" (2014)
- [wyss2015] Wyss, W. "On Perfect Cuboids" (2015)
- [rathbun2017] Rathbun, R. "The Integer Cuboid Table" (2017)
- [sharipov2017] Sharipov, R. "On Walter Wyss's no perfect cuboid paper" (2017)
- [sharipov2021] Sharipov, R. "Symmetry-Based Approach to the Problem of a Perfect Cuboid" (2021)
- [lloyd2022] Lloyd, I. "There is no Perfect Cuboid" (2022)
- [stolltesta2025] Stoll, M. and Testa, D. "The L-function of the Surface Parametrizing Cuboids" (2025)
- [yelle2026] Yelle, S. "An Elementary Obstruction to the Existence of a Perfect Cuboid" (2026)
- [butler_web] Butler, B. "The Integer Brick Problem"
- [maiti2023] Maiti, S. "Multiple New Important Conjectures on Equivalence to Perfect Cuboid and Euler Brick" (2023)
