# Time-Constant Ranked Arbiter

- Role:
  - lower-overhead same-family control that keeps helper-free pre-handoff branch selection
- Mechanism:
  - each source is observed through a fast and a slow passive window
  - the branch score is the fast-minus-slow response
  - the grant selector uses that dual-window score with a lighter control branch than the RC-ranked champion
- Why it exists:
  - this is the smallest executable realization of the `003_time_constant_ranked_arbiter` concept note
  - it tests whether the surviving mixed-source cases require the full packet-scout controller or only a cheaper branch-ranking cue
- Dependency list:
  - `netlists/shared/source_pair_models.inc`
  - `netlists/shared/startup_cells.inc`
  - `netlists/shared/packet_scout_blocks.inc`
  - `netlists/shared/measurement_hooks.inc`
- Expected interpretation:
  - if it preserves the surviving cases with lower `e_ctrl`, the original RC-ranked champion is over-built for this simplified source model
