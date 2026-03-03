# Concept: linux_kernel_gcd_evolution

- Topic Context: Branchless Binary GCD
- Domains: Linux kernel, systems programming, code archaeology
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Linux kernel gcd.c evolution from naive Euclidean to Zhaoxiu Zeng's binary GCD with __ffs. Lessons from kernel optimization practices.

## Mathematical Formalization
Kernel: factor shared 2s, then iterate: if(a>b) swap; b-=a; b>>=__ffs(b). Has data-dependent swap branch.

## Implementation Hypothesis
Kernel prioritizes portability. Our version targets specific ISA (BMI2, AVX) for maximum throughput.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
