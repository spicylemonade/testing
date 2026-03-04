# SDP Relaxation for LCS Upper Bounds

## Topic Context

The LCS problem is an integer optimization problem: find a maximum-weight matching between
positions of two strings that respects ordering constraints. This can be formulated as an
integer linear program (ILP). The LP relaxation gives an upper bound, but the SDP relaxation
(via Lasserre or Sherali-Adams hierarchies) can be substantially tighter.

## Key Idea

For each pair of strings (x,y) of length n, the SDP relaxation value >= LCS(x,y).
Therefore E[SDP_value] >= E[LCS] = gamma_2 * n + o(n). Dividing by n gives an upper bound
on gamma_2 in the limit. The advantage over automata-based methods is that SDP relaxations
are systematic and provably converge to the true optimum.

## Implementation Backlog

1. [ ] Write ILP formulation of LCS for binary strings of length n
2. [ ] Implement LP relaxation; compute average LP value for n=5,7,10
3. [ ] Implement level-1 Lasserre SDP relaxation
4. [ ] Solve SDP for all 2^(2n) string pairs (feasible for n<=8)
5. [ ] Compute E[SDP_value]/n and compare with 0.826280
6. [ ] If improvement observed, scale to level-2 Lasserre
7. [ ] Investigate exploiting symmetry to reduce SDP size
