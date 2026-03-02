# Problem Specification: The Perfect Cuboid

## 1. The Diophantine System

A **perfect cuboid** is a rectangular box with edges (a, b, c), all positive integers, such that all three face diagonals and the space diagonal are also positive integers.

### 1.1 The Four Pythagorean-Type Equations

Given edges a, b, c > 0, define:
- **Face diagonal** d_ab = sqrt(a^2 + b^2) (face with edges a, b)
- **Face diagonal** d_ac = sqrt(a^2 + c^2) (face with edges a, c)
- **Face diagonal** d_bc = sqrt(b^2 + c^2) (face with edges b, c)
- **Space diagonal** d_s = sqrt(a^2 + b^2 + c^2)

The perfect cuboid problem requires all 7 values to be positive integers:

| Equation | Condition |
|----------|-----------|
| a^2 + b^2 = d_ab^2 | Face diagonal of ab-face is integer |
| a^2 + c^2 = d_ac^2 | Face diagonal of ac-face is integer |
| b^2 + c^2 = d_bc^2 | Face diagonal of bc-face is integer |
| a^2 + b^2 + c^2 = d_s^2 | Space diagonal is integer |

Note: The fourth equation is equivalent to d_ab^2 + c^2 = d_s^2 (or any permutation), connecting the face diagonal equations to the space diagonal.

### 1.2 Equivalent Formulation

The system can be restated: find positive integers a < b < c (WLOG) such that:
- a^2 + b^2 is a perfect square
- a^2 + c^2 is a perfect square
- b^2 + c^2 is a perfect square
- a^2 + b^2 + c^2 is a perfect square

An **Euler brick** satisfies only the first three conditions. A **perfect cuboid** additionally satisfies the fourth.

## 2. Known Modular and Divisibility Constraints

For a **primitive** perfect cuboid (gcd(a,b,c) = 1), if it exists:

### 2.1 Parity Conditions
- Exactly one edge is odd, the other two are even.
- The odd edge has two face diagonals that are odd.
- The space diagonal d_s is odd.

### 2.2 Divisibility by Powers of 2
- One edge must be divisible by 4.
- One edge must be divisible by 16.
- The product of all edges and diagonals is divisible by 2^8.

### 2.3 Divisibility by Small Primes
For a primitive perfect cuboid:
- At least two edges are divisible by 3 (at least one by 9).
- One edge is divisible by 5.
- One edge is divisible by 7.
- One edge is divisible by 11.
- One edge is divisible by 19.
- One edge or the space diagonal is divisible by 13.
- One edge, face diagonal, or space diagonal is divisible by 17.
- The product of all edges and face diagonals is divisible by 2^8 * 3^4 * 5^3 * 7 * 11 * 13 * 17 * 19 * 29 * 37 (Leech, 1977).

## 3. Necessary Conditions from the Literature

### Condition 1: Pythagorean Triple Structure
Each face of the cuboid corresponds to a Pythagorean triple. All three faces must simultaneously have Pythagorean triple structure. This means each pair of edges (a,b), (a,c), (b,c) must be the legs of a Pythagorean triple.

### Condition 2: Leech's 4:3 Exclusion
No face of a perfect cuboid can have aspect ratio 4:3 (Pythagorean parameters m=2, n=1). This was proved by Leech (1977) using a descent argument.

### Condition 3: Quadratic Residue Compatibility
For every prime p, the values a^2+b^2, a^2+c^2, b^2+c^2, and a^2+b^2+c^2 must all be quadratic residues mod p. This eliminates the majority of candidate triples for each prime.

### Condition 4: Space Diagonal Prime Factor Constraint
All prime factors of d_s must be congruent to 1 (mod 4), since d_s^2 = a^2 + b^2 + c^2 = d_ab^2 + c^2, and a sum of two squares has all prime factors either 2 or congruent to 1 mod 4 (Fermat's theorem on sums of two squares).

### Condition 5: Parity of Pythagorean Parameters
In the (m,n) parametrization of each face's Pythagorean triple, the parameters must satisfy specific parity and coprimality conditions that severely constrain the search space.

### Condition 6: Sharipov's Cuboid Conjectures
Sharipov (2012) formulated three cuboid conjectures about the irreducibility of certain polynomials. If all three are valid, no perfect cuboid exists. The conjectures relate to the factorization of the cuboid equations under S3 symmetry.

### Condition 7: De Grey-Gibbs-Helm Aspect Ratio Exclusions
De Grey, Gibbs, and Helm (2024) showed that large proportions of aspect ratios of faces and internal rectangles cannot appear in a perfect cuboid, further restricting the search space.

## 4. Sharipov's S3-Symmetry Reduction

### 4.1 The S3 Symmetry
The perfect cuboid equations have a natural S3 symmetry group corresponding to permutations of edges (a, b, c) and the corresponding permutations of face diagonals (d_bc, d_ac, d_ab). This symmetry reduces the effective dimensionality of the search.

### 4.2 Multisymmetric Polynomial Factorization
Sharipov (2012, arXiv:1205.3135) showed the cuboid equations can be factorized using multisymmetric polynomials (symmetric in the edge variables). The elementary multisymmetric polynomials are:
- e1 = a^2 + b^2 + c^2 = d_s^2
- e2 = a^2*b^2 + a^2*c^2 + b^2*c^2
- e3 = a^2*b^2*c^2

### 4.3 Reduction to Degree-12 Equation
Through the S3-symmetry factorization, the system can be reduced. The face diagonal conditions require that a^2+b^2, a^2+c^2, and b^2+c^2 are all perfect squares. Using the multisymmetric polynomials, these conditions combined with a^2+b^2+c^2 = d_s^2 lead to a system that can be expressed as a single high-degree Diophantine equation in the multisymmetric variables. Specifically, the condition that the three face diagonals are integers, combined with the constraint on e1, e2, e3, reduces to finding integer points on an algebraic variety of degree 12 (the product of the three face-diagonal conditions, each degree 4 in the original variables after squaring).

The cuboid factor equations (Sharipov, arXiv:1209.5706) constitute a system of eight polynomial equations whose parametric solutions involve intersections of rational and elliptic curves.

## 5. Known Near-Miss Examples

| Edges (a, b, c) | Face Diagonals | Space Diagonal | Gap |
|-----------------|----------------|----------------|-----|
| (44, 117, 240) | (125, 244, 267) | 270.5920... | 0.5920 |
| (85, 132, 720) | (157, 725, 732) | 732.0000137... | 0.0000137 |
| (160, 231, 792) | (281, 808, 825) | 828.0024... | 0.0024 |
| (240, 252, 275) | (348, 365, 373) | 375.2666... | 0.2666 |
| (140, 480, 693) | (500, 707, 843) | 844.9988... | 0.0012 |
| (104, 153, 672) | (185, 680, 689) | 692.8201... | 0.8201 |
| (1008, 1100, 1155) | (1492, 1533, 1595) | 1885.0000... | ~0.0003 |

The near-miss (85, 132, 720) is notable: its space diagonal sqrt(85^2 + 132^2 + 720^2) = sqrt(535849) = 732.0000137..., missing an integer by only about 1.37 * 10^-5.

## 6. Cross-Domain Insights from ConceptEvolve

### Insight 1: CSP-Inspired Multi-Prime Sieve
The quadratic residue constraints across primes form a constraint satisfaction network. Arc consistency propagation (from CSP theory) applied to multi-prime sieving can achieve > 95% candidate elimination.

### Insight 2: Elliptic Curve Fibration
Fixing one edge reduces the problem to finding rational points on an elliptic curve. Parametric families correspond to rational sections. The Mordell-Weil rank of each fiber determines the density of near-misses.

### Insight 3: Brauer-Manin Obstruction
If the algebraic variety V defined by the cuboid equations has non-trivial Brauer group, this could provide a proof of non-existence independent of computational search. The bridge chain CSP → lattice points → Brauer obstruction connects empirical observations to theoretical impossibility.
