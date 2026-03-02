# Concept: Force Computation

- Topic Context: Minimal gravity simulation
- Domains: computational physics, algorithm design, numerical methods
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Key Algorithms

1. **Brute-Force O(N^2)**: Direct pairwise summation with Plummer softening
2. **Barnes-Hut O(N log N)**: Quadtree spatial decomposition with opening angle theta
3. **FMM O(N)**: Fast Multipole Method (out of scope for minimal sim)

## ConceptEvolve Probe Results (Phase 3)

### Alternative 1: Barnes-Hut Tree Code

**Complexity**: O(N log N) construction + O(N log N) force evaluation  
**Trade-offs**:
- Pro: Dramatic speedup for N > ~100 bodies
- Pro: Accuracy controllable via theta parameter (0.3-1.0)
- Con: Tree construction overhead dominates for small N
- Con: Implementation complexity (quadtree, center-of-mass, recursive walk)

**Error analysis** (Pfalzner & Gibbon 1996 [pfalzner1996]):
- theta=0.5: ~1% force error, ~4x speedup at N=1000
- theta=0.3: ~0.1% force error, ~2x speedup at N=1000
- theta->0: converges to brute force

### Alternative 2: Vectorized/SIMD Brute Force

**Complexity**: O(N^2) but with hardware-level parallelism  
**Trade-offs**:
- Pro: Embarrassingly parallel -- map perfectly to numpy broadcasting
- Pro: No approximation error
- Pro: Simple to implement and debug
- Con: Fundamental O(N^2) scaling limits N to ~1000 in real-time

**Our implementation** uses numpy einsum for vectorized computation, achieving near-SIMD performance on CPU. For N<200, this is faster than Barnes-Hut due to zero tree overhead.

### Alternative 3: Cutoff-Radius Neighbor Lists

**Complexity**: O(N * k) where k is average neighbor count  
**Trade-offs**:
- Pro: Simple to implement with spatial hashing
- Pro: Ideal for short-range forces (SPH, molecular dynamics)
- Con: Gravity is long-range -- cannot truncate without significant error
- Con: Not suitable for gravitational simulation without far-field correction

**Decision**: Not implemented. Gravity's 1/r^2 long-range nature means cutoff introduces unacceptable errors for orbital dynamics.

## Walk Paths Explored

1. `force_computation -> spatial_trees -> particle_data_structures -> conservation_laws`
   - This path shows how spatial trees depend on particle data structures, and conservation metrics validate force accuracy.

2. `force_computation -> numerical_integration -> conservation_laws -> validation_benchmarks`
   - Forces flow into integrators, which are validated by conservation metrics against known benchmarks.

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect this concept to at least one sibling concept (numerical-integration, particle-data-structures).
- [x] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.

## References
- Barnes & Hut (1986): Hierarchical force algorithm [barnes1986]
- Pfalzner & Gibbon (1996): Tree methods error analysis [pfalzner1996]
- Greengard & Rokhlin (1987): FMM algorithm [greengard1987]
- Efstathiou et al. (1985): Plummer softening [efstathiou1985]
- Burtscher & Pingali (2011): GPU Barnes-Hut [burtscher2011]
