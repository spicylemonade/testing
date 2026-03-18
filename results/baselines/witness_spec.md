# Witness Specification

This document defines the canonical six-line witness format implied by the problem statement. It is a specification document only; no exact verifier exists in the current repo snapshot.

## Six-Line Format

1. Human summary line:
   - score as a fraction,
   - plus `m(G)`, `|R|`, `n(G)`, `|T|`.
   - This line is informational and should not be trusted by the verifier without recomputation.
2. `X`:
   - a list of integer pairs.
3. `d_1, ..., d_k`:
   - the product-grid shape.
4. `f_1, ..., f_k`:
   - each `f_i` is a partial dictionary from `d_1 x ... x (d_i - 1)` to `X`;
   - omitted entries mean `(0,0)`.
5. `T`:
   - a list of product-grid vertices.
6. `R`:
   - a list of dictionaries from vertices to elements of `X`;
   - each element of `R` must have exactly one nonzero support vertex.

## Product-Grid Encoding

- Vertex set:
  - `V = d_1 x ... x d_k`
  - each vertex is a list `[e_1, ..., e_k]` with `1 <= e_i <= d_i`.
- Edge generation:
  - for each stage `i` and each key `(a_1, ..., a_i)` in `f_i`,
  - all vertices whose first `i` coordinates are `(a_1, ..., a_i)` are connected to the corresponding vertices with first `i` coordinates `(a_1, ..., a_i + 1)`,
  - each such edge carries label `f_i(a_1, ..., a_i)`.
- Edge count:
  - `m(G) = sum_i sum_e 1_{f_i(e) != (0,0)} d_{i+1} ... d_k`.
- Vertex count:
  - `n(G) = d_1 ... d_k`.

## Legality Constraints

### On `X`

- `(0,0)` must be present.
- Every nonzero `(a,b)` in `X` must satisfy `a + b != 0`.
- `X` is finite.

### On `d_1, ..., d_k`

- The challenge is meaningful only for a nonempty grid.
- A future evaluator should reject zero dimensions as malformed for this task, even though the prose says "non-negative integers", because the witness is supposed to encode a nonempty constructible graph and forcing process.

### On `f_1, ..., f_k`

- Each key of `f_i` must have length `i`.
- The first `i-1` coordinates must lie in the ranges `1..d_1`, ..., `1..d_{i-1}`.
- The last coordinate must lie in `1..(d_i - 1)`.
- Every value must lie in `X`.
- Omitted keys mean `(0,0)` and do not contribute to `m(G)`.

### On `T`

- Each element of `T` must be a vertex of `V`.
- Duplicate vertices should be rejected or deduplicated before score recomputation; the safer canonical rule is to reject duplicates.

### On `R`

- Each element of `R` is a function `V -> X` with exactly one nonzero support vertex.
- The single nonzero value must belong to `X`.
- Support size is counted by value, not by dictionary entry count. A dictionary that stores `(0,0)` at extra vertices is malformed.

## Exact Score

- `score = (m(G) + |R|) / (n(G) - |T|)`.
- The denominator must be strictly positive.
- A verifier should recompute `m(G)`, `|R|`, `n(G)`, and `|T|` from lines 2-6 and ignore the human summary line if they disagree.

## Worked Validation Checks

### Check 1: `X` legality

- Example valid `X`:
  - `[(0,0), (1,0), (2,1)]`
- Example invalid `X`:
  - `[(0,0), (1,-1)]`
- Why invalid:
  - the nonzero element `(1,-1)` satisfies `a+b=0`, which the problem forbids.

### Check 2: `f_i` key shape

- Example:
  - `d = [3,2]`
  - `f_2` keys must have length `2`, with first coordinate in `1..3` and second in `1..1`.
- Invalid entry:
  - key `[4,1]` is out of range;
  - key `[2,2]` is also out of range because `d_2 - 1 = 1`.

### Check 3: `R` single-support condition

- Example valid element of `R`:
  - `{ [1,2]: (2,0) }`
- Example invalid element of `R`:
  - `{ [1,2]: (2,0), [1,1]: (0,0) }`
- Why invalid:
  - the canonical function representation is supposed to have exactly one nonzero support vertex, not one nonzero plus explicit zero clutter.

### Check 4: score recomputation

- Example:
  - `d = [2,3]`, so `n(G)=6`.
  - one nonzero entry in `f_1`, so it contributes `d_2 = 3` edges.
  - one nonzero entry in `f_2`, so it contributes `1` edge.
  - if `|R|=2` and `|T|=1`, then score is `(4 + 2) / (6 - 1) = 6/5`.
- A future evaluator must recompute this and ignore any mismatched human summary.

### Check 5: denominator positivity

- Example:
  - if `|T| = n(G)`, then the denominator is `0`.
- Why invalid:
  - the score is undefined, so such a witness must be rejected.

### Check 6: forcing-rule precondition for certifying a vertex

- A future exact verifier must not add a vertex `e` to `T` merely because some function in the span contains `(a,-a)` at `e`.
- It must also enforce the masking condition from the problem statement:
  - all other nonzero support of that function must lie inside `T`.
- This prevents illegal "certificate leakage" where a relation certifies more than one still-unforced vertex at once.

## Non-Negotiable Evaluator Behavior

- No repair step.
- No modular relaxation.
- No permissive coercion of malformed dictionaries.
- No trust in the human summary line.
- Exact forcing must be checked over `\mathbb{Z}` with the stated closure rules.
