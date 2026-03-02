"""Constraint propagation for the perfect cuboid problem.

Encodes the perfect cuboid conditions as integer constraints and uses
modular arithmetic plus number-theoretic constraints to prune the search space.
Implements constraint propagation without external SAT/SMT solvers.
"""

import math
import json
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import is_perfect_square
from src.modular_sieve import get_primes_up_to, compute_quadratic_residues


def build_allowed_residues(primes: list) -> dict:
    """For each prime p, build the set of (a%p, b%p, c%p) triples that pass
    all four quadratic residue constraints simultaneously."""
    allowed = {}
    for p in primes:
        qr = compute_quadratic_residues(p)
        valid = set()
        for a in range(p):
            a2 = (a * a) % p
            for b in range(p):
                b2 = (b * b) % p
                ab2 = (a2 + b2) % p
                if ab2 not in qr:
                    continue
                for c in range(p):
                    c2 = (c * c) % p
                    ac2 = (a2 + c2) % p
                    bc2 = (b2 + c2) % p
                    s2 = (a2 + b2 + c2) % p
                    if ac2 in qr and bc2 in qr and s2 in qr:
                        valid.add((a, b, c))
        allowed[p] = valid
        total = p ** 3
        print(f"  Prime {p:3d}: {len(valid):8d}/{total:8d} allowed ({len(valid)/total*100:.1f}%)")
    return allowed


def constraint_propagation_search(max_edge: int, num_primes: int = 10, verbose: bool = False):
    """Search using constraint propagation with pre-computed allowed residue triples.

    For each candidate (a, b, c), check membership in allowed sets for each prime.
    This is equivalent to multi-prime modular sieving but framed as constraint propagation.
    """
    primes = get_primes_up_to(50)[:num_primes]
    print(f"Building constraint tables for {len(primes)} primes...")
    allowed = build_allowed_residues(primes)

    results = []
    candidates_total = 0
    candidates_pruned = 0
    candidates_passed = 0
    perfect_found = False
    start_time = time.time()

    for a in range(1, max_edge + 1):
        for b in range(a, max_edge + 1):
            # Quick check: a^2 + b^2 must be a perfect square
            ab2 = a * a + b * b
            if not is_perfect_square(ab2):
                continue
            d_ab = math.isqrt(ab2)

            for c in range(b, max_edge + 1):
                candidates_total += 1

                # Constraint propagation: check all primes
                pruned = False
                for p in primes:
                    if (a % p, b % p, c % p) not in allowed[p]:
                        pruned = True
                        break

                if pruned:
                    candidates_pruned += 1
                    continue

                candidates_passed += 1

                # Exact checks
                ac2 = a * a + c * c
                bc2 = b * b + c * c

                if not is_perfect_square(ac2):
                    continue
                if not is_perfect_square(bc2):
                    continue

                # Euler brick found!
                d_ac = math.isqrt(ac2)
                d_bc = math.isqrt(bc2)
                s2 = a * a + b * b + c * c
                is_perfect = is_perfect_square(s2)

                if is_perfect:
                    perfect_found = True

                sd = math.sqrt(s2)
                frac = sd - math.floor(sd)
                gap = min(frac, 1.0 - frac)

                results.append({
                    "edges": [a, b, c],
                    "face_diagonals": [d_ab, d_ac, d_bc],
                    "space_diagonal": sd,
                    "is_perfect_cuboid": is_perfect,
                    "gap": gap,
                })

                if verbose:
                    status = "PERFECT!" if is_perfect else f"gap={gap:.8f}"
                    print(f"  Euler brick: ({a}, {b}, {c}) {status}")

    elapsed = time.time() - start_time

    return {
        "euler_bricks": results,
        "count": len(results),
        "perfect_cuboid_found": perfect_found,
        "max_edge": max_edge,
        "num_primes": num_primes,
        "primes_used": primes,
        "candidates_total": candidates_total,
        "candidates_pruned": candidates_pruned,
        "candidates_passed": candidates_passed,
        "pruning_rate": candidates_pruned / candidates_total if candidates_total > 0 else 0,
        "reduction_factor": candidates_total / candidates_passed if candidates_passed > 0 else float('inf'),
        "elapsed_seconds": elapsed,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-edge", type=int, default=1000)
    parser.add_argument("--num-primes", type=int, default=8)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    results = constraint_propagation_search(args.max_edge, args.num_primes, args.verbose)

    print(f"\nResults:")
    print(f"  Euler bricks: {results['count']}")
    print(f"  Perfect cuboid: {results['perfect_cuboid_found']}")
    print(f"  Total candidates: {results['candidates_total']}")
    print(f"  Pruned: {results['candidates_pruned']} ({results['pruning_rate']*100:.2f}%)")
    print(f"  Passed to exact check: {results['candidates_passed']}")
    print(f"  Reduction factor: {results['reduction_factor']:.1f}x")
    print(f"  Time: {results['elapsed_seconds']:.2f}s")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)


if __name__ == "__main__":
    main()
