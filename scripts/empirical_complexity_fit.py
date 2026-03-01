"""Item 020: Empirical complexity fitting.

Fits operation counts to theoretical complexity formulas via log-log regression.
Compares fitted exponents for HiBRA vs Dijkstra.
"""

import sys, os, csv, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np


def load_data(path="results/comprehensive_benchmark.csv"):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def group_median(rows, algo, gtype):
    """Get median total_ops for each n value."""
    data = {}
    for r in rows:
        if r['algorithm'] == algo and r['graph_type'] == gtype:
            n = int(r['n'])
            ops = int(r['total_ops'])
            data.setdefault(n, []).append(ops)
    result = {}
    for n, ops_list in sorted(data.items()):
        result[n] = sorted(ops_list)[len(ops_list)//2]
    return result


def log_log_regression(x_vals, y_vals):
    """Fit log(y) = a * log(x) + b. Return (a, b, R^2)."""
    if len(x_vals) < 2:
        return None, None, None
    lx = np.array([math.log(x) for x in x_vals])
    ly = np.array([math.log(y) for y in y_vals])
    n = len(lx)
    sx = np.sum(lx)
    sy = np.sum(ly)
    sxy = np.sum(lx * ly)
    sxx = np.sum(lx * lx)
    syy = np.sum(ly * ly)
    denom = n * sxx - sx * sx
    if denom == 0:
        return None, None, None
    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n
    ss_res = np.sum((ly - (a * lx + b))**2)
    ss_tot = np.sum((ly - np.mean(ly))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return a, b, r2


def n_log_n_regression(data):
    """Fit ops = c * n * log(n). Return (c, R^2)."""
    xs = []
    ys = []
    for n, ops in sorted(data.items()):
        if n > 0:
            xs.append(n * math.log(n))
            ys.append(ops)
    if len(xs) < 2:
        return None, None
    xs = np.array(xs)
    ys = np.array(ys)
    c = np.sum(xs * ys) / np.sum(xs * xs)
    ss_res = np.sum((ys - c * xs)**2)
    ss_tot = np.sum((ys - np.mean(ys))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return c, r2


def n_log_n_over_loglog_regression(data):
    """Fit ops = c * n * log(n) / log(log(n)). Return (c, R^2)."""
    xs = []
    ys = []
    for n, ops in sorted(data.items()):
        if n >= 16:
            logn = math.log(n)
            loglogn = math.log(max(2, logn))
            xs.append(n * logn / loglogn)
            ys.append(ops)
    if len(xs) < 2:
        return None, None
    xs = np.array(xs)
    ys = np.array(ys)
    c = np.sum(xs * ys) / np.sum(xs * xs)
    ss_res = np.sum((ys - c * xs)**2)
    ss_tot = np.sum((ys - np.mean(ys))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return c, r2


def main():
    rows = load_data()

    algos = ['hibra', 'dijkstra_fib', 'dijkstra_bin', 'batch_dijkstra']
    sparse_types = ['adversarial', 'sparse_er', 'layered_dag', 'grid', 'planted_spt']

    output_path = "results/complexity_fit.csv"
    with open(output_path, 'w') as f:
        f.write("algorithm,graph_type,log_log_exponent,log_log_R2,n_logn_c,n_logn_R2,n_logn_loglogn_c,n_logn_loglogn_R2\n")

    print("=" * 100)
    print("EMPIRICAL COMPLEXITY FITTING")
    print("=" * 100)

    for gtype in sparse_types:
        print(f"\n--- Graph family: {gtype} ---")
        for algo in algos:
            data = group_median(rows, algo, gtype)
            if len(data) < 3:
                continue

            ns = list(data.keys())
            ops = list(data.values())

            # Log-log regression
            a, b, r2 = log_log_regression(ns, ops)

            # Fit to n*log(n) model
            c_nlogn, r2_nlogn = n_log_n_regression(data)

            # Fit to n*log(n)/log(log(n)) model
            c_nlognll, r2_nlognll = n_log_n_over_loglog_regression(data)

            print(f"  {algo:20s}: exponent={a:.3f} R²={r2:.4f} | "
                  f"n·log(n): c={c_nlogn:.3f} R²={r2_nlogn:.4f} | "
                  f"n·log(n)/log(log(n)): c={c_nlognll:.3f} R²={r2_nlognll:.4f}")

            with open(output_path, 'a') as f:
                f.write(f"{algo},{gtype},{a:.6f},{r2:.6f},"
                        f"{c_nlogn:.6f},{r2_nlogn:.6f},"
                        f"{c_nlognll:.6f},{r2_nlognll:.6f}\n")

            # Print data points
            for n, op in sorted(data.items()):
                nlogn = n * math.log(n)
                ratio = op / nlogn if nlogn > 0 else 0
                print(f"    n={n:7d}: ops={op:12d}, ops/(n·log n)={ratio:.2f}")

    # Summary comparison
    print("\n" + "=" * 100)
    print("SUMMARY: Fitted exponents (log-log regression)")
    print("=" * 100)
    for gtype in sparse_types:
        print(f"\n{gtype}:")
        for algo in algos:
            data = group_median(rows, algo, gtype)
            if len(data) < 3:
                continue
            ns = list(data.keys())
            ops = list(data.values())
            a, b, r2 = log_log_regression(ns, ops)
            print(f"  {algo:20s}: ops ~ n^{a:.3f}  (R²={r2:.4f})")

    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    main()
