# Verification Summary

Review phase: `review_round_1`

## Recommendation

**Decision: REVISE**

The current package is strong enough for a narrower paper centered on structural
cleanup of the public recurrence, proof of the public prime-separation observation,
reproducible finite-horizon computation, and negative evidence against the strongest
H1/H2 mechanism stories. It is not strong enough, as written, for broad novelty,
mechanism, robustness, or asymptotic claims.

## Must-Fix Issues

1. **Reduce the claim hierarchy to what the evidence actually supports.**
   Keep the contribution statement centered on:
   - exact structural consequences of the recurrence;
   - proof of prime separation from the recurrence;
   - digest-checked million-step computation;
   - negative witness/hypergraph evidence against compact-certificate and
     prime-support mechanism claims.
   Remove or explicitly downgrade claims about a new positive mechanism, a
   differentiated prime-support explanation, a clean theorem-level separation from
   Ford-style overlap, broad robustness, or any boundedness/unboundedness implication.

2. **Rewrite literature-positioning and novelty language as author judgment rather than source-proved fact.**
   The Ford, OEIS, and Kimberling citations support adjacency and provenance. They do
   not themselves prove statements such as "this is the correct overlap branch" or
   "reconstruction alone cannot be novel." Recast those passages as explicit internal
   assessment, or attach the internal novelty-analysis artifacts where that judgment is
   being made.

3. **Add direct artifact support at the first claim site for the main negative computational conclusions.**
   The core data exist, but abstract/introduction/discussion language currently outruns
   its sentence-level traceability. Add explicit references when first asserting:
   - composite-only late record gaps;
   - singleton-heavy witness behavior;
   - balanced-factor growth;
   - non-compression of the witness data;
   - failure of prime-support observables to explain record gaps.

4. **Fix the benchmark narrative around variants and robustness.**
   `row_immediate` is the baseline process and `column_immediate` is an axis swap, not
   independent robustness ablations. Remove any external-facing language that treats
   them as meaningful perturbation evidence, and align the paper and experiment notes
   with the identity/symmetry interpretation.

5. **Stop treating `results/research_context.md` as an authoritative literature ledger unless it is regenerated.**
   The citation audit found it stale relative to the Semantic Scholar manifest. Either
   regenerate it from the manifest or demote it to non-authoritative metadata.

6. **Clean up weak bibliography entries if they remain in scope.**
   Replace metadata-only placeholders with primary records where the manuscript still
   invokes generalized/restricted multiplication-table descendants or algorithmic
   multiplication-table comparisons.

## Optional Improvements

These are not necessary for a narrow revision, but they become necessary if the goal
is to restore a stronger mechanism or publication-quality benchmark story.

1. Add one independently written reference implementation and require agreement with
   the baseline contract through at least `10^5` steps.

2. Add genuine controls:
   - same-snapshot tie-rule control;
   - admissibility perturbation that changes coverage rules rather than update staging.

3. Benchmark against matched non-record windows and size-matched surrogate product
   sets or witness hypergraphs to test whether the observed structures are actually
   discriminative.

4. Recompute witness taxonomies from full hypergraphs for every late baseline record
   gap and late axis-swapped row-gap record under multiple canonicalizations.

5. Extend the H1/H2 summary tables to the later gaps already present in the corpus,
   especially baseline gaps `25`, `28`, and `30`.

6. Run a horizon sweep across fixed checkpoints to test whether offset, witness, and
   gap metrics stabilize or drift.

## Action-Oriented Bottom Line

Accept the current work only after revision to a narrower claim set. Do not present it
as a new mechanism paper or a publication-quality robustness package in its current
form. If the objective is a broader mechanism or benchmark claim, the correct next step
is not acceptance but deeper experimental work on controls, baselines, and
canonicalization invariance.
