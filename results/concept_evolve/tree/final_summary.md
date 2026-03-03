# Final Concept Tree Summary

**Date:** 2026-03-03  
**Rubric Item:** item_023  
**Source:** ConceptEvolve tree (12 concepts, 22 walk paths, 10 reframings)

## 1. Concept Tree Overview

The concept evolution process explored 12 concepts generated from the seed topic "create a minimal gravity sim", organized into a tree with 17 semantic bridge edges and 22 traversable paths.

## 2. All Explored Concepts

### Adopted Concepts

| Concept | Folder | Status | Why Adopted |
|---------|--------|--------|------------|
| **Barnes-Hut Spatial Hierarchy** | 001_barnes_hut_spatial_hierarchy | Adopted | Core algorithm for O(N log N) force approximation. Implemented as `src/barneshut.py`. Provides configurable theta parameter for accuracy-speed trade-off. |
| **Symplectic Leapfrog Integrator** | 002_symplectic_leapfrog_integrator | Adopted | Primary integrator for all experiments. Provides bounded energy oscillation with one force evaluation per step. Validated on solar system and collapse scenarios. |
| **Verlet Position Integration** | 008_verlet_position_integration | Adopted | Implemented as Velocity Verlet in `src/gravity_sim.py`. Near-identical performance to leapfrog, providing redundancy and comparison capability. |
| **Adaptive Timestep Control** | 009_adaptive_timestep_control | Adopted | CFL-based adaptive dt reduces force evaluations by 50% while maintaining 0.003% energy conservation. Implemented in `src/gravity_sim.py`. |
| **Energy Drift Monitor** | 012_energy_drift_monitor | Adopted | Total energy (KE + PE) tracking at every timestep. Primary metric for integrator quality. Built into all simulation runs. |

### Explored but Deferred

| Concept | Folder | Status | Why Deferred |
|---------|--------|--------|-------------|
| **Fast Multipole Expansion** | 005_fast_multipole_expansion | Deferred | O(N) asymptotic complexity superior to Barnes-Hut, but implementation complexity is much higher (multipole expansion machinery). For N <= 2000, the benefit doesn't justify the effort. |
| **GPU Compute Shader Parallelism** | 007_gpu_compute_shader_parallelism | Deferred | Would require WebGPU or CUDA implementation, fundamentally different platform from Python. The rubric targets Python with NumPy. |
| **Graph Neural Particle Dynamics** | 004_graph_neural_particle_dynamics | Deferred | GNN-based force surrogate is intellectually interesting but requires training infrastructure and data generation. Orthogonal to the classical simulation rubric. |
| **Physics-Informed Neural Gravity** | 006_physics_informed_neural_gravity | Deferred | Hamiltonian Neural Networks could provide structure-preserving learned dynamics. Requires PyTorch/JAX, training pipeline. Out of scope for "minimal" simulator. |
| **Multipole Neural Hybrid** | 010_multipole_neural_hybrid | Deferred | Combines FMM + neural residual correction. Too complex for the project scope. |

### Explored and Discarded

| Concept | Folder | Status | Why Discarded |
|---------|--------|--------|--------------|
| **Boids Emergent Flocking** | 003_boids_emergent_flocking | Discarded | Local-interaction model doesn't capture long-range 1/r^2 gravity. Interesting analog but not applicable to the N-body problem as formulated. |
| **Swarm Gravitational Cohesion** | 011_swarm_gravitational_cohesion | Discarded | Agent-based emergence of gravity is scientifically fascinating but doesn't produce quantitatively correct orbits needed for the rubric's validation experiments. |

## 3. Cross-Domain Insights

### Insight 1: Near-Field/Far-Field Decomposition Is Universal

Discovered through reframing across Barnes-Hut, FMM, t-SNE, and transformer attention domains. The O(N^2) problem of pairwise interactions appears in astrophysics (gravity), electrostatics (Coulomb), dimensionality reduction (t-SNE repulsion), and deep learning (self-attention). All domains independently discovered the same solution: split into exact near-field + approximate far-field.

**Impact on project:** This insight informed the modular design of `src/gravity_sim.py` where `force_func` is a pluggable parameter, allowing easy swapping between direct and Barnes-Hut force computation.

### Insight 2: Symplectic Structure Is the Minimal Correctness Requirement

The concept evolve path `[symplectic_leapfrog_integrator, verlet_position_integration, energy_drift_monitor]` was the highest-connectivity subgraph. The reframing to molecular dynamics (Verlet), celestial mechanics (leapfrog), and Hamiltonian mechanics (symplectic structure) all converged on the same conclusion: preserving phase-space volume is more important than high-order accuracy.

**Impact on project:** This directed the implementation priority — leapfrog was chosen as the default integrator before any experiments were run, and the experimental results (40,000x better energy conservation than Euler) validated this choice.

### Insight 3: Softening/Regularization Is Domain-Independent

Discovered through reframing across SPH (kernel smoothing), force-directed layout (cooling), social gravity (distance decay), and molecular dynamics (Lennard-Jones). Every domain that simulates pairwise attractions must handle the zero-distance singularity. The solutions are remarkably consistent: add a softening/regularization parameter.

**Impact on project:** The gravitational softening parameter epsilon was designed as a first-class parameter from the start, informed by this cross-domain insight. It serves triple duty: preventing numerical singularities, enabling stable collision detection, and providing a natural scale for adaptive timestepping.

## 4. Walk Paths Analysis

The 22 walk paths in the concept tree fall into three clusters:

1. **Classical simulation path** (7 paths): Barnes-Hut → Verlet → Energy Monitor. This is the backbone path that was fully implemented.

2. **Neural/learned path** (10 paths): Various combinations of GNN, physics-informed neural, and multipole-neural hybrid concepts. These were all deferred as out of scope.

3. **Adaptive optimization path** (5 paths): Adaptive timestep → Energy Monitor, and symplectic → adaptive → energy. These informed the adaptive timestep implementation.

## 5. Steering Directions Outcome

The three steering directions from the initial concept evolve:

1. **Symplectic Integrator Zoo** — FULLY REALIZED. All three integrators implemented and compared.
2. **Barnes-Hut Spatial Hierarchy** — REALIZED with caveat. Algorithm correct, but pure-Python overhead prevents speed advantage at target N.
3. **Adaptive Timestep Control** — FULLY REALIZED. 50% force evaluation savings demonstrated.

The prioritization of Direction 1 (integrator zoo) proved correct — it was the foundation that all downstream experiments depended on.
