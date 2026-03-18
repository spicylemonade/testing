# Phase 3 H2 Program

## Route

`H2_target_direction_abelian`

## Constraint

H2 is not a parallel free-for-all. It operates only on the same extracted corridor families produced by the frozen H1 grammar.

It becomes active only if the pre-registered H1 pivot trigger fires.

## Invariant Package

For each extracted candidate family, compute:

- rank of the exact relation matrix,
- Smith normal form of the relation matrix,
- support size of `R`,
- edge density `m(G) / n(G)`,
- determinant pattern and coordinate-height summary of the chosen nonzero labels in `X`,
- target-direction torsion or invariant factors aligned with the line spanned by `(1,-1)`.

## Comparison Features It Must Beat

The imported abelian invariants survive only if they improve screening or prioritization relative to these raw arithmetic descriptors:

- rank,
- Smith normal form,
- support size,
- edge density,
- determinant pattern in `X`,
- coordinate height of `X`,
- corridor width and grammar description length.

## Reporting Rule

H2 must report on the same family IDs and the same matched baselines as H1.

Valid H2 claim:

- “target-direction abelian invariants screened the same corridor family better than direct arithmetic features”

Invalid H2 claim:

- “arithmetic Kakeya forcing is an abelian network”

## Kill Condition

Kill H2 immediately if invariant-guided screening does not retain the best exact certificates more efficiently than the direct arithmetic feature set.
