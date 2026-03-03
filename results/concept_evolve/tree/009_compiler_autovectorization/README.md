# Concept: compiler_autovectorization

- Topic Context: Branchless Binary GCD
- Domains: compiler optimization, code generation, ISA extensions
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Study how GCC/Clang handle branchless GCD patterns. Identify when compiler reintroduces branches or defeats CMOV usage.

## Mathematical Formalization
Compiler may transform ternary to CMOV only with specific flag patterns. Risk: CMOV for swap but JCC for loop exit.

## Implementation Hypothesis
Use __builtin_ctzll, explicit ternary for CMOV generation, or inline asm for guaranteed branchless code.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
