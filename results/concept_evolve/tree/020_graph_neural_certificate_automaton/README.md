# graph_neural_certificate_automaton
Train a graph cellular automaton to propose promising edge-label layouts, slope alphabets, and seed masks on constructible grids. The learned model is only a proposer; exact forceability is still checked by a symbolic verifier, but the proposal prior can drastically shrink the discrete search space.
## Domains
graph_machine_learning, cellular_automata, combinatorial_optimization
## Mathematical Sketch
Let h_e^{t+1} = phi(h_e^t, Agg_{e_prime ~ e}(h_{e_prime}^t, ell_{e,e_prime})) be a graph-CA update on a candidate constructible graph. A decoder predicts edge labels, X-membership, and seed masks; train with loss L = surrogate_unforced + lambda score_proxy + mu verifier_disagreement.
## Why This Bridge Might Matter
No cited paper targets exact combinatorial proof certificates; the new piece is using graph NCA as a learned prior over AK witness space while keeping verification symbolic.
## Implementation Backlog
- Build: solver/gnca_model.py
- Build: solver/proposal_sampler.py
- Test: Train on tiny 2-layer and 3-layer grids, then evaluate whether the learned proposer improves verifier hit rate on larger held-out grids relative to random or hand-crafted proposals.
- Check: This is not claiming that a neural CA proves the theorem by itself. The network only proposes candidate local structures that are then audited by the exact arithmetic-Kakeya verifier.
## Closest Prior Art
- Learning Graph Cellular Automata (arXiv:2110.14237)
- Variational Neural Cellular Automata (arXiv:2201.12360)
- HyperNCA: Growing Developmental Networks with Neural Cellular Automata (arXiv:2204.11674)
