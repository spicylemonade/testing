"""Elliptic curve parametric family generator for Euler bricks.

Generates Euler brick candidates by exploiting the elliptic curve structure
of the Pythagorean constraint system. Uses rational arithmetic to find
parametric families that produce Euler bricks beyond what Saunderson/Euler give.

The key idea: two Pythagorean equations sharing a leg define a curve of genus 1.
Rational points on this curve parametrize potential cuboid face pairs.
"""

import math
import sys
import os
from fractions import Fraction
from typing import List, Tuple, Set, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from space_diagonal import isqrt, near_miss_score, NearMissTracker
from euler_brick import verify_euler_brick, generate_pythagorean_triples
from metrics import SearchMetrics


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def rational_parametric_bricks(max_param: int = 200) -> List[Tuple[int, ...]]:
    """Generate Euler bricks via rational parametric families.

    Method: For each pair of Pythagorean triples (a1,b1,c1) and (a2,b2,c2),
    construct candidate bricks using products and ratios. This exploits the
    multiplicative structure of the sum-of-squares representation.

    Specifically, if a^2 + b^2 = c^2 and s^2 + t^2 = u^2, then:
    - (as)^2 + (bs)^2 = (cs)^2  (scaling)
    - (au - bt)^2 + (at + bu)^2 = (cu)^2  (Brahmagupta-Fibonacci identity)

    This gives us new Pythagorean triples that can share legs with existing ones.
    """
    triples = generate_pythagorean_triples(max_param)
    bricks = set()

    # For each pair of triples, use Brahmagupta-Fibonacci to create shared-leg systems
    for i, (a1, b1, c1) in enumerate(triples):
        for a2, b2, c2 in triples:
            # Using Brahmagupta-Fibonacci identity:
            # (a1*a2 - b1*b2)^2 + (a1*b2 + b1*a2)^2 = (c1*c2)^2
            # (a1*a2 + b1*b2)^2 + (a1*b2 - b1*a2)^2 = (c1*c2)^2

            x1 = abs(a1 * a2 - b1 * b2)
            y1 = abs(a1 * b2 + b1 * a2)
            x2 = abs(a1 * a2 + b1 * b2)
            y2 = abs(a1 * b2 - b1 * a2)
            h = c1 * c2

            # Now (x1, y1, h) and (x2, y2, h) are both Pythagorean triples
            # sharing hypotenuse h. This means:
            # x1^2 + y1^2 = h^2
            # x2^2 + y2^2 = h^2

            # If x1 == x2 or y1 == y2 or x1 == y2 or y1 == x2,
            # we get a shared leg, which is what we need for a cuboid face pair.

            # Approach: try to form cuboids with these as building blocks
            # For each triple, we also have the original scaled triples
            for ea, eb, ec in [
                (a1 * c2, b1 * c2, c1 * c2),  # first triple scaled
                (a2 * c1, b2 * c1, c1 * c2),  # second triple scaled
            ]:
                # Try to match with Brahmagupta products
                for pa, pb in [(x1, y1), (x2, y2), (y1, x1), (y2, x2)]:
                    # Check if ea matches pa (shared leg)
                    if ea == pa:
                        # Legs: eb, pb, shared leg ea
                        # Face1: ea^2 + eb^2 = ec^2 ✓
                        # Face2: ea^2 + pb^2 = h^2 ✓ (since pa=ea, pa^2+pb^2=h^2... wait)
                        # Actually (pa, pb, h) is a triple, and pa=ea, so:
                        # ea^2 + pb^2 = h^2
                        # We need: eb^2 + pb^2 = f^2 for some integer f
                        brick = verify_euler_brick(ea, eb, pb)
                        if brick:
                            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
                            bricks.add(edges)

                    if eb == pa:
                        brick = verify_euler_brick(ea, eb, pb)
                        if brick:
                            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
                            bricks.add(edges)

                    if ea == pb:
                        brick = verify_euler_brick(ea, eb, pa)
                        if brick:
                            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
                            bricks.add(edges)

    result = []
    for a, b, c in sorted(bricks):
        brick = verify_euler_brick(a, b, c)
        if brick:
            result.append(brick)
    return result


def extended_parametric_search(max_m: int = 100) -> List[Tuple[int, ...]]:
    """Extended search using multi-hop Pythagorean triple combinations.

    This generates triples at larger scales by composing the Brahmagupta-Fibonacci
    identity multiple times, finding Euler bricks that simple parametric families miss.
    """
    triples = generate_pythagorean_triples(max_m)
    bricks = set()

    # Build a leg-to-triples map for quick lookup
    from collections import defaultdict
    leg_map = defaultdict(list)

    # Include multiples up to a reasonable bound
    max_val = max_m * max_m * 2
    for a, b, c in triples:
        for k in range(1, max_val // c + 1):
            ka, kb, kc = k * a, k * b, k * c
            leg_map[ka].append((ka, kb, kc))
            leg_map[kb].append((kb, ka, kc))

    # For each shared leg, try to form cuboids
    for leg_val, leg_triples in leg_map.items():
        for i in range(len(leg_triples)):
            _, other_a, hyp_a = leg_triples[i]
            for j in range(i + 1, len(leg_triples)):
                _, other_b, hyp_b = leg_triples[j]

                # Check third face diagonal
                if isqrt(other_a * other_a + other_b * other_b) is not None:
                    edges = tuple(sorted([leg_val, other_a, other_b]))
                    bricks.add(edges)

    result = []
    for a, b, c in sorted(bricks):
        brick = verify_euler_brick(a, b, c)
        if brick:
            result.append(brick)
    return result


def run_elliptic_search():
    """Run the elliptic curve parametric family search."""
    from euler_brick import generate_saunderson_bricks, generate_euler_two_triple_bricks

    metrics = SearchMetrics(method="elliptic_families")
    tracker = NearMissTracker(k=200)
    metrics.start_timer()

    # Generate bricks from classical families for comparison
    saunderson = set()
    for brick in generate_saunderson_bricks(50):
        edges = tuple(sorted([brick[0], brick[1], brick[2]]))
        saunderson.add(edges)

    euler_classic = set()
    for brick in generate_euler_two_triple_bricks(30):
        edges = tuple(sorted([brick[0], brick[1], brick[2]]))
        euler_classic.add(edges)

    classical = saunderson | euler_classic

    # Generate from our extended methods
    print("Generating bricks via Brahmagupta-Fibonacci parametric families...")
    bf_bricks = rational_parametric_bricks(150)
    bf_edges = {tuple(sorted([b[0], b[1], b[2]])) for b in bf_bricks}

    print("Generating bricks via extended multi-hop search...")
    ext_bricks = extended_parametric_search(200)
    ext_edges = {tuple(sorted([b[0], b[1], b[2]])) for b in ext_bricks}

    all_new = (bf_edges | ext_edges) - classical
    all_bricks = bf_edges | ext_edges | classical

    metrics.euler_bricks_found = len(all_bricks)
    metrics.total_candidates = len(bf_edges) + len(ext_edges)

    # Check all for perfect cuboid property
    for edges in all_bricks:
        a, b, c = edges
        score = near_miss_score(a, b, c)
        tracker.add(a, b, c, score)
        g = isqrt(a * a + b * b + c * c)
        if g is not None:
            metrics.perfect_cuboids_found += 1
            print(f"*** PERFECT CUBOID FOUND: ({a}, {b}, {c}) ***")

    metrics.stop_timer()

    print(f"\nResults:")
    print(f"  Classical families: {len(classical)} bricks")
    print(f"  Brahmagupta-Fibonacci: {len(bf_edges)} bricks")
    print(f"  Extended multi-hop: {len(ext_edges)} bricks")
    print(f"  New (not in classical): {len(all_new)} bricks")
    print(f"  Total unique: {len(all_bricks)} bricks")
    print(f"  Perfect cuboids: {metrics.perfect_cuboids_found}")
    print(f"  Time: {metrics.wall_clock_seconds:.2f}s")

    metrics.save("results/elliptic_families_metrics.json")

    return all_bricks, all_new, metrics, tracker


if __name__ == "__main__":
    all_bricks, new_bricks, metrics, tracker = run_elliptic_search()

    print(f"\nTop 10 near-misses from elliptic families:")
    for score, (a, b, c) in tracker.get_top(10):
        s = a * a + b * b + c * c
        print(f"  ({a}, {b}, {c}) score={score:.6e} sqrt(s)={math.sqrt(s):.4f}")
