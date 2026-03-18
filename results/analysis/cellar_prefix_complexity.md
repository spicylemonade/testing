# Cellar Prefix Complexity

Prepared for rubric `item_027` and `item_028`.

## Conservative claim

The recorded packet supports a **no-go under the implemented exact encoding**, not a universal theorem that stack memory is never useful.

Supported claim:

- on the exact tail-panel encoding used here, no stack-only split beyond the static boundary-debt control state was observed
- the literal cellar branch therefore fails under this encoding

Unsupported claim:

- that every weaker static summary would match the cellar stack
- that pushdown memory can never matter on some other tokenization or transfer regime

## Why the encoding is hostile to a local cellar advantage

For `n = 2h + 1`, unread suffix bits can affect an assigned prefix through half-correlation shifts touching:

- the left boundary window `[0, k - 1]`
- the right boundary window `[t - k, t - 1]`

for each `1 <= k <= h`.

Computational exposure checks from `hadamard668.cellar.exposure_report`:

- `n = 79`: every cut `1 <= t < 79` exposes all `t` prefix bits
- `n = 167`: every cut `1 <= t < 167` exposes all `t` prefix bits

So the exact bottleneck is residual-state width, not a small hidden frontier that a stack can summarize cheaply.

## Exact panel evidence

Artifact: `results/experiments/cellar_phase6.json`

### Solved `4 x 79` control

- panel: `control_4x79_tail12`
- exact root completions: `1`
- weight-feasible prefixes: `2001`
- exact extendable prefixes: `13`
- boundary-debt frontier: `13`
- cellar-stack frontier: `13`
- completion-set purity under the recorded encoding: exact

Additional held-out control checks:

- `control_4x79_tail10`: exact root completions `1`, boundary frontiers `11`, cellar frontiers `11`
- `control_4x79_tail14`: exact root completions `1`, boundary frontiers `15`, cellar frontiers `15`

These panels leave no room for a `25%` proof-carrying improvement at unchanged witness retention, because the static frontier is already exact on the solved control family.

### Locked `167` exact-prefix panels

Tested panels:

- `target_167_tail12::direct_greedy::random_weight::30001`
- `target_167_tail12::direct_greedy::random_weight::30004`
- `target_167_tail12::direct_greedy::random_weight::30012`
- `target_167_tail12::direct_greedy::random_weight::30011`
- `seed_projection_tail12::shift_0`
- `seed_projection_tail12::shift_1`
- `seed_projection_tail12::single_flip_41`
- `seed_projection_tail12::cluster_40_42`

For every recorded `167` panel:

- exact root completions: `0`
- boundary-debt frontier: `0`
- cellar-stack frontier: `0`

This is informative as a no-go packet around the real anchors, but it is still degenerate evidence: with zero exact completions, purity is automatic.

## Complexity call

Best-supported classification:

- the exact tail-panel languages recorded here collapse to a finite residual-state problem under the implemented boundary-debt encoding
- that is enough to retire the literal cellar branch as currently encoded
- it is not yet enough to prove that all weaker non-stack encodings are equivalent or that pushdown memory can never help with transfer or proof reuse

## Item verdicts

`item_027`

- closed by option `(b)` as a conservative equivalence/no-go result under the implemented encoding

`item_028`

- closed as a sharply falsifiable regularity claim for the recorded exact tail-panel encoding, not as a universal theorem

Practical consequence:

- the branch no longer has a credible “untried stack expressivity” story
- any reopen must now target a different value proposition: compression, cross-order transfer, or proof-carrying feedback
