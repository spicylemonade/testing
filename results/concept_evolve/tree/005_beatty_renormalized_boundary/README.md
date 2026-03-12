# beatty_renormalized_boundary

## Context
A coarser explanation may exist even if T is not exactly automatic: the row and column leaders could shadow complementary Beatty pairs with bounded local noise. In that regime, bounded first differences become a renormalized Beatty discrepancy problem rather than a purely multiplicative one.

## Mathematical Sketch
Fit r_n = \lfloor \alpha n + u_n \rfloor and c_n = \lfloor \beta n + v_n \rfloor with \alpha \approx \beta and sublinear or bounded-block errors u_n,v_n. Test whether d_n \in D for a small set D and whether u_n,v_n correlate with Ostrowski/Fibonacci numeration classes.

## Why This Bridge Might Matter
The novelty is the renormalization: T is not claimed to be Beatty, only to admit a Beatty-like coarse envelope whose local noise carries the hard arithmetic information.

## Implementation Backlog
- analysis/beatty_fit.py
- data/ostrowski_labels.json
- notes/renormalized_boundary.md

## Starting Experiment
Fit alpha and beta from n<=6000, compute deviation histograms on multiple scales, and test whether record-gap times cluster in specific numeration classes.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- Restrictions of m-Wythoff Nim and p-complementary Beatty sequences (openalex:W2155926991)
- Decomposition of Beatty and Complementary Sequences (openalex:W4378474395)
- Beatty Sequences for a Quadratic Irrational: Decidability and Applications (openalex:W4391833421)
