# 011 — Bandit Position Selection

## Topic Context

The protein stability optimization problem has two nested decisions: (1) **which positions** to mutate (k out of ~300), and (2) **which amino acids** to place at those positions. Most methods conflate these decisions, but they have very different computational structures.

Position selection is a classic multi-armed bandit problem: each candidate position is an "arm" with unknown reward (the best possible stability improvement at that position). The goal is to identify the top-k arms with minimal evaluations. Thompson sampling and UCB algorithms have strong theoretical guarantees for this setting.

Qiu et al. (Princeton) provide Bayesian regret bounds for tree-based protein optimization with bandit guidance, showing that efficient position selection enables near-optimal design discovery. The key insight is that evaluating a random mutation at a position provides noisy but informative evidence about that position's value — even before we know the optimal amino acid.

## Key Connections

- **Separation of concerns**: Position selection (which arms) vs amino acid optimization (what reward from each arm) can be solved sequentially
- **Budget allocation**: Thompson sampling naturally allocates more evaluations to uncertain positions, focusing effort where it matters most

## Implementation Backlog

1. [ ] Implement Thompson sampling for position arm selection
2. [ ] Implement UCB1 for position selection (as baseline comparison)
3. [ ] Define reward model: single mutation ddG at sampled position
4. [ ] Implement posterior update for Beta/Gaussian posteriors
5. [ ] Build two-phase pipeline: position selection then amino acid optimization
6. [ ] Compare with static top-k position selection from single-mutant screening
7. [ ] Benchmark on proteins where top positions are ambiguous (close scores)
8. [ ] Analyze position overlap between bandit-selected and oracle-optimal
9. [ ] Tune exploration-exploitation trade-off (UCB constant, Thompson temperature)
10. [ ] Integrate with game-theoretic or beam search for the amino acid optimization phase
