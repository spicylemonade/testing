# Benchmark Report

## Round

- Phase: `review_round_1`

## Verdict

- Conditional pass for the theorem-backed rational AP/FUAP lane.
- Not publication-ready for any broader sparse-irrational claim. The current benchmark does not yet justify `quadratic-specific`, `periodic-CF-specific`, or `zero-intercept-specific` language.

## What the outputs actually show

- `results/experiments/full_panel_results.json` covers 145 executed cases, 20 waivers, 11 slopes, and 15 selectors.
- `results/experiments/metrics_full_panel.json` reports 32 exact recurrences, but 28 of them are rational AP/FUAP baselines; the only nondegenerate irrational exact certificates are the 4 `quadratic_convergent_even` cases for `phi`, `phi_minus_1`, `sqrt2`, and `one_plus_sqrt2`.
- The pooled `exact_hit_rate = 0.2207` is not claim-calibrated: the case table implies 28/40 exact on rational rows versus only 4/105 exact on irrational rows.
- `results/experiments/metrics_full_panel.json` still contains 15 `uncertified_exact_holdout` rows, including the nonquadratic control `salem_quartic / ost_suffix_001`.
- `results/experiments/claim_sensitive_ablation.json` extends long holdouts for only 11 selected cases, not for the full uncertain set.

## Benchmark blockers

### Missing baselines

- No inhomogeneous intercept baseline `floor(n r + beta)` appears in the current outputs. The selector `beta_endpoint_suffix_10` is not a substitute for the falsifier's requested intercept control, so zero-intercept specificity is untested.
- The nonquadratic comparison lane is too thin for a family claim: there is one cubic Pisot (`plastic`), one Salem quartic, and one transcendental (`e`). That can reject a crude `all Pisot survive` story, but not support a sharp `quadratic is the boundary` story.
- Coverage below `1` is also thin: only `1/2` and `phi_minus_1` are present. Any publication claim about general `0 < r < 1` behavior would outrun the benchmark.

### Missing controls

- There are no continued-fraction-prefix-matched nonquadratic controls. Current negatives (`plastic`, Salem quartic, `e`) do not test whether `quadratic_convergent_even` succeeds because of eventual periodicity or because a long finite prefix already imitates the same recurrence.
- There are no density- and complexity-matched perturbation controls for the winning sparse selector. `quadratic_convergent_even` is compared to a few nearby templates, but not to de-convergent or randomized selectors with the same growth profile.
- `results/experiments/metrics_full_panel.json` reports `false_positive_rate = 0.0`, but only on a small curated panel and without a confidence interval. That is not publication-grade calibration.

### Missing or weak ablations

- `results/experiments/full_panel_results.json` fixes `fit_length = 12`, and no fit-window ablation is reported. Since `results/experiments/claim_sensitive_ablation.json` already shows that higher order creates many extra false fits, window-length sensitivity is a missing benchmark knob.
- The long-holdout ablation is selective rather than exhaustive: it covers 11 handpicked cases, not all 15 `uncertified_exact_holdout` rows. The omitted set includes `salem_quartic / ost_suffix_001`, `phi / ost_single_nonzero_digit`, and `phi_minus_1 / ost_single_nonzero_digit`.
- The selector-variant ablation is local and one-sided. It probes variants near `quadratic_convergent_even`, but it does not apply the same perturbation family to matched nonquadratic controls.
- The modulus ablation is weakly informative: dropping `{7,11,25}` changes 0 of 49 candidate verdicts, which shows redundancy of the current modulus panel, not that modular shadows still separate positives from hard negatives under different prime choices.

### Missing error analysis

- `results/experiments/evaluation_memo.md` gives 3 failure studies, but the unexplained risk pool is larger: 15 `uncertified_exact_holdout`, 7 `selector_shadow_failure`, 21 `set_sequence_confusion`, and 43 `post_selection_leakage` tags in `results/experiments/metrics_full_panel.json`.
- The strongest control anomaly, `salem_quartic / ost_suffix_001`, is not analyzed at all. Until that case is either broken by longer holdout or structurally explained, the sparse-lane story is not cleanly quadratic.
- The current outputs also do not explain why `quadratic_convergent_even` certifies while same-slope Ostrowski selectors on `phi` and `phi_minus_1` remain only leaks.

### Missing stress tests

- No all-leak replay is run to `320` or `640` terms.
- No slope-perturbation stress test uses nonquadratic irrationals sharing the same first continued-fraction digits as `phi` or `sqrt2`.
- No intercept stress (`beta` sweep) or selector-jitter stress is run on the certified quadratic lane.

## Falsifiable follow-ups

- Add an intercept control panel for `floor(n r + beta)` with at least `beta = 1/2` and one irrational `beta` on the same sparse selectors. If the four certified `quadratic_convergent_even` hits survive unchanged, the mechanism is not zero-intercept-specific; if they disappear, the current narrative changes materially.
- For each of `phi` and `sqrt2`, construct nonquadratic irrationals sharing the first 20 and 40 continued-fraction digits and rerun `quadratic_convergent_even`. If exact certificates still appear, the current quadratic evidence is likely prefix-driven rather than structural.
- Extend `40/80/160/320` holdouts and certificate attempts to all 15 `uncertified_exact_holdout` rows, especially `salem_quartic / ost_suffix_001`, `phi / ost_single_nonzero_digit`, and `phi_minus_1 / ost_single_nonzero_digit`.
- Ablate `fit_length` across `8/12/16/24` and add density-matched perturbation selectors around `quadratic_convergent_even`. A publication-safe sparse claim should survive these changes without creating new nonquadratic exact certificates.
- Expand the control bank with at least 3 additional nonquadratic algebraic slopes and 3 additional unbounded-type/transcendental slopes under the same selector families. If any exact certificate appears, the proposed boundary needs revision; if none do, the quadratic narrative becomes materially stronger.

## Publication-safe claim boundary

- Benchmark support is strong enough for: rational AP/FUAP baselines and the 4 exact-certified `quadratic_convergent_even` identities as isolated constructions.
- Benchmark support is not strong enough for: a quadratic-family characterization, a periodic-CF characterization, a zero-intercept characterization, or any claim that the sparse lane has been cleanly separated from matched nonquadratic controls.
