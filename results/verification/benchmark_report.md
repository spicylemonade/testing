# Benchmark Report

Snapshot date: 2026-03-19 UTC
Verification phase: `post_deepen`

## Scope

This audit reads:

- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/baselines/benchmark_spec.md`
- current experiment outputs under `results/experiments/`

The scope here is narrow: baselines, ablations, controls, stress tests, error
analysis, compute parity, and publication-quality claim boundaries.

The repo currently contains two benchmark states:

- blocker-era documents such as `results/swarm/falsifier.md`,
  `results/experiments/h1_tiny_grid_report.md`,
  `results/experiments/h1_controls.md`, and
  `results/experiments/complexity_sweep.md` still describe a no-verifier,
  `0`-decode regime;
- post-deepen documents such as `results/research_context.md`,
  `results/theory/forcing_trace_normal_form.md`,
  `results/theory/local_rule_no_go_atlas.md`,
  `results/experiments/h1_exact_advantage.md`,
  `results/experiments/macrocell_scaling.md`,
  `results/experiments/arithmetic_sensitivity_phase_transition.md`, and
  `results/experiments/spatial_coupling_threshold.md` assume the exact engine in
  `tools/kakeya_ca_exact.py` exists and was used.

This report treats the exact verifier as present and audits the remaining
benchmark gaps. The stale blocker-era documents are themselves a benchmark
provenance failure.

## Headline Verdict

- Exact evaluator availability: `pass`
- Benchmark provenance consistency: `fail`
- Baseline execution: `fail`
- Control and ablation execution: `fail`
- Error analysis and compute parity reporting: `fail`
- Publication-quality benchmark readiness: `fail`

What survives is narrower: exact negative-result and obstruction claims. What
does not survive is any claim of CA advantage, coupling advantage, scaling
advantage, robustness, or phase-transition behavior.

## What The Current Evidence Actually Shows

- `tools/kakeya_ca_exact.py` is now a real exact verifier, trace engine, and
  bounded search entry point.
- `results/theory/forcing_trace_normal_form.md` and the trace corpus establish
  exact negative structure in the audited `2x2` regime.
- `results/theory/local_rule_no_go_atlas.md` establishes an exact one-sided
  strip obstruction in widths `2` and `3`.
- `results/experiments/h1_exact_advantage.md`,
  `results/experiments/spatial_coupling_threshold.md`,
  `results/experiments/macrocell_scaling.md`, and
  `results/experiments/arithmetic_sensitivity_phase_transition.md` are negative
  feasibility reports, not matched benchmark wins.

That is enough for exact null-result reporting. It is not enough for any
baseline-cleared empirical method claim.

## Missing Baselines

| Claim block | Required baselines | Current state | Why this is insufficient | Falsifiable next test |
| --- | --- | --- | --- | --- |
| `H1` exact advantage | Random Local Search, Whole-Witness Mutation, Decoder-Matched Search | `results/experiments/h1_controls.md` has placeholder rows only; `results/experiments/h1_exact_advantage.md` has no comparator runs or distributions | No evidence isolates CA-specific value from generic search or decoder reuse | On one already audited exact geometry family, run CA plus all three baselines with the same exact decoder, same `X` or `|X|` budget, same density band, and same exact-decode count `N`; kill the empirical `H1` claim if CA fails to beat all three on legality hit rate, forcing hit rate, and median verified score |
| `H1` negative-search efficiency | Same three H1 baselines | Not executed even though exact negative searches now exist | The absence of a positive family does not waive benchmarking; otherwise "the CA search failed in an informative way" is unmeasured | Re-run one reported negative block from `results/experiments/h1_exact_advantage.md` with matched baselines and compare exact-valid yield, legality hit rate, forcing hit rate, and best or median verified score; if all families are equally null, drop CA-specific search-efficiency language |
| `H2` spatial coupling | Uncoupled repetition, Random Local Search, Whole-Witness Mutation | `results/experiments/spatial_coupling_threshold.md` names these only as acceptance criteria; there is no comparator table | No evidence that coupling beats simple repetition or generic search on the same micro-bank | Freeze one micro-bank, two coupling widths, and one slab-count block; kill `H2` if the coupled construction does not beat uncoupled repetition and both non-CA baselines on hit rate or median verified score under the same exact budget |
| `H3` macrocell scaling | Flat-lattice CA, static grammar enumeration, independent local matching | `results/experiments/macrocell_scaling.md` names flat CA and static grammar only as required future comparators; no executed runs | No evidence that macrocell typing adds anything beyond representation or enumeration | Evaluate the same interface bank on the largest held-out macroboard against all required comparators; if there is no win over both flat CA and static grammar, keep the claim purely negative |
| Branch-specific benchmark freezing for `H2` and `H3` | Dedicated frozen benchmark artifacts, not just H1 carryover | `results/swarm/falsifier.md` explicitly says there is no H1-equivalent frozen benchmark artifact for `H2` or `H3` | Without lane-specific matrices, later baseline claims are under-specified and not audit-ready | Write branch-specific benchmark specs before any new promotion; if those specs are absent, treat `H2` and `H3` experiment notes as feasibility memos, not benchmark claims |

## Missing Controls And Ablations

| Missing test | Current state | Why this blocks publication-quality claims | Falsifiable completion criterion |
| --- | --- | --- | --- |
| `X`-label shuffle at fixed geometry | Still unexecuted in the post-deepen experiment set | No evidence the signal depends on arithmetic labels rather than geometry or density | Re-run the same comparison block with fixed geometry and fixed nonzero-label multiset; kill the claim if shuffled runs retain at least `50%` of unshuffled hit rate or at least `75%` of the median-score gain |
| Held-out legal `X` | Mentioned in acceptance criteria, absent as an explicit executed row | Geometry generalization without held-out `X` still allows alphabet overfit | Add a held-out-`X` row with the same cardinality and complexity band; kill the claim if the effect disappears across held-out legal alphabets |
| Held-out larger grids or aspect ratios | `results/experiments/h1_controls.md` is empty; `results/experiments/h1_exact_advantage.md` spans multiple geometries but not as a frozen in-vs-out-of-distribution comparison block | Multi-geometry failure notes are not the same as a generalization test on a fixed promoted family against matched baselines | Freeze one family and one in-distribution block, then evaluate on held-out shapes under the same budget; kill the claim if hit rate falls below `25%` of in-distribution hit rate or the median gain disappears everywhere |
| Small, medium, unrestricted complexity sweep | `results/experiments/complexity_sweep.md` is a blocker-era document and has not been rerun against the exact engine | No evidence clears the bounded-slope trap or the low-rational-complexity trap | Rerun the sweep under the exact engine and matched baselines; kill the claim if gains occur only in `small` and not in `medium` or `unrestricted` |
| Modular-to-integer lift | Still only a placeholder row | Any modular-only effect remains off-target for the integer witness problem | Report a lift result with the same exact score accounting; reject any claim that disappears before integer lift-back |
| Decoder ablation or randomization | Required in the benchmark spec, absent from the experiment outputs | Decoder leakage remains unmeasured even though the verifier now exists | Remove or randomize nonsemantic decoder choices inside the same comparison block; kill the claim if the gain disappears |
| Canonicalization ablation or randomization for `H1` | Named in `results/experiments/h1_exact_advantage.md` only as a future check | No evidence the apparent signal is CA-specific rather than canonicalization-specific | Randomize or ablate canonical class IDs while holding the decoder and budget fixed; kill `H1` if the same effect is reproducible without the claimed proof-state structure |
| Template randomization for `H2` | Named only as an acceptance condition in `results/experiments/spatial_coupling_threshold.md` | A coupling story without template-randomization collapse can still be geometry theater | On the same micro-bank and slab block, randomize the template bank; kill `H2` if the putative coupling gain survives |
| Interface randomization or independent local matching for `H3` | Not executed | Macrocell typing could hide the work in the interface library | Compare against independent local matching or a randomized interface bank under the same exact budget; kill `H3` if the advantage survives |

## Missing Error Analysis And Fairness Reporting

| Missing evidence | Current state | Why this is insufficient | Falsifiable completion criterion |
| --- | --- | --- | --- |
| Full verified score distributions | `results/experiments/h1_exact_advantage.md` reports only best exact forced counts on negative searches; other benchmark rows are empty | Best-of-many or best-forced-count reporting is not the frozen benchmark metric | For every family and baseline, report count, min, quartiles, median, and max of verified score; keep forced-count diagnostics as secondary debug output only |
| Legality hit rate | Missing from the post-deepen experiment notes | Without it, one cannot tell whether a method fails because it proposes illegal witnesses or because legal witnesses still do not force | Report the fraction of proposals that decode to legal witnesses for every family and baseline |
| Forcing hit rate | Missing from the post-deepen experiment notes | Without it, exact-valid yield is unmeasured even in a negative result paper | Report the fraction of legal witnesses that pass exact forcing for every family and baseline |
| Failure-reason distribution | Not broken out beyond "no hit" or "failed to recover a family" | Publication review cannot separate malformed outputs, failed forcing, denominator pathologies, and other failure modes | Count at minimum `illegal X`, `malformed f_i`, `malformed R`, `failed forcing`, `denominator failure`, and `other` in every comparison block |
| Score decomposition | No experiment file exposes `m(G)`, `|R|`, `n(G)`, and `|T|` separately | A branch can look good for the wrong reason if only the collapsed score is shown | Publish the four components beside every reported verified score summary |
| Generator-side compute parity | The benchmark spec warns that exact-decode parity alone is not enough, but the post-deepen experiments do not publish proposal counts, SAT solves, or wall-clock or solver budgets | A CA branch could receive materially more proposer-side compute than its baselines while still claiming matched decode counts | Publish per-family proposal count, exact verifier calls, solver invocations, and wall-clock or solver-step budget; if CA gets materially more search compute, mark the block unmatched |
| Negative-result preservation with candidate-level traceability | Negative outcomes are preserved narratively, but not as full candidate ledgers | Reviewers cannot re-audit whether discarded candidates were illegal, low-score, or simply underreported | Store the candidate ledger for each comparison block, or at minimum an aggregate table that preserves all evaluated candidates inside the fixed budget |
| Benchmark provenance after the exact-trace pivot | Old reports still say no verifier exists while new ones use one | It is unclear which evaluator, budget, and claim boundary are authoritative | Write one post-deepen evaluation manifest naming `tools/kakeya_ca_exact.py`, the active budget table, and every superseded blocker-era benchmark file; if this cannot be done, withdraw cross-document benchmark claims |

## Where The Evidence Is Insufficient For Publication-Quality Claims

The current artifact set does **not** support any of the following claims:

- `H1` beats Random Local Search, Whole-Witness Mutation, or Decoder-Matched Search.
- The observed signal depends on arithmetic labels rather than fixed geometry.
- The decoder is not doing the real work.
- The method generalizes to held-out legal alphabets or held-out aspect ratios.
- The method escapes the bounded-slope or modular-only traps.
- Spatial coupling beats uncoupled repetition or matched non-CA baselines.
- Macrocell typing beats flat-lattice CA or static grammar enumeration.
- There is a measured arithmetic-sensitivity phase transition.

The current artifact set **does** support a narrower claim boundary:

- exact negative-result reporting for the audited search families;
- exact local-obstruction results in the audited `2x2`, width-`2`, and
  width-`3` regimes;
- honest preservation of negative outcomes without substituting proxy success
  metrics.

## Priority Next Checks

1. Freeze a post-deepen benchmark manifest.
   Name the exact evaluator entry point, the comparison budgets, and which
   blocker-era files are superseded. If this cannot be written cleanly, keep
   all benchmark claims at the negative-result level.

2. Run one matched `H1` comparison block on an already audited geometry family.
   Use CA plus Random Local Search, Whole-Witness Mutation, and
   Decoder-Matched Search with identical exact-decode counts, identical
   generator-side compute limits, identical `X` or `|X|` budget, and identical
   density band.

3. Add the frozen benchmark reporting fields to every post-deepen run.
   Report legality hit rate, forcing hit rate, full verified score
   distributions, score decomposition, failure reasons, and compute ledgers.
   Do not headline `best exact forced count` alone.

4. Only if a family has nonzero exact-valid yield, run the mandatory kill tests.
   Apply label shuffle, held-out `X`, held-out geometry, complexity sweep, and
   decoder or canonicalization ablations with the thresholds already written in
   `results/core/lane_gates.md`.

5. Keep `H2` and `H3` benchmark claims closed until their lane-specific
   baselines and randomization controls are frozen and executed.
   Without uncoupled repetition, template randomization, flat-lattice CA,
   static grammar, and interface-matching controls, those lanes are still
   feasibility stories rather than benchmark-cleared results.
