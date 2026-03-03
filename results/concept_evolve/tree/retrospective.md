# Concept-Tree Retrospective and Future Roadmap

## Referenced concept folders

1. `results/concept_evolve/tree/001_scenario_seed_contract`
2. `results/concept_evolve/tree/002_newtonian_force_kernel`
3. `results/concept_evolve/tree/003_fixed_step_integrator`
4. `results/concept_evolve/tree/004_diagnostics_metrics_contract`
5. `results/concept_evolve/tree/005_cli_manifest_reproducibility`

These five concepts remain the main dependency spine and are exercised by current walk paths:

`scenario_seed_contract -> newtonian_force_kernel -> fixed_step_integrator -> diagnostics_metrics_contract -> cli_manifest_reproducibility`

## Retrospective notes

- Strength: deterministic scenario generation and artifact emission are strong enough for reproducibility audits.
- Strength: concept ordering correctly predicted implementation sequence (baseline -> stability -> scalability).
- Gap: no explicit node currently represents a standalone Barnes-Hut force contract and hybrid integrator coupling.
- Gap: diagnostics concept still needs unified metric-schema enforcement across all scripts.

## Top 10 follow-up experiments (prioritized)

| Priority | Experiment | Prerequisites | Expected signal |
| ---: | --- | --- | --- |
| 1 | Metric-contract lock experiment | Shared `metrics.py`, schema versioning in all collection scripts | Same trajectories produce identical metric outputs across pipelines (no definition drift). |
| 2 | Replay portability drill | Manifest command normalization (`PYTHONPATH=src` or package entrypoint), full SHA normalization | Fresh-shell replay succeeds and deterministic runs hash-match artifacts. |
| 3 | 2x2 deconfounding factorial (`direct/BH x Euler/symplectic`) | Add `symplectic_bh` in simulator/CLI; update matrix runner | Separable integrator and force effects with clear effect sizes. |
| 4 | `bh_min_n` discontinuity sweep around threshold | Factorial harness from #3 | Smooth behavior across N near fallback boundary; no abrupt runtime/error jumps. |
| 5 | Adaptive close-encounter timestep ablation | Near-collision detectors and adaptive policy implementation | Three-body absolute drift improves by at least one order of magnitude. |
| 6 | Long-horizon high-N stress matrix | Checkpointed matrix extension and compute budgeting | Stable drift-vs-time trend estimates replace short-horizon proxies. |
| 7 | Perturbation ensembles for deterministic scenarios | Scenario perturbation controls and ESS reporting | Non-degenerate uncertainty intervals for two-body/three-body analyses. |
| 8 | Measurement-isolation benchmark suite | Dedicated micro/macro benchmark harness and subprocess RSS tracking | Runtime/memory variance tightens and benchmark comparability improves. |
| 9 | Runtime-target engineering campaign | Output from #8 plus kernel optimization branch | Baseline N=256 runtime moves materially toward threshold trajectory. |
| 10 | 3D + scenario-diversity expansion | 3D state/force generalization and expanded scenario library | Core directional findings persist (or are explicitly scoped) under richer physics. |

## Dependency-aware execution order

1. Contract and portability hardening: priorities **1 -> 2**.
2. Deconfounded method science: priorities **3 -> 4 -> 5**.
3. Stronger evidence quality: priorities **6 -> 7**.
4. Performance branch: priorities **8 -> 9**.
5. External-validity expansion: priority **10**.
