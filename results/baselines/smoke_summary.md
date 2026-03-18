# Baseline Smoke Summary

All four non-CA baselines were run from the same non-exact q/s seed `results/baselines/smoke_seed_n7_q3.json` under the same shared accounting:

- evaluation budget: `80`
- restart count: `3`
- RNG seed: `17`
- restart perturbation: `2` packet flips per nonzero restart
- exactness interface: `scripts/run_baseline.py` -> `hadamard_ca.harness.run_harness(...)`

The smoke seed starts at:

- order: `28`
- seed fingerprint: `0290b5377f3bc186b98d0b4f3f654b361339026cdf6ee4881e85678df0e32657`
- defect summary: support `3`, `l1 = 12`, `max_abs = 4`

Observed outcomes:

- `greedy`: exact hit, `74` evaluations, canonical fingerprint `37e654cc9d22ebd353e25e1d1bf2021a6e6d0f83c215491991baf0f718941bcf`
- `tabu`: exact hit, `74` evaluations, canonical fingerprint `37e654cc9d22ebd353e25e1d1bf2021a6e6d0f83c215491991baf0f718941bcf`
- `simulated_annealing`: exact hit, `80` evaluations, canonical fingerprint `a321beaca53a49bb00cdd852a8f7e3a276107ef59cc7bf22ebe8dea6ba9f326b`
- `stochastic_hillclimb`: exact hit, `27` evaluations, canonical fingerprint `37e654cc9d22ebd353e25e1d1bf2021a6e6d0f83c215491991baf0f718941bcf`

Interpretation:

- The four baselines now share one concrete representation, one harness, one seed file format, and one exactness definition.
- The smoke batch is only a representation/control check, not a frontier result.
- Simulated annealing reaches exactness through a different canonical q/s fingerprint than the exhaustively recovered control, which confirms that the harness accepts exactness independently of matching a single reference fingerprint.
