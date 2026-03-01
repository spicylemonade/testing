"""Run full baseline benchmarks and generate plots for item_010."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.benchmarks.runner import run_benchmark, ALGORITHMS
from src.benchmarks.graph_gen import GENERATORS
import csv

def main():
    # Use sizes appropriate for Python implementation speed
    # n=10^3, 10^4 with m/n in {2, 5, 10, n/2}
    # For n=10^5 and 10^6, use only sparse configs to avoid timeouts
    families = list(GENERATORS.keys())

    rows_all = []

    # Main benchmark: n in {1000, 10000} with full density range
    print("=== Main benchmark: n=1000, 10000 ===")
    rows = run_benchmark(
        algo_names=['dijkstra_fib', 'dmmsy'],
        families=families,
        sizes=[1000, 10000],
        density_ratios=[2, 5, 10],
        output_csv='results/baselines_main.csv',
        timeout_sec=120,
    )
    rows_all.extend(rows)

    # Large-scale sparse: n=100000 with m/n=2,5
    print("\n=== Large-scale sparse: n=100000 ===")
    rows = run_benchmark(
        algo_names=['dijkstra_fib', 'dmmsy'],
        families=['sparse_random', 'high_diameter', 'expander', 'adversarial'],
        sizes=[100000],
        density_ratios=[2, 5],
        output_csv='results/baselines_large.csv',
        timeout_sec=300,
    )
    rows_all.extend(rows)

    # Merge all results into baselines.csv
    fieldnames = ['algorithm', 'graph_family', 'n', 'm', 'wall_time_ms',
                  'comparisons', 'additions', 'decrease_keys', 'error']
    with open('results/baselines.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_all)

    print(f"\nAll results merged into results/baselines.csv ({len(rows_all)} rows)")


if __name__ == '__main__':
    main()
