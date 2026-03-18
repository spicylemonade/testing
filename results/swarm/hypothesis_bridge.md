# Cross-Domain Bridge Hypotheses for Hadamard 668

Assumption: in this repo, the prompt term `cellar automata` is treated as `cellular automata`.

Pivot note before proposing anything new:

- Do not recycle `H1_defect_syndrome_ca_64m` as a live bridge. The first frontier kill test and the exact one-packet scan already show that the current single-packet q/s lattice is frozen or fake-local on the canonical seed.
- Do not spend the main budget on direct row-emission CA. That path remains too exposed to existing CA-construction overlap.
- Do not count `H2_lag_space_ca_167` itself as a fresh bridge here. It is the existing backup branch, not a new cross-domain pivot.

## 1. Hybrid-Cellular-Automata Stress Redistribution on a Composite Packet Graph

**Title:** Import topology-optimization HCA laws to allocate repair pressure over a low-splash composite packet library

**Closest prior art:** Hybrid cellular automata for topology optimization; the repo's promoted `anti-splash composite packet library` idea; the held `adaptive_criticality_ca_schedule` branch.

**Why it is different:** The topology-optimization HCA literature uses local stress or compliance redistribution to decide where material should grow or shrink under a hard volume budget. The bridge here is to reinterpret the retained composite packet library as the design space and the exact Gram-defect load as the local stress field. That is narrower and more testable than another generic temperature schedule: the CA update law would live on a seed-matched composite packet graph, enforce a hard cap on simultaneously active packet mass, and try to keep defect reduction spatially bounded. This directly targets the current failure mode, namely that single-packet q/s moves have large changed-lag footprints and no improving one-packet moves on the canonical seed.

**Falsifiable prediction:** On the same retained composite packet library and the same order-668 frontier seed, an HCA-style local stress redistribution law should beat fixed-rule CA, greedy, tabu, and simulated annealing on lexicographic seed improvement or exact-hit rate while also reducing median changed-lag footprint. Reject the hypothesis if the advantage disappears once the packet basis is shared across baselines, or if the method still requires dense all-packet rescoring every step.

**Required experiments:** Enumerate symmetry-safe 2-packet and 4-packet composites; compute exact delta fingerprints and keep only low-splash candidates; build the composite-packet influence graph; define a local stress or compliance density from exact defect mass; implement an HCA update law with a hard local activity budget; benchmark against fixed-schedule CA and matched non-CA baselines on the small exact controls first and then on the canonical order-668 seed.

## 2. Decoder-Relay CA with SAT+CAS Handoffs

**Title:** Use a decoder-style defect graph to route exact SAT+CAS effort only into locally stressed regions

**Closest prior art:** `Cellular-automaton decoders for topological quantum memories`; `The SAT+CAS Method for Combinatorial Search with Applications to Best Matrices`; the repo's `ldpc_hadamard_decoder_graph` and `sat_clause_diffusion_automaton` concepts.

**Why it is different:** Decoder work repairs code syndromes, while SAT+CAS work proves exact results inside structured combinatorial families. This bridge uses CA for neither direct construction nor generic scoring. Instead, it builds a sparse defect-packet or clause-packet graph from exact delta tables around a structured Hadamard repair subproblem, lets a CA transport conflict mass on that graph, and hands only the most stressed neighborhood to exact SAT+CAS repair. The novelty survives only if the CA relay improves exact progress per unit of exact reasoning rather than acting as a thin wrapper around ordinary branching heuristics.

**Falsifiable prediction:** On Williamson or best-matrix controls and then on compressed subinstances derived from the order-668 seed, the relay should deliver more exact hits per SAT+CAS call, or smaller proof-search trees at the same exact-hit rate, than plain SAT+CAS branching, decoder-only weighted bit-flip, and clause-score greedy handoff. Reject the hypothesis if graph construction cost erases the gain, if the useful neighborhoods become dense, or if the CA layer adds nothing beyond standard branching scores.

**Required experiments:** Choose one compressed Hadamard family with a clean exact baseline; compile the SAT+CAS subproblem and exact packet deltas; derive a sparse clause-packet graph; implement CA stress transport and a handoff rule for invoking exact repair on one neighborhood at a time; compare solver calls, wall-clock time, exact-hit rate, neighborhood density, and family-leakage behavior against SAT+CAS and decoder-only controls.

## 3. Prime-Field CA Seed Prior for the 167-Core with Leakage Audit

**Title:** Use finite-field CA over `F_167` only as a structured seed generator, not as a direct constructor

**Closest prior art:** `Bent Functions from Cellular Automata`; `Cellular Automata-Based Methods for the Construction of Mutually Unbiased Bases`; `Constructing Orthogonal Latin Squares from Linear Cellular Automata`; the repo's `lbca_prime_seed_projection` concept.

**Why it is different:** Direct CA-construction claims are already too close to the overlap zone around H3. The pivot is narrower: exploit prime-field CA only to sample algebraically biased traces on the prime core behind `668 = 4 x 167`, then project those traces into q/s or four-channel seeds for a separate repair stage. CA is a seed prior over structured starts, not the solver and not the proof method. That makes the bridge distant from current Hadamard-search heuristics while still easy to falsify statistically.

**Falsifiable prediction:** After binary or quaternary projection, the best prime-field CA seed families should produce a heavier tail of low-support, low-`l1`, or post-repair-improving starts than random balanced seeds, m-sequences, and simple perturbations of the published `64`-modular seed. Reject the hypothesis if the residual distribution is statistically indistinguishable from those baselines or if the best seeds canonically collapse into an already known family such as Williamson, Turyn, Goethals-Seidel, or cocyclic search.

**Required experiments:** Enumerate or optimize linear and bipermutive rules over `F_167`; design several projection maps into q/s or four-channel sequence tuples; compare initial support, `l1`, and `max_abs` distributions under a shared downstream repair method; run the same family-leakage audit used for H2; keep the branch only if the seed prior improves the tail before any special-case postprocessing.
