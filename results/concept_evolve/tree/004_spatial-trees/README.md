# Concept: Spatial Trees

- Topic Context: Minimal gravity simulation
- Domains: computational geometry, tree data structures, spatial indexing
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Key Components

1. **QuadTreeNode**: Bounding box, center of mass, total mass, children, body list
2. **Tree construction**: Recursive insertion with subdivision at capacity
3. **Force walk**: Recursive traversal with opening angle criterion

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect to force_computation (Barnes-Hut uses quadtree).
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.
