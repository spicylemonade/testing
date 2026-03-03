# Concept: Fixed-Step Integrator

## Role

Advances system state with constant `dt`, producing trajectory frames and invariants.

## Baseline dependency notes

- Depends on `002_newtonian_force_kernel` acceleration contract and state schema from `001_scenario_seed_contract`.
- Implemented in `src/gravity_sim/simulator.py` as `step_baseline_euler` and `simulate` loop.
- Provides stepwise outputs consumed by `scripts/collect_baseline_metrics.py` and `results/baseline/trajectories/*.json`.

## Validation checks

- Repeated fixed-seed runs must yield hash-identical canonical JSON trajectory files.
- Step/time counters must be monotonic and equal to configured `steps` and `dt`.
