# Survey of Known Modular Arithmetic Constraints on Perfect Cuboids

## 1. Parity and Divisibility by 2

For a **primitive** perfect cuboid (a, b, c, d, e, f, g) where gcd(a, b, c) = 1:

### 1.1 Edge Parity [kraitchik1945]
- Exactly **one edge is odd** (WLOG, say c)
- The other two edges (a, b) are **even**
- One even edge is divisible by **4** (WLOG, say b ≡ 0 mod 4)
- The other even edge is divisible by **16** (WLOG, say a ≡ 0 mod 16)

### 1.2 Diagonal Parity [kraitchik1945]
- Two face diagonals are **odd**: d = sqrt(a²+b²) and f = sqrt(a²+c²)
- One face diagonal is **even**: e = sqrt(b²+c²)
- The space diagonal g is **odd**

### 1.3 Divisibility by 4 and 16 [kraitchik1945, roberts2009]
- At least one edge divisible by 4
- At least one edge divisible by 16
- The product abc is divisible by 64 (= 4 × 16)

## 2. Odd Prime Divisibility Constraints

### 2.1 Divisibility by 3 [kraitchik1947]
- Two edges are divisible by 3
- At least one edge is divisible by 9
- The product abc is divisible by 27 (3³)

### 2.2 Divisibility by 5 [kraitchik1947]
- At least one edge is divisible by 5

### 2.3 Divisibility by 7 [roberts2009]
- At least one edge is divisible by 7

### 2.4 Divisibility by 11 [kraitchik1947]
- At least one edge is divisible by 11

### 2.5 Divisibility by 13 [roberts2009]
- One edge **or** the space diagonal must be divisible by 13

### 2.6 Divisibility by 17, 29, 37 [roberts2009]
- For each prime p ∈ {17, 29, 37}: at least one edge, face diagonal, or space diagonal must be divisible by p

### 2.7 Divisibility by 19 [roberts2009]
- At least one edge is divisible by 19

## 3. Product Divisibility (Leech's Constraint)

The product of all edges and face diagonals of a primitive perfect cuboid must be divisible by:

**2⁸ · 3⁴ · 5³ · 7 · 11 · 13 · 17 · 19 · 29 · 37**

This follows from combining the individual prime divisibility constraints. The exponents reflect the minimum guaranteed multiplicity of each prime across the seven quantities.

## 4. Congruence Conditions Modulo 24 and 48

### 4.1 Mod 24 Constraints [kraitchik1945]
The edge triple (a, b, c) modulo 24 is heavily constrained. In a primitive cuboid with a ≡ 0 (mod 16), b ≡ 0 (mod 4), c odd:

| Residue class | Constraint |
|---|---|
| a mod 24 | ∈ {0, 16} (since a ≡ 0 mod 16) |
| b mod 24 | ∈ {4, 8, 12, 20} (divisible by 4, not 16) |
| c mod 24 | ∈ {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23} (odd) |

Combined with the requirement that a²+b², b²+c², and a²+c² are all perfect squares, many of these residue combinations are eliminated.

### 4.2 Mod 48 Constraints [roberts2009]
Tighter constraints modulo 48 further reduce the search space. The divisibility by 16 of one edge combined with mod-3 constraints creates a sieve that eliminates over 99% of candidate triples.

## 5. Space Diagonal Constraints

### 5.1 Odd Prime Factors [roberts2009]
- The space diagonal g can **only** have prime factors congruent to 1 (mod 4)
- This is because g² = a² + b² + c² and each face diagonal is an integer, meaning g² is a sum of squares in multiple ways
- Primes p ≡ 3 (mod 4) cannot divide g to an odd power

### 5.2 Composite Requirement
- g is neither a prime power nor a product of two primes
- The edges a, b, c are all composite numbers (none can be prime)

## 6. Current Search Bounds

### 6.1 Matson's Bounds [matson2014]
- No perfect cuboid with odd edge < 2.5 × 10¹³
- No perfect cuboid with smallest even side < 5 × 10¹¹

### 6.2 Rathbun's Bounds [rathbun2017]
- Complete enumeration of all cuboid types for smallest edge up to ~2 × 10¹¹
- 167,043 cuboids found (none perfect)

### 6.3 Butler's Bounds [butler_web]
- Odd sides checked up to ~3 × 10¹²

## 7. Quadratic Residue Analysis

For each prime p, one can compute the set of quadratic residues mod p and determine which triples (a² mod p, b² mod p, c² mod p) can possibly satisfy all four equations simultaneously. Primes for which the surviving fraction is small provide the most effective sieve stages.

Roberts computed that analyzing quadratic residues mod p for small primes (p ≤ 37) already eliminates the vast majority of candidates [roberts2009]. The combined sieve across multiple primes achieves rejection rates exceeding 99%.

## 8. Implications for Computational Search

These constraints collectively mean that in any search range [1, N]:
- Only ~1/16 of triples satisfy the parity constraints
- Only ~1/3 satisfy divisibility by 3
- Only ~1/5 satisfy divisibility by 5, 1/7 for 7, etc.
- The combined filtering reduces the search space by a factor of approximately 10⁴ to 10⁵
- After filtering, the remaining candidates must be checked for whether a²+b², b²+c², a²+c² are perfect squares (computationally expensive)

## References

Cited entries correspond to keys in sources.bib:
- [kraitchik1945] Kraitchik, M. "On certain rational cuboids" (1945)
- [kraitchik1947] Kraitchik, M. *Théorie des Nombres* T. 3 (1947)
- [roberts2009] Roberts, T.S. "Some constraints on the existence of a perfect cuboid" (2009)
- [matson2014] Matson, R. "Results of computer search for a perfect cuboid" (2014)
- [rathbun2017] Rathbun, R. "The Integer Cuboid Table" (2017)
- [butler_web] Butler, B. "The Integer Brick Problem"
