# Formal Mathematical Specification: The Perfect Cuboid Problem

## 1. Problem Statement

A **perfect cuboid** (also called a **perfect box** or **perfect Euler brick**) is a rectangular parallelepiped (box) with integer edges, integer face diagonals, and an integer space diagonal.

### 1.1 Variables

Let the three edge lengths of the box be:
- **a, b, c** ∈ ℤ⁺ (positive integers)

The three face diagonals are:
- **d** = diagonal of the a×b face
- **e** = diagonal of the b×c face
- **f** = diagonal of the a×c face

The space diagonal is:
- **g** = body diagonal of the box

### 1.2 Constraint Equations

The seven unknowns (a, b, c, d, e, f, g) must satisfy:

**Face diagonal equations (Pythagorean relations):**
1. a² + b² = d²
2. b² + c² = e²
3. a² + c² = f²

**Space diagonal equation:**
4. a² + b² + c² = g²

**Positivity constraint:**
5. a, b, c, d, e, f, g ∈ ℤ⁺

Note that equation (4) is not independent — it follows from any one face diagonal equation combined with the remaining edge. For example, from (1): d² = a² + b², so a² + b² + c² = d² + c², and the space diagonal equation becomes d² + c² = g².

### 1.3 Equivalent Formulation: Four Simultaneous Pythagorean Triples

The perfect cuboid requires **four Pythagorean triples** sharing legs:

| Triple | Legs | Hypotenuse |
|--------|------|------------|
| T₁ | (a, b) | d |
| T₂ | (b, c) | e |
| T₃ | (a, c) | f |
| T₄ | (d, c) or (a, e) or (b, f) | g |

These four triples must use only the **same three edge values** (a, b, c) as legs, with all hypotenuses (d, e, f, g) being integers.

### 1.4 Parametric Form via Pythagorean Triple Parametrization

Every primitive Pythagorean triple can be written as:
- (m² - n², 2mn, m² + n²) for coprime integers m > n > 0 with m - n odd

For the perfect cuboid, we need parameters (m₁, n₁), (m₂, n₂), (m₃, n₃) such that the three face triples share the correct leg values. Specifically:

- From T₁: {a, b} = {m₁² - n₁², 2m₁n₁}, d = m₁² + n₁²
- From T₂: {b, c} = {m₂² - n₂², 2m₂n₂}, e = m₂² + n₂²
- From T₃: {a, c} = {m₃² - n₃², 2m₃n₃}, f = m₃² + n₃²

The constraint that these triples share edge values creates a highly over-determined system.

## 2. Related Structures

### 2.1 Euler Brick (Face Cuboid)

An **Euler brick** satisfies only equations (1)-(3) — all face diagonals are integers, but the space diagonal need not be. Euler bricks are known to exist in infinite families.

**Smallest Euler brick:** (a, b, c) = (44, 117, 240) with face diagonals (125, 267, 244).

**Saunderson's parametric family** (1740): For any Pythagorean triple (u, v, w) with u² + v² = w²:
- a = u|4v² - w²|
- b = v|4u² - w²|
- c = 4uvw

This generates infinitely many Euler bricks, including (44, 117, 240) from (u,v,w) = (3,4,5).

**Euler's parametric family** (1770): Using two Pythagorean triples (p, q, r) and (s, t, u):
- a = ps
- b = qt
- c = ... (more complex expressions involving products)

### 2.2 Almost-Perfect Cuboids (Near-Misses)

Several types of near-misses are known:

- **Body cuboid**: edges and space diagonal integer, but one face diagonal irrational
- **Edge cuboid**: face diagonals and space diagonal integer, one edge irrational
- **Face cuboid** (= Euler brick): edges and face diagonals integer, space diagonal irrational

The best known near-misses for the full perfect cuboid come from Euler bricks where a² + b² + c² is close to a perfect square.

### 2.3 K3 Surface Formulation

The perfect cuboid problem can be reformulated as finding rational points on a specific K3 surface. Following van Luijk (2000) and Stoll-Testa:

The system of equations defines a surface S in projective space. After appropriate birational transformations, S is a K3 surface. The existence of a perfect cuboid is equivalent to the existence of a rational point on S outside the known trivial loci.

The Picard number and Néron-Severi lattice of this K3 surface have been studied. The Brauer-Manin obstruction is a potential mechanism for non-existence — the surface may have points over every local field ℚₚ but no global rational point.

## 3. Known Results

### 3.1 Existence Status
- **Open problem** as of 2026. No perfect cuboid has been found.
- No definitive proof of non-existence has been accepted by the mathematical community.
- Computational searches have verified non-existence for edges up to approximately 5 × 10¹¹ (Matson).

### 3.2 Necessary Conditions (Modular Constraints)
Following Kraitchik and subsequent work:

1. **Parity**: In a primitive perfect cuboid, exactly one edge is odd (WLOG, say c), the other two are even.
2. **Divisibility by 4**: At least one edge must be divisible by 4.
3. **Divisibility by 16**: The product abc must be divisible by 16.
4. **Mod 24/48**: Specific congruence conditions constrain possible residues.
5. **Prime divisors**: The product of the three edges must be divisible by 2⁴ · 3² · 5 · 7 · 11 · 13 · 17 · 19 · 29 · 37 (at minimum, the product of edges times diagonals must have many small prime factors).

### 3.3 Classical Sources

1. **Saunderson, N.** (1740). *The Elements of Algebra*. Cambridge. — First parametric family of Euler bricks.
2. **Euler, L.** (1770). *Vollständige Anleitung zur Algebra*. — Systematic study of integer-sided boxes and parametric solutions for Euler bricks.
3. **Kraitchik, M.** (1953). *On certain rational cuboids*. Scripta Mathematica, 19, 317-319. — Modular arithmetic constraints on perfect cuboids.

## 4. Computational Complexity

The naive search over all triples (a, b, c) with a ≤ b ≤ c ≤ N requires O(N³) operations. With the modular filter rejecting ~99% of candidates and the Pythagorean triple parametrization reducing the search to compatible triple pairs, the effective search space is much smaller but still exponential in the bit-length of the solution.

The problem has connections to:
- **Integer quadratic programming** (NP-hard in general)
- **Simultaneous Pell equations** (decidable but computationally hard)
- **Rational points on K3 surfaces** (no general algorithm known)
