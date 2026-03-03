# Concept: lehmer_hybrid_256bit

- Topic Context: Branchless Binary GCD
- Domains: multi-precision arithmetic, matrix-based reduction, GMP internals
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
For 256-bit: extract top 64 bits, compute cofactors via fast 64-bit half-GCD, apply transformation matrix to reduce full-width operands.

## Mathematical Formalization
Extract top 64 bits. Compute 2x2 cofactor matrix from 64-bit half-GCD. Apply: a'=u00*a+u01*b; b'=u10*a+u11*b.

## Implementation Hypothesis
For 256-bit: extract top limb, run branchless 64-bit GCD for cofactors, multiply 4-limb numbers by 2x2 matrix. Repeat.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
