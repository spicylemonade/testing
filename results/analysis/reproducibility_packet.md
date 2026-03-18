# Reproducibility Packet

Prepared for rubric `item_024`.

## Scope

This packet covers the implemented Hadamard-`668` CA program, which consists of:

- `H1`: support-space CA on the exact `167/80` cyclic obstruction;
- `H2`: structured `q/s` defect-transport CA on the published `64`-modular seed;
- matched non-CA baselines and negative controls;
- the final stop/go decision based on deterministic JSON artifacts under `results/experiments/`.

## Module map

- Analysis of module wiring: `results/analysis/module_map.md`
- Artifact construction: `hadamard668/artifacts.py`
- Support-space search branch: `hadamard668/h1.py`
- Structured modular-search branch: `hadamard668/h2.py`
- Verifiers and objective contracts: `hadamard668/verifiers.py`
- Experiment runner: `hadamard668/experiments.py`

## Provenance-critical artifacts

- Exact cyclic target: `results/artifacts/target_167_weight_80.json`
- Solved same-template control: `results/artifacts/control_4x79.json`
- Published modular seed: `results/artifacts/seed_668_mod64.json`
- Small structured lift control: `results/artifacts/h2_control_structured_n9.json`

## Experiment matrix

- `H1` control sweep:
  - output: `results/experiments/h1_control_sweep.json`
  - methods: `parallel_gain_ca`, `direct_greedy`, `random_rule_ca`, `random_walk`
  - seeds: perturbed known solution plus random weight-matched supports
- `H1` target sweep:
  - output: `results/experiments/h1_target_sweep.json`
  - methods: same four methods
  - seeds: random supports plus deterministic projections from the modular seed
- `H2` toy ladder:
  - output: `results/experiments/h2_ladder.json`
  - methods: same four methods
  - starts: three deterministic exact-repair perturbations of the length-`9` structured control
- `H2` order-`668` attempt:
  - output: `results/experiments/h2_seed_attempt.json`
  - methods: same four methods
  - start: deterministic single-`s`-flip degradation of the published seed

## Baselines and controls

- Matched serious baseline:
  - `direct_greedy`
- Negative controls:
  - `random_rule_ca`
  - `random_walk`
- Fairness lock:
  - same representation;
  - same neighborhood;
  - same step budget;
  - same `phase_move_cap`;
  - same verifier and orbit accounting.

## Reproduction commands

```bash
python3 -m hadamard668.artifacts export
python3 -m hadamard668.experiments run-h1
python3 -m hadamard668.experiments run-h2
python3 -m hadamard668.experiments run-all
```

## Expected qualitative outcomes

- `H1`: no exact hit; `direct_greedy` beats `parallel_gain_ca` on control and target.
- `H2` ladder: weak sanity check only; random controls solve most starts.
- `H2` order-`668`: `parallel_gain_ca` ties `direct_greedy` on decisive metrics.

## Final claim allowed by the evidence

The repo supports a reproducible negative result:

- in the reported `H1/H2` runs, the implemented CA rules did not produce an order-`668` solution;
- in those same runs, they did not outperform matched non-CA baselines on the decisive tested tasks;
- under this repo's evidence gate, any justified continuation should be treated as a new branch with a materially different representation.
