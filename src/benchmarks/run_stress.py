"""Stress testing with adversarial graph families for item_021.

Runs HopGuidedSSSP on 3 adversarial graph families designed to
stress the algorithm's weak points. Verifies correctness and
reports operation counts.
"""

import sys, os, csv, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.benchmarks.runner import run_single
from src.benchmarks.adversarial import ADVERSARIAL_GENERATORS


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
    fieldnames = ['algorithm', 'graph_family', 'n', 'm', 'wall_time_ms',
                  'comparisons', 'additions', 'decrease_keys', 'error']
    rows = []

    sizes = [500, 1000, 5000, 10000]
    density_ratios = [2, 5, 10]

    for name, gen_fn in ADVERSARIAL_GENERATORS.items():
        for n in sizes:
            for ratio in density_ratios:
                m = int(n * ratio)
                adj, actual_n, actual_m = gen_fn(n, m=m, seed=42)
                label = f"{name} n={actual_n} m={actual_m}"

                # Run novel algorithm
                print(f"  hop_guided on {label}...", end=" ", flush=True)
                result = run_single('hop_guided', adj, actual_n,
                                   timeout_sec=120)

                if result['error']:
                    print(result['error'])
                else:
                    # Verify against Dijkstra
                    ref = run_single('dijkstra_fib', adj, actual_n,
                                    timeout_sec=120)
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

                rows.append({
                    'algorithm': 'hop_guided',
                    'graph_family': name,
                    'n': actual_n,
                    'm': actual_m,
                    'wall_time_ms': f"{result['wall_time_ms']:.2f}",
                    'comparisons': result['comparisons'],
                    'additions': result['additions'],
                    'decrease_keys': result['decrease_keys'],
                    'error': result['error'] or '',
                })

                # Also run Dijkstra for comparison
                ref_result = run_single('dijkstra_fib', adj, actual_n,
                                       timeout_sec=120)
                rows.append({
                    'algorithm': 'dijkstra_fib',
                    'graph_family': name,
                    'n': actual_n,
                    'm': actual_m,
                    'wall_time_ms': f"{ref_result['wall_time_ms']:.2f}",
                    'comparisons': ref_result['comparisons'],
                    'additions': ref_result['additions'],
                    'decrease_keys': ref_result['decrease_keys'],
                    'error': ref_result['error'] or '',
                })

    os.makedirs('results', exist_ok=True)
    with open('results/stress_test.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to results/stress_test.csv ({len(rows)} rows)")


if __name__ == '__main__':
    main()
