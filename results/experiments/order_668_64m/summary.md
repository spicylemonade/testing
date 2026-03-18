# Order-668 Frontier Batch Summary

Matched first-kill batch on the canonical `64`-modular frontier seed with shared evaluation budget `80`, restart count `3`, RNG seed `17`, and `restart_packet_flips = 2`.

Seed objective: support `13`, `l1 = 2880`, `max_abs = 512`.

Method-level readout:

- `H1_defect_syndrome_ca_64m`: exact_hit `False`, best `13/2880/512`, median terminal `33/2356/384`, seed improvement `False`, evaluations `32`, restarts `3/3`
- `greedy`: exact_hit `False`, best `13/2880/512`, median terminal `13/2880/512`, seed improvement `False`, evaluations `80`, restarts `1/3`
- `tabu`: exact_hit `False`, best `13/2880/512`, median terminal `25/3036/520`, seed improvement `False`, evaluations `80`, restarts `1/3`
- `simulated_annealing`: exact_hit `False`, best `13/2880/512`, median terminal `13/2880/512`, seed improvement `False`, evaluations `80`, restarts `1/3`
- `stochastic_hillclimb`: exact_hit `False`, best `13/2880/512`, median terminal `33/2992/496`, seed improvement `False`, evaluations `26`, restarts `3/3`

Interpretation:

- `H1_defect_syndrome_ca_64m` never improved the lexicographic objective. Its best state remained the published seed, and all three restart terminals diffused support above `13` active lags even while `l1` and `max_abs` dropped.
- `greedy` and `simulated_annealing` stayed pinned to the seed objective throughout the matched budget.
- `tabu` and `stochastic_hillclimb` explored worse support profiles and also failed to improve on the seed objective.

Decision:

- Stop broad H1 sweeps after this first frontier kill test. The branch does not satisfy the continue gate in `results/verification/benchmark_gate.md`: no exact hit, no best-objective gain over the seed, and no strict terminal support-plus-magnitude advantage over matched non-CA baselines.
- Keep `H2_lag_space_ca_167` gated until the runtime audit and verification pack summarize this locality-failure evidence cleanly.
