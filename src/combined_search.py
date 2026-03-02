"""Combined search integrating all methods for large-scale perfect cuboid search.

Combines: modular_filter, quadratic_sieve, triple_decomposition, and elliptic_families.
"""

import math
import sys
import os
import json
import csv
import time
import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from space_diagonal import isqrt, near_miss_score, NearMissTracker
from modular_filter import is_euler_brick_candidate
from quadratic_sieve import QuadraticSieve
from triple_decomposition import find_euler_bricks_via_triples
from elliptic_families import extended_parametric_search
from euler_brick import generate_all_bricks
from metrics import SearchMetrics


class ComputeTimeout(Exception):
    pass


def combined_search(max_edge: int = 100000, timeout_seconds: int = 300):
    """Run combined search using all methods."""
    metrics = SearchMetrics(method="combined_search", search_bound=max_edge)
    tracker = NearMissTracker(k=200)
    all_euler_bricks = set()
    perfect_cuboids = []

    # Set timeout
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(ComputeTimeout()))
        signal.alarm(timeout_seconds)

    metrics.start_timer()
    log_path = "results/search_log.jsonl"
    os.makedirs("results", exist_ok=True)

    try:
        # Stage 1: Triple decomposition (most efficient for finding Euler bricks)
        print(f"Stage 1: Triple decomposition (max_edge={max_edge})...")
        bricks_td, _, metrics_td, tracker_td = find_euler_bricks_via_triples(max_edge)
        stage1_count = len(bricks_td)
        for brick in bricks_td:
            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
            all_euler_bricks.add(edges)
        print(f"  Found {stage1_count} Euler bricks via triple decomposition")
        metrics.filter_stages["triple_decomposition"] = stage1_count

        # Stage 2: Parametric families
        print("Stage 2: Parametric families...")
        param_bricks = generate_all_bricks(min(100, int(math.sqrt(max_edge))))
        stage2_new = 0
        for brick in param_bricks:
            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
            if edges[2] <= max_edge and edges not in all_euler_bricks:
                all_euler_bricks.add(edges)
                stage2_new += 1
        print(f"  Found {stage2_new} additional bricks from parametric families")
        metrics.filter_stages["parametric_families"] = stage2_new

        # Stage 3: Extended multi-hop families
        print("Stage 3: Extended multi-hop families...")
        max_m_ext = min(100, int(math.sqrt(max_edge) / 10) + 10)
        ext_bricks = extended_parametric_search(max_m_ext)
        stage3_new = 0
        for brick in ext_bricks:
            edges = tuple(sorted([brick[0], brick[1], brick[2]]))
            if edges[2] <= max_edge and edges not in all_euler_bricks:
                all_euler_bricks.add(edges)
                stage3_new += 1
        print(f"  Found {stage3_new} additional bricks from extended families")
        metrics.filter_stages["extended_families"] = stage3_new

        # Check all bricks for perfect cuboid
        print(f"\nChecking {len(all_euler_bricks)} total Euler bricks for perfect cuboid...")
        for edges in all_euler_bricks:
            a, b, c = edges
            metrics.total_candidates += 1
            metrics.euler_bricks_found += 1

            g = isqrt(a * a + b * b + c * c)
            score = near_miss_score(a, b, c)
            if score != float('inf'):
                tracker.add(a, b, c, score)
                metrics.near_misses_found += 1

            if g is not None:
                metrics.perfect_cuboids_found += 1
                perfect_cuboids.append((a, b, c))
                print(f"*** PERFECT CUBOID FOUND: ({a}, {b}, {c}) ***")

    except ComputeTimeout:
        print(f"\nSearch timed out after {timeout_seconds}s")
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

    metrics.stop_timer()

    # Write search log
    with open(log_path, 'w') as f:
        for edges in sorted(all_euler_bricks):
            a, b, c = edges
            d = isqrt(a*a + b*b)
            e = isqrt(b*b + c*c)
            fl = isqrt(a*a + c*c)
            s = a*a + b*b + c*c
            g_approx = math.sqrt(s)
            score = near_miss_score(a, b, c)
            entry = {
                "a": a, "b": b, "c": c,
                "d": d, "e": e, "f": fl,
                "space_diag_sq": s,
                "space_diag_approx": round(g_approx, 6),
                "near_miss_score": score if score != float('inf') else None,
                "is_perfect": isqrt(s) is not None,
            }
            f.write(json.dumps(entry) + "\n")

    # Write near-misses to CSV
    near_miss_path = "results/near_misses.csv"
    top_misses = tracker.get_top()
    with open(near_miss_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'c', 'score', 'space_diag_sq', 'nearest_sq'])
        for score_val, (a, b, c) in top_misses:
            s = a * a + b * b + c * c
            r = math.isqrt(s)
            nearest = r * r if (s - r * r) <= ((r + 1) * (r + 1) - s) else (r + 1) * (r + 1)
            writer.writerow([a, b, c, f"{score_val:.10e}", s, nearest])

    metrics.save("results/metrics.json")

    # Write summary
    summary_path = "results/search_summary.md"
    with open(summary_path, 'w') as fout:
        fout.write("# Combined Search Summary\n\n")
        fout.write("## Configuration\n")
        fout.write(f"- Maximum edge: {max_edge:,}\n")
        fout.write(f"- Methods: triple decomposition + parametric families + extended multi-hop\n\n")
        fout.write("## Results\n")
        fout.write(f"- Total Euler bricks found: {len(all_euler_bricks)}\n")
        fout.write(f"- Perfect cuboids found: {len(perfect_cuboids)}\n")
        fout.write(f"- Wall clock time: {metrics.wall_clock_seconds:.2f}s\n\n")
        fout.write("## Rejection Rate by Stage\n")
        for stage, count in metrics.filter_stages.items():
            fout.write(f"- {stage}: {count} bricks\n")
        fout.write(f"\n## Top 50 Near-Misses\n")
        fout.write("| Rank | a | b | c | Score | s=a²+b²+c² | sqrt(s) |\n")
        fout.write("|------|---|---|---|-------|-------------|--------|\n")
        for i, (score, (a, b, c)) in enumerate(tracker.get_top(50), 1):
            s = a * a + b * b + c * c
            fout.write(f"| {i} | {a} | {b} | {c} | {score:.4e} | {s} | {math.sqrt(s):.4f} |\n")

    print(f"\n{metrics.report()}")
    print(f"\nSearch log: {log_path}")
    print(f"Summary: {summary_path}")

    return all_euler_bricks, perfect_cuboids, metrics, tracker


if __name__ == "__main__":
    max_edge = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    combined_search(max_edge, timeout)
