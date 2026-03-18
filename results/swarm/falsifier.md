# Falsifier Memo: Hadamard 668 via "Cellar/Cellular" Automata

Scope:
- This memo targets the CA-flavored hypotheses in `results/swarm/hypothesis_negative_space.md` and `results/swarm/hypothesis_bridge.md`.
- I interpret "cellar automata" as either a typo for `cellular automata` or an unstable rebrand. Do not build a novelty claim on the phrase itself.

## Hard external facts that narrow the target

- As of the 2025 primary literature, order `668` is still treated as the smallest open case in Hadamard's conjecture. That matters because any novelty claim will be judged against an open-problem standard, not against toy-order success. `[Eliahou 2025]`
- The strongest recent positive result is not an exact Hadamard matrix, but a `64`-modular Hadamard matrix of order `668`. Eliahou's 2025 construction gives rows orthogonal to `641` others, leaving only `26` nonzero off-diagonal Gram entries per row. Any "repair" proposal must compete with this exact near-solution baseline, not with a blank slate. `[Eliahou 2025]`
- The strongest recent negative-space reduction is even sharper: in the circulant Goethals-Seidel route to order `668`, one must determine whether a binary vector of length `167` and weight `80` exists with a specific prescribed autocorrelation vector once three other length-`167` vectors have been fixed. Any CA proposal that does not touch this exact `167`-length autocorrelation-realizability problem is probably off-target. `[Constantine and Constantine 2025]`
- The CA/design literature is not blank territory. The 2025 survey is centered on CA-generated orthogonal Latin squares, orthogonal arrays, and cryptographic design objects. CA-derived bent-function work explicitly passes through Hadamard matrices, but through narrow, highly structured subclasses. So the claim cannot be "CA has never touched Hadamard-like objects." The only defensible claim is narrower: "CA has not yet been shown to help with the specific order-668 obstruction." `[Manzoni, Mariot, and Menara 2025] [Gadouleau, Mariot, and Picek 2020]`
- CA reachability is a real risk, not a formality. Recent controllability work shows that only peripherally linear rules are fully controllable, while for other Boolean 1D CA the reachability ratio vanishes as system size grows. A CA family with poor reachability can fail simply because it never comes near the needed certificate class. `[Bagnoli, Dridi, and Fates 2025]`

## Highest-risk novelty illusions

- **"Cellular automata for Hadamard 668 is completely untried."** Too broad. Direct order-`668` CA search appears underexplored, but adjacent CA work already covers orthogonal design generation, bent-function/Hadamard structure, and CA-based heuristic search. A reviewer can kill an overbroad novelty claim immediately. `[Manzoni, Mariot, and Menara 2025] [Gadouleau, Mariot, and Picek 2020] [Mariot et al. 2021/2022]`
- **"Prime-length `167` CA search is a new search space."** Probably false if the CA stays inside four circulant components or Williamson-type encodings. For odd prime `n`, Williamson-type solutions with circulant components collapse to cyclic shifts of classical Williamson solutions. At `n = 167`, a circulant CA can easily be just a new updater on an old ansatz. `[Fitzpatrick and O'Keeffe 2023]`
- **"Defect-transport CA is new."** Only partly. CA as a local repair/decoder layer is a known paradigm in other constraint systems. Without a Hadamard-specific invariant or a coverage argument, this looks like generic local search with a CA wrapper. `[Herold et al. 2015]`
- **"Rule-space search is novel because it is more compact."** Weak. Compactness is not novelty unless it yields better certificate rate, better reachability, or stronger pruning than direct search on the same constrained objects.
- **"Cellar automata" is a distinct method class.** Weak and unstable. In context it reads like a typo for `cellular automata`; if reinterpreted as a stack/pushdown automaton, the proposal becomes a pruning language for a classical search tree, not a new CA dynamics.

## Hypothesis-by-hypothesis easiest failure modes

### 1. Autocorrelation-realization CA on the `167`-cycle

- Fastest failure: CA-generated supports do not outperform direct search on raw weight-`80` subsets when both are scored only against the exact periodic-autocorrelation target from the cyclic reduction. `[Constantine and Constantine 2025]`
- Cleanest rehash accusation: the CA reachable set stays inside cyclic/circulant/Goethals-Seidel/SDS-like families already studied by exact or structured search.
- Literature branch that can invalidate weak claims: circulant Williamson-type theory for odd primes. If the state space is effectively four circulant components, the "new" method is probably not new. `[Fitzpatrick and O'Keeffe 2023]`
- Missing control: compare against direct search over the same weight-`80` support space with the same symmetry reduction, same evaluation budget, and same exact verifier.
- Missing control: include a solved positive control from the same Goethals-Seidel/circulant template, not just toy orders from unrelated families. The `4 x 79` worked example in the convolution-number paper is the obvious minimum. `[Constantine and Constantine 2025]`
- Benchmark trap: beating random subsets is not meaningful here. The target is a single highly structured `167/80` object, not a generic low-energy region.

### 2. Defect-transport / modulus-lifting CA from the `64`-modular seed

- Fastest failure: defect mass decreases but exact certification never improves. The method can look active while never removing the hard `26`-defect residue of the best current seed. `[Eliahou 2025]`
- Cleanest rehash accusation: the update rule is just simulated annealing, greedy balanced sign-swaps, or quantum/Ising-style local search rewritten in CA language. The Hadamard-search literature already has SA, simulated quantum annealing, quantum annealing, and QAOA formulations. `[Suksmono 2016/2018] [Suksmono 2019/2022] [Suksmono 2025]`
- Literature branch that can invalidate weak claims: CA decoders/repair layers. Local defect motion by CA is already an established pattern outside Hadamard search, so novelty must come from the Hadamard-specific defect encoding, not from "CA repairs defects." `[Herold et al. 2015]`
- Missing controls:
  - same-seed non-CA local search,
  - same-neighborhood greedy or annealed sign-swaps,
  - smaller solved modular-to-exact lift tasks before touching `668`.
- Benchmark trap: letting the CA start from Eliahou's `64`-modular seed while baselines start cold.

### 3. Orbit/path-representative CA or visibly-pushdown pruning

- Fastest failure: it cannot reconstruct known smaller certificates or even the published `64`-modular `668` seed.
- Cleanest rehash accusation: this is equivalence-aware branch-and-bound or SAT+CAS filtering on a compressed encoding, not a genuinely new method.
- Literature branch that can invalidate weak claims: SAT+CAS and exact structured enumeration. If the automaton's pruning power comes from hard-coded algebraic constraints rather than dynamical discovery, the automaton is presentation, not contribution. `[Bright, Kotsireas, and Ganesh 2018]`
- Missing control: matched exact search on the same path/run-length representation without the automaton.
- Benchmark trap: reporting only random-prefix rejection rates instead of end-to-end certificate rate and wall clock.

### 4. CA rule/seed quality-diversity

- Fastest failure: the archive collapses to trivial periodic or low-entropy orbits that look diverse under weak descriptors but are equivalent under shifts/complements.
- Cleanest rehash accusation: CA-based heuristic search is already established in adjacent design/Boolean-function work; rule evolution and heuristic optimization are not new on their own. `[Mariot et al. 2021/2022]`
- Literature branch that can invalidate weak claims: CA-derived bent/semi-bent search. If direct quality-diversity or evolutionary search on raw supports covers the same descriptor space, the CA layer is cosmetic. `[Gadouleau, Mariot, and Picek 2020] [Mariot et al. 2021/2022]`
- Missing control: direct QD over raw `167`-bit supports with the same descriptors and the same exact verifier.

## Missing controls weak papers usually skip

- **Exact-target control:** recover solved smaller instances and, at minimum, reproduce the published `64`-modular `668` seed. `[Eliahou 2025]`
- **Same-template positive control:** include at least one solved `4 x p` circulant Goethals-Seidel instance before touching `p = 167`. `[Constantine and Constantine 2025]`
- **Representation control:** compare CA rule-space search against direct search over the exact same structured objects.
- **Non-CA local-search control:** same neighborhood, same constraints, same verifier, no CA.
- **Reachability control:** prove or estimate how much of the candidate space the chosen CA family can even reach. `[Bagnoli, Dridi, and Fates 2025]`
- **Equivalence control:** quotient by cyclic shifts, reversals, complements, and block symmetries before claiming diversity or coverage.
- **Certificate control:** report exact witnesses or exact modulus lifts, not just lower defect mass, lower autocorrelation distance, or visually interesting patterns.
- **Negative controls:** random rule families, random balanced subsets, and intentionally weak local rules.

## Benchmark traps

- **Random-baseline trap:** beating uniform random supports proves almost nothing for the `167/80` obstruction.
- **Metric-leakage trap:** autocorrelation distance or defect mass may not correlate tightly with exact certification.
- **Seed unfairness trap:** the proposed method gets the `64`-modular seed, baselines do not.
- **Compression trap:** the proposal uses path/run-length compression but baselines are left in raw coordinates.
- **Toy-order trap:** strong results only on tiny orders where many methods succeed, while the prime-length `167` case behaves differently.

## Literature branches that can kill weak claims quickly

- **Exact/structured Hadamard search:** Goethals-Seidel, modular Golay quadruples, supplementary difference sets, Williamson/Turyn variants, and SAT+CAS enumeration. `[Bright, Kotsireas, and Ganesh 2018]`
- **Heuristic Hadamard search:** simulated annealing, simulated quantum annealing, quantum annealing, and QAOA are already on the board. `[Suksmono 2016/2018] [Suksmono 2019/2022] [Suksmono 2025]`
- **CA combinatorial-design literature:** orthogonal Latin squares, orthogonal arrays, and CA-derived bent/Hadamard structure already exist. `[Mariot, Formenti, and Leporati 2016] [Gadouleau, Mariot, and Picek 2020] [Manzoni, Mariot, and Menara 2025]`
- **CA controllability/reachability literature:** many rule families cover vanishingly small fractions of state space at scale. `[Bagnoli, Dridi, and Fates 2025]`
- **CA decoder/repair literature:** local defect propagation by CA is already mature outside Hadamard search. `[Herold et al. 2015]`

## Bottom line

- The only defensible novelty claim is narrow:
  - target either the exact `167/80` cyclic obstruction or the published `64`-modular `668` defect pattern,
  - show matched baselines against exact search and non-CA local search,
  - prove the CA reaches more than a classical structured-family reparameterization.
- Anything broader is easy to attack as off-target, derivative, or a transfer of known CA ideas into a setting where the hard part remains elsewhere.

## Source anchors

- `[Eliahou 2025]` M. Eliahou, *A 64-modular Hadamard matrix of order 668*, Australasian Journal of Combinatorics 93(2), 2025.
- `[Constantine and Constantine 2025]` G. Constantine and T. Constantine, *Convolution numbers: the cyclic case*, arXiv:2501.18066, 2025.
- `[Fitzpatrick and O'Keeffe 2023]` P. Fitzpatrick and H. O'Keeffe, *Williamson type Hadamard matrices with circulant components*, Discrete Mathematics 346(12), 113615, 2023.
- `[Bright, Kotsireas, and Ganesh 2018]` C. Bright, I. S. Kotsireas, and V. Ganesh, *A SAT+CAS Method for Enumerating Williamson Matrices of Even Order*, AAAI 2018.
- `[Suksmono 2016/2018]` A. B. Suksmono, *Finding a Hadamard Matrix by Simulated Annealing of Spin-Vectors*, arXiv:1606.03815; and *Finding a Hadamard Matrix by Simulated Quantum Annealing*, Entropy 20(2):141, 2018.
- `[Suksmono 2019/2022]` A. B. Suksmono, *Finding Hadamard Matrices by a Quantum Annealing Machine*, Scientific Reports 9, 2019; A. B. Suksmono and Y. Minato, *Quantum computing formulation of some classical Hadamard matrix searching methods and its implementation on a quantum computer*, Scientific Reports 12, 2022.
- `[Suksmono 2025]` A. B. Suksmono, *A quantum approximate optimization method for finding Hadamard matrices*, Scientific Reports 15, 2025.
- `[Mariot, Formenti, and Leporati 2016]` L. Mariot, E. Formenti, and A. Leporati, *Constructing Orthogonal Latin Squares from Linear Cellular Automata*, arXiv:1610.00139, 2016.
- `[Gadouleau, Mariot, and Picek 2020]` M. Gadouleau, L. Mariot, and S. Picek, *Bent Functions from Cellular Automata*, IACR ePrint 2020/1272.
- `[Mariot et al. 2021/2022]` L. Mariot, M. Saletta, A. Leporati, and L. Manzoni, *Heuristic Search of (Semi-)Bent Functions based on Cellular Automata*, arXiv:2111.13248 / Natural Computing, 2022.
- `[Manzoni, Mariot, and Menara 2025]` L. Manzoni, L. Mariot, and G. Menara, *Combinatorial Designs and Cellular Automata: A Survey*, arXiv:2503.10320, 2025.
- `[Bagnoli, Dridi, and Fates 2025]` F. Bagnoli, S. Dridi, and N. Fates, *Regional Controllability of Cellular Automata as a SAT Problem*, arXiv:2504.03691, 2025.
- `[Herold et al. 2015]` M. Herold, E. T. Campbell, J. Eisert, and M. J. Kastoryano, *Cellular-automaton decoders for topological quantum memories*, npj Quantum Information 1, 15010, 2015.
