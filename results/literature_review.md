# Comprehensive Literature Review: The Perfect Cuboid Problem

## 1. Introduction

The perfect cuboid problem asks whether there exists a rectangular box with integer edges a, b, c, integer face diagonals d, e, f, and an integer space diagonal g. Despite over 300 years of investigation, the problem remains open.

## 2. Historical Origins and Euler Bricks

### 2.1 Early Work (1719-1770)

**Halcke (1719)** published the first known Euler brick: (a, b, c) = (44, 117, 240) with face diagonals (125, 267, 244) in *Deliciae Mathematicae* [halcke1719]. The space diagonal sqrt(44² + 117² + 240²) = sqrt(73225) ≈ 270.6 is not an integer.

**Saunderson (1740)**, the blind mathematician who succeeded Newton as Lucasian Professor at Cambridge, discovered the first parametric family [saunderson1740]: for any Pythagorean triple (u, v, w), set a = u|4v² - w²|, b = v|4u² - w²|, c = 4uvw. This generates infinitely many Euler bricks, including the smallest (44, 117, 240) from (u,v,w) = (3,4,5). Notably, the brick (240, 252, 275) is NOT in Saunderson's family.

**Euler (1770)** systematically studied integer-sided boxes in *Vollständige Anleitung zur Algebra* [euler1770], finding additional parametric families and establishing the problem's enduring appeal.

### 2.2 Non-Existence in Parametric Families

**Pocklington (1912)** proved that u⁴ + 18u²v² + v⁴ cannot be a perfect square [pocklington1912]. Since for Saunderson's family, a² + b² + c² = w²(u⁴ + 18u²v² + v⁴), this implies no perfect cuboid arises from this family.

**Spohn (1972)** formalized this result for the "derived cuboid" construction [spohn1972], showing that the Saunderson family is provably incapable of producing a perfect cuboid.

## 3. Modular Arithmetic Constraints

### 3.1 Kraitchik's Foundational Work

**Kraitchik (1945, 1947)** established the first systematic modular constraints [kraitchik1945, kraitchik1947]:
- At least one edge divisible by 4, another by 16
- Product abc divisible by high powers of small primes
- Specific congruence conditions modulo 24 and 48

### 3.2 Roberts's Extended Constraints

**Roberts (2009)** used quadratic residue analysis to prove additional divisibility requirements [roberts2009]:
- One edge divisible by 7
- One edge divisible by 19
- One edge or space diagonal divisible by 13
- For primes 17, 29, 37: one edge, face diagonal, or space diagonal must be divisible

### 3.3 Leech's Product Constraint

Leech extended Kraitchik's work to show the product of all sides and face diagonals must be divisible by 2⁸ · 3⁴ · 5³ · 7 · 11 · 13 · 17 · 19 · 29 · 37.

### 3.4 Parity Constraints

For a primitive perfect cuboid:
- Exactly one edge is odd; two edges are even
- Two face diagonals are odd; one is even
- The space diagonal is odd
- The space diagonal can only have prime factors congruent to 1 (mod 4)

## 4. Computational Searches

### 4.1 Rathbun's Systematic Enumeration

**Rathbun (2017)** published *The Integer Cuboid Table* [rathbun2017], an exhaustive search covering smallest edge from 44 to ~2 × 10¹¹. He discovered 167,043 cuboids total: 61,042 Euler bricks, 32,286 edge cuboids, 57,103 face cuboids, and 16,612 edge cuboids with complex edge length. No perfect cuboids were found.

### 4.2 Butler's Even-Side Enumeration

**Butler** performed systematic searches of odd sides up to ~3 × 10¹² [butler_web], using an algorithm that subdivides candidates by divisibility by 16 to exploit modular constraints.

### 4.3 Matson's Extended Search

**Matson (2014)** extended Butler's methods [matson2014] to establish that:
- No perfect cuboid exists with an odd edge smaller than 2.5 × 10¹³
- The smallest even side must exceed 5 × 10¹¹
- Statistical analysis of near-misses shows diminishing trends, suggesting non-existence

### 4.4 Summary of Search Bounds

| Researcher | Year | Bound | Parameter |
|---|---|---|---|
| Rathbun | 2017 | ~2 × 10¹¹ | Smallest edge |
| Butler | ~2000 | 3 × 10¹² | Odd side |
| Matson | 2014 | 2.5 × 10¹³ | Odd edge |
| Matson | 2014 | 5 × 10¹¹ | Smallest even side |

## 5. Algebraic Geometry Approaches

### 5.1 van Luijk's K3/General-Type Surface

**van Luijk (2000)** formulated the perfect cuboid problem as finding rational points on an algebraic surface [vanluijk2000]. Key results:
- Found enough curves to generate a rank-64 subgroup of the Picard group
- Applied Faltings' Theorem to constrain certain subfamilies
- Showed (assuming Bombieri-Lang) that perfect cuboids are not Zariski dense

### 5.2 Stoll-Testa's Definitive Surface Analysis

**Stoll and Testa (2010, revised 2025)** provided the most comprehensive algebraic-geometric treatment [stolltesta2010]:
- The cuboid surface S has 48 isolated singular points; its minimal desingularization is a surface of **general type**
- **Geometric Picard rank = 64** (proven, not just conjectured)
- Van Luijk's curves generate the **full** Picard group
- The surface admits a K3 surface as a quotient
- By Bombieri-Lang conjecture: if true, rational points on S are not Zariski dense

### 5.3 L-Functions and Cohomology

**Stoll and Testa (2025)** computed the étale cohomology and L-function of the cuboid surface [stolltesta2025], connecting it to elliptic modular cusp forms.

## 6. Symmetry and Elliptic Curve Approaches

### 6.1 Sharipov's Symmetry-Based Approach

**Sharipov (2021)** studied the perfect cuboid problem through the lens of the symmetry group of the Diophantine system [sharipov2021]. The system has a natural S₃ × (Z/2Z)³ symmetry acting on the seven unknowns.

### 6.2 Colman's Gaussian Integer Construction

**Colman (1971)** explored perfect cuboids in Gaussian integers [colman1971], showing that the problem simplifies over Z[i] but this does not directly yield real solutions.

### 6.3 Elliptic Curve Parametric Families

Each face diagonal equation defines a conic; pairs of face equations sharing a leg define an elliptic curve. Rational points on these curves generate parametric families of Euler bricks. The challenge is that the fourth constraint (integer space diagonal) imposes an additional condition that is generically not satisfied.

## 7. Recent Non-Existence Proof Attempts

### 7.1 Lloyd (2022)

**Lloyd** claimed to prove non-existence [lloyd2022] by showing the space diagonal of an Euler brick cannot be odd (contradicting Roberts's result that it must be odd). The paper was withdrawn (v2) and resubmitted (v3) but has not been accepted by the mathematical community.

### 7.2 Yelle (2026)

**Yelle** proposed an elementary obstruction [yelle2026] using "additive parametrization" and "triangular remainder." The proof uses infinite descent: a minimal odd prime in a triangular remainder propagates to all lengths, yielding a contradiction. This is a very recent preprint (February 2026) that has not undergone peer review.

### 7.3 Wyss (2015) and Sharipov's Response

**Wyss (2015)** claimed to prove non-existence [wyss2015]. **Sharipov (2017)** published a detailed critique [sharipov2017] identifying gaps in the argument.

### 7.4 Maiti (2020, 2023)

**Maiti** published both a claimed non-existence proof and follow-up conjectures relating perfect cuboids to Euler bricks [maiti2023].

### 7.5 Assessment

None of the claimed proofs have been accepted through peer review. The problem remains open. The Stoll-Testa result that the surface is of general type provides the strongest theoretical evidence that solutions are unlikely, but falls short of a proof.

## 8. Cross-Domain Connections

### 8.1 K3 Surfaces and Brauer-Manin Obstruction

The quotient K3 surface of the cuboid surface may exhibit a Brauer-Manin obstruction — solutions exist locally (mod p for all p) but not globally. This is a leading theoretical explanation for non-existence.

### 8.2 Lattice Theory and Geometry of Numbers

The problem is equivalent to finding lattice points on the intersection of quadric hypersurfaces in 7-dimensional space. The Hasse-Minkowski theorem applies locally but may fail globally.

### 8.3 Constraint Satisfaction

The problem has natural connections to CSP/SAT solving, where modular constraints act as propagation rules.

## 9. Near-Miss Analysis

The smallest Euler brick (44, 117, 240) has space diagonal squared = 73225, nearest perfect square = 73441 = 271², giving a near-miss residual of 216. The near-miss distribution contains information about the feasibility of the problem.

Key near-misses include:
- (44, 117, 240): residual 216 (sqrt ≈ 270.6)
- (85, 132, 720): residual (sqrt ≈ 737.99...)
- (140, 480, 693): residual (sqrt ≈ 863.99...)

## 10. Conclusion

The perfect cuboid problem sits at the intersection of number theory, algebraic geometry, and computational mathematics. Computational evidence strongly suggests non-existence (searches up to 10¹³ have found nothing), algebraic geometry shows the solution variety is of general type (suggesting extreme rarity), and multiple proof attempts have been made but none accepted. The problem remains one of the most famous open questions in elementary number theory.

## References

All references cited as [key] correspond to entries in sources.bib.
