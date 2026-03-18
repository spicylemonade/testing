# Novelty Report

## Scope

This audit evaluates the claims actually made in `research_paper.tex` against the closest named prior art and the repo's own gap notes. It follows the narrowed framing already present in:

- `results/literature/prior_art_gap.md`
- `results/swarm/falsifier.md`
- `results/analysis/novelty_collapse_audit.md`

The lexical watchlist remains useful as query-noise control, but it is not the main novelty burden. The real comparison set is:

- exact Hadamard anchors and structured search,
- heuristic Hadamard search,
- CA-based combinatorial-design and Hadamard-adjacent search,
- reserve branches that risk collapsing into exact pruning with CA branding.

## Executive Call

- Positive method novelty: fail.
- Narrow negative-result contribution: pass.
- Main reason: the repo is materially distinct only as a matched-control no-go on exact `668`-relevant artifacts. It is not materially distinct as a new general search paradigm, a new Hadamard construction, or a validated literal `cellar automata` method.

## Major-Claim Audit

### 1. Exact artifact reconstruction and benchmark framing

- Claimed contribution:
  - the paper reconstructs the `4 x 79` same-template control, the exact `167/80` cyclic obstruction, the published mod-`64` order-`668` seed, and the structured `n = 9` control.
- Closest paper or line of work:
  - Constantine and Constantine, *Convolution numbers: the cyclic case* (2025);
  - Eliahou, *A 64-modular Hadamard matrix of order 668* (2025).
- Distinctness call:
  - weak but acceptable as packaging.
- Overlap signal:
  - the mathematical objects are imported from the primary sources rather than discovered here; the paper's contribution is artifactization and matched benchmarking, not a new reduction or construction.
- Weak differentiation:
  - this is not stand-alone mathematical novelty. It is only useful insofar as it enables the later matched-control no-go claim.
- Missing gap evidence:
  - none required beyond honest wording, but the manuscript should not market artifact reconstruction itself as a new scientific result.

### 2. `H1`: support-space CA on the exact `167/80` cyclic obstruction

- Claimed contribution:
  - a CA-style local rule on raw weight-`80` supports over `Z/167Z`, tested against the exact cyclic obstruction.
- Closest paper or line of work:
  - Constantine and Constantine (2025) for the exact target object;
  - heuristic Hadamard search and same-space direct local search for the method comparison class;
  - structured Hadamard-family work only as a collapse guardrail.
- Concrete overlap signal:
  - in `hadamard668/h1.py`, `parallel_gain_ca` and `direct_greedy` inspect the same admissible adjacent swaps, score them with the same exact objective, and share the same phase schedule and `phase_move_cap`; the real difference is move-selection policy.
- Distinctness call:
  - distinct enough to benchmark fairly, not distinct enough to sustain a positive method claim.
- Weak differentiation:
  - the branch does not supply a new cyclic reduction, a new exact solver, or a new search space.
  - once the code is inspected, the method delta is narrow: local-dominance selection versus best-improving selection on the same neighborhood.
- Missing gap evidence:
  - no reachability advantage over ordinary same-space local search;
  - `results/analysis/experiment_readout.md` and the manuscript's H1 results both show `direct_greedy` visiting more unique orbits and winning on both the `4 x 79` control and the exact `167/80` target.
- Closest-paper verdict:
  - relative to Constantine and Constantine, the work is only a benchmark on their exact obstruction.
  - relative to same-space local search, the work is not a surviving new method because the matched baseline wins.

### 3. `H2`: defect-transport CA on the published mod-`64` order-`668` seed

- Claimed contribution:
  - a CA-style local repair rule on structured `(q, s)` states derived from Eliahou's published seed.
- Closest paper or line of work:
  - Eliahou (2025) for the seed and defect structure;
  - heuristic Hadamard-search papers by Suksmono and coauthors as the nearest heuristic competitor family;
  - CA decoder / local-repair work as the nearest non-Hadamard guardrail.
- Concrete overlap signal:
  - in `hadamard668/h2.py`, `parallel_gain_ca` and `direct_greedy` inspect the same parity-phased candidate flips, score them with the same modular objective, and share the same declared variable family and `phase_move_cap`; again, the main difference is move selection.
- Distinctness call:
  - weaker than `H1`.
- Weak differentiation:
  - the branch is not a new modular-Hadamard construction and should not be framed as progress on modular-Hadamard theory.
  - without a certificate-rate, reachability, or quality advantage over matched local search, `H2` reads as a local-search wrapper with CA branding.
- Missing gap evidence:
  - the `n = 9` ladder is not discriminative because random controls solve most starts;
  - on the only real degraded order-`668` start, the CA ties the matched baseline exactly on every decisive metric.
- Closest-paper verdict:
  - relative to Eliahou, this is a repair benchmark on a published seed, not a new construction.
  - relative to prior heuristic Hadamard search, the branch does not establish a materially new algorithmic capability.

### 4. Fairness, invariants, and local-delta proofs

- Claimed contribution:
  - the paper proves invariants, exact local-delta formulas, connectivity statements, and fairness properties for the executed rules.
- Closest paper or line of work:
  - implementation-specific audit lemmas for local search and benchmark interpretation, not a distinct Hadamard or CA research line.
- Distinctness call:
  - useful for auditability, weak as novelty.
- Concrete overlap signal:
  - the propositions mostly certify what the code already enforces: conserved weight or variable family, exact candidate scoring, connectivity of the chosen local graph, and candidate-set identity between CA and baseline.
- Weak differentiation:
  - these results justify interpretation of the benchmark, but they are not an independent mathematical advance once the methods themselves lose or tie.
- Missing gap evidence:
  - none if the paper presents them as audit support;
  - serious overclaim risk if they are framed as stand-alone theory contributions rather than as fairness locks.

### 5. Broad claim: `CA for Hadamard-like search is new`

- Claimed contribution at risk:
  - any wording that implies CA had not already reached combinatorial-design or Hadamard-adjacent search.
- Closest paper or line of work:
  - Manzoni, Mariot, and Menara, *Combinatorial Designs and Cellular Automata: A Survey* (2025);
  - Mariot, Formenti, and Leporati (2016) on orthogonal Latin squares from linear CA;
  - Gadouleau, Mariot, and Picek (2020) and Mariot et al. (2021/2022) on CA-based bent and semi-bent search.
- Distinctness call:
  - fail.
- Overlap signal:
  - CA already appears in design generation and Hadamard-adjacent Boolean-function search;
  - the repo's own prior-art notes already treat this as settled.
- Weak differentiation:
  - the paper can only claim novelty at the level of the exact `167/80` obstruction and the published mod-`64` seed under matched controls.
  - it cannot claim that `CA meets Hadamard-like objects` is itself new.
- Missing gap evidence:
  - none available, because the literature already blocks the broad claim.

### 6. Structured exact-search and family-parameter collapse risk

- Claimed contribution at risk:
  - any wording that lets the work drift into circulant / Williamson / Goethals-Seidel / SAT+CAS territory.
- Closest paper or line of work:
  - Bright, Kotsireas, and Ganesh, *A SAT+CAS Method for Enumerating Williamson Matrices of Even Order* (2018);
  - Fitzpatrick and O'Keeffe, *Williamson type Hadamard matrices with circulant components* (2023);
  - Djokovic and Kotsireas, *Goethals-Seidel Difference Families with Symmetric or Skew Base Blocks* (2018).
- Distinctness call:
  - pass as a defensive differentiation, not as affirmative novelty.
- Overlap signal:
  - the current executed branches operate on raw support or defect states rather than family parameters, and the manuscript is careful about that.
- Weak differentiation:
  - this distinction prevents novelty collapse into exact-search literature, but it does not by itself create a strong new contribution.
- Missing gap evidence:
  - for reserve symbolic branches, a future paper would need to prove the automaton is doing more than exact pruning or equivalence-aware filtering.

### 7. Literal `cellar` / pushdown and other reserve branches

- Claimed contribution:
  - the manuscript treats literal `cellar automata` as a reserve pushdown-style idea with deferred autocorrelation debt.
- Closest paper or line of work:
  - SAT+CAS and other structured exact-pruning methods;
  - compressed / symbolic search representations more broadly.
- Distinctness call:
  - unresolved and unvalidated.
- Overlap signal:
  - this branch changes the state representation materially, which is the main reason it survives as a reserve concept;
  - but without an executed transition system and matched comparator, it is still easier to read as a pruning presentation than as a validated new automaton family.
- Weak differentiation:
  - the representation change is promising enough to keep as a hypothesis;
  - it is not evidence-backed novelty and should receive no credit from the failed `H1/H2` packet.
- Missing gap evidence:
  - no transition system,
  - no matched non-automaton comparator,
  - no solved positive control in that representation,
  - no end-to-end win over static prefix filtering or exact pruning.

## Novelty Illusions To Remove

- The lexical watchlist items are not meaningful technical comparators for the active claim. They are evidence of query drift, not evidence that the novelty burden has been met.
- The executed branch names overstate method distance. In both `H1` and `H2`, the CA and non-CA baselines share state, neighborhood, objective, verifier, budget, and accepted-move cap; the decisive method delta is move selection.
- `Defect transport` is not a novelty claim by itself. Without a measurable advantage over matched local repair, it collapses into an ordinary heuristic wrapper.
- The paper did not discover a validated CA route to order `668`. It discovered that two carefully specified CA rule families fail under matched controls.
- The phrase `cellar automata` is not a contribution. Until a formal model, matched comparator, and positive control exist, it is only a reserve label.

## Missing Gap Evidence That Blocks Any Stronger Claim

- Evidence that the CA rules reach certificate-relevant states that same-space non-CA local search does not.
- A discriminative positive control for `H2`; the current `n = 9` ladder is too easy to support a mechanism claim.
- More than one real degraded `668` start for `H2` if the project ever wants to generalize beyond rejection of the executed branch.
- Proof that any reserve symbolic / pushdown branch beats a matched non-automaton search rather than merely rephrasing exact pruning.

## Surviving Contribution

The only materially distinct, evidence-backed claim is narrow:

- the repo implemented two Hadamard-specific CA-style search branches tied to the exact `167/80` cyclic obstruction and the published mod-`64` order-`668` seed;
- it benchmarked them against matched same-representation non-CA controls;
- the implemented CA rules did not beat those controls.

That is a legitimate negative-result contribution. Anything broader collapses into known prior art, weak differentiation, or missing gap evidence already flagged in `results/literature/prior_art_gap.md` and `results/analysis/novelty_collapse_audit.md`.

VERDICT: REVISE
