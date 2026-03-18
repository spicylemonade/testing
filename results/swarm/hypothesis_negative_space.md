# Hypothesis Negative Space: Hadamard 668 via Cellular Automata

Interpret "cellar automata" as **cellular automata**.

## Local constraints from this run

- `results/literature/gap_frontier.md` and `results/literature/gap_frontier.json` contain no ranked frontier items.
- `results/research_context.json` shows `concept_evolve: {}` and `director_brief_present: false`.
- The bootstrap watchlist is mostly polluted by generic "automata" matches rather than actual Hadamard-668 prior art, so novelty has to be enforced manually.

## Over-explored families to avoid by default

- Standard algebraic construction stacks: Paley, Williamson, Goethals-Seidel, Cooper-Wallis, Baumert-Hall, Ehlich, supplementary difference sets, cocyclic variants.
- Structured exhaustive search over those same families: SAT+CAS enumeration, Turyn/Williamson sequence enumeration, direct matching/hashing over SDS candidates.
- Global black-box optimization over matrix entries or structured encodings: simulated annealing, quantum annealing, QAOA, generic GA/EA on the sequence bits alone.

Reason to avoid them here: the literature already keeps revisiting these branches, and recent work still treats order 668 as open while also exposing scaling limits in the structured-search setting. The strongest recent local targets are more specific:
- in the cyclic Goethals-Seidel reduction, the obstruction is whether a particular length-167, weight-80 binary sequence with a prescribed autocorrelation exists;
- in a different direction, a 64-modular Hadamard matrix of order 668 now exists, which suggests that lifting a near-solution may be more promising than restarting from scratch.

## Direction 1: Autocorrelation-realization CA on the 167-cycle

**Hypothesis.** Use a 1D cyclic binary CA on 167 cells as a *compressed generator of candidate supports*, and search rule/seed pairs whose orbit slices realize the missing periodic autocorrelation profile needed to close the current 668 reduction.

Why this attacks negative space:
- Recent work reduces the open 668 case to the realizability of one missing binary autocorrelation profile, not to a completely unconstrained 668 x 668 search.
- Prior work largely searched algebraic templates or structured sequence families directly.
- A CA search in **rule space** may be smaller and more compositional than direct search in the full sequence space.

Why it is not just "do Goethals-Seidel again":
- The CA is not used as a final certificate family; it is used as a generator of orbit slices whose local dynamics may concentrate probability mass on realizable autocorrelation patterns.
- The search target is the missing weight-80 sequence itself, not a polished restatement of SDS matching.

First test:
1. Recover or reconstruct the target length-167 autocorrelation vector implied by the known three blocks.
2. Search elementary and small-radius binary CA with hard constraints on orbit weight, run count, and cyclic symmetry breaking.
3. Score orbit slices only by distance to the target periodic autocorrelation and PSD feasibility.
4. If a slice hits the target exactly, lift it back into the 4-block certificate and verify the corresponding Hadamard construction.

Fast falsifier:
- If CA-generated slices do not outperform random cyclic subsets of weight 80 on autocorrelation distance after a modest GPU sweep, kill this branch.

Angle to avoid:
- Do **not** collapse back into direct SDS/Goethals-Seidel matching or into plain Turyn/Williamson sequence enumeration with CA as cosmetic packaging.

## Direction 2: Modulus-lifting CA from the 64-modular 668 seed

**Hypothesis.** Start from the known 64-modular Hadamard matrix of order 668 and use a CA to perform local sign updates that lift modular orthogonality step by step, ideally past modulus 668 where the matrix would become an actual Hadamard matrix.

Why this attacks what prior work ignored:
- Recent work already gives a 64-modular order-668 object, but not a dynamic mechanism for lifting it to exact orthogonality.
- Exact searches usually restart from scratch inside a rigid family; they do not exploit a near-solution as a structured warm start.
- Local update rules can target the residual Gram-matrix defects directly instead of optimizing a global score from a random initialization.

Why it is not derivative:
- The search is over **repair dynamics on a certified near-solution**, not over another static family.
- The objective is a modulus ladder, not "solve 668 from zero with a fancier optimizer".

First test:
1. Reconstruct the published 64-modular order-668 matrix and its defect pattern.
2. Encode each off-diagonal Gram entry as a local residue state and define CA updates that only accept moves improving a lexicographic objective `(modulus reached, defect count, max defect magnitude)`.
3. Test whether local updates can lift small benchmark instances from `2^r`-modular to `2^(r+1)`-modular before touching 668.
4. Try block-local and row-local rule sets separately to see whether one consistently improves the modulus.

Fast falsifier:
- If the best CA cannot lift solved smaller instances by even one modulus step, or cannot improve the 668 seed beyond modulus 64, kill this branch.

Angle to avoid:
- Do **not** stop at "another modular paper" or drift back into a plain Goethals-Seidel/SAT search that happens to start from the modular seed.

## Direction 3: Orbit-representative path CA on compressed 167-bit supports

**Hypothesis.** Search the missing weight-80 support through its unique path representative in each cyclic orbit, and run a CA on the compressed run/descent encoding rather than on raw 167-bit strings.

Why this attacks what prior work ignored:
- The cyclic-convolution analysis gives a natural compressed state space: when length 167 and weight 80 are coprime, each cyclic orbit has a unique path representative.
- The same analysis shows that runs, descents, and low-dimensional autocorrelation marginals carry real combinatorial information, but current searches still mostly operate on raw sequences or rigid algebraic templates.
- A path/run CA gives a local dynamical language matched to the combinatorics of the obstruction itself.

Why it is not derivative:
- The cells are not raw bits; they are run lengths, ascent/descent markers, or short path motifs.
- Compression is not just preprocessing for SAT or annealing; it is the native search space.

First test:
1. Convert weight-80 subsets of `Z_167` to canonical path representatives.
2. Define a CA on run-length tokens or descent indicators that preserves total weight and cyclic admissibility.
3. Score candidates by distance to the target autocorrelation, plus simple necessary conditions from PSD and low-order marginals.
4. Compare against a raw-bit CA with the same evaluation budget to see whether path compression actually helps.

Fast falsifier:
- If the compressed CA offers no better hit rate on the target autocorrelation than a raw-bit baseline, or if it spends most of its time in invalid/noncanonical states, abandon it.

Angle to avoid:
- Do **not** fall back to raw-sequence SAT/GA search with a tokenization layer on top. If the rules no longer act on path-orbit structure, this direction has collapsed into an old family.

## Best first bet

Start with **Direction 1**.

Reason:
- It attacks the sharpest currently identified obstruction for 668.
- It keeps the search target narrow enough to falsify quickly.
- It uses CA as a genuinely new parameterization of the missing object instead of as a wrapper around an existing search family.

## Pivot rules

- If a branch becomes "search Williamson/Turyn/SDS objects, but with a CA front-end", mark it derivative and stop polishing it.
- If a branch cannot express either the specific 167/80 autocorrelation target or the 64-modular lifting target with explicit local invariants, it is probably too far from the actual obstruction.
- If a branch cannot beat random cyclic-subset baselines on the specific 167-length autocorrelation target, kill it early.

## Evidence snapshot

- Order 668 is still treated as open in the standard Hadamard sieve literature and in recent computational work.
- The 2025 convolution-number paper sharpens the problem to a missing length-167 autocorrelation-realizability question inside a Goethals-Seidel style reduction.
- A 2025 construction provides a 64-modular Hadamard matrix of order 668, so "repair a near-solution" is a live alternative to "search from scratch".
- Standard families and their computational variants remain active: Goethals-Seidel plus supplementary difference sets, SAT+CAS enumeration of Williamson variants, simulated annealing from Turyn sequences, and quantum/QAOA formulations of Williamson/Turyn/Baumert-Hall searches.
- CA is connected to Hadamard-adjacent combinatorics through linear bipermutive CA, MOLS, and bent-function constructions, but that route currently lands in very structured regimes rather than the 668 obstruction.

## Minimal references used for this memo

- Local repo artifacts: `results/research_context.json`, `results/literature/gap_frontier.json`, `results/literature/prior_art_watchlist.md`
- Piza Volio, *Search of Hadamard Matrices by Turyn Sequences* (2011)
- Kharaghani, Đoković, and Tayfeh-Rezaie, *Some new orders of Hadamard and skew-Hadamard matrices* (2013/2014)
- Bright, Kotsireas, Heinle, Ganesh, and Czarnecki, *A SAT+CAS Method for Enumerating Williamson Matrices of Even Order* (2018)
- Suprijadi et al., *Quantum computing formulation of some classical Hadamard matrix searching methods* (2022)
- Constantine and Constantine, *Convolution numbers* (2025)
- Eliahou, *A 64-modular Hadamard matrix of order 668* (2025)
- Arostegui et al., *A quantum approximate optimization method for finding Hadamard matrices* (2025)
- Mariot et al., *Mutually Orthogonal Latin Squares based on Cellular Automata* (2019)
- Gadouleau, Mariot, and Picek, *Bent Functions from Cellular Automata* (2020)
- Mariot et al., *Heuristic search of (semi-)bent functions based on cellular automata* (2022)
- Wolnik et al., *A split-and-perturb decomposition of number-conserving cellular automata* (2020)
