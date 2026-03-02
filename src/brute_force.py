"""Brute-force Euler brick finder with modular pre-filtering.

Systematically searches for Euler bricks up to a given edge bound and checks
each for the perfect cuboid property (integer space diagonal).
"""

import json
import math
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import is_perfect_square, Cuboid


def find_euler_bricks(max_edge: int, use_filters: bool = True, verbose: bool = False):
    """Find all Euler bricks with 1 <= a <= b <= c <= max_edge.

    Uses modular pre-filtering to skip candidates that cannot produce
    integer face diagonals.

    Returns:
        List of dicts with edges, diagonals, and near-miss info.
    """
    results = []
    candidates_checked = 0
    candidates_filtered = 0
    perfect_found = False
    start_time = time.time()

    for a in range(1, max_edge + 1):
        a2 = a * a
        for b in range(a, max_edge + 1):
            b2 = b * b
            ab2 = a2 + b2

            # Filter 1: a^2 + b^2 must be a perfect square
            if not is_perfect_square(ab2):
                candidates_filtered += 1
                continue

            d_ab = math.isqrt(ab2)

            for c in range(b, max_edge + 1):
                candidates_checked += 1
                c2 = c * c

                # Filter 2: a^2 + c^2 must be a perfect square
                ac2 = a2 + c2
                if not is_perfect_square(ac2):
                    candidates_filtered += 1
                    continue

                # Filter 3: b^2 + c^2 must be a perfect square
                bc2 = b2 + c2
                if not is_perfect_square(bc2):
                    candidates_filtered += 1
                    continue

                # Found an Euler brick!
                d_ac = math.isqrt(ac2)
                d_bc = math.isqrt(bc2)
                sd_sq = a2 + b2 + c2
                sd = math.sqrt(sd_sq)
                is_perfect = is_perfect_square(sd_sq)

                if is_perfect:
                    perfect_found = True

                frac = sd - math.floor(sd)
                gap = min(frac, 1.0 - frac)

                result = {
                    "edges": [a, b, c],
                    "face_diagonals": [d_ab, d_ac, d_bc],
                    "space_diagonal": sd,
                    "space_diagonal_sq": sd_sq,
                    "is_perfect_cuboid": is_perfect,
                    "gap": gap,
                }
                results.append(result)

                if verbose:
                    status = "PERFECT!" if is_perfect else f"gap={gap:.8f}"
                    print(f"  Euler brick: ({a}, {b}, {c}) diags=({d_ab}, {d_ac}, {d_bc}) sd={sd:.4f} {status}")

    elapsed = time.time() - start_time
    return {
        "euler_bricks": results,
        "count": len(results),
        "perfect_cuboid_found": perfect_found,
        "max_edge": max_edge,
        "candidates_checked": candidates_checked,
        "candidates_filtered": candidates_filtered,
        "elapsed_seconds": elapsed,
        "search_rate": candidates_checked / elapsed if elapsed > 0 else 0,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Brute-force Euler brick search")
    parser.add_argument("--max-edge", type=int, default=1000, help="Maximum edge length")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print each brick found")
    args = parser.parse_args()

    print(f"Searching for Euler bricks with max edge = {args.max_edge}...")
    results = find_euler_bricks(args.max_edge, verbose=args.verbose)

    print(f"\nResults:")
    print(f"  Euler bricks found: {results['count']}")
    print(f"  Perfect cuboid found: {results['perfect_cuboid_found']}")
    print(f"  Candidates checked: {results['candidates_checked']}")
    print(f"  Candidates filtered: {results['candidates_filtered']}")
    print(f"  Time: {results['elapsed_seconds']:.2f}s")
    print(f"  Rate: {results['search_rate']:.0f} candidates/s")

    if results['euler_bricks']:
        best = min(results['euler_bricks'], key=lambda x: x['gap'])
        print(f"  Closest near-miss: ({best['edges']}) gap={best['gap']:.10f}")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  Results saved to {args.output}")


if __name__ == "__main__":
    main()
