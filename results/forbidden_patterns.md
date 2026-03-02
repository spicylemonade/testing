# Forbidden Patterns in Collatz Parity Sequences

## Parameters
- N = 200000, k = 4..12

## Key Structural Constraint

The pattern '11' (consecutive odd steps) is **provably forbidden** because
3n+1 always produces an even number when n is odd. This means the next
Collatz step after an odd step is always a division by 2 (even step).

## Forbidden Pattern Counts

| k | Total Forbidden | Trivial (contain '11') | Non-trivial |
|---|----------------|----------------------|-------------|
| 4 | 8 | 8 | 0 |
| 5 | 19 | 19 | 0 |
| 6 | 43 | 43 | 0 |
| 7 | 94 | 94 | 0 |
| 8 | 201 | 201 | 0 |
| 9 | 423 | 423 | 0 |
| 10 | 880 | 880 | 0 |
| 11 | 1815 | 1815 | 0 |
| 12 | 3719 | 3719 | 0 |

## Non-trivial Forbidden Patterns

**No non-trivial forbidden patterns found** for k ≤ {max_k}.
All forbidden patterns are explained by the '11' constraint.

## Generalized Maps

- 5n+1: 43 forbidden 6-grams (43 contain '11')
- 7n+1: 43 forbidden 6-grams (43 contain '11')
