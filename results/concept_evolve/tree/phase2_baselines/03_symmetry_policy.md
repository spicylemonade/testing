# 03 Symmetry Policy

## Prerequisites

- certificate grammar frozen
- active geometry fixed to the corridor family

## Dependency Edges

- depends on: certificate grammar
- enables: duplicate-free search
- enables: fair benchmark accounting

## Why This Branch Could Lower Score

- Canonicalization prevents the search from wasting budget on mirrored or renamed duplicates.
- Keeping stage-order and aspect-ratio perturbations out of the quotient preserves them as real controls.

## Why This Branch Could Fail

- An over-aggressive quotient could erase genuine perturbation baselines.
- An under-aggressive quotient could overcount diversity and inflate search performance.
- If canonicalization ignores payload differences, distinct `R/T` programming can be mislabeled as one family.
