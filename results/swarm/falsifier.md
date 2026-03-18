# Falsifier Memo

Scope: adversarial read of the three bridge hypotheses in [hypothesis_bridge.md](/home/archivara/work/repo/results/swarm/hypothesis_bridge.md) against the actual certificate problem and the most obvious prior-art branches.

## Literature-Screen Caveat

- The repo-local `prior_art_watchlist.md` is not trustworthy for this task; it was generated from a corrupted LaTeX-token query and mostly surfaced unrelated math papers.
- A direct Semantic Scholar search for `arithmetic Kakeya cellular automata` also produced mostly quantum-dot cellular-automata hardware papers, not relevant combinatorics. So absence of direct hits is not positive novelty evidence. The falsification standard has to come from nearby mature literatures, not from a literal keyword gap.

## Immediate Kill Criteria

- Reject any result that is not extracted to an exact legal certificate `(X; d_i; f_i; T; R)` and checked under the verifier semantics. A CA trajectory, decoder success rate, or bootstrap-style filling event is not evidence by itself.
- Reject any score claim benchmarked against stale or relaxed targets. The live bar is `<= 1.675`, not older `1.75`-style formulations and not “trending below `1.70` on moderate sizes.”
- Reject any method claim that hides complexity outside the score: exploding CA state count, exploding coordinate height in `X`, bespoke global compilers, or scale-specific macrotiles. Those may still produce a legal certificate, but they do not support a strong “cellular automata” novelty claim.
- Reject any claimed advantage that disappears under matched controls for `|X|`, coordinate height, stage depth `k`, edge density `m/n`, product geometry, and optimizer budget.

## Cross-Cutting Failure Modes

### 1. The CA story may be only a search prior

The formal system is not local. Rule (3) allows arbitrary global `\mathbb{Z}`-linear combinations, while the forcing rule depends on exact support clearing outside `T \cup {e}`. If the CA only proposes motifs and the real work is done by a separate exact linear-algebra back-end, then the contribution is “a heuristic search prior for small-graph certificates,” not “solving it using cellular automata.”

Weak claim form to avoid:
- “Arithmetic Kakeya forcing is a cellular automaton.”

More defensible claim form:
- “A CA-inspired search prior proposes candidate certificates that are then exactly verified.”

### 2. The comparison set can be gamed easily

Any of these will invalidate a weak empirical claim:
- Comparing only against isotropic grids instead of against direct certificate search on the same `X` and same product geometry.
- Comparing a CA family with a tuned extractor against random or isotropic controls with a weaker extractor.
- Reporting only best-of-many hits rather than a frontier over search budget and family size.
- Ignoring symmetry quotienting. Many candidate certificates are equivalent up to sign flips, coordinate swaps, `GL_2(\mathbb{Z})` changes of basis, or stage reorderings.

### 3. Finite-size wins are especially suspect here

The score is boundary-sensitive through both `m(G)` and the forcing terms `R,T`. A family can look strong on one aspect ratio or one recursion depth and then revert once boundary overhead stops dominating. A sub-`1.675` claim is weak unless it survives:
- increasing scale with the same local rule family,
- stage reordering,
- anisotropy perturbations,
- removal of hand-placed boundary seeds,
- and extraction to exact sparse `f_i` dictionaries rather than an implicit spacetime picture.

### 4. Novelty can collapse even if the certificate is real

A verified certificate could still look derivative if the paper overstates what is new. The easiest accusation may start one level earlier: the `X`-constructible / forcing-pair formulation already looks like a verifier-friendly repackaging of Katz-Tao small-graph / sum-difference arguments, so a CA reinterpretation risks becoming a second relabeling. Beyond that, the work can still look derivative if it mostly repackages existing theories:
- bootstrap percolation / critical droplet language for bridge 1,
- abelian networks / chip-firing / sandpile language for bridge 2,
- expander codes / local decoders / peeling thresholds for bridge 3.

The novelty burden is not “we used that language.” The novelty burden is “that imported invariant predicts or explains low-score certificates better than direct arithmetic baselines.”

## Bridge 1: Critical-Droplet Anisotropic Forcing

### Easiest way it fails

Critical droplet difficulty may have no predictive value for certificate score after legal extraction. Bootstrap percolation difficulty is about threshold growth from random or seeded occupied sets under local monotone rules. The arithmetic Kakeya objective is a deterministic ratio `(m+r)/(n-t)` under exact linear elimination. Those are different objectives, and a monotone-growth proxy can easily optimize the wrong thing.

### Easiest rehash accusation

If the paper says “forcing behaves like anisotropic bootstrap percolation” and then ranks rules by droplet difficulty, the natural response is: this is bootstrap percolation folklore plus a compiler. The bar for novelty is much higher than importing Toom-like or anisotropic language.

### Missing controls

- Matched isotropic controls with the same radius, same `|X|`, same coordinate height, and same extractor.
- Random sparse-label controls with the same edge density and same aspect ratios.
- Direct arithmetic baselines on the same graph family with no CA prior at all.
- Bounded-slope controls. If the rule only realizes a bounded or low-rational-complexity slope alphabet, Tao-style bounded-slope barriers are the obvious explanation, not CA structure.
- Extraction controls: the same CA rule evaluated once by spacetime occupancy and once by exact verifier-compatible extraction.

### Benchmark traps

- Using fill time, droplet size, or occupation threshold as a proxy for score.
- Claiming success because the family trends below `1.70` at moderate `n` without an exact sub-`1.675` certificate.
- Letting the effective label set `X` or the rule table grow with scale while still marketing the method as a finite local rule.

### Literature branches that can invalidate weak claims

- Arithmetic Kakeya / bounded-slope branch: Green-Ruzsa; Tao on boundedly many slopes and rational complexity.
- Bootstrap percolation / critical CA branch: Bollobas-Duminil-Copin-Morris-Smith; Hartarsky-Mezei; anisotropic bootstrap percolation literature.
- Open-problem frontier branch: if the family is still bounded-slope or “elementary,” the known `3/2`-type ceiling is the immediate objection.

## Bridge 2: Multispecies Abelian-Network Forcing

### Easiest way it fails

The imported abelian-network invariants may be too coarse. Halting, least action, or critical-group structure might correlate weakly with forcing completion but not with low score. It is easy to rediscover that some families halt or have attractive torsion without learning anything about minimizing `m+r` relative to `n-t`.

### Easiest rehash accusation

This bridge is one sentence away from “chip-firing / sandpile / abelian networks can encode local propagation.” That is not new. Abelian networks already package communicating automata with local commutativity and explicitly contain bootstrap percolation as an example. Recasting arithmetic forcing in that language is not itself a contribution.

### Missing controls

- Compare every abelian invariant against trivial arithmetic features: rank, Smith normal form of the raw relation matrix, determinant pattern in `X`, support size of `R`, degree profile, and edge density.
- Compare predictive power for low score against a direct brute-force or greedy certificate search on the same family.
- Compare target-direction torsion claims against shuffled-label controls and random basis changes in `\mathbb{Z}^2`.
- Force the same family to pass both “halts / has critical-group feature” and “gives a low verified score.” If the first happens often and the second rarely, the bridge is not doing useful work.

### Benchmark traps

- Treating “halts on all inputs” as relevant. The certificate problem does not ask for a robust automaton over all inputs; it asks for one exact forcing witness.
- Treating recurrent-state or critical-group language as if it directly certifies the existence of isolated `(a,-a)` residues.
- Counting a search-speedup from invariant screening as a mathematical advance. That is a tooling gain unless it translates into a theorem or a verified score improvement over arithmetic baselines.

### Literature branches that can invalidate weak claims

- Abelian networks I-III and the chip-firing / sandpile critical-group literature.
- Any paper already interpreting bootstrap percolation or related growth models as abelian networks.
- Arithmetic Kakeya papers where the real signal is still determinant structure or sum-difference arithmetic, not automata theory.

## Bridge 3: Integer-Lifted Tanner Gadgets with Local CA Decoders

### Easiest way it fails

Decoder success under random noise is not the same as producing `(1,-1)` at single vertices by exact integer linear combination. Expander-code and topological-code decoders live in syndrome spaces over finite alphabets; the Kakeya certificate lives in an integer module with exact support constraints. The bridge can fail simply because threshold heuristics do not survive the lift.

### Easiest rehash accusation

Without a very explicit arithmetic gain, this will read as: “we put sparse checks on a graph and ran a local decoder.” That is classical expander-code / peeling-decoder territory, plus a problem-specific compiler.

### Missing controls

- Degree-matched random bipartite and product-graph controls, not just grids.
- Finite-field versus integer-lifted controls. If the integer lift does not beat the direct finite-field-inspired gadget after legal extraction, the arithmetic lift is cosmetic.
- Exact elimination controls. Compare the local decoder against a nonlocal arithmetic solver on the same candidate gadget.
- Stopping-set / threshold controls under deterministic adversarial seeds, not only random-noise models.

### Benchmark traps

- Reporting decoder threshold, syndrome shrinkage, or stopping-set statistics as if they were score.
- Using nonconstructible Tanner graphs and only later approximating them by legal product graphs.
- Claiming improvement from irregularity without matching for `|X|`, coefficient height, and extraction complexity.

### Literature branches that can invalidate weak claims

- Expander codes and local correctability literature.
- Local peeling / sweep / cellular-automaton decoder literature for coding and topological codes.
- Any decoder-threshold work where the actual contribution is probabilistic robustness rather than deterministic exact certification.

## Missing Baselines That Should Exist Before Any Strong Claim

- Direct certificate search with no CA story at all on the same `X` and same product families.
- Low-height asymmetric `X` enumeration baselines, since the repo already identifies arithmetic geometry of `X` as a more likely lever than raw CA dynamics.
- Bounded-slope and slowly growing-`X` baselines, because current frontier notes suggest the near-`1.675` regime is entangled with unbounded `X`.
- Same-family ablations:
  - remove anisotropy,
  - randomize seeds in `R,T`,
  - randomize labels in `X`,
  - replace local decoder with exact elimination,
  - freeze `X` while scaling `n`,
  - freeze the CA rule while perturbing aspect ratios.

If the claimed gain does not survive these ablations, it is not a robust bridge.

## Literature Branches That Need To Be Cleared Explicitly

- Core arithmetic Kakeya / sum-difference line: Green-Ruzsa, Pohoata-Zakharov, Tao, Cowen-Breen, and Katz-Tao-adjacent small-graph arguments.
- Barrier / obstruction line: bounded slopes, rational complexity, and elementary-argument ceilings.
- Non-uniformity / counterexample line: Lemm-style warnings against over-trusting symmetric or homogeneous search spaces.
- Bootstrap percolation / critical CA line for bridge 1.
- Abelian networks / chip-firing / sandpile line for bridge 2.
- Expander-code / local-decoder / peeling-threshold line for bridge 3.

## Bottom Line

The most likely bad outcome is not “the certificate is false.” It is:
- the CA framing only generates candidates while exact arithmetic does the real work,
- the reported gain disappears under matched arithmetic baselines,
- or the work lands as a repackaging of bootstrap percolation, abelian networks, or local-decoder folklore.

For this task, a weak sub-`1.675` empirical trend is not enough. The bar is an exact certificate, a matched-baseline win, and a novelty claim narrow enough that prior-art overlap cannot immediately swallow it.
