# 010: Conformal Welding and Boundary Correspondence

## Topic Context

Conformal welding is the process of constructing a Jordan curve (and hence a simply connected domain) from a homeomorphism h: S^1 -> S^1. The curve is the common boundary of two conformal maps: one from the unit disk and one from the complement.

Carroll and Ortega-Cerda used conformal welding to prove the existence of harmonically symmetric domains. The key advantage of this approach is that the welding homeomorphism provides a natural parameterization of the space of simply connected domains, enabling systematic optimization.

## Implementation Backlog

1. [ ] Implement conformal welding solver (Fredholm integral equation approach)
2. [ ] Parameterize h via Fourier coefficients
3. [ ] Verify: h = identity gives unit disk
4. [ ] Implement Bloch radius computation for welded domains
5. [ ] Set up CMA-ES optimizer over Fourier coefficients
6. [ ] Run with n=3 harmonics (matching known extremal symmetry)
7. [ ] Extend to n=5,7 harmonics for finer search
8. [ ] Compare discovered domains with Carroll-Ortega-Cerda construction
