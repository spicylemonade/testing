# Final Findings

## Claim 1: Symplectic integration dramatically improves two-body fidelity at near-equal runtime.

- **Quantitative artifact:** `results/research/symplectic_eval.json` shows median max-energy-drift reduction from `1.8696%` (baseline) to `0.000800%` (symplectic), with runtime ratio `0.991`.
- **Figure:** `figures/final/claim_01_two_body_drift_runtime.png`
- **Citation support:** `[@wisdom1991; @yoshida1990]`

## Claim 2: In chaotic three-body dynamics, symplectic stepping improves relative drift but remains absolutely unstable.

- **Quantitative artifact:** `results/research/symplectic_eval.json` reports `71.05%` median drift reduction (`1.764e6%` -> `5.106e5%`), while `results/experiments/statistics.md` confirms runtime near parity.
- **Figure:** `figures/final/claim_02_three_body_energy_runtime.png`
- **Citation support:** `[@forest1990; @reintamayo2015]`

## Claim 3: Barnes-Hut meets high-N scalability goals with strong speedups and controllable error.

- **Quantitative artifact:** `results/research/scaling_eval.json` shows best throughput improvements of `+637.8%` (`7.38x`) at `N=512` and `+479.9%` (`5.80x`) at `N=1024`, with low-error configurations (`0.034%` and `0.0049%` final-position error).
- **Figure:** `figures/final/claim_03_barnes_hut_speed_error_tradeoff.png`
- **Citation support:** `[@barnes1986; @springel2005; @potter2017]`

## Claim 4: Baseline robustness is highly sensitive to dt and softening, and runtime threshold remains unmet.

- **Quantitative artifact:** `results/experiments/statistics.md` sensitivity tables show median random-N64 drift rising from `3197%` to `8826%` as dt increases (`5e-4` -> `2e-3`) and decreasing from `13708%` to `1223%` as softening increases (`5e-4` -> `2e-3`). `results/baseline/metrics.json` shows baseline N=256 runtime `287.9 ms/step` vs `1.0 ms/step` target.
- **Figure:** `figures/final/claim_04_sensitivity_and_runtime_gap.png`
- **Citation support:** `[@duncan1998; @chambers1999; @rein2019]`
