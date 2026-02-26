"""Scaling analysis: throughput vs grid size for each algorithm.

Item 019: log-log plots and empirical scaling exponents.
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.grid_generators import random_grid
from src.traversal.dda import dda_traversal
from src.traversal.branchless import branchless_dda_traversal
from src.traversal.cache_aware import cache_aware_dda_traversal
from src.traversal.hierarchical import hierarchical_traversal, HierarchicalGrid
from src.traversal.adaptive_hybrid import adaptive_hybrid_traversal, AdaptiveGrid
from benchmarks.harness import generate_rays_uniform, benchmark_algorithm

SEED = 42
N_RAYS = 1000
N_RUNS = 3


if __name__ == '__main__':
    grid_sizes = [16, 32, 64, 128, 256, 512]
    density = 0.3
    results = []

    algorithms_base = {
        'dda': dda_traversal,
        'branchless': branchless_dda_traversal,
        'cache_aware': cache_aware_dda_traversal,
    }

    for gs in grid_sizes:
        print(f"Grid size: {gs}^3")
        grid = random_grid(gs, density=density, seed=SEED)
        rays = generate_rays_uniform(N_RAYS, gs, seed=SEED)

        hgrid = HierarchicalGrid(grid)
        agrid = AdaptiveGrid(grid)

        all_algs = {
            **algorithms_base,
            'hierarchical': lambda g, r, hg=hgrid: hierarchical_traversal(hg, r),
            'adaptive_hybrid': lambda g, r, ag=agrid: adaptive_hybrid_traversal(ag, r),
        }

        for alg_name, alg_fn in all_algs.items():
            metrics = benchmark_algorithm(alg_fn, grid, rays, n_runs=N_RUNS)
            entry = {
                'grid_size': gs,
                'algorithm': alg_name,
                'throughput': metrics['throughput_rays_per_sec'],
                'avg_voxels_per_ray': metrics['avg_voxels_per_ray'],
                'mean_time_s': metrics['mean_time_s'],
                'std_time_s': metrics['std_time_s'],
            }
            results.append(entry)
            print(f"  {alg_name:18s}: {metrics['throughput_rays_per_sec']:>8.0f} rays/s, "
                  f"{metrics['avg_voxels_per_ray']:.1f} voxels/ray")

    Path('results').mkdir(exist_ok=True)
    with open('results/scaling_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} data points to results/scaling_results.json")
