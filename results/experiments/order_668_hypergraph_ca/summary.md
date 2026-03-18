# Hypergraph CA Summary

Fixed-rule two-step causal-cone hypergraph CA on the retained composite library.

## Setup

- Retained library: `results/analysis/composite_packet_retained_library.json`
- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Retained action count: `9`
- Unique retained-library states: `512`
- Causal-cone lookup budget per run: `256` transition lookups.
- Perturbation ladder rule: keep only frontier states with no immediate retained-action improvement but with at least one improving 2-step causal-cone hyperedge.

## Ladder

- `canonical_frontier`: state `0`, objective `13/2880/512`, packet mask `[]`.
- `barrier_ladder_01`: state `109`, objective `14/2812/496`, packet mask `['q[53]', 'q[136]', 's[53]', 's[84]', 's[136]', 's[166]']`.
- `barrier_ladder_02`: state `17`, objective `14/2820/496`, packet mask `['q[29]', 'q[114]', 's[84]', 's[166]']`.
- `barrier_ladder_03`: state `291`, objective `15/2408/416`, packet mask `['q[29]', 'q[53]', 'q[114]', 'q[136]', 's[29]', 's[35]', 's[38]', 's[44]', 's[47]', 's[114]']`.
- `barrier_ladder_04`: state `429`, objective `15/2408/416`, packet mask `['q[29]', 'q[53]', 'q[114]', 'q[136]', 's[35]', 's[38]', 's[44]', 's[47]', 's[53]', 's[84]', 's[136]', 's[166]']`.
- `barrier_ladder_05`: state `36`, objective `15/2544/448`, packet mask `['s[35]', 's[38]', 's[44]', 's[47]']`.

## Outcomes

- `canonical_frontier`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `1`, lookups `210`.
  pairwise_graph_ca: best `13/2880/512`, accepted updates `0`, lookups `9`.
  zero_coupling: best `13/2880/512`, accepted updates `0`, lookups `9`.
  zero_refractory: best `13/2880/512`, accepted updates `0`, lookups `9`.
  scorer_only: best `13/2880/512`, accepted updates `0`, lookups `9`.
- `barrier_ladder_01`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `1`, lookups `210`.
  pairwise_graph_ca: best `14/2812/496`, accepted updates `0`, lookups `9`.
  zero_coupling: best `14/2812/496`, accepted updates `0`, lookups `9`.
  zero_refractory: best `14/2812/496`, accepted updates `0`, lookups `9`.
  scorer_only: best `14/2812/496`, accepted updates `0`, lookups `9`.
- `barrier_ladder_02`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `1`, lookups `210`.
  pairwise_graph_ca: best `14/2820/496`, accepted updates `0`, lookups `9`.
  zero_coupling: best `14/2820/496`, accepted updates `0`, lookups `9`.
  zero_refractory: best `14/2820/496`, accepted updates `0`, lookups `9`.
  scorer_only: best `14/2820/496`, accepted updates `0`, lookups `9`.
- `barrier_ladder_03`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `1`, lookups `210`.
  pairwise_graph_ca: best `15/2408/416`, accepted updates `0`, lookups `9`.
  zero_coupling: best `15/2408/416`, accepted updates `0`, lookups `9`.
  zero_refractory: best `15/2408/416`, accepted updates `0`, lookups `9`.
  scorer_only: best `15/2408/416`, accepted updates `0`, lookups `9`.
- `barrier_ladder_04`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `1`, lookups `210`.
  pairwise_graph_ca: best `15/2408/416`, accepted updates `0`, lookups `9`.
  zero_coupling: best `15/2408/416`, accepted updates `0`, lookups `9`.
  zero_refractory: best `15/2408/416`, accepted updates `0`, lookups `9`.
  scorer_only: best `15/2408/416`, accepted updates `0`, lookups `9`.
- `barrier_ladder_05`
  hypergraph_causal_cone_ca: best `13/2744/480`, accepted updates `2`, lookups `256`.
  pairwise_graph_ca: best `15/2544/448`, accepted updates `0`, lookups `9`.
  zero_coupling: best `15/2544/448`, accepted updates `0`, lookups `9`.
  zero_refractory: best `15/2544/448`, accepted updates `0`, lookups `9`.
  scorer_only: best `15/2544/448`, accepted updates `0`, lookups `9`.

## Verdict

- The hypergraph branch is genuinely novel for this repo pass: the fixed two-step cone rule beats every single-action baseline on the canonical frontier seed and on every ladder state under the same transition-lookup budget.
- The accepted hypergraph updates are precomputed 2-step local cones on the retained action graph, not rescored sweeps over the original 334-packet basis.
