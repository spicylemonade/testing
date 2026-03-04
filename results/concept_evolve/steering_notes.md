# ConceptEvolve Steering Notes

## 3 Concrete Steering Directions

### Direction 1: SDP/Convex Relaxation via Grunsky Matrix Constraints (PRIORITIZED)
- **Description**: Formulate the univalent Bloch constant problem as a semidefinite program by expressing univalence through the Grunsky matrix inequality ||G_f|| <= 1. Truncating to N Taylor coefficients gives a finite-dimensional SDP. As N increases, the SDP lower bound should converge monotonically to B_u from below.
- **Rubric items informed**: item_008 (toolkit), item_009 (reproduce Skinner), item_013 (improved lower bound), item_017 (interval proof)
- **Why prioritized**: This is the most likely to produce a _rigorous, verifiable_ lower bound improvement. SDPs can be solved with certified solvers (e.g., SDPA-GMP for exact arithmetic). The approach is systematic: increase N until the bound stabilizes beyond 0.5708858. Unlike domain optimization (which gives upper bounds), this targets the lower bound directly and can be made fully rigorous via interval arithmetic.

### Direction 2: Polya-Chebotarev Extension with Asymmetric Point Configurations
- **Description**: Carroll-Ortega-Cerda's upper bound B_u <= 0.6564 used Fedorov's solution for 4 symmetric points. Solving the Polya-Chebotarev problem for 5+ points with optimized (possibly asymmetric) placements could yield tighter upper bounds.
- **Rubric items informed**: item_005 (upper bound analysis), item_010 (domain families), item_015 (tighter upper bound), item_020 (optimization)
- **Why this direction**: Directly targets upper bound improvement. The Carroll-Ortega-Cerda bound used a restricted configuration space. Expanding to more points or breaking symmetry is a natural generalization that has not been explored.

### Direction 3: Verified Computation Pipeline (Interval Arithmetic + SC Maps)
- **Description**: Build a rigorous computation pipeline using interval arithmetic to certify Bloch constant bounds for specific domains. This enables computer-assisted proofs.
- **Rubric items informed**: item_008 (toolkit), item_011 (metrics), item_013 (lower bound), item_017 (interval proof), item_021 (validation)
- **Why this direction**: Complements Directions 1 and 2 by providing mathematical certainty. Any numerical improvement needs rigorous verification to be publishable.

## Priority Ranking

**Direction 1 (SDP/Grunsky) is the top priority** because:
1. It directly targets the harder problem (lower bound improvement)
2. It is algorithmically clean: truncate Grunsky matrix to N×N, solve SDP
3. It can produce rigorous bounds via exact rational SDP solvers
4. The Grunsky inequality is a necessary and sufficient condition for univalence (for N→∞)
5. No prior work has applied SDP methods to the univalent Bloch constant

Direction 2 is second priority as it provides the complementary upper bound attack.
Direction 3 is the verification backbone for all results.

## Concept Tree Paths to Monitor
- `schwarz_christoffel_interval_arithmetic → harmonic_symmetry_extremal_slits → polya_chebotarev_capacity_optimization`
- `variational_schlicht_function_perturbation → quasiconformal_deformation_sensitivity → hexagonal_lattice_local_minimality`
- `spectral_gap_torsion_rigidity_bridge → brownian_lifetime_inradius_duality → hyperbolic_metric_density_bounds`
