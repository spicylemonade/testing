# Verification Summary

Review phase: `post_deepen`

## Recommendation

**Decision: REVISE**

The post-deepen package is strong enough for a narrower paper built around:

- proof-level cleanup of exact consequences of the public recurrence;
- proof of the public prime-separation observation from the recurrence;
- reproducible million-step computation with partial independent checking; and
- matched-control negative evidence against compact anchor/backbone, hypergraph, and
  modular mechanism stories.

It is still not strong enough, as written, for a broader novelty, mechanism,
robustness, or asymptotic pitch. Acceptance should be tied to revision into that
narrower claim set. If the goal is to keep the stronger mechanism or benchmark story,
the work needs further deepening after revision rather than acceptance now.

## Must-Fix Issues

1. **Reduce the claim set to the supported contribution boundary.**
   Keep the manuscript centered on structural cleanup, proof of prime separation,
   validated finite-horizon computation, and negative mechanism evidence. Remove or
   explicitly demote claims about:
   - a new positive mechanism for row-gap formation;
   - a promoted frontier certificate or hypergraph rigidity law;
   - a prime-support explanation of late records;
   - a clean theorem-level escape from Ford-style overlap; or
   - any progress claim on boundedness or unboundedness of `T(1,n+1) - T(1,n)`.

2. **Rewrite novelty and overlap language as internal assessment, not source-proved fact.**
   OEIS, Kimberling, Ford, and multiplicative-basis citations support provenance and
   adjacent comparison classes. They do not by themselves prove that Ford is the
   decisive novelty boundary or that reconstruction alone cannot be novel. Recast that
   language as author judgment and pair it with the internal novelty analysis where
   the paper makes those stronger conclusions.

3. **Fix sentence-level citation routing at the strongest claim sites.**
   The paper's quantitative claims are mostly correct, but the abstract, discussion,
   and conclusion still compress strong results without local artifact support. Add
   direct citations where the paper first asserts:
   - composite-only late record gaps and full-witness late-gap summaries;
   - anchor discrimination and failure of bounded-support generalization;
   - schedule AUROC versus the length baseline;
   - prefix-depth obstruction values;
   - hypergraph near-miss and matched-control overlap;
   - nonpredictive modular-locking results; and
   - the axis-swapped `31` claim, if that sentence remains.

4. **Repair the benchmark narrative around variants, controls, and evidence routing.**
   `row_immediate` is the baseline process and `column_immediate` is the axis swap.
   They cannot be presented as independent robustness ablations. Update the
   manuscript, experiment notes, and final-status language so every computational
   claim routes to a current post-deepen artifact rather than to stale small-corpus
   summaries.

5. **Either justify the headline witness-taxonomy statements from full-pair artifacts or weaken them.**
   The full-hypergraph audit improved the evidence base, but some headline witness
   narratives still depend on first-witness bookkeeping. If singleton-share,
   balanced-share, or cycle-rank language remains in the main claim spine, back it
   with full-pair / multi-canonicalization artifacts at the sentence where it is
   asserted. Otherwise, downgrade those statements to exploratory observations.

6. **Stop treating stale literature metadata as authoritative.**
   `results/research_context.md` is stale relative to the current manifest and should
   be regenerated or explicitly demoted to non-authoritative metadata. Clean up weak
   bibliography placeholders if they remain in scope after the claim set is narrowed.

## Optional Improvements

These are not required for a narrow revision. They become necessary if the project
wants to restore a stronger mechanism or publication-quality benchmark claim.

1. Extend the independent checker to the full `10^6` horizon and require exact
   agreement on row/column terms, record-gap locations, and matched-window exports.

2. Add at least one genuinely nearby admissibility or tie-rule control that preserves
   a substantial baseline prefix while changing coverage decisions.

3. Recompute the headline witness taxonomy from full witness-pair sets across the
   whole phase-6 record/control corpus under at least two canonicalizations.

4. Replace or augment the affine surrogates with a harder size- and
   factor-budget-matched surrogate family.

5. Run the core mechanism-style metrics at fixed checkpoints such as `10^5`,
   `3 x 10^5`, `10^6`, and `3 x 10^6` to test whether the current finite-horizon
   conclusions drift.

6. Expand the evidence ledger so each H1/H2 and final-status statement points to one
   current authoritative post-deepen artifact.

## Bottom Line

The correct disposition is **REVISE**. The package now supports a concrete, narrower
paper with audited negative results, but it does not support the broader novelty and
mechanism rhetoric in its current form. Revise first; deepen only if the goal is to
recover stronger mechanism, robustness, or asymptotic claims.
