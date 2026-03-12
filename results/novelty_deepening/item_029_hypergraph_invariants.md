# Item 029: Full-Witness Hypergraph Audit

## Candidate Invariants Checked

- full-graph cycle rank
- full/lex/balanced leaf fraction
- full/lex/balanced description length per skipped value
- full/lex/balanced component, edge, and vertex counts

## Eliminated Candidate

- The truly full-witness Betti/forest story collapses to `cycle_rank = 0` everywhere: on records, controls, and surrogates the factor graph is a forest.
- So the first cycle-rank / arboricity pass is structurally true but not discriminative.

## Strongest Near-Miss

The strongest surviving near-miss is the canonical-forest leaf fraction derived from the full witness hypergraph under two canonicalizations.

- Balanced record band: `[0.9473684210526315, 0.9811320754716981]`.
- Lexicographic record band: `[0.9444444444444444, 0.9807692307692307]`.
- Balanced surrogate failure rate: `1.000`.
- Lexicographic surrogate failure rate: `0.960`.
- Balanced record-vs-control AUROC: `0.871`.
- Lexicographic record-vs-control AUROC: `0.816`.
- Balanced matched-control overlap inside the record band: `0.289`.
- Maximum lex-vs-balanced leaf-fraction gap on the true record windows: `0.023`.

## Verdict

No candidate invariant currently clears the full item-029 gate.

1. The invariant is derived from the full hypergraph, not from first-witness bookkeeping: every window starts from the full witness pair set and then projects to two canonical spanning forests.
2. The balanced and lexicographic canonicalizations agree to within a leaf-fraction gap of at most `0.023` on every true record window through `10^6`, and they do reject at least `96%` of the affine size-matched surrogate windows.
3. That is still not enough for a credible `T`-specific rigidity law here: about `28.9%` of the matched non-record windows remain inside the balanced record band, and the current affine surrogate family is undercovered enough that surrogate separation alone is too weak to justify promotion.

## Conclusion

Item 029 should close as a failed positive search. The canonical-forest leaf fraction is the best near-miss found so far, but it remains a descriptive overlap metric rather than a credible `T`-specific full-witness invariant.
