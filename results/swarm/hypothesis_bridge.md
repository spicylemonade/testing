Overlap/pivot note: I am explicitly rejecting two derivative framings up front: "forcing pairs are just sandpiles with new names" and "constructible graphs are just tilings/SFT encodings." The three hypotheses below only stay interesting if they add a new invariant, a quantitative transfer theorem, or a verifier-coupled search method. They should be killed immediately if their signal survives `X`-label shuffling.

## 1. Flow-Firing Odometers as Exact Forcing Decoders
**Closest prior art:** Flow-firing / higher-dimensional chip-firing, abelian networks, and abelian logic gates.

**Why it is different:** The bridge is not to reinterpret `R,T` forcing as generic avalanche reachability. Instead, compile an `X`-constructible graph into a fixed flow-firing automaton on a planar cell complex where each legal toppling corresponds to a verifier-legal signed edge update, and where the odometer or burning certificate is decoded back into exact `R,T` growth. The new claim is that a sandpile-specific invariant, not just local propagation, can rank or constrain candidate low-score families.

**Falsifiable prediction:** For a fixed compiler from constructible graphs to flow-firing instances, odometer concentration near a small set of "charge sinks" will predict which vertices become verifier-certifiable in `T`, and this predictive power will disappear when the same graph geometry is kept but the nonzero labels in `X` are shuffled.

**Required experiments:**
- Implement one fixed graph-to-flow-firing compiler and one fixed decoder from toppling traces back to legal `R,T` updates.
- Benchmark on small constructible graphs with true labels, shuffled-label controls, and degenerate-label controls.
- Measure whether odometer features forecast eventual verifier-certified `T` growth better than raw graph features such as degree profile or layer depth.
- If the signal is real, search for low-score families by optimizing the flow-firing invariant first and only then decoding candidate proofs.

## 2. Number-Conserving Cellular Automata as a Rational-Complexity Search Prior
**Closest prior art:** Number-conserving cellular automata and particle representations of conservative CA, together with bounded-slope / rational-complexity work on arithmetic Kakeya.

**Why it is different:** This is not a vague "spread means projection growth" analogy. The proposal is to encode each slope in `X` as a conserved particle species in a small-radius CA, so that local collisions implement only admissible linear interactions and the anisotropic current profile becomes a proxy for low rational complexity. The bridge only matters if one can transfer a CA observable such as direction-dependent current imbalance or support growth, after subtracting the trivial light-cone baseline, to actual projection-set cardinalities or to verified score.

**Falsifiable prediction:** Among conservative CA with the same radius and alphabet size, rules whose current strongly suppresses the `(1,-1)` channel while keeping the `x . G` channels concentrated will decode into constructible graphs with systematically lower verified score than random search or unconstrained evolutionary search; that advantage should vanish under `X`-label shuffling.

**Required experiments:**
- Enumerate or sample small 2D number-conserving CA families with a fixed encoding of slopes as particle species.
- For each rule, evolve many small seeds, decode the terminal or periodic configurations into candidate `X`, `G`, `R`, and `T`, and evaluate the true score exactly.
- Regress verified score against CA observables such as directional current, support width, entropy rate, and collision counts after removing the transport baseline.
- Compare against random graph search, local mutation search, and label-shuffle controls to test whether the CA is capturing arithmetic structure rather than generic transport.

## 3. Verifier-Coupled Neural Cellular Automata for Symbolic Proof Growth
**Closest prior art:** Growing neural cellular automata / differentiable morphogenesis, plus machine-assisted symbolic search for difficult mathematics.

**Why it is different:** The NCA is not being used as a black-box generator of pretty patterns. It is a local-rule synthesizer whose state alphabet is discretized into candidate edge labels, glue decisions, and seed `R,T` markers, with an exact post-hoc decoder that keeps only verifier-valid outputs. The bridge becomes non-derivative because the model must learn a reusable local growth rule that generalizes across larger product grids, rather than memorizing one hand-tuned construction.

**Falsifiable prediction:** If arithmetic structure is genuinely learnable by a local CA, then a neural CA trained only on small constructible instances will generalize to larger layer sizes and produce verifier-valid candidates with better score than random initialization or direct sequence models; the gain should collapse when trained on label-shuffled data or when the exact decoder is replaced by a permissive heuristic.

**Required experiments:**
- Build a differentiable relaxation of the six-line output format in which cell states represent local edge labels, gluing actions, and seed forcing data.
- Train a neural CA with curriculum on small instances, but score candidates only through an exact discrete decoder and verifier-validity filter.
- Test out-of-size generalization on larger `d_1 x ... x d_k` grids and compare with autoregressive sequence models, evolutionary search, and random search.
- Run ablations for label shuffling, decoder removal, and conservation constraints to determine whether the learned rule is discovering arithmetic content or only generic recursive structure.
