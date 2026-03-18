# Novelty Report

## Scope

This audit evaluates the contribution actually supported by the current repo artifacts, code, and experiment packet. It treats the lexical watchlist as noise control only and focuses on the exact Hadamard anchors, the closest heuristic and CA-adjacent lines, and the reserve branches that remain after the fairness-corrected `H1/H2` failures.

## Executive Call

- Positive method novelty: fail.
- Narrow negative-result contribution: pass.
- Main reason: the repo targeted the right exact objects, but the implemented CA rules are usually only a thin scheduler change on top of the same neighborhoods, objectives, and verifier contracts used by the matched non-CA baselines.

## Claim-By-Claim Comparison

### 1. `H1`: autocorrelation-realization CA on the exact `167/80` cyclic obstruction

- Closest object prior art: Constantine and Constantine (2025), which supplies the exact unresolved length-`167`, weight-`80` cyclic autocorrelation target and the `4 x 79` same-template control.
- Closest method line: heuristic Hadamard search on fixed structured objects, especially the simulated-annealing / quantum-annealing / QAOA family, plus plain same-space direct local search.
- Concrete overlap signal:
  - the repo does not introduce a new reduction of the `167/80` problem;
  - in `hadamard668/h1.py`, `parallel_gain_ca` and `direct_greedy` enumerate the same admissible adjacent swaps on the same odd-cycle matching schedule, score them with the same exact target-distance objective, and share the same `phase_move_cap`;
  - the main algorithmic difference is local-dominance selection versus taking the best improving swaps.
- Distinctness call: distinct enough to benchmark fairly, not distinct enough to sustain a positive algorithmic contribution once the matched baseline wins.
- Weak differentiation:
  - the branch is novel only at the level of "apply this local update policy to this exact obstruction";
  - it is not a new mathematical formulation, not a new search space, and not a demonstrated reachability improvement over same-space local search.
- Missing gap evidence:
  - no evidence that the CA reaches certificate-relevant states unavailable to ordinary local search;
  - the repo's own orbit logging cuts the other way, with `direct_greedy` visiting more unique orbits on both the solved control and the target sweep;
  - after the fairness-corrected rerun, `direct_greedy` beats `parallel_gain_ca` on both decisive `H1` sweeps.

### 2. `H2`: defect-transport CA on the published `64`-modular order-`668` seed

- Closest object prior art: Eliahou (2025), which provides the exact published mod-`64` seed and therefore the true near-solution baseline.
- Closest method line: local Hadamard heuristics such as simulated annealing / quantum annealing / QAOA, plus CA decoder / local-repair work outside Hadamard search.
- Concrete overlap signal:
  - the branch does not claim a new modular-Hadamard construction; it starts from Eliahou's seed and applies local flips in a fixed neighborhood;
  - in `hadamard668/h2.py`, `parallel_gain_ca` and `direct_greedy` inspect the same parity-phased candidate flips, score them with the same modular objective, use the same variable family, and share the same `phase_move_cap`;
  - again, the main difference is local-dominance selection versus taking the best improving flips.
- Distinctness call: weaker than `H1`.
- Weak differentiation:
  - "defect transport by CA" is not enough by itself because local defect repair is already a known idea, and Hadamard search already has multiple local heuristic formulations;
  - without a clear certificate-rate or reachability advantage, the branch reads as local search with CA branding.
- Missing gap evidence:
  - the small `n = 9` ladder is not discriminative because random controls solve most starts;
  - the decisive degraded-`668` seed attempt ties the matched non-CA baseline on every load-bearing metric, so the repo shows no method-level gain beyond task-specific framing.

### 3. Broad claim: "`cellular automata` for Hadamard-like objects is untried"

- Closest line of work: the CA/design literature summarized by Manzoni, Mariot, and Menara (2025), together with CA-based bent and semi-bent function work and older CA design-generation papers.
- Distinctness call: fail.
- Overlap signal:
  - CA is already present in combinatorial-design generation, Boolean-function search, and Hadamard-adjacent structure;
  - the repo's own gap notes already say the literature is not blank territory here.
- Novelty implication:
  - the repo can only claim novelty at the level of the exact `167/80` obstruction or the published mod-`64` seed under matched controls;
  - it cannot claim that "CA meets Hadamard search" is itself new.

### 4. Reserve claims: literal `cellar` / pushdown, `sat_user_propagator_ca`, and `convolution_slice_ca`

- Closest paper or line of work:
  - SAT+CAS and equivalence-aware exact search for compressed or symbolic filtering;
  - the exact cyclic obstruction line around Constantine and Constantine (2025) for support-side reparameterizations;
  - CA controllability and decoder-style repair work for message-passing or frontier-control narratives.
- Distinctness call: unproven.
- `autocorrelation_debt_pushdown` / literal `cellar`
  - strongest surviving reserve idea because it changes the information channel from flat local updates to deferred-debt state on canonical orbit words;
  - still highly vulnerable to collapse into static prefix filtering or SAT+CAS packaging;
  - missing gap evidence: show better-than-static prefix filtering on the same tokenization, preserve same-template positive controls, and beat a non-automaton search under the same exact-oracle budget.
- `sat_user_propagator_ca`
  - borderline distinctness only if exact conflicts become local, reusable online proposal updates;
  - otherwise it is just SAT+CAS with CA branding;
  - missing gap evidence: locality, reuse, safety, and end-to-end win over a static filter plus exact solver.
- `convolution_slice_ca`
  - the cleanest H1-side representation change, but still vulnerable to being only a relabeling of the failed support-space search;
  - missing gap evidence: prove the liability field is the primary search object, not just a coordinate change, then beat a same-representation non-CA comparator with the same symmetry reduction, positive control, and exact verifier.

## Novelty Illusions To Remove

- The lexical watchlist items are not substantive comparators for the active branch. They are seed-query noise guards, not evidence that the novelty burden has been met.
- The branch names overstate the method distance. In both executed branches, the CA and non-CA baselines share state, neighborhood, objective, verifier, and move cap; the main delta is move selection policy.
- The repo did not discover a validated CA route to order `668`. It discovered that two carefully scoped CA rule families fail under matched controls.
- The phrase `cellar automata` is not a contribution. Without a formal model and benchmark win, it is only an unstable label for reserve concepts.

## Surviving Contribution

The only claim that survives as materially distinct and evidence-backed is narrow:

- the repo implemented Hadamard-specific search branches tied to the exact `167/80` cyclic obstruction and the published mod-`64` order-`668` seed;
- it benchmarked those branches against matched same-representation non-CA controls;
- the implemented CA rules did not beat those controls.

That is a legitimate negative-result contribution. Anything stronger collapses into existing prior art, weak differentiation, or missing gap evidence.

VERDICT: REVISE
