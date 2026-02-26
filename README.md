# Fast Voxel Grid Traversal: Novel Algorithms and Benchmarks

A research project implementing, benchmarking, and extending voxel grid traversal
algorithms. Seven traversal methods are provided—from the classic Amanatides-Woo
DDA to a novel **Adaptive Hybrid** that combines hierarchical empty-space skipping
with branchless DDA and density-based strategy selection.

## Key Results

| Scenario | Best Algorithm | Speedup vs DDA |
|---|---|---|
| Dense grid, single-ray | Branchless DDA | 1.33x |
| Sparse (structured) | Hierarchical / Adaptive Hybrid | 2.1–4.7x |
| Batch processing (count) | SIMD-vectorized DDA | 6.65x |
| Coherent ray bundles | Coherent Batch (count) | 7–10x |
| Mixed sparse/dense | Adaptive Hybrid | 2.1x sparse, 0.7x dense |

All algorithms are implemented in pure Python/NumPy, verified with 180 tests at 98%
code coverage, and benchmarked across 500+ configurations.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd repo

# Install dependencies
pip install -r requirements.txt
```

**Requirements:** Python 3.9+, NumPy ≥ 1.24, Matplotlib ≥ 3.7, pytest ≥ 7.0

## Quick Start

```python
import numpy as np
from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import random_grid
from src.traversal.dda import dda_traversal

# Create a 64^3 grid with 30% random occupancy
grid = random_grid(64, density=0.3, seed=42)

# Define a ray: origin outside the grid, direction into it
ray = Ray(
    origin=np.array([-1.0, 32.0, 32.0]),
    direction=np.array([1.0, 0.0, 0.0])
)

# Traverse — returns list of (voxel_index, t_enter, t_exit)
voxels = dda_traversal(grid, ray)
for (x, y, z), t_enter, t_exit in voxels[:5]:
    print(f"  Voxel ({x},{y},{z})  t=[{t_enter:.3f}, {t_exit:.3f}]")
```

### Batch Processing (SIMD-vectorized)

```python
from src.traversal.simd_dda import simd_dda_batch

# Process 1000 rays simultaneously
rays = [Ray(np.array([-1.0, i*0.064, 32.0]),
            np.array([1.0, 0.0, 0.0])) for i in range(1000)]
results = simd_dda_batch(grid, rays)  # dict: ray_index -> [(voxel, t_enter, t_exit), ...]
```

### Hierarchical Traversal (for sparse grids)

```python
from src.traversal.hierarchical import HierarchicalGrid, hierarchical_traversal

hgrid = HierarchicalGrid(grid)  # Pre-build 8^3 brick occupancy map
voxels = hierarchical_traversal(hgrid, ray)  # Skips empty bricks
```

## Algorithms

### 1. Amanatides-Woo DDA (`src/traversal/dda.py`)
The classic digital differential analyzer for uniform grids. Steps one voxel at a
time along the axis with the smallest next boundary crossing.
**Complexity:** O(N) per ray where N is the grid side length.

### 2. 3D Bresenham (`src/traversal/bresenham.py`)
Integer-arithmetic line rasterization extended to 3D. Supports both 26-connected
and 6-connected (supercover) modes.
**Complexity:** O(N) per ray.

### 3. Branchless DDA (`src/traversal/branchless.py`)
Replaces the standard if-else axis selection with comparison masking. The inner
loop has only one conditional branch (loop termination).
**Complexity:** O(N) per ray; ~1.33x faster than standard DDA.

### 4. Cache-Aware DDA (`src/traversal/cache_aware.py`)
Stores voxels in Morton (Z-order) curve layout for improved spatial locality.
Uses `src/utils/morton.py` for 3D ↔ Morton index conversion.
**Complexity:** O(N) per ray; up to 1.37x on large grids (≥256³).

### 5. SIMD-Vectorized Batch DDA (`src/traversal/simd_dda.py`)
Processes batches of rays simultaneously using NumPy array operations. The inner
DDA step operates on arrays of ray states with no per-ray Python loops.
**Complexity:** O(N) per ray; 6.65x throughput in count-only mode via amortized
vectorization overhead.

### 6. Hierarchical DDA (`src/traversal/hierarchical.py`)
Two-level structure: coarse 8³-brick occupancy bitmask + fine per-voxel DDA.
Skips entirely empty bricks at the coarse level.
**Complexity:** O(N/B + K·B) where B=8 is brick size, K = occupied bricks hit.
2.1–4.7x on structured sparse grids.

### 7. Adaptive Hybrid (Novel) (`src/traversal/adaptive_hybrid.py`)
Combines hierarchical empty-space skipping with branchless fine-level DDA and a
density-based strategy selector that chooses per-brick between full traversal and
skip mode. See [DESIGN.md](DESIGN.md) for the design rationale.
**Complexity:** Same as hierarchical; selects optimal strategy per brick.

### 8. Coherent Ray Batching (`src/traversal/coherent_batch.py`)
Clusters rays by direction similarity (octant + angular bin hashing), then
applies shared-step vectorized DDA per group. Best for coherent distributions.
**Complexity:** O(N·R/G) amortized where R = rays, G = groups.
7–10x on highly coherent bundles (spread ≤ 0.01).

## Project Structure

```
src/core/              Core data structures (VoxelGrid, Ray, generators)
src/traversal/         All 8 traversal implementations
src/utils/             Morton codes, timing utilities
tests/                 180 tests (pytest), 98% coverage
benchmarks/            Benchmark harness and scripts
results/               JSON benchmark data
figures/               Publication-quality PNG plots
```

See [STRUCTURE.md](STRUCTURE.md) for full details.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=term-missing
```

## Running Benchmarks

```bash
# Baseline benchmarks (DDA + Bresenham)
python benchmarks/run_baseline.py

# Scaling analysis (throughput vs grid size)
python benchmarks/run_scaling.py

# Sensitivity analysis (density + coherence sweeps)
python benchmarks/run_sensitivity.py

# Comprehensive benchmark (all algorithms, all configurations)
python benchmarks/run_comprehensive.py
```

Results are saved as JSON in `results/` and plots as PNG in `figures/`.

## Documentation

- **[RESULTS.md](RESULTS.md)** — Full experimental results, tables, and analysis
- **[DESIGN.md](DESIGN.md)** — Novel adaptive hybrid algorithm design rationale
- **[literature_review.md](literature_review.md)** — Survey of 17 papers and implementations
- **[sources.bib](sources.bib)** — BibTeX bibliography (17 entries)

## References

Key papers that informed this work:

1. Amanatides, J. & Woo, A. (1987). *A Fast Voxel Traversal Algorithm for Ray Tracing.* Eurographics.
2. Siddon, R. L. (1985). *Fast calculation of the exact radiological path for a 3D CT array.* Medical Physics.
3. Laine, S. & Karras, T. (2010). *Efficient Sparse Voxel Octrees.* IEEE TVCG.
4. Kämpe, V., Sintorn, E. & Assarsson, U. (2013). *High Resolution Sparse Voxel DAGs.* ACM TOG.
5. Museth, K. (2021). *NanoVDB: A GPU-Friendly and Portable VDB Data Structure.* SIGGRAPH.
6. Morton, G. M. (1966). *A computer oriented geodetic data base and a new technique in file sequencing.* IBM.
7. dubiousconst282 (2024). *A guide to fast voxel ray tracing using sparse 64-trees.*

See [sources.bib](sources.bib) for the complete bibliography.

## License

Research project. See individual source files for details.
