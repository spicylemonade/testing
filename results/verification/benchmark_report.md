# Benchmark Report

Prepared for verification phase `post_researcher`.

## Executive verdict

- Matched-control fairness: `pass`
- Evidence that the implemented CA rules beat matched non-CA baselines: `fail`
- Evidence sufficiency for a publication-quality benchmark claim: `insufficient`
- Allowed claim: only a narrow branch-specific no-go. The packet does not justify broader statements about CA search for Hadamard-`668`.

## What the packet already establishes

- The benchmark design is meaningfully matched on representation, neighborhood, budget, verifier, and symmetry accounting for the implemented `H1/H2` branches. See `results/analysis/baseline_benchmark_sheet.md:5-57` and `results/analysis/phase4_oversight_stop_go.md:14-18`, `32-36`.
- The decisive branch outcomes are stable under the recorded packet: `H1` loses to `direct_greedy` on both the control and target sweep, and `H2` ties `direct_greedy` on the only real `668` start. See `results/analysis/experiment_readout.md:5-67`.
- That is enough for the repo's internal stop/go gate and for the narrow final no-go packet. See `results/analysis/phase5_final_evidence_gate.md:7-15`.

## Findings

### 1. The solved H1 positive control does not validate solver competence

- On the nominally solved `control_4x79` task, exact-hit rate is `0/16` for both `direct_greedy` and `parallel_gain_ca`. See `results/analysis/experiment_readout.md:7-13`.
- A paired read of the raw runs in `results/experiments/h1_control_sweep.json` shows `direct_greedy` beats `parallel_gain_ca` on `11/16` matched seeds, `parallel_gain_ca` wins `4/16`, and `1/16` ties. That is enough to prefer the baseline, but not enough to claim the control strongly validates the search stack.
- The control therefore ranks heuristics by distance on a same-template instance, but it does not show that the published evaluation stack can actually recover a known certificate under the locked budget.
- This is the main missing control for publication-quality interpretation, because the falsifier explicitly required solved same-template positive controls and certificate-level reporting. See `results/swarm/falsifier.md:60-69`.
- Falsifiable recommendation: preregister an exact-recovery gate on perturbed-solution seeds for at least one solved `4 x p` control. If no serious method achieves nonzero recovery at the locked budget, either raise the budget until one does or treat the positive-control packet as failed.

### 2. H2 is underpowered on the real task

- The real `668` evaluation consists of one degraded start only: deterministic `s[41]` flip of the published seed. See `results/analysis/baseline_benchmark_sheet.md:50-57` and `results/analysis/experiment_readout.md:56-67`.
- The real `668` evaluation also fixes `q` and searches only in `s`, so the executed benchmark closes only the `s`-local-repair branch, not broader mixed-state repair variants. See `results/analysis/baseline_benchmark_sheet.md:33-39`.
- The toy ladder contains only three start families, with one run per method/start cell, and the repo already records the residual risk explicitly: "three toy ladder starts and one degraded 668 start." See `results/analysis/phase2_baseline_review.md:38-41`.
- A tie on one real start is sufficient to stop this implemented branch internally, but it is not sufficient to support a broader publication claim that defect-transport CA is generically noncompetitive on modular-seed repair.
- Falsifiable recommendation: construct a locked panel of degraded `668` starts spanning single-flip, multi-flip, clustered-defect, and lower-modulus perturbations, and either add matched `q`-only / mixed `(q,s)` variants or narrow the claim explicitly to `s`-only repair.

### 3. There is no CA ablation matrix or budget-scaling stress test

- The raw experiment artifacts show one CA rule setting per branch. In `H1`, every `parallel_gain_ca` run uses `window=2`, `min_gain=6`, and `phase_move_cap=4`. In `H2`, every `parallel_gain_ca` run uses `window=1`, `min_gain=100`, and `phase_move_cap=4`.
- No additional experiment outputs beyond `h1_control_sweep.json`, `h1_target_sweep.json`, `h2_ladder.json`, and `h2_seed_attempt.json` appear under `results/experiments/`, so there is no recorded parameter ablation or budget ladder.
- The early-plateau pattern is real but not fully stress-tested. Derived from the raw runs, the H1 CA reaches its best score with median `best_step=4` on the control and `best_step=10` on the target; `16/24` H1 target runs peak by the first snapshot at step `12`. The real H2 `668` tie peaks by step `2`.
- Those data strongly suggest rule-family stagnation, but without a locked ablation grid an external reviewer can still argue that only one CA setting was falsified.
- Falsifiable recommendation: run a preregistered matrix over `window`, `min_gain`, `phase_move_cap`, and budget steps on a fixed seed panel while keeping the comparator fixed. Any publication claim should survive that matrix, not a single CA setting.

### 4. The baseline set is fair but too narrow for publication-facing comparison

- The serious comparator set is only `direct_greedy`, with `random_rule_ca` and `random_walk` as negative controls. See `results/analysis/baseline_benchmark_sheet.md:16-28` and `45-57`.
- That is adequate for the repo's fairness gate, but it is thinner than the falsifier's benchmark bar and thinner than the heuristic Hadamard literature already cited by the project. See `results/swarm/falsifier.md:62-69` and `79-85`.
- In particular, there is no same-representation annealed or tabu-style non-CA baseline, and there is no exact or exhaustive reference baseline reported for the tiny `n=9` ladder starts.
- Falsifiable recommendation: add at least one stronger same-representation heuristic baseline per branch and add exhaustive or proved-optimal reference data for the `n=9` ladder starts. If CA still loses or ties, the negative result becomes materially harder to contest.

### 5. Reachability and error analysis are logged, but not explained

- The packet records `unique_orbits`, `orbit_collapse_ratio`, and trajectory snapshots, and the H1 readout already shows a clear reachability deficit for the CA relative to `direct_greedy`. See `results/analysis/experiment_readout.md:17-20` and `33-36`.
- A paired read of the raw `H1` target runs in `results/experiments/h1_target_sweep.json` is decisive on ranking: `direct_greedy` beats `parallel_gain_ca` on `24/24` matched seeds. That supports the stop decision.
- On the real `H2` run, the current summaries also compress a multi-metric tradeoff too aggressively: the serious methods record transient best states of `l1_defect=2944` at `best_step=2` before finishing back at `3200`, while the negative controls reach lower final `l1_defect` only after dropping from modulus `16` to modulus `8`. With `snapshot_every=8`, the recorded snapshots do not even show the serious methods' best step.
- The real `H2` run also exhibits an unreported reachability split: the serious methods visit only `2` unique orbits each, while the negative controls visit `49` unique orbits each. Without an orbit-growth analysis, it is unclear whether the branch fails because of deliberate modulus preservation, poor coverage, or both.
- There is therefore still no coverage estimate, no paired win/loss table in the artifact packet itself, no defect-location persistence analysis for `H2`, and no explicit best-versus-final or Pareto analysis showing how `two_adic_modulus`, `l1_defect`, `defect_count`, and `max_defect_magnitude` trade off.
- This matters because the falsifier explicitly warned about reachability and metric-leakage traps. See `results/swarm/falsifier.md:66-77`.
- Falsifiable recommendation: report paired seed-level wins/losses, reachable-orbit estimates on tractable controls, shift-level defect persistence on `H2`, and best-versus-final / Pareto curves over `(two_adic_modulus, l1_defect, defect_count, max_defect_magnitude)`. The benchmark should diagnose why the CA fails, not only that it fails.

### 6. The raw experiment artifacts are not fully self-describing

- The repo already notes that the H1 fairness lock remains partly load-bearing in the benchmark sheet and code because the raw JSON does not serialize every fairness parameter symmetrically. See `results/analysis/phase4_oversight_stop_go.md:17-21` and `results/analysis/phase5_final_evidence_gate.md:31-36`.
- In the run artifacts, CA methods serialize `window`, `min_gain`, and `phase_move_cap`, while `direct_greedy` records only `snapshot_every`.
- That is acceptable for internal governance because the benchmark sheet and code fill the gap, but it is below publication-grade auditability for benchmark artifacts.
- Falsifiable recommendation: normalize every run record to emit neighborhood id, move cap, acceptance rule, variable family, verifier id, and symmetry reducer for every method, then rerun the canonical packet.

## Branch-by-branch sufficiency

- `H1`: sufficient to reject the currently implemented CA rule against the matched baseline on the exact `167/80` target. Not sufficient to claim that the benchmark suite has validated same-template solver competence, because the positive control never hits exactly.
- `H2`: sufficient to stop the currently implemented CA rule family on the tested degraded `668` start. Not sufficient to generalize beyond that single real-start condition.
- Overall: the benchmark evidence supports only the narrow statement from the final evidence gate. The implemented `H1/H2` branches failed under matched controls and produced no order-`668` advantage.

## Minimum upgrade set before any publication-facing benchmark claim

1. Make at least one solved same-template control genuinely solve under the published evaluation stack.
2. Expand `H2` from one real degraded seed to a prespecified real-start panel.
3. Add a CA ablation matrix and a budget ladder.
4. Add at least one stronger same-representation non-CA heuristic baseline per branch.
5. Emit fully self-describing run records so fairness can be audited from artifacts alone.
