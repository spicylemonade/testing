"""Run novel algorithm benchmarks for item_018.

Runs HopGuidedSSSP on all 8 graph families at multiple sizes,
verifies correctness against Dijkstra, and stores results in CSV.
"""

import sys, os, csv, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.benchmarks.runner import run_single, ALGORITHMS
from src.benchmarks.graph_gen import GENERATORS, generate


def verify_correctness(dist_novel, dist_ref, n, label):
    """Verify novel distances match Dijkstra reference."""
    for v in range(n):
        d_n = dist_novel[v]
        d_r = dist_ref[v]
        if d_r == float('inf'):
            assert d_n == float('inf'), f"{label}: v={v}: novel={d_n}, ref=inf"
        else:
            assert abs(d_n - d_r) < 1e-9, f"{label}: v={v}: novel={d_n}, ref={d_r}"


def main():
    families = list(GENERATORS.keys())

    rows_all = []
    fieldnames = ['algorithm', 'graph_family', 'n', 'm', 'wall_time_ms',
                  'comparisons', 'additions', 'decrease_keys', 'error']

    # Main benchmark: n=1000, 10000 with density ratios 2, 5, 10
    configs = [
        (families, [1000, 10000], [2, 5, 10], 120),
        # Larger sparse: n=100000
        (['sparse_random', 'high_diameter', 'expander', 'adversarial'],
         [100000], [2, 5], 300),
    ]

    for fams, sizes, ratios, timeout in configs:
        for family in fams:
            for n in sizes:
                for ratio in ratios:
                    m = int(n * ratio)
                    if m > n * (n - 1):
                        m = n * (n - 1)

                    try:
                        adj, actual_n, actual_m = generate(family, n, m=m, seed=42)
                    except Exception as e:
                        print(f"  SKIP {family} n={n} m={m}: {e}")
                        continue

                    label = f"{family} n={actual_n} m={actual_m}"

                    # Run novel algorithm
                    print(f"  hop_guided on {label}...", end=" ", flush=True)
                    result = run_single('hop_guided', adj, actual_n,
                                       timeout_sec=timeout)

                    if result['error']:
                        print(result['error'])
                    else:
                        # Verify correctness against Dijkstra
                        ref = run_single('dijkstra_fib', adj, actual_n,
                                        timeout_sec=timeout)
                        if ref['dist'] is not None and result['dist'] is not None:
                            try:
                                verify_correctness(result['dist'], ref['dist'],
                                                 actual_n, label)
                                print(f"{result['wall_time_ms']:.1f}ms (correct)")
                            except AssertionError as ae:
                                print(f"INCORRECT: {ae}")
                                result['error'] = str(ae)
                        else:
                            print(f"{result['wall_time_ms']:.1f}ms")

                    row = {
                        'algorithm': 'hop_guided',
                        'graph_family': family,
                        'n': actual_n,
                        'm': actual_m,
                        'wall_time_ms': f"{result['wall_time_ms']:.2f}",
                        'comparisons': result['comparisons'],
                        'additions': result['additions'],
                        'decrease_keys': result['decrease_keys'],
                        'error': result['error'] or '',
                    }
                    rows_all.append(row)

    # Write novel results CSV
    os.makedirs('results', exist_ok=True)
    with open('results/novel_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_all)

    print(f"\nResults saved to results/novel_results.csv ({len(rows_all)} rows)")


if __name__ == '__main__':
    main()
