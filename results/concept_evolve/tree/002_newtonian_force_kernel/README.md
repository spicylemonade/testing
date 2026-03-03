# Concept: Newtonian Force Kernel

## Role

Implements deterministic O(N^2) pairwise accelerations under softened Newtonian gravity.

## Baseline dependency notes

- Depends on force-law and softening contract from `results/baseline/design_spec.md`.
- Implemented in `src/gravity_sim/simulator.py` (`accelerations`), consumed by baseline and symplectic stepping.
- Feeds diagnostics in `results/baseline/metrics.json` through downstream integration outputs.

## Validation checks

- Pairwise updates must preserve action-reaction symmetry in deterministic loop order.
- Softening parameter must prevent singular acceleration blowups in near-collision states.
