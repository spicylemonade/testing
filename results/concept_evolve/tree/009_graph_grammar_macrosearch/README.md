# graph_grammar_macrosearch

## Topic context
Treat constructible graphs as a graph-grammar search space rather than as flat combinatorial objects. Learn or hand-design a small production system whose derivation trees already respect the user's recursive construction law, then search over that grammar with exact score extraction at each node.

Primary domains: graph_grammars, program_synthesis, combinatorial_search.

Mathematical sketch:
Let \Gamma be a grammar whose productions rewrite typed interface graphs into larger typed interface graphs. Each derivation tree D\in\mathcal{L}(\Gamma) maps to a legal constructible graph G(D). Search \Gamma for D minimizing S(G(D),R(D),T(D)) subject to exact extractability of R(D),T(D).

Closest prior art:
- Graph grammar induction (DOI:10.1016/bs.adcom.2019.07.003)
- RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design (DOI:10.1145/3414685.3417831)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

Novelty claim:
The novelty is a parser-controlled search over exact arithmetic Kakeya certificate grammars, not graph grammar induction in general.

Differentiation:
Unlike generic graph-grammar work, every derivation must decode to a legal witness in the user's certificate format. That verifier coupling is the part that makes the bridge nontrivial.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
