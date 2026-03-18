# Phase 2 Symmetry And Canonicalization Policy

## Goal

Prevent duplicated search effort and benchmark inflation from equivalent encodings of the same corridor family.

## Quotientable Symmetries

### 1. Global sign flip

- Apply `x -> -x` to every nonzero element of `X`, every nonzero edge label in `f_i`, and every singleton in `R`.
- This preserves the target line up to sign and does not change forceability or score.

### 2. Coordinate swap

- Apply `(a,b) -> (b,a)` uniformly to all nonzero labels in `X`, `f_i`, and `R`.
- Since `(1,-1)` maps to `(-1,1) = -(1,-1)`, the target line is preserved up to sign.

### 3. Corridor reflection

- Reverse the width direction:
  - reverse the substitution word,
  - swap `left` and `right` boundary tags,
  - reverse the horizontal dictionary index `c -> W-c`,
  - reflect `R` and `T` across the width axis.

### 4. Row reflection

- Reverse the row order:
  - `r -> H+1-r`,
  - reverse the vertical profile `nu`,
  - reflect row indices in `R`, `T`, and `f_2`.

### 5. State relabeling

- Rename states in `Sigma` by first occurrence order after expansion.
- Equivalent substitution systems that differ only by state names are identified.

## Not Quotientable

### 1. Stage order

- The transposed family is **not** quotientable to the original family.
- Reason: swapping stage order changes which edges live in `f_1` versus `f_2`, which is part of the legal constructible grammar.
- We therefore treat stage-order swap as a required perturbation baseline, not as an equivalence.

### 2. Aspect ratio

- `H x W` and `H' x W'` with different ratios are not quotientable.
- Reason: boundary overhead and transfer behavior are score-relevant in this problem.

### 3. Duplicate macrotiles with different local payloads

- If two columns share interfaces but differ in `seed_tag`, `solved_tag`, or emitted horizontal profile, they are distinct states.

## Canonical Form

Every candidate is stored and benchmarked in a canonical form.

### Canonicalization steps

1. Expand the family to a concrete corridor word.
2. Apply all quotientable symmetries listed above.
3. For each symmetric image, serialize the tuple
   - `X`
   - `H`
   - `nu`
   - expanded word with state payloads
   - extracted `f_2`
   - extracted `R`
   - extracted `T`
4. Choose the lexicographically smallest serialization.

### Search rule

- Two candidates with the same canonical serialization are treated as duplicates.
- Future search and benchmark scripts must canonicalize before counting a candidate as new.

## Why This Policy Is Strict Enough

- It removes superficial duplication from sign, swap, reflection, and state naming.
- It keeps stage-order and aspect-ratio perturbations available as genuine controls rather than hiding them inside the quotient.
- It prevents the search from claiming diversity when it only found mirrored or renamed variants.
