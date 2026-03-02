"""Novel search combining S3-symmetry reduction with elliptic curve perspective.

Exploits the S3 symmetry group of the cuboid equations to reduce redundant
permutations, and frames the search in terms of Pythagorean triple
intersections (the elliptic curve connection from De Grey-Gibbs-Helm 2024).
"""

import math
import json
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import Cuboid, is_perfect_square


def build_pythagorean_pair_index(max_val: int) -> dict:
    """Build index: for each integer n, store all (a, b) such that a^2 + b^2 = n^2.

    This is the key optimization: instead of iterating over all (a,b,c) and checking,
    we iterate over Pythagorean triples and look for intersections.
    """
    pairs = {}  # maps leg -> list of (other_leg, hypotenuse)
    for m in range(2, int(math.sqrt(max_val)) + 2):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue
            a_prim = m * m - n * n
            b_prim = 2 * m * n
            c_prim = m * m + n * n

            for k in range(1, max_val // c_prim + 1):
                a, b, c = k * a_prim, k * b_prim, k * c_prim
                if a > max_val or b > max_val:
                    continue
                pairs.setdefault(a, []).append((b, c))
                pairs.setdefault(b, []).append((a, c))
    return pairs


def novel_search(max_edge: int, verbose: bool = False):
    """Search for Euler bricks using Pythagorean triple intersection.

    For each pair of Pythagorean triples sharing a leg (say leg = a),
    with the other legs being b and c, check if (b, c) also form a
    Pythagorean pair. This is S3-reduced since we enforce a <= b <= c.

    The elliptic curve connection: fixing a, the set of b values such that
    (a, b, d_ab) is Pythagorean maps to points on a conic. Requiring a
    second triple (a, c, d_ac) with (b, c, d_bc) also Pythagorean is
    equivalent to intersecting two conics, which generically gives an
    elliptic curve.
    """
    start_time = time.time()

    pairs = build_pythagorean_pair_index(max_edge)

    results = []
    seen = set()
    candidates = 0
    perfect_found = False

    # For each value of a, find all b such that (a, b) is a Pythagorean pair
    for a in sorted(pairs.keys()):
        if a > max_edge:
            continue
        partners = pairs[a]  # list of (other_leg, hypotenuse) for Pythagorean triples with leg a

        # For each pair of partners (b, c) with b <= c,
        # check if b^2 + c^2 is also a perfect square
        for i in range(len(partners)):
            b, d_ab = partners[i]
            if b < a:
                continue  # enforce a <= b
            if b > max_edge:
                continue

            for j in range(i + 1, len(partners)):
                c, d_ac = partners[j]
                if c < b:
                    continue  # enforce b <= c
                if c > max_edge:
                    continue

                candidates += 1
                edges = (a, b, c)
                if edges in seen:
                    continue

                # Check if b^2 + c^2 is a perfect square
                bc2 = b * b + c * c
                if not is_perfect_square(bc2):
                    continue

                seen.add(edges)
                d_bc = math.isqrt(bc2)

                # Found an Euler brick!
                cuboid = Cuboid(a, b, c)
                is_perfect = cuboid.is_perfect_cuboid()
                if is_perfect:
                    perfect_found = True

                gap = cuboid.space_diagonal_gap()
                sd = cuboid.space_diagonal()

                result = {
                    "edges": list(edges),
                    "face_diagonals": [d_ab, d_ac, d_bc],
                    "space_diagonal": sd,
                    "space_diagonal_sq": cuboid.space_diagonal_sq,
                    "is_perfect_cuboid": is_perfect,
                    "gap": gap,
                }
                results.append(result)

                if verbose:
                    status = "PERFECT!" if is_perfect else f"gap={gap:.8f}"
                    print(f"  Euler brick: ({a}, {b}, {c}) diags=({d_ab}, {d_ac}, {d_bc}) {status}")

    elapsed = time.time() - start_time

    # Sort by gap
    results.sort(key=lambda x: x["gap"])

    return {
        "euler_bricks": results,
        "count": len(results),
        "perfect_cuboid_found": perfect_found,
        "max_edge": max_edge,
        "candidates_checked": candidates,
        "elapsed_seconds": elapsed,
        "search_rate": candidates / elapsed if elapsed > 0 else 0,
        "method": "pythagorean_triple_intersection_s3_reduced",
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Novel Euler brick search via triple intersection")
    parser.add_argument("--max-edge", type=int, default=5000)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print(f"Novel search: max_edge={args.max_edge}")
    results = novel_search(args.max_edge, args.verbose)

    print(f"\nResults:")
    print(f"  Euler bricks: {results['count']}")
    print(f"  Perfect cuboid: {results['perfect_cuboid_found']}")
    print(f"  Candidates: {results['candidates_checked']}")
    print(f"  Time: {results['elapsed_seconds']:.2f}s")

    if results['euler_bricks']:
        print(f"\n  Top 10 closest near-misses:")
        for r in results['euler_bricks'][:10]:
            print(f"    {r['edges']} gap={r['gap']:.10f}")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
