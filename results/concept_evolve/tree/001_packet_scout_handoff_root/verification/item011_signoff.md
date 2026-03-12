# Item 011 Sign-Off

Date: 2026-03-12
Scope: baseline-set and metric review before champion implementation
Status: PASS with guardrails

## Execution Note

- Attempted delegated `worker`, `benchmark_auditor`, and `falsifier` child reviews via `codex exec`.
- Result: responses-proxy disconnects prevented those child runs from writing their target files.
- Fallback used here:
  - direct parent review over the same file set, with the role outputs preserved as explicit sections below so the gate is documented instead of skipped.

## Worker Review

- Baseline inventory:
  - `netlists/baselines/fixed_startup_path/fixed_startup_path.cir`
  - `netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir`
- Shared-hook parity:
  - both baselines use the same `source_pair_models.inc`, `startup_cells.inc`, and `measurement_hooks.inc`
  - both expose `n_src_a`, `n_src_b`, `n_src_a_p`, `n_src_a_n`, `n_src_b_p`, `n_src_b_n`, `n_store`, `n_handoff`, and `n_ctrl`
  - both include `VMEAS_A`, `VMEAS_B`, and `VCTRL_MON`
- Hidden-helper-rail check:
  - pass
  - there is no extra supply source besides the floating source pair and `CSTORE`
  - control energy is taken from `n_store` through `VCTRL_MON`, not from an unstated bias rail
- Implementation risks:
  - the startup pump is intentionally abstract, so later claims must stay about startup arbitration and isolation behavior, not absolute converter efficiency
  - the nonaware baseline currently differs from the fixed baseline mainly by parallel routing and higher control load; if later stress cases do not activate reverse-loss behavior, the baseline may be too close to the champion's abstraction envelope

## Benchmark Auditor Review

- Verdict: PASS to proceed to champion implementation
- Why this passes:
  - the two required baseline families exist for the same source contract
  - metric definitions are frozen before champion netlists
  - both baseline decks execute locally in `ngspice` and report the shared measures
- Metric completeness:
  - `startup_ok`: present
  - `t_handoff`: present
  - `e_backdrive`: present
  - `e_ctrl`: present
- Explicit rejections:
  - open-loop-only comparisons are rejected as insufficient
  - fixed-threshold-only comparisons are rejected as insufficient
  - a single fixed startup path alone is not enough to validate H1
- Remaining benchmark condition:
  - every champion result must be compared against both current baselines, not against only the weaker fixed-path line

## Falsifier Review

- Main attack surface:
  - the nonaware multi-input baseline is still somewhat optimistic because its full-wave routing abstraction may suppress the very wrong-way current behavior that H1 is meant to control
- Consequence:
  - if champion wins only on `e_ctrl` while `e_backdrive` stays near zero across the matrix, the novelty claim will compress toward "extra logic with slightly better accounting"
- Required guardrails before final claims:
  - keep the mixed-polarity cases in the primary matrix
  - keep the `1:20` impedance asymmetry cases in the primary matrix
  - add later falsifier cases where a source collapses or one path leaks, so the nonaware baseline cannot hide behind benign conditions
- Explicit rejection:
  - do not replace the current baseline pair with fixed-threshold-only or open-loop-only startup comparators; those are weaker than the already implemented baseline set and would invalidate the benchmark gate

## Integrator Decision

- Decision: PASS the baseline gate for core-concept implementation, with two conditions
- Condition 1:
  - retain both current baselines for all later champion comparisons
- Condition 2:
  - if the first adversarial matrix shows negligible `e_backdrive` for the nonaware baseline, revisit the router leakage or coupling assumptions before making any source-awareness claim

## Net Result

- `item_011` is clear to proceed
- The current baseline set is strong enough to block weak comparison drift
- The claim boundary remains narrow:
  - helper-free startup correctness and handoff behavior under heterogeneous weak sources
  - not a claim about universal cold-start superiority or absolute energy-harvesting efficiency
