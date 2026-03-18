# Prior Work Comparison

## Scope

This comparison uses the observed behavior of:

- `control_n5_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:H1_defect_syndrome_ca_64m`
- `order_668_64m:H1_defect_syndrome_ca_64m`
- `order_668_64m:greedy`
- `order_668_64m:simulated_annealing`
- `order_668_64m:tabu`

against named papers from `sources.bib`:

- `eliahou2025_64mod668` :: *A 64-Modular Hadamard Matrix of Order 668*
- `tsompanas2017` :: *Cellular Automata Applications in Shortest Path Problem*
- `suksmono2018` :: *Finding a Hadamard Matrix by Simulated Quantum Annealing*
- `suksmono2019` :: *Finding Hadamard Matrices by a Quantum Annealing Machine*
- `bright2019` :: *The SAT+CAS method for combinatorial search with applications to best matrices*
- `artacho2013` :: *Douglas-Rachford feasibility methods for matrix completion problems*

## Comparison Matrix

| Work | State representation | Locality | Seed dependence | Certification / exactness | Compute budget framing | Comparison to this run |
| --- | --- | --- | --- | --- | --- | --- |
| This run: `H1_defect_syndrome_ca_64m` on `order_668_64m:H1_defect_syndrome_ca_64m` | Compact q/s sequences plus sparse lag-syndrome / packet-lattice state | Intended local CA coupling, but still driven by full packetwise defect deltas | Fully seed-dependent on the recovered order-668 frontier object | Exact-hit gate is explicit, but no exact order-668 hit was found | One small matched pilot: budget `80`, requested restarts `3`, seed `17` | Control-valid but frontier-negative: H1 never beats the seed objective and diffuses support on all frontier restarts |
| `eliahou2025_64mod668` | Published compact q/s seed and modular defect profile for order `668` | Not a local search method; constructive mathematical object | Entire contribution is the frontier seed itself | Near-solution only; not an exact Hadamard matrix | No heuristic search budget; theorem/construction framing | Our run inherits the seed directly from this paper and fails to improve it exactly |
| `tsompanas2017` | CA state over a shortest-path / routing problem | Genuinely local propagation in its own problem domain | Not seed-matched to a fixed near-solution in the Hadamard sense | Optimization/routing outcome, not exact Hadamard certification | Heuristic CA optimization budget | Closest CA-shape comparator; our H1 currently looks closer to CA-flavored local repair than to a new exact-search method |
| `suksmono2018` | Hadamard search cast as annealing / energy minimization over candidate matrices | Global energy-driven updates rather than local defect transport | Not tied to the 2025 order-668 seed | Search for exact Hadamard structure through annealing objective | Annealing schedule / heuristic runtime | `order_668_64m:simulated_annealing` is the nearest in-repo analog; both are heuristic, but H1 does not show a frontier advantage over the matched annealing-style baseline |
| `suksmono2019` | Hadamard search on a quantum-annealing formulation | Global objective encoding, not local CA neighborhoods | Not seed-matched to the recovered 64-modular object | Optimization formulation aimed at exact Hadamard search | Hardware / annealing budget rather than matched restart accounting | Our benchmark is much narrower: one seed-matched falsification scaffold, not a claim of hardware-level competitiveness |
| `bright2019` | Structured-family symbolic / SAT+CAS representation for exact combinatorial search | Not local; family-restricted and proof-oriented | Seed independence is stronger because the method searches a constrained family directly | Certificate-rich exact search | Solver time and proof-oriented combinatorial search budget | Our H1 branch is far weaker on certification; this run is a heuristic gate, not a proof-producing exact-search method |
| `artacho2013` | Matrix-completion feasibility formulation | Global feasibility / projection updates rather than local CA dynamics | Problem instance dependent, but not tied to one published near-solution | Feasibility-style convergence target, not CA repair | Iterative feasibility budget | Useful non-CA comparison point: our H1 is more local and more seed-specific, but much weaker on convergence guarantees |

## Cross-Work Conclusions

- On state representation, this run is narrowest when compared to `eliahou2025_64mod668`: it is explicitly a seeded repair program on top of that frontier object rather than an independent construction or a seed-independent exact search.
- On locality, the current H1 branch does not yet separate itself cleanly from generic local-heuristic literature such as `tsompanas2017`. The frontier failure keeps the CA claim conditional.
- On seed dependence, this run is much more dependent on one published near-solution than `bright2019`, `suksmono2018`, or `suksmono2019`.
- On certification, this run is much weaker than `bright2019` and weaker than exact-search claims in the annealing literature because it produces no exact order-668 witness and no proof artifact.
- On exactness, the control runs show `H1` is executable, but the decisive frontier experiment `order_668_64m:H1_defect_syndrome_ca_64m` remains non-exact and does not outperform the matched non-CA baselines on the required gate.
- On compute budget, the present comparison is intentionally small and fair inside one representation. That is enough to reject continued H1 sweeps, but not enough to claim competitiveness with the broader Hadamard-search literature.

## Decision

Relative to the literature, the current contribution is best described as:

- a seeded CA falsification attempt on the frontier object from `eliahou2025_64mod668`
- benchmarked tightly enough to reject broad H1 continuation
- still far short of the certification and generality standards represented by `bright2019`

The literature comparison therefore supports the verification-pack decision: `pivot to H2`, do not continue broad H1 sweeps.
