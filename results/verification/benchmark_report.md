# Benchmark Report

## Scope

This report evaluates the benchmark contract actually exercised by the saved experiment batches.

Experiment IDs reviewed:

- `control_n5_q0:H1_defect_syndrome_ca_64m`
- `control_n5_q0:greedy`
- `control_n7_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:tabu`
- `control_n7_q0:simulated_annealing`
- `order_668_64m:H1_defect_syndrome_ca_64m`
- `order_668_64m:greedy`
- `order_668_64m:tabu`
- `order_668_64m:simulated_annealing`
- `order_668_64m:stochastic_hillclimb`

Paper keys used for benchmark framing:

- `eliahou2025_64mod668`
- `tsompanas2017`
- `suksmono2018`
- `suksmono2019`
- `bright2019`

## Benchmark Contract

- Shared q/s representation: all methods operate in the same compact q/s coordinates anchored to the frontier seed from `eliahou2025_64mod668`.
- Shared frontier seed: every order-668 run reads `results/frontier/order_668_64m/seed_sequences.json`.
- Shared pilot accounting:
  - evaluation budget `80`
  - requested restart count `3`
  - RNG seed `17`
  - restart diversification `restart_packet_flips = 2`
- Shared exactness gate: `exact_hit` from the common harness, not a soft residual proxy.

## Control-Batch Readout

- `control_n5_q0:H1_defect_syndrome_ca_64m`, `control_n5_q0:greedy`, and `control_n7_q0:H1_defect_syndrome_ca_64m` confirm that the H1 branch and the non-CA baselines run through the same harness successfully.
- `control_n7_q0:tabu` also reaches exactness under the shared contract.
- `control_n7_q0:simulated_annealing` fails on the harder control, which is acceptable as a benchmark observation and not a fairness defect because the accounting cap remains matched.

## Frontier-Batch Readout

- `order_668_64m:H1_defect_syndrome_ca_64m`, `order_668_64m:greedy`, `order_668_64m:tabu`, `order_668_64m:simulated_annealing`, and `order_668_64m:stochastic_hillclimb` all finish with `exact_hit = false`.
- `order_668_64m:H1_defect_syndrome_ca_64m` uses only `32` objective evaluations but spends `2.129s`, reflecting the cost of CA field evaluation rather than a better objective outcome.
- `order_668_64m:greedy` and `order_668_64m:simulated_annealing` preserve the seed objective, while H1 lowers `l1` and `max_abs` only by increasing support above the seed support on every restart.

## Interpretation Against Literature

- Relative to `tsompanas2017`, the current benchmark is strong enough to test whether a CA-shaped rule brings anything beyond local-heuristic behavior inside one matched representation. The answer in this batch is no.
- Relative to `suksmono2018` and `suksmono2019`, this repo does not claim to reproduce annealing or quantum-annealing scale. The benchmark is a seed-matched falsification scaffold, not a literature-level performance comparison.
- Relative to `bright2019`, the current setup is much weaker on certification and search breadth. It is a practical branch gate, not a replacement for certificate-rich exact combinatorial search.

## Verdict

- The benchmark scaffold is fair enough for branch elimination.
- It is not evidence that any method here is competitive with the broader Hadamard-search literature.
- For the current question, the decisive result is simple: under one matched pilot contract, H1 does not earn continuation beyond the first frontier kill test.
