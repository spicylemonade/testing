# Hypothesis Negative Space

## Repo Notes

- `results/literature/gap_frontier.md` had no populated frontier content.
- `results/swarm/director_brief.md` was not present in this repo snapshot.
- No obvious ConceptEvolve artifact names were present under `results/` or in a repo-wide filename search.
- I treat the request for "cellar automata" as "cellular automata"; I found no distinct method family under the "cellar automata" name.

## Negative-Space Thesis

The crowded search space around Hadamard order 668 is not "all possible search." It is mostly:

- classical structured constructions and their descendants (`Williamson`, `Goethals-Seidel`, `Turyn`, cocyclic / `D4t`, block-circulant, Kronecker/product lifts),
- exact search inside those families (`SAT` + `CAS`, compression, partitioning, autocorrelation pruning),
- energy-based heuristics on the raw matrix (`simulated annealing`, `simulated quantum annealing`, `QAOA`, geometric/local search, genetic/metaheuristic variants),
- modular / near-Hadamard approximations treated as endpoints rather than as sparse defect scaffolds.

Cellular automata are not completely absent from Hadamard-adjacent literature, but the visible overlap is construction-oriented (for example bent-function or mutually-unbiased-basis pipelines) rather than a direct search heuristic for an open real order such as `668`.

The under-explored space is not "another optimizer on the same ansatz." It is a local-rule dynamical system that acts on a representation smaller than the full `668 x 668` sign matrix, and that uses the current best approximate structure as a starting point instead of starting from random noise.

## Direction 1: Defect-Gas Cellular Automata on the 64-Modular Seed

### Why this is negative-space

The 2025 `64`-modular order-`668` construction already gets extremely close to exact orthogonality: the Gram matrix has only `26` nonzero off-diagonal entries. Prior work appears to stop at the approximation and the pattern-guessing argument, rather than treating those remaining defects as a sparse dynamical system to be repaired.

### Hypothesis

Represent `D = H H^T - 668 I` as a defect field and run an asynchronous cellular automaton on the defect support, not on the full sign matrix. Each local CA update selects a small, balance-preserving flip packet in a compressed representation of the candidate matrix and tries to move, merge, or annihilate nearby defect charges. If the defect support is truly sparse and structured, a defect-transport CA may reach an exact Hadamard matrix faster than global entrywise search.

### First Experiment

- Start from the known `64`-modular order-`668` matrix or its generating quadruple.
- Compress updates into orbit packets or short row/column blocks instead of individual entries.
- Use local rules that preserve normalization and row balance while reducing nearby Gram defects.
- Measure whether defect count and defect magnitude collapse faster than a matched random local search baseline on the same seed.

### Fast Falsifier

If the defect support diffuses or plateaus after a modest number of asynchronous sweeps, the "sparse defect logistics" assumption was wrong and this branch should be downgraded quickly.

### Why this might work now

Most search methods spend compute rediscovering global structure from scratch. This one assumes the hard part is already present and treats the remaining gap as sparse defect logistics.

### Angle To Avoid

Do not turn this into plain `Ising` hill-climbing, `SA`, `SQA`, or `QAOA` on raw matrix entries. The novelty is the CA evolving the defect graph around a near-solution, not another generic energy minimizer.

## Direction 2: Lag-Space Cellular Automata on Four Relaxed 167-Channels

### Why this is negative-space

The literature around order `4n` search heavily uses supplementary sequences, periodic autocorrelation, and compression, but usually inside rigid symmetry classes. For `668 = 4 x 167`, prime `167` is the awkward part: it makes product constructions weak and strongly structured sequence families easy to overfit.

### Hypothesis

Search in lag space rather than matrix space. Represent a candidate by four length-`167` channels with only weak shared constraints, then define a `1D` cellular automaton over lag residues `k in Z_167`. Each CA cell stores the current local contribution to periodic autocorrelation and updates using neighboring lag defects, conserved parity, and short-range balance rules. The goal is to drive the entire lag-defect spectrum to zero without forcing full circulancy or a standard Williamson/Turyn template.

### First Experiment

- Initialize from random balanced four-channel states and from the `64`-modular seed.
- Let CA states encode local lag residuals plus a small repair action alphabet.
- Permit quasi-circulant or orbit-mixed updates, but forbid the search from collapsing back into a fully classical sequence family.
- Track whether defect entropy falls in lag space before exact reconstruction in matrix space.

### Fast Falsifier

If the only successful trajectories are the ones that recover a standard circulant or Williamson-style template, then this direction is not new enough to justify continued work.

### Why this might work now

The local object in Hadamard search is often the autocorrelation defect, but most solvers only use it as a pruning certificate. A lag-space CA would use it as the state variable itself.

### Angle To Avoid

Do not rebrand a standard `Williamson`, `Turyn`, or fully circulant supplementary-sequence search as "cellular automata." If the representation restores the old family, the hypothesis has collapsed back into explored territory.

## Direction 3: Generative Spacetime Cellular Automata for Row Emission

### Why this is negative-space

Most exact and heuristic methods search over a static matrix. A much less explored question is whether the `668` rows can be generated as a short-rule spacetime orbit, so the search variable is a CA rule table plus seed rather than `446,224` free signs.

### Hypothesis

Use a reversible or asynchronous `1D` cellular automaton on a ring of size `167` with four interleaved channels. Let time steps emit row blocks; after `668` steps, the emitted spacetime slices define the candidate Hadamard matrix. Orthogonality is then a temporal correlation cancellation property of the orbit. The search problem becomes: find a local rule whose orbit has the correct global pairwise correlation structure.

### First Experiment

- Restrict to radius-`1` or radius-`2` rules with explicit balance-preserving constraints.
- Search rule tables and seeds, not matrix entries.
- Score candidates first by low-rank defect spectrum and near-`64`-modular behavior, then by exact orthogonality.
- Prefer rules with nontrivial mixing and long transients over short periodic or Sylvester-like orbits.

### Fast Falsifier

If the rule search only finds short periodic or power-of-two-like behavior and never approaches the observed `64`-modular defect profile, then the generative CA compression is probably too rigid for order `668`.

### Why this might work now

This attacks the scale bottleneck directly. If the matrix is generated by a compact local law, the true search space may be much smaller than the explicit matrix representation suggests.

### Angle To Avoid

Do not brute-force elementary/Wolfram-style rules and do not follow the existing linear-CA-to-bent-function route. That line is structurally tied to special power-of-two Hadamard constructions and is not a plausible direct path to order `668`.

## Preferred Ordering

1. Direction 1 first: highest leverage because it starts from the strongest known near-solution instead of inventing structure from scratch.
2. Direction 2 second: strongest hedge if Direction 1 cannot localize defect transport cleanly.
3. Direction 3 third: most radical and compressive, but also the highest risk.

## Explicit Pivot Guard

If any direction drifts into one of these families, log the overlap and stop polishing it:

- another optimizer over a fixed structured family,
- another full-matrix energy minimizer,
- another modular approximation paper without an exact repair mechanism,
- another power-of-two CA / bent-function construction that cannot even represent order `668`.
