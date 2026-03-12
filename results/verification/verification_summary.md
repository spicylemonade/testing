# Verification Summary

## Decision

**REVISE**

The current package should not be accepted in its present framing as a new mechanism
or publication-quality robustness package. The verification reports do support a
narrower contribution: a validated computational baseline plus negative mechanistic
evidence, with the boundedness question still unresolved.

## Must-Fix Issues

1. **Reframe the contribution statement.**
   Remove or explicitly retract claims that the package has established:
   - a new frontier certificate;
   - a differentiated prime-support mechanism;
   - a theorem-level explanation of the gap process.
   The defensible framing is: validated recurrence implementation, reproducible
   finite-horizon evidence, rejection of the strong raw-witness H1 story, and a
   documented overlap risk with the Ford divisor/product-coverage branch.

2. **Attach sources at the claim site.**
   The final notes currently route support through a coarse source matrix. Add direct
   citations to the exact local artifacts used for empirical claims, especially:
   - `results/experiments/run_1000000/contract.json`
   - `results/experiments/variant_comparison.md`
   - `results/analysis/h1_h2_gap_summary.json`
   - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
   Keep bibliography citations for provenance and literature comparison, not for local
   experiment outputs.

3. **Tighten the Ford overlap language.**
   The current writeup overstates the Ford comparison relative to the citation support.
   Either cite the exact Ford results being invoked or soften the language to
   heuristic overlap risk / resemblance. The present record supports an overlap
   concern, not a theorem-backed equivalence.

4. **Enforce the benchmark claim boundary.**
   State plainly that the benchmark package supports finite-horizon negative-result
   claims only. It does not yet support:
   - asymptotic boundedness or unboundedness claims;
   - a T-specific mechanism separated from generic local divisor/product coverage;
   - broad robustness under nearby perturbations;
   - performance conclusions beyond one-off observational logs.

## Optional Improvements

- Add one independently written reference implementation and require agreement with
  the baseline through at least `10^5` steps.
- Repeat the `10^6` baseline and perturbation runs with structural digests so the
  large-horizon package is not effectively single-run.
- Add the two missing controls: a same-snapshot tie-rule variant and an admissibility
  perturbation.
- Benchmark record-gap metrics against matched non-record windows and size-matched
  surrogate product sets.
- Export full witness hypergraphs for all late baseline and perturbation record gaps,
  then rerun witness-taxonomy summaries without chosen-witness bias.
- Remove or properly source the uncited cross-domain comparison block in
  `results/evaluation/literature_comparison.md`.
- Replace the metadata-only bibliography placeholders for the Koukoulopoulos and Brent
  entries with primary records.

## Recommended Positioning

Present the current work as a reproducible computational and negative-result dossier.
If the goal remains an external-facing mechanism paper, do the revision above first and
then deepen with the missing controls and surrogate baselines before making stronger
claims.

## Status

The mathematical status remains **still unresolved**. The current evidence is strong
enough to reject the original compact-certificate optimism and to document the
finite-horizon record-gap behavior more carefully, but not strong enough to establish a
distinct positive mechanism or an asymptotic conclusion.
