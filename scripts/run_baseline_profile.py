"""Run baseline Dijkstra profiling across all graph families and sizes."""
import sys
sys.path.insert(0, '.')

import signal
from src.benchmark import benchmark_single, write_csv_header, append_csv_row
from src.graph_generators import GENERATORS
from src.dijkstra import dijkstra_fibonacci, dijkstra_binary

OUTPUT = "results/dijkstra_baseline.csv"


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError("Timed out")


write_csv_header(OUTPUT)

SIZES = [1000, 10000, 100000]
FAMILIES = ['adversarial', 'sparse_er', 'layered_dag', 'grid', 'planted_spt', 'dense']
NUM_TRIALS = 3

for n in SIZES:
    for gtype in FAMILIES:
        # Skip dense for n >= 100000 (too many edges)
        if gtype == 'dense' and n >= 10000:
            continue

        gen_fn = GENERATORS[gtype]

        for trial in range(NUM_TRIALS):
            seed = 42 + trial
            graph, _ = gen_fn(n, seed=seed)
            m = graph.m

            # Binary heap (always fast enough)
            r = benchmark_single(dijkstra_binary, "dijkstra_bin", graph, gtype, n, m, trial)
            append_csv_row(OUTPUT, r)
            print(f"dijkstra_bin/{gtype} n={n} trial={trial}: ops={r['total_ops']}, {r['wall_time_ms']:.1f}ms")

            # Fibonacci heap (skip for n >= 100000 due to Python overhead)
            if n <= 10000 or (gtype == 'adversarial' and n <= 10000):
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(60)  # 60 second timeout
                try:
                    r = benchmark_single(dijkstra_fibonacci, "dijkstra_fib", graph, gtype, n, m, trial)
                    signal.alarm(0)
                    append_csv_row(OUTPUT, r)
                    print(f"dijkstra_fib/{gtype} n={n} trial={trial}: ops={r['total_ops']}, {r['wall_time_ms']:.1f}ms")
                except TimeoutError:
                    signal.alarm(0)
                    print(f"dijkstra_fib/{gtype} n={n} trial={trial}: TIMEOUT (skipped)")

print(f"\nDone. Results in {OUTPUT}")
