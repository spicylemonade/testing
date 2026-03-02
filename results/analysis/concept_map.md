# Concept Map: Gravitational Simulation Design Space

**Date**: 2026-03-02  
**Item**: item_004  
**Source**: results/concept_evolve/tree/ (14 concept folders, 16 concept cards)

## Overview

The ConceptEvolve tree generated 14 materialized concept folders with 10 walk paths
representing different traversal strategies through the design space. This document
summarizes the 5 most promising concept paths for our minimal gravity simulator.

## Top 5 Concept Paths

### Path 1: The Symplectic Spine (HIGHEST PRIORITY)

**Route**: `01_newtonian_gravity -> 03_leapfrog_integration -> 04_symplectic_methods -> 07_conservation_laws`

**Justification**: This is the correctness backbone of the simulator. Starting from
Newton's gravitational law, we build the leapfrog integrator (2nd order symplectic),
compose it into Yoshida 4th-order, and validate via conservation law monitoring. Every
other path depends on this one being correct.

**Rubric items**: item_007, item_008, item_009, item_010, item_013, item_019

**Risk**: Low. All components are well-understood and analytically verifiable.

### Path 2: The Scaling Path

**Route**: `01_newtonian_gravity -> 10_force_decomposition -> 05_barnes_hut_tree -> 09_vectorized_computation`

**Justification**: This path addresses the O(N^2) scaling wall. Newton's third law
exploitation gives a free 2x speedup on brute-force. Barnes-Hut tree reduces to O(N log N).
Vectorized computation (SoA numpy arrays) maximizes single-core performance.

**Rubric items**: item_007, item_012, item_018, item_021

**Risk**: Medium. Barnes-Hut tree implementation is the most complex single component.

### Path 3: The Validation Pipeline

**Route**: `08_initial_conditions -> 02_plummer_softening -> 01_newtonian_gravity -> 03_leapfrog_integration`

**Justification**: Starting from well-characterized initial conditions (Kepler orbits,
Plummer spheres), through softened gravity, to symplectic integration. This path produces
the validation experiments: Kepler orbit closure, Plummer relaxation, energy conservation.

**Rubric items**: item_006, item_010, item_020

**Risk**: Low. Analytical solutions exist for all validation cases.

### Path 4: The Adaptive Methods Path

**Route**: `03_leapfrog_integration -> 06_adaptive_timestepping -> 14_regularization_techniques`

**Justification**: Extends the basic integrator with adaptive time-stepping for eccentric
orbits and close encounters. Regularization techniques handle the remaining singularity
cases that softening alone cannot address.

**Rubric items**: item_014

**Risk**: Medium. Adaptive time-stepping breaks strict symplecticity; careful criterion
selection needed.

### Path 5: The Cross-Domain Path

**Route**: `12_molecular_dynamics_crossover -> 06_adaptive_timestepping -> 03_leapfrog_integration`

**Justification**: Imports techniques from molecular dynamics (Verlet integration, neighbor
lists, cell lists) that are directly applicable to gravitational N-body. The Verlet method
originated in MD (Verlet, 1967) and IS the leapfrog integrator.

**Rubric items**: item_015, item_016

**Risk**: Low. Well-established cross-domain transfer.

## Concept Adjacency Graph Summary

The adjacency graph in `results/concept_evolve/tree/adjacency.json` shows:
- Most connected nodes: `01_newtonian_gravity` (4 edges), `03_leapfrog_integration` (4 edges)
- These are the central concepts bridging force computation and time integration
- Peripheral nodes: `11_gpu_acceleration`, `13_spectral_methods` — lower priority for minimal sim
- Strong cluster: nodes 01-04, 07 form the core physics/integration cluster
- Strong cluster: nodes 05, 09, 10 form the performance/scaling cluster

## Implementation Priority

Based on walk paths and rubric alignment:
1. **Core physics** (paths 1, 3): items 006-010
2. **Tree code** (path 2): item 012
3. **Higher-order methods** (path 4): items 013-014
4. **Novel optimization** (path 5): items 015-016
