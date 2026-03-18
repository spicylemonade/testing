# Active Branch Brief

Prepared for rubric `item_002`.

## Decision

- `H1` champion: **Autocorrelation-Realization CA on the 167-cycle**
- `H2` backup: **Defect-Transport CA lift from the 64-modular 668 seed**
- `H3` reserve: **Orbit- / representation-aware CA on canonicalized 167-supports**

I am keeping the orchestrator's `H1 -> H2 -> H3` ordering. The only explicit addition is a side-check, not a promotion: later concept iteration will test whether the user meant a literal non-cellular "`cellar automata`" model, but that does **not** replace the champion branch unless a formal definition appears.

## Why H1 Stays Champion

- The strongest exact obstruction is the missing length-167, weight-80 support with prescribed cyclic autocorrelation extracted by Constantine and Constantine.
- This branch is the cleanest falsification target: either a CA-style generator reaches that exact obstruction more effectively than same-space direct search, or it does not.
- It keeps the novelty claim narrow enough to survive review: not "CA solves Hadamard search in general," but "CA may help with this one exact unresolved obstruction."

## Why H2 Remains Backup

- Eliahou's 64-modular order-668 construction is the strongest positive foothold, so any repair-style CA should start there rather than from random matrices.
- The branch has crisp metrics: reached modulus, defect count, and max defect magnitude.
- The novelty risk is higher than H1 because this can collapse into ordinary local search with CA branding, so it should only be promoted after H1 fails a registered gate.

## Why H3 Stays Reserve

- The reserve role is for representation changes that might help with reachability or equivalence collapse but are also easiest to reinterpret as ordinary exact search with a different encoding.
- Current concept-evolve outputs surfaced two relevant reserve variants:
  - orbit/path-aware support CA,
  - literal "`cellar`" as an automata-theoretic prefix / pushdown filter.
- Both are worth preserving as fallback ideas, but neither should outrank H1 or H2 before the exact-target and modular-seed baselines are tested.

## Non-Negotiable Kill Rules

### H1 kill rules

- Kill `H1` if it loses to a symmetry-aware direct-search baseline on the same weight-80 support space under the same evaluation budget.
- Kill `H1` if its reachable states collapse into a classical circulant / Williamson / Goethals-Seidel restatement rather than a materially different proposal family.
- Do not spend beyond one modest sweep unless it shows an exact hit, a closest-target advantage, or a reachability argument strong enough to justify more budget.

### H2 kill rules

- Promote `H2` only after `H1` fails cleanly.
- Kill `H2` if the same update budget cannot lift solved smaller controls by one modulus step.
- Kill `H2` if it cannot improve the published order-668 seed beyond modulus 64 under the same-seed, same-neighborhood non-CA comparator.

### H3 kill rules

- Kill `H3` if compressed or path-state search adds no advantage over a non-CA search using the same representation.
- Kill `H3` if the automaton spends most of its effort outside valid canonical states or reduces to a pruning presentation of branch-and-bound / SAT+CAS.
- Do not promote `H3` before H1/H2 unless new evidence shows the user intended a genuinely different formal automaton model.

## Immediate Execution Consequences

1. Extract the exact `167/80` target and the `4 x 79` same-template positive control into machine-usable artifacts.
2. Lock a matched direct-search baseline and verifier contract before any CA sweep.
3. Run one modest H1 control sweep first.
4. Open H2 only if H1 fails that first gate.

## Evidence Inputs Used

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/novelty_guard.json`
- `results/literature/gap_frontier.md`
- `results/swarm/director_brief.md`
- `results/swarm/hypotheses.json`
- `results/swarm/tool_plan.md`
- `results/swarm/falsifier.md`
- `results/concept_evolve/concept_cards.json`
- `results/concept_evolve/steering_directions.json`
