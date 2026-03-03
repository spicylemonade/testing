# Limitations, Validity Threats, and Mitigation Roadmap

This document synthesizes the current gravity-sim limitations from phase-2/3/4 artifacts and maps each mitigation to explicit dependency chains and future work items.

## Limitation register with mitigation mapping

| ID | Current limitation (evidence) | Mitigation proposal | Dependency chain | Future work item(s) |
| --- | --- | --- | --- | --- |
| L1 | Absolute stability remains poor in challenging regimes: three-body max energy drift is still `5.106e5%` for symplectic and `1.764e6%` for baseline; random-N drift remains in the thousands (`results/experiments/statistics.md`). | Add close-encounter handling and adaptive or hybrid timestep controls, then retune `dt`/softening by scenario with absolute-threshold gates. | `src/gravity_sim/simulator.py` -> `scripts/run_experiment_matrix.py` -> `scripts/analyze_experiment_statistics.py` | `FW-01`, `FW-02`, `FW-05` |
| L2 | Runtime target is unmet by a wide margin: baseline N=256 runtime is `287.923911 ms/step` vs `<=1.0 ms/step` target (`results/experiments/statistics.md`, `results/baseline/metrics.json`). | Separate algorithmic and implementation bottlenecks; optimize force kernel path (vectorization/JIT), and add strict performance gates at fixed N/horizon. | `src/gravity_sim/simulator.py` + `src/gravity_sim/barnes_hut.py` -> dedicated benchmark script -> `results/experiments/statistics.json` | `FW-03`, `FW-10` |
| L3 | Force and integrator effects are confounded for scalable runs because `barnes_hut` currently uses Euler stepping (`src/gravity_sim/simulator.py`, `results/research/subagent_phase3/failure_case_exploration.md`). | Implement `symplectic_bh` and run 2x2 ablations (direct vs BH force crossed with Euler vs symplectic integrator) under identical seeds/configs. | `src/gravity_sim/simulator.py` + `src/gravity_sim/barnes_hut.py` -> `scripts/collect_scaling_eval.py` + `scripts/collect_symplectic_eval.py` | `FW-02` |
| L4 | Modeling scope is limited to 2D states and scalar angular momentum (`src/gravity_sim/scenarios.py`, `src/gravity_sim/simulator.py`), reducing physical realism and comparability to 3D prior work (`results/experiments/prior_work_comparison.md`). | Generalize state, forces, and diagnostics to 3D; preserve deterministic contracts and regenerate baseline/scaling references. | `src/gravity_sim/scenarios.py` -> `src/gravity_sim/simulator.py` -> `src/gravity_sim/barnes_hut.py` -> metrics scripts | `FW-04` |
| L5 | High-N experiments are short-horizon (`steps` as low as 4-20 at N>=512 in `results/experiments/protocol.md`), so secular error behavior is under-observed. | Add long-horizon stress matrix with horizon-normalized comparisons and checkpointed runs for feasible wall-clock cost. | `results/experiments/protocol.md` -> `scripts/run_experiment_matrix.py` -> `results/experiments/raw/*` | `FW-05` |
| L6 | Scenario diversity is narrow (analytic two-body, one deterministic three-body setup, one random generator family), limiting robustness claims across mass ratios and encounter regimes. | Expand scenario library: unequal-mass binaries, resonant triples, clustered random initial conditions, and near-collision stress fixtures. | `src/gravity_sim/scenarios.py` -> protocol/matrix scripts -> statistics pipeline | `FW-06`, `FW-09` |
| L7 | Metric definitions still differ across scripts: baseline metrics use final-frame drift and mean step time, while experiment matrix uses max-over-time drift and runtime-per-step medians (`scripts/collect_baseline_metrics.py`, `scripts/run_experiment_matrix.py`). | Move to one shared metrics module and emit metric-definition schema/version in every artifact and manifest row. | new `src/gravity_sim/metrics.py` -> `scripts/collect_baseline_metrics.py` + `scripts/collect_symplectic_eval.py` + `scripts/run_experiment_matrix.py` + `scripts/analyze_experiment_statistics.py` | `FW-07` |
| L8 | Reproducibility is strong but not fully portable: manifest replay command is only partially executable in a fresh shell and command/artifact schema are not perfectly aligned (`results/experiments/subagent_audit.md`). | Emit executable replay commands with explicit environment bootstrap (`PYTHONPATH=src` or packaged entrypoint), add `schema_version`, and normalize full commit hashes across artifacts. | `scripts/run_experiment_matrix.py` + `src/gravity_sim/cli.py` + `results/final/reproducibility.md` | `FW-08` |
| L9 | Seeded replication is uneven across scenarios: two-body and current three-body constructors ignore seed variation (`src/gravity_sim/scenarios.py`), which weakens uncertainty estimation. | Introduce controlled perturbation ensembles (phase/randomized initial offsets with fixed distributions) and report effective sample size per scenario. | `src/gravity_sim/scenarios.py` -> `results/experiments/protocol.md` -> `scripts/analyze_experiment_statistics.py` | `FW-09` |
| L10 | Performance measurements remain sensitive to instrumentation choices (snapshot cadence, in-process memory measurement) and host-level variance (`results/baseline/subagent_gap_report.md`, `results/experiments/subagent_audit.md`). | Add isolated micro/macro benchmark harnesses with fixed snapshot policy, subprocess-level peak RSS, and repeated host-normalized timing runs. | new benchmark harness script(s) -> `scripts/analyze_experiment_statistics.py` -> `results/experiments/statistics.md` | `FW-03`, `FW-10` |

## Threats to validity and mitigations

| Threat ID | Threat to validity | Why this threatens claims | Mitigation and dependency mapping | Future work item(s) |
| --- | --- | --- | --- | --- |
| TV1 | Construct validity risk from metric-contract drift across pipelines. | Same label (for example "energy drift") can represent different computations, invalidating cross-phase comparisons. | Standardize formulas in shared metrics package, include schema version in every result, and fail CI on definition drift. Depends on metrics refactor across all collection scripts. | `FW-07` |
| TV2 | Internal validity risk from method confounding (integrator vs force approximation; direct fallback around `bh_min_n`). | Observed gains/losses may be wrongly attributed to one component when multiple factors changed simultaneously. | Run factorial ablations and discontinuity tests around `bh_min_n`, then publish component-isolated effect sizes. Depends on simulator method expansion and matrix script updates. | `FW-02`, `FW-05` |
| TV3 | External validity risk from narrow domain coverage (2D, short horizon, small scenario family, single-host runs). | Results may not transfer to realistic long-horizon 3D astrophysical workloads. | Extend to 3D and broader scenario suites, increase horizon length, and rerun on multiple hardware profiles with normalized benchmark reporting. | `FW-04`, `FW-05`, `FW-06`, `FW-10` |
| TV4 | Statistical conclusion validity risk from low effective stochastic variation in deterministic scenarios. | Confidence intervals can appear tight while not reflecting real uncertainty under perturbed initial conditions. | Add controlled perturbation ensembles and power-analysis checks; report per-scenario effective sample size and robustness intervals. | `FW-09` |

## Future dependency/work-item backlog

| Work item | Objective | Key dependencies | Expected deliverables |
| --- | --- | --- | --- |
| FW-01 | Adaptive stability controls for close encounters | `src/gravity_sim/simulator.py`, `results/research/subagent_phase3/ablation_plan.md` | stability sweep artifact for adaptive/hybrid timestep policies |
| FW-02 | Hybrid `symplectic_bh` + deconfounded ablations | `src/gravity_sim/simulator.py`, `src/gravity_sim/barnes_hut.py`, phase-3 ablation protocol | hybrid method implementation + 2x2 ablation report |
| FW-03 | Runtime-target engineering for baseline/high-N paths | force kernels + benchmark harness + threshold gates | optimized runtime artifact with pass/fail evidence |
| FW-04 | 3D model generalization | scenarios, simulator, Barnes-Hut, diagnostics stack | 3D trajectories and invariant metrics |
| FW-05 | Long-horizon matrix extension | experiment protocol/matrix/statistics scripts | long-horizon experiment batch + drift-over-time summaries |
| FW-06 | Scenario-library expansion | `src/gravity_sim/scenarios.py`, protocol, matrix scripts | new benchmark scenarios and scenario-specific robustness report |
| FW-07 | Unified metrics contract + schema versioning | shared metrics module + all collection/analysis scripts | single metric API + schema-pinned outputs |
| FW-08 | Reproducibility portability hardening | matrix manifest emitter, CLI entrypoint, reproducibility guide | portable replay tooling and normalized provenance schema |
| FW-09 | Statistical power and perturbation ensembles | scenario generators, protocol seeds, stats analysis | effective-sample-size reporting + robust CIs |
| FW-10 | Measurement isolation and hardware-normalized benchmarks | dedicated benchmark scripts + statistics integration | reproducible benchmark suite with noise controls |

## Recommended execution order

1. `FW-07` then `FW-08` to lock measurement and provenance contracts before additional large batches.
2. `FW-02` and `FW-01` to separate method effects and improve stability in hard regimes.
3. `FW-05` and `FW-09` to strengthen horizon coverage and statistical confidence.
4. `FW-03` and `FW-10` to close runtime gaps with credible performance methodology.
5. `FW-04` and `FW-06` to increase external validity and literature comparability.

These work items should be imported into the phase-5 dependency roadmap artifact (`item_024`) as prerequisite-linked experiments, then cross-checked during final closeout synthesis (`item_025`).
