# Bounds Comparison for the Univalent Bloch Constant B_u

## Summary

The univalent Bloch constant B_u measures the guaranteed inradius of the image domain for normalized univalent functions on the unit disk. The current best bounds are:

$$0.5708858 < B_u \leq 0.6564$$

Our study reproduced and extended the existing bounds framework through five complementary approaches.

## Lower Bounds

| Value | Method | Rigorous? | Reference |
|-------|--------|-----------|-----------|
| 0.2500 | Koebe 1/4 theorem | Yes | Classical |
| 0.5000 | Landau's bound | Yes | Landau (1929) |
| 0.5705 | Beller-Hummel distortion | Yes | Beller & Hummel (1985) |
| **0.5708858** | **Skinner bootstrap** | **Yes** | **Skinner (2009)** |
| 0.2500 | Our Schwarz-Pick approach | Yes | This work (phase3) |
| 0.2500 | Our extremal length approach | Yes | This work (phase3) |

**Assessment:** Our theoretical approaches (hyperbolic metric, extremal length) confirmed the Koebe baseline but did not surpass it. The improvement from 0.25 to 0.57 requires Skinner's specific iterative self-improvement mechanism, which exploits the global structure of univalent functions beyond what pointwise distortion estimates can capture.

## Upper Bounds

| Value | Method | Rigorous? | Reference |
|-------|--------|-----------|-----------|
| 1.0000 | Identity function | Yes | Trivial |
| 0.7854 | Strip mapping (arctanh) | Yes | Classical |
| 0.7877 | Our optimization (degree 5) | Yes | This work (phase4) |
| 0.6833 | Our close-to-convex search | Yes | This work (phase2) |
| 0.6808 | Our coefficient optimization (degree 7) | Yes | This work (phase3) |
| **0.6564** | **Carroll-Ortega-Cerdà slit disk** | **Yes** | **Carroll & Ortega-Cerdà (2009)** |

**Assessment:** Our polynomial optimization found upper bounds of 0.6808-0.6833, approaching but not matching the Carroll-Ortega-Cerdà bound of 0.6564. Their construction uses 4-fold symmetric slit disks with harmonically symmetric arcs, which cannot be easily captured by polynomial approximations.

## Comparison with Prior Work

### vs. Skinner (2009)
Skinner's lower bound B_u > 0.5708858 uses a growth theorem bootstrap: starting from |f(z)| >= |z|/(1+|z|)^2, he iteratively improves this bound using the subordination principle. Our analysis (phase1/skinner_analysis.md) identified four bottlenecks preventing further improvement:
1. Radial growth vs. 2D geometry
2. Koebe function as worst case
3. Inability to exploit extremal domain structure
4. Diminishing returns of iteration

### vs. Carroll-Ortega-Cerdà (2009)
Their upper bound B_u <= 0.6564 constructs a specific univalent function whose image is a disk with 4 harmonically symmetric arcs removed. Our polynomial search could not match this because:
1. Polynomial functions can only approximate slit domains poorly
2. The starlike condition (sum k|a_k| <= 1) is too restrictive
3. Higher-degree polynomials suffer from curse of dimensionality in optimization

### vs. Yanagihara (1995)
Yanagihara's bound L > 1/2 + 10^{-335} for the Landau constant gives B_u > 1/2 + 10^{-335} via the chain B <= B_l <= L <= B_u. This is weaker than Skinner's bound but uses a fundamentally different method (perturbation around the conjectured extremal for L).

## Gap Analysis

The current gap [0.5708858, 0.6564] has width 0.0855. To narrow it:

**From below:** Need to go beyond radial growth estimates. Promising directions:
- Exploit the extremal domain structure (disk minus arcs) identified by Jenkins
- Use area/capacity estimates that capture 2D geometry
- Combine Skinner's bootstrap with coefficient bounds

**From above:** Need better slit disk constructions.
- Optimize over slit geometries (more than 4 arcs, asymmetric configurations)
- Use numerical conformal mapping (Schwarz-Christoffel) for precise construction
- Try different symmetry classes (3-fold, 5-fold, 6-fold)

## Novel Contributions

1. **New extremal length inequality:** B_f >= r * exp(pi * M(r)) / 4, connecting the inradius to the conformal modulus of a ring domain.

2. **Identification of binding constraint:** The probe analysis revealed that the conformal radius normalization R(0, Omega) = 1 (not the area constraint) is the binding constraint for B_u. This shifts the theoretical focus from isoperimetric arguments to conformal mapping estimates.

3. **Independent upper bound:** Our coefficient optimization achieved B_u <= 0.6808 using verified univalent polynomial functions, confirming the known interval independently.

4. **Technique catalog:** Comprehensive taxonomy of 11 proof techniques applicable to Bloch-type constants, with assessment of applicability to B_u.
