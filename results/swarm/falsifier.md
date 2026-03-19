# Falsifier Memo

Scope: adversarial memo for the current "solve arithmetic Kakeya using cellular automata" program. Focus: easiest invalidators, prior-art overlap, missing controls, benchmark traps, and novelty illusions. Grounded in `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, and the saved phase-4/5 artifacts.

## Executive Readout

- The current artifact set does not support the headline "solve this using cellular automata." `H1_macrocell_substitution` dies by exact one-seed obstruction before scoring, `H2_target_direction_abelian` is only a four-family local null, `H3_slope_bloom` was never activated, and the only exact surviving witnesses are direct no-CA corridor controls at score `2.0` and `29/14`; see `results/phase4_h1_frontier.md`, `results/phase4_h2_screen.md`, `results/phase5_negative_results.md`, and `results/final_handoff.md`.
- The easiest falsifier is immediate: ask for a legal `(X; d_i; f_i; T; R)` certificate with score `<= 1.675` produced by the CA route itself. No saved artifact clears that bar.
- A genuine CA certificate `<= 1.675` would not be a modest workflow win. It would sit at the current theorem frontier, so weak "CA-guided" language will be attacked as either overclaiming or hiding the real arithmetic mechanism.
- `results/literature/prior_art_watchlist.md` is not novelty evidence. It is dominated by corrupted-token false positives, so the real novelty pressure comes from the arithmetic Kakeya, bootstrap/critical CA, abelian-network, and local-decoder branches listed below.

## Already-Fired Kill Criteria

- `H1_macrocell_substitution`: exact one-seed obstruction fired before any level-1 versus level-2 transfer comparison. The frozen family never produces a real second-label bootstrap start; see `results/phase4_h1_frontier.md`.
- `H2_target_direction_abelian`: killed because support size, rank, and target-solvable count already separate the dead H1 rows from the direct controls on the same tiny family set; see `results/phase4_h2_screen.md`.
- Direct corridor residual: survives only as a fragile finite-size control. Boundary seed removal kills the width-4 witness, `R/T` randomization kills it, and frozen-`X` scaling fails; see `results/phase4_ablations.md`.
- `H3_slope_bloom`: not activated. Any positive or negative claim about H3 is currently speculative; see `results/phase5_negative_results.md`.

## Cross-Cutting Failure Modes

- No exact certificate: a CA trajectory, occupancy picture, decoder threshold, halting claim, or forcing proxy does not count. Only a legal exact certificate with verified score counts.
- Baseline incompleteness: the saved artifacts are missing the pre-registered `baseline_low_height_asymmetric_X`, `baseline_bounded_slope`, and `baseline_slowly_growing_X` rows. Without them, "the CA route failed" is confounded with "the whole fixed-`X` corridor regime is weak"; see `results/verification/benchmark_report.md`.
- Level-2 comparator gap: there is no true matched `2 x 8` direct no-CA baseline using the same 4-nonzero palette and matched budgets. The current width-8 successes are exploratory, one-trial, 3-label rows, so any H1-versus-direct level-2 benchmark claim is incomplete; see `results/phase4_h1_frontier.md` and `results/verification/benchmark_report.md`.
- Proxy leakage: the program says exact score is the target, but seed ranking still uses `forcing_order_fast()` inside search. Any search-efficiency or CA-screening claim is exposed unless the exact-elimination replacement comparator is truly run; see `scripts/ca_kakeya_search.py` and `results/phase4_ablations.md`.
- Hidden complexity: if the method needs growing `X`, growing rule tables, scale-specific macrotiles, bespoke repair passes, or a richer extractor than the scored object exposes, the CA story is cosmetic. Complexity has merely been displaced.
- Baseline unfairness: the direct search controls are not iso-expressive with frozen H1. H1 gets one singleton seed and no initial `T`, while direct search gets `initial_t_budget=2`, up to eight seeds, and looser seed placement. That is an upper control, not a clean apples-to-apples mechanism comparison.
- Symmetry inflation: the policy requires quotienting by sign flips, swaps, relabelings, and other symmetries, but the saved search payloads do not expose canonical IDs. Any hit-rate or diversity claim is vulnerable to duplicate counting.
- Finite-size illusion: the only exact wins live at width `4` and `6` with score `2.0`. Nothing approaches the `1.70` neighborhood, much less `1.675`, and the surviving witnesses are boundary-sensitive.

## Route-Specific Rehash And Failure Risks

### H1: `H1_macrocell_substitution`

- Easiest failure: exact obstruction already kills the route. Any narrative about poor transfer or flat scaling is weaker than the actual falsifier.
- Easiest rehash accusation: "bootstrap percolation / macrocell substitution plus compiler" or "tensor-product gadget search in CA language." If the extractor or boundary repair is doing the mathematical work, the CA is only a search prior.
- Missing controls that would invalidate a weak revival:
  - a true matched `2 x 8` no-CA comparator,
  - iso-expressive seed and initial-`T` budgets,
  - aspect-ratio and `H in {3,4}` rows,
  - stage-order perturbations run before declaring transfer failure or success.
- Immediate invalidator: any H1 fix that adds level-specific interface alphabets, repair passes, richer boundary exceptions, or post-extraction edits is route drift, not evidence for the frozen hypothesis.

### H2: `H2_target_direction_abelian`

- Easiest failure: no incremental predictive lift beyond raw arithmetic features. On the saved four-family screen, the null is almost trivial because the dead H1 rows already have `support_size=1` and `target_solvable_vertices=0`.
- Easiest rehash accusation: "chip-firing / abelian networks relabeling." If rank, Smith form, support, and solvability already explain the data, the abelian vocabulary adds no mathematics.
- Missing controls that would invalidate a weak positive claim:
  - evaluation on the full direct-search archive rather than four family IDs,
  - a true matched width-8 control,
  - retention / ranking metrics for best exact certificates,
  - incremental-lift tests after conditioning on rank, Smith tail, support size, edge density, determinant pattern, and coordinate height.

### H3: `H3_slope_bloom`

- Easiest failure: realized slope set and rational complexity stay bounded or become periodic after exact extraction. Then H3 is just bounded-slope retuning and inherits the known "close to 2" behavior of low-complexity regimes.
- Easiest rehash accusation: "local decoder / sweep CA plus compiler" or "hand-coded slope curriculum." If the gain comes from level-dependent label growth or scheduler complexity, it is not a CA-native arithmetic mechanism.
- Missing controls that would invalidate a weak positive claim:
  - explicit bounded-slope and slowly-growing-`X` baselines,
  - exact extraction to the same certificate grammar as H1,
  - reporting realized slope and rational-complexity statistics rather than decoder-style surrogate metrics,
  - proof that the schedule length and rule description do not grow fast enough to hide the real complexity.

## Benchmark Traps

- Stale target confusion: external FrontierMath materials currently expose both `<= 1.75` and `<= 1.675` wording. Any benchmark claim that quietly uses the easier bar is invalid. The live repo bar is `<= 1.675`.
- Best-of-many storytelling: reporting one lucky witness without a frontier over trials, seeds, and budgets will be dismissed as search noise.
- Width mixing: treating width-4 and width-6 direct controls as sufficient comparators for an H1 level-2 width-8 claim is invalid.
- Palette mixing: comparing 4-nonzero width-4/6 rows to exploratory 3-label width-8 rows is not a matched benchmark.
- Boundary programming masquerading as mechanism: if the witness dies as soon as boundary seeds or initial solved vertices are perturbed, the likely explanation is hand-programmed boundary help, not a scalable CA rule.
- Surrogate substitution: fill time, droplet size, occupancy, decoder threshold, or halting are not score.
- Underlogged traces: without per-trial verifier outcomes, failure reasons, grammar size, active state count, and rational-complexity summaries, hidden complexity cannot be audited.

## Novelty Illusions

- "There are no direct hits for `arithmetic Kakeya cellular automata`, so the idea is novel."
  - False. Literal searches mostly return irrelevant CA hardware or coding papers. A keyword gap is not a novelty argument.
- "The verifier-friendly `X`-constructible / forcing-pair language is a new framework."
  - Weak. The repo's own prior-art gap already treats it as a repackaging inside the Katz-Tao / Green-Ruzsa finite-certificate line.
- "Arithmetic forcing is a cellular automaton."
  - Weak. Rule `(3)` is global integer-span closure, and the exact extractor does the real arithmetic work.
- "The abelian-network interpretation adds new mathematics."
  - Weak unless it beats raw arithmetic descriptors on matched families. The saved H2 screen does not.
- "The direct corridor controls reveal a scalable new mechanism."
  - Weak. They are boundary-sensitive, fail under frozen-`X` scale-up, and often survive random relabeling of `X`, which points toward a corridor or boundary artifact rather than a precise arithmetic mechanism.
- "A CA-based `<= 1.675` witness would just be another search result."
  - False. It would pressure the current arithmetic Kakeya theorem frontier and would be judged against the sum-difference literature, not just against heuristic search papers.

## Literature Branches That Swallow Weak Claims

- Core arithmetic Kakeya / sum-difference line:
  - Katz-Tao on arithmetic projections.
  - Green-Ruzsa on the arithmetic Kakeya conjecture and equivalent forms.
  - Cowen-Breen et al. on pattern-problem reformulations.
  - Pohoata-Zakharov on generalized arithmetic Kakeya.
  - Tao on boundedly many slopes and rational complexity.
- Counterexample and asymmetry warning line:
  - Lemm on new counterexamples for sums-differences.
- Bootstrap / critical CA line that swallows H1-style language:
  - Bollobas-Duminil-Copin-Morris-Smith.
  - Balogh-Bollobas-Morris-Riordan and nearby linear-algebra / bootstrap-percolation work.
  - Hartarsky-Mezei and the bootstrap-percolation difficulty literature.
- Abelian-network / chip-firing line that swallows H2-style language:
  - Bond-Levine I-III.
  - Chan-Levine and nearby critical-group / nonhalting-network work.
- Local-decoder / expander-code line that swallows H3-style language:
  - Sipser-Spielman.
  - Hemenway-Ostrovsky-Wootters.
  - Kubica-Preskill and related local CA decoder papers.

## Bottom Line

- The easiest way the current "solve this using cellular automata" story fails is the simplest one: the repo has no CA-produced exact certificate anywhere near `<= 1.675`.
- The easiest way a future weak claim gets invalidated is not by a deep theorem. It is by asking whether the effect survives exact extraction, matched non-CA baselines, bounded-slope / slowly-growing-`X` controls, symmetry quotienting, and boundary-seed ablations.
- The safest current formulation is narrow and negative: exact H1 obstruction, local H2 null, H3 untested, and fragile direct corridor controls around `2.0`. Anything broader is presently exposed to prior-art overlap, missing controls, or benchmark confounding.
