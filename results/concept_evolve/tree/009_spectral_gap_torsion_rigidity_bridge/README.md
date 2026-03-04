# 009: Spectral Gap and Torsion Rigidity Bridge

## Topic Context

The first Dirichlet eigenvalue lambda_1 and torsion rigidity P of a simply connected domain encode its spectral properties. Both are bounded in terms of the inradius R_D, creating a bridge to the Bloch constant.

The Faber-Krahn inequality says the disk minimizes lambda_1 for given area. The inradius version (lambda_1 >= pi^2/(4R^2)) links to the Bloch constant because B_u involves the inradius of the conformal image.

Van den Berg and Bucur (2025) recently studied the torsion function for simply connected domains, establishing new relationships between the L^p norm of the torsion function and spectral data.

## Implementation Backlog

1. [ ] Set up FEniCS/FreeFEM for eigenvalue computation
2. [ ] Compute lambda_1 for strip, disk, slit domains (inradius 1)
3. [ ] Compute torsion function and its integral (torsion rigidity)
4. [ ] Plot lambda_1 * R^2 vs Bloch radius for various domains
5. [ ] Identify domains near the spectral-Bloch boundary
6. [ ] Test whether spectral extremality implies Bloch extremality
7. [ ] Use shape derivatives of lambda_1 for domain optimization
