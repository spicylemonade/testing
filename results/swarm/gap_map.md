# Gap Map: Negative Space Around Hadamard 668 via Cellular Automata

Interpretation note: the prompt says "cellar automata". This reads like a typo for `cellular automata`, and the map below assumes that interpretation.

## Working Baseline

- Order `668 = 4 x 167`, with `167` prime. That immediately pushes any structured search toward `n = 167` subproblems.
- Order `668` is still unresolved in current public references, and the latest concrete progress I found is a `64`-modular Hadamard matrix of order `668`, built from a length-`167` modular Golay quadruple inside a Goethals-Seidel array.
- That 2025 construction is close but not exact: each row is orthogonal to `641` others, leaving only `26` nonzero off-diagonal Gram entries per row. This is the best concrete stepping-stone I found for a CA-style repair idea.
- The local literature artifacts in this repo are low-signal: they do not contain a credible Hadamard-specific frontier.
- Targeted checking suggests the useful contrast is:
  - Hadamard search already has classical structured families and generic heuristics.
  - Cellular automata has adjacent combinatorial-design work, but not a direct order-668 Hadamard search program.

## What Looks Already Popular or Already Covered

- Structured Hadamard search itself is not empty territory. Relevant examples include Goethals-Seidel / Golay / Turyn constructions, SAT+CAS searches for Williamson families, and quantum/annealing formulations of Williamson-, Baumert-Hall-, and Turyn-based search.
- Cellular automata is also not blank territory in combinatorial design, but the nearby literature is about:
  - orthogonal Latin squares / orthogonal arrays,
  - bent functions and very structured Hadamard-type objects,
  - CA controllability and local-decoder style dynamics.
- I did not find evidence of a direct cellular-automata search for a real Hadamard matrix of order `668`, or even a mature CA program for hard open Hadamard orders.

## Five Concrete Gaps

### 1. No CA-native encoding of the `668` orthogonality constraints

- Gap: I did not find an established cellular-automata state/update scheme that makes the `668 x 668` real Hadamard constraints local in a meaningful way, or even a CA encoding of the `166` aperiodic autocorrelation constraints that appear in the known length-`167` Golay-quadruple route.
- Why this matters: a naive CA over raw `+/-1` entries treats a global pairwise-orthogonality problem as if it were a local pattern-formation problem. That is exactly where CA methods usually fail.
- Why it looks under-served: the nearby CA papers focus on Latin-square and orthogonal-array generation, while the best current `668` approximation is sequence-driven and phrased in terms of modular Golay conditions at length `167`.
- Failure mode: the CA settles into symmetric or periodic attractors with low local defect but terrible global row-correlation profile.
- Best next step: do not start with the full `668 x 668` matrix. Start with a defect representation or with structured `n = 167` block data instead.
- Priority: medium. It is foundational, but a raw-matrix CA search is probably under-served for good reason.

### 2. Pure circulant/Williamson-style CA search at `n = 167` is a novelty trap

- Gap: a CA restricted to four circulant components or close Williamson-type ansatzes is likely not a new search space at all.
- Why this matters: `167` is prime, and recent work on Williamson-type Hadamard matrices with circulant components shows that for odd-prime orders this space collapses back onto classical Williamson structure up to cyclic shift.
- Negative-space interpretation: if the CA only explores that ansatz, it is mostly re-implementing an old structured search family with a new update rule.
- Failure mode: large compute spend with zero coverage expansion beyond what classical algebraic search already examined.
- Best next step: if CA is used, it should either:
  - leave the pure circulant-component family, or
  - explicitly prove that the CA state space is strictly richer than a Williamson/Goethals-Seidel reformulation.
- Priority: very high. This is the cleanest fake-novelty risk in the whole project.

### 3. Missing bridge from CA-generated design objects to `n = 167` Hadamard data

- Gap: CA design papers generate orthogonal Latin squares, orthogonal arrays, bent-function-related Hadamard structure, and MUB ingredients, but I did not find a clear pipeline from those outputs to the specific `n = 167` ingredients that order `668` search usually needs.
- Why this matters: "CA can generate combinatorial designs" is not enough. The missing question is whether CA outputs can be converted into modular Golay quadruples, Goethals-Seidel blocks, supplementary difference sets, Turyn-type sequences, or another exact order-`668` witness format.
- Why it looks under-served: this sits between two communities that do not appear to talk to each other much:
  - CA-based combinatorial design generation,
  - exact/structured Hadamard construction at hard open orders.
- Failure mode: producing elegant CA-generated designs that never certify a real Hadamard matrix of order `668`.
- Best next step: define an explicit translation target at `n = 167` first, then ask whether any CA family can hit it.
- Priority: very high. This is the main under-served interface that could create actual novelty.

### 4. CA as a local defect-repair layer on top of an exact verifier appears untried

- Gap: the under-served opportunity is not "replace all search with CA", but "use CA as a distributed repair or decoder layer" inside a hybrid search loop.
- Why this matters: Hadamard search already uses stronger exact or hybrid machinery than plain heuristics. Separately, CA has shown value in adjacent settings where local rules repair constraint violations or drive a system toward a satisfiable region.
- Negative-space opportunity: let the CA operate on a defect field:
  - row-pair inner-product defects,
  - block incompatibilities,
  - the sparse `26`-entry residual defect pattern left by the current `64`-modular order-`668` matrix.
- Then let an exact checker or CAS/SAT layer validate or restart.
- Failure mode: oscillating defect patterns, frozen domains, or repeated movement inside one equivalence orbit.
- Best next step: prototype a CA on the Gram-defect graph, not on matrix entries directly.
- Priority: high. This is the most plausible genuinely new CA role without pretending CA alone solves the whole problem.

### 5. No serious reachability/coverage discipline for the chosen CA family

- Gap: I did not find a serious framework for proving what a chosen CA ansatz can and cannot represent, or even whether its reachable set remains nontrivial as the system size grows.
- Why this matters: nearby CA-Hadamard-adjacent work is often highly structured. For example, CA constructions tied to bent functions or linear bipermutive rules cover special subclasses, not the full open-order search space.
- Negative-space interpretation: before running large searches, the project needs a falsification layer that asks:
  - what invariants does this CA preserve,
  - which equivalence classes are even reachable,
  - whether the reachable set intersects any known constructive families.
- Why it looks under-served: recent CA controllability work shows that only special rule families are fully controllable, while reachability ratios for other rules vanish as system size grows. That warning has not been internalized in Hadamard-style CA proposals.
- Failure mode: the CA explores a tiny orbit family that cannot possibly contain an order-`668` witness, but the limitation is discovered only after substantial compute.
- Best next step: require every CA proposal to ship with:
  - a reachability argument,
  - a smaller-order benchmark ladder,
  - an equivalence-aware novelty check.
- Priority: high. This is the guardrail that keeps the project from mistaking a representation constraint for a hard open problem.

## Prioritized View

1. `Gap 2` is the first filter. If the CA ansatz is only a circulant/Williamson reformulation at prime `167`, stop.
2. `Gap 3` is the main under-served research interface. The project needs a real bridge from CA outputs to exact order-`668` construction data.
3. `Gap 4` is the most plausible constructive angle: CA as a repair/decoder layer inside a hybrid exact loop.
4. `Gap 5` is mandatory discipline. Without it, the search can look active while covering almost nothing.
5. `Gap 1` remains real, but mostly as a warning: a raw full-matrix CA search is low-priority unless someone first proves a useful locality principle.

## Practical Recommendation

- Do not sell "cellular automata for Hadamard 668" as a full standalone solver yet.
- The defensible version is narrower:
  - use CA to navigate or repair structured `n = 167` defect states,
  - keep exact certification outside the CA,
  - explicitly prove that the CA reaches a search space not already exhausted by classical structured methods.

## Source Anchors Used For This Map

- OEIS `A007299`, which still lists `668` among the unresolved Hadamard orders and records it as the smallest unresolved case below `1000`.
- Eliahou, `A 64-modular Hadamard matrix of order 668`, Australasian Journal of Combinatorics 93(2), 2025.
- Bright, Kotsireas, and Ganesh, `A SAT+CAS Method for Enumerating Williamson Matrices of Even Order`, AAAI 2018.
- Fitzpatrick and O'Keeffe, `Williamson type Hadamard matrices with circulant components`, Discrete Mathematics 346(12), 2023.
- Bambang et al., `Quantum computing formulation of some classical Hadamard matrix searching methods and its implementation on a quantum computer`, Scientific Reports 11, 2021.
- Solihah et al., `A quantum approximate optimization method for finding Hadamard matrices`, Scientific Reports 15, 2025.
- Mariot, Formenti, and Leporati, `Constructing Orthogonal Latin Squares from Linear Cellular Automata`, 2016.
- Gadouleau, Mariot, and Picek, `Bent Functions from Cellular Automata`, IACR ePrint 2020/1272.
- Manzoni, Mariot, and Menara, `Combinatorial Designs and Cellular Automata: A Survey`, 2025.
- Bagnoli, Dridi, and Fates, `Regional controllability of cellular automata as a SAT problem`, Natural Computing 25(1), 2026.
- Herold et al., `Cellular-automaton decoders for topological quantum memories`, npj Quantum Information 1, 2015.
