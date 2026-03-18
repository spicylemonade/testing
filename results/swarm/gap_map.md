# Gap Map: Hadamard 668 via Cellular Automata

Interpret the prompt's `cellar automata` as `cellular automata`.

The repo has already eliminated the first obvious CA branch. `H1_defect_syndrome_ca_64m` never beat the canonical `64`-modular seed objective `13/2880/512`, reached no exact hit, and oscillated between support diffusion and paralysis under matched same-coordinate baselines. The negative space below is therefore the space that still looks under-served after that failure, not a list of generic CA ideas.

## Ranked gaps

### 1. Anti-splash composite packet library on the canonical seed
- Why this is under-served: the current work tunes rules on a single-packet `q/s` basis, but the actuator library itself appears wrong.
- Repo evidence: exhaustive one-packet and two-packet scans found zero improving moves on the canonical seed; a typical one-packet move perturbs about `51` of the `166` lag slots; `H1` either diffuses support or stays pinned to the seed.
- Concrete setting: discover symmetry-safe composite packets or short micro-orbits whose far-field lag effects cancel, so one move acts on a genuinely local defect neighborhood instead of splashing across the whole lag field.
- First honest falsifier: kill this line if the new library does not both lower changed-lag footprint sharply relative to single-packet flips and expose any improving or strategically neutral neighborhood on the canonical seed.
- Overlap trap: if the composite packets only help because they smuggle in `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, or block-circulant structure, the result is optimizer-over-known-family rather than a new CA direction.

### 2. Honest locality geometry: defect-packet influence graph, not raw `q/s` adjacency
- Why this is under-served: `H1` looks local in syntax but not in effect. The natural local object appears to be the sparse defect field and its packet-influence graph, not the raw packet ring.
- Repo evidence: `H1_precheck` warns that exact all-packet scoring can collapse into generic local search; the concept-evolution notes point to defect-packet influence graphs and lag fields; `H2` exists precisely because the current packet neighborhoods look fake-local.
- Concrete setting: move from ring-style packet neighborhoods to a bounded-degree defect-packet graph or lag-field graph with explicit local messages, local memory, and bounded touched-edge counts.
- First honest falsifier: kill this line if the supposedly local graph CA still depends on near-global packet rescoring, absolute packet IDs, or whole-state ranking at each step.
- Overlap trap: a graph that is only a thin wrapper around full objective evaluation is not a CA contribution; it is scorer-driven local search wearing graph language.

### 3. Bounded barrier-crossing CA with real local state
- Why this is under-served: the canonical seed has no improving radius-`1` or radius-`2` moves, so monotone sparse CA is dead on arrival. What remains is tightly bounded coordination of neutral or worsening steps.
- Repo evidence: exhaustive scans are frozen; `H1` alternates between diffusion and paralysis; the concept notes explicitly say memory, refractory state, or cluster labels are core mechanism rather than decoration.
- Concrete setting: add age, refractory state, cluster tags, or short local avalanches on the same packet library so the CA can coordinate small barrier-crossing bursts without becoming a global temperature schedule.
- First honest falsifier: kill this line if any gain only appears when burst size, sensing radius, or coordination grows toward whole-state behavior.
- Overlap trap: if the only working version needs global burst scheduling or broad synchronized activation, it has collapsed into annealing or generic local search.

### 4. `H2_lag_space_ca_167` with a hard family-leakage audit
- Why this is under-served: the autocorrelation defect field is the true local object, but it is usually used as a pruning certificate rather than as the CA state itself.
- Repo evidence: `H2` is the designated fallback only when `H1` fails for locality reasons; the negative-space notes keep lag-space CA as the best backup; the novelty audit says `H2` is only distinct if it does not collapse into known structured-family syntax.
- Concrete setting: run one lag-space representation over the prime core `167`, keep one matched non-CA lag-space control, and audit family leakage before spending broad budget.
- First honest falsifier: kill or relabel this line if any promising behavior depends on `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, or block-circulant constraints rather than on a new lag-local dynamic.
- Overlap trap: "lag-space CA" is not a novelty shield; if it is only a relabeled sequence-family search, treat it as such.

### 5. Certificate-coupled frontier recovery, not raw frontier-only heuristics
- Why this is under-served: pure heuristics and exact family search are both well served. The less crowded lane is CA as a proposer on frontier-adjacent states, with exact filters that reject false progress.
- Repo evidence: there is still no exact witness; the current pilot lacks a matched `CA-off` baseline and comes from one canonical seed plus tiny controls; the bridge notes keep certificate-coupled hybrids alive while treating broad `H3` rule-table search as overlap-heavy.
- Concrete setting: build a small perturbation ladder around the canonical `64`-modular seed and run `full CA`, `CA-off`, and matched non-CA controls under the same exactness gate, with exact autocorrelation / Gram / certificate filters after each phase.
- First honest falsifier: kill this line if the CA only repairs lightly perturbed seeds, or if the exact filter does the real work while the CA adds nothing beyond scorer-only search.
- Overlap trap: if certification dominates and the CA becomes a generic proposal generator, the contribution is hybrid heuristic scaffolding rather than a new CA method.

## What Not To Spend Budget On

- more `H1` rule-weight tuning on the current single-packet basis
- random-start full `668 x 668` lattice CA
- broad `H3` rule-table or Wolfram-style sweeps
- rebranding known structured-family search or global energy descent as `CA`

## Routing Implication

- Do not reopen broad `H1` sweeps on the existing basis.
- The next defensible order is `CA-off isolation -> actuator/locality redesign -> H2 only if the failure remains locality-driven after those checks`.
