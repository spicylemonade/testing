# Project Structure

## Directory Layout

```
src/                     # Source code for all algorithms and data structures
  core/                  # Core data structures
    voxel_grid.py        # VoxelGrid class (NxNxN occupancy grid)
    ray.py               # Ray class (origin, direction, parameterized evaluation)
    grid_generators.py   # Test grid generators (empty, full, random, sphere, planes)
  traversal/             # Traversal algorithm implementations
    dda.py               # Amanatides-Woo DDA baseline
    bresenham.py         # 3D Bresenham / supercover traversal
    simd_dda.py          # NumPy-vectorized batch DDA
    branchless.py        # Branchless DDA variant
    cache_aware.py       # Morton-code (Z-order) cache-aware traversal
    hierarchical.py      # Two-level bitmask-based empty-space skipping
    adaptive_hybrid.py   # Novel adaptive hybrid algorithm
    coherent_batch.py    # Coherent ray batching with shared state
  utils/                 # Utility modules
    morton.py            # Morton code encoding/decoding
    timing.py            # High-resolution timing utilities

tests/                   # Test suite (pytest) — 180 tests, 98% coverage
  test_core.py           # Tests for VoxelGrid, Ray, generators
  test_dda.py            # DDA correctness tests
  test_bresenham.py      # Bresenham correctness tests
  test_correctness.py    # Cross-algorithm correctness & stress tests (95 tests)
  test_coverage.py       # Additional coverage tests (Morton, coherent batch, SIMD, etc.)

benchmarks/              # Benchmark scripts
  harness.py             # Configurable benchmarking harness
  run_baseline.py        # Baseline DDA + Bresenham benchmarks
  run_scaling.py         # Scaling analysis (throughput vs grid size)
  run_sensitivity.py     # Sensitivity analysis (density + coherence sweeps)
  run_comprehensive.py   # Full benchmark suite (7 algos × 4 sizes × 3 dists × 3 densities)

data/                    # Test grids and generated data
results/                 # Experimental results (JSON)
figures/                 # Publication-quality figures (PNG + PDF)
docs/                    # Documentation
  figures/               # Additional documentation figures

README.md                # Project overview, quick-start, algorithm descriptions
literature_review.md     # Comprehensive literature review (17 papers)
RESULTS.md               # Experimental results and analysis
DESIGN.md                # Novel algorithm design rationale
sources.bib              # BibTeX bibliography (17 entries)
requirements.txt         # Python dependencies
```

## Design Principles

- **Modularity**: Each algorithm in its own file with a common interface
- **Testability**: Every public function has unit tests
- **Reproducibility**: Fixed random seeds (42), JSON result output
- **Performance**: NumPy vectorization, minimal Python overhead in hot paths
