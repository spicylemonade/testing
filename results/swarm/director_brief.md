# Director Brief

## Decision

- Champion direction: Modular Shadow / p-adic Semilinearity Barrier.
- Backup direction: Pisot Self-Matching Beyond Quadratic Units.

## Why this pair

- The champion has the best novelty-to-falsifiability ratio in the current scout set. It attacks the exact arithmetic subsequence problem directly, avoids the derivative Sturmian or bounded-partial-quotient lane, and addresses the falsifier's main traps: rational triviality, sparse post-selection, prefix fitting, and word/value confusion.
- The backup is the cleanest exceptional-family positive route. If the champion screen leaves any irrational survivors, the most plausible non-cosmetic story from the scouts is a narrow Pisot mechanism rather than a broad quadratic or bounded-type thesis.
- The generalized-polynomial / LRS framing remains valuable, but only as a reserve umbrella after genuine irrational survivors have been isolated.

## Deprioritized directions

- Ostrowski-Automaton Classification of Hidden Recurrences: too close to the recent quadratic Beatty decidability lane and too exposed to the falsifier's `quadratic is the wrong invariant` objection.
- Sparse Hankel-Rank Barrier for Generic Slopes: useful as a diagnostic lens, but too easy to contaminate with tuned low-rank fits if selector classes are not frozen first.
- Sparse Rigidity Frontier for Structured Selectors: promising as supporting intuition, but not the first theorem target while the definition lock and novelty screen are still incomplete.

## Unresolved blockers

- `results/swarm/gap_map.md` is missing.
- `results/literature/prior_art_gap.md` has no filled differentiation evidence.
- `results/literature/gap_frontier.md` is empty.
- The phrase `homogeneous linearly recurrent subsequence` is still unsafe: the project has not fixed value recurrence versus symbolic recurrence, arbitrary extraction versus structured selector classes, coefficient ring, or whether degenerate recurrences are allowed.
- Because of those gaps, no theorem claim should be treated as stable yet.

## Exact next experiment for the researcher

- Definition lock: take `r > 0`; define a subsequence by increasing indices `n_k`; define `b_k = floor(n_k r)` to satisfy a nondegenerate homogeneous constant-coefficient recurrence over `Z`; record explicitly whether arbitrary indices are allowed or only predeclared selector families.
- Pre-register one discriminator panel before running anything:
  - slopes: `2`, `3/2`, `5/3`, `phi`, `sqrt(2)`, the plastic constant, one Salem example, `e`;
  - selector families: arithmetic progressions, fixed finite unions of arithmetic progressions, Ostrowski-definable selectors, linear-recursive selectors;
  - recurrence orders: `d = 1..4`;
  - moduli: `2`, `3`, `5`, `7`, `11`, plus one prime-square follow-up for any survivor.
- For each fixed selector family and recurrence profile, test whether every exact candidate produces a consistent eventual semilinear shadow across the chosen moduli. Do not retune selectors after a failure.
- Decision rule:
  - if only rational slopes survive, promote the champion as the main theorem program under the chosen selector class;
  - if a Pisot slope survives cleanly while non-Pisot controls fail, hand off immediately to the backup;
  - if generic irrationals survive, demote the champion and stop claiming novelty until the literature gap is repaired.
