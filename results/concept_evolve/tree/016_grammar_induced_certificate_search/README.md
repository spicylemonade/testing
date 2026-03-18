# grammar_induced_certificate_search
Use graph-grammar induction to search directly in the recursive language of constructible graphs instead of in flat adjacency lists. The goal is to mine reusable gluing productions that preserve forceability while compressing witness size and search branching factor.
## Domains
graph_grammars, program_synthesis, additive_combinatorics, cellular_automata
## Mathematical Sketch
Let P be a production system whose rules have the form H -> glue(H_0,...,H_k; theta), where theta records identified vertices and inserted X-labelled edges. Optimize L(P) = score(P) + lambda |P| over grammars whose generated graphs admit full forcing, using positive examples from successful motifs and negative examples from stalled motifs.
## Why This Bridge Might Matter
The novelty is to treat arithmetic Kakeya witnesses as a grammar-learning problem over proof-generating graph families, not as one-off graphs.
## Implementation Backlog
- Build: solver/grammar_state.py
- Build: solver/production_search.py
- Test: Seed the search with hand-designed low-depth constructions, induce productions, and test whether induced grammars regenerate the seeds and extrapolate to larger forceable graphs.
- Check: Prior grammar work aims to imitate observed graph distributions. Here the grammar is judged by exact forceability and score, so it is a proof-search object rather than a generative-model benchmark.
## Closest Prior Art
- Graph Grammar Induction (DOI:10.1016/bs.adcom.2019.07.003)
- Data-Efficient Graph Grammar Learning for Molecular Generation (arXiv:2203.08031)
- SAT-Based Generation of Planar Graphs (DOI:10.4230/LIPIcs.SAT.2023.14)
