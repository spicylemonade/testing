"""Modular arithmetic sieve for aggressive candidate filtering.

Combines two key optimizations:
1. Pythagorean triple enumeration (skip non-Pythagorean (a,b) pairs entirely)
2. Multi-prime modular sieve on c values using numpy vectorization
"""

import math
import time
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import is_perfect_square


def compute_quadratic_residues(p: int) -> set:
    """Compute the set of quadratic residues mod p."""
    return {(x * x) % p for x in range(p)}


def build_sieve_tables(primes: list) -> dict:
    """Build quadratic residue lookup tables for a list of primes."""
    tables = {}
    for p in primes:
        qr = compute_quadratic_residues(p)
        tables[p] = qr
    return tables


def get_primes_up_to(n: int) -> list:
    """Sieve of Eratosthenes."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def generate_pythagorean_pairs(max_leg: int):
    """Generate all (a, b, hyp) where a <= b and a^2+b^2 = hyp^2, with a,b <= max_leg.

    Uses (m,n) parametrization for primitive triples, then scales.
    """
    pairs = {}  # maps (a, b) -> hyp, with a <= b
    for m in range(2, int(math.sqrt(2 * max_leg)) + 2):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue
            a0 = m * m - n * n
            b0 = 2 * m * n
            c0 = m * m + n * n
            if a0 > b0:
                a0, b0 = b0, a0
            for k in range(1, max_leg // a0 + 1):
                a, b, c = k * a0, k * b0, k * c0
                if a > max_leg or b > max_leg:
                    break
                if a > b:
                    a, b = b, a
                pairs[(a, b)] = c
    return pairs


def find_euler_bricks_sieved(max_edge: int, num_primes: int = 25, verbose: bool = False):
    """Find Euler bricks using Pythagorean pair enumeration + multi-prime modular sieve.

    Step 1: Enumerate all Pythagorean pairs (a, b) with a <= b <= max_edge.
    Step 2: For each pair, use vectorized modular sieve to filter c candidates.
    Step 3: Exact check on survivors.
    """
    primes = get_primes_up_to(100)[:num_primes]

    # Build numpy-friendly QR tables
    qr_masks = {}
    for p in primes:
        qr = compute_quadratic_residues(p)
        mask = np.zeros(p, dtype=bool)
        for x in qr:
            mask[x] = True
        qr_masks[p] = mask

    qr_sets = build_sieve_tables(primes)

    # Step 1: Enumerate Pythagorean pairs
    pyth_pairs = generate_pythagorean_pairs(max_edge)

    results = []
    total_c_candidates = 0
    total_c_sieved = 0
    total_c_exact_checked = 0
    perfect_found = False
    start_time = time.time()

    for (a, b), d_ab in sorted(pyth_pairs.items()):
        a2 = a * a
        b2 = b * b
        ab2 = a2 + b2

        # c ranges from b to max_edge
        c_start = b
        c_end = max_edge
        if c_start > c_end:
            continue

        c_arr = np.arange(c_start, c_end + 1, dtype=np.int64)
        n_c = len(c_arr)
        total_c_candidates += n_c

        c2_arr = c_arr * c_arr
        ac2_arr = np.int64(a2) + c2_arr
        bc2_arr = np.int64(b2) + c2_arr

        # Vectorized modular sieve
        mask = np.ones(n_c, dtype=bool)
        for p in primes:
            qr_mask = qr_masks[p]
            ac_mod = (ac2_arr % p).astype(np.intp)
            bc_mod = (bc2_arr % p).astype(np.intp)
            mask &= qr_mask[ac_mod]
            mask &= qr_mask[bc_mod]
            if not mask.any():
                break

        n_sieved = n_c - int(mask.sum())
        total_c_sieved += n_sieved

        # Exact check on survivors
        surviving_indices = np.where(mask)[0]
        for idx in surviving_indices:
            c = int(c_arr[idx])
            c2 = c * c
            ac2 = a2 + c2
            bc2 = b2 + c2
            total_c_exact_checked += 1

            if not is_perfect_square(ac2):
                continue
            if not is_perfect_square(bc2):
                continue

            # Euler brick found!
            d_ac = math.isqrt(ac2)
            d_bc = math.isqrt(bc2)
            s2 = ab2 + c2
            is_perfect = is_perfect_square(s2)
            if is_perfect:
                perfect_found = True

            sd = math.sqrt(s2)
            frac = sd - math.floor(sd)
            gap = min(frac, 1.0 - frac)

            results.append({
                "edges": sorted([a, b, c]),
                "face_diagonals": [d_ab, d_ac, d_bc],
                "space_diagonal": sd,
                "space_diagonal_sq": s2,
                "is_perfect_cuboid": is_perfect,
                "gap": gap,
            })

            if verbose:
                status = "PERFECT!" if is_perfect else f"gap={gap:.8f}"
                print(f"  Euler brick: ({a}, {b}, {c}) diags=({d_ab}, {d_ac}, {d_bc}) {status}")

    elapsed = time.time() - start_time
    sieve_rate = total_c_sieved / total_c_candidates if total_c_candidates > 0 else 0

    # Deduplicate (some bricks may be found via different (a,b) orderings)
    seen = set()
    unique_results = []
    for r in results:
        key = tuple(sorted(r["edges"]))
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return {
        "euler_bricks": unique_results,
        "count": len(unique_results),
        "perfect_cuboid_found": perfect_found,
        "max_edge": max_edge,
        "num_primes": num_primes,
        "primes_used": primes,
        "total_pythagorean_pairs": len(pyth_pairs),
        "total_c_candidates": total_c_candidates,
        "candidates_sieved": total_c_sieved,
        "sieve_rate": sieve_rate,
        "candidates_checked": total_c_exact_checked,
        "total_considered": total_c_candidates,
        "elapsed_seconds": elapsed,
        "search_rate": total_c_candidates / elapsed if elapsed > 0 else 0,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Modular sieve Euler brick search")
    parser.add_argument("--max-edge", type=int, default=1000)
    parser.add_argument("--num-primes", type=int, default=25)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print(f"Sieved search: max_edge={args.max_edge}, primes={args.num_primes}")
    results = find_euler_bricks_sieved(args.max_edge, args.num_primes, args.verbose)

    print(f"\nResults:")
    print(f"  Euler bricks: {results['count']}")
    print(f"  Perfect cuboid: {results['perfect_cuboid_found']}")
    print(f"  Pythagorean pairs: {results['total_pythagorean_pairs']}")
    print(f"  C candidates: {results['total_c_candidates']}")
    print(f"  Sieved out: {results['candidates_sieved']} ({results['sieve_rate']*100:.1f}%)")
    print(f"  Exact checks: {results['candidates_checked']}")
    print(f"  Time: {results['elapsed_seconds']:.2f}s")
    print(f"  Rate: {results['search_rate']:.0f} candidates/s")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"  Saved to {args.output}")


if __name__ == "__main__":
    main()
