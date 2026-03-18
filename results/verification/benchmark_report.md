# Benchmark Report

Prepared for verification phase `review_round_1`.

## Executive verdict

- Matched-control fairness for the executed packet: `pass`.
- Evidence that the implemented CA rules beat matched non-CA baselines: `fail`.
- Evidence sufficiency for a publication-quality benchmark claim: `fail`.
- Allowed claim: only the narrow no-go from `results/analysis/phase5_final_evidence_gate.md:7-15`:
  - the repo tested the implemented `H1/H2` CA branches,
  - those branches failed under matched controls,
  - they produced no order-`668` solution and did not beat the matched `direct_greedy` baseline.
- This bar matters because `results/research_context.md:3-12` shows the work is already at `post_writer` with the draft completed, so the benchmark packet now has to survive publication-quality scrutiny rather than only the internal stop/go gate.

## What the current packet does establish

- `H1` is a decisive no-go for the current CA rule family. On the solved `4 x 79` control, both serious methods have exact-hit rate `0/16`, and `direct_greedy` beats `parallel_gain_ca` on `11/16` matched seeds, with `4/16` CA wins and `1/16` tie. On the exact `167/80` target, `direct_greedy` beats `parallel_gain_ca` on `24/24` matched seeds. See `results/analysis/experiment_readout.md:5-37` plus paired reads of `results/experiments/h1_control_sweep.json` and `results/experiments/h1_target_sweep.json`.
- `H2` is a decisive no-go only for the tested `s`-local repair branch. The `n = 9` ladder has only three starts and is weak because `random_rule_ca` solves `3/3`, while the only real order-`668` start is one deterministic `s[41]` flip where `parallel_gain_ca` and `direct_greedy` tie exactly. See `results/analysis/experiment_readout.md:39-67`, `results/analysis/baseline_benchmark_sheet.md:30-57`, and `results/analysis/phase2_baseline_review.md:19-28`.
- That is enough for the repo's internal no-go packet, but not enough for a stronger benchmark claim. The falsifier explicitly asked for solved same-template positive controls, matched non-CA baselines, reachability controls, and certificate-level reporting. See `results/swarm/falsifier.md:60-69`.

## Findings

### 1. The solved `H1` positive control still fails the publication bar

- The strongest positive control in the packet is `control_4x79`, but it does not validate solver competence under the published budget: exact-hit rate is `0/16` for both `direct_greedy` and `parallel_gain_ca`. See `results/analysis/experiment_readout.md:7-21`.
- The control therefore ranks heuristics by distance, not by exact recovery. That is good enough to reject the CA rule, but it is not good enough to claim that the benchmark stack has demonstrated competence on a solved same-template problem.
- This is precisely the kind of missing control the falsifier warned about. See `results/swarm/falsifier.md:62-68`.
- Falsifiable recommendation: preregister an exact-recovery gate on the solved same-template panel. If the current budget gives `0` exact recoveries on the perturbed-solution seeds, either raise the budget until at least one serious method succeeds or mark the positive-control packet as failed.

### 2. `H2` is under-stressed on the real order-`668` task

- The real order-`668` packet contains one degraded start only: deterministic `s[41]` flip of the published seed, with `q` fixed and search restricted to `s`. See `results/analysis/baseline_benchmark_sheet.md:33-55` and `results/analysis/experiment_readout.md:56-67`.
- The toy ladder adds only three deterministic starts, with one run per method/start cell. The repo already records this residual risk explicitly: "three toy ladder starts and one degraded 668 start." See `results/analysis/phase2_baseline_review.md:38-41`.
- `H1` has broader seed-family coverage than `H2`, but even there the packet is not a true robustness panel: control and target use different start distributions and different seed counts, so cross-condition generalization claims remain weak.
- A tie on one real start is enough to stop the implemented `s`-repair branch. It is not enough to support a broader claim that defect-transport CA is generically noncompetitive on modular-seed repair.
- Falsifiable recommendation: lock a real-start panel that includes at least one single-flip, one multi-flip, one clustered-defect, and one lower-modulus degradation, then rerun matched `s`-only baselines. If any broader claim is kept, add matched `q`-only or mixed `(q,s)` variants as separate benchmark cells.

### 3. The baseline set is fair but too narrow

- The serious comparator set is only `direct_greedy`; `random_rule_ca` and `random_walk` are negative controls, not strong competitors. See `results/analysis/baseline_benchmark_sheet.md:16-20` and `results/analysis/baseline_benchmark_sheet.md:45-49`.
- That is adequate for the internal fairness gate, but it is thinner than the falsifier's bar for publication-facing evaluation. See `results/swarm/falsifier.md:64-69` and `results/swarm/falsifier.md:73-77`.
- There is no same-representation annealed, tabu, restart, or beam-style non-CA baseline for either branch.
- There is also no exact or exhaustive reference baseline for the `n = 9` ladder, even though `results/artifacts/h2_control_structured_n9.json` records a total search space of only `262144` `(q, s)` pairs.
- Falsifiable recommendation: add at least one stronger same-representation non-CA heuristic per branch, and add an exhaustive or proved-optimal reference for the `n = 9` ladder starts. If CA still loses or ties after that, the negative result becomes materially harder to attack.

### 4. There is no CA ablation matrix and no budget-scaling stress test

- The raw artifacts show exactly one CA parameterization per branch. In `H1`, every `parallel_gain_ca` run uses `window=2`, `min_gain=6`, and `phase_move_cap=4`. In `H2`, every `parallel_gain_ca` run uses `window=1`, `min_gain=100`, and `phase_move_cap=4`.
- There is also only one locked budget and one schedule per branch: `budget_steps=96` with `odd-cycle-3-matching` for `H1`, and `budget_steps=48` with `line-2-phase` for `H2`.
- No additional experiment outputs beyond `h1_control_sweep.json`, `h1_target_sweep.json`, `h2_ladder.json`, and `h2_seed_attempt.json` appear under `results/experiments/`, so there is no recorded parameter ablation, schedule stress test, or budget ladder.
- The early-plateau pattern is real but under-tested. In the raw runs, `H1` CA reaches its best score at median `best_step=4` on the control and `best_step=10` on the target, with `16/24` target runs peaking by the first snapshot at step `12`. The real `H2` tie peaks at `best_step=2`.
- Those data strongly suggest stagnation of the current CA rules, but without a preregistered ablation grid an external reviewer can still argue that only one CA setting was falsified.
- Falsifiable recommendation: run a fixed-grid ablation over `window`, `min_gain`, `phase_move_cap`, and budget on a locked seed panel while keeping the comparator fixed. Any publication claim should survive that matrix, not a single CA setting.

### 5. Error analysis is logged, but not deep enough

- The packet already records `best_state`, `final_state`, `unique_orbits`, `orbit_collapse_ratio`, and trajectory snapshots, so this is not a missing-logging problem.
- The problem is missing diagnosis. On `H1`, the summaries give means and medians, but not uncertainty intervals, paired win tables in the artifact packet itself, or a failure-mode aggregation beyond seed-family splits.
- On the real `H2` run, the serious methods record transient best states of `l1_defect=2944` at `best_step=2` before finishing back at `3200`, while the negative controls reach lower final `l1_defect` only after dropping from modulus `16` to modulus `8`. With `snapshot_every=8`, the recorded snapshots do not show the serious methods' best step at all.
- The same `H2` run also shows an unexplained reachability split: the serious methods visit `2` unique orbits each, while the negative controls visit `49` unique orbits each. Without orbit-growth or defect-persistence analysis, it is unclear whether the branch fails because of poor coverage, deliberate modulus preservation, or both.
- This is exactly where the falsifier warned about metric leakage and reachability traps. See `results/swarm/falsifier.md:66-77`.
- Falsifiable recommendation: report paired seed-level wins/losses, bootstrap intervals for the `H1` seed panels, orbit-growth curves on tractable controls, shift-level defect persistence for `H2`, and best-versus-final / Pareto views over `(two_adic_modulus, l1_defect, defect_count, max_defect_magnitude)`.

### 6. The raw benchmark artifacts are not fully self-describing

- The repo already notes that the `H1` fairness lock remains partly load-bearing in the benchmark sheet and code because the raw JSON does not serialize every fairness parameter symmetrically. See `results/analysis/phase5_final_evidence_gate.md:31-36`.
- In the run artifacts, CA methods serialize `window`, `min_gain`, and `phase_move_cap`, while `direct_greedy` records only `snapshot_every`.
- That is acceptable for internal governance because `results/analysis/baseline_benchmark_sheet.md` and the code fill the gap, but it is below publication-grade auditability for benchmark artifacts.
- Falsifiable recommendation: normalize every run record to emit neighborhood id, move cap, acceptance rule, verifier id, equivalence reducer, and variable family for every method, then rerun the canonical packet.

## Branch-by-branch sufficiency

- `H1`: sufficient to reject the currently implemented CA rule against the matched baseline on the exact `167/80` target. Not sufficient to claim that the benchmark suite validated same-template solver competence, because the solved positive control never hits exactly.
- `H2`: sufficient to stop the currently implemented CA rule family on the tested degraded `s`-only start. Not sufficient to generalize beyond that single real-start condition.
- Overall: the benchmark evidence supports only the narrow no-go statement already enforced by `results/analysis/phase5_final_evidence_gate.md:7-29`.

## Minimum upgrade set before any publication-facing benchmark claim

1. Make at least one solved same-template control recover exactly under the published evaluation stack.
2. Expand `H2` from one real degraded seed to a prespecified real-start panel.
3. Add at least one stronger same-representation non-CA baseline per branch and an exact reference baseline for the `n = 9` ladder.
4. Run a preregistered CA ablation matrix and a budget ladder.
5. Add paired win/loss reporting, uncertainty estimates, and explicit best-versus-final error analysis.
6. Emit fully self-describing run records so fairness can be audited from artifacts alone.
