# 009: Path Record Expansion

## Overview

While delay records measure how LONG a trajectory takes, path records measure how HIGH a trajectory reaches. The expansion X_2(n) = Mx(n)/n^2 normalizes the maximum by the starting number squared. Whether X_2 is bounded is a major open question (Roosendaal's Open Question 1).

## Current State

- 97 path records are known
- Highest expansion: X_2 ~ 16.315 at P_88 = 1,980,976,057,694,848,447
- Expansion records are extremely rare: X_2 first exceeded 12.66 at n = 27, then not again until n = 319,804,831

## Key Theorem (Roosendaal)

For all odd path records P_i >= 3: Mx(P_i) = 16 mod 36. This structural constraint significantly narrows the search space.

## Implementation Backlog

1. [ ] Implement 128-bit Collatz iteration with Mx tracking
2. [ ] Reproduce known path records up to P_50
3. [ ] Apply the mod 36 constraint as an additional sieve filter
4. [ ] Search for new path records beyond current frontier
5. [ ] Test whether X_2 shows signs of boundedness or divergence
6. [ ] Connect expansion distribution to extreme value theory
