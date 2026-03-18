# rational_complexity_slope_curriculum
Use rational complexity as a curriculum variable for the slope set X and for when new labels are allowed to enter the local automaton. The search begins with low-complexity slopes that support many cheap local identities, and only expands X when the current CA dynamics provably stalls.
## Domains
additive_combinatorics, curriculum_learning, cellular_automata
## Mathematical Sketch
Let kappa(x) be a rational-complexity penalty on nonzero x in X. Search over nested alphabets X_0 subset X_1 subset ... with objective score(G,R,T) + beta sum_{x in X} kappa(x); permit the transition X_j -> X_{j+1} only after the local closure operator on X_j reaches a fixed point without full forcing.
## Why This Bridge Might Matter
The new idea is to convert rational complexity from an analytic descriptor into a concrete control knob for certificate search and CA alphabet growth.
## Implementation Backlog
- Build: solver/rational_complexity.py
- Build: solver/curriculum_scheduler.py
- Test: Compare unrestricted slope mutation against the curriculum on identical beam-search budgets, and track score, number of unique local lemmas, and verifier success rate.
- Check: The math papers study rational complexity analytically; the self-organization paper studies open-ended exploration. This concept merges them into an exact search prior for AK witnesses.
## Closest Prior Art
- Sum-difference exponents for boundedly many slopes, and rational complexity (arXiv:2511.15135)
- Generalized Arithmetic Kakeya (arXiv:2411.13395)
- Intrinsically Motivated Discovery of Diverse Patterns in Self-Organizing Systems (arXiv:1901.10857)
