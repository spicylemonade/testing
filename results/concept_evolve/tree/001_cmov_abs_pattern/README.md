# Concept: cmov_abs_pattern

- Topic Context: Branchless Binary GCD
- Domains: x86 microarchitecture, branchless programming, GCD algorithms
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Replace conditional branches in the sign/swap step of binary GCD with a branchless absolute-value and conditional-move sequence. Uses SUB, NEG, CMOV to compute |a-b| and min(a,b) without any JCC instructions.

## Mathematical Formalization
Given a,b: diff = a - b; mask = diff >> 63 (arithmetic shift); abs_diff = (diff ^ mask) - mask; min_val = b ^ ((a ^ b) & mask)

## Implementation Hypothesis
The inner loop becomes: sub rax,rbx; cmovl rbx,rax; neg rax; cmovs rax,rbx; tzcnt rcx,rax; sarx rax,rax,rcx. Zero JCC.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
