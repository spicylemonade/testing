# 001: Harmonic Symmetry and Extremal Slit Domains

## Topic Context

The univalent Bloch-Landau constant B_u is defined as the infimum of Bloch radii over all univalent functions in the schlicht class. The best known upper bound B_u < 0.6564 was obtained by Carroll and Ortega-Cerda (2009) by constructing domains formed by removing harmonically symmetric arcs from a disk.

**Harmonic symmetry** means that for each removed arc gamma_k, the harmonic measure from the origin of each side of gamma_k is equal. This condition arises naturally from the theory of conformal welding and is connected to Fedorov's solution of the Polya-Chebotarev problem for symmetric point configurations.

The domain that achieves the bound is a disk with 3 arcs removed, each arc positioned at 120-degree intervals, with arc lengths determined by the Polya-Chebotarev solution for 4 symmetrically placed points (the arc endpoints).

## Key Mathematical Objects

- **Harmonic measure**: omega(0, E, D) for E a subset of the boundary of D
- **Slit domain**: D minus a collection of arcs
- **Conformal welding**: technique for constructing domains with prescribed boundary identification
- **Polya-Chebotarev continuum**: minimal capacity set containing given points

## Implementation Backlog

1. [ ] Implement numerical conformal mapping for disk-minus-arcs domains
2. [ ] Parameterize arc configurations (position, length, number)
3. [ ] Compute inradius of image under conformal map from unit disk
4. [ ] Optimize over arc parameters for n=3,4,5,6-fold symmetry
5. [ ] Break symmetry and test asymmetric configurations
6. [ ] Compare all results with Carroll-Ortega-Cerda bound of 0.6564
7. [ ] Implement interval arithmetic verification for best candidate
8. [ ] Document extremal domain geometry and plot

## Connection to B_u Chain

B <= B_l <= L <= B_u. This concept addresses the **upper bound** on B_u by constructing specific domains that provide upper bounds on the supremum of Bloch radii.
