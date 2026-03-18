# H Causal-Cone Hypergraph CA 668

This branch operates on the retained composite actuator library from `results/analysis/composite_packet_retained_library.json`, not on the original one-packet H1 basis.

## State And Locality

- Nodes are the `9` retained composite actions.
- State is the exact retained-library quotient:
  - `512` unique packet-parity states reachable from the canonical frontier seed by XOR-combining the retained composites.
  - every transition is precomputed exactly from packet parity, so the runtime never rescans the original `334` packet basis.
- Pairwise locality is defined by changed-lag overlap between retained actions.
- Hypergraph locality is defined by bounded-arity `2`-step causal cones:
  - a hyperedge `(a, b)` is allowed only when `a` and `b` overlap on changed lags and their union stays inside the retained low-splash envelope.

## Fixed Rule

- Pairwise baselines:
  - `pairwise_graph_ca`
  - `zero_coupling`
  - `zero_refractory`
  - `scorer_only`
- Hypergraph rule:
  - evaluate every precomputed `2`-step causal cone rooted at the current local neighborhood
  - accept the full cone as one macro-update only if its end state strictly improves the current lexicographic objective
  - keep one-step refractory on the last cone endpoint

## Canonical Frontier Result

- Seed: `results/frontier/order_668_64m/seed_sequences.json`
- Best single-action baseline result:
  - `13 / 2880 / 512`
- Hypergraph result:
  - one accepted cone `[(q[53], q[136]), (q[29], s[29], q[114], s[114])]`
  - exact retained-state target `13 / 2744 / 480`

The corresponding raw run is:

- `results/experiments/order_668_hypergraph_ca/runs/canonical_frontier__hypergraph_causal_cone_ca.json`

## Branch Verdict

This branch survives as genuinely new evidence for this repo pass.

- It is not another retuning of H1.
- It beats every single-action retained-basis baseline on the canonical frontier seed and on the structural barrier ladder in `results/experiments/order_668_hypergraph_ca/summary.md`.
- The novelty lives in short-horizon local dynamics on a retained hypergraph, not in a new exact witness or a new Hadamard construction.
