# Benchmark Report

## Review Round

- `post_deepen`

## Scope

- Audited inputs: `research_rubric.json`, `results/research_context.md`, `results/swarm/falsifier.md`, `results/analysis/baseline_benchmark_sheet.md`, `results/analysis/experiment_readout.md`, `results/analysis/phase2_baseline_review.md`, `results/analysis/phase4_oversight_stop_go.md`, `results/analysis/phase5_final_evidence_gate.md`, `results/analysis/cellar_design_brief.md`, `results/analysis/cellar_prefix_complexity.md`, `results/analysis/cellar_no_go.md`, `results/analysis/paper_metrics.json`, `results/analysis/cellar_paper_metrics.json`, and the current experiment artifacts under `results/experiments/`.
- Budget focus: controls, baselines, ablations, error analysis, and stress-test sufficiency only.

## Executive Call

- Branch-retirement no-go claim for the executed `H1`, `H2`, and literal `cellar` encodings: `pass`.
- Publication-grade positive efficacy or mechanism claim: `fail`.
- Publication-grade benchmark breadth / robustness claim: `fail`.
- Main reason: the packet is strong enough to kill the tested rule families, but too narrow, too single-baseline, and too degenerate in key places to support anything broader.

## Supporting Evidence

- `H1` is dead under matched same-representation controls. In `results/analysis/paper_metrics.json`, `direct_greedy` beats `parallel_gain_ca` on `11/16` solved-control seeds with `4` CA wins and `1` tie, and on `24/24` exact-`167/80` target seeds with no ties. Exact-hit rate stays `0/16` on the solved `4 x 79` control and `0/24` on the exact target for both serious methods.
- `H2` is dead only for the tested `s`-local repair branch. `results/experiments/h2_ladder.json` contains only three toy starts and `random_rule_ca` solves `3/3`. On the only real order-`668` start in `results/experiments/h2_seed_attempt.json`, `parallel_gain_ca` and `direct_greedy` tie exactly at best `two_adic_modulus = 16`, `l1_defect = 2944`, `defect_count = 25`, and `max_defect_magnitude = 496`.
- The literal `cellar` reopen is dead under the implemented tail-panel encoding. `results/analysis/cellar_paper_metrics.json` shows identical boundary-debt and stack frontiers on control tails `10`, `12`, and `14` (`11/11`, `13/13`, `15/15`), while the four `167` target panels and four degraded `668` seed projections in `results/experiments/cellar_phase6.json` all have zero exact completions and zero surviving frontier for both boundary-debt and stack states.

## Findings

### 1. Positive controls are still too weak or too degenerate for publication-grade benchmarking

- `H1` does not recover the solved `4 x 79` control under the published budget: exact-hit rate is `0/16` for both `direct_greedy` and `parallel_gain_ca`.
- `H2` uses an easy toy ladder as its only solved control, and that ladder is not discriminative: `random_rule_ca` solves `3/3`, `parallel_gain_ca` solves `2/3`, `random_walk` solves `2/3`, and `direct_greedy` solves `1/3`.
- The cellar control family proves soundness, not advantage. On tails `10`, `12`, and `14`, the static boundary-debt comparator is already exact, so the stack never faces a nontrivial same-template solved control where it can separate.
- Publication blocker: the packet can rank failures, but it does not demonstrate that the benchmark stack can solve a nontrivial same-template control in a discriminative way.
- Falsifiable upgrade: keep the current evaluation stack and add at least one solved same-template control per branch where at least one serious method succeeds exactly or achieves verified frontier savings, and at least one weak/random control fails on a nontrivial fraction of starts. If no such control exists, keep the claim limited to branch retirement.

### 2. Baseline coverage is too narrow

- `H1` and `H2` each use one serious same-representation non-CA comparator: `direct_greedy`.
- The `n = 9` ladder search space in `results/artifacts/h2_control_structured_n9.json` is only `262144` `(q, s)` pairs, yet the packet has no exhaustive or exact reference baseline there.
- The cellar branch compares the stack only to one very strong static summary, and `results/analysis/cellar_design_brief.md` explicitly allows that summary to be effectively prefix-identifying on the recorded panels.
- Publication blocker: one comparator is enough to kill the current rule instance, not enough to support claims about CA versus the relevant baseline class.
- Falsifiable upgrade: add one stronger same-representation comparator per branch, and add an exact enumerator for the `n = 9` ladder. For cellar, add a comparator ladder that removes parts of the boundary-debt state; if the stack only matches the strongest static summary, the result is an encoding no-go, not a memory-advantage study.

### 3. The packet lacks ablations, so it falsifies settings rather than rule families

- `H1` CA runs use one setting: `window = 2`, `min_gain = 6`, `phase_move_cap = 4`.
- `H2` CA runs use one setting: `window = 1`, `min_gain = 100`, `phase_move_cap = 4`.
- There is no budget ladder for `H1` or `H2`.
- The formal move cap is shared, but the effective accepted-move budget is not. Median accepted moves differ sharply even on matched runs: `38` versus `6.5` on the `H1` solved control, `75` versus `17.5` on the `H1` target, and `91` versus `3` on the `H2` ladder for `direct_greedy` versus `parallel_gain_ca`.
- Phase 6 never gets the required feedback-channel ablation from rubric item `029`; the branch fails before any gain appears, so no ablation demonstrates that a claimed gain disappears when the feedback channel is removed.
- Real Phase 6 anchor panels all use free suffix length `12`.
- Publication blocker: the repo can honestly say these specific encodings failed. It cannot claim the broader CA or cellar mechanism was stress-tested across reasonable settings.
- Falsifiable upgrade: run a preregistered grid over `window`, `min_gain`, `phase_move_cap`, and budget on locked seeds, plus an accepted-move-matched ablation where the CA and comparator medians are kept within `+/-10%`. For cellar, add `stack off`, `feedback off`, weaker-static-summary, and tail-length `10/12/14` ablations on the same panel family.

### 4. Real-anchor stress testing is too thin outside `H1`

- `H1` has the healthiest real target panel: `24` exact `167/80` seeds across `modular_projection` and `random_weight`.
- `H2` has only one real degraded `668` start: `seed_sflip41_mod16`.
- Phase 6 uses four `167` target panels and four degraded `668` seed projections, but every one of those real-anchor panels has zero exact completions and zero frontier for both boundary-debt and stack states.
- Publication blocker: `H2` cannot support a robustness claim from one real start, and Phase 6 cannot support a mechanism claim from only zero-frontier real panels.
- Falsifiable upgrade: expand `H2` to a preregistered real-start panel of at least `20` degraded starts spanning single-flip, clustered, and lower-modulus corruptions. For cellar, require at least one real or surrogate panel with nonzero exact frontier before making any memory-mechanism claim; if every real panel remains zero-frontier, state only that no signal was found on the sampled panels.

### 5. Error analysis exists, but not at publication strength

- `results/analysis/paper_metrics.json` contains confidence intervals and paired `H1` seed tables, but the canonical experiment artifacts and current benchmark packet do not surface them as primary evidence.
- `H1` target trajectories already hint at a specific failure mode that is not analyzed: `parallel_gain_ca` reaches its best state by step `24` in all `24` target runs, while `direct_greedy` does so in only `7/24`, which looks like early CA stagnation rather than late-budget failure.
- On the decisive `H2` real run, both serious methods hit their best state at step `2`, but `snapshot_every = 8`, so the saved snapshots skip the decisive event.
- In that same run, weak controls lower final `l1_defect` only by collapsing from modulus `16` to modulus `8`, which exposes a real multi-objective tradeoff but leaves it under-analyzed.
- Phase 6 zero-frontier panels make purity automatic; they do not show how the stack behaves on ambiguous real prefixes.
- The Phase 6 schema does not serialize `oracle_calls`, cache hits, or wall-clock cost, so the rubric path based on a "smaller exact-oracle budget" is not independently auditable from `results/experiments/cellar_phase6.json`.
- Publication blocker: reviewers cannot distinguish poor search, metric leakage, and insufficient budget from the current diagnostic packet alone.
- Falsifiable upgrade: publish paired seed-level win/loss tables and uncertainty intervals in the canonical benchmark artifact, add a best-step / trajectory taxonomy for `H1`, save event-level snapshots at every best-step update, and report best-versus-final Pareto views over `(two_adic_modulus, l1_defect, defect_count, max_defect_magnitude)`. For cellar, add witness-retention, frontier-savings, `oracle_calls`, cache-hit, and wall-time views on nondegenerate panels.

### 6. Artifact auditability is still not clean enough

- `results/analysis/phase5_final_evidence_gate.md` already notes that the `H1` fairness lock is partly load-bearing in the benchmark sheet and code because the raw JSON does not serialize every fairness parameter symmetrically.
- In the run artifacts, `parallel_gain_ca` exposes `window`, `min_gain`, and `phase_move_cap`, while `direct_greedy` mostly exposes only `snapshot_every`.
- Phase 6 held-out control metrics for `control_4x79_tail10` and `control_4x79_tail14` live in `results/analysis/cellar_paper_metrics.json`, not in the canonical `results/experiments/cellar_phase6.json` artifact.
- `results/analysis/cellar_prefix_complexity.md` uses shorthand panel labels (`shift_0`, `shift_1`, `single_flip_41`, `cluster_40_42`) that do not match the canonical labels in `results/experiments/cellar_phase6.json` (`single_flip_0_mod8`, `single_flip_41_mod16`, `cluster3_0_2_mod8`, `cluster5_0_4_mod8`).
- Publication blocker: a reader cannot audit fairness and Phase 6 panel identity from the canonical experiment outputs alone.
- Falsifiable upgrade: normalize every run record to emit neighborhood id, acceptance rule, move cap, verifier id, equivalence reducer, and variable family for every method. Fold the held-out cellar controls into the canonical experiment artifact and use one label scheme everywhere.

## Branch-By-Branch Sufficiency

- `H1`: sufficient to reject the currently implemented CA rule against the matched baseline on the exact `167/80` target. Not sufficient to claim solver competence or benchmark breadth, because the solved positive control never hits exactly.
- `H2`: sufficient to reject the tested `s`-local repair branch on the tested real degraded seed. Not sufficient to generalize beyond that single real-start condition.
- `cellar`: sufficient to retire the exact tail-panel encoding implemented here. Not sufficient to claim anything broader about weaker static summaries or pushdown utility outside this encoding.

## Unresolved Risks

- A broader manuscript could accidentally overgeneralize from one serious baseline and one CA setting per branch.
- The only real `H2` start could be unrepresentative, and the easy `n = 9` ladder could mislead if treated as mechanism evidence.
- The Phase 6 no-go depends on a strong boundary-debt summary; the current evidence does not show whether weaker non-stack summaries would separate from the stack.
- Several benchmark facts remain analysis-only rather than canonical-artifact facts.

## Recommendation

- `PASS` only for the narrow benchmark claim: the executed `H1`, `H2`, and Phase 6 cellar encodings fail under their matched controls.
- `FAIL` for any publication-grade efficacy, mechanism, or broad benchmark claim until the specific upgrades above are executed.
- Overall verdict: `REVISE`.
