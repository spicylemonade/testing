# Probe Synthesis: Skinner's Method Bottleneck

## Target
The primary bottleneck in Skinner's growth theorem bootstrap for B_u > 0.5708858: the method reduces the 2D inradius problem to 1D radial estimates, discarding geometric information about the shape of the extremal domain.

## Key Findings from ConceptEvolve Probe

### Forced Bridges to Other Domains

The probe identified 6 cross-domain connections:

1. **Isoperimetric inequalities** → The classical Bonnesen inequality relates area, perimeter, and inradius. For domains with conformal radius 1 at the origin, specialized isoperimetric bounds could constrain B_f using 2D area information that radial methods discard.

2. **Harmonic measure / Brownian motion** → The expected exit time of Brownian motion from f(D) provides a genuinely 2D measure of domain "thickness." The Bañuelos-Carroll (1994) framework connects exit times to conformal mapping estimates, potentially replacing radial growth with 2D probabilistic bounds.

3. **Spectral theory (Laplacian eigenvalues)** → The Faber-Krahn and Hayman inequalities relate the first Dirichlet eigenvalue to both area and inradius. While individually loose, combining spectral bounds with conformal normalization could be informative.

4. **Quasiconformal theory** → Bishop's conformal welding theorem provides constructive bounds for slit-disk domains. The quasiconformal extension of the extremal map constrains the boundary geometry.

5. **Optimal transport** → The Brenier map between D and f(D) encodes the full 2D distortion. For extremal functions, the transport plan must balance area coverage against inradius minimization.

6. **Steiner symmetrization** → Symmetrization increases inradius while preserving area, proving the extremal domain must be symmetric. This gives structural information beyond radial estimates.

### Steering Directions

1. **Area-inradius bounds** (medium priority): Use isoperimetric-type inequalities specialized to simply connected domains with given conformal radius. Expected impact: improve lower bound from 0.25 to 0.3-0.4.

2. **Symmetrization argument** (high priority): Prove n-fold symmetry of the extremal domain, narrowing the search space. Expected impact: structural constraint enabling tighter numerical optimization.

3. **Exit time / harmonic measure** (highest priority): Replace Skinner's radial approach entirely with Brownian exit time estimates. The expected exit time is a 2D quantity that captures the full domain geometry. Expected impact: potentially a new conceptual route to B_u > 0.57.

### Anomaly Results

1. **Area is NOT the binding constraint**: The extremal domain (disk minus arcs) has area close to πR² (nearly full disk), much larger than the minimum area π from the area theorem. The conformal radius normalization R(0,Ω) = 1 is the real constraint, not the area. This means isoperimetric arguments alone are insufficient.

2. **The Bloch semi-norm gap**: For the conjectured extremal, β(f*) = sup_z |f'(z)|(1-|z|²) ≈ 2.63, while B_f ≈ 0.6564. The ratio B_f/β(f) ≈ 0.25, exactly the Koebe constant. This means the Koebe bound d(w,∂Ω) ≥ R(w,Ω)/4 is nearly TIGHT for the extremal. To improve the lower bound, one must show that the Koebe 1/4 factor can be improved for domains with the specific structure of the extremal.

## Synthesis

The most promising direction is the **exit time / harmonic measure** approach because:
- It captures 2D geometry natively (no reduction to 1D)
- It connects to a well-developed probabilistic theory
- The Bañuelos-Carroll framework is specifically designed for simply connected domains
- It could provide a qualitatively new lower bound argument

However, the **anomaly results** suggest caution: the binding constraint is the conformal radius (not area), and the Koebe 1/4 factor is nearly tight for the extremal. This means any 2D approach must still work within the conformal radius framework to be effective.

The most immediately actionable direction is the **symmetrization argument**: proving that the extremal domain must be n-fold symmetric would enable restricted numerical optimization that could tighten both upper and lower bounds simultaneously.
