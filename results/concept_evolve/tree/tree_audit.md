# Concept Tree Audit

This note synthesizes the delegated `concept-tree-explorer` pass for rubric item `item_010`.

## Active top 3
- `004_skolem_automatic_intersection_filter` -> `H1`
- `005_convergent_hankel_detector` -> `H1`
- `009_pisot_beta_endpoint_sampler` -> `H2`

## Audit outcomes
- Every surviving concept folder now has an `alignment` tag (`H1`, `H2`, `H3`, or `retire`) inside its `concept.json` file.
- Every surviving concept folder now has one concrete `proposed_baseline_experiment` in machine-readable form.
- `results/concept_evolve/tree/index.json` was regenerated to point at the actual underscore-based folders rather than the stale hyphenated paths.
- `results/concept_evolve/tree/active_graph.json` records the promoted bridge graph used for the baseline and champion/backup workflows.

## Hygiene fixes applied
- Removed the duplicate hyphenated concept directories created during the interrupted evolve kickoff.
- Rebuilt the tree index after fixing the slug convention in `.archivara/concept_evolve.py`.

## Remaining research debt
- The tree is tagged, but experiment artifacts still need to be attached to at least half of the folders before sign-off.
- `results/literature/gap_frontier.md` and `results/swarm/gap_map.md` remain weak inputs for later novelty synthesis.
