# Literature Comparison Memo

## Scope

This memo compares the current experiment package against the literature branches that
actually survived Phase 1:

- OEIS `A129258` / `A129259` and Kimberling as provenance
- Ford's multiplication-table and divisor-in-an-interval work as the main overlap risk
- multiplicative-basis papers as the de-prioritized H3 control branch
- the `reframings.json` domains only where they illuminate the current data

## 1. OEIS / Kimberling Provenance

What the experiments add:

- the validated baseline extends the public small-horizon picture to a reproducible
  million-step artifact with record gaps up to `30`;
- the gap trajectory now includes late records `25`, `28`, and `30`;
- the package includes witness-level and full-hypergraph artifacts rather than just row
  terms.

What the experiments do **not** add:

- no proof of boundedness;
- no disproof of boundedness;
- no replacement for OEIS / Kimberling as the canonical provenance of the object and the
  question.

Comparison:

- Relative to OEIS `A129258`, `A129259`, and Kimberling's problem statement, the current
  package is an empirical/mechanistic supplement only.
- The correct framing is still: *the public problem remains open, but the repo now has a
  stronger validated evidence package than the public term dump alone*.

## 2. Ford Overlap Branch

This remains the closest relevant mathematical comparison.

What looks Ford-like in the current data:

- skipped values in late record gaps are still explained by local border-factor pairs;
- late gaps remain dominated by low multiplicity rather than high redundancy;
- the full-hypergraph export for gaps `21`, `25`, `28`, and `30` shows weak factor reuse
  even after all admissible witnesses are enumerated.

Concrete signals:

- gap `30` has `29` skipped values but only `43` total admissible witness pairs;
- those `43` pairs use `39` distinct row factors and `41` distinct column factors;
- the balanced-factor share rises from `1/18` at gap `19` to `13/29` at gap `30`.

Interpretation relative to Ford:

- this is exactly why the novelty report treats Ford as the main overlap hazard;
- the data still looks closer to divisor/product coverage near a frontier than to a new
  compact mex-coupled certificate;
- the current package is strongest when used as a **negative comparison** against Ford:
  the raw witness language does not separate itself cleanly from Ford-style local
  coverage.

## 3. Multiplicative-Basis Branch

The million-step data does not justify reviving the H3 multiplicative-basis lane.

- The active experiments remain local and frontier-based, not asymptotic basis-density
  arguments.
- The variant comparison shows that nearby admissibility changes alter trajectories
  without changing the qualitative negative result, which is not the kind of evidence
  that would support a near-minimal multiplicative-basis theorem.
- The current witness and hypergraph artifacts still speak about local consecutive
  coverage, not order-2 basis optimality.

Comparison:

- Pach-Sandor, Pus, Dressler, and Nathanson remain useful only as overlap controls.
- Nothing in the current run package materially narrows the multiplicative-basis branch
  into a proof program.

## 4. Reframe Artifact Versus Data

`results/concept_evolve/reframings.json` generated several possible domain views. The
experiments already discriminate among them.

Still plausible:

- **nonunique factorization theory**: the full witness hypergraphs really are constrained
  factorization objects, and the new export makes this framing more concrete than it was
  before the million-step run.
- **combinatorics on words / symbolic dynamics** only as a descriptive question: the gap
  word may still be studied, but the current data does not show a finite low-complexity
  witness alphabet behind it.

Currently weak:

- **Beatty/complementary sequence** and **uniform mex periodicity** frames are not
  supported by the growing record gaps or by the lack of a stable small witness grammar.
- **statistical-physics / adsorption** is still phenomenological only; it has not yet
  produced a sharper claim than the direct witness data.

Interpretation:

- the reframe artifact is useful as a pruning tool.
- after the million-step run, the factorization/hypergraph framing is the only one that
  still lines up directly with the stored evidence.

## 5. Bottom Line

Compared with the literature, the current package says:

- stronger than OEIS/Kimberling on reproducible evidence, but not on final theorem status;
- too close to Ford-style local coverage to support a positive mechanism claim;
- not strong enough to reopen the multiplicative-basis branch;
- most naturally interpreted through constrained factorization / witness-hypergraph
  language, which is exactly the narrowed H1 rescue path left alive by the novelty round.
