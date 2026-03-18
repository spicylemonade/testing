# Baseline Audit

Snapshot date: 2026-03-18 UTC

## Inputs

- `results/baselines/benchmark_spec.md`
- `results/baselines/witness_spec.md`
- `results/verification/verification_summary.md`
- `results/swarm/tool_plan.md`
- `results/swarm/falsifier.md`
- specialist review passes from `benchmark_auditor`, `falsifier`, and `integrator`

## Checklist

| Control | Status | Notes |
| --- | --- | --- |
| Label shuffling | Pass | The benchmark plan requires fixed-geometry, fixed-label-multiset `X` shuffles and the tool plan makes shuffle collapse a hard gate. |
| Decoder leakage | Fail | The benchmark plan now includes decoder-matched and decoder-ablation controls, but leakage cannot be audited cleanly because no exact verifier/decoder entry point exists in the current snapshot. |
| Compute parity | Pass | The plan fixes matched exact-decode counts, matched `X` or `|X|`, matched edge-density bands, and forbids best-of-many-only reporting. |
| Out-of-distribution grids | Pass | Larger or different-aspect-ratio held-out grids are required, including for decoder-matched baselines. |
| Rational-complexity sweeps | Pass after patch | The falsifier correctly flagged the original spec as underspecified. The benchmark spec was updated to use a primitive-label surrogate complexity `c(a,b) = max(|a'|,|b'|)` with explicit small / medium / unrestricted regimes. |

## Sharpest Remaining Weakness

The verifier gap still dominates. Without an independent exact decode-and-verify path, decoder leakage remains a live failure mode and the rest of the matrix is a policy document rather than an enforceable audit.

## Overall Verdict

- Planning readiness: pass
- Execution readiness: conditional fail

The baseline matrix is acceptable as a pre-run specification, but no baseline or CA comparison should actually run until the exact verifier blocker is resolved.
