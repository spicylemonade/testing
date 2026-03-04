# 007 — Pareto Multi-Scorer Ensemble

## Topic Context

Real-world protein engineering rarely optimizes a single property. A mutation that dramatically improves thermostability may simultaneously reduce expression, increase aggregation, or abolish catalytic activity. Wu et al. (2026, New Biotechnology) demonstrated this explicitly: structure-based design with ABACUS-R increased thermal stability by ~15°C but caused 80-100% activity loss, while the integrated multi-objective approach (ABACUS-R + MSA Transformer via MCMC) achieved ΔTm ~8°C while preserving >95% wild-type activity.

The Fleishman lab's LAffAb approach generates combinatorial antibody libraries with up to 9 mutations that co-optimize affinity and stability, achieving up to 30-fold affinity gains while maintaining stability.

Multi-objective optimization via NSGA-II (Non-dominated Sorting Genetic Algorithm II) maintains a population of solutions along the Pareto front, giving the user a menu of trade-offs rather than a single "best" solution.

## Key Connections

- **Pareto dominance avoids arbitrary weight selection**: Instead of choosing how to weight ddG vs expression, present the entire trade-off surface
- **Crowding distance preserves diversity**: Ensures the Pareto front covers the full range of property trade-offs

## Implementation Backlog

1. [ ] Implement NSGA-II with mutation set representation
2. [ ] Define crossover and mutation operators for mutation sets
3. [ ] Integrate ESM-2, ProteinMPNN, and aggregation predictor as objectives
4. [ ] Implement non-dominated sorting and crowding distance
5. [ ] Benchmark on proteins with known multi-property experimental data
6. [ ] Compute hypervolume indicator for Pareto front quality
7. [ ] Add expression level predictor (e.g., from ESM-2 perplexity)
8. [ ] Compare vs single-objective optimization on individual properties
9. [ ] Visualize Pareto fronts for interpretability
10. [ ] Add user-specified constraint regions (e.g., "ddG must improve by at least 2 kcal/mol")
