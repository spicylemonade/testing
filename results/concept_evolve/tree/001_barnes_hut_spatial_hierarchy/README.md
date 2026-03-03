# Barnes-Hut Spatial Hierarchy

## Topic Context

The Barnes-Hut algorithm (1986) is the foundational acceleration technique for N-body gravity simulations. It reduces the O(N^2) pairwise force computation to O(N log N) by constructing a spatial tree (quadtree in 2D, octree in 3D) that aggregates distant particles into single nodes characterized by their total mass and center of mass. The opening angle parameter theta controls how aggressively distant nodes are approximated.

This technique is central to virtually all large-scale astrophysical simulations (galaxy formation, planetary dynamics, cosmological structure) and has been adapted for electrostatics, vortex methods, and even graph layout algorithms.

### Key Ideas
- Recursive spatial subdivision into quadrants/octants
- Bottom-up computation of center-of-mass and total mass
- Top-down force walk with theta-based pruning
- Rebuild tree every timestep (avoids tangling)

### Cross-Domain Connections
- Identical to KD-trees used in ML for nearest-neighbor search
- Same principle as hierarchical clustering in data mining
- DNS caching hierarchy mirrors the spatial hierarchy

## Implementation Backlog

- [ ] Implement 2D quadtree data structure with insert and query
- [ ] Compute center-of-mass and total mass bottom-up
- [ ] Implement force walk with configurable theta
- [ ] Benchmark against direct summation for N=1000,10000
- [ ] Profile tree construction vs force walk time
- [ ] Extend to 3D octree
- [ ] Implement parallel tree walk for GPU
- [ ] Compare with Fast Multipole Method for same accuracy
