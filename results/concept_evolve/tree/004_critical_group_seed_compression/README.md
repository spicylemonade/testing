# critical_group_seed_compression

## Topic context
Focus the abelian-network bridge on the seed term r rather than on dynamics alone. Compute Smith-normal-form style invariants of the extracted relation lattice to remove seed generators that are redundant modulo the critical subspace, directly targeting the score numerator.

Primary domains: algebraic_graph_theory, chip_firing, automated_search.

Mathematical sketch:
Given a compiled candidate with relation lattice L_G \subseteq \mathbb{Z}^{2|V|}, solve \min |R_0| subject to \forall v\in V,\ (1,-1)e_v \in \operatorname{span}_{\mathbb{Z}}(L_G\cup R_0) and each generator in R_0 has singleton support drawn from X. Use Smith normal form of \mathbb{Z}^{2|V|}/L_G to expose residue classes that require explicit seeding.

Closest prior art:
- Abelian networks III. The critical group (arXiv:1409.0170)
- On the arithmetic Kakeya conjecture of Katz and Tao (arXiv:1712.02108)
- Bounds on arithmetic projections, and applications to the Kakeya conjecture (Math. Res. Lett. 6 (1999) 625-630)

Novelty claim:
The new element is an explicit algebraic compression objective for seed sets in arithmetic Kakeya certificates, driven by quotient-lattice structure rather than by ad hoc pruning.

Differentiation:
Critical groups are classical; what is not classical is optimizing the exact verifier score by using quotient-lattice information to compress singleton seeds under the user's legality rules.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
