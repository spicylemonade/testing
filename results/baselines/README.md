# Baseline Configurations

The non-CA baselines in this directory use the same compact q/s coordinate system as the recovered order-668 frontier seed and the shared exactness harness in `hadamard_ca.harness`.

Shared pilot settings for the initial matched smoke run:

- evaluation budget: `80`
- restart count: `3`
- RNG seed: `17`
- restart perturbation: `2` packet flips per nonzero restart
- exactness check: `scripts/run_baseline.py` -> `hadamard_ca.harness.run_harness(...)`

Smoke seed:

- `results/baselines/smoke_seed_n7_q3.json`
- Derived from the exact length-`7` control by flipping packet `q[3]`.
- Seed fingerprint: `0290b5377f3bc186b98d0b4f3f654b361339026cdf6ee4881e85678df0e32657`

Exact launch commands for the smoke batch:

```bash
python3 scripts/run_baseline.py \
  --config results/baselines/greedy.json \
  --seed-file results/baselines/smoke_seed_n7_q3.json \
  --output results/baselines/smoke_runs/greedy.json

python3 scripts/run_baseline.py \
  --config results/baselines/tabu.json \
  --seed-file results/baselines/smoke_seed_n7_q3.json \
  --output results/baselines/smoke_runs/tabu.json

python3 scripts/run_baseline.py \
  --config results/baselines/simulated_annealing.json \
  --seed-file results/baselines/smoke_seed_n7_q3.json \
  --output results/baselines/smoke_runs/simulated_annealing.json

python3 scripts/run_baseline.py \
  --config results/baselines/stochastic_hillclimb.json \
  --seed-file results/baselines/smoke_seed_n7_q3.json \
  --output results/baselines/smoke_runs/stochastic_hillclimb.json
```

Frontier launch template on the canonical order-668 seed:

```bash
python3 scripts/run_baseline.py \
  --config results/baselines/<method>.json \
  --seed-file results/frontier/order_668_64m/seed_sequences.json \
  --output results/experiments/order_668_64m/<method>.json
```
