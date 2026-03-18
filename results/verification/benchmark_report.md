# Benchmark Report

Review round: `review_round_1`

## Bottom Line

The artifact set supports one clean benchmark-safe negative result:

- the frozen `H1_macrocell_substitution` family is dead by an exact structural obstruction (`results/phase4_h1_obstruction.json`);
- the current `H2_target_direction_abelian` screen shows no gain on a tiny local family set (`results/phase4_h2_screen.json`);
- surviving direct corridor controls remain around score `2.0` and are fragile under the limited ablations that were actually run (`results/phase4_h1_frontier.md`, `results/phase4_ablations.md`).

It does **not** support a publication-quality benchmark claim about CA-guided search, matched level-2 performance, or route-level robustness. The main gaps are: incomplete matched baselines, missing pre-registered non-CA controls, confounded ablations, and weak trace-level error analysis.

## Finding 1: The matched baseline program is incomplete at level 2

The pre-registered H1 comparison requires matched direct no-CA baselines on the same `2 x W_1` and `2 x W_2` geometries with the same `X` and matched budgets (`results/phase3_h1_program.md`, `results/phase2_baseline_matrix.md`, `results/phase4_experiment_matrix.md`). That is not what the stored artifacts provide.

- The saved direct controls at widths `4` and `6` use the 4-nonzero same-sum palette, but their trial budgets already differ: `50` trials at width `4` versus `20` at width `6` (`results/phase4_width4_seed601.json`, `results/phase4_width6_seed602.json`).
- The only width-`8` “success” rows are exploratory 1-trial artifacts with 3 nonzero labels, not the 4-nonzero palette used for the matched width-`4` and width-`6` rows (`results/phase4_width8_seed501.json`, `results/phase4_sparse_unrestricted_seed502.json`, `results/phase4_h1_frontier.md`).
- `H1_L2` is width `8`, but the H2 screen compares it only against width-`4` and width-`6` direct controls, even though H2 was supposed to use the same matched baselines as H1 (`results/phase4_h2_screen.md`, `results/phase4_h2_screen.json`, `results/phase3_h2_program.md`).

Impact: the repo can kill frozen H1 on its exact obstruction, but it cannot yet make a benchmark-complete statement that matched direct search also fails cleanly on the corresponding level-2 geometry.

Falsifiable missing test:

- run a true `2 x 8` direct no-CA comparator with the same 4-nonzero same-sum `X`, the same `boundary_band`, and the same seed / `initial_t` budgets used for the matched corridor program;
- report a frontier over at least `{20, 50, 200}` trials across at least `10` RNG seeds;
- include that same width-`8` row in any future H2 screen.

If the best exact score still stays near `2.0` or worse, the H1-vs-direct negative benchmark becomes materially stronger. If it improves toward `1.70`, the current negative benchmark story is overstated.

## Finding 2: Three pre-registered non-CA baselines are missing entirely

The experiment matrix pre-registers three non-CA baseline families that are not present in the saved outputs:

- `baseline_low_height_asymmetric_X`
- `baseline_bounded_slope`
- `baseline_slowly_growing_X`

These rows are required by `results/phase2_baseline_matrix.md` and `results/phase4_experiment_matrix.md`, but the stored evidence contains only the frozen H1 obstruction, direct corridor controls, the narrow H2 screen, and width-4 witness ablations.

Impact: this is the largest benchmark gap. Without those baseline families, the current evidence does not distinguish:

- “the CA route is uncompetitive” from
- “the entire fixed-`X` corridor regime is weak, while non-CA changes in `X` geometry carry the real signal.”

That means the current bounded-slope / rational-complexity interpretation is still benchmark-incomplete. Right now it is an interpretation, not a controlled in-repo comparator result.

Falsifiable missing test:

- run one matched low-height asymmetric `X` sweep on the same corridor geometry;
- run one explicit bounded-slope control on the same geometry;
- run one slowly growing-`X` schedule on the same geometry;
- report exact-score frontiers under the same verifier and matched budgets.

If those non-CA rows materially beat the direct corridor frontier, the correct conclusion shifts from “CA failed” to “`X` geometry dominates this regime.”

## Finding 3: The control and ablation program is only partially executed, and some rows are confounded

The current ablation set is enough to show that one width-`4` direct witness is fragile. It is not enough to support a route-level robustness claim.

Observed weaknesses:

- `baseline_isotropic` and `baseline_random_label` appear only as perturbations of one width-`4` witness, not as matched frontier rows over the planned family set (`results/phase4_ablations.md`, `results/phase4_ablations.json`).
- `ablation_stage_order` was never run; it is marked `not_applicable` after H1 died (`results/phase4_ablations.json`).
- `ablation_aspect_ratio` never leaves the height-`2` corridor family, even though the active geometry in the baseline plan explicitly included `H in {2,3,4}` (`results/phase2_baseline_matrix.md`, `results/phase4_h1_frontier.md`).
- `ablation_freeze_X_scale_n` is confounded. The ablation script changes to `seed_budget=6` and `boundary_band=2`, unlike the base direct rows that used `boundary_band=0` and larger search budgets (`scripts/phase4_ablations.py`, `results/phase4_width4_seed601.json`, `results/phase4_width6_seed602.json`).
- `ablation_exact_elimination_replacement` was not actually executed as a comparator run. The report only says that all rows use exact verification, but the search code still uses `forcing_order_fast()` as a surrogate inside `greedy_seed_search()` to choose seeds (`results/phase4_ablations.md`, `scripts/phase4_ablations.py`, `scripts/ca_kakeya_search.py`).
- The saved width-`8` boundary stress archive is too thin: sixteen single-trial files, all with `best: null`, mixing different `X` tracks and offering no matched frontier over seeds or budgets (`results/phase4_sparse_boundary_seed201.json`, `results/phase4_sparse_boundary4_seed301.json`, `results/phase4_sparse_boundary12_seed401.json`).

Impact: the current control program supports only a narrow fragility claim for one witness. It does not yet support publication-grade claims about boundary sensitivity, scaling failure, or elimination-versus-surrogate parity.

Falsifiable missing tests:

- re-run `freeze_X_scale_n` under the same budgets as the base direct rows;
- expand `randomize_R`, `randomize_T`, and `randomize_X` to at least `20` draws each on the best width-`4` and width-`6` witnesses;
- add at least one matched `H=3` aspect-ratio row;
- run a true exact-elimination replacement comparator on the same candidate family with the surrogate ranking step removed;
- redo the width-`8` boundary stress as separate matched sweeps for the 3-nonzero and 4-nonzero `X` tracks, with fixed budgets and at least `20` seeds per setting.

If the same failures persist under those matched conditions, the fragility and non-scaling claims become benchmark-grade. If they do not, the current ablation story was underpowered or confounded.

## Finding 4: Error analysis and trace auditability are insufficient for publication-quality benchmarking

The reporting plan required more than exact scores. It also required visible complexity and audit fields such as:

- `|Sigma_active|`
- serialized grammar description length
- search budget consumed
- rational-complexity summary of `X`
- frontier reporting over search budget and family size

Those fields are not fully present in the saved phase-4 artifacts (`results/phase2_baseline_matrix.md`, `results/phase2_benchmark_signoff.md`, `results/phase4_h1_frontier.md`, `results/phase4_h2_screen.md`, `results/phase4_ablations.md`).

The raw JSON traces are also too thin for proper error analysis:

- the direct-search payloads store `trials`, `boundary_band`, `x_labels`, `history`, and `best`, but not `seed_budget`, `initial_t_budget`, grammar size, or per-trial verifier outcome (`scripts/ca_kakeya_search.py`);
- `history` records only the sampled geometry and `best_score_so_far`, not per-trial success/failure, failure reason, support size, or exact score of failed candidates;
- the saved frontiers are single-seed trajectories, not seed-aggregated curves with uncertainty.

Impact: hidden-complexity claims, optimizer-budget matching, verifier-success efficiency, and failure-mode analysis are not auditable from the raw artifacts alone.

Falsifiable missing test / logging requirement:

- re-run the benchmark rows with per-trial logs that include exact verifier success/failure, score when present, failure reason, `seed_budget`, `initial_t_budget`, `boundary_band`, `|X|`, coordinate-height summary, active-state count, and grammar length;
- report aggregate frontiers across multiple seeds rather than only single-seed best-of-run traces.

If the benchmark story still holds under that logging, it becomes auditable. If not, the current evidence was relying on underspecified traces.

## Finding 5: The H2 null result is local, not general

The current H2 result is a narrow null on four family IDs:

- `h1_identity_L1`
- `h1_identity_L2`
- `phase4_width4_seed601`
- `phase4_width6_seed602`

That is enough to say the abelian-style invariant package adds no value on this tiny screened set (`results/phase4_h2_screen.md`, `results/phase4_h2_screen.json`). It is not enough to support a broader claim that H2 adds no screening value for the corridor program as a whole, because:

- the screen omits a real matched width-`8` direct control;
- it does not compare on the full saved direct-search archive;
- it does not quantify ranking quality or retention quality over a broader family set.

Falsifiable missing test:

- evaluate the H2 invariant package against the full saved direct-search archive;
- include a true matched width-`8` direct control;
- compare ranking / retention of the best exact certificates against the raw arithmetic feature set named in `results/phase3_h2_program.md`.

If H2 still shows no ranking gain, the null becomes much more credible. If it improves retention of the best exact rows, the current immediate-kill conclusion was too strong.

## Publication-Safe Claim Right Now

The benchmark-safe claim is narrow:

- frozen H1 is exactly obstructed before scoring;
- H2 shows no screening gain on the tiny local family set that was actually tested;
- direct corridor controls remain around score `2.0`, are boundary-sensitive, and do not currently approach the `1.70` neighborhood.

Anything stronger than that still lacks the matched baselines, ablation depth, control coverage, or trace-level auditability required for a publication-quality benchmark section.
