# ConceptEvolve Steering Notes

**Date:** 2026-03-04
**Project:** Fast Combinatorial Protein Stability Optimization (StabOpt)

---

## 3 Concrete Steering Directions

### Direction 1: Epistasis-Decomposed Beam Search with Cascading Funnel Scoring (PRIORITIZED)

**Summary:** Combine structure-based epistasis decomposition (cluster mutations into weakly-interacting groups by Calpha distance) with adaptive beam search across clusters, using a cascading scoring funnel (ESM-2 fast prescreening -> additive+pairwise energy model -> ProteinMPNN re-ranking).

**Rubric items informed:**
- item_008 (ESM-2 and ProteinMPNN single-mutation scoring)
- item_013 (pairwise epistasis scoring with structural proximity)
- item_014 (additive-plus-pairwise energy model)
- item_015 (beam search combinatorial optimizer)
- item_018 (consensus re-ranking with ProteinMPNN)

**Why prioritized:** This direction is the most implementable within the 15-minute GPU budget. All components use pretrained models off-the-shelf (no training needed). The cascading funnel architecture naturally maps to the rubric's phased implementation. The beam search provides a tunable speed-quality tradeoff via beam width. Most importantly, the epistasis decomposition by structural proximity is well-grounded in Faure et al. (2024) findings that >90% of epistatic interactions occur between residues within 10A.

### Direction 2: Game-Theoretic Best-Response Dynamics for Position Selection

**Summary:** Treat each mutation position as a player in a cooperative game. Use iterative best-response dynamics where each position sequentially optimizes its amino acid choice while others are held fixed. Convergence to Nash equilibrium gives a locally optimal multi-mutant.

**Rubric items informed:**
- item_016 (evolutionary/alternative optimizer — best-response as alternative to genetic algorithm)
- item_022 (ablation study — compare game-theoretic vs beam search vs evolutionary)
- item_017 (novel search heuristics from adjacent domains)

**Rationale:** Provides theoretical convergence guarantees and a principled decomposition of the combinatorial problem. Complements beam search by offering a different inductive bias (local equilibrium vs greedy expansion). Inexpensive to implement as an alternative optimizer.

### Direction 3: Submodular Maximization with Diminishing Returns Guarantee

**Summary:** Frame the mutation selection problem as submodular maximization: the marginal benefit of adding a mutation diminishes as more mutations are already selected (due to epistasis saturating). Under the submodularity assumption, greedy selection achieves a (1-1/e) approximation guarantee. Use a lazy greedy evaluation strategy to minimize scorer calls.

**Rubric items informed:**
- item_010 (greedy baseline — upgraded with lazy evaluation and approximation guarantee)
- item_015 (beam search — hybrid beam + lazy greedy)
- item_022 (ablation — submodular vs non-submodular scoring)
- item_024 (technical report — theoretical contribution)

**Rationale:** Provides the strongest theoretical guarantee among all directions. The key insight from concept_004 (submodular stability maximization) is that protein stability under additive+pairwise models often exhibits approximate submodularity. The lazy greedy algorithm can reduce scorer calls by 10-50x while maintaining approximation guarantees.

---

## Priority Ranking

1. **Direction 1 (Epistasis Beam Search + Funnel)** — This is the core pipeline. It directly addresses the rubric's scoring and optimization modules (items 008, 013-015, 018) and is most likely to produce a working end-to-end pipeline within the time budget.

2. **Direction 3 (Submodular Maximization)** — Enhances the greedy baseline with theoretical guarantees and practical speedups. Low implementation cost, high payoff for both the technical report and the ablation study.

3. **Direction 2 (Game-Theoretic)** — Most novel but highest risk. Implement as an alternative optimizer (item_016) after the beam search pipeline is working. Good for the "novel heuristics" concept exploration (item_017).

---

## Integration Plan

The prioritized Direction 1 maps cleanly to the rubric phases:
- Phase 2: Implement ESM-2 and ProteinMPNN scorers (item_008), brute-force and greedy baselines (items 009-010)
- Phase 3: Add epistasis scoring (item_013), energy model (item_014), beam search (item_015), ProteinMPNN re-ranking (item_018)
- Phase 3 alternative: Implement Direction 2 as evolutionary.py alternative (item_016)
- Phase 4: Compare all approaches in ablation study (item_022)
