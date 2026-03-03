# Concept: simd_batch_gcd

- Topic Context: Branchless Binary GCD
- Domains: SIMD programming, data-parallel algorithms, AVX-512
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Process multiple independent GCD pairs simultaneously using AVX2/AVX-512. Main challenge: TZCNT has no SIMD equivalent - must emulate via bit isolation and LZCNT.

## Mathematical Formalization
For 4 pairs in AVX2: 4x SUB, 4x blend (replaces CMOV), 4x NEG+blend (abs), 4x emulated TZCNT, 4x variable shift.

## Implementation Hypothesis
Emulate TZCNT: t = v & (-v) isolates lowest bit; use VPLZCNTD or VPSHUFB nibble lookup for bit position.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
