# 003 — Surrogate Cascading Funnel

## Topic Context

The fundamental challenge in multi-mutant optimization is the trade-off between scoring accuracy and throughput. A 300-residue protein with 8 mutable positions has ~19^8 ≈ 17 billion possible combinations. No single scorer is fast enough AND accurate enough to evaluate all of them within a 15-minute budget.

The cascading funnel borrows from drug discovery, where screening campaigns use progressively more expensive assays: a fluorescence-based primary screen evaluates millions of compounds, biochemical assays confirm thousands of hits, and cell-based assays validate dozens of leads. Similarly, we can arrange protein stability predictors from cheapest to most expensive:

- **ESM-2 masked marginal** (~1μs/variant on GPU): sequence-based, captures evolutionary plausibility
- **ProteinMPNN** (~1ms/variant): structure-conditioned, captures local packing
- **RaSP** (~100ms/variant): trained on Rosetta energies, more physics-aware
- **Rosetta/FoldX** (~10s/variant): explicit energy functions, highest accuracy

The key insight from multi-fidelity optimization is that cheap/noisy evaluations are highly informative for *filtering* (identifying clearly bad candidates) even when they're poorly calibrated for *ranking* (ordering the top candidates).

## Key Connections

- **Recall vs precision trade-off at each stage**: Early stages optimize for recall (don't miss the best), later stages for precision (rank correctly among the top)
- **Threshold calibration**: Optimal thresholds depend on inter-scorer correlation and noise levels

## Implementation Backlog

1. [ ] Implement ESM-2 masked marginal scoring with batch GPU inference
2. [ ] Implement ProteinMPNN conditional probability scorer
3. [ ] Implement RaSP ddG predictor integration
4. [ ] Build funnel pipeline with configurable stage sizes (N1, N2, N3)
5. [ ] Add threshold auto-calibration from Mega-scale validation split
6. [ ] Benchmark recall of true top-10 variants at each stage
7. [ ] Profile end-to-end timing on A100 for representative proteins
8. [ ] Optimize ESM-2 batch size for maximum throughput
9. [ ] Add optional Rosetta/FoldX final stage for highest-stakes applications
10. [ ] Implement parallel scoring across funnel stages where independent
