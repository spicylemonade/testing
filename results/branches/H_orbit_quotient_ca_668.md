# H Orbit-Quotient CA 668

This branch quotients the retained composite library by symmetry-controlled orbit signatures so the runtime rule depends on transport-shape classes, not on raw packet coordinates.

## Orbit Construction

- Cyclic quotient: absolute packet indices are discarded; only the local transport-shape class survives.
- Dihedral quotient: the signature is invariant under reversal because it depends only on orbit representative support class, changed-count bin, transport-width bin, and sign-run count.
- q/s sign quotient: global sign orientation is removed from the signature, so the rule table never memorizes a specific q/s sign representative.
- Orbit neighborhoods are defined by changed-lag overlap between orbit representatives at each state, not by raw packet indices.

## Training Mix

- Control `control_n5_q0`: `24` states, `162` improving orbit representatives.
- Control `control_n7_q0`: `24` states, `338` improving orbit representatives.
- Control `control_n9_hardest_pair`: `64` states, `2259` improving orbit representatives.
- Frontier perturbation `barrier_ladder_01`: state `109`, `3` improving orbit representatives.
- Frontier perturbation `barrier_ladder_02`: state `17`, `3` improving orbit representatives.
- Frontier perturbation `barrier_ladder_03`: state `291`, `1` improving orbit representatives.
- Frontier perturbation `barrier_ladder_04`: state `429`, `1` improving orbit representatives.
- Orbit rule-table size: `137` signatures.

## Canonical Frontier Result

- Orbit CA best objective: `13/2744/480`.
- Raw-coordinate baseline: `13/2880/512`.
- Scorer-only control: `13/2880/512`.
- Accepted orbit signature: `['split_annihilate', 2, 'conserve', '9_plus', 'wide', 8]`.
- Chosen representative: `[['q[53]', 'q[136]'], ['q[29]', 's[29]', 'q[114]', 's[114]']]`.
- Orbit neighborhood size at first step: `20`.

## Perturbation Suite

- `canonical_frontier`: orbit `13/2744/480`, raw baseline `13/2880/512`, scorer_only `13/2880/512`.
- `barrier_ladder_01`: orbit `13/2880/512`, raw baseline `14/2812/496`, scorer_only `14/2812/496`.
- `barrier_ladder_02`: orbit `13/2744/480`, raw baseline `14/2820/496`, scorer_only `14/2820/496`.
- `barrier_ladder_03`: orbit `13/2744/480`, raw baseline `15/2408/416`, scorer_only `15/2408/416`.
- `barrier_ladder_04`: orbit `13/2744/480`, raw baseline `15/2408/416`, scorer_only `15/2408/416`.
- `barrier_ladder_05`: orbit `13/2744/480`, raw baseline `15/2544/448`, scorer_only `15/2544/448`.

## Verdict

- The orbit quotient survives: one fixed rule table, trained without the canonical seed, improves the canonical frontier representative and the perturbation ladder while beating the best raw-coordinate single-action baseline and scorer_only under the same lookup budget.
