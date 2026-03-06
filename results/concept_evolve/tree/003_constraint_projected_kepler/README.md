# constraint_projected_kepler

## Context
After an explicit step, apply a small position-based-dynamics-style projection that restores soft invariants such as total energy, angular momentum, and barycenter. This treats orbital drift the way graphics treats penetrations: as a correctable constraint violation rather than a failure that always demands a smaller global timestep.

## Domains
- computer_graphics
- astrophysics
- human_computer_interaction

## Mathematical Formalization
Given z' = (q', v') after one step, solve min_{Delta z} ||Delta z||^2 subject to C_H(z' + Delta z) ~= 0, C_L(z' + Delta z) ~= 0, and C_B(z' + Delta z) = sum_i m_i q_i - B0 = 0 using 1-2 Gauss-Seidel passes

## Closest Prior Art
- Position based dynamics (`9b2ba0c0508aadcf95870dd377b1544f838141cb`)
- Hierarchical Position Based Dynamics (`f9c62b65e442e353f0ab0937de3d84fa65873828`)
- Symplectic maps for the N-body problem. (`377d069236ca0108a79170e634986a0d7edffdfa`)

## Novelty
The novelty is to cast conserved-orbit structure as PBD-style constraints, making stability a controllable post-process that matches interactive teaching goals.

## Differentiation
Position based dynamics papers focus on geometric constraints for cloth, soft bodies, and contacts. This concept instead projects onto orbital invariants, so it is not a reimplementation of cloth or rigid-body PBD inside a gravity setting.

## Experiment Seed
Take a two-body ellipse and a three-body choreography with intentionally large dt; compare user-visible stability, energy drift, and correction magnitude against a smaller-dt reference.

## Implementation Backlog
1. Encode energy, angular momentum, and barycenter constraints.
2. Implement one-pass Gauss-Seidel state correction.
3. Gate the projection behind a drift threshold.
4. Visualize correction magnitude in the UI.
5. Compare against a smaller-dt reference.

## Planned Paths
- `results/concept_evolve/tree/003_constraint_projected_kepler/concept.json`
- `results/concept_evolve/tree/003_constraint_projected_kepler/README.md`
- `results/concept_evolve/tree/003_constraint_projected_kepler/literature.json`
- `prototypes/minigrav/stabilizers/invariant_projection.py`
- `prototypes/minigrav/ui/projection_overlay.py`
