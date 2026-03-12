# complementary_linearization

## Context
The border sequences are chosen by two consecutive mex operations before the multiplicative interior is updated, so there is a natural complementary-sequence skeleton underneath the full process. This card isolates that skeleton and treats the interior products as a perturbative correction term.

## Mathematical Sketch
Let m_n(1)<m_n(2)<\cdots be the missing values of P_n. Then (r_{n+1}, c_{n+1})=(m_n(1), m_n(2)). Seek coarse recurrences r_{n+1}=F(r_{\le n},c_{\le n})+\Delta^R_n and c_{n+1}=G(r_{\le n},c_{\le n})+\Delta^C_n where F,G are complementary-sequence laws and \Delta captures multiplicative corrections.

## Why This Bridge Might Matter
The new proposal is to separate the pairwise mex skeleton from the multiplicative interior and study the latter as a correction process rather than as the whole recurrence.

## Implementation Backlog
- analysis/complementary_backbone_fit.py
- data/correction_terms.json
- notes/paired_mex_skeleton.md

## Starting Experiment
Infer low-order state machines for (r_n,c_n) and their correction terms on n<=3000, then evaluate predictive stability on the next 3000 steps.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- Row 1 of prime separator array A129258. (oeis:A129259)
- Linear Complementary Equations and Systems (openalex:W4402770752)
- Anti-recurrence sequences (openalex:W4415108737)
- Decomposition of Beatty and Complementary Sequences (openalex:W4378474395)
