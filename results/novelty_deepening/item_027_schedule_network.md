# Item 027: Abelian Frontier Network Audit

## Audited Schedules

The audit used `1000` late snapshots from the baseline run and compared three legal schedules derived from the proved recurrence identities:

1. Batched snapshot schedule: choose the first two missing values of the current product set.
2. Row-immediate schedule: choose the row mex, adjoin the whole new row, then choose the column mex.
3. Column-immediate schedule: choose the least missing value first as a new column term, then complete the row choice; this is the axis-swapped schedule.

## Stabilization Result

- Batched vs row-immediate equality on all sampled states: `True`.
- Column-immediate axis-swap identity on all sampled states: `True`.
- Maximum number of pending new-row products strictly below the next column mex on the audited snapshots: `1`.

Because the only pending new-row product below the next column mex is the trivial unit product, randomized asynchronous insertion of the row products cannot alter the stabilized border pair. The one-step frontier update is therefore abelian up to axis swap on the audited late states.

## Observable Test

- Held-out AUROC using window length alone on the anchor-matched corpus: `0.526`.
- Held-out AUROC using the schedule-independent right-defect depth `end - c_n`: `0.957`.
- Relative improvement over window length: `0.820`.

## Conclusion

The abelian-network reframing is structurally correct at one step: the stabilized pair does not depend on schedule except for the proved axis swap. A window-level right-defect depth is genuinely schedule-independent and improves sharply over the equal-length baseline on the held-out matched-window corpus, but it still reduces to the same anchor geometry already isolated in Item 026 rather than a new asymptotic mechanism.
