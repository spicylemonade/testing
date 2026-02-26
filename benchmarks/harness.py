"""Benchmarking harness for voxel traversal algorithms.

Configurable grid sizes, ray counts, distributions, and occupancy levels.
Outputs results as JSON for downstream analysis.
"""

import json
import time
import sys
import os
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import random_grid, full_grid, empty_grid


GRID_SIZES = [32, 64, 128, 256]
RAY_COUNTS = [1000, 10000, 100000]
SEED = 42


def generate_rays_uniform(n, grid_size, seed=42):
    """Generate uniformly random rays through the grid."""
    rng = np.random.RandomState(seed)
    origins = rng.uniform(-1, grid_size + 1, (n, 3))
    directions = rng.randn(n, 3)
    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    norms[norms < 1e-10] = 1.0
    directions = directions / norms
    return [Ray(origins[i], directions[i]) for i in range(n)]


def generate_rays_coherent(n, grid_size, seed=42):
    """Generate coherent ray bundles (similar direction, nearby origins)."""
    rng = np.random.RandomState(seed)
    # Base direction + small perturbation
    base_dir = np.array([1.0, 0.3, -0.2])
    base_dir = base_dir / np.linalg.norm(base_dir)
    perturbations = rng.randn(n, 3) * 0.05
    directions = base_dir + perturbations
    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    directions = directions / norms
    # Origins clustered near one face
    origins = np.column_stack([
        rng.uniform(-1, 0, n),
        rng.uniform(grid_size * 0.3, grid_size * 0.7, n),
        rng.uniform(grid_size * 0.3, grid_size * 0.7, n),
    ])
    return [Ray(origins[i], directions[i]) for i in range(n)]


def generate_rays_axis_aligned(n, grid_size, seed=42):
    """Generate axis-aligned rays (along X, Y, or Z)."""
    rng = np.random.RandomState(seed)
    rays = []
    for i in range(n):
        axis = rng.randint(3)
        direction = np.zeros(3)
        direction[axis] = 1.0 if rng.random() > 0.5 else -1.0
        origin = rng.uniform(0, grid_size, 3)
        if direction[axis] > 0:
            origin[axis] = -1.0
        else:
            origin[axis] = grid_size + 1.0
        rays.append(Ray(origin, direction))
    return rays


RAY_GENERATORS = {
    'uniform': generate_rays_uniform,
    'coherent': generate_rays_coherent,
    'axis_aligned': generate_rays_axis_aligned,
}


def benchmark_algorithm(algorithm_fn, grid, rays, n_runs=5):
    """Benchmark a traversal algorithm.

    Args:
        algorithm_fn: callable(grid, ray) -> list of voxels
        grid: VoxelGrid
        rays: list of Ray objects
        n_runs: number of repetitions

    Returns:
        dict with timing statistics and metrics
    """
    timings = []
    total_voxels = 0

    for run in range(n_runs):
        voxel_count = 0
        start = time.perf_counter_ns()
        for ray in rays:
            result = algorithm_fn(grid, ray)
            voxel_count += len(result)
        end = time.perf_counter_ns()
        elapsed_ns = end - start
        timings.append(elapsed_ns)
        if run == 0:
            total_voxels = voxel_count

    timings_sec = [t / 1e9 for t in timings]
    n_rays = len(rays)

    return {
        'timings_ns': timings,
        'mean_time_s': float(np.mean(timings_sec)),
        'std_time_s': float(np.std(timings_sec)),
        'min_time_s': float(np.min(timings_sec)),
        'max_time_s': float(np.max(timings_sec)),
        'throughput_rays_per_sec': float(n_rays / np.mean(timings_sec)),
        'avg_voxels_per_ray': float(total_voxels / n_rays) if n_rays > 0 else 0,
        'n_rays': n_rays,
        'n_runs': n_runs,
    }


def run_benchmarks(algorithms, grid_sizes=None, ray_counts=None,
                   distributions=None, densities=None, n_runs=5,
                   output_path=None):
    """Run full benchmark suite.

    Args:
        algorithms: dict of {name: callable(grid, ray)}
        grid_sizes: list of grid side lengths
        ray_counts: list of ray counts
        distributions: list of distribution names
        densities: list of occupancy density values
        n_runs: repetitions per config
        output_path: path to save JSON results

    Returns:
        list of result dicts
    """
    if grid_sizes is None:
        grid_sizes = GRID_SIZES
    if ray_counts is None:
        ray_counts = RAY_COUNTS
    if distributions is None:
        distributions = list(RAY_GENERATORS.keys())
    if densities is None:
        densities = [0.5]

    results = []
    total = len(algorithms) * len(grid_sizes) * len(ray_counts) * len(distributions) * len(densities)
    idx = 0

    for alg_name, alg_fn in algorithms.items():
        for gs in grid_sizes:
            for density in densities:
                grid = random_grid(gs, density=density, seed=SEED)
                for dist_name in distributions:
                    gen_fn = RAY_GENERATORS[dist_name]
                    for rc in ray_counts:
                        idx += 1
                        print(f"[{idx}/{total}] {alg_name} | grid={gs}^3 | "
                              f"density={density} | dist={dist_name} | rays={rc}")

                        rays = gen_fn(rc, gs, seed=SEED)
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

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {output_path}")

    return results


def get_memory_usage_bytes(grid):
    """Estimate memory usage of a VoxelGrid."""
    return grid.data.nbytes


if __name__ == '__main__':
    from src.traversal.dda import dda_traversal

    algorithms = {
        'dda': dda_traversal,
    }

    results = run_benchmarks(
        algorithms,
        grid_sizes=[32, 64],
        ray_counts=[1000],
        n_runs=3,
        output_path='results/quick_bench.json',
    )
    print(f"\nCompleted {len(results)} benchmarks")
