# SOA_STATE

Structure-of-Arrays (SoA) particle state: flat typed arrays for positions, velocities, and masses. Maximum cache coherence, minimal allocation, zero indirection. The anti-OOP particle system.

## Mathematical Formalization

State S = (X, V, M) where X in R^(N x d), V in R^(N x d), M in R^N. All operations are batched: X' = X + V*dt is a single vectorized op over contiguous memory.

## Analogical Connections

- SoA <-> columnar databases (Parquet, Arrow) optimized for analytical queries over rows
- SoA <-> GPU texture buffers (data must be contiguous for SIMD/warp execution)
- Flat arrays <-> tensor layout in deep learning frameworks (contiguous for matmul)

## Implementation Hypothesis

In Python: numpy arrays of shape (N,2) for pos/vel, (N,) for mass. In TS: Float64Array(N*2) with stride-2 access. The entire simulation state is 5*N floats = 40KB for N=1000.

## Experiment Seed

Benchmark AoS (array of Body objects) vs SoA (flat arrays) for N=100,1000,10000 force calculations. Measure wall-clock time. SoA should be 2-5x faster due to cache effects.
