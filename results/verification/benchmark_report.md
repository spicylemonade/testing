# Benchmark Report

## Verdict

- Verdict: conditional pass for the narrow claim set.
- The benchmark is now strong enough to support the periodic-gap theorem lane and the four certified `quadratic_convergent_even` identities, but it still does not justify a full quadratic-family characterization.

## What the current outputs establish

- `results/experiments/full_panel_results.json` now reports 145 executed cases, 20 justified waivers, and 32 exact-certified cases.
- The exact-certified set splits cleanly into 28 rational AP/FUAP baselines and 4 nondegenerate quadratic-convergent cases: `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)`.
- `results/experiments/metrics_full_panel.json` publishes the promised full-run metrics plus per-case `holdout_exact_20`, `exact_certificate_present`, `risk_tags`, and the exact-hit split by `nondegenerate` (`28` degenerate rational baselines, `4` nondegenerate quadratic cases).
- `results/experiments/claim_sensitive_ablation.json` closes the key benchmark follow-ups from the earlier audit:
  - raising the order cap from `d <= 4` to `d <= 6` and `d <= 8` adds no new exact-certified case;
  - extending holdouts to `40/80/160` keeps the four certified quadratic-convergent cases stable;
  - the three plastic positive-density prefix fits fail by length `40`.

## What remains limited

- Several sparse quadratic holdout cases remain empirical only, even after the longer holdout pass: `phi/fib_indices`, `phi_minus_1/fib_indices`, `sqrt2/pell_indices`, and `one_plus_sqrt2/pell_indices` continue to satisfy their fitted recurrences through `160` samples but still lack structural certificates.
- The selector-template ablation around `quadratic_convergent_even` suggests that nearby quadratic convergent templates also carry exact holdouts, but those variants remain uncertified and must stay outside the theorem language.
- The nonquadratic negative evidence is still a named-example screen rather than a family theorem. The current controls (`plastic`, Salem quartic, `e`) are enough to block a broad Pisot-first narrative, not to prove a universal higher-degree impossibility result.

## Publication-quality claim limits

- Safe benchmark-backed claims: the periodic-gap rational lane; the four certified quadratic-convergent identities; the negative statement that the concrete beta-endpoint suffix-`10` construction does not rescue the higher-degree control panel.
- Not safe from benchmark evidence alone: any claim that the sparse irrational story is fully classified, that all quadratic selector variants are exact, or that higher-degree Pisot/Salem/transcendental families fail in general.
