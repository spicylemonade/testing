# Verification Summary

Review round: `review_round_1`.

## Decision

- `REVISE`
- The package is not ready to accept as currently written, but it does not need a new wide verification sweep if the claims are narrowed to the evidence already in hand.

## Must-Fix Issues

- Rewrite the contribution hierarchy so the only clear novelty-bearing theorem is the periodic-gap characterization for ordered Beatty-value recurrences under frozen eventually periodic-gap selectors.
- Demote the supporting lemmas, the modular-shadow pipeline, the four `quadratic_convergent_even` identities, and the `quadratic, not broad Pisot` point to supporting roles: proof infrastructure, methodology, exact examples, and falsifier/scope discipline.
- Remove or soften unsupported language in the paper and claim memo: no quadratic-family boundary, no periodic-CF boundary, no zero-intercept-specific claim, no all-positive-density-selector phrasing, and no workflow-level theorem claim for the modular-shadow layer.
- Separate evidence levels explicitly in outward-facing text: proved theorem, exact-certified examples, and empirical holdouts/diagnostics should not be blended into one contribution list.
- Add formal BibTeX/software citations for Walnut and Pecan if they remain in the final package, and cite curated gap notes/branch rows rather than the raw lexical watchlist.

## Optional Improvements

- If the authors want to keep a broader sparse-irrational narrative, deepen the benchmark with intercept controls `floor(n r + beta)`, continued-fraction-prefix-matched nonquadratic controls, exhaustive long holdouts for all `uncertified_exact_holdout` rows, `fit_length` ablations, and a larger nonquadratic control bank.
- Analyze the strongest unresolved anomaly cases, especially `salem_quartic / ost_suffix_001`, and explain why `quadratic_convergent_even` certifies while nearby Ostrowski selectors on `phi` and `phi_minus_1` remain leakage cases.
- Strengthen calibration/error analysis before presenting screening metrics such as `false_positive_rate = 0.0` as publication-grade evidence.

## Publication-Safe Framing

- Safe now: the periodic-gap theorem for eventually periodic-gap selectors, the rational AP/FUAP baseline lane, and the four exact-certified `quadratic_convergent_even` identities as isolated constructions.
- Not safe now: five co-equal novelty claims, a quadratic-only family theorem, a periodic-CF theorem, a zero-intercept theorem, or a broad novelty claim for the modular-shadow workflow.

## Action Path

- Preferred path: revise the manuscript/package to match the supported claim boundary and clean up citations.
- Only choose `DEEPEN` instead if the goal is to preserve the broader sparse/quadratic narrative rather than narrow it.
