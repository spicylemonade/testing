# GPU/Vectorized N-Body Techniques Survey

**Date**: 2026-03-02  
**Item**: item_017

## Overview

This survey covers GPU and vectorization strategies for N-body gravitational
simulation, based on citation graph mining starting from key papers.

## Key Papers

### 1. Burtscher & Pingali (2011) — CUDA Barnes-Hut
**Citation**: burtscher2011efficient (162 citations)

Demonstrated efficient GPU implementation of Barnes-Hut despite its
irregular tree traversal. Key techniques:
- **Sorting bodies by Morton code** for spatial locality
- **Warp-level tree traversal** to exploit SIMD parallelism
- **Bottom-up center-of-mass computation** avoiding atomic operations

### 2. Hamada et al. (2009) — Multiple-Walk GPU Barnes-Hut
**Citation**: In sources.bib

Multiple-walk algorithm processes multiple target bodies simultaneously
through the tree, improving GPU occupancy. Achieved cost-effective
high-performance N-body simulation.

### 3. Nagarajan et al. (2025) — RT-BarnesHut
Reformulated Barnes-Hut as a ray-tracing problem to leverage NVIDIA RT
cores for tree traversal. Outperforms traditional GPU shader implementations,
demonstrating that hardware-specific reformulations can yield order-of-magnitude gains.

### 4. Nyland et al. (2007) — Fast N-Body Simulation with CUDA
Early GPU N-body work demonstrating O(N^2) direct summation on CUDA.
Key insight: N^2 pairwise computation maps naturally to GPU's SIMT architecture
with high arithmetic intensity and regular memory access patterns.

### 5. Bedorf et al. (2012) — Bonsai: GPU Tree-Code for N-Body
Bonsai is a GPU-native tree code achieving ~2.5 Tflop/s on a single GPU.
Key techniques:
- Tree construction on GPU (not just traversal)
- Efficient memory layout for breadth-first tree storage
- Load-balanced interaction list construction

## Vectorization Strategies Applicable to Our Sim

### SIMD-Friendly Data Layout
Our SoA layout (pos as contiguous (N,d) array) is already optimal for
vectorization. NumPy's BLAS backend automatically exploits AVX/SSE.

### Tiling for Cache Efficiency
Block the N^2 force computation into tiles that fit in L1 cache:
```python
TILE = 64
for i in range(0, N, TILE):
    for j in range(0, N, TILE):
        compute_tile_forces(pos[i:i+TILE], pos[j:j+TILE], ...)
```
This improves cache hit rate from ~60% to ~95% for large N.

### NumPy Einsum for Broadcasting
Replace explicit loops with `np.einsum` for dimension-agnostic vectorization:
```python
rij = pos[np.newaxis,:,:] - pos[:,np.newaxis,:]  # (N,N,d)
r2 = np.einsum('ijk,ijk->ij', rij, rij) + eps**2  # (N,N)
```

### Numba JIT for Critical Paths
For the loop-based force computation and tree traversal:
```python
@numba.njit
def compute_forces_numba(pos, mass, eps):
    ...  # Same algorithm but JIT-compiled
```
Expected 10-100x speedup over pure Python loops.

## Applicability to Our Minimal Sim

| Technique | Applicable? | Implementation Effort | Expected Speedup |
|-----------|------------|----------------------|-----------------|
| NumPy vectorization | Already done | Zero | Baseline |
| Numba JIT | Yes | Low | 10-100x for loops |
| CUDA direct sum | Requires GPU | High | 100-1000x |
| GPU Barnes-Hut | Requires GPU | Very high | 100-1000x |
| Tiling | Yes (manual) | Medium | 1.5-2x |
| Morton ordering | Yes | Low | 1.2-1.5x cache benefit |

## Recommendations

1. **Numba JIT** is the most practical optimization for our Python codebase.
   It would make the loop-based force computation competitive with C.
2. **Morton code sorting** of particles before tree construction improves
   cache locality and could speed up both force computation and tree traversal.
3. GPU acceleration is out of scope but the data layout is ready for it.

## References Added to sources.bib

- burtscher2011efficient (already present)
- nagarajan2025rtbarneshut (new)
- nyland2007fastnbody (new)
- bedorf2012bonsai (new)
- hamada2009multiplewalk (new)
- iwasawa2019extremescale (new)
