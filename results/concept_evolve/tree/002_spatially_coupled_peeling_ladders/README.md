# Spatially Coupled Peeling Ladders

View forcing propagation as a peeling wave on a Tanner-like graph whose variable nodes are witness vertices and whose check nodes are local certificate templates. Then use spatial coupling across recursive layers so a tiny boundary seed launches a long exact-certificate wave with lower cost density than uncoupled repetition.

## Context
Let H=(V,C,E) with variable nodes V and local certificate checks C. Define T_{t+1}=T_t \cup \{v\in V\setminus T_t : \exists c\in C,\ \mathrm{supp}(c)\subseteq T_t\cup\{v\},\ c(v)=(a,-a)\}. Partition V=\bigsqcup_i V_i with coupling window w and search for geometries where activation of V_i forces activation of V_{i+1} while minimizing S=(m+r)/(n-t).

## Implementation Backlog
- Prototype the bridge: Start from a small verified gadget, chain copies into d_1 x d_2 x d_3 ladders with sparse inter-slab edges, estimate wave viability by density-evolution style simulation, and exact-verify only geometries whose wave front survives.
- Run the seed test: Use 6-10 coupled slabs built from one tiny verified gadget, sweep coupling width and boundary seeds, and compare exact score against uncoupled repeats at matched edge density.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Threshold Saturation via Spatial Coupling: Why Convolutional LDPC Ensembles Perform So Well over the BEC (10.1109/TIT.2010.2095072)
- The effect of spatial coupling on compressive sensing (10.1109/ALLERTON.2010.5706927)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

## Novelty Delta
The novelty is importing spatial coupling specifically to engineer exact arithmetic-certificate propagation, not parity-check decoding or sparse recovery.

## Why It Is Distinct
The checks are signed arithmetic singleton certificates rather than parity constraints, and the objective is witness score density instead of communication threshold.
