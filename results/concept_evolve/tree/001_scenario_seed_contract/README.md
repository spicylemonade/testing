# Concept: Scenario Seed Contract

## Role

Defines deterministic scenario generation and state schema boundaries used by all baseline and advanced methods.

## Baseline dependency notes

- Depends on `results/baseline/design_spec.md` for canonical state schema (`positions`, `velocities`, `masses`) and seed policy.
- Depends on `src/gravity_sim/scenarios.py` for two-body/three-body/random scenario constructors.
- Provides deterministic inputs to `src/gravity_sim/simulator.py` and `src/gravity_sim/cli.py`.

## Validation checks

- Seed `42` must regenerate identical initial states across repeated runs.
- Center-of-mass initialization should remain near origin to simplify drift diagnostics.
