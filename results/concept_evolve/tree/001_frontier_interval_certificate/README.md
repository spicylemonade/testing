# frontier_interval_certificate

## Context
A long first-row gap means the entire interval between successive row leaders is already covered by the current product frontier P_n = R_n C_n. This card proposes importing covering-system style interval certificates to show that such full coverage forces a rigid witness pattern that may be uniformly bounded.

## Mathematical Sketch
Let R_n={r_1,...,r_n}, C_n={c_1,...,c_n}, P_n={r_i c_j : i,j\le n}. If g_n=r_{n+1}-r_n, then [r_n+1, r_n+g_n-1] \subseteq P_n. Seek L such that any interval I of length > L cannot admit witness sets W(x)={(r,c)\in R_n\times C_n: rc=x} for every x\in I without violating an uncovered-set density bound.

## Why This Bridge Might Matter
The new step is to treat consecutive covered integers in T as an endogenous covering system whose moduli and residues come from divisor witnesses, rather than from an externally prescribed congruence family.

## Implementation Backlog
- notes/interval_certificate.md
- experiments/record_gap_witness_scan.py
- data/record_gap_certificates.json

## Starting Experiment
Compute record gaps up to at least n=10^4, extract minimal witness families for each interior integer in those intervals, and cluster the certificates by overlap graph. A stable finite motif library would be strong evidence for a bounded-gap proof path.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- Row 1 of prime separator array A129258. (oeis:A129259)
- Solution of the minimum modulus problem for covering systems (openalex:W2165692739)
- On the Erdős covering problem: the density of the uncovered set (openalex:W3211924274)
- Anti-recurrence sequences (openalex:W4415108737)
