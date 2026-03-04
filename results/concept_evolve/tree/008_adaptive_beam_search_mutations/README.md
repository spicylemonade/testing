# 008 — Adaptive Beam Search Mutations

## Topic Context

Beam search is a workhorse algorithm in NLP for sequence generation: at each step, maintain the W highest-scoring partial sequences and expand each by all possible next tokens. It generalizes greedy search (W=1) and approximates exhaustive search (W→∞).

For protein mutation optimization, beam search incrementally builds mutation sets: starting from wild-type, at each step try adding each candidate mutation to each beam entry, score all expansions, and keep the top W. This is inherently GPU-friendly because the scoring calls at each step are independent and can be batched.

The **adaptive** variant adjusts beam width dynamically. When scores are tightly clustered (high entropy of score distribution), many candidates are competitive and wider exploration is needed. When one candidate clearly dominates, resources are better spent on depth than breadth.

## Key Connections

- **Relationship to greedy**: Greedy is beam search with W=1 — beam search strictly generalizes greedy
- **Relationship to MCTS**: Beam search is MCTS without backpropagation — once a candidate leaves the beam, it's gone
- **GPU throughput**: Batch scoring of W × |candidates| expansions is perfectly parallelizable

## Implementation Backlog

1. [ ] Implement basic beam search with fixed width
2. [ ] Implement adaptive width based on score entropy
3. [ ] Add deduplication of beam entries (same mutation set from different orderings)
4. [ ] Implement stochastic beam search (sample from top instead of hard cutoff)
5. [ ] Benchmark vs greedy, random, and exhaustive search
6. [ ] Profile GPU utilization and optimize batch sizing
7. [ ] Add early termination when beam converges
8. [ ] Implement diverse beam search (penalize similar beam entries)
9. [ ] Compare ordering strategies: random position order vs highest-variance first
10. [ ] Integrate with cascading funnel for final-stage re-ranking
