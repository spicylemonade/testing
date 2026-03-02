# Survey of Computational and Algorithmic Approaches for Perfect Cuboid Search

## 1. Butler's Even-Side Enumeration [butler_web]

### Algorithm Description
Butler's approach systematically enumerates candidate edge triples by exploiting the known divisibility constraints on even edges. The algorithm:

1. **Subdivides by parity class**: One edge must be divisible by 16, another by 4 (not 16), and the third is odd. This creates three classes of candidate triples.
2. **Enumerate the "16-edge"**: Loop over a = 16, 32, 48, ..., up to the bound.
3. **Enumerate the "4-edge"**: For each a, loop over b = 4, 8, 12, ... (not divisible by 16).
4. **Check face diagonal**: Compute a² + b² and test if it's a perfect square. If not, skip.
5. **Enumerate the odd edge**: For each valid (a, b), enumerate c = 1, 3, 5, ...
6. **Check remaining face diagonals and space diagonal**: Test b² + c² and a² + c² for perfect squareness, then a² + b² + c².

### Key Optimizations
- Uses the C `hypot` function for fast hypotenuse computation
- Flags candidates where the hypotenuse is within 1 part in 10¹² of an integer
- Only 181 bits of precision needed to search up to 10¹⁴

### Complexity
- **Time complexity**: O(N² · f(N)) where N is the bound and f(N) accounts for face-diagonal filtering. In practice, the face diagonal filter rejects ~99.97% of (a, b) pairs.
- **Search range achieved**: Odd sides up to ~3 × 10¹²

### Cite: [butler_web]

## 2. Rathbun's Parametric Search [rathbun2017]

### Algorithm Description
Rathbun's approach uses the **Pythagorean group Py(n)** framework to enumerate all cuboid types systematically:

1. **Pythagorean triple enumeration**: Generate all primitive Pythagorean triples (a, b, c) with c = m² + n² ≤ N using the (m, n) parametrization.
2. **Common-leg matching**: Index triples by each leg value. Two triples sharing a common leg a define a potential cuboid face pair: if (a, b₁, c₁) and (a, b₂, c₂) are both primitive triples, then edges (b₁, b₂, a) have two integer face diagonals.
3. **Third face + space diagonal check**: For each matched pair, check if b₁² + b₂² is a perfect square (third face diagonal) and if a² + b₁² + b₂² is a perfect square (space diagonal).

### Key Optimizations
- Pre-computation of all Pythagorean triples and hash-based indexing by leg values
- Separate tracking of different cuboid types (body, face, edge)
- Efficient GCD computation for primitivity testing

### Complexity
- **Time complexity**: O(N · log(N)) for triple generation, O(K²) for pair matching where K is the average number of triples sharing a leg value.
- **Search range achieved**: Smallest edge up to ~2 × 10¹¹
- **Results**: 167,043 cuboids found across all types, 0 perfect cuboids

### Cite: [rathbun2017]

## 3. Matson's Hash-Table Sieving [matson2014]

### Algorithm Description
Matson extended Butler's algorithm with hash-table-based sieving:

1. **Modular pre-sieve**: Apply all known modular constraints (mod 16, mod 3, mod 5, mod 7, etc.) to eliminate candidates before any floating-point computation.
2. **Hash-table of perfect squares**: Pre-compute a hash table of squares mod M for a large modulus M. Before computing sqrt, check if a² + b² ≡ k² (mod M) for any k — this rejects non-squares quickly.
3. **Multi-precision verification**: Only candidates surviving the hash-table sieve undergo full-precision integer square root testing.
4. **Statistical tracking**: Record near-miss statistics (how many bits match in the best cases) to assess the probability of a solution existing at larger scales.

### Key Optimizations
- The hash-table sieve rejects ~99.99% of candidates that pass the modular pre-sieve
- Multi-level hashing with different moduli catches different types of non-squares
- Parallelization across independent ranges

### Complexity
- **Time complexity**: O(N²/S) where S is the combined sieve rejection factor (~10⁴-10⁵)
- **Search range achieved**: Odd edge up to 2.5 × 10¹³, even side up to 5 × 10¹¹
- **Key finding**: Near-misses become rarer with increasing edge size, suggesting non-existence

### Cite: [matson2014]

## 4. Elliptic Curve Parametric Family Generation [colman1971, sharipov2021]

### Algorithm Description
The elliptic curve approach generates Euler brick candidates from rational points on elliptic curves:

1. **Curve construction**: Each pair of face diagonal equations (e.g., a² + b² = d² and b² + c² = e²) defines a biquadratic curve. By fixing one variable and parametrizing, this reduces to an elliptic curve.
2. **Rational point generation**: Find rational points on the elliptic curve using:
   - Known torsion points
   - 2-descent to find generators of the Mordell-Weil group
   - Height-based search for points of small height
3. **Scaling to integers**: Each rational point (a/d, b/d, c/d) is scaled by the common denominator to produce integer Euler brick candidates.
4. **Space diagonal test**: Check a² + b² + c² for perfect squareness.

### Key Optimizations
- Group law on the elliptic curve generates infinitely many candidates from a single generator
- Multi-descent techniques find generators more efficiently
- Parametric families from different curves produce non-overlapping Euler bricks

### Complexity
- **Time complexity**: O(H²) for finding rational points up to height H on a single curve; generating K points from a rank-r curve takes O(K^(1/r)) time per point.
- **Search range achieved**: Can generate Euler bricks with edges up to ~10²⁰ efficiently, but the space diagonal check has the same difficulty as brute force.
- **Results**: Produces Euler bricks not found by Saunderson/Euler families, but no perfect cuboids.

### Cite: [colman1971, sharipov2021]

## 5. Comparison Table

| Method | Search Parameter | Range Achieved | Candidates/sec | Key Strength |
|---|---|---|---|---|
| Butler enumeration | Odd side | 3 × 10¹² | ~10⁷ | Simple, complete coverage |
| Rathbun parametric | Smallest edge | 2 × 10¹¹ | ~10⁶ | Finds all cuboid types |
| Matson hash-sieve | Odd edge | 2.5 × 10¹³ | ~10⁸ (post-sieve) | Deepest search, statistics |
| Elliptic curves | Parametric | ~10²⁰ (per family) | ~10³ curves | Explores non-brute-force space |

## 6. Implications for Our Implementation

Based on this survey, our implementation strategy should:

1. **Start with Rathbun-style triple matching** (item_012) for completeness and comparison against published catalogs
2. **Layer Matson-style hash sieving** (items 008, 016) for maximum throughput
3. **Include elliptic curve families** (item_013) to explore parametric space beyond brute force
4. **Combine all methods** (item_018) for the most efficient search pipeline

## References

All cited keys correspond to entries in sources.bib.
