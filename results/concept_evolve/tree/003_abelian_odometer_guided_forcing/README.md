# abelian_odometer_guided_forcing

## Topic context
View the evolving multiset of local relations as an abelian network with a preferred output letter corresponding to the target direction (1,-1). Use odometer-style least-action quantities and production-matrix summaries only to rank candidate motifs before exact verification.

Primary domains: abelian_networks, chip_firing, additive_combinatorics.

Mathematical sketch:
Associate to each candidate graph G a production matrix P and a relation-transport map \Phi_G: \mathbb{Z}^{|R|}\to \mathbb{Z}^{2|V|}. Define an odometer proxy u as the minimal nonnegative vector with \Phi_G(u)+R_0 reaching a target singleton basis direction. Use spectral and odometer summaries of P to prioritize candidates, then check exact legality with the original forcing rules.

Closest prior art:
- Abelian networks I. Foundations and examples (arXiv:1309.3445)
- Abelian networks II. Halting on all inputs (arXiv:1409.0169)
- Abelian networks III. The critical group (arXiv:1409.0170)

Novelty claim:
The new claim is narrowly predictive: abelian-network invariants may help locate low-score arithmetic Kakeya certificates without asserting an exact equivalence of models.

Differentiation:
This is not just renaming forcing as chip-firing. The contribution only survives if the imported invariants improve search quality after matching on ordinary linear-algebra descriptors.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
