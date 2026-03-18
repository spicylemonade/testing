# egraph_slope_identity_engine
Use e-graphs to discover reusable rewrite rules among slope expressions and local forcing lemmas. This compresses repeated linear manipulations across many candidate certificates and can suggest which low-complexity slopes are worth inserting into X.
## Domains
symbolic_rewriting, additive_combinatorics, program_synthesis
## Mathematical Sketch
Build a DSL whose terms denote expressions obtained from singleton seeds, edge differences, and eliminations modulo forced support. Equality saturation maintains an e-graph of equivalent slope expressions, and a cost model C(term) rewards short derivations of a(1,-1) at target vertices.
## Why This Bridge Might Matter
The concept is new because it applies equality saturation to arithmetic Kakeya local proof algebra, turning hidden linear identities into searchable reusable lemmas.
## Implementation Backlog
- Build: solver/slope_dsl.py
- Build: solver/egraph_rules.py
- Test: Collect exact derivations from tiny forceable instances, infer rewrite rules, and measure whether search branching shrinks on held-out instances with the learned rule set enabled.
- Check: This is not a reimplementation of compiler-oriented e-graph work. The e-classes represent forcing obligations and slope identities, and the output is a smaller exact proof search space.
## Closest Prior Art
- Rewrite Rule Inference Using Equality Saturation (arXiv:2108.10436)
- Sum-difference exponents for boundedly many slopes, and rational complexity (arXiv:2511.15135)
- Generalized Arithmetic Kakeya (arXiv:2411.13395)
