# 008: Hyperbolic Metric Density Bounds

## Topic Context

The hyperbolic (Poincare) metric on a simply connected domain Omega characterizes its conformal geometry. The density sigma_Omega(z) satisfies the Liouville equation and is connected to the Bloch constant via the Schwarz-Pick lemma.

Eremenko studied the hyperbolic metric of lattice complements, showing that it relates to the Lame equation's accessory parameters. This deep connection between the Bloch/Landau constants and elliptic PDE theory provides a differential-equations approach to bound improvements.

## Key Relationships

- sigma_Omega >= 1/(2*R_Omega) where R_Omega is the inradius
- B_f relates to the product of |f'| and 1/sigma on the image
- For lattice complements, sigma is determined by elliptic functions

## Implementation Backlog

1. [ ] Implement numerical solver for Liouville equation on general domains
2. [ ] Compute hyperbolic metric for disk-minus-slits domains
3. [ ] Compare with exact formulas for lattice complements
4. [ ] Find inf sigma_Omega for each candidate domain
5. [ ] Extract Bloch constant bounds from metric data
6. [ ] Visualize metric density as heat maps
7. [ ] Investigate relationship to Lame equation accessory parameters
