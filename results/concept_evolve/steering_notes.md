# Concept Evolve Steering Notes

## 3 Concrete Steering Directions

### Direction 1: Slit Domain Upper Bound Campaign (PRIORITIZED)
**Description:** Construct explicit univalent functions mapping D to disk-minus-arcs domains and compute B_f to improve the trivial upper bound B_u <= 1.

**Rubric items informed:** item_010, item_020, item_023

**Rationale for priority:** This direction is prioritized because:
1. Carroll & Ortega-Cerda (2008) already demonstrated B_u <= 0.6564 using 4-fold symmetric domains, providing a concrete template to build on.
2. The computation is entirely numerical and can be verified independently.
3. Even reproducing the Carroll-Ortega-Cerda bound would be a significant contribution to our analysis.
4. The upper bound gap (0.5709 to 0.6564) is where the true value likely lies, and tightening the upper bound narrows this gap.

**First step:** Implement conformal maps from D to slit domains and compute inradii.

### Direction 2: Skinner Refinement + Coefficient Optimization for Lower Bound
**Description:** Reproduce and improve upon Skinner's B_u > 0.5708858 by identifying loose inequalities in the proof and incorporating de Branges coefficient bounds.

**Rubric items informed:** item_004, item_008, item_012, item_016, item_019

**Rationale:** Skinner's method is the state-of-the-art lower bound. Understanding exactly where slack exists is essential for any improvement. The de Branges theorem |a_n| <= n provides exact constraints that Skinner may not have fully exploited.

### Direction 3: Hyperbolic Geometry + Extremal Length Approach
**Description:** Reformulate B_u using the Poincaré metric and extremal length to derive bounds from a different mathematical framework.

**Rubric items informed:** item_014, item_018

**Rationale:** This provides an independent verification path and may reveal structural insights that the coefficient-based and function-theoretic approaches miss.

## Priority Ranking
1. **Direction 1** (Upper bound) - Highest immediate impact, most computationally tractable
2. **Direction 2** (Lower bound refinement) - Addresses the core mathematical challenge
3. **Direction 3** (Alternative framework) - Provides independent verification and new perspectives

## Connection to Concept Tree
The concept tree in `results/concept_evolve/tree/` contains 14 concept nodes organized around these three directions:
- **Upper bound cluster:** extremal_slit_domains, goodman_domain_generalization, polya_chebotarev_higher_order
- **Lower bound cluster:** skinners_method_refinement, koebe_distortion_refinement, de_branges_coefficient_bounds, bonk_distortion_extension
- **Alternative framework cluster:** schwarz_pick_hyperbolic, extremal_length_connection, covering_surface_ahlfors
- **Cross-cutting:** loewner_chain_optimization, variational_euler_lagrange, jenkins_criterion, numerical_extremal_search
