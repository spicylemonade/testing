# Benchmark Report

## Bottom Line

The current artifact set is sufficient for one narrow negative claim:

- the frozen `H1_macrocell_substitution` family is dead by an exact one-seed obstruction;
- the narrow `H2_target_direction_abelian` screen adds no value on the tiny tested family set;
- direct no-CA corridor controls remain around score `2.0` and look boundary-sensitive.

It is not sufficient for a publication-quality benchmark claim about CA-guided arithmetic Kakeya search. Several pre-registered baselines are missing, several controls are only partial, and the stored experiment traces do not support the planned efficiency or hidden-complexity comparisons.

## Finding 1: The matched no-CA baseline is incomplete and not budget-matched

Evidence: the experiment matrix requires `baseline_no_ca_same_geometry` on the same geometry and the same fixed `X`, and the frozen H1 program requires matched direct baselines on both `2 x W_1` and `2 x W_2`. The width-4 and width-6 direct controls use 4 nonzero labels, but they already differ in trial budget (`50` versus `20`). The only reported width-8 controls (`results/phase4_width8_seed501.json` and `results/phase4_sparse_unrestricted_seed502.json`) use 3 nonzero labels and only 1 trial each.

Impact: the repo can kill the frozen H1 family on its own obstruction, but it does not complete the pre-registered direct no-CA comparator for the level-2 geometry, and it does not provide a budget-matched width frontier. That blocks any publication-quality statement that H1 underperforms a fully matched direct search at level 2 or that the width trend itself is benchmarked cleanly.

Required test: run a `2 x 8` direct no-CA search with the same 4-nonzero palette, the same `initial_t` budget, the same `boundary_band`, and the same seed budget as the H1 comparison. Report a frontier over at least `{20, 50, 200}` trials across at least 10 RNG seeds. If the best exact score still stays near `2.0` or worse, the H1 no-go becomes benchmark-complete at level 2.

## Finding 2: Three pre-registered baseline families were never executed

Evidence: the matrix explicitly includes `baseline_low_height_asymmetric_X`, `baseline_bounded_slope`, and `baseline_slowly_growing_X`. I do not see explicit result rows or saved artifacts for any of the three. The current writeup only infers bounded-slope / rational-complexity failure from literature alignment, not from an in-repo matched control.

Impact: this is the largest benchmark gap. Without those rows, the evidence does not separate "the CA route is uncompetitive" from "the whole fixed-`X` corridor regime is weak unless `X` asymmetry or `|X|` growth is allowed." That is below publication quality for a causal benchmark claim.

Required test: on the same corridor geometry, run:

- one low-height asymmetric `X` sweep at matched `|X|` and coordinate-height budget;
- one explicit bounded-slope control row;
- one slowly growing-`X` schedule.

If those non-CA baselines materially outperform the fixed-`X` corridor rows, the correct claim is about `X` geometry, not CA structure.

## Finding 3: The reportable benchmark fields and error analysis are incomplete

Evidence: the benchmark plan requires `|Sigma_active|`, serialized grammar description length, search budget consumed, interface-mismatch count, rational-complexity summary, and frontiers over search budget and family size. The phase-4 markdown summaries do not report those fields. The raw random-search JSON histories record only trial metadata and `best_score_so_far`; they do not record per-trial verifier success, per-trial score, or failure reason.

Impact: hidden complexity and optimizer-budget matching are not auditable from the current artifacts. Claims about verifier-success efficiency or about CA compression versus direct search are therefore unsupported.

Required test: re-run benchmark rows with per-trial logs containing exact success/failure, score, failure reason, active-state count, grammar length, and `X` complexity summary. Report frontier curves, not just best witnesses. If H1 is still dead under that logging, the negative claim becomes audit-ready.

## Finding 4: The control and ablation program is only partially satisfied

Evidence: isotropic and random-label controls were run only on the width-4 direct control witness. `randomize_R`, `randomize_T`, and `randomize_X` use only 4 deterministic trials each. `ablation_stage_order` is unexecuted and marked not applicable after H1 dies. `ablation_aspect_ratio` is only partially covered by width changes inside height-2 direct controls; the active-height set `{2,3,4}` was never exercised beyond `H=2`. The `freeze_X_scale_n` row is also confounded: the ablation script changes to `seed_budget=6` and `boundary_band=2`, unlike the base searches that used `boundary_band=0` and larger seed budgets.

Impact: the current controls are enough to show that one width-4 direct witness is fragile. They are not enough to support a route-level robustness claim, and the current frozen-`X` scale failure is not a clean matched negative result.

Required test:

- re-run `freeze_X_scale_n` under the same `boundary_band`, seed budget, and `initial_t` budget as the base rows;
- for the top exact witnesses at widths 4 and 6, run at least 20 randomizations each for `R`, `T`, and `X`;
- add at least one matched `H=3` aspect-ratio row.

If the same failures persist under matched budgets and across multiple witnesses, the fragility claim becomes benchmark-grade.

## Finding 5: The width-8 stress tests and H2 screen are too small for broad claims

Evidence: there are 16 `results/phase4_sparse_boundary*.json` files; each is a single width-8 trial with `best: null`. The reported width-8 unrestricted controls are also single-trial rows. The H2 screen evaluates only four family IDs total: two dead H1 representatives and two successful direct controls.

Impact: these artifacts support narrow local statements only. They do not support a broad width-8 no-go, and they do not support a general claim that abelian-style invariants add no screening value outside this tiny family set.

Required test:

- repeat the width-8 unrestricted and boundary-band rows with matched budgets and at least 20 seeds per setting;
- expand H2 evaluation to the full saved direct-search archive and compare ranking quality against raw arithmetic features on verified forcing rows.

If abelian features still do not improve ranking, H2 can be killed as a general screening layer for this corridor program.

## What Is Publication-Safe Right Now

The current evidence can safely support only this claim:

- the frozen H1 grammar is exactly obstructed;
- the pre-registered H2 backup adds no value on the tiny screened family set;
- surviving direct corridor witnesses stay around score `2.0`, are boundary-sensitive, and do not currently approach the `1.70` neighborhood.

Anything stronger than that still lacks the planned baselines, matched reporting fields, or stress-test depth required for a publication-quality benchmark section.
