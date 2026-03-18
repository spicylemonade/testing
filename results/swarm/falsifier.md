# Falsifier Memo

The auto-generated watchlist for this run is low-signal. The real falsification pressure comes from the arithmetic-Kakeya literature and from the gap between local CA dynamics and the verifier's nonlocal integer-linear closure.

## Fastest kill criteria

- Kill the claim if the apparent gain disappears under exact verifier-valid evaluation over `\mathbb{Z}`. A CA pattern that only looks good before the six-line witness is decoded is not evidence.
- Kill the claim if the gain survives `X`-label shuffling at fixed graph geometry and fixed nonzero-label multiset. Then the method is exploiting geometry or edge density, not arithmetic structure.
- Kill the claim if the best witnesses live only in tiny fixed alphabets or boundedly many slopes. That is the regime most vulnerable to bounded-slope / rational-complexity objections rather than progress toward the `<= 1.675` target.
- Kill the claim if the decoder or compiler is doing the hard work. If the CA emits loose proposals that need aggressive repair, the novelty is in the repair heuristic, not in the automaton.
- Kill the claim if performance vanishes out of size or out of alphabet. A local rule that only works on the grid sizes seen during search is memorizing one witness family.

## Missing controls

- Exact integer verifier control:
  Every candidate must be scored only after exact decoding into `(X,G,R,T)` and exact forcing verification over `\mathbb{Z}`. No proxy score, no mod-`p` relaxation, no permissive repair.
- Label-shuffle control:
  Keep the constructible graph geometry fixed, randomly permute the nonzero labels in `X`, and re-evaluate. A real arithmetic signal should collapse.
- Complexity-matched baseline:
  Compare against random graph search, local mutation search, and whole-witness evolutionary search with the same compute budget, the same `|X|`, and the same edge-density budget.
- Decoder-matched baseline:
  Keep the same compiler, extractor, and exact verifier, but replace the CA with non-CA search. Otherwise the arithmetic content may sit in the handwritten decoder rather than in the automaton.
- Rational-complexity sweep:
  Run small-, medium-, and unrestricted-complexity `X` regimes. A CA that only wins in the lowest-complexity regime is exactly the bounded-slope trap.
- Mod-`p` / mod-`N` lift control:
  Any curriculum or toy success over finite fields or rings must be followed by integer lift-back. If the motif dies over `\mathbb{Z}`, it was a modular mirage.
- Construction-cost accounting:
  Count the full verifier-visible cost `m(G) + |R|` after compilation. Do not score only local propagation density or certificate count.
- Out-of-distribution generalization:
  Hold out larger `d_1 x ... x d_k` shapes, different aspect ratios, and different valid alphabets `X`. Otherwise the CA is just fitting one grammar.
- Equivalent-formulation transfer:
  If the search is claimed to discover arithmetic structure, test whether the same motif survives translation to a nearby equivalent formulation, not only the chosen forcing-pair encoding.

## Benchmark traps

- Proxy-metric trap:
  Forced-vertex growth, odometer mass, current imbalance, entropy reduction, or certificate reuse are not acceptable endpoints. They are only admissible if they predict lower exact verified score.
- Compute mismatch trap:
  "Best found by CA" is meaningless if the baselines get less search budget or weaker parameterizations.
- Decoder leakage trap:
  If the decoder enforces most of the witness validity, the CA is not learning arithmetic structure. The control is decoder ablation and decoder-randomization.
- Nearby-size leakage:
  Training on `d x d` and testing on `d+1 x d` is weak evidence. The holdout must be large enough that memorized local tilings stop working.
- Fixed-`X` trap:
  Repeatedly optimizing one hand-chosen small alphabet invites overfitting to that alphabet's accidental linear relations.
- Best-of-many reporting trap:
  Report hit rate and distribution of scores, not only the best witness after many restarts.
- Modular toy-task trap:
  Finite-field or `\mathbb{Z}/N\mathbb{Z}` tasks are acceptable curricula, not acceptable evidence for the integer target.
- Encoding trap:
  A method may optimize quirks of the six-line serialization rather than the mathematics. Equivalent encoding checks are needed.
- Frontier trap:
  Any proxy win that does not survive exact accounting of the stated objective `(m(G)+|R|)/(n(G)-|T|) <= 1.675` is irrelevant to the task.

## Novelty illusions and overlap accusations

- "This is just bounded-slope search in CA clothing."
  A fixed small CA alphabet naturally induces a small slope set and low rational complexity. Without a mechanism that escapes that regime, the work risks rehashing bounded-slope arithmetic-Kakeya territory.
- "This is just a tweak of existing small constructive witnesses."
  If the output is another tidy self-similar gadget or a minor perturbation of known small constructive examples, the CA framing is cosmetic.
- "This is just generic automated search."
  If the contribution is only that an automated system searched the witness space, the closest overlap is generic mathematical-discovery search, not a new arithmetic-Kakeya insight.
- "This is just a sandpile / flow-firing analogy."
  If odometer or avalanche features merely track graph depth or bottlenecks, the flow-firing story adds no arithmetic content.
- "This is just tilings / SFT / linear-CA pattern generation."
  Reversible, bipermutive, or periodic patterns are not novel unless they give a verifier-visible forcing advantage.
- "This is just finite-field or modular behavior."
  Additive CA are far more natural over finite alphabets than over the integer witness space. A method that only works modulo `p` or `N` does not address the target object.
- "This is just pattern-problem or generalized-AK overlap without transfer."
  If the search signal exists only in a nearby equivalent formulation, the work is not novel until it transfers back to the stated forcing-pair problem.

## Literature branches that invalidate weak claims

- Green-Ruzsa, *On the arithmetic Kakeya conjecture of Katz and Tao* (2017):
  Must be cleared for equivalent formulations and for the finite-field variant. Weak claims that rediscover finite-field structure or restate an equivalent formulation should be rejected.
- Cowen-Breen, Karangozishvili, Varadarajan, Wang, *Pattern Problems related to the Arithmetic Kakeya Conjecture* (2020):
  Must be cleared if the CA is really optimizing a denser pattern-count problem rather than the forcing-pair problem itself.
- Pohoata-Zakharov, *Generalized Arithmetic Kakeya* (2024):
  Must be cleared if a claim is dressed up as a new formulation or iterative strengthening but does not produce a stronger witness in the original setting.
- Tao, *Sum-difference exponents for boundedly many slopes, and rational complexity* (2025):
  This is the main structural warning against small-alphabet CA stories. If the method cannot leave low-complexity slope regimes, it is probably polishing the wrong corner of the search space.
- Hickman-Wright, *The Fourier restriction and Kakeya problems over rings of integers modulo `N`* (2018):
  Must be cleared before claiming anything from modular curricula or automata over finite rings.
- AlphaEvolve and related machine-math discovery systems (2025):
  Must be cleared before claiming novelty for "automated search found a construction." The differentiator has to be a verifier-coupled extractor, a reusable invariant, or a genuinely new witness.
- Flow-firing / chip-firing / abelian-network literature:
  Must be cleared if the bridge hypothesis uses odometers, burning tests, or abelian invariants. Otherwise the work risks being a transferless analogy.
- Number-conserving CA and neural CA literature:
  Must be cleared if the claim is methodological rather than mathematical. Reusing standard CA search machinery does not create arithmetic novelty.

## Easiest empirical failure modes by hypothesis

- Symbolic forcing-front CA:
  Easiest failure is that local state summaries correlate with eventual forcing on tiny grids but stop predicting anything once exact integer elimination is required. Another easy failure is total collapse under label shuffling.
- Sparse-defect amplifier:
  Easiest failure is that the "defects" are just hand-placed ad hoc certificates. If density-matched random perturbations perform the same, the defect story is empty.
- Reversible / bipermutive CA:
  Easiest failure is that reversibility only creates pretty periodic structure. If density-matched nonreversible rules give the same decoded scores, the reversible invariant is irrelevant.
- Flow-firing / abelian-network bridge:
  Easiest failure is that odometer or sink features predict `T` growth no better than raw graph depth, degree, or layer position. Then the sandpile bridge is not carrying arithmetic information.
- Number-conserving CA prior:
  Easiest failure is that directional-current observables look correlated with score before exact decoding, but the correlation disappears after exact witness verification or outside tiny fixed alphabets.
- Neural CA:
  Easiest failure is apparent generalization that vanishes on larger grids, new aspect ratios, or new alphabets `X`. If exact decoder validity drops sharply out of distribution, the model learned a brittle serialization prior.

## Bottom line

- The easiest accusation is not "cellular automata are irrelevant."
- It is "this is a bounded-slope, modular, or generic-search artifact that never survives exact integer verification and never escapes existing formulations."
- Any CA program here should be treated as false until it passes exact `\mathbb{Z}` verification, label-shuffle controls, complexity sweeps, and out-of-distribution witness tests.
