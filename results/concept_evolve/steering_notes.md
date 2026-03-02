# ConceptEvolve Steering Notes

**Topic**: create a minimal gravity sim  
**Date**: 2026-03-02  
**Based on**: 16 concept cards, 14 materialized concept folders, 10 walk paths

## Three Concrete Steering Directions

### SD1: Symplectic-First Architecture (PRIORITIZED)

**Description**: Build the simulation around symplectic integrators from the ground up. Use
leapfrog (Störmer-Verlet) as the minimum viable integrator, then compose it into Yoshida 4th-order
via the triple-jump technique. Energy conservation becomes architectural rather than accidental.

**Rubric items informed**: item_008, item_010, item_013, item_019

**Why prioritized**: Energy conservation is the single most important correctness signal for N-body
simulation. The concept card LEAPFROG_CORE shows that symplecticity guarantees bounded energy
oscillation rather than secular drift. The walk path `03_leapfrog_integration -> 04_symplectic_methods
-> 07_conservation_laws` directly connects the integrator choice to the validation metrics. Without
symplecticity, all experiments in Phase 4 (energy conservation, Plummer relaxation) would produce
meaningless results.

### SD2: Vectorized SoA Data Layout

**Description**: Use Structure-of-Arrays data layout with numpy arrays rather than Python object
hierarchies. All particle state stored as flat arrays: positions (N,d), velocities (N,d), masses (N).
Force computation vectorized via numpy broadcasting.

**Rubric items informed**: item_006, item_007, item_012, item_018

**Rationale**: The concept card SOA_STATE quantifies: "the entire simulation state is 5*N floats =
40KB for N=1000." Python object overhead (dict headers, pointer indirection) would inflate this by
10-100x and destroy cache coherence. For the scaling experiments (item_018, N up to 5000), vectorized
numpy is non-negotiable. The walk path `01 -> 10_force_decomposition -> 05_barnes_hut_tree ->
09_vectorized_computation` shows force computation and data layout are tightly coupled.

### SD3: Hierarchical Force Approximation Path

**Description**: Follow the concept path from brute-force O(N^2) through Newton's-third optimization
to Barnes-Hut O(N log N) tree code. This provides a natural baseline -> improvement progression
that maps directly to the rubric phases.

**Rubric items informed**: item_012, item_015, item_016, item_018, item_021

**Rationale**: The BARNES_HUT_TREE concept card predicts the crossover at N~300-500 where tree code
becomes faster than brute-force. The NEWTONS_THIRD_EXPLOIT card gives a free 2x speedup for the
brute-force baseline. Together these provide the three force methods needed for the scaling
experiment (item_018): brute-force, optimized brute-force, and Barnes-Hut.

## Priority Ranking

1. **SD1 (Symplectic-First)** — Correctness before speed. Wrong physics at any speed is useless.
2. **SD2 (Vectorized SoA)** — Performance foundation. Enables all experiments at required N scales.
3. **SD3 (Hierarchical Force)** — Scaling breakthrough. Needed for Phase 3/4 but builds on SD1+SD2.

## Concept Backlog (from walk paths)

The 10 walk paths in `walk_paths.json` suggest this implementation order:
1. Forces + integrators + conservation (paths 1, 6)
2. Initial conditions + softening (paths 4, 10)
3. Force optimization + tree code (paths 3, 5, 9)
4. Adaptive methods + regularization (paths 2, 7, 8)
