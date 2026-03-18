# CA Program Analysis

Prepared for rubric `item_021`.

## Outcome summary

The implemented cellular-automata program does not improve the current order-`668` search state.

- `H1` did not produce an exact `167/80` witness and was outperformed by the matched direct-search baseline on both the solved control and the real target.
- `H2` did not lift or improve the degraded order-`668` modular seed beyond the matched same-neighborhood baseline.
- The strongest honest recommendation is `stop`, not `continue`.

## Failure modes

### 1. Reachability collapse on the support-space CA

`parallel_gain_ca` fires too few productive moves and explores fewer dihedral orbits than `direct_greedy` on both `H1` sweeps. The current local-dominance rule therefore reduces diversity and does not buy a compensating exact-target advantage.

### 2. Metric leakage on the toy modular ladder

The structured `n = 9` ladder initially looks favorable to the CA, but random controls solve most starts as well. That means the ladder is a sanity check, not evidence that the CA has discovered a meaningful repair mechanism.

### 3. No decisive gain on the real order-668 seed

The only decisive `H2` experiment is the real degraded seed attempt. There the CA and the matched non-CA search tie exactly on modulus, `l1_defect`, defect count, and maximum defect magnitude. Any claim of CA-specific repair therefore collapses.

### 4. Novelty collapse risk

Once `H1` loses and `H2` ties, the surviving interpretation is not `CA helps with Hadamard 668`, but `these CA rule families are another local-search wrapper on the same neighborhoods`.

## Decision quality

The stop decision is high quality rather than accidental.

- Kill rules were registered before the decisive sweeps.
- Fairness issues were repaired before the stop/go call.
- Negative controls and equivalence-aware reachability accounting were present.
- The program stopped on the decisive same-representation comparisons instead of on cosmetic metrics.

## Recommendation

Stop the current CA program.

Only reopen the research under a new branch if all of the following hold:

- the state representation changes materially;
- the comparator changes with it and remains matched;
- the new branch passes a same-template positive control;
- the new branch survives a novelty-collapse audit before any broad compute budget is spent.
