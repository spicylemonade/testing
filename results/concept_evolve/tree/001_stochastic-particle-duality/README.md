# Concept: stochastic_particle_duality

- Topic Context: Try your absolute hardest and derive new tighter nontrivial bounds

# Chvátal–Sankoff constant for a binary alphabet

## Description of constant

Let $\lambda_{n,2}$ be the random variable assigning two uniformly random binary strings of length $n$ the length of their longest common subsequence.
Then $C_{31a}$ is the (well-defined) limit $C_{31a} := \lim_{n \to \infty}\frac{\mathbb{E}[\lambda_{n,2}]}{n}$.

## Known upper bounds

| Bound | Reference | Comments |
| ----- | --------- | -------- |
| 1 | Trivial | |
| 0.837623 | [DP1995] | |
| 0.826280 | [L2009] | Computer assisted |

## Known lower bounds

| Bound | Reference | Comments |
| ----- | --------- | -------- |
| 0 | Trivial | |
| > 0 | [CS1975] | Showed existence of limit |
| 0.773911 | [D1994] | Computer assisted |
| 0.788071 | [L2009] | Computer assisted |
| 0.792665992 | [H2024] | Computer assisted |

## Additional comments

- Chvátal–Sankoff constants on Wikipedia: https://en.wikipedia.org/wiki/Chv%C3%A1tal%E2%80%93Sankoff_constants

## References

- [CS1975] Chvatal, Václáv, and David Sankoff. Longest common subsequences of two random sequences. Journal of applied probability 12.2 (1975): 306-315.
- [H2024] Heineman, George T., et al. Improved Lower Bounds on the Expected Length of Longest Common Subsequences. arXiv preprint (2024) arXiv:2407.10925.
- [L2009] Lueker, George S. Improved bounds on the average length of longest common subsequences. Journal of the ACM (JACM) 56.3 (2009): 1-38.
- [DP1995] Dančík, Vlado, and Mike Paterson. Upper bounds for the expected length of a longest common subsequence of two binary sequences. Random Structures and Algorithms 6.4 (1995): 449-458.
- [D1994] Dancík, Vladimír. Expected length of longest common subsequences. Diss. University of Warwick, 1994.
- Domains: statistical_mechanics, probability_theory, combinatorics

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.