# Cellar No-Go

Prepared for rubric `item_029` and `item_030`.

## Feedback branch outcome

The proof-carrying feedback layer does not have a viable baseline to improve under the recorded encoding.

Held-out same-template control checks:

- `control_4x79_tail10`: exact root completions `1`, exact extendable frontier `11`, static frontier `11`
- `control_4x79_tail12`: exact root completions `1`, exact extendable frontier `13`, static frontier `13`
- `control_4x79_tail14`: exact root completions `1`, exact extendable frontier `15`, static frontier `15`

Implication:

- the static boundary-debt frontier is already exact on the solved control family
- any additional local veto or proof-carrying guard can only duplicate existing rejects or drop witness prefixes
- the required `25%` held-out reduction at unchanged witness retention is therefore unattainable under this encoding

So `item_029` is an honest failure, not an unfinished task.

## Real-anchor stress packet

Artifact: `results/experiments/cellar_phase6.json`

Exact `167/80` completion tasks:

- `target_167_tail12::direct_greedy::random_weight::30001`
- `target_167_tail12::direct_greedy::random_weight::30004`
- `target_167_tail12::direct_greedy::random_weight::30012`
- `target_167_tail12::direct_greedy::random_weight::30011`

Degraded order-`668` anchored starts, projected into exact `167/80` tail panels:

- `seed_projection_tail12::single_flip_0_mod8`
- `seed_projection_tail12::single_flip_41_mod16`
- `seed_projection_tail12::cluster3_0_2_mod8`
- `seed_projection_tail12::cluster5_0_4_mod8`

Exact endpoint results on every recorded `167` or `668`-anchored panel:

- exact root completions: `0`
- boundary-debt frontier: `0`
- cellar-stack frontier: `0`

No panel produced:

- an exact witness
- a new exact-prefix completion
- a stack-only frontier reduction
- any exact-oracle saving unavailable to the matched static baseline

## Publication-grade verdict

The literal cellar / pushdown reopen fails on the actual anchors tested here.

- On solved same-template controls, the static boundary-debt frontier is already exact.
- On exact `167/80` tail panels near the best existing H1 candidates, no completions were found.
- On four degraded order-`668` starts with single-flip and clustered lower-modulus perturbations, no exact `167/80` tail completion was found after canonical projection.

The publishable claim is therefore a constrained no-go:

- under the exact tail-panel encoding implemented in `hadamard668/cellar.py`, cellar memory does not buy a surviving advantage over the matched static residual state, and the branch should be retired rather than promoted.
