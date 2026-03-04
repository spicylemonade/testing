# Novel Search Heuristics from Adjacent Domains

**Date:** 2026-03-04
**Source:** ConceptEvolve tree exploration (12 concepts, 67 walk paths)

## Summary

From the concept tree, three cross-domain analogies provide actionable improvements to our beam search and evolutionary optimizers for combinatorial protein stability optimization.

---

## 1. Top Insight: Submodular Maximization with Lazy Evaluation (Concept 004)

**Analogy Domain:** Sensor placement, feature selection, influence maximization in social networks.

**Key Idea:** When the objective function is approximately submodular (diminishing returns when adding mutations), the greedy algorithm with lazy evaluations achieves a (1 - 1/e) ≈ 0.63 approximation ratio with dramatically fewer function evaluations.

**Concrete Integration into Beam Search:**

The additive energy model (without epistasis) is exactly submodular. The additive+pairwise model is approximately submodular when positive epistatic interactions are sparse. We can exploit this:

1. **Lazy evaluation:** In beam search, when expanding partial solutions, skip re-evaluating candidates whose marginal gain upper bound (from the previous round) is already below the current threshold. This is the "lazy greedy" trick from Minoux (1978) and applies directly to our beam expansion step.

2. **Priority queue pruning:** Maintain candidates in a max-heap sorted by their marginal gain from the previous depth. Only re-evaluate when a candidate rises to the top of the heap. This reduces the number of energy model evaluations by 3-5x in practice.

3. **Approximate submodularity certification:** Before optimization, compute the "submodularity ratio" γ of the energy model by sampling random triples of mutations and checking diminishing returns. If γ > 0.8, use the lazy evaluation shortcut with high confidence.

**Implementation:** Add a `lazy_beam_search` option to `stabopt/optimization/beam_search.py` that maintains a priority queue with cached marginal gains.

**Expected Speedup:** 2-5x fewer energy model calls at each beam depth, with negligible quality loss when the submodularity ratio is high.

**Literature:** Nemhauser et al. (1978), Minoux (1978), Krause & Golovin (2014) — submodular optimization survey. The analogy to protein fitness landscapes being approximately additive (hence submodular) is supported by Faure et al. (2024).

---

## 2. MCTS with UCB Exploration (Concept 005)

**Analogy Domain:** Game-playing (AlphaGo), program synthesis, chemical retrosynthesis.

**Key Idea:** Monte Carlo Tree Search (MCTS) with Upper Confidence Bound (UCB1) exploration naturally balances exploitation (deepening promising mutation paths) with exploration (trying under-explored mutation combinations). Unlike beam search which commits to a fixed width at each depth, MCTS allocates computation adaptively.

**Concrete Integration into Evolutionary Optimizer:**

Replace the fixed-generation evolutionary loop with an MCTS-guided search:

1. **Tree structure:** Each node represents a partial mutation set. Children are obtained by adding one mutation. The tree is built incrementally.
2. **Rollout policy:** From a partial set of k' < k mutations, randomly complete to k mutations and evaluate with the energy model.
3. **UCB1 selection:** $a^* = \arg\max_a \bar{Q}(s,a) + c\sqrt{\frac{\ln N(s)}{N(s,a)}}$ where c controls exploration.
4. **Backpropagation:** Update ancestor statistics with the rollout score.

This naturally handles the "beam width" problem — MCTS will spend more time exploring branches that look promising without needing a fixed beam width parameter.

**Expected Improvement:** Better exploration of mutation space for k >= 6, where beam search may miss good combinations due to premature pruning. Particularly valuable when epistatic interactions create rugged fitness landscapes.

---

## 3. Cascading Funnel with Adaptive Thresholds (Concept 003)

**Analogy Domain:** Drug screening cascades, chip layout verification, multi-fidelity optimization.

**Key Idea:** Use a hierarchy of scoring models from fast/approximate to slow/accurate, filtering candidates at each level. This is the "funnel" or "cascade" paradigm from drug discovery.

**Concrete Integration into Pipeline:**

Our current pipeline already has this structure (ESM-2 → epistasis → optimization → ProteinMPNN re-ranking), but it can be tightened:

1. **Level 1 (fastest):** Additive-only scoring with ESM-2 single-mutation LLRs. Filter from N×19 to top-100 candidates. (~20s)
2. **Level 2 (moderate):** Compute pairwise epistasis only for top-100 candidates. Filter candidate combinations using beam search with additive+pairwise model. Keep top-200 k-mutation sets. (~40s)
3. **Level 3 (expensive):** Re-score top-200 sets using full conditional masked marginals (re-run ESM-2 with all mutations applied to compute the true multi-mutant LLR, not the additive approximation). (~60s)
4. **Level 4 (validation):** ProteinMPNN structural consistency for final top-20. (~30s)

**Adaptive Thresholds:** Instead of fixed cutoffs at each level, use the score distribution to set percentile-based thresholds. If level 1 scores are bimodal (indicating clear signal), tighten the threshold; if unimodal, keep more candidates.

**Expected Improvement:** The cascading approach ensures we don't waste expensive model evaluations on clearly poor candidates, while the adaptive thresholds prevent over-pruning when the fitness landscape is flat.

---

## Integration Priority

**Submodular lazy evaluation** is the highest-priority integration because:
1. It requires minimal code changes (modify beam expansion loop)
2. The speedup is well-characterized theoretically
3. It does not change solution quality for additive models
4. The protein stability landscape is empirically well-approximated by additive models (Faure et al. 2024 show ~80-90% of variance is explained by additive effects)

The MCTS and cascading funnel ideas are longer-term improvements that would require more significant refactoring.

---

## References

- Nemhauser, Wolsey, Fisher (1978). "An analysis of approximations for maximizing submodular set functions"
- Minoux (1978). "Accelerated greedy algorithms for maximizing submodular set functions"
- Krause & Golovin (2014). "Submodular function maximization" (survey chapter)
- Faure et al. (2024). "The genetic architecture of protein stability"
- Browne et al. (2012). "A survey of Monte Carlo tree search methods"
- Auer, Cesa-Bianchi, Fischer (2002). "Finite-time analysis of the multiarmed bandit problem" (UCB1)
