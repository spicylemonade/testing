# Local Rule No-Go Atlas

## Class under audit

We audit the following proof-carrying CA class:

- full-support strip witnesses of heights `2` and `3`;
- radius-1, one-sided updates, meaning a fresh column may use only:
  - row-singleton labels imported from the column immediately to its left;
  - the internal vertical edge labels of the fresh column itself;
- exact forcing checked by the rational-span verifier in
  `tools/kakeya_ca_exact.py`;
- alphabet restricted to the audited palette
  `[(1,0),(0,1),(1,1),(1,2)]`.

This is a completeness-guaranteed search class because every local rule in the
class reduces to a finite exact closure problem on a single fresh `h x 1`
column.  The exhaustive logs are:

- `results/theory/forcing_traces/local_strip_states/width2_one_sided.json`
- `results/theory/forcing_traces/local_strip_states/width3_one_sided.json`

## Exhaustive outcome

The checked counts are:

- height `2`: `256` local states;
- height `3`: `8,192` local states.

In both classes the number of strict-improvement cases is `0`.

Therefore:

> No one-sided radius-1 proof-carrying strip rule over the audited palette can
> activate a fresh column of height `2` or `3`.

This is an exact impossibility statement, not a proxy-model failure.  Every
case was run through the exact quotient-span forcing rule.

## Failure mechanism

The obstruction is local and algebraic.

For height `2`, the internal fresh-column dynamics split into:

- a symmetric mode carried by the horizontal rail differences;
- an antisymmetric mode carried by the single vertical rung.

The target of forcing a single vertex requires both modes.  One-sided input can
import symmetric information from the left, but it cannot manufacture the
missing antisymmetric diagonal direction in a fresh seedless column.  The exact
table confirms that this obstruction never disappears anywhere in the audited
alphabet.

Height `3` has a larger internal mode space, but the exhaustive local table
shows that one-sided row-singleton input is still insufficient to create a new
forced row.  So the first two nontrivial strip widths both fail for the same
high-level reason: unilateral transport does not create the first genuinely new
local proof certificate.

## First barrier break

The first exact-valid family immediately beyond this no-go frontier is the
coupled `2x2` warm-up regime, whose trace corpus is stored under
`results/theory/forcing_traces/tiny_2x2_full_seeds_le3/`.

That regime is not unilateral:

- it uses coupled information from multiple seeded corners;
- the exact-valid traces always have the same two-layer nucleation pattern:
  one corner appears first, then the other three vertices collapse.

So the barrier breaks only once the automaton is allowed to use coupled local
state rather than a left-to-right wave.

## Frontier statement

The score frontier relevant to the original task is not blocked by geometry
alone:

- a full `2xN` strip with `o(N)` seeds would beat `1.675`;
- a full `3xN` strip with `O(1)` initial resources would also beat `1.675`.

The atlas shows that the failure of the first simple CA lanes is instead caused
by an exact local-rule obstruction.  This separates the phenomenon from:

- decoder leakage, because the check is exact;
- geometry-only sparsity effects, because the audited strips are full-support;
- a bounded-slope mirage, because the obstruction persists already inside a
  four-label palette that contains the warm-up-valid `7/4` micro-gadgets.

## Consequence

Any remaining CA search below the target score must leave the unilateral strip
class.  The admissible next regimes are:

- two-sided coupled strips;
- typed macrocells whose interior starts with more than one boundary source;
- wider blocks whose first activation is genuinely multi-column.
