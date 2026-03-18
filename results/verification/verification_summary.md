# Verification Summary

Phase: `review_round_1`

## Decision

**Disposition: REVISE**

The current artifact set supports a narrow, benchmark-safe negative result, not a broader novelty or benchmark claim. The safe core is:

- `H1_macrocell_substitution` is killed by an exact one-seed obstruction.
- `H2_target_direction_abelian` shows no lift on the tiny tested family set.
- direct no-CA corridor controls remain around score `2.0` and look fragile under the saved ablations.

This should be revised now rather than deepened immediately. The blocking issues are overclaiming, citation mismatches, and scope drift. A deeper experimental pass is only needed if the team still wants a stronger benchmark or broader novelty position.

## Must-Fix Issues

1. Reframe the contribution to match the verified evidence.
   - Present the work as an exact benchmark-and-falsification artifact inside the existing finite-certificate arithmetic-Kakeya setting.
   - Treat the width-2 corridor verifier theorem and the one-seed obstruction theorem as corridor-local contributions, not a new framework, new arithmetic-Kakeya theorem line, or general mechanism.
   - Remove or explicitly reject claims of a successful CA mechanism, useful abelian-network mechanism, decoder-style route, or broader verifier-first reformulation.

2. Tighten the benchmark section to the publication-safe scope.
   - Limit the supported benchmark claim to: exact H1 failure before scoring, no H2 lift on the tested family IDs, and direct corridor controls that stay around `2.0`.
   - Replace language such as "does not scale," "plateau," or matched level-2 failure with narrower wording like "no clean transfer was found in the saved frozen-`X` bounded search."
   - Keep bounded-slope / low-rational-complexity discussion as interpretation or consistency language, not as a measured in-repo fact.

3. Fix the citation problems that currently break claim-to-source alignment.
   - Add explicit provenance for the `1.675` target and `1.70` threshold. Use `epochai2025arithmetickakeya` plus repo-local planning artifacts if those numbers stay in the paper.
   - Remove or properly source the width-8 boundary-stress `0/16` claim. The current ablation citation does not support it.
   - Either cite or export the exact H1 identity representative, or weaken that prose to the level supported by the saved H1 program and obstruction artifacts.
   - Replace the false-positive prior-art citation with the actual prior-art watchlist / gap artifacts.
   - Drop or properly source the setup/runtime/seed details if they remain.

4. Clean up bibliography hygiene before paper-facing reuse.
   - Fix concrete metadata issues such as the `pohoata2024` author entry.
   - Normalize mixed preprint/journal metadata where needed.
   - Verify stronger frontier-history and comparison citations before keeping those statements.

5. Keep empirical claims locally qualified.
   - H2 claims must stay scoped to the tested four-family set.
   - Ablation claims must stay scoped to the saved width-4 witness and tiny randomized samples.
   - Width-8 comparisons should stay exploratory unless matched controls are added.

## Optional Improvements

1. Add the missing matched level-2 direct control if a stronger benchmark claim is still desired.
   - Run a true `2 x 8` direct no-CA comparator with the same 4-nonzero same-sum `X`, `boundary_band`, and matched budgets.
   - Report frontiers over at least `{20, 50, 200}` trials and multiple RNG seeds.

2. Execute the missing pre-registered non-CA baselines.
   - `baseline_low_height_asymmetric_X`
   - `baseline_bounded_slope`
   - `baseline_slowly_growing_X`
   These are needed only if the paper wants to argue that the CA route is specifically uncompetitive rather than the whole fixed-`X` corridor regime being weak.

3. Deconfound and expand the ablation program.
   - Re-run frozen-`X` scaling under the same budgets as the base direct rows.
   - Expand `randomize_R`, `randomize_T`, and `randomize_X` beyond the current tiny samples.
   - Add at least one `H=3` aspect-ratio row.
   - Run a true exact-elimination replacement comparator.
   - Split width-8 boundary stress into matched 3-nonzero and 4-nonzero sweeps.

4. Improve auditability of the raw traces.
   - Log per-trial verifier outcome, failure reason, score, `seed_budget`, `initial_t_budget`, `boundary_band`, `|X|`, active-state count, grammar length, and search-budget usage.
   - Report seed-aggregated frontiers instead of only single-seed best-of-run traces.

5. Broaden the H2 screen only if H2 remains active as a route.
   - Evaluate H2 over the full saved direct-search archive.
   - Include a true matched width-8 direct control.
   - Compare ranking and retention against raw arithmetic features, not only the current four family IDs.

## Actionable Bottom Line

Choose **REVISE** for this round. The draft can be made internally consistent by narrowing the claims, repairing the citation boundaries, and keeping every empirical statement at the scope actually supported by the saved artifacts. Choose **DEEPEN** only if the goal shifts to a stronger benchmark or broader novelty claim than the current evidence can carry.
