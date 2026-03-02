# Phase Transitions in Generalized Collatz Family

## Parameters
- test_n = 5000, max_iter = 100000
- a ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21], b ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

## Phase Diagram

- a=3, b=1 convergence: 1.000 (expected ~1.0)
- a=5, b=1 convergence: 0.099 (expected ~0.0)

## Critical Boundary

- Boundary cells (0.1 < frac < 0.9): 7 / 121
- Boundary fraction: 0.058

## Critical Transitions
- b=1: transition between a=3 (convergent) and a=5 (divergent)
- b=3: transition between a=3 (convergent) and a=5 (divergent)
- b=5: transition between a=3 (convergent) and a=5 (divergent)
- b=7: transition between a=3 (convergent) and a=5 (divergent)
- b=9: transition between a=3 (convergent) and a=5 (divergent)
- b=11: transition between a=3 (convergent) and a=5 (divergent)
- b=13: transition between a=3 (convergent) and a=5 (divergent)
- b=15: transition between a=3 (convergent) and a=5 (divergent)
- b=17: transition between a=3 (convergent) and a=5 (divergent)
- b=19: transition between a=3 (convergent) and a=5 (divergent)
- b=21: transition between a=3 (convergent) and a=5 (divergent)

## Escape Time Analysis Near Boundary

- a=3, b=1: mean escape = 0, n_divergent = 0
- a=5, b=1: mean escape = 337, n_divergent = 4534
- a=7, b=1: mean escape = 140, n_divergent = 4932
- a=9, b=1: mean escape = 98, n_divergent = 5000
- a=11, b=1: mean escape = 79, n_divergent = 5000
- a=3, b=3: mean escape = 0, n_divergent = 0
- a=5, b=3: mean escape = 315, n_divergent = 4588
- a=7, b=3: mean escape = 143, n_divergent = 4951
- a=9, b=3: mean escape = 98, n_divergent = 5000
- a=11, b=3: mean escape = 79, n_divergent = 5000
- a=3, b=5: mean escape = 0, n_divergent = 0
- a=5, b=5: mean escape = 317, n_divergent = 4161
- a=7, b=5: mean escape = 135, n_divergent = 4618
- a=9, b=5: mean escape = 99, n_divergent = 5000
- a=11, b=5: mean escape = 78, n_divergent = 4966
