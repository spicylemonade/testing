# Item 030 DEEPEN Near-Tie Matrix

Date: 2026-03-12
Scope: bounded DEEPEN experiment for `H1_confidence_gated_abstention`
Status: PASS with a narrowed survival claim

## Matrix Contract

- Manifest:
  - `results/manifests/deepen_near_tie_manifest.json`
- Runner:
  - `tools/run_h1_deepen.py`
- Core compared designs:
  - `confidence_gated`
  - `source_blind`
  - `time_constant_ranked`
- Same-scaffold control on decisive cases:
  - `blind_packet_merge`
- Case budget:
  - `12` core cases
  - `4` additional no-packet control runs
- Regimes covered:
  - static near ties with small `VOC` offsets:
    - `100/101 mV`
    - `100/103 mV`
    - `100/105 mV`
  - impedance spread:
    - `1:1`
    - `1:3`
  - temporal ambiguity resolution:
    - source B delayed by `4 s`

## Main Artifacts

- Raw results:
  - `results/raw/deepen/`
- Run log:
  - `results/manifests/deepen_near_tie_runlog.jsonl`
- Table:
  - `tables/deepen_results.csv`
- Summary:
  - `tables/deepen_summary.json`
- Figure:
  - `figures/h1_deepen_confidence_tradeoff.svg`

## Key Findings

### 1. The lane survives the pre-registered gate against `source_blind`

- Static near ties:
  - `confidence_gated` startup successes: `6/6`
  - median explicit handoff time: `4.668195 s`
  - median gain versus `source_blind`: `-0.000545 s`
  - commit count: `0/6`
- Late-arrival cases:
  - `confidence_gated` startup successes: `6/6`
  - median explicit handoff time: `5.028505 s`
  - median gain versus `source_blind`: `+0.30882 s`
  - commit count: `6/6`
  - median `t_commit`: `1.02799 s`
- Interpretation:
  - the design does not improve static near ties
  - it does improve cases where the ambiguity resolves temporally

### 2. The interesting result is not “better ranking”; it is temporal separability detection

- On static near ties, the confidence node never commits and the deck collapses to the blind baseline.
- On late-arrival cases, the confidence node commits early and recovers a substantial part of the delay penalty carried by `source_blind`.
- This is the sharpest design-law statement supported by the matrix:
  - confidence gating matters only when the source evidence changes over time; for static near ties it should abstain and stay blind

### 3. The no-packet control reveals a useful frontier

- `blind_packet_merge` median on the four decisive control cases:
  - `t_handoff = 4.67638 s`
  - `e_backdrive = 1.54753e-09 J`
- `confidence_gated` median on the same control cases:
  - `t_handoff = 4.85884 s`
  - `e_backdrive = 0`
- `source_blind` median on the same control cases:
  - `t_handoff = 5.01093 s`
  - `e_backdrive = 0`
- Interpretation:
  - the no-packet merge path is fastest, but it reopens measurable wrong-way energy
  - the confidence-gated path recovers part of the speed gain while keeping the zero-backdrive posture of the packet-isolated family

### 4. `time_constant_ranked` remains faster on this matrix

- Static median explicit handoff time:
  - `4.65209 s`
- Late-arrival median explicit handoff time:
  - `4.673435 s`
- Median gain of `confidence_gated` versus `time_constant_ranked`:
  - static: `-0.01611 s`
  - late: `-0.355075 s`
- Consequence:
  - the DEEPEN lane is not a new best-overall selector
  - it survives only as a bounded abstention controller relative to the blind baseline and the no-packet frontier

## Decision

- Lane outcome:
  - `SURVIVE`, but only with the narrowed claim already encoded in `deepen_summary.json`
- Surviving claim:
  - confidence-gated abstention is useful as a temporal-separability controller
  - it should not be sold as a universally superior selector or as better than `time_constant_ranked`
- Open risk carried into the final verification pass:
  - the novelty must now be defended as a bounded operating-regime result rather than a broad architecture win
