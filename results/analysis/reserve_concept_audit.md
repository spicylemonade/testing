# Reserve Concept Audit

Prepared for rubric `item_013`.

## Commands and artifacts used

- Existing concept tree from `evolve`: `results/concept_evolve/tree/index.json`, `adjacency.json`, `walk_paths.json`
- Recovered reserve probe: `results/concept_evolve/probe_result.json`
- Verification-context reframe: `results/concept_evolve/reframings.json`
- Verification-context iterate pass: `results/concept_evolve/concept_delta.json`, `results/concept_evolve/bridge_candidates.json`
- Literal-branch walk: `python3 .archivara/concept_evolve.py walk --seed pushdown --depth 4`
- Supporting reserve selection memo: `results/analysis/phase3_hypothesis_selection.md`

## Labeled reserve branches

### `R1` `autocorrelation_debt_pushdown`

- Status: retained as champion reserve
- Why retained:
  - it is the clearest literal reading of `cellar automata`;
  - it changes the state language from flat local CA updates to canonical-path prefix filtering with deferred debt;
  - it stays tied to the exact `167/80` obstruction.
- Why not promoted:
  - no transition system or benchmark exists yet;
  - it can still collapse into ordinary prefix pruning or SAT+CAS packaging.
  - `iterate` promotes it only as the leading bridge for future work, not as an executed success.

### `R2` `sat_user_propagator_ca`

- Status: retained as backup reserve
- Why retained:
  - it adds adaptive exact-feedback loops rather than repeating the failed flat CA rules;
  - it is a plausible way to turn exact conflicts into reusable local vetoes.
- Why not promoted:
  - no matched static-propagator baseline exists yet;
  - it remains borderline with SAT+CAS unless the feedback loop proves measurable value.

### `R3` `convolution_slice_ca`

- Status: retained as secondary reserve
- Why retained:
  - it is the cleanest alternate state representation on the H1 side;
  - it localizes the exact cyclic obstruction into liability fields rather than raw support bits.
- Why not promoted:
  - it still needs its own same-representation non-CA comparator;
  - it must prove that the liability state adds more than a relabeling of support search.

### `R4` `density_classifier_support_repair`

- Status: retired
- Why retired:
  - it is too close to the already tested support-space CA family;
  - its own backlog collapses to the same kind of neighborhood-vs-hill-climbing comparison that H1 already lost.

## Literal `cellar automata` call

The literal reading now exists in the repo as a formal reserve concept:

- it is not another 1D cellular rule;
- it is a pushdown or prefix-debt filter over canonical path encodings of the `167/80` target;
- it should be described as a reserve automaton-theoretic pivot, not as a validated CA result.

The reframe pass also surfaced a reservoir-computing interpretation of the phrase `cellar automata`, but the iterate pass retired that reading as too weakly connected to the exact obstruction and too vulnerable to novelty illusion.

## Promotion gates

Any reserve branch must satisfy all of the following before promotion:

- a new design brief and a new matched non-CA comparator;
- retention of known smaller positive controls;
- exact verifier integration and equivalence-aware accounting;
- evidence that the branch's gain comes from its stateful mechanism, not only from compression or canonicalization.
