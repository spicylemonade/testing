# ultracompact_rule_minification

## Topic context
Regularize the search toward tiny rule descriptions, tiny interface alphabets, and tiny slope sets, then see which compact motifs still survive exact extraction. This treats compactness as an engineering bias for discovering reusable modules rather than as a theorem about arithmetic Kakeya itself.

Primary domains: compressed_models, cellular_automata, automated_theorem_search.

Mathematical sketch:
Minimize a description-length objective DL = DL(\rho)+DL(X)+DL(\mathcal{I}) subject to S_{\mathrm{extract}}(\rho,X,\mathcal{I}) \le \tau. Search the Pareto frontier between extracted score, rule-table size, and interface complexity.

Closest prior art:
- muNCA: Texture Generation with Ultra-Compact Neural Cellular Automata (arXiv:2111.13545)
- CAX: Cellular Automata Accelerated in JAX (arXiv:2410.02651)
- Differentiable Logic Cellular Automata: From Game of Life to Pattern Generation (arXiv:2506.04912)

Novelty claim:
The bridge is new only if description-length pressure helps discover exact arithmetic certificates that would be hard to find by unconstrained search.

Differentiation:
This is not texture compression and not just small-model enthusiasm. Compactness is valuable here only as a search prior for exact witness structures.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
