# Falsifier Controls

## Rational-triviality
- Checked on the same frozen panel and exact checker outputs in `results/experiments/full_panel_results.json`.
- Exact rational positives now occupy the full eventually-periodic-gap AP/FUAP lane (28 cases), and every one carries the `rational_triviality` tag rather than being counted as novelty.
- Rational sparse selectors still generate 5 long exact leaks, but they remain classified as post-selection artifacts and never enter the theorem-backed lane.
- Verdict: pass.

## Sparse-subsequence leakage
- The 20-term screen still quarantines 12 rows as `sparse_subsequence_leak`; none is promoted without an infinite certificate.
- The revision holdout extension in `results/experiments/claim_sensitive_ablation.json` runs all 15 `uncertified_exact_holdout` rows to length `320`: 11 still survive exactly and remain leaks, while `salem_quartic / ost_suffix_001` breaks at `80`.
- Representative surviving leaks: `phi / fib_indices`, `phi / ost_single_nonzero_digit`, `sqrt2 / pell_indices`, and `one_plus_sqrt2 / pell_indices`.
- Verdict: pass.

## Prefix fitting
- Prefix-only positives are now confined to the 3 plastic positive-density rows `ap_1_0`, `union_mod3_01`, and `union_mod6_013`.
- All 3 fail by holdout length `40` in `results/experiments/claim_sensitive_ablation.json`, so none survives the strengthened follow-up.
- Verdict: pass.

## Word/value confusion
- Controlled by `results/definition_lock.md`: symbolic recurrence never counts unless it compiles back to an exact numeric recurrence of `floor(n_k r)`.
- The full panel runner uses only numeric selectors and exact integer value checks.
- Verdict: pass.

## Set/sequence confusion
- Controlled by the same definition lock and by the curated comparison files: Beatty-set membership or generalized-Beatty constructions are not counted unless the ordered sampled values satisfy the recurrence.
- The revision keeps the AP/FUAP theorem lane and the sparse empirical lane separate rather than rephrasing either one as an unordered-set statement.
- Verdict: pass.

## Failed controls
- None in the theorem-backed lane.
- The remaining empirical leaks are explicitly documented in `results/experiments/claim_sensitive_ablation.md` and `results/experiments/evaluation_memo.md` instead of being promoted to broader claims.
