# anisotropic_droplet_compiler

## Topic context
Treat a candidate forcing pair as a deterministic anisotropic bootstrap-percolation rule on the product grid underlying the constructible graph. The CA is only a proposer: once a droplet grows across the grid, an exact extractor converts the growth history into legal edge relations and seed generators, then measures the true score.

Primary domains: additive_combinatorics, bootstrap_percolation, statistical_physics.

Mathematical sketch:
Choose an update family \mathcal{U}_X on V = [d_1]\times\cdots\times[d_k]. A site v becomes active if there exists a local pattern P\in\mathcal{U}_X with P+v \subseteq A_t. Compile A_\infty into a relation lattice L(A_\infty)\subseteq \mathbb{Z}^{2|V|}, and accept only if \forall v\in V,\ (1,-1)e_v \in \operatorname{span}_{\mathbb{Z}}(L(A_\infty)\cup R_0) with support constraints respected. Optimize S=(m+r)/(n-t).

Closest prior art:
- Universality for two-dimensional critical cellular automata (arXiv:1406.6680)
- Sharp Metastability Threshold for Two-Dimensional Bootstrap Percolation (arXiv:math/0206132)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

Novelty claim:
The new step is to compile anisotropic droplet growth into exact arithmetic Kakeya certificates, rather than using bootstrap percolation only as an analogy or threshold theorem.

Differentiation:
This is not a reimplementation of universality or metastability results because the objective is not a threshold or infection time. The search target is an exact legal witness minimizing (m+r)/(n-t), with extraction constraints that percolation papers do not address.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
