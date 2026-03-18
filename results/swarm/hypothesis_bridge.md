# Cross-Domain Bridge Hypotheses for Hadamard 668 via Cellular Automata

Assumption: the task term `cellar automata` means `cellular automata`.

Overlap warning before proposing anything new: a direct claim that "cellular automata construct Hadamard objects" is already too close to existing LBCA/OCA work on orthogonal Latin squares, self-orthogonal Latin squares, mutually unbiased bases, and CA-derived bent functions/Hadamard matrices. The novelty pivot below is to use cellular automata as a search dynamic, repair operator, or structured prior for the hard order-668 search, rather than as a generic standalone construction.

## 1. Syndrome-Decoder Cellular Automaton for Compressed Hadamard Search

**Title:** Treat Williamson/Turyn residuals as a syndrome field and decode them with a local cellular automaton

**Closest prior art:** `Cellular-automaton decoders for topological quantum memories` and the Hadamard search formulations in `Quantum computing formulation of some classical Hadamard matrix searching methods and its implementation on a quantum computer` and `A quantum approximate optimization method for finding Hadamard matrices`.

**Why it is different:** The prior Hadamard work converts Williamson, Baumert-Hall, or Turyn constraints into an energy for annealing or QAOA. The prior CA decoder work uses local syndrome propagation to eliminate defects in topological codes. The bridge hypothesis is to reinterpret off-zero autocorrelation terms or compressed orthogonality violations as decoder syndromes on a finite lattice, then use a nearest-neighbor CA to move and annihilate defects instead of minimizing a generic Ising energy. That is a different algorithmic role for CA than both direct CA constructions and quantum optimization.

**Falsifiable prediction:** On compressed Hadamard benchmarks with known solutions, a decoder-style CA should lower residual autocorrelation faster than matched simulated annealing and should produce a strictly higher exact-feasibility rate from the same seed distribution. If defect density and exact-hit rate are not improved over annealing under equal update budgets, reject the hypothesis.

**Required experiments:** Build a factor-graph or lattice representation of Williamson/Turyn constraints; define syndrome cells from each violated autocorrelation term; implement synchronous and asynchronous CA update rules with local field diffusion and defect attraction; benchmark against simulated annealing, tabu search, and plain greedy flips on known orders before attempting order 668; measure residual decay, escape from metastable states, and exact-feasibility rate.

## 2. Goal-Guided Neural Cellular Automaton as a Learned Repair Operator

**Title:** Train a neural cellular automaton to repair near-Hadamard states instead of hand-designing local moves

**Closest prior art:** `Growing Neural Cellular Automata`, `Goal-Guided Neural Cellular Automata: Learning to Control Self-Organising Systems`, and `Differentiable cellular automata`.

**Why it is different:** Existing NCA work learns local rules that grow or maintain target patterns. Existing Hadamard search work uses fixed symbolic energies and generic optimization. The bridge is to train an NCA on smaller known Hadamard constructions and corrupted near-solutions so that each cell sees only local defect channels and learns a repair policy for compressed sequence or block variables. This is not a direct CA construction of a Hadamard matrix, and it is not standard annealing: it is a learned local error-correction policy for a rigid combinatorial object.

**Falsifiable prediction:** An NCA trained only on smaller known orders and noisy perturbations should improve held-out exact-repair rate on larger compressed instances relative to non-learned local search. If the learned rule only memorizes training sizes and fails to transfer to larger held-out instances, reject the hypothesis.

**Required experiments:** Encode compressed Hadamard candidates as a CA lattice with channels for signs, symmetry class, and local defect summaries; generate training data from known constructions plus controlled corruption; train differentiable or straight-through NCA updates to minimize final defect count and maximize exact repair; compare transfer to unseen orders and to order-668 subinstances; ablate neighborhood radius, asynchronous updates, and discrete-vs-continuous state representations.

## 3. Finite-Field LBCA Seeds for Prime-Length Turyn Search

**Title:** Use finite-field linear bipermutive cellular automata as a structured seed generator for the length-167 core of order 668

**Closest prior art:** `Bent Functions from Cellular Automata` and `Cellular Automata-Based Methods for the Construction of Mutually Unbiased Bases`.

**Why it is different:** Those papers show that CA can directly generate power-of-two Hadamard-adjacent objects such as bent functions and complex Hadamard or MUB structures. Reusing that claim for order 668 would be derivative and also mismatched to the prime core `167`. The pivot is to use finite-field LBCA over `F_167` or related prime-length state spaces only as a structured prior for the real four-sequence Williamson/Turyn search behind `668 = 4 * 167`. CA is supplying algebraically biased seeds and block dictionaries, not claiming a direct construction.

**Falsifiable prediction:** LBCA-derived seed families, after binary or quaternary projection into candidate sequence tuples, should produce lower initial autocorrelation residuals and a heavier tail of near-feasible states than random seeds, m-sequences, or SAT warm starts. If their residual distribution is statistically indistinguishable from those baselines, reject the hypothesis.

**Required experiments:** Enumerate or optimize LBCA rules over prime-length alphabets for diffusion, period, and pairwise decorrelation; project their spacetime traces into binary sequence tuples compatible with Williamson/Turyn compression; measure autocorrelation residuals and exact-feasibility rate before and after a common local-repair postprocessor; compare seed-quality distributions on smaller known orders, then run the best families on order-668 instances.
