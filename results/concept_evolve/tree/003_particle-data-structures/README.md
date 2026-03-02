# Concept: Particle Data Structures

- Topic Context: Minimal gravity simulation
- Domains: software engineering, data modeling, scientific computing
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Key Design Decisions

1. **Body dataclass**: mass (scalar), position (2D array), velocity (2D array), acceleration (2D array)
2. **System class**: Collection manager with add/remove/query, vectorized bulk accessors
3. **Serialization**: JSON for small state, numpy arrays for bulk data

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect to force_computation (force arrays), numerical_integration (state updates).
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.
