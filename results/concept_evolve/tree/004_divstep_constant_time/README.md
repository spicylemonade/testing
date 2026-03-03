# Concept: divstep_constant_time

- Topic Context: Branchless Binary GCD
- Domains: cryptographic algorithms, modular arithmetic, constant-time programming
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Adapt Bernstein-Yang 2019 divstep for plain GCD. Fixed iteration count (2n-1 for n-bit) with no data-dependent branches. Constant-time but more total iterations.

## Mathematical Formalization
divstep(delta,f,g): if delta>0 and g_odd: (1-delta,g,(g-f)/2); elif g_odd: (1+delta,f,(g+f)/2); else: (1+delta,f,g/2).

## Implementation Hypothesis
Fixed 127 iterations for 64-bit. Each: 2 CMOV (conditional swap) + 1 conditional add + 1 right shift. All branchless.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
