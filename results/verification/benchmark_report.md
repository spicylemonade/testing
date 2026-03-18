# Benchmark Report

Snapshot date: 2026-03-18 UTC

## Scope

This audit reviews:

- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/baselines/benchmark_spec.md`
- `results/baselines/witness_spec.md`
- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`
- `results/verification/verification_summary.md`
- `results/core/lane_gates.md`
- `results/swarm/tool_plan.md`
- `results/swarm/phase_3_h1_review.md`

The question is narrow: does the current artifact set support publication-quality benchmark claims about `H1` relative to matched baselines and mandatory controls?

## Headline Verdict

- Blocker-handling integrity: `pass`
- Benchmark evidence for empirical claims: `fail`
- Publication-quality readiness: `fail`

The current outputs show honest blocker handling, not benchmark evidence. The tiny-grid sweep records `0 / 3` H1 families and `0` exact decodes; the control and complexity reports are empty by design. That preserves compute hygiene and negative results, but it leaves every empirical benchmark claim untested.

## What The Current Artifacts Actually Establish

- The benchmark matrix is specified clearly enough to audit later.
- The exact score `(m(G)+|R|)/(n(G)-|T|)` remained the only admissible objective.
- No proxy score, permissive decoder, or repaired witness was substituted.
- The run preserved negative results honestly by reporting blocked status and empty distributions.

Those are process strengths, not benchmark outcomes. They do not show baseline superiority, robustness, decoder independence, or generalization.

## Missing Evidence By Category

### Baselines

| Required evidence | Current state | Audit judgment | Falsifiable completion criterion |
| --- | --- | --- | --- |
| Random local search baseline | Defined in `results/baselines/benchmark_spec.md`, never executed | missing | Run on the same grid block with the same `X` or `|X|`, density band, decoder, and exact-decode count `N` as the CA family; report legality hit rate, forcing hit rate, and full score distribution |
| Whole-witness mutation baseline | Defined in `results/baselines/benchmark_spec.md`, never executed, and not broken out separately in `results/experiments/h1_controls.md` | missing plus reporting gap | Give it its own comparison row and matched-budget distribution; do not merge it into a generic non-CA bucket |
| Decoder-matched search baseline | Placeholder exists in `results/experiments/h1_controls.md`, but executions and distributions are empty | missing | Run with the identical decoder, extractor, legality checks, and verifier stack; if CA gains vanish here, the decoder is doing the work |

### Ablations And Controls

| Required evidence | Current state | Audit judgment | Existing kill or pass rule |
| --- | --- | --- | --- |
| `X`-label shuffle at fixed geometry | Planned, not executed | missing | Kill `H1` if shuffled runs retain at least `50%` of unshuffled hit rate or at least `75%` of the median-score gain over matched baselines |
| Decoder ablation or decoder randomization | Required in `results/baselines/benchmark_spec.md`, absent from phase-4 outputs | missing | Kill the CA-specific claim if removing nonessential decoder choices removes the effect |
| Matched-budget parity in actual runs | Planned and documented, never exercised | missing execution evidence | Require identical exact-decode count `N` for CA and every baseline in the same comparison block |
| No-repair runtime audit | Design rule exists, but no decoded run log shows rejection counts for malformed candidates | missing | Record how many candidates are rejected directly by decode-time legality checks; any repair step is an automatic fail |

### Error Analysis

| Required evidence | Current state | Audit judgment | Falsifiable completion criterion |
| --- | --- | --- | --- |
| Legality hit rate | `not available` | missing | Report per family and per baseline, not only in aggregate |
| Forcing hit rate | `not available` | missing | Report per family and per baseline under the shared exact verifier |
| Failure-reason distribution | The benchmark spec defines categories, but the phase-4 outputs record only the infrastructure blocker | missing | Count at minimum `illegal X`, `malformed f_i`, `malformed R`, `failed forcing`, `denominator failure`, and `other` for every comparison block |
| Restart and seed variance | No family-level score distributions exist | missing | Preserve all scores inside the fixed budget so median and quartile comparisons are meaningful |

### Stress Tests

| Required evidence | Current state | Audit judgment | Existing kill or pass rule |
| --- | --- | --- | --- |
| Held-out larger grids or aspect ratios | Planned, not executed | missing | Kill `H1` if held-out hit rate falls below `25%` of in-distribution hit rate or the median gain disappears on every held-out geometry |
| Held-out alphabets `X` | Required by `results/swarm/falsifier.md` and `results/swarm/phase_3_h1_review.md`, but no phase-4 artifact reserves this test | missing from plan and execution | Add explicit held-out-`X` rows; kill `H1` if the effect disappears across held-out legal alphabets |
| Small, medium, unrestricted complexity sweep | Placeholder exists, no runs | missing | Kill `H1` as bounded-slope trapped if gains occur only in `small` and not in `medium` or `unrestricted` at matched budget |
| Modular curriculum to integer lift | Placeholder exists, no runs | missing | Reject any empirical story that wins only before integer lift-back |
| Equivalent-formulation or encoding transfer | Called out in `results/swarm/falsifier.md`, absent from phase-4 outputs | missing from plan and execution | Re-evaluate the same candidate family under a semantically equivalent serialization or nearby forcing formulation; kill the claim if rankings change materially |

## Where The Evidence Is Insufficient For Publication-Quality Claims

The current artifact set does not support any of the following claims:

- `H1` beats random local search, whole-witness mutation, or decoder-matched search.
- The observed signal depends on arithmetic labels rather than fixed geometry.
- The decoder is not the true source of the gain.
- The method generalizes beyond tiny seen geometries or beyond the tuned alphabet.
- The method escapes bounded-slope or low-rational-complexity traps.
- Any modular or curriculum signal transfers back to the integer target.
- Any family improves exact verified score toward `<= 1.675`.

The only defensible benchmark claim is narrower: the run preserved benchmark hygiene while blocked on the missing exact `(X,G,R,T)` decoder and verifier.

## Priority Next Checks

1. Do not expand search. Recover or implement a shared exact decoder and verifier first.
2. Run one fully matched comparison block: one CA family versus Random Local Search, Whole-Witness Mutation, and Decoder-Matched Search, all on the same grid block with identical `X` or `|X|`, density band, decoder, and exact-decode budget.
3. Split the control report into explicit rows for all three baseline families plus label-shuffle, decoder-ablation, held-out geometry, held-out `X`, and complexity-regime tests.
4. Preserve candidate-level failure reasons and full score distributions for every family and baseline. Without that, there is no publishable error analysis.
5. Apply the existing kill thresholds verbatim once data exists. If the CA signal survives label shuffling, disappears under decoder ablation, vanishes on held-out geometries or alphabets, or wins only in the `small` complexity regime, reject the empirical CA claim.
