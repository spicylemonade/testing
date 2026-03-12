# Tool Plan

## Global Routing

- Default to local repo artifacts, shell commands, and existing helper scripts.
- Do not run broad web search, wide literature expansion, theorem search, LP/ILP work, or extra horizon-chasing just to get larger numbers.
- Route work in this order:
  1. champion corpus build for `H1_anchor_offset_backbone`;
  2. falsifier controls on that same corpus;
  3. backup structural audit for `H2_witness_forest_invariant` only if the champion does not clear controls;
  4. reserve modular scan only if both active lanes fail;
  5. writing and review only after one lane survives the gates.

## Role Routing And Budgets

### `orchestrator`

- Tools: local shell, repo files, existing helper scripts.
- Budget envelope: one bounded round of coordination; at most one researcher bundle, one falsifier pass, one benchmark audit, one reviewer pass, and one citation audit.
- Routing rule: do not fork parallel explorations of all three hypotheses. Keep the reserve lane closed unless the first two fail.

### `researcher`

- Tools: local generator/checker scripts and artifact export helpers only.
- Budget envelope: one independently checked run plus one corpus export pass.
- Deliverable:
  - verify the recurrence update order with a separately written checker on a substantial prefix;
  - export all late record gaps in the current known regime plus matched non-record windows;
  - log previous-column anchor position, `Delta_n`, left/right interval lengths, skipped-prime flags, minimal witness summaries, and full witness hypergraphs;
  - include small-`q` residue logs only if they are effectively free from the same export.
- Stop rule: no new variant families and no extra horizon extension unless required to recover the already known late-record regime.

### `falsifier`

- Tools: local corpus, matched-window comparisons, surrogate product-window controls.
- Budget envelope: one attack pass, stopping at the first decisive failure.
- Deliverable:
  - test whether anchor/offset observables actually separate record windows from matched non-record windows;
  - test whether the same observables survive surrogate/null controls;
  - if the champion fails, immediately test whether the backup witness-forest invariants are any more discriminative.

### `writer`

- Tools: local markdown, claim sheets, and audit memos only.
- Budget envelope: one short memo or one negative-result handoff.
- Deliverable:
  - if a lane clears controls, write only the validated mechanism claim and its limits;
  - if no lane clears controls, write the blocker memo instead of speculative framing.

### `reviewer`

- Tools: local claim drafts, benchmark audit, falsifier memo, and exported corpus summaries.
- Budget envelope: one review pass.
- Deliverable:
  - reject any draft that slides back into OEIS/Kimberling provenance recovery, Ford-style local coverage language without explicit clearance, or prime-obstruction rhetoric that ignores composite-only records;
  - verify that update-order correctness, matched-control coverage, and witness-canonicalization caveats are stated explicitly.

### `citation auditor`

- Tools: local watchlist first; web only for exact source-of-record checks.
- Budget envelope: at most three targeted checks.
- Deliverable:
  - verify exact OEIS and Kimberling provenance wording;
  - clear any direct Ford/divisor-interval comparison language before it appears in a draft;
  - no broad exploratory search.

### `benchmark auditor`

- Tools: local experiment summaries, exported corpus artifacts, checker outputs.
- Budget envelope: one audit memo.
- Deliverable:
  - confirm independent checker agreement with the main generator on the audited prefix;
  - confirm matched non-record sampling and surrogate controls were actually used;
  - confirm row-immediate and column-immediate outputs are not presented as genuine robustness evidence;
  - flag any witness statistics that still depend on chosen-witness canonicalization.

## Decision Gates

- `H1_anchor_offset_backbone` stays active only if anchor/offset metrics beat matched non-record and surrogate controls.
- `H2_witness_forest_invariant` is promoted only if the forest-like profile survives full-hypergraph export, canonicalization checks, and surrogate controls.
- `H3_modular_obstruction_lift` opens only if the first two lanes fail and residue logging is already available at negligible marginal cost.
- If none of the lanes clears its gate, the correct output is a negative-result dossier and an explicit blocker memo, not a widened search program.
