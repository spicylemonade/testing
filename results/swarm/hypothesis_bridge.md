# Cross-Domain Bridge Hypotheses For Hadamard 668

Overlap and pivot note:
The current repo watchlist is dominated by generic automata papers with only lexical overlap to the Hadamard-668 problem. That makes "plain cellular automata from scratch" look derivative and low-signal. I therefore interpret "cellar automata" as a stack or pushdown automata idea for sequence search, and I keep cellular automata only where they act on a strong Hadamard-specific seed.

## 1. Visibly Pushdown Automata Over Run-Length Correlation Debt

- Title: Visibly Pushdown Automata Over Run-Length Correlation Debt
- Closest prior art: sequence-based Hadamard searches using Williamson or Goethals-Seidel type blocks, plus the recent 64-modular order-668 construction that already exposes a structured 4-by-167 block view.
- Why it is different: instead of searching raw bit strings or flat SAT clauses, encode each partial length-167 block as a word over run-length tokens. The stack stores unresolved multiscale autocorrelation debt, parity debt, and block-symmetry obligations. This is the strongest interpretation of "cellar automata": a search language in which only prefixes with a legal completion remain in the frontier.
- Falsifiable prediction: if this bridge is real, the automaton should accept all known smaller block constructions and the published 64-modular order-668 seed while rejecting at least 99% of random prefixes that survive only local tests. If it cannot even reconstruct those known cases, the hypothesis fails quickly.
- Required experiments: derive a run-length tokenization for 4 length-167 blocks; infer or hand-design visibly pushdown transitions from smaller known Hadamard families; benchmark pruning rate against flat backtracking or SAT on smaller orders; then run the automaton as a proposal filter for exact or modular searches at order 668.

## 2. Defect-Transport Cellular Automata Lift From the 64-Modular Seed

- Title: Defect-Transport Cellular Automata Lift From the 64-Modular Seed
- Closest prior art: the 64-modular Hadamard matrix of order 668, plus physics-style Hadamard searches based on simulated annealing or quantum approximate optimization, and generic cellular-automata optimization work.
- Why it is different: this is not a CA that searches the full matrix space from scratch. Start from the known 64-modular matrix, compute its off-diagonal Gram defects, and evolve those defects as particles on a local interaction graph. CA rules move, merge, or annihilate correlation defects while preserving row balance and any chosen block symmetries. The method turns a global combinatorial search into a local defect-transport problem.
- Falsifiable prediction: from the same 64-modular starting point and the same move budget, defect-transport CA should reduce total off-diagonal correlation energy faster than annealing or naive hill-climbing. If an exact Hadamard lies near that seed, the CA should reach zero defects more often; if not, it should stall on reproducible invariant walls that expose why the seed cannot be lifted.
- Required experiments: reconstruct the published 64-modular matrix; define a defect graph and conserved quantities; implement local CA update rules and matched annealing baselines; validate on perturbed smaller Hadamard matrices where the ground truth is known; then compare lift performance at order 668.

## 3. Quaternionic Shadow Decoding Into Real Order-668 Candidates

- Title: Quaternionic Shadow Decoding Into Real Order-668 Candidates
- Closest prior art: recent work on quaternionic perfect sequences and Hadamard matrices, together with code-oriented Hadamard constructions such as full propelinear-code lifts.
- Why it is different: prior work stays inside quaternionic families or starts from already-known real Hadamards. This bridge uses quaternionic perfect sequences only as a richer latent proposal space. Their phase patterns are projected into binary "shadows," and those shadows are decoded toward real modular or exact orthogonality. The imported assumption is that noncommutative phase structure is a better proposal distribution for the real 4-by-167 search than direct binary random restarts.
- Falsifiable prediction: at small orders where exhaustive comparison is feasible, binary shadows of quaternionic perfect sequences should satisfy real modular filters or low-defect real constraints far more often than random binary seeds. If that enrichment is absent, the bridge is wrong and should be dropped.
- Required experiments: exhaustively enumerate small quaternionic perfect-sequence instances; define several shadow maps into binary block tuples; measure enrichment for exact and 32 or 64-modular real constraints; if enrichment appears, sample quaternionic proposals at length 167 and connect them to the published modular seed with local repair or decoding.
