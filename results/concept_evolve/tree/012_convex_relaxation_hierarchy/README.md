# Convex Relaxation Hierarchy for Upper Bounds

## Topic Context

The Dancik-Paterson (1995) / Lueker (2009) upper bound method works as follows:

1. Define a dual automaton that reads random symbol pairs
2. The automaton maintains a buffer state tracking "alignment potential"
3. At each step, the automaton's score increases by at most the probability of seeing a match
4. The steady-state expected score rate is an upper bound on gamma_2
5. This is equivalent to solving an LP whose optimum is the upper bound

### Current Best Upper Bound
Lueker (2009): gamma_2 <= 0.826280 (buffer size h ~ 15)

### Hierarchy Approach
The LP can be strengthened systematically:
- Level 0: Local constraints only (original Dancik-Paterson)
- Level 1: Add pairwise transition consistency (2-step look-ahead)
- Level 2: Add triple transition consistency (3-step look-ahead)
- Each level is a larger LP with a smaller optimum
- In the limit, the hierarchy converges to gamma_2

## Key Insight

Each level adds constraints that enforce consistency over longer windows.
The improvement per level should be substantial because the LCS alignment
has long-range correlations that local constraints miss.

## Implementation Backlog

1. [ ] Reproduce Lueker's LP for h=8 (verify 0.826... is achievable)
2. [ ] Add 2-step look-ahead constraints (pairwise transition consistency)
3. [ ] Solve augmented LP
4. [ ] Measure improvement (target: > 10^-4 improvement)
5. [ ] If successful, add 3-step constraints (level 2)
6. [ ] Study convergence rate: how fast does LP_k -> gamma_2?
7. [ ] Compare with SDP relaxation (concept 004)
