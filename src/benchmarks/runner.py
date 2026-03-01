"""Benchmark runner for SSSP algorithms.

Times algorithms, counts operations, and outputs CSV results.
"""

import sys, os, time, csv, signal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.baselines.dijkstra_fib import dijkstra_fibonacci
from src.baselines.dmmsy import dmmsy_sssp
from src.benchmarks.graph_gen import GENERATORS, generate


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Computation timed out")


ALGORITHMS = {
    'dijkstra_fib': dijkstra_fibonacci,
    'dmmsy': dmmsy_sssp,
}


def run_single(algo_name, adj, n, source=0, timeout_sec=300):
    """Run a single algorithm on a graph and return results."""
    algo_fn = ALGORITHMS[algo_name]

    # Set timeout
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_sec)

    try:
        start = time.perf_counter()
        result = algo_fn(adj, source, n)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        signal.alarm(0)

        return {
            'wall_time_ms': elapsed_ms,
            'comparisons': result.comparisons,
            'additions': result.additions,
            'decrease_keys': result.decrease_keys,
            'dist': result.dist,
            'error': None,
        }
    except TimeoutError:
        signal.alarm(0)
        return {
            'wall_time_ms': timeout_sec * 1000,
            'comparisons': -1,
            'additions': -1,
            'decrease_keys': -1,
            'dist': None,
            'error': 'timeout',
        }
    except Exception as e:
        signal.alarm(0)
        return {
            'wall_time_ms': -1,
            'comparisons': -1,
            'additions': -1,
            'decrease_keys': -1,
            'dist': None,
            'error': str(e),
        }
    finally:
        signal.signal(signal.SIGALRM, old_handler)


def run_benchmark(algo_names, families, sizes, density_ratios,
                  output_csv='results/baselines.csv', timeout_sec=300,
                  seed=42):
    """Run full benchmark suite.

    Parameters
    ----------
    algo_names : list of str
    families : list of str
    sizes : list of int (values of n)
    density_ratios : list of float (m/n ratios)
    output_csv : str
    timeout_sec : int
    seed : int
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    fieldnames = ['algorithm', 'graph_family', 'n', 'm', 'wall_time_ms',
                  'comparisons', 'additions', 'decrease_keys', 'error']

    rows = []
    total = len(algo_names) * len(families) * len(sizes) * len(density_ratios)
    done = 0

    for family in families:
        for n in sizes:
            for ratio in density_ratios:
                m = int(n * ratio)
                # Skip dense graphs when m > n*(n-1)
                if m > n * (n - 1):
                    m = n * (n - 1)

                # Generate graph
                try:
                    adj, actual_n, actual_m = generate(family, n, m=m, seed=seed)
                except Exception as e:
                    print(f"  SKIP {family} n={n} m={m}: {e}")
                    continue

                for algo_name in algo_names:
                    done += 1
                    print(f"  [{done}/{total}] {algo_name} on {family} "
                          f"n={actual_n} m={actual_m}...", end=" ", flush=True)

                    result = run_single(algo_name, adj, actual_n,
                                        timeout_sec=timeout_sec)

                    row = {
                        'algorithm': algo_name,
                        'graph_family': family,
                        'n': actual_n,
                        'm': actual_m,
                        'wall_time_ms': f"{result['wall_time_ms']:.2f}",
                        'comparisons': result['comparisons'],
                        'additions': result['additions'],
                        'decrease_keys': result['decrease_keys'],
                        'error': result['error'] or '',
                    }
                    rows.append(row)
                    status = result['error'] or f"{result['wall_time_ms']:.1f}ms"
                    print(status)

    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to {output_csv} ({len(rows)} rows)")
    return rows


if __name__ == '__main__':
    # Quick test with small sizes
    rows = run_benchmark(
        algo_names=['dijkstra_fib', 'dmmsy'],
        families=list(GENERATORS.keys()),
        sizes=[100, 500],
        density_ratios=[2, 5],
        output_csv='results/baselines_test.csv',
        timeout_sec=60,
    )
