# thickness_monotone_pruner

## Topic context
Import Gacs-style thickness as a structural quality functional for partial certificates. Instead of claiming the Kakeya forcing system is a Toom rule, use thickness gain as a pruning statistic that filters motifs before exact linear-algebra extraction.

Primary domains: cellular_automata, dynamical_systems, additive_combinatorics.

Mathematical sketch:
Define a thickness surrogate \Theta(A,T) on partially solved sets A\subseteq V by penalizing narrow bottlenecks and disconnected active shells. Prefer candidate local rules with \Theta(A_{t+1},T_t)-\Theta(A_t,T_t) \ge \delta>0 for most reachable states, then verify whether large \Theta correlates with low extracted score S.

Closest prior art:
- A Toom rule that increases the thickness of sets (DOI:10.1007/BF01015567)
- Universality for two-dimensional critical cellular automata (arXiv:1406.6680)
- Sum-difference exponents for boundedly many slopes, and rational complexity (arXiv:2511.15135)

Novelty claim:
The novelty is not a new Toom-type theorem. It is the use of a thickness-like invariant as an explicit pruning functional for exact arithmetic certificate search.

Differentiation:
No prior paper above optimizes or even defines arithmetic Kakeya score through a thickness surrogate. If the surrogate fails empirically, the concept should be dropped rather than inflated into a broader CA claim.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
