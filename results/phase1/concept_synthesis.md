# Concept Tree Synthesis: Cross-Domain Transferable Ideas

**Date:** 2026-03-04
**Source:** ConceptEvolve tree at `results/concept_evolve/tree/`
**Total concepts generated:** 12

---

## Overview

ConceptEvolve generated 12 concept cards spanning domains including game theory, drug discovery, multi-fidelity optimization, submodular optimization, Monte Carlo tree search, diffusion models, bandit algorithms, and quantum-inspired methods. The semantic bridge graph has 17 nodes and 27 edges, with 67 walk paths identifying concept chains.

---

## Top 3 Transferable Ideas

### Idea 1: Drug Discovery Cascading Funnel (from concept_003: surrogate_cascading_funnel)

**Source domain:** Drug discovery / multi-fidelity optimization
**Analogy:** High-throughput drug screening uses a cascading funnel — millions of compounds are screened with fast/cheap assays, then thousands are validated with medium-throughput assays, and finally dozens are optimized with expensive functional assays.

**Transfer to protein stability:** Arrange stability predictors in a speed/accuracy cascade:
- **Stage 1 (microseconds):** ESM-2 masked marginal scoring — screen all N×19 single mutations
- **Stage 2 (milliseconds):** Additive+pairwise energy model — score K^depth combinatorial candidates
- **Stage 3 (seconds):** ProteinMPNN conditional log-likelihood — re-rank top 50-100 candidates
- Optional **Stage 4:** Rosetta/RaSP physics-based validation of top 10

**Mathematical formulation:** Given scorers f_1 (fast), f_2 (medium), f_3 (slow/accurate) with costs c_1 << c_2 << c_3, define funnel: S_1 = top_N1({x : f_1(x) > t_1}), S_2 = top_N2({x in S_1 : f_2(x) > t_2}), S_3 = argmax_{x in S_2} f_3(x).

**Relevance to rubric items:** item_008 (scoring baselines), item_013 (epistasis scoring), item_018 (consensus re-ranking)

**Citations:**
- Multi-fidelity Bayesian optimization: Kandasamy et al. (2016) "Multi-fidelity Bayesian Optimisation"
- Drug discovery funnel: Mayr et al. (2009) "Practical aspects of hit identification"
- Cascading classifiers: Viola & Jones (2001) cascade architecture

### Idea 2: Submodular Maximization with Approximation Guarantees (from concept_004: submodular_stability_maximization)

**Source domain:** Combinatorial optimization / sensor placement / feature selection
**Analogy:** Placing sensors to maximize information coverage exhibits diminishing returns — each additional sensor adds less new information. This is the submodularity property. Under submodularity, the greedy algorithm (always pick the next best item) achieves a (1-1/e) ≈ 63% approximation guarantee.

**Transfer to protein stability:** If the stability benefit of adding mutation m_k diminishes as more mutations are already in the set (epistatic saturation), the mutation selection problem is approximately submodular. Greedy selection with lazy evaluation then provides:
1. A provable approximation ratio (theoretical contribution)
2. O(k × N) evaluations instead of C(N,k) (practical speedup via lazy greedy)
3. A strong baseline that beam search/evolutionary methods must beat

**Mathematical formulation:** Let f(S) = -ddG(S) be the stability improvement. If f is monotone submodular (diminishing marginal returns), then the greedy algorithm selecting k mutations achieves f(S_greedy) >= (1 - 1/e) × f(S*).

**Relevance to rubric items:** item_010 (greedy baseline), item_014 (energy model), item_024 (theoretical contribution in report)

**Citations:**
- Nemhauser, Wolsey, Fisher (1978) — foundational submodular maximization result
- Faure et al. (2024) — epistatic interactions saturate at pairwise level, consistent with submodularity
- Krause & Golovin (2014) — submodular optimization for sensor placement

### Idea 3: Game-Theoretic Equilibrium Search (from concept_001: game_theoretic_mutation_selection)

**Source domain:** Game theory / network routing / auction design
**Analogy:** In congestion games, each player (router) selects a path to minimize latency, considering other players' choices. The Nash equilibrium represents a stable configuration. Best-response dynamics converge to equilibrium by having each player sequentially optimize their choice.

**Transfer to protein stability:** Each mutation position is a "player" choosing an amino acid. The shared payoff is -ddG. Best-response dynamics: each position sequentially picks its best amino acid given the current choices at all other positions. This decomposes the exponential search space into per-position decisions.

**Mathematical formulation:** Let S = {s_1,...,s_k} be mutable positions with action sets A_i. Payoff u(a_1,...,a_k) = -ddG. Nash equilibrium: a_i* = argmax_{a_i} u(a_i, a_{-i}*). Best-response: a_i^{t+1} = argmax_{a_i} u(a_i, a_{-i}^t). Converges in O(k × |A|) calls per sweep vs O(|A|^k) brute force.

**Relevance to rubric items:** item_016 (evolutionary/alternative optimizer), item_017 (novel heuristics), item_022 (ablation study)

**Citations:**
- Bal et al. (2025) "GameOpt" — directly applies cooperative games to combinatorial protein BO
- Monderer & Shapley (1996) — potential games and convergence of best-response dynamics
- Nash (1950) — foundational equilibrium concept

---

## Additional Promising Concepts (Brief Notes)

4. **MCTS Mutation Tree** (concept_005): Monte Carlo tree search for exploring mutation combinations. UCB1 selection balances exploration/exploitation. Useful when epistasis creates complex, non-additive landscapes.

5. **Bandit Position Selection** (concept_011): Thompson sampling to adaptively allocate evaluation budget to informative positions. Efficient when only a subset of positions are worth mutating.

6. **Diffusion-Guided Mutation Sampling** (concept_009): Use ESM-2 as a masked diffusion model to generate diverse multi-mutant candidates in parallel. Avoids sequential construction bias of beam search.

---

## Integration Priority

The **cascading funnel** (Idea 1) forms the backbone of our pipeline architecture. **Submodular maximization** (Idea 2) provides theoretical grounding and a strong greedy baseline. **Game-theoretic search** (Idea 3) offers an alternative optimizer for the ablation study. These three ideas collectively address the rubric's requirements for scoring (funnel), theoretical contribution (submodularity), and multiple optimizer comparison (game theory vs beam search vs evolutionary).
