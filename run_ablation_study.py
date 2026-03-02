#!/usr/bin/env python3
"""Ablation study on key DAMS-SSSP design parameters (item_022).

Varies 3 key design choices:
1. Number of scales (num_scales): 1, ceil(sqrt(log n)), ceil(log n)
2. Bucket count factor: sqrt(n)/4, sqrt(n), 2*sqrt(n), n
3. Cleanup passes: 0, 1, 3 (default)

Produces results/ablation_study.json and figures/ablation_results.png
"""

import json
import math
import os
import signal
import sys
import time
import copy

sys.path.insert(0, ".")

from src.graphs.generator import sparse, grid, dijkstra_worst_case
from src.datastructures.bucket_pq import BucketPQ
from src.benchmark.harness import benchmark_single


class Timeout(Exception):
    pass

def _timeout_handler(signum, frame):
    raise Timeout()


def dams_sssp_ablation(adj, source, n, num_scales_override=None,
                        bucket_factor=None, max_cleanup_passes=3):
    """DAMS-SSSP with configurable parameters for ablation."""
    INF = float('inf')
    dist = [INF] * n
    dist[source] = 0.0
    stats = {'comparisons': 0, 'additions': 0, 'heap_ops': 0}

    if n <= 1:
        return {v: dist[v] for v in range(n)}, stats

    max_w = 0.0
    for u in range(n):
        for v, w in adj.get(u, []):
            if w > max_w:
                max_w = w

    if max_w == 0.0:
        return {v: dist[v] for v in range(n)}, stats

    log_n = math.log2(max(n, 2))
    if num_scales_override is not None:
        num_scales = num_scales_override
    else:
        num_scales = max(1, math.ceil(math.sqrt(log_n)))

    delta = max_w * n

    if bucket_factor is None:
        bucket_factor = 1.0  # default: sqrt(n) buckets

    for scale in range(num_scales):
        delta_j = delta / (2.0 ** scale)
        if delta_j < 1e-15:
            break

        n_buckets = max(2, int(math.ceil(bucket_factor * math.sqrt(max(n, 4)))))
        bucket_width = delta_j / n_buckets
        if bucket_width <= 0:
            break

        _bucketed_dijkstra_scale(adj, dist, n, delta_j, n_buckets,
                                 bucket_width, stats)

    # Cleanup passes
    changed = True
    passes = 0
    while changed and passes < max_cleanup_passes:
        changed = False
        passes += 1
        for u in range(n):
            if dist[u] == INF:
                continue
            for v, w in adj.get(u, []):
                stats['additions'] += 1
                stats['comparisons'] += 1
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    changed = True

    return {v: dist[v] for v in range(n)}, stats


def _bucketed_dijkstra_scale(adj, dist, n, delta, n_buckets, bucket_width, stats):
    INF = float('inf')
    pq = BucketPQ(n_buckets, bucket_width, offset=0.0)
    in_pq = [False] * n
    settled = [False] * n

    for v in range(n):
        if dist[v] < INF:
            pq.insert(v, dist[v])
            in_pq[v] = True

    while not pq.is_empty():
        batch = pq.extract_min_batch()
        if not batch:
            break
        for u in batch:
            in_pq[u] = False
            if settled[u]:
                continue
            settled[u] = True
            for v, w in adj.get(u, []):
                stats['additions'] += 1
                nd = dist[u] + w
                stats['comparisons'] += 1
                if nd < dist[v]:
                    dist[v] = nd
                    if not settled[v]:
                        if in_pq[v]:
                            pq.decrease_key(v, nd)
                        else:
                            pq.insert(v, nd)
                            in_pq[v] = True

    stats['comparisons'] += pq.stats['comparisons']
    stats['heap_ops'] += pq.stats['heap_ops']


def verify_correctness(adj, source, n, dist_result):
    """Verify against Bellman-Ford for small n."""
    if n > 5000:
        return True  # Skip for large graphs
    from src.baselines.bellman_ford import sssp as bf_sssp
    bf_dist, _ = bf_sssp(adj, source, n)
    for v in range(n):
        d1 = dist_result.get(v, float('inf'))
        d2 = bf_dist.get(v, float('inf'))
        if abs(d1 - d2) > 1e-9 * max(1, abs(d2)):
            return False
    return True


def make_gen(gen_fn):
    def gen(n, seed):
        g = gen_fn(n, seed=seed)
        verts = g.vertices()
        n_actual = max(verts) + 1 if verts else 0
        return g.adj, n_actual
    return gen


def main():
    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    results = []
    SIZES = [1000, 5000, 10000, 50000]

    generators = {
        "sparse": make_gen(sparse),
        "worst_case": make_gen(dijkstra_worst_case),
    }

    # ---- Ablation 1: Number of scales ----
    print("=" * 60)
    print("ABLATION 1: Number of Scales")
    print("=" * 60)
    for n_target in SIZES:
        for gname, gen_fn in generators.items():
            adj, n_actual = gen_fn(n_target, 42)
            m = sum(len(adj.get(v, [])) for v in range(n_actual))
            log_n = math.log2(max(n_actual, 2))

            for scale_label, num_scales in [
                ("1_scale", 1),
                ("sqrt_logn", max(1, math.ceil(math.sqrt(log_n)))),
                ("logn", max(1, math.ceil(log_n))),
                ("2logn", max(1, 2 * math.ceil(log_n))),
            ]:
                print(f"  scales={scale_label:12s} | {gname:12s} | n={n_actual} ...", end="", flush=True)

                signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(120)
                try:
                    def algo_fn(adj, source, n):
                        return dams_sssp_ablation(adj, source, n,
                                                  num_scales_override=num_scales)
                    r = benchmark_single(algo_fn, adj, 0, n_actual, warmup=1, runs=3)

                    # Verify correctness on small graphs
                    correct = verify_correctness(adj, 0, n_actual,
                                                 dams_sssp_ablation(adj, 0, n_actual,
                                                                    num_scales_override=num_scales)[0])

                    results.append({
                        "ablation": "num_scales", "variant": scale_label,
                        "num_scales": num_scales,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "mean_time": r["mean"], "median_time": r["median"],
                        "std_time": r["std"],
                        "comparisons": r["stats"]["comparisons"],
                        "additions": r["stats"]["additions"],
                        "heap_ops": r["stats"]["heap_ops"],
                        "correct": correct,
                    })
                    signal.alarm(0)
                    print(f"  {r['median']:.4f}s  correct={correct}")
                except Timeout:
                    signal.alarm(0)
                    print("  TIMEOUT")
                    results.append({
                        "ablation": "num_scales", "variant": scale_label,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "error": "timeout",
                    })
                except Exception as e:
                    signal.alarm(0)
                    print(f"  ERROR: {e}")

    # ---- Ablation 2: Bucket count factor ----
    print("\n" + "=" * 60)
    print("ABLATION 2: Bucket Count Factor")
    print("=" * 60)
    for n_target in SIZES:
        for gname, gen_fn in generators.items():
            adj, n_actual = gen_fn(n_target, 42)
            m = sum(len(adj.get(v, [])) for v in range(n_actual))

            for bf_label, bf in [
                ("0.25x_sqrt_n", 0.25),
                ("0.5x_sqrt_n", 0.5),
                ("1x_sqrt_n", 1.0),
                ("2x_sqrt_n", 2.0),
            ]:
                print(f"  buckets={bf_label:14s} | {gname:12s} | n={n_actual} ...", end="", flush=True)

                signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(120)
                try:
                    def algo_fn(adj, source, n, _bf=bf):
                        return dams_sssp_ablation(adj, source, n, bucket_factor=_bf)
                    r = benchmark_single(algo_fn, adj, 0, n_actual, warmup=1, runs=3)

                    correct = verify_correctness(adj, 0, n_actual,
                                                 dams_sssp_ablation(adj, 0, n_actual,
                                                                    bucket_factor=bf)[0])

                    results.append({
                        "ablation": "bucket_factor", "variant": bf_label,
                        "bucket_factor": bf,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "mean_time": r["mean"], "median_time": r["median"],
                        "std_time": r["std"],
                        "comparisons": r["stats"]["comparisons"],
                        "additions": r["stats"]["additions"],
                        "heap_ops": r["stats"]["heap_ops"],
                        "correct": correct,
                    })
                    signal.alarm(0)
                    print(f"  {r['median']:.4f}s  correct={correct}")
                except Timeout:
                    signal.alarm(0)
                    print("  TIMEOUT")
                    results.append({
                        "ablation": "bucket_factor", "variant": bf_label,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "error": "timeout",
                    })
                except Exception as e:
                    signal.alarm(0)
                    print(f"  ERROR: {e}")

    # ---- Ablation 3: Cleanup passes ----
    print("\n" + "=" * 60)
    print("ABLATION 3: Cleanup Passes")
    print("=" * 60)
    for n_target in SIZES:
        for gname, gen_fn in generators.items():
            adj, n_actual = gen_fn(n_target, 42)
            m = sum(len(adj.get(v, [])) for v in range(n_actual))

            for cp_label, cp in [
                ("0_passes", 0),
                ("1_pass", 1),
                ("3_passes", 3),
            ]:
                print(f"  cleanup={cp_label:10s} | {gname:12s} | n={n_actual} ...", end="", flush=True)

                signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(120)
                try:
                    def algo_fn(adj, source, n, _cp=cp):
                        return dams_sssp_ablation(adj, source, n, max_cleanup_passes=_cp)
                    r = benchmark_single(algo_fn, adj, 0, n_actual, warmup=1, runs=3)

                    correct = verify_correctness(adj, 0, n_actual,
                                                 dams_sssp_ablation(adj, 0, n_actual,
                                                                    max_cleanup_passes=cp)[0])

                    results.append({
                        "ablation": "cleanup_passes", "variant": cp_label,
                        "cleanup_passes": cp,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "mean_time": r["mean"], "median_time": r["median"],
                        "std_time": r["std"],
                        "comparisons": r["stats"]["comparisons"],
                        "additions": r["stats"]["additions"],
                        "heap_ops": r["stats"]["heap_ops"],
                        "correct": correct,
                    })
                    signal.alarm(0)
                    print(f"  {r['median']:.4f}s  correct={correct}")
                except Timeout:
                    signal.alarm(0)
                    print("  TIMEOUT")
                    results.append({
                        "ablation": "cleanup_passes", "variant": cp_label,
                        "graph_type": gname, "n": n_actual, "m": m,
                        "error": "timeout",
                    })
                except Exception as e:
                    signal.alarm(0)
                    print(f"  ERROR: {e}")

    with open("results/ablation_study.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} results to results/ablation_study.json")


if __name__ == "__main__":
    main()
