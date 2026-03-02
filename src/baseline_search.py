"""Baseline brute-force search for perfect cuboids.

Exhaustively searches all triples (a,b,c) with a<=b<=c up to a configurable bound.
Applies modular filtering, checks face diagonals, then space diagonal.
"""

import math
import csv
import os
import sys
import time
import signal

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modular_filter import is_candidate, is_euler_brick_candidate
from space_diagonal import is_perfect, near_miss_score, NearMissTracker, isqrt
from metrics import SearchMetrics
from config import SearchConfig


class ComputeTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise ComputeTimeout()


def baseline_search(config: SearchConfig) -> SearchMetrics:
    """Run baseline brute-force search.

    Searches all triples (a, b, c) with 1 <= a <= b <= c <= config.search_bound.
    """
    metrics = SearchMetrics(
        method="baseline_brute_force",
        search_bound=config.search_bound,
    )
    tracker = NearMissTracker(k=config.top_k_near_misses)

    near_miss_path = os.path.join(config.output_dir, "near_misses.csv")
    os.makedirs(config.output_dir, exist_ok=True)

    perfect_cuboids = []

    metrics.start_timer()

    N = config.search_bound
    stage_raw = 0
    stage_modfilter = 0
    stage_face_diag = 0
    stage_euler_brick = 0

    for a in range(1, N + 1):
        for b in range(a, N + 1):
            # Quick check: is a^2 + b^2 a perfect square?
            ab2 = a * a + b * b
            d = isqrt(ab2)
            if d is None:
                stage_raw += 1
                metrics.total_candidates += (N - b + 1)  # Skip all c values
                continue

            for c in range(b, N + 1):
                metrics.total_candidates += 1
                stage_raw += 1

                # Check modular filter
                if config.use_modular_filter and not is_euler_brick_candidate(a, b, c):
                    continue
                stage_modfilter += 1
                metrics.passed_modular_filter += 1

                # Check remaining face diagonals
                bc2 = b * b + c * c
                e = isqrt(bc2)
                if e is None:
                    continue
                ac2 = a * a + c * c
                f = isqrt(ac2)
                if f is None:
                    continue

                stage_face_diag += 1
                metrics.passed_face_diagonal += 1
                metrics.euler_bricks_found += 1

                # This is an Euler brick! Check space diagonal.
                s = a * a + b * b + c * c
                g = isqrt(s)

                score = near_miss_score(a, b, c)
                tracker.add(a, b, c, score)
                metrics.near_misses_found += 1

                if g is not None:
                    # PERFECT CUBOID FOUND!
                    metrics.perfect_cuboids_found += 1
                    perfect_cuboids.append((a, b, c, d, e, f, g))
                    print(f"*** PERFECT CUBOID FOUND: ({a}, {b}, {c}) ***")
                    print(f"    Face diags: ({d}, {e}, {f}), Space diag: {g}")

    metrics.stop_timer()

    metrics.filter_stages = {
        "raw_candidates": stage_raw,
        "passed_modular": stage_modfilter,
        "euler_bricks": stage_face_diag,
    }

    # Write near-misses to CSV
    top_misses = tracker.get_top()
    with open(near_miss_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'c', 'score', 'space_diag_sq', 'nearest_sq'])
        for score_val, (a, b, c) in top_misses:
            s = a * a + b * b + c * c
            r = math.isqrt(s)
            nearest = r * r if (s - r * r) <= ((r + 1) * (r + 1) - s) else (r + 1) * (r + 1)
            writer.writerow([a, b, c, f"{score_val:.10e}", s, nearest])

    # Save metrics
    metrics.save(os.path.join(config.output_dir, "metrics.json"))

    return metrics, perfect_cuboids, tracker


def run_benchmark():
    """Run a benchmark to measure search throughput."""
    # Small benchmark to measure candidates/second
    config = SearchConfig(
        search_bound=1000,
        use_modular_filter=True,
        output_dir="results",
    )

    print("Running baseline search benchmark (bound=1000)...")
    metrics, cuboids, tracker = baseline_search(config)
    print(metrics.report())

    # Write benchmark results
    bench_path = os.path.join(config.output_dir, "baseline_benchmarks.md")
    with open(bench_path, 'w') as f:
        f.write("# Baseline Search Benchmarks\n\n")
        f.write("## Configuration\n")
        f.write(f"- Search bound: {config.search_bound}\n")
        f.write(f"- Modular filter: {config.use_modular_filter}\n\n")
        f.write("## Results\n")
        f.write(f"- Total candidates: {metrics.total_candidates:,}\n")
        f.write(f"- Passed modular filter: {metrics.passed_modular_filter:,}\n")
        f.write(f"- Euler bricks found: {metrics.euler_bricks_found:,}\n")
        f.write(f"- Perfect cuboids found: {metrics.perfect_cuboids_found}\n")
        f.write(f"- Near-misses tracked: {metrics.near_misses_found}\n")
        f.write(f"- Wall clock time: {metrics.wall_clock_seconds:.2f}s\n")
        f.write(f"- Throughput: {metrics.candidates_per_second:,.0f} candidates/sec\n\n")

        # Now run without filter to compare
        config2 = SearchConfig(search_bound=1000, use_modular_filter=False, output_dir="results")
        print("\nRunning without modular filter for comparison...")
        metrics2, _, _ = baseline_search(config2)
        f.write("## Without Modular Filter\n")
        f.write(f"- Throughput: {metrics2.candidates_per_second:,.0f} candidates/sec\n")
        f.write(f"- Euler bricks found: {metrics2.euler_bricks_found}\n\n")

        f.write("## Filter Effectiveness\n")
        if metrics.total_candidates > 0:
            rejection = 1.0 - metrics.passed_modular_filter / max(1, metrics.total_candidates)
            f.write(f"- Modular filter rejection rate: {rejection:.4%}\n")
        f.write(f"- Speedup from filtering: reduces face diagonal checks significantly\n")

    print(f"\nBenchmarks saved to {bench_path}")
    print(f"Near-misses saved to results/near_misses.csv")

    # Show top near-misses
    top = tracker.get_top(10)
    if top:
        print("\nTop 10 near-misses:")
        for score, (a, b, c) in top:
            s = a * a + b * b + c * c
            r = math.isqrt(s)
            print(f"  ({a}, {b}, {c}) score={score:.6e} s={s} sqrt≈{math.sqrt(s):.4f}")

    return metrics


if __name__ == "__main__":
    run_benchmark()
