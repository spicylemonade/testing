# Hybrid Proposal: Symplectic + Barnes-Hut

## Walk-path evidence

The proposal is grounded in concept-tree walk paths of length >=3, including:

`scenario_seed_contract -> newtonian_force_kernel -> fixed_step_integrator -> diagnostics_metrics_contract -> cli_manifest_reproducibility`

This path appears in `results/concept_evolve/tree/walk_paths.json` and `results/concept_evolve/walk_session.json`.

## Probe evidence

A focused probe on the hybrid method was run and summarized in `results/concept_evolve/probe_result.json`. Key takeaway: combine Barnes-Hut throughput gains with symplectic stepping, but control approximation error through theta/dt coupling.

## Hybrid method definition

Method ID: `symplectic_bh`

- Integrator: symplectic kick-drift-kick style update (fixed step).
- Force model: Barnes-Hut approximation (`theta`, `leaf_size`, `bh_min_n`) with softened Newtonian force law.
- Intended regime: medium/high N where direct O(N^2) becomes bottleneck.

## Concrete experiment seed and dependencies

Experiment seed: `42`

Proposed run:

`python3 -m gravity_sim.cli run --method barnes_hut --scenario random --n 512 --steps 300 --dt 0.0008 --seed 42 --softening 0.001 --theta 0.8 --leaf-size 8 --bh-min-n 64 --out results/research/hybrid_seed42_n512.json`

Dependencies:

1. `src/gravity_sim/scenarios.py` (deterministic state generation contract)
2. `src/gravity_sim/barnes_hut.py` (scalable force approximation)
3. `src/gravity_sim/simulator.py` (symplectic and baseline stepping contracts)
4. `scripts/collect_symplectic_eval.py` (stability metric definitions)
5. `scripts/collect_scaling_eval.py` (speed/error tradeoff measurement)

## Expected signal

- Throughput keeps a large fraction of Barnes-Hut gain at N>=512.
- Energy drift improves relative to Euler-based high-N runs under matched seed/config.
- Error-vs-speed point at `theta=0.8` lies near the Pareto frontier.
