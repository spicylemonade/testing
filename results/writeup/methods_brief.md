# Methods Brief

## Scope

- This item records `H1_defect_syndrome_ca_64m` as a seeded CA repair pilot on the published 64-modular order-668 frontier object, not as a new exact-search method. Evidence: `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `eliahou2025_64mod668`.
- The decisive comparison is a matched pilot against `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb` under one shared harness. Evidence: `results/verification/benchmark_report.md`.

## Matched Contract

- All order-668 runs use the same compact q/s representation and the same frontier seed file, so the comparison is representation-matched and seed-matched inside one scaffold. Evidence: `results/verification/benchmark_report.md`; `results/verification/runtime_audit.md`; `eliahou2025_64mod668`.
- The saved pilot accounting is fixed at evaluation budget `80`, requested restarts `3`, RNG seed `17`, `restart_packet_flips = 2`, and a common `exact_hit` gate. Evidence: `results/verification/benchmark_report.md`.
- The runtime audit reports complete provenance and accounting across all `15` saved runs, including seeds, configs, restart statistics, objective evaluations, wall time, canonical fingerprints, and traces. Evidence: `results/verification/runtime_audit.md`.

## Readout

- Matched controls show that H1 executes successfully on solved cases, so the branch is not being retired for a trivial coding failure. Evidence: `results/verification/verification_summary.md`; `results/verification/novelty_report.md`.
- On the canonical frontier batch, no method reaches `exact_hit = true`, and H1 does not deliver an exact improvement over the published seed. Evidence: `results/verification/verification_summary.md`; `results/verification/benchmark_report.md`; `eliahou2025_64mod668`.
- H1 fails the continuation gate because `greedy` and `simulated_annealing` preserve the seed objective while H1 lowers `l1` and `max_abs` only by increasing support above the seed support on every restart. Evidence: `results/verification/benchmark_report.md`; `results/verification/novelty_report.md`.
- The frontier runtime pattern does not rescue H1: the run uses only `32` objective evaluations but still spends `2.129s`, which the benchmark report attributes to CA field-evaluation cost rather than to a better objective outcome. Evidence: `results/verification/benchmark_report.md`; `results/verification/runtime_audit.md`.

## Claim Discipline

- The safe novelty statement is narrow: this repo completed a seeded-CA falsification step on top of the frontier object from `eliahou2025_64mod668`; it did not establish that cellular automata are new here or that H1 is a distinct CA repair method for order `668`. Evidence: `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `tsompanas2017`; `eliahou2025_64mod668`.
- The current benchmark is strong enough to eliminate an H1 continuation branch, but it is not evidence of competitiveness with broader annealing or SAT+CAS Hadamard-search work. Evidence: `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `suksmono2018`; `suksmono2019`; `bright2019`.

## Next Action

- The next action remains `pivot to H2` because the verification pack interprets the H1 failure as a locality or actuator-basis mismatch rather than as missing controls or missing accounting. Evidence: `results/verification/verification_summary.md`; `results/verification/novelty_report.md`.
- That pivot should stay narrow by satisfying the H2 family-leakage guard before spending more frontier budget. Evidence: `results/verification/verification_summary.md`.
