"""Advanced Pythagorean triple decomposition search for perfect cuboids.

Uses the (m,n) parametrization to enumerate all Pythagorean triples,
indexes by legs, finds pairs sharing common legs, then checks for cuboids.
"""

import math
import sys
import os
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from space_diagonal import isqrt, is_perfect, near_miss_score, NearMissTracker
from metrics import SearchMetrics


def generate_all_pythagorean_triples(max_hyp: int) -> List[Tuple[int, int, int]]:
    """Generate all primitive Pythagorean triples with hypotenuse <= max_hyp."""
    triples = []
    max_m = int(math.isqrt(max_hyp)) + 1
    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if math.gcd(m, n) != 1:
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            if c > max_hyp:
                break
            triples.append((min(a, b), max(a, b), c))
    return triples


def build_leg_index(triples: List[Tuple[int, int, int]], max_edge: int
                    ) -> Dict[int, List[Tuple[int, int, int]]]:
    """Index Pythagorean triples by each leg value.

    For each triple (a, b, c), create entries for legs a and b,
    including all multiples k*(a,b,c) where k*max(a,b) <= max_edge.
    """
    leg_index = defaultdict(list)
    for a, b, c in triples:
        # Add all multiples
        for k in range(1, max_edge // max(a, b) + 1):
            ka, kb, kc = k * a, k * b, k * c
            if ka > max_edge or kb > max_edge:
                break
            # Index by each leg
            leg_index[ka].append((ka, kb, kc))
            leg_index[kb].append((kb, ka, kc))
    return leg_index


def find_euler_bricks_via_triples(max_edge: int, max_hyp: int = None
                                  ) -> Tuple[List[Tuple], SearchMetrics, NearMissTracker]:
    """Find Euler bricks by matching Pythagorean triples sharing common legs.

    For a box with edges (a, b, c):
    - Face ab needs a^2+b^2 = d^2  -> triple (a, b, d)
    - Face bc needs b^2+c^2 = e^2  -> triple (b, c, e)
    - Face ac needs a^2+c^2 = f^2  -> triple (a, c, f)

    Strategy: index triples by legs, for each leg value b, find all pairs
    of triples (b, a, d) and (b, c, e), then check if a^2+c^2 is a perfect square.
    """
    if max_hyp is None:
        max_hyp = int(max_edge * math.sqrt(2)) + 1

    metrics = SearchMetrics(method="triple_decomposition", search_bound=max_edge)
    tracker = NearMissTracker(k=200)
    euler_bricks = []
    perfect_cuboids = []

    metrics.start_timer()

    # Generate primitive triples
    prim_triples = generate_all_pythagorean_triples(max_hyp)

    # Build leg index with all multiples
    leg_index = build_leg_index(prim_triples, max_edge)

    seen = set()

    # For each shared leg b, find all pairs of triples
    for b_val, triples_with_b in leg_index.items():
        for i in range(len(triples_with_b)):
            b1, a1, d1 = triples_with_b[i]  # b1 == b_val, other leg a1, hyp d1
            for j in range(len(triples_with_b)):
                if i == j:
                    continue
                b2, c1, e1 = triples_with_b[j]  # b2 == b_val, other leg c1, hyp e1

                metrics.total_candidates += 1

                # Now we have edges a1, b_val, c1 with face diags:
                # a1^2 + b_val^2 = d1^2  ✓
                # b_val^2 + c1^2 = e1^2  ✓
                # Check a1^2 + c1^2 = f^2
                f = isqrt(a1 * a1 + c1 * c1)
                if f is None:
                    continue

                metrics.passed_face_diagonal += 1

                # This is an Euler brick!
                edges = tuple(sorted([a1, b_val, c1]))
                if edges in seen:
                    continue
                seen.add(edges)

                a, b, c = edges
                euler_bricks.append((a, b, c, isqrt(a*a+b*b), isqrt(b*b+c*c), f))
                metrics.euler_bricks_found += 1

                # Check space diagonal
                g = isqrt(a * a + b * b + c * c)
                score = near_miss_score(a, b, c)
                tracker.add(a, b, c, score)
                metrics.near_misses_found += 1

                if g is not None:
                    metrics.perfect_cuboids_found += 1
                    perfect_cuboids.append((a, b, c))
                    print(f"*** PERFECT CUBOID FOUND: ({a}, {b}, {c}) ***")

    metrics.stop_timer()
    return euler_bricks, perfect_cuboids, metrics, tracker


def run_triple_search(max_edge: int = 10000):
    """Run the triple decomposition search and produce comparison report."""
    print(f"Running triple decomposition search (max_edge={max_edge})...")
    bricks, cuboids, metrics, tracker = find_euler_bricks_via_triples(max_edge)

    print(metrics.report())
    metrics.save("results/triple_decomp_metrics.json")

    # Write comparison report
    report_path = "results/triple_decomp_comparison.md"
    with open(report_path, 'w') as f:
        f.write("# Triple Decomposition Search Results\n\n")
        f.write("## Method\n")
        f.write("Pythagorean triple (m,n) parametrization with leg-based indexing.\n")
        f.write("Generates all primitive triples and multiples, indexes by leg values,\n")
        f.write("finds pairs sharing a common leg, checks third face diagonal.\n\n")
        f.write("## Results\n")
        f.write(f"- Search bound: {max_edge:,}\n")
        f.write(f"- Candidate pairs tested: {metrics.total_candidates:,}\n")
        f.write(f"- Euler bricks found: {metrics.euler_bricks_found:,}\n")
        f.write(f"- Perfect cuboids found: {metrics.perfect_cuboids_found}\n")
        f.write(f"- Wall clock time: {metrics.wall_clock_seconds:.2f}s\n")
        f.write(f"- Throughput: {metrics.candidates_per_second:,.0f} pairs/sec\n\n")

        f.write("## Comparison with Baseline\n")
        f.write("The triple decomposition approach is orders of magnitude more efficient\n")
        f.write("than brute-force because it only examines (a,b,c) triples where at least\n")
        f.write("two face diagonals are already guaranteed to be integers.\n\n")

        f.write("## Euler Bricks Found (first 30)\n")
        f.write("| a | b | c | d | e | f |\n")
        f.write("|---|---|---|---|---|---|\n")
        for brick in bricks[:30]:
            a, b, c, d, e, fl = brick
            f.write(f"| {a} | {b} | {c} | {d} | {e} | {fl} |\n")

        f.write(f"\nTotal Euler bricks: {len(bricks)}\n\n")

        f.write("## Top 20 Near-Misses\n")
        f.write("| a | b | c | score | s=a²+b²+c² | sqrt(s) |\n")
        f.write("|---|---|---|-------|-------------|--------|\n")
        for score, (a, b, c) in tracker.get_top(20):
            s = a * a + b * b + c * c
            f.write(f"| {a} | {b} | {c} | {score:.6e} | {s} | {math.sqrt(s):.4f} |\n")

    print(f"\nReport saved to {report_path}")
    print(f"Found {len(bricks)} Euler bricks with smallest edge < {max_edge}")

    return bricks, cuboids, metrics, tracker


if __name__ == "__main__":
    max_edge = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    run_triple_search(max_edge)
