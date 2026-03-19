# Phase 6 Complexity-Accounted Frontier

## Benchmark Spec

- Geometry: `height 2, width 8`.
- Rerun mode: one deterministic direct-control motif per family, each checked by the exact verifier under the same seed and boundary budgets
- Seed budget: `3`.
- Initial-T budget: `1`.
- Boundary band: `1`.

## Ledger

- Score, |X|, coordinate height, grammar length, active state count, extractor complexity, seed budget, and boundary initialization are all treated as first-class coordinates.
- A row with no forcing witness is represented explicitly rather than hidden behind best-of-run score reporting.

## Rows

- `same_palette_2x8`: score=None, hit_rate=0.0000, |X|=5, height=3, grammar=None, active_states=None.
- `low_height_asymmetric_2x8`: score=None, hit_rate=0.0000, |X|=5, height=2, grammar=None, active_states=None.
- `bounded_slope_2x8`: score=None, hit_rate=0.0000, |X|=5, height=2, grammar=None, active_states=None.
- `slowly_growing_x_2x8`: score=None, hit_rate=0.0000, |X|=7, height=2, grammar=None, active_states=None.
- `legacy_exploratory_width8_3label`: score=2.0714285714285716, hit_rate=1.0000, |X|=4, height=2, grammar=31, active_states=3.

## Frontier

- Pareto frontier rows: legacy_exploratory_width8_3label, bounded_slope_2x8, low_height_asymmetric_2x8.
- Score-only leader: `legacy_exploratory_width8_3label`.
- Complexity statement: Score-only ranking would promote the saved exploratory width-8 witness at 29/14, but the ledger shows that every matched rerun with fixed |X|=5 and the same extractor stays empty. The apparent improvement is therefore outside the matched benchmark envelope, which score-only reporting cannot express.

## Novelty Position

- This is not a restatement of the current paper or of Tao's bounded-slope warning because the ledger treats hidden complexity variables as part of the exact optimization problem itself. The comparison is between verifier-backed witnesses under one explicit coordinate system, not between prose-level warnings.
