# Witness Spec

## Purpose

This file specifies the canonical six-line witness format described in the problem statement, together with legality checks and exact score accounting. It is written so that a future exact evaluator can be implemented without guessing any silent conventions.

## Six-Line Format

1. Human-readable score line
   - Format: a fraction plus the tuple `(m(G), |R|, n(G), |T|)`.
   - This line is advisory only and is not the source of truth.
2. `X`
   - A finite list of integer pairs.
   - Must contain `(0,0)`.
3. `d_1, ..., d_k`
   - A list of positive integers describing the product grid.
4. `f_1, ..., f_k`
   - A list of `k` partial dictionaries.
   - `f_i` maps tuples in `d_1 x ... x d_{i-1} x (d_i - 1)` to labels in `X`.
   - Omitted keys mean `(0,0)`.
5. `T`
   - A list of vertices of the grid `d_1 x ... x d_k`.
6. `R`
   - A list of partial dictionaries from vertices to labels in `X`.
   - Each element of `R` must have exactly one nonzero supported vertex in the initial witness.

## Product-Grid Semantics

Given `d = [d_1, ..., d_k]`, the vertex set is

`V = { [e_1, ..., e_k] : 1 <= e_i <= d_i for all i }`.

For each `i`, the dictionary `f_i` defines edges between the vertices with prefixes

- `[a_1, ..., a_i, *, ..., *]`
- `[a_1, ..., a_i + 1, *, ..., *]`

when `f_i(a_1, ..., a_i)` is nonzero. The total edge count is

`m(G) = sum_i sum_e 1_{f_i(e) != (0,0)} d_{i+1} ... d_k`.

The vertex count is

`n(G) = d_1 ... d_k`.

## Legality Constraints

### `X`

- `(0,0)` must be present.
- Every nonzero label `(a,b)` must satisfy `a + b != 0`.
- All labels used anywhere in `f_i` or `R` must belong to `X`.

### `G = (d, f_1, ..., f_k)`

- `k >= 1`.
- Each `d_i` must be a positive integer.
- There must be exactly `k` dictionaries in line 4.
- Every key in `f_i` must have length `i`.
- Every key component must lie in the proper range:
  - `1 <= a_j <= d_j` for `j < i`
  - `1 <= a_i <= d_i - 1`
- Omitted entries are interpreted as `(0,0)`, not as missing data.

### `T`

- Every vertex in `T` must lie in `V`.
- Future evaluators should deduplicate repeated vertices before computing `|T|`.

### `R`

- Each element of `R` is a partial dictionary from vertices to labels in `X`.
- In the initial witness, each element of `R` must have exactly one supported vertex with a nonzero label.
- The supported label must belong to `X`.
- Future evaluators should reject any initial `R` element that already has two or more nonzero supported vertices.

## Forcing Semantics

An exact evaluator should treat `(R,T)` as forcing if repeated use of the following operations reaches `T = V`:

1. Edge relation insertion:
   - for any edge induced by some nonzero `f_i(prefix) = x`, add the two-support function taking one endpoint to `x` and the adjacent endpoint to `-x`.
2. Singleton certification:
   - if some function equals `(a,-a)` on one vertex `e` with `a != 0` and is zero outside `T U {e}`, then add `e` to `T`.
3. Closure under subtraction:
   - if `f, g in R`, then `f - g` may be added.

## Exact Score

The score is

`S(X,G,R,T) = (m(G) + |R|) / (n(G) - |T|)`.

The denominator must be strictly positive for a legal certificate of this form.

## Worked Validation Checks

### Check 1: illegal nonzero label in `X`

- Input:
  - `X = [(0,0), (2,-2)]`
- Failure:
  - `(2,-2)` has coordinate sum `0`, so line 2 is illegal.

### Check 2: malformed `f_i` key shape

- Input:
  - `d = [3,4]`
  - `f_1` contains key `[2,1]`
- Failure:
  - keys of `f_1` must have length `1`, not `2`.

### Check 3: out-of-range edge prefix

- Input:
  - `d = [3,4]`
  - `f_2` contains key `[3,4]`
- Failure:
  - the second coordinate of an `f_2` key must lie in `1..d_2-1 = 1..3`, so `[3,4]` is illegal.

### Check 4: invalid initial `R` support

- Input:
  - one `R` entry maps `[1,1] -> (1,0)` and `[1,2] -> (0,1)`
- Failure:
  - an initial `R` element must have exactly one nonzero supported vertex.

### Check 5: invalid `T` vertex

- Input:
  - `d = [2,2,2]`
  - `T` contains `[1,3,1]`
- Failure:
  - the second coordinate is outside `1..2`.

### Check 6: exact score accounting

- Input:
  - `d = [2,3]`, so `n(G) = 6`
  - `f_1` has one nonzero entry and contributes `d_2 = 3` edges
  - `f_2` has two nonzero entries and contributes `2` edges
  - `|R| = 4`
  - `|T| = 1`
- Result:
  - `m(G) = 3 + 2 = 5`
  - `S = (5 + 4) / (6 - 1) = 9/5`

## Evaluator Guidance

- Do not trust the human-readable first line.
- Compute `m(G)`, `n(G)`, `|R|`, and `|T|` from lines 2-6.
- Reject illegal labels, malformed keys, out-of-range vertices, or malformed initial `R`.
- Only after legality checks should the forcing closure and score be evaluated.
