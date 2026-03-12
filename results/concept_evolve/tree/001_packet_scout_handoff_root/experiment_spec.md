# H1 Experiment Spec

This file freezes the source model and measurement contract before any baseline or champion netlist is written.

## Shared Source Model

- Topology:
  - two-source Thevenin input pair feeding a common cold-start front end
- Per-source parameters:
  - `VOC_A`, `VOC_B`: final open-circuit voltage
  - `R_A`, `R_B`: source resistance
  - `POL_A`, `POL_B`: source polarity, encoded as `+1` or `-1`
  - `RAMP_MVPS`: ramp rate in `mV/s`
- Default common values for first implementation:
  - `R_UNIT = 1k`
  - `C_STORE = 10u`
  - `V_HANDOFF = 1.2`
  - `V_HANDOFF_FALL = 1.0`
- Voltage levels that every baseline and the champion must support:
  - `20 mV`
  - `50 mV`
  - `100 mV`
  - `300 mV`
- Ramp rates that every baseline and the champion must support:
  - `0.1 mV/s`
  - `1 mV/s`
  - `10 mV/s`
  - `100 mV/s`
- Impedance ratios that every baseline and the champion must support:
  - `1:1`
  - `1:5`
  - `1:20`
- Mixed-polarity contract:
  - same-polarity nominal: `POL_A = +1`, `POL_B = +1`
  - mixed-polarity stress: `POL_A = +1`, `POL_B = -1`
- No hidden helper rail:
  - every startup and control block must draw energy only from the two source ports and `C_STORE`

## Parameter Mapping

- Baseline resistance mapping:
  - `R_A = R_UNIT`
  - `R_B = ratio * R_UNIT`
- Nominal equal-voltage pair:
  - `VOC_A = VOC_B = VLEVEL`
- Mixed-strength pair for later matrix selection:
  - `VOC_A = VLEVEL`
  - `VOC_B = VLEVEL`
  - impedance asymmetry, not hidden voltage favoritism, creates the ranking problem

## Measurement Hook Contract

Every netlist must expose the same node names and current-sense elements.

- Required nodes:
  - `n_src_a`
  - `n_src_b`
  - `n_store`
  - `n_handoff`
  - `n_ctrl`
- Required series sense elements:
  - `VMEAS_A`
  - `VMEAS_B`
  - `VCTRL_MON`
- Required measurements to implement in a shared include later:
  - `startup_ok`
  - `t_handoff`
  - `e_backdrive`
  - `e_ctrl`

## Metric Definitions

### Startup Success

- `startup_ok = 1` only if:
  - `V(n_store)` reaches at least `V_HANDOFF`, and
  - `V(n_handoff)` crosses its enable threshold before `t_stop`, and
  - no auxiliary source outside the declared two-source model was used

### Time-To-Handoff

- `t_handoff` is the first time when both conditions hold:
  - `V(n_store) >= V_HANDOFF`
  - `V(n_handoff)` indicates the main arbiter may take over

### Back-Drive Loss

- `e_backdrive` is the pre-handoff energy pushed the wrong way into either source port:
  - `e_backdrive = sum_i integral(max(0, -P_src_i)) dt`
  - where `P_src_i` is the instantaneous port power measured through `VMEAS_A` or `VMEAS_B`
- The sign convention will be normalized in the shared measurement include so all netlists report the same quantity.

### Startup-Control Energy

- `e_ctrl` is the pre-handoff energy consumed by startup-control logic only:
  - probe clocks
  - ranking logic
  - UVLO and handoff gating
  - arbitration logic that exists before the main converter is alive
- Measurement rule:
  - all explicit control-only branches must pass through `VCTRL_MON`
  - if a baseline has no separate controller, its isolation or arbitration devices must still be counted through the same control monitor path

## Stop-Time Rule

- The transient stop time for a case is:
  - `t_stop = max(1.25 * VLEVEL / RAMP_MVPS, 8 * R_EQ * C_STORE)`
- `R_EQ` is the smaller of `R_A` and `R_B`
- The exact per-case `t_stop` used in experiments will be stored in the case manifest under `results/manifests/`

## Interpretation Guardrails

- Do not claim a win from steady-state conversion efficiency alone.
- Do not count reverse-current suppression as a win unless `startup_ok` or `t_handoff` also improves under equal accounting.
- Do not compare against baselines that hide control energy in an idealized source or a precharged node.
