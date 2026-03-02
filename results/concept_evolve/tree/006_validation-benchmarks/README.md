# Concept: Validation Benchmarks

- Topic Context: Minimal gravity simulation
- Domains: celestial mechanics, numerical validation, benchmark design
- Purpose: Provide ground truth for testing simulation correctness.

## Test Problems

1. **Kepler two-body**: Analytical period and orbit shape
2. **Figure-eight 3-body**: Chenciner & Montgomery (2000) periodic solution
3. **Plummer sphere**: Statistical density profile for N-body
4. **Hyperbolic encounter**: Analytical hyperbolic orbit for adaptive timestep testing
5. **Solar system inner planets**: Approximate real-world test

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect to numerical_integration, force_computation, conservation_laws.
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.
