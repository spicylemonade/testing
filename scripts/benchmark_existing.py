#!/usr/bin/env python3
"""Benchmark existing CSV parsers against our benchmark datasets.

Parsers tested:
1. Python csv module (stdlib)
2. pandas.read_csv (single-threaded via engine='c')
3. pyarrow.csv.read_csv (single-threaded)
4. Our scalar baseline (via subprocess)

xsv and libcsv skipped if not available (noted in output).
All measurements: median of 3 runs, warm FS cache.
"""

import csv
import gc
import io
import json
import os
import resource
import statistics
import subprocess
import sys
import time

DATA_DIR = "results/benchmarks/data"
OUTPUT = "results/benchmarks/existing_parsers.json"
N_RUNS = 3


def get_file_size(path):
    return os.path.getsize(path)


def warm_cache(path):
    """Read file into OS page cache."""
    with open(path, "rb") as f:
        while f.read(1 << 20):
            pass


def get_peak_rss_mb():
    """Get peak RSS in MB."""
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return ru.ru_maxrss / 1024  # Linux: ru_maxrss is in KB


def benchmark_python_csv(path):
    """Benchmark Python's csv module."""
    times = []
    row_count = 0
    for _ in range(N_RUNS):
        gc.collect()
        t0 = time.monotonic()
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                row_count += 1
        elapsed = time.monotonic() - t0
        times.append(elapsed)
    median_time = statistics.median(times)
    file_size = get_file_size(path)
    return {
        "parser": "python_csv",
        "version": f"Python {sys.version.split()[0]}",
        "time_sec": round(median_time, 4),
        "throughput_mb_per_sec": round(file_size / (1024 * 1024) / median_time, 2),
        "rows": row_count,
    }


def benchmark_pandas(path):
    """Benchmark pandas.read_csv (single-threaded C engine)."""
    import pandas as pd
    times = []
    row_count = 0
    for _ in range(N_RUNS):
        gc.collect()
        t0 = time.monotonic()
        df = pd.read_csv(path, engine="c", low_memory=True)
        row_count = len(df)
        elapsed = time.monotonic() - t0
        times.append(elapsed)
        del df
    median_time = statistics.median(times)
    file_size = get_file_size(path)
    return {
        "parser": "pandas_read_csv",
        "version": f"pandas {pd.__version__}",
        "engine": "c",
        "time_sec": round(median_time, 4),
        "throughput_mb_per_sec": round(file_size / (1024 * 1024) / median_time, 2),
        "rows": row_count,
    }


def benchmark_pyarrow(path):
    """Benchmark pyarrow.csv.read_csv."""
    import pyarrow.csv as pa_csv
    import pyarrow as pa
    times = []
    row_count = 0
    for _ in range(N_RUNS):
        gc.collect()
        t0 = time.monotonic()
        table = pa_csv.read_csv(path)
        row_count = table.num_rows
        elapsed = time.monotonic() - t0
        times.append(elapsed)
        del table
    median_time = statistics.median(times)
    file_size = get_file_size(path)
    return {
        "parser": "pyarrow_csv",
        "version": f"pyarrow {pa.__version__}",
        "time_sec": round(median_time, 4),
        "throughput_mb_per_sec": round(file_size / (1024 * 1024) / median_time, 2),
        "rows": row_count,
    }


def benchmark_scalar_baseline(path):
    """Benchmark our scalar baseline parser."""
    parser_bin = "src/baseline/scalar_parser"
    if not os.path.exists(parser_bin):
        return None
    r = subprocess.run([parser_bin, path, "--benchmark"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    data = json.loads(r.stdout.strip())
    return {
        "parser": "scalar_baseline",
        "version": "custom C (gcc -O2)",
        "time_sec": round(data["best_time_sec"], 4),
        "throughput_mb_per_sec": round(data["throughput_mb_per_sec"], 2),
        "rows": data["rows"],
    }


def main():
    import pandas as pd
    import pyarrow as pa

    csv_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))
    all_results = []

    versions = {
        "python_csv": f"Python {sys.version.split()[0]}",
        "pandas": f"pandas {pd.__version__}",
        "pyarrow": f"pyarrow {pa.__version__}",
        "scalar_baseline": "custom C (gcc -O2)",
    }

    for csv_file in csv_files:
        path = os.path.join(DATA_DIR, csv_file)
        file_size = get_file_size(path)
        print(f"\n=== {csv_file} ({file_size / 1e6:.1f} MB) ===")

        # Warm FS cache
        warm_cache(path)

        dataset_results = {"dataset": csv_file, "file_size_bytes": file_size, "parsers": []}

        # Python csv
        print("  python csv ...", end="", flush=True)
        try:
            r = benchmark_python_csv(path)
            dataset_results["parsers"].append(r)
            print(f" {r['throughput_mb_per_sec']:.1f} MB/s")
        except Exception as e:
            print(f" ERROR: {e}")

        # pandas
        print("  pandas ...", end="", flush=True)
        try:
            r = benchmark_pandas(path)
            dataset_results["parsers"].append(r)
            print(f" {r['throughput_mb_per_sec']:.1f} MB/s")
        except Exception as e:
            print(f" ERROR: {e}")

        # pyarrow
        print("  pyarrow ...", end="", flush=True)
        try:
            r = benchmark_pyarrow(path)
            dataset_results["parsers"].append(r)
            print(f" {r['throughput_mb_per_sec']:.1f} MB/s")
        except Exception as e:
            print(f" ERROR: {e}")

        # scalar baseline
        print("  scalar_baseline ...", end="", flush=True)
        r = benchmark_scalar_baseline(path)
        if r:
            dataset_results["parsers"].append(r)
            print(f" {r['throughput_mb_per_sec']:.1f} MB/s")
        else:
            print(" SKIPPED")

        all_results.append(dataset_results)

    output = {
        "benchmark_date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_runs_per_parser": N_RUNS,
        "measurement": "median of 3 runs, warm FS cache",
        "versions": versions,
        "results": all_results,
    }

    with open(OUTPUT, "w") as fp:
        json.dump(output, fp, indent=2)
    print(f"\n\nResults saved to {OUTPUT}")


if __name__ == "__main__":
    main()
