# Benchmark Report

Snapshot date: 2026-03-18 UTC

## Scope

This is an audit of the blocked phase-4 experiment pass, not an audit of successful H1 evidence.

Inputs audited:

- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`
- `results/baselines/benchmark_spec.md`
- `results/core/lane_gates.md`
- `results/verification/verification_summary.md`

Required specialist roles used for this checkpoint:

- `monitor`
- `benchmark_auditor`
- `falsifier`
- `integrator`

The child audit turns were launched against the artifact set above. They completed without writing additional files, so the synthesized judgment below is grounded directly in the audited inputs.

## Overall Judgment

- Experimental-evidence status: `blocked`
- Benchmark-integrity status: `pass with blocker`

The run did not execute exact experiments, but it did preserve the benchmark plan honestly instead of substituting proxy metrics or uneven compute.

## Audit Findings

### Matched budgets
- Judgment: `pass`
- Finding: the planned first-gate budget remained fully unspent:
  - H1 families run: `0 / 3`
  - exact decodes per family: `0 / 10^3`
  - promoted families for controls: `0`
- Consequence: no method, CA or non-CA, received an unfair decode advantage.

### Identical decoder usage
- Judgment: `blocked but preserved`
- Finding: no exact decoder was available, so no method used a decoder at all.
- Consequence: there is no decoder asymmetry in the recorded pass, but there is also no executable evidence. The benchmark remains blocked until a real exact decoder/verifier exists.

### Full score accounting
- Judgment: `pass`
- Finding: the artifacts preserve the exact target score `(m(G)+|R|)/(n(G)-|T|)` and leave score fields as `not available` or `[]` rather than inserting proxy values.
- Consequence: the run did not leak into surrogate metrics such as pattern density, modular behavior, or heuristic certificate counts.

### Negative-result preservation
- Judgment: `pass`
- Finding: the blocker is recorded consistently across the sweep, control, and complexity artifacts; empty distributions are written explicitly rather than omitted.
- Consequence: the phase-4 record remains falsifiable and audit-ready.

### Later-phase closure
- Judgment: `pass`
- Finding: `h1_tiny_grid_report.md` explicitly keeps later experiment items closed, `h1_controls.md` records no promoted families, and `complexity_sweep.md` records no exact-valid regimes.
- Consequence: the run does not accidentally imply that controls or sweeps were passed.

## Benchmark Risk Notes

- The only unresolved integrity risk is infrastructural, not comparative: the missing exact decoder/verifier prevents any non-vacuous compute-parity comparison.
- Because nothing ran, the current parity result is a degenerate one: fair by non-execution, but not yet informative about method quality.

## Minimum Conclusion

The benchmark framework stayed disciplined under the blocker:

- matched budgets were preserved,
- identical decoder usage was blocked uniformly,
- full score accounting was preserved,
- and negative results were preserved.

