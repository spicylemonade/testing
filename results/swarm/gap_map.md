# Gap Map: Hadamard 668 via Cellular Automata

Interpreting the prompt's "cellar automata" as `cellular automata`. The current repo watchlist is mostly keyword noise, so the gaps below are ranked against the actual order-668 / Hadamard search landscape rather than the raw local nearest-neighbor list.

## Ranked gaps

### 1. Defect-repair CA seeded from the new 64-modular order-668 objects
- Why this looks under-served: recent order-668 progress already supplies `64`-modular matrices whose normalized Gram matrix leaves only a sparse pattern of residual `64`-valued defects, but the literature trail stops at relaxed or approximate objects instead of dynamic repair.
- Concrete setting: define CA state on entry signs, row blocks, or correlation defects and update against the Gram-matrix conflict graph rather than from a random matrix.
- Failure mode to respect: a naive bit-flip CA on the raw `668 x 668` grid will still inherit a glassy landscape, because each local sign change perturbs many row inner products at once.
- Why it is worth ranking first: it uses the freshest order-668 artifact as a launch point instead of competing head-on with mature exact-search families.

### 2. Nonlocal or factor-graph CA that matches dense orthogonality constraints
- Why this looks under-served: mainstream CA work in combinatorial design still clusters around local rules for Latin squares, orthogonal arrays, and related objects; Hadamard search is dominated by all-to-all orthogonality constraints.
- Concrete setting: cells should represent rows, blocks, or correlation residues on a dense interaction graph, with asynchronous or message-passing style updates.
- Failure mode to respect: nearest-neighbor lattice CA is likely a category error here, because Hadamard feasibility is global and dense, not geometric and local.
- Why it matters: if CA is to be novel here, the novelty is the representation of locality, not merely parallel update speed.

### 3. Symmetry-aware CA over compressed algebraic families for order `4p` with `p = 167`
- Why this looks under-served: order `668 = 4 x 167` sits in a prime case where broad raw-matrix search wastes effort across huge symmetry orbits and families already known to collapse to structured forms.
- Concrete setting: encode cells as sequence variables, orbit representatives, or block families compatible with cocyclic / Williamson-type constraints instead of individual matrix entries.
- Failure mode to respect: an unconstrained CA can spend almost all of its budget rediscovering equivalent or already-ruled-out states, which is novelty-negative even if the dynamics look new.
- Why it matters: the gap is not "apply CA somewhere"; it is "apply CA on the right quotient space for the only structured families that matter at 668."

### 4. Completion-style CA that grows partial orthogonal structure instead of solving the full matrix at once
- Why this looks under-served: matrix-completion and deleted-vector formulations exist, but they remain small-scale and are not framed as progressive CA dynamics for building large orthogonal row sets.
- Concrete setting: start from a partial submatrix, modular seed, or structured row family and let CA updates add and repair rows while preserving a tractable subset of constraints.
- Failure mode to respect: without exact feasibility checks, late-stage completion can become exponentially brittle and yield attractive near-misses that do not publish.
- Why it matters: this creates intermediate benchmarks below full order `668`, which is critical for falsifying bad CA representations early.

### 5. Certificate-coupled CA hybrids: CA as proposer, exact methods as filter
- Why this looks under-served: the popular tracks are exact SAT/CAS/PSD search on structured families or global annealing / quantum formulations, not a hybrid loop where local dynamics propose candidates and exact filters kill infeasible branches.
- Concrete setting: use CA to generate local moves or family transitions, then invoke PSD, autocorrelation, SAT, or supplementary-difference-set checks after each phase.
- Failure mode to respect: pure CA without certificates risks producing only "interesting almost-Hadamards," which does not move the order-668 existence question much.
- Why it matters: even a negative result is valuable if the hybrid produces family-specific impossibility evidence rather than another unconstrained heuristic trace.

## What appears over-served or low-value

- Plain `2D` nearest-neighbor CA on the sign matrix is the weakest option; it mismatches the dense constraint graph.
- Random-start CA with no algebraic seed is likely dominated by rugged-energy heuristics that already struggle to scale.
- Rebranding existing annealing, SAT, or sequence-family search as "CA" without changing the state space or certification loop is not a genuine gap.

## Evidence anchors used for ranking

- `64`-modular Hadamard work now reaches order `668` and frames exact order `668` as still elusive; this makes defect-repair from relaxed objects more credible than blind search.
- Recent CA-and-design surveying emphasizes Latin squares, mutually orthogonal Latin squares, and orthogonal-array style constructions rather than direct real Hadamard synthesis.
- Order-`4p` cocyclic theory for primes with `p ≡ 3 (mod 4)` sharply narrows which structured families are even worth exploring at `p = 167`.
- Matrix-completion / Douglas-Rachford and quantum-search papers show that generic global feasibility methods exist, but they remain small-scale or heavily resource-constrained.
- SAT/CAS work on Williamson-style matrices shows the exact-search frontier is strongest when the search stays certificate-rich and family-aware.
- Heuristic search inside cocyclic families already exists, so the open space is not "another heuristic on the same family" but a better state representation, seed, or certification loop.
