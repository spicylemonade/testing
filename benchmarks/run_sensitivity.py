"""Sensitivity analysis: density sweep and coherence sweep.

Item 022: measure impact of grid occupancy and ray coherence on each algorithm.
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
from src.traversal.branchless import branchless_dda_traversal
from src.traversal.cache_aware import cache_aware_dda_traversal
from src.traversal.hierarchical import hierarchical_traversal, HierarchicalGrid
from src.traversal.adaptive_hybrid import adaptive_hybrid_traversal, AdaptiveGrid
from benchmarks.harness import generate_rays_uniform, benchmark_algorithm


SEED = 42
GRID_SIZE = 128
N_RAYS = 1000
N_RUNS = 3

ALGORITHMS = {
    'dda': dda_traversal,
    'branchless': branchless_dda_traversal,
    'cache_aware': cache_aware_dda_traversal,
}


def generate_coherent_rays(n, gs, spread=0.05, seed=42):
    rng = np.random.RandomState(seed)
    bd = np.array([1.0, 0.3, -0.2])
    bd /= np.linalg.norm(bd)
    pert = rng.randn(n, 3) * spread
    dirs = bd + pert
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    origs = np.column_stack([
        rng.uniform(-1, 0, n),
        rng.uniform(gs * 0.3, gs * 0.7, n),
        rng.uniform(gs * 0.3, gs * 0.7, n),
    ])
    return [Ray(origs[i], dirs[i]) for i in range(n)]


# ---- Density sweep ----
def run_density_sweep():
    print("=" * 60)
    print("DENSITY SWEEP: 5% to 95% occupancy, 128^3, 1K rays")
    print("=" * 60)
    densities = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
    rays = generate_rays_uniform(N_RAYS, GRID_SIZE, seed=SEED)
    results = []

    for density in densities:
        grid = random_grid(GRID_SIZE, density=density, seed=SEED)
        hgrid = HierarchicalGrid(grid)
        agrid = AdaptiveGrid(grid)

        all_algs = {
            **ALGORITHMS,
            'hierarchical': lambda g, r, hg=hgrid: hierarchical_traversal(hg, r),
            'adaptive_hybrid': lambda g, r, ag=agrid: adaptive_hybrid_traversal(ag, r),
        }

        for alg_name, alg_fn in all_algs.items():
            metrics = benchmark_algorithm(alg_fn, grid, rays, n_runs=N_RUNS)
            entry = {
                'sweep': 'density',
                'density': density,
                'algorithm': alg_name,
                'throughput': metrics['throughput_rays_per_sec'],
                'mean_time_s': metrics['mean_time_s'],
                'std_time_s': metrics['std_time_s'],
            }
            results.append(entry)
            print(f"  d={density:.2f} {alg_name:18s}: {metrics['throughput_rays_per_sec']:>8.0f} rays/s")

    return results


# ---- Coherence sweep ----
def run_coherence_sweep():
    print("\n" + "=" * 60)
    print("COHERENCE SWEEP: spread 0.01 to 10.0, 128^3, 1K rays, density=0.3")
    print("=" * 60)
    spreads = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    grid = random_grid(GRID_SIZE, density=0.3, seed=SEED)
    hgrid = HierarchicalGrid(grid)
    agrid = AdaptiveGrid(grid)
    results = []

    all_algs = {
        **ALGORITHMS,
        'hierarchical': lambda g, r, hg=hgrid: hierarchical_traversal(hg, r),
        'adaptive_hybrid': lambda g, r, ag=agrid: adaptive_hybrid_traversal(ag, r),
    }

    for spread in spreads:
        rays = generate_coherent_rays(N_RAYS, GRID_SIZE, spread=spread, seed=SEED)
        for alg_name, alg_fn in all_algs.items():
            metrics = benchmark_algorithm(alg_fn, grid, rays, n_runs=N_RUNS)
            entry = {
                'sweep': 'coherence',
                'spread': spread,
                'algorithm': alg_name,
                'throughput': metrics['throughput_rays_per_sec'],
                'mean_time_s': metrics['mean_time_s'],
                'std_time_s': metrics['std_time_s'],
            }
            results.append(entry)
            print(f"  spread={spread:5.2f} {alg_name:18s}: {metrics['throughput_rays_per_sec']:>8.0f} rays/s")

    return results


if __name__ == '__main__':
    density_results = run_density_sweep()
    coherence_results = run_coherence_sweep()

    all_results = density_results + coherence_results
    Path('results').mkdir(exist_ok=True)
    with open('results/sensitivity_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved {len(all_results)} data points to results/sensitivity_results.json")
