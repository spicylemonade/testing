# Cross-Domain Techniques for Gravity Simulation

**Date**: 2026-03-02  
**Item**: item_005

## Overview

Three cross-domain techniques applicable to gravitational N-body simulation, identified
from concept tree exploration and literature review.

## Technique 1: Verlet Integration from Molecular Dynamics

**Source domain**: Computational chemistry / molecular dynamics  
**Concept folder**: `12_molecular_dynamics_crossover`, `03_leapfrog_integration`

The Verlet integrator (Verlet, 1967) was originally developed for simulating Lennard-Jones
fluids in molecular dynamics. It is mathematically identical to the leapfrog/Störmer-Verlet
integrator used in celestial mechanics. The key insight: both gravitational and molecular
potentials are conservative, so symplectic integration preserves the phase-space structure
in both domains.

**MD techniques transferable to gravity**:
- **Neighbor lists** (Verlet lists): Track which particles are within a cutoff radius.
  Update lists only when particles move beyond a skin distance. For gravity, this doesn't
  directly apply (gravity is long-range), but it informs the Barnes-Hut near/far
  decomposition.
- **Cell lists**: Divide space into cells, only check neighboring cells for interactions.
  This is the conceptual ancestor of the Barnes-Hut tree.
- **Multiple time-step methods** (RESPA): Different forces integrated at different time
  scales. Short-range forces at small dt, long-range at large dt. Directly applicable to
  gravity via Ahmad-Cohen (1973) neighbor scheme.

**References**: verlet1967computer, ahmad1973numerical

## Technique 2: Force-Directed Graph Layout from Network Science

**Source domain**: Information visualization / graph theory  
**Concept folder**: `13_spectral_methods`

Force-directed graph layout algorithms (Fruchterman-Reingold, ForceAtlas2) are N-body
simulations with modified force laws:
- **Repulsive force**: Coulomb-like 1/r^2 repulsion between all node pairs
- **Attractive force**: Hooke's law spring forces along edges

The Barnes-Hut tree is already used in production graph layout tools (Gephi's ForceAtlas2)
to achieve O(N log N) scaling for large networks.

**Transferable techniques**:
- **Temperature/cooling schedules**: Gradually reduce the "kinetic energy" of nodes to
  converge to a stable layout. Analogous to simulated annealing. For gravity, this maps
  to adding artificial damping for finding equilibrium configurations.
- **Gravity parameter**: ForceAtlas2 includes a "gravity" parameter that pulls disconnected
  components toward the center. This is literally Newtonian gravity added to the spring
  system.
- **Jitter control**: Small random perturbations prevent convergence to degenerate
  configurations. Analogous to stochastic perturbations in N-body for escaping symmetric
  saddle points.

**References**: barnes1986hierarchical (same algorithm used in both domains)

## Technique 3: Gradient Descent / Optimization Theory Duality

**Source domain**: Machine learning / optimization theory  
**Concept folder**: `12_molecular_dynamics_crossover`

There is a deep structural isomorphism between gravitational dynamics and gradient descent
with momentum:

| Gravity | Optimization |
|---------|-------------|
| Position x | Parameters theta |
| Velocity v | Momentum buffer |
| Acceleration a = -grad(Phi) | Gradient g = grad(L) |
| Time step dt | Learning rate lr |
| Potential Phi | Loss function L |
| Symplectic integrator | Momentum SGD |

**Transferable techniques**:
- **Learning rate warmup**: Analogous to slowly increasing dt from a cold start to
  avoid initial instabilities in N-body.
- **Gradient clipping**: Cap the maximum force magnitude. Equivalent to softening or
  acceleration limiting in N-body.
- **Adam optimizer**: Adaptive per-parameter learning rates. Analogous to per-particle
  adaptive time-stepping.
- **Nesterov momentum**: A specific composition of gradient and momentum steps that
  achieves better convergence. The Yoshida integrator can be viewed as a similar
  composition achieving higher accuracy.

**References**: yoshida1990construction (composition technique shared with optimization)

## Application to Our Simulator

| Technique | Implementation Priority | Rubric Items |
|-----------|------------------------|--------------|
| Verlet/MD neighbor lists | Low (gravity is long-range) | item_012 (conceptual) |
| Force-directed layout | Stretch (novel demo) | item_015, item_016 |
| Optimization duality | Conceptual only | item_015 |

The most directly applicable technique is the MD-to-gravity transfer of the Verlet
integrator and cell/neighbor list concepts, which inform our Barnes-Hut implementation.
