# Falsifier Memo: Hadamard 668 via "Cellar" / Cellular Automata

Scope:
- This memo attacks the current and likely reopen branches around Hadamard order `668`.
- It treats the implemented `H1` and `H2` branches as already tested and retired, and the literal `cellar` reading as reserve-only.
- Budget posture: do not invent new methods here except to state what a reopened branch would have to prove before it deserves any budget.

## Executive kill shot

The easiest falsifier is already inside the repo:

- `H1` lost to the matched non-CA baseline on both the solved `4 x 79` control and the real `167/80` target.
- `H2` tied the matched non-CA baseline exactly on the decisive degraded order-`668` seed attempt.
- `H3` / literal `cellar` remains unexecuted reserve only and cannot inherit credit from `H1/H2`.

So the burden is no longer "maybe CA helps with Hadamard 668." The burden is much narrower:

- does a reopened branch use a materially different information channel than the failed raw-support swaps and `s`-flip defect transport;
- does it beat a same-representation non-CA comparator;
- does it survive a prior-art collapse audit against exact Hadamard and CA-design literature.

If the answer to any of those is no, kill the branch immediately.

## Hard facts that make weak claims easy to attack

- Order `668` is still treated in the recent literature as an open exact Hadamard case, so toy-order success or soft-metric improvement is not enough.
- The best current foothold is Eliahou's `64`-modular order-`668` matrix, not an exact Hadamard witness. Any "repair" claim must compete against that published near-solution, not against a cold start.
- Constantine and Constantine reduce the circulant Goethals-Seidel route at order `668` to the exact `167/80` cyclic autocorrelation realizability problem. Any search branch that does not touch that obstruction or the published modular seed is probably off-target.
- CA is not new to Hadamard-adjacent objects. The live prior-art burden is against CA work on combinatorial designs and bent-function search, plus direct heuristic Hadamard search.
- The phrase `cellar automata` is not contribution-grade novelty. In this repo it is, at best, a reserve label for a pushdown/prefix-debt automaton; externally, the phrase already appears in unrelated literature.

## Current branch status

### `H1` raw-support CA on the exact `167/80` obstruction

Immediate failure test:
- If the reopen keeps the same support-bit state, same adjacent-swap neighborhood, and same exact target-distance objective, it is already dead.

Why:
- On the solved `4 x 79` control, `direct_greedy` beat `parallel_gain_ca` on mean best distance (`41.5` vs `48.375`) and median unique orbits (`13` vs `4`).
- On the actual `167/80` target sweep, neither method found a witness, and `direct_greedy` again beat `parallel_gain_ca` on mean best distance (`147.917` vs `188.5`) while visiting more unique orbits.

Rehash accusation:
- If the reachable states collapse into a classical circulant / Goethals-Seidel / Williamson-style family, the branch is only a new updater on an old structured ansatz.
- If the only change is parallel local firing instead of greedy choice on the same swap neighborhood, the branch is a local-search wrapper, not a new method family.

Missing controls that would invalidate any weak claim:
- same support representation;
- same symmetry reduction;
- same move cap and step budget;
- same exact verifier;
- same-template solved positive control before touching `167`.

### `H2` defect-transport CA from the published `64`-modular `668` seed

Immediate failure test:
- If the reopen keeps fixed `q`, searches only by local `s` flips, and optimizes the same modular-defect objective, it is already dead.

Why:
- The decisive order-`668` attempt starts from a deterministic degradation of the published seed.
- `parallel_gain_ca` and `direct_greedy` tied exactly on every load-bearing metric:
  - `two_adic_modulus = 16`
  - `l1_defect = 2944`
  - `defect_count = 25`
  - `max_defect_magnitude = 496`
  - accepted moves `= 48`

Rehash accusation:
- If the update rule is only an annealing / greedy / Ising-style local move policy written in CA language, it collapses into the existing heuristic Hadamard-search family.
- If the branch sells local defect motion itself as novel, it collapses into generic CA-decoder / local-repair rhetoric.

Missing controls that would invalidate any weak claim:
- same-seed non-CA comparator;
- same neighborhood and phase schedule;
- same modular verifier;
- same cold-start or same-seed conditions across methods;
- a smaller solved lift task that discriminates better than the current toy ladder.

### Literal `cellar` / pushdown / prefix-debt reserve branch

Immediate failure test:
- If the branch does not define a new state representation and a same-representation non-CA comparator before experiments, kill it.

Why:
- The repo keeps the literal `cellar` reading only as `autocorrelation_debt_pushdown`, a reserve concept over canonical path encodings of the exact `167/80` obstruction.
- No executed benchmark exists.
- The branch is already flagged as highly vulnerable to collapsing into static prefix pruning, branch-and-bound, or SAT+CAS packaging.

Rehash accusation:
- If the "automaton" is just a compressed search tree with hard-coded algebraic guards, it is presentation, not contribution.
- If solver conflicts are only replayed as ordinary propagation constraints, the branch becomes SAT+CAS with CA branding.
- If the gain comes from canonicalization or compression alone, the automaton is not doing the work.

Missing controls that would invalidate any weak claim:
- one solved same-template positive control under the same representation;
- one matched non-automaton search on the same canonical/path encoding;
- witness retention, false-negative rate, and wall clock, not just prefix rejection;
- proof that deferred debt carries information the comparator does not already expose.

### Secondary reserve branches

`convolution_slice_ca`
- Kill it if the liability-field state is only a relabeling of raw support search.
- Kill it if a same-representation non-CA liability search matches it.

`sat_user_propagator_ca`
- Kill it if learned conflicts stay global, nonreusable, or equivalent to ordinary exact pruning.
- Kill it if the only observed gain is fewer solver calls without unchanged witness retention.

## Novelty illusions to reject on sight

- "Cellular automata for Hadamard-like search is untried."
  False. CA already appears in combinatorial-design generation and bent / semi-bent search.

- "Cellar automata" is a distinct new method class.
  Weak. The phrase is unstable, already used elsewhere, and in this repo names only a reserve hypothesis.

- "The order-668 search starts from scratch."
  False. The published `64`-modular seed is already the positive anchor.

- "Soft metric improvement means real progress."
  False. The repo's own decisive comparison shows that lower defect or distance on toy settings can fail to translate into any exact or modulus-lift gain on the real `668` attempt.

- "More explored states means better reachability."
  False. Negative controls can explore broadly and still lose on the real objective.

- "Prime-length `167` CA search is automatically new."
  False if the reachable family reduces to circulant / supplementary-difference-set / Williamson machinery already present in the literature.

## Missing controls weak papers usually skip

- exact same-representation comparator;
- same verifier and same neighborhood;
- same seed privilege across methods;
- same-template solved positive control;
- equivalence-aware accounting;
- exact witness or exact modulus-lift reporting rather than only surrogate metrics;
- negative controls that separate "more motion" from "better search";
- a novelty note against exact Hadamard anchors and CA-design anchors before claiming progress.

If any reopened branch skips these, the paper should be treated as invalid by construction.

## Benchmark traps

- Toy-ladder trap:
  The current `n = 9` lift ladder is a sanity check, not evidence of CA-specific promise. Random controls also solve most starts.

- Random-baseline trap:
  Beating random subsets or random rules proves little about the exact `167/80` obstruction.

- Metric-leakage trap:
  Lower autocorrelation distance or lower defect mass can fail to correlate with exact certification.

- Seed-unfairness trap:
  Giving the proposed method the published `64`-modular seed while baselines start elsewhere invalidates the comparison.

- Compression trap:
  Letting the proposed branch use canonical/path compression while the baseline stays in raw coordinates turns representation into hidden budget.

- Family-leakage trap:
  If family parameters, exact-solver artifacts, or stronger invariants are exposed only to the proposed method, the comparison is broken.

## Literature branches that invalidate weak claims quickly

### Exact Hadamard / structured-search anchors

- Constantine and Constantine (2025): exact `167/80` cyclic obstruction and solved `4 x 79` control.
- Eliahou (2025): published `64`-modular order-`668` seed.
- Bright, Kotsireas, and Ganesh (2018): SAT+CAS enumeration of Williamson matrices.
- Programmatic SAT / exact-search literature around Williamson and complex Golay objects.
- Fitzpatrick and O'Keeffe (2023) plus Goethals-Seidel / SDS family references: family-level collapse checks.

These kill any branch that quietly becomes exact structured search, family-parameter search, or proof packaging.

### Direct heuristic Hadamard-search competitors

- Simulated annealing of spin vectors.
- Simulated quantum annealing.
- Quantum annealing formulations.
- Quantum-computing reformulations of classical Hadamard search.
- QAOA for Hadamard matrices.

These kill any claim that "a new heuristic search wrapper for Hadamard matrices" is enough by itself.

### CA-side prior art

- CA survey work on combinatorial designs.
- Orthogonal Latin squares from linear CA.
- Bent-function construction from CA.
- Heuristic search for semi-bent / bent functions based on CA.
- CA controllability / SAT-reachability work.
- CA decoder / local-repair work.

These kill any broad claim of novelty for "CA meets Hadamard-like discrete structure" or "CA moves defects locally."

### Phrase-level novelty failure

- The literal phrase `cellar automata` already appears in unrelated literature, so the phrase itself cannot carry novelty.

## Bottom line

- The implemented cellular-automata program is already a no-go under matched controls.
- Any reopened branch is falsified immediately if it reuses the `H1` raw-support swap channel or the `H2` `s`-flip defect-transport channel.
- Any literal `cellar` reopen survives only as a reserve branch with:
  - a new state representation,
  - a same-representation non-CA comparator,
  - a solved same-template positive control,
  - the same verifier and equivalence accounting,
  - and a fresh novelty-collapse audit.

Without that, the easiest honest verdict is:

- rehash of prior heuristic search,
- rebranding of exact pruning,
- or another local-search wrapper that already failed in this repo.

## Evidence anchors

Local repo:
- `results/analysis/baseline_benchmark_sheet.md`
- `results/analysis/kill_rules.md`
- `results/analysis/experiment_readout.md`
- `results/analysis/phase2_baseline_review.md`
- `results/analysis/phase3_hypothesis_selection.md`
- `results/analysis/novelty_collapse_audit.md`
- `results/analysis/reserve_concept_audit.md`
- `results/analysis/phase5_final_evidence_gate.md`

External literature:
- M. Eliahou, *A 64-modular Hadamard matrix of order 668* (2025).
- G. Constantine and T. Constantine, *Convolution numbers: the cyclic case* (2025).
- C. Bright, I. S. Kotsireas, and V. Ganesh, *A SAT+CAS Method for Enumerating Williamson Matrices of Even Order* (2018).
- P. Fitzpatrick and H. O'Keeffe, *Williamson type Hadamard matrices with circulant components* (2023).
- A. B. Suksmono heuristic and quantum Hadamard-search papers (2016, 2018, 2019, 2022, 2025).
- L. Manzoni, L. Mariot, and G. Menara, *Combinatorial Designs and Cellular Automata: A Survey* (2025).
- L. Mariot, E. Formenti, and A. Leporati, *Constructing Orthogonal Latin Squares from Linear Cellular Automata* (2016).
- M. Gadouleau, L. Mariot, and S. Picek, *Bent Functions from Cellular Automata* (2020).
- L. Mariot et al., *Heuristic search of (semi-)bent functions based on cellular automata* (2021/2022).
- F. Bagnoli, S. Dridi, and N. Fates, *Regional controllability of cellular automata as a SAT problem* (2025).
- M. Herold et al., *Cellular-automaton decoders for topological quantum memories* (2015).
- M. L. Scott et al., *Cellar automata models for reservoir computing and stretching of liquid marbles* (2024).
