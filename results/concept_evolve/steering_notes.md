# Concept Evolve Steering Notes

## Three Concrete Steering Directions

### Direction 1 (PRIORITIZED): Univalent Distortion Theorem Improvement via Coefficient Analysis
- **Rationale:** The most direct path to improving the lower bound B_u > 0.5708858. Uses the de Branges theorem (|a_n| <= n for univalent f) combined with Bloch seminorm constraints to derive sharper pointwise distortion bounds. This is a classical approach that can be made rigorous with interval arithmetic.
- **Rubric items informed:** item_007, item_008, item_011, item_013, item_015, item_017, item_019
- **Why prioritized:** This direction has the highest probability of yielding a certifiably rigorous improvement. It builds directly on Skinner's method with concrete, implementable enhancements. The coefficient constraints from de Branges are strict and underutilized in the current best bound.

### Direction 2: SDP Hierarchy for Rigorous Lower Bounds via Grunsky Matrix Constraints
- **Rationale:** Modern semidefinite programming provides a systematic, convergent hierarchy of relaxations. The Grunsky inequality ||G_N||_op <= 1 is a necessary condition for univalence that can be encoded as a linear matrix inequality (LMI). This gives a principled approach to lower bounds that improve with computational budget.
- **Rubric items informed:** item_011, item_015, item_017, item_018, item_019
- **Why second:** Requires installing SDP solvers (MOSEK or SCS) and careful formulation. The convergence rate in N is unknown a priori; may need N > 20 to beat Skinner's bound.

### Direction 3: Higher-Order Symmetry Configurations for Upper Bounds
- **Rationale:** Carroll & Ortega-Cerda used 3-fold symmetric arc removal from the disk to get B_u <= 0.6564. Testing 5-fold, 7-fold, and asymmetric configurations via numerical conformal mapping could tighten this upper bound.
- **Rubric items informed:** item_009, item_012, item_016, item_020
- **Why third:** Upper bound improvement is a complementary contribution but less impactful than lower bound improvement (the gap is 0.5709 to 0.6564). Requires Schwarz-Christoffel toolbox implementation.

## Walk Path Analysis

The concept tree reveals 36 walk paths connecting 12+ concepts. Key high-value paths:
1. `interval_arithmetic_certification → sdp_relaxation_covering → bloch_constant_B_u` — Direct certification pipeline
2. `variational_arc_removal → harmonic_symmetry_optimization → polya_chebotarev_slit_domains → quadratic_differentials → bloch_constant_B_u` — Complete upper bound pipeline
3. `hyperbolic_spectral_gap → optimal_transport_conformal → variational_arc_removal → harmonic_symmetry_optimization` — Cross-domain bridge for novel techniques

## Summary
Focus on Direction 1 (coefficient-based distortion improvement) as the primary research thrust, with Direction 2 (SDP hierarchy) as backup and Direction 3 (upper bound optimization) as complementary work.
