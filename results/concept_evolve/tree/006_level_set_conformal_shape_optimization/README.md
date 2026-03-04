# 006: Level Set Conformal Shape Optimization

## Topic Context

Level set methods represent domain boundaries as zero level sets of higher-dimensional functions and evolve them via Hamilton-Jacobi PDEs. This approach, pioneered by Osher-Sethian and applied to shape optimization by Allaire and others, handles topology changes naturally.

For the Bloch constant problem, the idea is: parameterize simply connected domains via their boundary, compute the conformal map and Bloch radius, then use the shape gradient to evolve the boundary toward extremality.

## Implementation Backlog

1. [ ] Implement level set evolution on a 2D grid
2. [ ] Couple with conformal map solver (boundary integral or SC method)
3. [ ] Compute shape derivative of Bloch radius
4. [ ] Handle simply-connectedness constraint during evolution
5. [ ] Test with various initial shapes (disk, ellipse, rectangle)
6. [ ] Compare discovered extremal shapes with known slit domains
7. [ ] Add multi-resolution refinement for boundary accuracy
