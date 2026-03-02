# Constraint Solver Report

## Approach
CSP-based search using pre-computed valid residue classes for moduli
16, 9, 5, 7, 11, 13. Only triples in the intersection of valid
residue classes are examined. First face diagonal (a,b) is checked
before iterating over c.

## Residue Class Filtering
The combined modular sieve dramatically reduces the search space:
- Total candidates: 15,433,491
- total: 15,433,491
- passed_mod16: 6,175,022
- passed_all_modular: 515,122
- euler_bricks: 37

## Results
- Search bound: 5,000
- Euler bricks found: 37
- Perfect cuboids found: 0
- Wall clock time: 9.35s
- Throughput: 1,650,940 candidates/sec

## Comparison with Baseline
The constraint solver approach reduces the number of arithmetic
operations by pre-filtering with modular residue classes, but the
overhead of residue lookups means the raw throughput may not exceed
the optimized baseline for small search bounds. The advantage grows
with larger bounds where the filtering ratio increases.
