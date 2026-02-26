"""Run baseline benchmarks for DDA and Bresenham algorithms."""

import sys
import os
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.traversal.dda import dda_traversal
from src.traversal.bresenham import bresenham_traversal
from src.core.ray import Ray
from benchmarks.harness import run_benchmarks


def bresenham_adapter(grid, ray):
    """Adapter to make Bresenham match DDA interface for benchmarking.

    Computes start/end points from the ray and grid bounds.
    """
    size = grid.size
    # Compute ray entry/exit with the grid
    inv_dir = ray.inv_direction
    t0 = (0.0 - ray.origin) * inv_dir
    t1 = (float(size) - ray.origin) * inv_dir
    t_enter_arr = np.minimum(t0, t1)
    t_exit_arr = np.maximum(t0, t1)

    t_min = np.max(t_enter_arr)
    t_max = np.min(t_exit_arr)

    for i in range(3):
        if ray.direction[i] == 0.0:
            if ray.origin[i] < 0.0 or ray.origin[i] > size:
                return []

    if t_max < max(t_min, 0.0):
        return []

    t_min = max(t_min, 0.0)
    p0 = ray.at(t_min + 1e-10)
    p1 = ray.at(t_max - 1e-10)
    # Clamp to grid bounds
    p0 = np.clip(p0, 0, size - 0.001)
    p1 = np.clip(p1, 0, size - 0.001)

    voxels = bresenham_traversal(p0, p1, connectivity=26)
    # Filter to grid bounds and return as tuples
    return [(v, 0.0, 0.0) for v in voxels
            if 0 <= v[0] < size and 0 <= v[1] < size and 0 <= v[2] < size]


if __name__ == '__main__':
    algorithms = {
        'dda': dda_traversal,
        'bresenham': bresenham_adapter,
    }

    # Use reasonable sizes for Python-speed benchmarks
    grid_sizes = [32, 64, 128]
    ray_counts = [1000, 10000]
    distributions = ['uniform', 'coherent', 'axis_aligned']
    densities = [0.5]

    print("Running baseline benchmarks...")
    print(f"Configs: {len(algorithms)} algos x {len(grid_sizes)} sizes x "
          f"{len(ray_counts)} ray counts x {len(distributions)} dists = "
          f"{len(algorithms) * len(grid_sizes) * len(ray_counts) * len(distributions)}")

    results = run_benchmarks(
        algorithms,
        grid_sizes=grid_sizes,
        ray_counts=ray_counts,
        distributions=distributions,
        densities=densities,
        n_runs=5,
        output_path='results/baseline_results.json',
    )

    # Summary table
    print("\n" + "=" * 80)
    print("BASELINE RESULTS SUMMARY")
    print("=" * 80)
    print(f"{'Algorithm':<12} {'Grid':>6} {'Rays':>7} {'Distribution':>14} "
          f"{'Throughput':>14} {'Voxels/Ray':>12}")
    print("-" * 80)
    for r in results:
        print(f"{r['algorithm']:<12} {r['grid_size']:>4}^3 {r['ray_count']:>7} "
              f"{r['distribution']:>14} {r['throughput_rays_per_sec']:>12.0f}/s "
              f"{r['avg_voxels_per_ray']:>10.1f}")

    # Write summary to RESULTS.md
    with open('RESULTS.md', 'w') as f:
        f.write("# Experimental Results\n\n")
        f.write("## Baseline Performance (DDA and Bresenham)\n\n")
        f.write("| Algorithm | Grid Size | Rays | Distribution | Throughput (rays/s) | Avg Voxels/Ray |\n")
        f.write("|-----------|-----------|------|-------------|--------------------|--------------|\n")
        for r in results:
            f.write(f"| {r['algorithm']} | {r['grid_size']}^3 | {r['ray_count']} | "
                    f"{r['distribution']} | {r['throughput_rays_per_sec']:.0f} | "
                    f"{r['avg_voxels_per_ray']:.1f} |\n")

    print(f"\nTotal configurations: {len(results)}")
    print("Results saved to results/baseline_results.json and RESULTS.md")
