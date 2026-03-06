# epicycle_patch_streaming

## Context
Represent large ring or disk scenes as co-moving patches in Hill coordinates and only instantiate high-fidelity particles near the camera or selected body. The bridge is between planetary-ring local models and game-engine chunk streaming: physics lives in local frames while the UI still feels like one world.

## Domains
- planetary_science
- game_engine_architecture
- numerical_analysis

## Mathematical Formalization
For patch p centered at R_p, evolve local states under Hill equations: x_ddot - 2 Omega y_dot - 3 Omega^2 x = f_x, y_ddot + 2 Omega x_dot = f_y, z_ddot + Omega_z^2 z = f_z; remap bodies when ||x_local|| > L_p / 2

## Closest Prior Art
- Symplectic integrators in the shearing sheet (`c3ae70601355411b026e65f87e96d7f91be8afc5`)
- REBOUND: An open-source multi-purpose N-body code for collisional dynamics (`5240c4a18da2b6dcae3fbfa633c01bee1670d0a0`)
- Stochastic orbital migration of small bodies in Saturn's rings (`d3638068ed56d60817d059d8219958e4210afa0e`)

## Novelty
The new element is to reinterpret shearing-sheet locality as a streaming architecture, making a large interactive world feasible with minimal local physics.

## Differentiation
Research shearing-sheet codes usually study one local box at a time. This concept uses many transient local boxes as a runtime system, driven by visibility and interaction rather than by a fixed scientific domain.

## Experiment Seed
Simulate a narrow ring and an asteroid belt with a moving camera; compare memory, runtime, and trajectory continuity against a single global-coordinate implementation.

## Implementation Backlog
1. Implement a patch manager and local-to-global transforms.
2. Add a shearing-sheet or epicycle integrator per patch.
3. Aggregate far patches into moments.
4. Stream patches by camera or selected body.
5. Validate continuity as bodies cross patch boundaries.

## Planned Paths
- `results/concept_evolve/tree/005_epicycle_patch_streaming/concept.json`
- `results/concept_evolve/tree/005_epicycle_patch_streaming/README.md`
- `results/concept_evolve/tree/005_epicycle_patch_streaming/literature.json`
- `prototypes/minigrav/world/patch_manager.py`
- `prototypes/minigrav/world/shearing_patch.py`
