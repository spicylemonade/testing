# Variant 02: Dual-Bucket Polarity Merge

- Role: mixed-polarity fallback inside the champion subtree
- Source or polarity inference:
  - keep opposite-polarity branches in separate scout buckets and infer viability from which bucket can sustain charge without reverse collapse
- Minimum-energy accumulation:
  - accumulate the first useful startup energy in polarity-separated buckets before a controlled merge into the main reservoir
- Handoff gating:
  - use a merge latch that only releases the main arbiter after one bucket proves dominant and the merge node stays monotonic
- Dependency list:
  - `netlists/shared/source_pair_models.inc`
  - `netlists/shared/startup_cells.inc`
  - positive scout bucket
  - negative scout bucket
  - merge clamp
  - cross-coupled merge latch
  - post-merge handoff gate
- Predicted failure mode:
  - bucket leakage and merge overhead dominate below `50 mV`, collapsing any mixed-polarity advantage over a simpler nonaware startup path
