# product_graph_percolation

## Context
The product frontier induces a highly heterogeneous divisor-incidence network: integers are covered when some left-right divisor pair activates them. This card studies record gaps as a percolation or matching phenomenon on that arithmetic graph rather than as a raw sequence problem.

## Mathematical Sketch
For each x \le X define E_x = \{(r,c)\in R_n\times C_n : rc=x\}. Coverage of x means E_x\neq\emptyset. Aggregate the E_x into a bipartite divisor graph with degree distribution inherited from divisor counts and analyze consecutive covered blocks via branching or matching heuristics.

## Why This Bridge Might Matter
The novelty is to regard consecutive integer coverage as a heterogeneous bipartite activation problem whose edges come from divisor arithmetic, not from a random graph generator.

## Implementation Backlog
- analysis/divisor_graphs.py
- data/record_gap_graph_features.json
- notes/percolation_model.md

## Starting Experiment
For each record gap interval, compute degree statistics of the covering witness graph and compare against shuffled and configuration-model baselines.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- An optimal algorithm for on-line bipartite matching (openalex:W2162656786)
- Random graphs with arbitrary degree distributions and their applications (openalex:W2169015768)
- The multiplication table problem for bipartite graphs (openalex:W2487318500)
