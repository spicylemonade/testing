# 004: Fitness Landscape of Collatz Delay

## Overview

Sewall Wright's (1932) concept of a fitness landscape provides a powerful metaphor for understanding the distribution of Collatz delay records. By defining "fitness" as the total stopping time D(n), the positive integers become a landscape with peaks (delay records), valleys (numbers with unusually low delay), and ridges (families of related high-delay numbers).

## Key Observations

- Delay records come in "families" sharing nearly identical residues (Roosendaal)
- About 7-8 records per decade of n, implying average gap ratio ~1.36
- The landscape is highly rugged: local optima are abundant but global records are rare
- Residue families suggest the landscape has "ridgelines" in the space of binary representations

## Biological Parallels

- **Adaptive walks**: Starting from any integer and performing greedy ascent (always moving to the neighbor with highest delay) typically gets stuck at a local optimum, not a global delay record
- **NK model ruggedness**: The "K" parameter is the number of binary digits that interact non-locally through the 3x+1 map. This is effectively infinite, making the landscape maximally rugged
- **Neutral networks**: Many consecutive integers have the same delay class, forming "neutral plateaus" in the landscape

## Implementation Backlog

1. [ ] Compute D(n) for n in [1, 10^7] and visualize as landscape
2. [ ] Implement genetic algorithm with bit-flip mutations
3. [ ] Compare GA convergence to exhaustive enumeration
4. [ ] Characterize peak shapes around known delay records
5. [ ] Compute ruggedness statistics (autocorrelation of D along n)
6. [ ] Identify neutral networks (connected components of equal delay)
