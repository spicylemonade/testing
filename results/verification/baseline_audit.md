# Baseline Audit

Pre-run audit date: 2026-03-18 UTC

Inputs reviewed:

- `results/baselines/benchmark_spec.md`
- `results/baselines/witness_spec.md`
- `results/swarm/falsifier.md`
- `results/swarm/tool_plan.md`
- `results/verification/verification_summary.md`

Required review roles for this checkpoint:

- `benchmark_auditor`
- `falsifier`
- `integrator`

## Verdict

- Baseline-plan status: `pass`
- Execution status: `blocked`

The baseline matrix is structurally acceptable for a first exact-verification pass, but no run is authorized until an exact verifier exists.

## Checklist

### Label shuffling

- Status: `pass`
- Reason:
  - `results/baselines/benchmark_spec.md` explicitly includes a label-shuffled geometry control with fixed graph geometry and fixed nonzero-label multiset.

### Decoder leakage

- Status: `pass`
- Reason:
  - the spec includes a decoder-matched non-CA baseline using the same compiler/extractor path and forbids repair.
  - this is the minimum control required to test whether the decoder is doing the hard work.

### Compute parity

- Status: `pass`
- Reason:
  - parity is defined by exact-decode count rather than wall-clock time.
  - illegal candidates still count against budget.
  - all methods are required to share the same exact-decode, alphabet, and density budgets.

### Out-of-distribution grids

- Status: `pass`
- Reason:
  - the benchmark spec now explicitly requires at least one larger or different-aspect-ratio held-out grid family for any promoted method.

### Rational-complexity sweeps

- Status: `pass`
- Reason:
  - the benchmark spec now explicitly requires small-, medium-, and unrestricted-complexity `X` regimes under matched budgets.

## Additional Audit Notes

- Distribution reporting:
  - `pass`
  - hit rate and full score distributions are required; best-of-many-only reporting is forbidden.
- Score accounting:
  - `pass`
  - the shared evaluator target remains the full score `(m(G)+|R|)/(n(G)-|T|)`.
- Verifier dependency:
  - `fail-open blocker`
  - no exact evaluator exists, so this audit clears the plan only, not execution.

## Required Next Step

Do not run the CA lane or any baseline until the exact verifier blocker in `results/verification/verification_summary.md` is resolved or the run is formally closed as a no-go.
