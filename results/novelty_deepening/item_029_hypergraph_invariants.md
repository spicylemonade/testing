# Item 029: Full-Witness Hypergraph Audit

## Candidate Invariants Checked

- full-graph cycle rank
- full/lex/balanced leaf fraction
- full/lex/balanced description length per skipped value
- full/lex/balanced component, edge, and vertex counts

## Strongest Surrogate Separator

- Best candidate by surrogate failure rate: `balanced_graph.leaf_fraction`.
- Record range: `0.9473684210526315` to `0.9811320754716981`.
- Surrogate windows outside that record range: `1.000`.
- Matched non-record windows still inside that record range: `0.289`.

## Canonicalization Stability

- Maximum lex-vs-balanced description-density gap on the true record windows: `0.083`.
- Maximum lex-vs-balanced leaf-fraction gap on the true record windows: `0.023`.

## Verdict

No candidate invariant currently clears the full item-029 gate.

1. The strongest surrogate separators are canonical-tree description density and related size counts, but they also overlap heavily with the matched non-record windows. They therefore describe anchored covered intervals in general, not true record formation.
2. The genuinely full-witness invariant `cycle_rank = 0` is stable across all true record windows, but it also holds on the surrogate family and so does not survive the Ford-style control.
3. The chosen-canonicalization metrics are stable across lexicographic and balanced selections, but their surrogate separation is entangled with the affine surrogate undercoverage rather than with a record-specific rigidity law.

## Conclusion

Item 029 should close as a failed positive search: the corpus supports a tree-like full witness graph, but no invariant found so far is both canonicalization-stable and genuinely specific to true record windows rather than to the broader anchored-coverage geometry.
