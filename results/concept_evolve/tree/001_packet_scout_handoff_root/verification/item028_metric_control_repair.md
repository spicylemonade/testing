# Item 028 Metric And Control Repair

Date: 2026-03-12
Scope: repair the DEEPEN experiment contract before any confidence-gated promotion run
Status: PASS

## What Changed

- Replaced the old `handoff_flag` switch-based output in `netlists/shared/startup_cells.inc` with a small hysteretic behavioral latch.
  - reason:
    - the previous `n_handoff` node sat effectively high from time zero in the abstract decks, which made explicit event timing impossible and hid the contract drift behind store-threshold proxies
- Updated `netlists/shared/measurement_hooks.inc`.
  - canonical event metrics now come from explicit `n_handoff` events
  - store-threshold times are still recorded as diagnostic proxies:
    - `t_store_proxy`
    - `t_store_proxy_fall`
    - `t_store_proxy_rise2`
- Repaired the same-scaffold no-packet control in `netlists/ablations/blind_packet_merge/blind_packet_merge.cir`.
  - the control now reuses `packet_scout_blocks.inc`
  - packet isolation is removed by a direct merged startup path inside `blind_packet_merge_gate`
  - scout observation branches and `VCTRL_MON` accounting remain on the shared scaffold
- Extended the shared runners so `blind_packet_merge` is callable through:
  - `tools/run_h1_matrix.py`
  - `tools/run_h1_falsifier.py`
  - `tools/run_h1_robustness.py`

## Smoke Tests

All smoke tests were executed through the shared Python runners with temporary netlists outside the tracked raw-results tree.

### `blind_packet_merge` startup smoke test

- Case:
  - `sm_002`
- Result:
  - return code `0`
  - `startup_ok = 1`
  - `t_handoff = 18.3217 s`
  - `t_store_proxy = 18.2449 s`
  - `handoff_seen_final = 0.6704915`

### `blind_packet_merge` falsifier smoke test

- Case:
  - `fa_001`
- Result:
  - return code `0`
  - `startup_ok = 1`
  - `t_handoff = 10.9354 s`
  - `t_store_proxy = 10.8334 s`
  - `handoff_seen_final = 0.6704915`

### Cross-check on the existing comparison set

- Case:
  - `sm_002`
- All four packet-family decks now execute with explicit handoff timing:
  - `champion`: `t_handoff = 18.6235 s`, `t_store_proxy = 18.5461 s`
  - `source_blind`: `t_handoff = 18.6412 s`, `t_store_proxy = 18.5637 s`
  - `time_constant_ranked`: `t_handoff = 18.4678 s`, `t_store_proxy = 18.3911 s`
  - `blind_packet_merge`: `t_handoff = 18.3217 s`, `t_store_proxy = 18.2449 s`

## Acceptance Check

- Explicit `n_handoff` events are now measurable and parseable.
- `startup_ok` now depends on both store threshold and observed handoff activity.
- The same-scaffold no-packet control runs under the shared tooling with equal accounting.
- The DEEPEN lane can proceed to confidence-gated implementation without relying on the old store-only proxy contract.
