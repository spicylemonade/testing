# Concept: Force Computation

- Topic Context: Minimal gravity simulation
- Domains: computational physics, algorithm design, numerical methods
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Key Algorithms

1. **Brute-Force O(N^2)**: Direct pairwise summation with Plummer softening
2. **Barnes-Hut O(N log N)**: Quadtree spatial decomposition with opening angle theta
3. **FMM O(N)**: Fast Multipole Method (out of scope for minimal sim)

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect this concept to at least one sibling concept (numerical-integration, particle-data-structures).
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.

## References
- Barnes & Hut (1986): Hierarchical force algorithm
- Pfalzner & Gibbon (1996): Tree methods error analysis
- Greengard & Rokhlin (1987): FMM algorithm
