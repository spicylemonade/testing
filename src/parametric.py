"""Parametric family generators for Euler brick families.

Implements Saunderson's, Euler's, and modern parametric families.
For each family, generates Euler bricks and checks for perfect cuboid property.
"""

import math
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import Cuboid, is_perfect_square


def saunderson_family(max_param: int = 200):
    """Saunderson's (1740) parametric family.

    Given Pythagorean triple (u, v, w) with u^2 + v^2 = w^2:
        a = |u(4v^2 - w^2)|
        b = |v(4u^2 - w^2)|
        c = |4uvw|
    """
    results = []
    # Generate Pythagorean triples using (m, n) parametrization
    for m in range(2, max_param):
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if math.gcd(m, n) != 1:
                continue
            u = m * m - n * n
            v = 2 * m * n
            w = m * m + n * n

            a = abs(u * (4 * v * v - w * w))
            b = abs(v * (4 * u * u - w * w))
            c = abs(4 * u * v * w)

            if a == 0 or b == 0 or c == 0:
                continue

            edges = sorted([a, b, c])
            cuboid = Cuboid(*edges)
            if cuboid.is_euler_brick():
                results.append({
                    "family": "saunderson",
                    "params": {"m": m, "n": n, "u": u, "v": v, "w": w},
                    "edges": edges,
                    "is_perfect": cuboid.is_perfect_cuboid(),
                    "gap": cuboid.space_diagonal_gap(),
                })
    return results


def euler_family_1(max_param: int = 200):
    """Euler's first parametric family (1770).

    For parameters (p, q) with p > q > 0:
        a = |p^4 - 6p^2*q^2 + q^4|
        b = |4pq(p^2 - q^2)|
        c = |2pq(p^2 + q^2)| -- not always Euler brick, check
    Actually, Euler's families are more complex. We use a known parametric form:
        Given coprime m, n with m > n > 0, m-n odd:
        a = m^2 - n^2, b = 2mn, c = m^2 + n^2 gives one Pythagorean triple.
    We combine two Pythagorean triples sharing a leg to build Euler bricks.
    """
    results = []
    # Build a map: leg -> list of Pythagorean triples containing that leg
    leg_to_triples = {}
    for m in range(2, max_param):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            # a and b are legs, c is hypotenuse
            for k in range(1, max_param // max(a, b) + 1):
                ka, kb, kc = k * a, k * b, k * c
                leg_to_triples.setdefault(ka, []).append((ka, kb, kc))
                leg_to_triples.setdefault(kb, []).append((kb, ka, kc))

    # Find pairs of triples sharing a leg — this gives face diagonals for two faces
    seen = set()
    for shared_leg, triples in leg_to_triples.items():
        if len(triples) < 2:
            continue
        for i in range(len(triples)):
            for j in range(i + 1, len(triples)):
                _, b1, c1 = triples[i]
                _, b2, c2 = triples[j]
                # Edges are: shared_leg (a), b1, b2
                # Face diags: c1 (for a,b1), c2 (for a,b2)
                # Need b1^2 + b2^2 to be perfect square too
                if is_perfect_square(b1 * b1 + b2 * b2):
                    edges = sorted([shared_leg, b1, b2])
                    key = tuple(edges)
                    if key not in seen:
                        seen.add(key)
                        cuboid = Cuboid(*edges)
                        if cuboid.is_euler_brick():
                            results.append({
                                "family": "euler_shared_leg",
                                "edges": list(edges),
                                "is_perfect": cuboid.is_perfect_cuboid(),
                                "gap": cuboid.space_diagonal_gap(),
                            })
    return results


def bremner_family(max_param: int = 100):
    """Family based on Bremner (1988) approach via cubic surfaces.

    Uses the observation that if (a, b, d_ab) and (a, c, d_ac) are
    Pythagorean triples, we need b^2 + c^2 = d_bc^2. We parametrize
    using two Pythagorean families sharing edge a.
    """
    results = []
    seen = set()

    for m1 in range(2, max_param):
        for n1 in range(1, m1):
            if (m1 - n1) % 2 == 0 or math.gcd(m1, n1) != 1:
                continue
            # First triple: (m1^2-n1^2, 2*m1*n1, m1^2+n1^2)
            leg1_a = m1 * m1 - n1 * n1
            leg1_b = 2 * m1 * n1

            for m2 in range(2, max_param):
                for n2 in range(1, m2):
                    if (m2 - n2) % 2 == 0 or math.gcd(m2, n2) != 1:
                        continue
                    leg2_a = m2 * m2 - n2 * n2
                    leg2_b = 2 * m2 * n2

                    # Try matching legs to form an Euler brick
                    # Case: shared edge = leg1_a * k1 = leg2_a * k2
                    g = math.gcd(leg1_a, leg2_a)
                    if g == 0:
                        continue
                    k1 = leg2_a // g
                    k2 = leg1_a // g
                    a = leg1_a * k1
                    b = leg1_b * k1
                    c = leg2_b * k2

                    if a > 0 and b > 0 and c > 0:
                        if is_perfect_square(b * b + c * c):
                            edges = sorted([a, b, c])
                            key = tuple(edges)
                            if key not in seen:
                                seen.add(key)
                                cuboid = Cuboid(*edges)
                                if cuboid.is_euler_brick():
                                    results.append({
                                        "family": "bremner_shared_edge",
                                        "params": {"m1": m1, "n1": n1, "m2": m2, "n2": n2},
                                        "edges": list(edges),
                                        "is_perfect": cuboid.is_perfect_cuboid(),
                                        "gap": cuboid.space_diagonal_gap(),
                                    })
    return results


def generate_all_families(max_param: int = 50):
    """Generate Euler bricks from all parametric families."""
    all_results = []
    seen_edges = set()

    print("Generating Saunderson family...")
    for r in saunderson_family(max_param):
        key = tuple(r["edges"])
        if key not in seen_edges:
            seen_edges.add(key)
            all_results.append(r)

    print(f"  Found {len(all_results)} bricks from Saunderson")

    print("Generating Euler shared-leg family...")
    count_before = len(all_results)
    for r in euler_family_1(max_param):
        key = tuple(r["edges"])
        if key not in seen_edges:
            seen_edges.add(key)
            all_results.append(r)
    print(f"  Found {len(all_results) - count_before} new bricks from Euler")

    print("Generating Bremner shared-edge family...")
    count_before = len(all_results)
    for r in bremner_family(min(max_param, 30)):
        key = tuple(r["edges"])
        if key not in seen_edges:
            seen_edges.add(key)
            all_results.append(r)
    print(f"  Found {len(all_results) - count_before} new bricks from Bremner")

    # Sort by gap (closest near-miss first)
    all_results.sort(key=lambda x: x["gap"])

    return all_results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-param", type=int, default=50)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    results = generate_all_families(args.max_param)

    print(f"\nTotal unique Euler bricks: {len(results)}")
    perfect = [r for r in results if r["is_perfect"]]
    if perfect:
        print(f"PERFECT CUBOIDS FOUND: {len(perfect)}")
        for p in perfect:
            print(f"  {p['edges']}")
    else:
        print("No perfect cuboid found.")

    if results:
        print(f"\nTop 10 closest near-misses:")
        for r in results[:10]:
            print(f"  {r['edges']} ({r['family']}) gap={r['gap']:.10f}")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump({"parametric_bricks": results, "total": len(results)}, f, indent=2)


if __name__ == "__main__":
    main()
