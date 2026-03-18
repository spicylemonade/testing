# affine_ca_negative_filter
Use negative results about affine cellular automata to prune search families that are too linear to isolate anti-diagonal residue effectively. The idea is to reserve nonlinearity for thresholded forcing decisions or grammar-level branching, rather than wasting time on affine surrogates that are structurally incapable of rich behavior.
## Domains
automata_theory, cellular_automata, search_pruning, additive_combinatorics
## Mathematical Sketch
If a surrogate update rule U on local states is affine over F_p, then the reachable configuration family remains in an affine closure C_U. Reject any surrogate family whose invariants imply that isolated anti-diagonal detection cannot break out of C_U; require a nonlinear gate g(M_e) = 1[(1,-1) intersects M_e nontrivially] or grammar-level branching to enter the search space.
## Why This Bridge Might Matter
The new contribution is methodological: use automata-theoretic impossibility results to shape the certificate-search model class before optimization begins.
## Implementation Backlog
- Build: solver/affine_filter.py
- Build: solver/rule_classification.py
- Test: Ablate search with and without the affine-family filter, and measure whether rejected families indeed fail to produce complete forcing on small exact instances.
- Check: This is not a theorem claiming AK witnesses cannot arise from affine dynamics. It is a practical search prior that treats affine limitations as a reason to bias architecture and grammar design.
## Closest Prior Art
- Simulation Limitations of Affine Cellular Automata (arXiv:2311.14477)
- Regional Controllability of Cellular Automata as a SAT Problem (arXiv:2504.03691)
- U-bootstrap percolation: Characterizations and metastability (arXiv:1806.11405)
