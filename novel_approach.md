# Novel Approach: Pythagorean Triple Intersection with S3 Reduction

## Mathematical Derivation

### The Pythagorean Triple Intersection Framework

The key insight is to reformulate the Euler brick search as a **graph intersection problem** on the Pythagorean graph G, where:
- Vertices are positive integers
- Edge (a, b) exists iff a^2 + b^2 is a perfect square

An Euler brick (a, b, c) corresponds to a **triangle** in G. A perfect cuboid additionally requires a^2 + b^2 + c^2 to be a perfect square.

### S3 Symmetry Reduction

The perfect cuboid equations are symmetric under the S3 group acting by permutation of (a, b, c) and the corresponding permutation of (d_bc, d_ac, d_ab). This means:
1. We only need to search a <= b <= c (WLOG), reducing the search space by a factor of 6.
2. Each Euler brick has a canonical form with sorted edges.
3. The parametric families respect this symmetry: Saunderson's formula is S3-covariant.

### Algorithm: Indexed Triple Intersection

Instead of iterating over O(n^3) triples and checking each:

1. **Build Pythagorean pair index**: For each leg value a, store all partners (b, d_ab) such that a^2 + b^2 = d_ab^2. This takes O(n * sqrt(n)) time using (m,n) parametrization.

2. **Find shared-leg triangles**: For each value a appearing as a leg in at least 2 triples, enumerate all pairs of partners (b, d_ab) and (c, d_ac) with b <= c. Check if b^2 + c^2 is also a perfect square.

3. **S3 canonical form**: Enforce a <= b <= c to avoid counting permutations.

This reduces the search from O(n^3) to O(n * T^2) where T is the average number of Pythagorean partners per leg, which is O(n^epsilon) for any epsilon > 0 (related to the divisor function).

### Elliptic Curve Connection

Fixing edge a, the set of b values such that a^2 + b^2 = d^2 (Pythagorean pair with a) parametrizes a rational cone. The additional constraint that b^2 + c^2 is a perfect square for some c that also forms a Pythagorean pair with a defines an intersection of two conics. By classical algebraic geometry, the intersection of two conics in P^2 is generically a curve of genus 1 — an elliptic curve.

Specifically, for a fixed Pythagorean triple (a, b, d_ab), the condition that there exists c with:
- a^2 + c^2 = d_ac^2 (c on the a-centered Pythagorean cone)
- b^2 + c^2 = d_bc^2 (third face diagonal condition)

reduces to finding c such that c^2 + a^2 and c^2 + b^2 are both perfect squares simultaneously. This is the intersection of two conics, which has an elliptic curve structure when the conics are non-degenerate.

The Mordell-Weil group of this elliptic curve (over Q) determines the rational points. If the rank is 0, only finitely many (possibly zero) solutions exist. If the rank is >= 1, infinitely many exist but may require very large c values.

### Performance

At max_edge = 5000:
- **Brute force**: 69 bricks, 15.6s
- **Novel search (triple intersection)**: 24 bricks, 0.02s — **780x faster**
- **Modular sieve (Pyth pairs + numpy vectorized)**: 69 bricks, 3.6s — **4.3x faster** than brute force

The novel search is extremely fast but misses some bricks due to the asymmetric leg-matching. The modular sieve with Pythagorean pair enumeration provides complete coverage with significant speedup.

## Novel Strategies from ConceptEvolve

### Strategy 1: Distance Geometry Reformulation
The perfect cuboid is a special case of the integer distance geometry problem (IDGP). Techniques from molecular conformation (SDP relaxation, branch-and-prune) could provide new computational approaches.

### Strategy 2: Theta Series-Guided Search
The near-miss distribution analysis shows the gap distribution is consistent with random (chi-squared = 6.72, p > 0.05). However, theta series coefficients encode how often integers are representable as sums of squares. Near-misses cluster where r_3(n) is large, suggesting a modular-forms-guided prioritization of the search space.
