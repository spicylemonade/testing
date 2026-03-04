# Pólya-Chebotarev Slit Domains

## Topic Context

The Pólya-Chebotarev problem is a classical problem in potential theory: given n points in the complex plane, find the connected compact set of minimal logarithmic capacity containing all n points. The solution consists of analytic arcs (critical trajectories of a quadratic differential) forming a tree-like structure.

For the univalent Bloch constant, the extremal domain is expected to be a disk with slits. The slit endpoints are branch points, and the slit structure must satisfy the Pólya-Chebotarev optimality condition (minimizing capacity). Fedorov solved the case of 4 symmetrically placed points explicitly, which Carroll & Ortega-Cerdà used.

## Connection to B_u

The upper bound construction works as follows:
1. Choose N points on the unit circle (candidate slit endpoints)
2. Find the minimal capacity continuum connecting them (Pólya-Chebotarev)
3. Remove this continuum from the disk
4. The resulting simply connected domain has a computable conformal radius
5. This conformal radius gives an upper bound on B_u

## Implementation Backlog

1. **[P0]** Implement Schiefermayr's inverse polynomial method for N=4
2. **[P0]** Reproduce Fedorov's solution for 4 symmetric points
3. **[P1]** Extend to N=5,6 using homotopy continuation (PHCpack/HomotopyContinuation.jl)
4. **[P2]** Compute conformal radius of resulting domains
5. **[P2]** Compare with harmonic symmetry approach (concept 001)
6. **[P3]** Study non-symmetric point configurations
