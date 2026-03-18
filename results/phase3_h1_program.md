# Phase 3 H1 Program

## Route

`H1_macrocell_substitution`

## Frozen Active Family

The active H1 family is a height-2 corridor substitution automaton.

- `H = 2`
- `k = 2`
- `d_1 = 2`
- `d_2 = W_\ell`
- substitution width `w = 2`
- active state cap `|Sigma_active| <= 8`

## Frozen Interface Alphabet

`I = {closed, carry_a, carry_b, gate}`

Composition rule:

- internal column boundaries must satisfy equality of the outgoing interface of the left column and the incoming interface of the right column;
- outer boundaries must satisfy the fixed boundary condition
  - leftmost `i_L = closed`
  - rightmost `i_R = closed`

This is the only allowed composition rule for H1.

## Frozen Template States

The active search may use only a subset of the following templates.

1. `L_a = (left, closed, carry_a, [p1, 0], [0, 0])`
2. `L_b = (left, closed, carry_b, [0, p2], [0, 0])`
3. `M_a = (middle, carry_a, carry_a, [0, 0], [0, 0])`
4. `M_b = (middle, carry_b, carry_b, [0, 0], [0, 0])`
5. `M_g = (middle, gate, gate, [0, 0], [0, 0])`
6. `M_ab = (middle, carry_a, carry_b, [0, 0], [0, 0])`
7. `R_a = (right, carry_a, closed, [0, 0], [0, 0])`
8. `R_b = (right, carry_b, closed, [0, 0], [0, 0])`

No additional state template is allowed in the active H1 pilot.

## Exact Extractor

The vertical profile is fixed to one token:

- `nu = [z]`

The horizontal extractor `eta` depends only on the shared interface of an adjacent legal pair:

- shared `closed` -> `[0, 0]`
- shared `carry_a` -> `[u, 0]`
- shared `carry_b` -> `[0, v]`
- shared `gate` -> `[w, w]`

where `u, v, w, z` are four distinct nonzero elements of `X`.

The active H1 search varies only:

- the actual integer vectors chosen for `u, v, w, z`,
- the active subset of template states,
- the substitution map `sigma : Sigma_active -> Sigma_active^2`.

It does **not** vary:

- the interface alphabet,
- the extractor form,
- the boundary rule,
- the corridor height.

## Level-1 To Level-2 Transfer Protocol

1. Choose one legal seed word `w_0`.
2. Apply the frozen substitution once to obtain the level-1 word `w_1`.
3. Extract the exact certificate `(X; d_i; f_i; T; R)` from `w_1` and score it exactly.
4. Apply the same substitution again to obtain the level-2 word `w_2`.
5. Extract the exact certificate from `w_2` with the same `X`, `nu`, and extractor.
6. Compare:
   - `S_1`
   - `S_2`
   - matched direct no-CA baselines on the same `2 x W_1` and `2 x W_2` geometries
   - same grammar-size and state-count caps

## Success Signal

H1 survives only if at least one family shows:

- legal exact extraction at both levels,
- `S_2 < S_1`,
- and a matched-baseline advantage that is not explained by boundary programming or bounded-slope collapse.

## Immediate Kill Conditions

- interface composition requires any global patch,
- `S_2 >= S_1`,
- the family is only strong because of `R/T` boundary programming,
- the extracted family stays bounded-slope or low-rational-complexity after scale-up.
