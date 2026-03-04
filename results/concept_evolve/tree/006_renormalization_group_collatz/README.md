# 006 — Renormalization Group Collatz

## Concept

Imports renormalization group (RG) ideas from statistical physics to study Collatz dynamics. The key operation is coarse-graining: instead of tracking individual integers, we study the Collatz map's action on residue classes modulo 2^k. As k increases, finer structure emerges in a hierarchical, self-similar fashion — analogous to how block-spin transformations in the Ising model reveal critical behavior across scales.

The k-step renormalized map is:

```
T_k : Z/(2^k Z) -> Z/(2^k Z)
```

Fixed points of T_k correspond to residue classes whose Collatz trajectories exhibit self-similar structure. High-delay residue classes at level k refine into a predictable subset of classes at level k+1, forming a renormalization tree.

## Cross-Domain Connections

| Source Domain | Analogy | Mapping |
|---|---|---|
| Statistical physics | Kadanoff block spin transformation | Residue classes mod 2^k ~ block spins at scale k; iteration ~ RG flow |
| Signal processing | Wavelet multiresolution analysis | Successive refinement mod 2^k ~ wavelet decomposition at increasing resolution |
| Data science | Hierarchical clustering | Renormalization tree of residue classes ~ dendrogram of clustered delay behaviors |

The RG perspective suggests that if Collatz dynamics has a "critical point" (analogous to a phase transition), it would manifest as power-law scaling of average delay with residue class granularity k. Deviations from scaling would indicate the presence of relevant perturbations — specific residue classes that dominate delay records.

## Implementation Backlog

1. **Residue class iterator** — For each k in 1..20, enumerate all 2^k residue classes and compute the Collatz map restricted to Z/(2^k Z).
2. **Average delay computation** — Sample integers in each residue class (up to 2^30) and compute average total stopping time per class.
3. **Renormalization tree construction** — Build the tree relating residue classes across levels k and k+1; identify branches with anomalously high average delay.
4. **Scaling analysis** — Fit power-law and logarithmic models to delay vs. k for the dominant branches; test for scale invariance.
5. **Candidate prediction** — Use the highest-delay branches at k=16..20 to predict specific residue classes likely to contain the next delay record.

## References

- Wilson, K.G. (1971). "Renormalization Group and Critical Phenomena." *Physical Review B*, 4(9), 3174–3183.
- Lagarias, J.C. (1985). "The 3x+1 problem and its generalizations." *American Mathematical Monthly*, 92(1), 3–23.
- Kontorovich, A.V. & Lagarias, J.C. (2010). "Self-similarity in the Collatz conjecture." *Journal of Number Theory*.
