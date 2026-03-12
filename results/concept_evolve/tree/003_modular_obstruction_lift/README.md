# modular_obstruction_lift

## Context
Modular Stanley sequences show that greedy rules can hide large-gap mechanisms behind arithmetic congruence structure. This card asks whether the T frontier admits a multiplicative analog: residue or ratio obstructions that repeatedly force long covered blocks before the next row leader appears.

## Mathematical Sketch
Search for q and residue sets A_q,B_q such that R_n \bmod q \subseteq A_q, C_n \bmod q \subseteq B_q, and the product set A_q B_q leaves a structured family of residue classes over- or under-covered. A disproof route would construct q_k with interval-supporting obstructions; a proof route would rule out persistent q-stable holes.

## Why This Bridge Might Matter
The novelty is the transfer of modular large-gap heuristics from additive greedy sets to an endogenous multiplicative frontier driven by two coupled mex operations.

## Implementation Backlog
- experiments/modulus_scan.py
- data/residue_heatmaps/
- notes/obstruction_catalog.md

## Starting Experiment
At each record gap, store occupancy vectors for R_n and C_n modulo q<=200 and run change-point tests on the most deviant moduli.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- On the growth of the counting function of Stanley sequences (openalex:W2036535490)
- Novel structures in Stanley sequences (openalex:W2115732821)
- Generalized multiplicative Sidon sets (openalex:W847854434)
- Additive and multiplicative Sidon sets (openalex:W1982898207)
