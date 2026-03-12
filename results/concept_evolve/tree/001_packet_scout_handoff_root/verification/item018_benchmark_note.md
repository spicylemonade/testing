# Item 018 Benchmark Note

Date: 2026-03-12
Scope: benchmark the H1 champion against both required baselines under equal accounting
Status: PASS as a benchmark artifact, but no measured champion advantage yet

## Inputs

- Manifest:
  - `results/manifests/startup_matrix_manifest.json`
- Run log:
  - `results/manifests/startup_runlog.jsonl`
- Flat long-form results:
  - `tables/startup_results.csv`
- Wide comparison table with literature mapping:
  - `tables/benchmark_comparison.csv`
- Aggregate benchmark summary:
  - `tables/benchmark_summary.json`
- Equal-accounting basis:
  - shared `VCTRL_MON`, `VMEAS_A`, `VMEAS_B`, and `measurement_hooks.inc`

## Coverage

- Executed cases:
  - `24`
- Designs compared per case:
  - `champion`
  - `fixed`
  - `nonaware`
- Total benchmark rows:
  - `72`
- Literature-family mapping:
  - same-polarity low-asymmetry cases map to the recovered TEG startup family
  - same-polarity impedance-spread cases map to the multi-source PMU and interface family
  - mixed-polarity cases map to the closest 2024 multi-input self-powered interface family, with the most extreme mixed cases also tagged against the helper-assisted low-voltage startup falsifier

## Measured Result

- Startup success:
  - the champion, fixed baseline, and nonaware baseline all succeed in `17/24` cases
- Time to handoff:
  - median successful `t_handoff` is `18.5522 s` for the champion
  - median successful `t_handoff` is `18.2153 s` for the fixed baseline
  - median successful `t_handoff` is `18.2712 s` for the nonaware baseline
- Back-drive loss:
  - `e_backdrive = 0` for every design in every primary-matrix case
- Startup-control energy:
  - median `e_ctrl` is `8.313151e-05 J` for the champion
  - median `e_ctrl` is `1.0235677e-04 J` for the fixed baseline
  - median `e_ctrl` is `1.2973635e-04 J` for the nonaware baseline

## Pairwise Readout

- Champion versus fixed baseline:
  - better startup count: `0`
  - faster successful handoff cases: `6`
  - lower control-energy cases: `13`
  - lower back-drive cases: `0`
- Champion versus nonaware baseline:
  - better startup count: `0`
  - faster successful handoff cases: `5`
  - lower control-energy cases: `22`
  - lower back-drive cases: `0`

## Interpretation Guardrail

- This benchmark does not yet support the headline H1 source-awareness claim.
- The reason is load-bearing:
  - the primary matrix shows no startup-success improvement and no back-drive separation relative to either baseline
- What survives from this artifact:
  - the champion sometimes reduces startup-control energy
  - the champion does not obviously win on startup correctness in the present matrix
- Consequence for the next phase:
  - the falsifier cases must stress source collapse, mixed polarity, extreme asymmetry, and chatter paths hard enough to reveal whether the current zero-back-drive result is a modeling artifact or a real null result
