# long_running_hyperedge_forcing
Derive a hypergraph whose hyperedges encode sufficient support patterns for anti-diagonal forcing, then deliberately search for long-running spanning processes. The hypothesis is that sparse but deep infection chains may recycle the same few edges many times and therefore beat denser, faster constructions on score.
## Domains
hypergraph_percolation, cellular_automata, additive_combinatorics
## Mathematical Sketch
Let H_F have vertex set V(G) and hyperedges S -> e whenever there exists a local linear derivation that forces e from support contained in S union {e}. For a seed set A, let tau_H(A) be the number of rounds until closure; optimize score(G,R,T) while preferring larger tau_H(A) under the constraint cl_H(A) = V.
## Why This Bridge Might Matter
The novelty is to treat infection time as a positive design feature for arithmetic Kakeya witnesses rather than as a complexity nuisance.
## Implementation Backlog
- Build: solver/dependency_hypergraph.py
- Build: solver/infection_time.py
- Test: On fixed small X, enumerate candidate graphs and compare score against derived hypergraph infection time to test whether longer-running instances systematically have better edge-to-coverage ratios.
- Check: The hypergraph papers study generic closure systems. Here the hyperedges come from exact integer-linear forcing semantics and are only a derived abstraction to guide witness search.
## Closest Prior Art
- On the Running Time of Hypergraph Bootstrap Percolation (arXiv:2206.02940)
- The maximal running time of hypergraph bootstrap percolation (DOI:10.1137/22M151995X)
- Linear algebra and bootstrap percolation (arXiv:1107.1410)
