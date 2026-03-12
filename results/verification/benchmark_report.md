# Benchmark Report

## Round

- Review round: `review_round_2`

## Verdict

- Conditional pass for the current narrow package: the benchmark is strong enough for the theorem-backed AP/FUAP rational lane and for the four isolated exact-certified `quadratic_convergent_even` examples.
- Still not publication-ready for any broader sparse-family claim. The current outputs do not justify `quadratic-only`, `periodic-CF-only`, `zero-intercept-specific`, or `robust sparse-selector` language.

## What the benchmark now supports

- `results/experiments/full_panel_results.json` and `results/experiments/metrics_full_panel.json` cover 145 executed cases with 20 justified waivers and 32 exact certificates.
- The exact hits are heavily concentrated: 28 are rational AP/FUAP baselines, and only 4 are nondegenerate irrational exact cases (`phi - 1`, `phi`, `sqrt(2)`, `1 + sqrt(2)` on `quadratic_convergent_even`).
- `results/experiments/ablation_summary.json` now cleanly separates the lanes: positive-density selectors give 28 exact cases, all rational; zero-density selectors give 4 exact cases, all from the same quadratic-convergent construction.
- `results/experiments/claim_sensitive_ablation.json` materially improves round 1 by pushing all 15 `uncertified_exact_holdout` rows to length `320`: `salem_quartic / ost_suffix_001` fails by `80`, and all 3 plastic prefix fits fail by `40`.
- That still leaves 11 unresolved long-holdout rows at `320`, split into 5 rational-trivial sparse leaks and 6 irrational quadratic leaks, so the sparse lane remains empirical rather than structural.

## Benchmark gaps

### Missing baselines

- No inhomogeneous baseline of the form `floor(n r + beta)` appears in the current outputs. `beta_endpoint_suffix_10` is a selector construction, not the falsifier's intercept control, so zero-intercept specificity remains untested.
- The nonquadratic control bank is still too thin for any boundary claim: one cubic Pisot (`plastic`), one Salem quartic, and one transcendental (`e`) can reject a crude `all nonquadratics survive` story, but they cannot support a sharp `quadratic is the boundary` story.
- There are still no continued-fraction-prefix-matched nonquadratic controls for the four quadratic winners, so the benchmark does not distinguish structural quadratic behavior from a long finite-prefix effect.

### Missing controls

- No same-slope intercept sweep is run on the four certified quadratic examples, so the package cannot claim that the sparse exact identities are specific to `floor(n r)` rather than to a nearby `floor(n r + beta)` problem.
- No density-matched or growth-matched selector-jitter control is run to the same `320`-term standard around `quadratic_convergent_even`. The machine-readable `quadratic_variant_ablation` in `results/experiments/claim_sensitive_ablation.json` records only `count: 20` screens for `odd`, `even_shift1`, and `every_third`.
- `results/experiments/metrics_full_panel.json` reports `false_positive_rate = 0.0`, but only on the curated frozen panel and without any uncertainty estimate or blind null bank. That is screening evidence, not publication-grade calibration.

### Weak ablations

- The order-cap and fit-length ablations are useful overfitting checks, not mechanism tests: raising the cap to `d <= 6` or `d <= 8` adds 0 new exact cases but creates 84 and 89 classification flips, while `fit_length = 8` creates 87 extra false candidates.
- The selector-family ablation is still coarse. It shows that the sparse story lives entirely in one construction family, but it does not test whether that family survives matched perturbations that preserve density and growth.
- The modulus ablation is weakly informative: dropping `{7,11,25}` changes 0 of 49 candidate verdicts, which shows redundancy of the current panel, not robustness to alternative prime choices.

### Incomplete error analysis

- `results/experiments/evaluation_memo.md` now explains the broken plastic and Salem anomalies, but it still does not explain the main unresolved pool: the 11 rows that keep exact holdouts through `320` without certificates.
- The current outputs do not explain why `quadratic_convergent_even` certifies while same-slope `fib_indices`, `pell_indices`, and `ost_single_nonzero_digit` remain long exact leaks on the same four quadratic slopes.
- The screen-level metric `holdout_exact_20` is not a calibrated proxy for final truth: 5 exact-certified rational FUAP rows still have `holdout_exact_20 = false`, so any benchmark table that mixes holdout-screen and certificate-level success needs a clearer error model.

### Missing stress tests

- No replay pushes the 11 surviving uncertified rows from `320` to `640`.
- No slope-perturbation stress test uses nonquadratic irrationals sharing the first 20 or 40 continued-fraction digits of `phi`, `phi - 1`, `sqrt(2)`, or `1 + sqrt(2)`.
- No disjoint-prime modular-shadow replay replaces the current modulus set with a fresh panel such as `{13,17,19,29,49}`.

## Where the evidence is still insufficient

- Publication-quality support exists for: the rational AP/FUAP characterization, the negative long-holdout ruling-out of the strongest nonquadratic anomaly, and the four exact-certified quadratic-convergent examples as isolated constructions.
- Publication-quality support does not exist for: a quadratic-family boundary, a periodic-continued-fraction boundary, a zero-intercept boundary, a robust sparse-selector phenomenon, or a calibrated `false_positive_rate = 0.0` claim.

## Falsifiable follow-ups

- Add an intercept panel `floor(n r + beta)` for the four certified quadratic slopes and matched controls with at least `beta = 1/2` and one irrational `beta`. If the certificates survive unchanged, drop any zero-intercept narrative; if they disappear, the sparse examples are intercept-sensitive and should be framed that way.
- For each of `phi`, `phi - 1`, `sqrt(2)`, and `1 + sqrt(2)`, construct nonquadratic irrationals sharing the first 20 and 40 continued-fraction digits and rerun `quadratic_convergent_even`. If any exact certificate appears, `quadratic` is not the right boundary.
- Extend `odd`, `even_shift1`, `every_third`, and one de-convergent jittered variant to the same `320`-term holdout and exact-certificate search used for the main winners. If any variant certifies, `quadratic_convergent_even` is not isolated.
- Replace the modulus panel with a disjoint set on all 22 non-`no_candidate`, nonexact rows. If the shadow classifications change materially, the current modular-shadow evidence is panel-sensitive rather than robust.
- Push the 11 surviving uncertified rows to `640` and either find structural certificates or force explicit breakpoints. If any of the 6 irrational quadratic leaks fail, the sparse narrative narrows further; if some certify, the claim boundary must widen and be rewritten.
- Add a blind null-control bank of prefix-matched nonquadratic slopes and report a confidence interval for the false-positive rate. If any exact certificate appears, `false_positive_rate = 0.0` should be retired from the benchmark story.
