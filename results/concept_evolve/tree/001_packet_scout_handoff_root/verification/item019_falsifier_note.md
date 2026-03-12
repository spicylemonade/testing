# Item 019 Falsifier Note

Date: 2026-03-12
Scope: adversarial startup stress for H1 across source collapse, mixed polarity, extreme impedance asymmetry, and chatter-intended conditions
Status: PASS as a falsifier artifact; H1 is narrowed, not killed

## Inputs

- Falsifier manifest:
  - `results/manifests/falsifier_cases.json`
- Falsifier run log:
  - `results/manifests/falsifier_runlog.jsonl`
- Falsifier result table:
  - `tables/falsifier_results.csv`
- Falsifier summary:
  - `tables/falsifier_summary.json`

## Coverage

- Cases executed:
  - `6`
- Designs per case:
  - `champion`
  - `fixed`
  - `nonaware`
- Total adversarial rows:
  - `18`
- Attack classes represented:
  - `source_collapse_same`
  - `source_collapse_mixed`
  - `polarity_mismatch_extreme`
  - `uvlo_chatter_same`
  - `uvlo_chatter_mixed`
  - `dual_collapse_extreme`

## Measured Result

- Champion startup successes:
  - `3/6`
- Fixed-baseline startup successes:
  - `2/6`
- Nonaware-baseline startup successes:
  - `2/6`
- Handoff-fall or second-rise events observed:
  - none
  - the chatter-intended cases turned into outright no-start behavior rather than measured handoff chatter

## Where The Champion Actually Differed

- `fa_001` source-collapse same-polarity case:
  - champion started successfully
  - fixed baseline failed
  - nonaware baseline also started, but much later and with nonzero back-drive
- `fa_005` mixed-polarity chatter-intended case:
  - champion and fixed both started
  - nonaware baseline failed and accumulated large wrong-way energy (`3.59288e-04 J`)
- `fa_004` and `fa_006`:
  - all three designs failed to start
  - only the nonaware baseline accumulated measurable back-drive in both cases

## What Did Not Survive

- No adversarial case produced a measured handoff fall or second rise.
- The champion still does not show a broad startup-success advantage over the fixed baseline.
- The champion still does not show a back-drive advantage over the fixed baseline in these falsifier cases; the separation is mostly against the nonaware multi-input baseline.

## Kill-Rule Readout

- H1 is **not** killed yet.
- Reason:
  - the adversarial suite finally exposed narrow startup-correctness separation in real stress cases, so the lane still has evidence worth carrying into the decision memo
- H2 and H3 were therefore **not activated** at this stage.
- Narrowed claim boundary after falsifier pass:
  - helper-free source-aware startup may help mainly by avoiding nonaware multi-input failure modes under collapse and mixed-polarity stress
  - it is not yet a general win over the fixed startup path
