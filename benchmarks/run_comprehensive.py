"""Comprehensive benchmark of all 7 traversal algorithms.

Item 018: benchmarks across grid sizes, ray counts, distributions, and densities.
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import random_grid
from src.traversal.dda import dda_traversal
from src.traversal.bresenham import bresenham_traversal
from src.traversal.branchless import branchless_dda_traversal
from src.traversal.cache_aware import cache_aware_dda_traversal
from src.traversal.hierarchical import hierarchical_traversal, HierarchicalGrid
from src.traversal.adaptive_hybrid import adaptive_hybrid_traversal, AdaptiveGrid
from src.traversal.simd_dda import simd_dda_traversal
from benchmarks.harness import (
    generate_rays_uniform, generate_rays_coherent, generate_rays_axis_aligned,
    benchmark_algorithm,
)


def bresenham_adapter(grid, ray):
    """Adapter to make Bresenham match DDA interface."""
    size = grid.size
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
    p0 = np.clip(p0, 0, size - 0.001)
    p1 = np.clip(p1, 0, size - 0.001)
    voxels = bresenham_traversal(p0, p1, connectivity=26)
    return [(v, 0.0, 0.0) for v in voxels
            if 0 <= v[0] < size and 0 <= v[1] < size and 0 <= v[2] < size]


SEED = 42
RAY_GENERATORS = {
    'uniform': generate_rays_uniform,
    'coherent': generate_rays_coherent,
    'axis_aligned': generate_rays_axis_aligned,
}


def make_hierarchical_adapter(grid, density):
    """Pre-build hierarchical grid, return adapter closure."""
    hgrid = HierarchicalGrid(grid)
    def traverse(g, ray):
        return hierarchical_traversal(hgrid, ray)
    return traverse


def make_adaptive_adapter(grid, density):
    """Pre-build adaptive grid, return adapter closure."""
    agrid = AdaptiveGrid(grid)
    def traverse(g, ray):
        return adaptive_hybrid_traversal(agrid, ray)
    return traverse


if __name__ == '__main__':
    grid_sizes = [32, 64, 128, 256]
    ray_counts = [1000, 10000]
    distributions = ['uniform', 'coherent', 'axis_aligned']
    densities = [0.1, 0.5, 0.9]
    n_runs = 3

    # Base algorithms (no pre-built grids needed)
    base_algorithms = {
        'dda': dda_traversal,
        'bresenham': bresenham_adapter,
        'branchless': branchless_dda_traversal,
        'cache_aware': cache_aware_dda_traversal,
        'simd_dda': simd_dda_traversal,
    }
    # Algorithms needing pre-built grids
    prebuild_algorithms = ['hierarchical', 'adaptive_hybrid']

    results = []
    total_base = len(base_algorithms) * len(grid_sizes) * len(ray_counts) * len(distributions) * len(densities)
    total_prebuild = len(prebuild_algorithms) * len(grid_sizes) * len(ray_counts) * len(distributions) * len(densities)
    total = total_base + total_prebuild
    idx = 0

    for gs in grid_sizes:
        # Limit ray count for large grids to keep runtime reasonable
        rc_for_size = ray_counts if gs <= 128 else [1000]

        for density in densities:
            grid = random_grid(gs, density=density, seed=SEED)

            # Pre-build hierarchical and adaptive grids once per (grid_size, density)
            h_fn = make_hierarchical_adapter(grid, density)
            a_fn = make_adaptive_adapter(grid, density)
            all_algorithms = {**base_algorithms, 'hierarchical': h_fn, 'adaptive_hybrid': a_fn}

            for dist_name in distributions:
                gen_fn = RAY_GENERATORS[dist_name]
                for rc in rc_for_size:
                    rays = gen_fn(rc, gs, seed=SEED)

                    for alg_name, alg_fn in all_algorithms.items():
                        idx += 1
                        print(f"[{idx}/{total}] {alg_name:16s} | grid={gs:>3}^3 | "
                              f"d={density:.1f} | {dist_name:>12s} | rays={rc}")

                        metrics = benchmark_algorithm(alg_fn, grid, rays, n_runs=n_runs)
                        result = {
                            'algorithm': alg_name,
                            'grid_size': gs,
                            'density': density,
                            'distribution': dist_name,
                            'ray_count': rc,
                            **metrics,
                        }
                        results.append(result)

    # Save results
    Path('results').mkdir(exist_ok=True)
    with open('results/experiment_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nTotal data points: {len(results)}")
    print("Results saved to results/experiment_results.json")

    # Quick summary
    print("\n" + "=" * 100)
    print("SUMMARY: Mean throughput (rays/s) by algorithm and grid size (density=0.5, uniform, 10K rays)")
    print("=" * 100)
    print(f"{'Algorithm':<18}", end="")
    for gs in grid_sizes:
        print(f"  {gs:>3}^3", end="")
    print()
    print("-" * 100)
    for alg in ['dda', 'bresenham', 'branchless', 'cache_aware', 'simd_dda', 'hierarchical', 'adaptive_hybrid']:
        print(f"{alg:<18}", end="")
        for gs in grid_sizes:
            matches = [r for r in results
                       if r['algorithm'] == alg and r['grid_size'] == gs
                       and r['density'] == 0.5 and r['distribution'] == 'uniform'
                       and r['ray_count'] == 10000]
            if matches:
                print(f"  {matches[0]['throughput_rays_per_sec']:>7.0f}", end="")
            else:
                print(f"  {'N/A':>7}", end="")
        print()
