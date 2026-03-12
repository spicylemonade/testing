# Falsifier Controls

## Rational-triviality
- Checked on the same frozen panel and exact checker outputs in `results/experiments/full_panel_results.json`.
- Exact rational positives remain confined to denominator-compatible arithmetic progressions (7 cases).
- Verdict: pass. The pipeline does not mistake rational baseline cases for novelty.

## Sparse-subsequence leakage
- Zero-density survivors are quarantined as `sparse_subsequence_leak` (13 cases), not promoted to theorem status.
- Representative cases: `phi` on `fib_indices`, `phi` on `ost_single_nonzero_digit`, `sqrt2` on `pell_indices`, `one_plus_sqrt2` on `pell_indices`.
- Verdict: pass. The same selector families, slopes, and moduli are reused; sparse candidates are explicitly demoted.

## Prefix fitting
- Prefix-only cases remain labeled `prefix_fit` (19 cases) or `selector_shadow_failure` (7 cases).
- Representative failure cases: plastic on `union_mod3_01` stays `prefix_fit`; plastic on `ap_2_0` and `ap_3_1` collapse to `selector_shadow_failure`.
- Verdict: pass. Long exact holdout plus modular replay suppresses convergent-driven mirages.

## Word/value confusion
- Controlled by `results/definition_lock.md`: symbolic recurrence never counts unless mapped back to an exact numeric recurrence of `floor(n_k r)`.
- The full panel runner uses only numeric selectors and exact integer value checks.
- Verdict: pass.

## Set/sequence confusion
- Controlled by the same definition lock and by the novelty files: Beatty-set membership or generalized-Beatty constructions are not counted unless the ordered sampled values satisfy the recurrence.
- Verdict: pass.

## Failed controls
- None in the current frozen replay. All risky cases were downgraded rather than promoted.