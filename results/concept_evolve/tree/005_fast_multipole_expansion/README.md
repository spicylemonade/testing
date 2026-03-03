# Fast Multipole Expansion

## Topic Context

The Fast Multipole Method, developed by Greengard and Rokhlin (1987), was named one of the top 10 algorithms of the 20th century. It achieves truly linear O(N) complexity for N-body force computation, compared to O(N log N) for Barnes-Hut. The key insight is to translate multipole expansions between levels of the spatial tree (M2M upward, M2L across, L2L downward) rather than evaluating each particle independently.

FMM is used in molecular dynamics (GROMACS integrates a CUDA FMM), electrostatics, acoustics, and gravitational dynamics. The expansion order p controls accuracy: p=6 typically gives ~6 digits of precision.

### Key Ideas
- Multipole expansion represents the far-field of a cluster of sources
- Local expansion represents the effect of far-away sources on a cluster
- Three translation operators: M2M, M2L, L2L
- O(N) complexity for any fixed precision

### Cross-Domain Connections
- Fourier decomposition of signals (frequency = multipole order)
- Wavelet multiresolution (locality + multi-scale)
- Particle-mesh methods in cosmological simulation

## Implementation Backlog

- [ ] Implement 2D multipole expansion up to order p
- [ ] Implement M2M translation operator
- [ ] Implement M2L translation operator
- [ ] Implement L2L translation operator
- [ ] Build tree and run full FMM algorithm
- [ ] Benchmark vs Barnes-Hut and direct summation
- [ ] Tune expansion order p vs accuracy
- [ ] Port to GPU using CUDA or compute shaders
