# Prior Work Comparison

This section compares current experiment outputs against prior literature from `sources.bib`, with explicit notes on metric alignment and comparability limits.

## Comparison table

| Prior work | Relevant current artifact(s) | Metric alignment | Direct comparison limits |
| --- | --- | --- | --- |
| Barnes-Hut 1986 `[@barnes1986]` | `results/research/scaling_eval.json` | Throughput gain vs approximation error (`throughput_improvement_pct`, `final_position_error_pct`) | Prior work uses classic 3D treecode studies; current setup is minimal 2D short-horizon evaluation.
| GADGET-2 2005 `[@springel2005]` | `results/research/scaling_eval.json`, `results/experiments/raw/run_manifest.jsonl` | Speed/accuracy tradeoff and scaling trend with N | GADGET-2 is TreePM + large-scale cosmological workflow, not directly matched by this fixed-step minimal simulator.
| PKDGRAV3 2017 `[@potter2017]` | `results/research/scaling_eval.json` | High-N throughput trend (`N=512,1024`) | Production massively parallel context differs from single-process local runs.
| Wisdom-Holman 1991 `[@wisdom1991]` | `results/research/symplectic_eval.json` | Energy and angular-momentum drift behavior under symplectic stepping | Long-horizon planetary mappings and splitting assumptions are not fully matched here.
| Yoshida 1990 `[@yoshida1990]` and Forest-Ruth 1990 `[@forest1990]` | `results/research/symplectic_eval.json` | Directional invariant improvement from symplectic methods | Their higher-order constructions are not implemented; only lower-order fixed-step variant evaluated.
| WHFast 2015 `[@reintamayo2015]` and REBOUND 2012 `[@rein2012]` | `results/research/symplectic_eval.json`, `results/experiments/raw/*` | Runtime/fidelity tradeoff under symplectic methods | Optimized production implementations and problem-specific tuning not replicated in this minimal code path.
| IAS15 2015 `[@reinspiegel2015]` | `results/research/symplectic_eval.json`, `results/baseline/metrics.json` | Accuracy and drift diagnostics | IAS15 is adaptive high-order; direct quantitative parity would require equal-accuracy or equal-cost normalization not present.

## Key alignment observations

- Two-body results show strong symplectic drift reduction (~99.96% median max-energy-drift improvement) at near-equal runtime, consistent with geometric integration expectations `[@wisdom1991; @yoshida1990]`.
- Three-body results improve in relative terms but remain far above target thresholds, so literature agreement is directional rather than quantitative `[@forest1990; @reintamayo2015]`.
- Barnes-Hut results reproduce expected theta-dependent speed/error tradeoff and significant throughput gains for `N>=512`, consistent with treecode literature `[@barnes1986; @springel2005; @potter2017]`.

## Where direct comparison is not possible

1. Current evaluation is short-horizon, fixed-step, and mostly 2D, while many references target long-horizon 3D astrophysical/cosmological settings.
2. Algorithm portfolios differ: FMM and mature hybrid close-encounter methods are cited but not yet implemented in this project `[@greengard1987; @duncan1998; @chambers1999; @rein2019]`.
3. Some low-N Barnes-Hut runs invoke direct-force fallback (`bh_min_n=64`), so those entries should not be compared as true tree approximations.
