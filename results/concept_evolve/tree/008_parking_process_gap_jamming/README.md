# parking_process_gap_jamming

## Context
Uncovered integers near the frontier can be treated phenomenologically as vacancies in a one-dimensional exclusion process. The mex rule always repairs the leftmost vacancy, so bounded differences would correspond to a jammed regime with uniformly short vacancy clusters.

## Mathematical Sketch
Let H_n(x)=1[x\notin P_n]. Study the run-length distribution of H_n on [1, r_n+W] for moving windows W and compare its cluster statistics to parking/RSA observables such as mean gap, skewness, kurtosis, and nearest-gap correlations.

## Why This Bridge Might Matter
The new bridge is to use jamming phenomenology as a diagnostic layer for a deterministic arithmetic process, focusing on cluster statistics rather than exact law equivalence.

## Implementation Backlog
- experiments/frontier_cluster_stats.py
- data/uncovered_cluster_moments.csv
- notes/jamming_heuristic.md

## Starting Experiment
Track uncovered-run histograms and higher moments across logarithmically spaced n, then compare with Page-Rényi and RSA reference values.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- The Page-Rényi Parking Process (openalex:W2200158250)
- Gap-size distribution functions of a random sequential adsorption model of segments on a line (openalex:W2064912741)
- The differential equation method for random graph processes and greedy algorithms (openalex:W5090298)
