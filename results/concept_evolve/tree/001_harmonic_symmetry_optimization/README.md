# Harmonic Symmetry Optimization

## Topic Context

The univalent Bloch constant B_u measures the largest disk guaranteed in the image of any normalized univalent function on the unit disk. The best known upper bound B_u ≤ 0.6564 (Carroll & Ortega-Cerdà, 2008) comes from constructing a specific domain: a disk with 3 harmonically symmetric arcs removed. Harmonic symmetry means that the harmonic measure of each arc, as seen from the origin, satisfies specific balance conditions.

The key insight is that the extremal domain (if it exists) must satisfy Jenkins' condition involving a quadratic differential. Carroll & Ortega-Cerdà exploited Fedorov's explicit solution of the Pólya-Chebotarev problem for 4 symmetric points to construct their domain.

## Mathematical Setup

An arc γ in D is **harmonically symmetric** w.r.t. 0 if ω(0, γ, D\γ) is constant along γ, where ω denotes harmonic measure. For N arcs placed with N-fold rotational symmetry:

- γ_k = e^{2πik/N} · γ_0, k = 0,...,N-1
- Each arc is parameterized by inner radius r, outer radius R, and angular width δ
- The simply connected domain D_N = D \ ∪ γ_k has a Riemann map f: D → D_N
- The covering radius of D_N is the inradius of D_N (radius of largest inscribed disk centered at 0)

## Implementation Backlog

1. **[P0]** Implement Schwarz-Christoffel mapping for disk minus N radial slits
2. **[P0]** Compute conformal radius / inradius as function of slit parameters
3. **[P1]** Set up CMA-ES optimization over slit parameters for N=3 (reproduce 0.6564)
4. **[P1]** Extend to N=4,5,6,7 and compare upper bounds
5. **[P2]** Verify harmonic symmetry condition numerically
6. **[P2]** Study convergence as N → ∞
7. **[P3]** Investigate non-symmetric arc placements
8. **[P3]** Connect to Thomson problem solutions for optimal arc placement

## Key Questions

- Does higher N always give tighter bounds?
- Is there a critical N beyond which the bound stabilizes?
- What is the limiting configuration as N → ∞?
