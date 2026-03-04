#!/usr/bin/env python3
"""Run scalar baseline parser benchmarks and save results."""
import json
import subprocess
import os
import glob

DATA_DIR = "results/benchmarks/data"
PARSER = "src/baseline/scalar_parser"
OUTPUT = "results/benchmarks/baseline_metrics.json"

def main():
    results = []
    csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))

    for f in csv_files:
        print(f"Benchmarking {os.path.basename(f)} ...")
        r = subprocess.run([PARSER, f, "--benchmark"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            data = json.loads(r.stdout.strip())
            results.append(data)
            print(f"  -> {data['throughput_mb_per_sec']:.1f} MB/s, {data['rows']} rows")
        else:
            print(f"  ERROR: {r.stderr}")

    output = {
        "parser": "scalar_baseline",
        "compiler": "gcc -O2",
        "results": results,
        "summary": {
            "avg_throughput_mb_per_sec": sum(r["throughput_mb_per_sec"] for r in results) / len(results) if results else 0,
            "total_bytes": sum(r["file_size_bytes"] for r in results),
        }
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as fp:
        json.dump(output, fp, indent=2)
    print(f"\nResults saved to {OUTPUT}")
    print(f"Average throughput: {output['summary']['avg_throughput_mb_per_sec']:.1f} MB/s")

if __name__ == "__main__":
    main()
