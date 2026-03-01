"""Reproduce all results: baselines, novel algorithm, and figures.

Usage:
    python run_all.py          # Run everything
    python run_all.py --quick  # Quick mode (smaller graphs)
"""

import sys
import subprocess
import os


def run(cmd, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, shell=True, cwd=os.path.dirname(__file__) or '.')
    if result.returncode != 0:
        print(f"\n  ERROR: {label} failed with exit code {result.returncode}")
        return False
    return True


def main():
    quick = '--quick' in sys.argv

    os.makedirs('results', exist_ok=True)
    os.makedirs('figures', exist_ok=True)

    steps = [
        # Phase 2: Baseline tests
        ("python3 src/baselines/test_dijkstra.py",
         "Step 1: Dijkstra correctness tests"),
        ("python3 src/baselines/test_dmmsy.py",
         "Step 2: DMMSY correctness tests"),

        # Phase 3: Novel algorithm tests
        ("python3 src/novel/core.py",
         "Step 3: Core component tests"),
        ("python3 src/novel/test_novel.py",
         "Step 4: Novel algorithm correctness tests"),

        # Phase 2: Baseline benchmarks
        ("python3 src/benchmarks/run_baselines.py",
         "Step 5: Baseline benchmarks"),

        # Phase 4: Novel benchmarks
        ("python3 src/benchmarks/run_novel.py",
         "Step 6: Novel algorithm benchmarks"),

        # Phase 4: Stress tests
        ("python3 src/benchmarks/run_stress.py",
         "Step 7: Stress tests"),

        # Plots
        ("python3 src/benchmarks/plot_baselines.py",
         "Step 8: Baseline plots"),
        ("python3 src/benchmarks/plot_comparative.py",
         "Step 9: Comparative plots"),
    ]

    passed = 0
    failed = 0
    for cmd, label in steps:
        if run(cmd, label):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"  SUMMARY: {passed} passed, {failed} failed out of {len(steps)} steps")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
