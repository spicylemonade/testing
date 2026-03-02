"""Experimental: Distance geometry reformulation of the perfect cuboid problem.

Inspired by ConceptEvolve's protein folding / distance geometry analogy.
The perfect cuboid can be seen as an integer distance geometry problem:
given pairwise distance constraints between 4 vertices of a rectangular box,
find integer edge lengths satisfying all constraints.

This prototype explores a "branch-and-bound" approach using modular constraints
as the bounding function.
"""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.cuboid import is_perfect_square, Cuboid
from src.modular_sieve import get_primes_up_to, compute_quadratic_residues


def sum_of_two_squares_representations(n: int, max_check: int = None) -> list:
    """Find all ways to write n = x^2 + y^2 with 0 < x <= y."""
    if max_check is None:
        max_check = int(math.isqrt(n))
    results = []
    for x in range(1, max_check + 1):
        rem = n - x * x
        if rem <= 0:
            break
        if rem >= x * x and is_perfect_square(rem):
            y = math.isqrt(rem)
            results.append((x, y))
    return results


def branch_and_bound_search(max_d_s: int, verbose: bool = False):
    """Search for perfect cuboids by iterating over possible space diagonal values.

    For each candidate d_s, decompose d_s^2 = a^2 + b^2 + c^2 and check if
    all face diagonals are also integers.

    The distance geometry perspective: d_s is the "diameter" of the box.
    """
    results = []
    for d_s in range(3, max_d_s + 1):
        d_s_sq = d_s * d_s

        # d_s^2 must be writable as a^2 + b^2 + c^2
        # Iterate over possible values of d_ab^2 = a^2 + b^2
        # Then c^2 = d_s^2 - d_ab^2, and we need c > 0 and c integer
        for d_ab in range(2, d_s):
            d_ab_sq = d_ab * d_ab
            c_sq = d_s_sq - d_ab_sq
            if c_sq <= 0:
                continue
            if not is_perfect_square(c_sq):
                continue
            c = math.isqrt(c_sq)

            # Now decompose d_ab^2 = a^2 + b^2
            reps = sum_of_two_squares_representations(d_ab_sq, c)
            for a, b in reps:
                if a > b:
                    a, b = b, a
                if b > c:
                    continue  # enforce a <= b <= c

                # Check remaining face diagonals
                ac_sq = a * a + c * c
                bc_sq = b * b + c * c
                if is_perfect_square(ac_sq) and is_perfect_square(bc_sq):
                    cuboid = Cuboid(a, b, c)
                    results.append({
                        "edges": [a, b, c],
                        "space_diagonal": d_s,
                        "is_perfect_cuboid": True,
                        "gap": 0.0,
                    })
                    if verbose:
                        print(f"PERFECT CUBOID: ({a}, {b}, {c}) d_s={d_s}")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-ds", type=int, default=2000, help="Max space diagonal")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print(f"Branch-and-bound search (distance geometry), max d_s={args.max_ds}")
    results = branch_and_bound_search(args.max_ds, args.verbose)
    if results:
        print(f"Found {len(results)} perfect cuboid(s)!")
        for r in results:
            print(f"  {r['edges']} d_s={r['space_diagonal']}")
    else:
        print("No perfect cuboid found.")
