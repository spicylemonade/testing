# 005 — MCTS Mutation Tree

## Topic Context

Monte Carlo Tree Search (MCTS) revolutionized game-playing AI by balancing exploration and exploitation through four phases: selection (navigate tree via UCB), expansion (add new nodes), simulation (random rollout), and backpropagation (update statistics). Applied to protein mutation optimization, the "game" is building a set of k mutations one at a time.

The critical advantage of MCTS over greedy search is that it can **backtrack**: if a promising first mutation leads to poor combinations, MCTS will explore alternatives. Greedy methods, once committed to a mutation, never reconsider.

Recent work has combined MCTS with protein design:
- **MCTD-ME** (Liu et al. 2025) integrates MCTS with masked diffusion models for inverse folding
- **ProtInvTree** uses reward-guided tree search for deliberate inverse folding
- **Tree search-based evolutionary bandits** (Qiu et al., Princeton) provide Bayesian regret bounds for tree-based protein sequence optimization

## Key Connections

- **Exploration constant c** controls the explore-exploit trade-off: too low -> greedy (may miss global optimum), too high -> random (wastes budget)
- **Virtual loss** enables parallel MCTS on GPU: penalize nodes being evaluated to encourage exploration of different branches

## Implementation Backlog

1. [ ] Implement MCTS node class with Q-value, visit count, children
2. [ ] Implement selection phase with UCB1 and PUCT
3. [ ] Implement expansion and rollout with ESM-2 scorer
4. [ ] Implement backpropagation of scores
5. [ ] Add virtual loss for parallel exploration
6. [ ] Implement progressive widening for large action spaces
7. [ ] Benchmark against greedy and beam search
8. [ ] Tune exploration constant on validation set
9. [ ] Add policy network prior from ESM-2 single-mutant scores
10. [ ] Profile and optimize for GPU batch inference during rollouts
