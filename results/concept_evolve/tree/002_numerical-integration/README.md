# Concept: Numerical Integration

- Topic Context: Minimal gravity simulation
- Domains: numerical analysis, Hamiltonian mechanics, geometric integration
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Key Methods

1. **Symplectic Euler** (1st order): Simplest symplectic method, asymmetric
2. **Leapfrog / Stormer-Verlet** (2nd order): Workhorse of N-body simulation
3. **Yoshida 4th-order**: Triple-jump composition of leapfrog stages
4. **Adaptive timestep**: Close-encounter detection with dt modulation

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect this concept to force_computation (force callback interface).
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.

## References
- Yoshida (1990): 4th-order symplectic construction
- Hairer et al. (2006): Geometric numerical integration
- Verlet (1967): Original velocity Verlet method
- Wisdom & Holman (1991): Symplectic maps for N-body
