# Hypothesis Negative Space

## Working Position

- Treat `cellar automata` as `cellular automata`. Neither the repo nor targeted literature checks surfaced a Hadamard-search method family under the former name.
- Do not spend more search budget on `H1_defect_syndrome_ca_64m` as an active direction. It is now the negative control: on the canonical `64`-modular order-`668` seed it never beat the seed objective `13/2880/512`, and exhaustive one-packet and two-packet checks found no improving moves in the current basis.
- Do not spend immediate budget on `H3_spacetime_row_emission_ca`. The repo already marks it reserve-only because direct CA-construction overlap is high and it is weakly tied to the actual order-`668` bottleneck.

## What To Avoid Repeating

The crowded space is already:

- exact or family-restricted search (`SAT+CAS`, `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, block-circulant),
- global energy minimization (`greedy`, `tabu`, `simulated_annealing`, quantum/Ising-style search),
- and direct CA-based construction of adjacent design objects rather than frontier-seeded exact repair.

The remaining negative space is narrower: representation-changing local dynamics around the published `64`-modular seed, especially where prior work either ignored the actuator basis, used lag defects only as scores, or could not scale exact reasoning to the real `668` frontier.

## Direction 1: Anti-Splash Composite Packet Library

### Gap Attacked

Prior work in the repo tested CA rules on the wrong actuator basis. The verified H1 failure says the current single-packet q/s moves are fake-local: a typical one-packet move perturbs about `51` lag slots, and no improving one-packet or two-packet move exists at the canonical seed. The untested question is whether any honest local dynamic appears only after changing the move library itself.

### Hypothesis

Discover symmetry-safe composite packets whose far-field lag effects cancel. The target is a retained library of `2`-packet, `4`-packet, and run-boundary moves with sharply lower lag-splash than the current one-packet basis but with enough frontier leverage to make local search nontrivial again.

### Why This Is Negative-Space

This attacks what prior work ignored: actuator-basis quality. It does not assume raw q/s adjacency is the right geometry, and it does not restart another full-matrix optimizer from scratch.

### First Kill Test

- Enumerate `2`-packet, `4`-packet, and run-boundary composites on the canonical seed and one harder control.
- Keep only packets with sharply lower lag-splash than the one-packet basis and with improving or strategically neutral behavior at the frontier.
- Compare the retained library against the current one-packet basis under identical accounting before adding any new CA rule.

### Angle To Avoid

Do not let this collapse into plain basis engineering or hidden family injection. If the gain comes only from the new packet library and every non-CA baseline benefits equally, the result is a useful preconditioner, not a CA contribution.

## Direction 2: Derived Defect-Packet Influence Graph / LDPC-Style Graph CA

### Gap Attacked

The probe and bridge notes say raw q/s index adjacency is the wrong notion of locality. Prior work in the repo has not yet tested whether locality becomes honest only after moving onto a derived influence graph whose edges reflect exact defect-packet interaction rather than sequence position.

### Hypothesis

Build a sparse bipartite graph with defect checks on one side and retained low-splash packet moves on the other. Defect nodes emit signed messages, packet nodes aggregate only local neighborhood state plus short memory, and an asynchronous graph CA chooses locally winning repairs without falling back to full global rescoring.

### Why This Is Negative-Space

This attacks what prior work failed to test: locality defined by algebraic influence instead of geometry or all-packets scoring. It keeps the method CA-shaped, but in a representation that matches the actual defect topology.

### First Kill Test

- Construct the sparse influence graph from exact delta tables of the retained packet library.
- Compare graph CA, weighted bit-flip, scorer-only, `greedy`, `tabu`, and `simulated_annealing` on the same graph, seed, and budget.
- Instrument neighborhood size, message count, active-node count, and dependence on global rescoring.

### Angle To Avoid

Do not let this become a sparse wrapper around global ranking, a plain syndrome-decoder copy, or a graph that quietly bakes in a classical structured family. If it only works as a preconditioner, label it that way.

## Direction 3: Lag-Residue CA on Four Relaxed 167-Channels

### Gap Attacked

Hadamard and sequence-search work uses autocorrelation defects as certificates, pruning terms, or side scores. It rarely elevates lag residues themselves into the primary CA state that gets repaired. For `668 = 4 x 167`, that omission matters because the repo evidence says the lag field is the more honest local object than the raw packet ring.

### Hypothesis

Represent the search state as four relaxed length-`167` channels and let each lag cell carry residue, short memory, and a proposed repair action. The CA evolves in lag space and decodes back to packet edits only through an exact map. The branch stays alive only if it survives an explicit family-leakage audit.

### Why This Is Negative-Space

This attacks what prior work failed to test: using lag defects as the operative state variable instead of using them only to score moves in a known structured family.

### First Kill Test

- Build one lag-residue representation only.
- Run one matched lag-space non-CA control in the same coordinates.
- Execute a saved leakage audit against `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, and block-circulant collapse before any serious frontier sweep.
- Promote only if the branch improves the seed objective or reaches exactness without family collapse.

### Angle To Avoid

Do not relabel supplementary-sequence or circulant-family search as CA. If successful states canonically map into a known family, relabel the branch as optimizer-over-known-family and stop treating it as negative-space novelty.

## Spend Order

1. Start with Direction 1. It tests the missing actuator-basis hypothesis before reopening any broader CA claim.
2. Open Direction 2 as the first real CA rebuild, but only on the retained low-splash library from Direction 1.
3. Open Direction 3 only after the family-leakage artifact exists.

## Reserve, Not Lead

- `Clause-stress diffusion automaton` is still worth keeping as a reserve hybrid for isolated defect clusters, but it is more derivative than the three directions above because it can collapse quickly into ordinary `SAT+CAS` scheduling or warning-propagation language.

## Explicit Pivot Rules

- Pivot immediately if a branch requires full-spectrum rescoring, whole-graph neighborhoods, or increasingly global packet libraries.
- Pivot immediately if a branch only works after re-entering a classical structured family.
- Pivot immediately if progress is only approximate and exact orthogonality remains out of reach.
- Keep `H1` only as the negative control and keep `H3` out of the immediate queue unless the repair-style representation pivots all fail for principled reasons.
