# Item 029 Confidence-Gated Abstention Variant

Date: 2026-03-12
Scope: implement the DEEPEN champion variant before the near-tie matrix
Status: PASS

## Reframe Call

- Command launched:
  - `python3 .archivara/concept_evolve.py reframe "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Durable helper output:
  - `results/concept_evolve/reframings.json`
- Outcome:
  - the helper again produced no useful framing payload, so the design was frozen directly from the director brief, the probe sub-problem, and the falsifier memo

## Mechanism

- New deck:
  - `netlists/champion/packet_scout_handoff/variant_04_confidence_gated_abstention/confidence_gated_abstention.cir`
- Shared sub-block:
  - `netlists/shared/packet_scout_blocks.inc::confidence_gated_packet_gate`
- Core behavior:
  - measure the normalized scout-margin ratio after a minimum scout amplitude
  - integrate that ratio on `n_conf`
  - keep `sel_a` and `sel_b` in the blind `0.5 / 0.5` posture while `n_commit` is low
  - blend toward the winner after `n_commit` rises
- Extra accounting:
  - the additional confidence logic is charged through `BCTRL_CONF` on the shared `VCTRL_MON` path

## Smoke Tests

All smoke tests were executed through the shared runner code with temporary netlists outside the tracked raw-results tree.

### Late-arrival separator probe

- Case:
  - same-polarity `100 mV` pair
  - `1:1` impedance
  - `10 mV/s`
  - source B suppressed until `2 s`
- Results:
  - `confidence_gated`
    - `startup_ok = 1`
    - `t_commit = 1.02771 s`
    - `t_handoff = 4.73294 s`
    - `e_ctrl = 5.04349e-08 J`
  - `source_blind`
    - `t_handoff = 4.76565 s`
    - `e_ctrl = 4.73809e-08 J`
  - `champion`
    - `t_handoff = 4.72978 s`
    - `e_ctrl = 4.79680e-08 J`
- Readout:
  - the confidence variant commits before handoff and slightly improves over `source_blind` on this clear-separation case while staying near the old champion

### Near-tie abstention probe

- Case:
  - same-polarity `100/103 mV` pair
  - `1:3` impedance
  - `10 mV/s`
- Results:
  - `confidence_gated`
    - `startup_ok = 1`
    - `t_commit = none`
    - `conf_final = 0.01659312`
    - `t_handoff = 4.70396 s`
    - `e_ctrl = 5.33279e-08 J`
  - `source_blind`
    - `t_handoff = 4.70351 s`
    - `e_ctrl = 5.04849e-08 J`
  - `champion`
    - `t_handoff = 4.69966 s`
    - `e_ctrl = 5.04611e-08 J`
- Readout:
  - the confidence node stays below threshold and the deck effectively remains in the blind fallback posture on the ambiguous case

## Acceptance Check

- The new helper-free `ngspice` deck exists on the existing packet scaffold.
- The design exposes `n_conf` and `n_commit` so the DEEPEN experiment can report abstain-to-commit transitions.
- The smoke tests show the intended qualitative behavior:
  - early commit on a clear late-arrival case
  - no commit on a near-tie case
- The lane is ready for the bounded near-tie matrix.
