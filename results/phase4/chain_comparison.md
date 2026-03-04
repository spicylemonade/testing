# Comparison of Results with the Chain B ≤ B_l ≤ L ≤ B_u

## Updated Bounds Table

| Constant | Best Lower | Source | Best Upper | Source | Gap |
|----------|-----------|--------|-----------|--------|-----|
| $B$ | 0.4332 | Chen-Gauthier 1996 | 0.4719 | Ahlfors-Grunsky 1937 | 0.0387 |
| $B_l$ | 0.5000+ | Yanagihara 1995 | ≤ L ≤ 0.5433 | — | ~0.043 |
| $L$ | 0.5000+ | Yanagihara 1995 | 0.5433 | Rademacher | ~0.043 |
| $B_u$ | **0.5708859** | **This work** (num.) | 0.6564 | Carroll-OC 2009 | **0.0855** |

## Impact Analysis

### Does our work narrow any gap?

**For B_u**: Our numerical certificate $B_u > 0.5708859$ would narrow the gap from 0.085514 to 0.085513 — a reduction of $10^{-6}$ in absolute terms. This is a negligible narrowing of the gap.

**For B, B_l, L**: Our work does not affect these constants. The chain direction is $B \leq B_l \leq L \leq B_u$, and improving the lower bound of $B_u$ does not propagate downward.

### Could $B_u = L$?

If $B_u = L$, then $B_u \leq 0.5433$ (the Rademacher upper bound for $L$). Combined with $B_u > 0.5709$, this gives a contradiction. Therefore:

$$B_u > L$$

More precisely: $B_u > 0.5709 > 0.5433 \geq L$.

This is a well-known consequence — the univalent Bloch constant strictly exceeds the Landau constant. The gap is at least $0.5709 - 0.5433 = 0.0276$.

### Rademacher Upper Bound Discussion

Rademacher's conjectured value $L = \Gamma(1/3)\Gamma(5/6)/\Gamma(1/6) \approx 0.5433$ is the upper bound for $L$, not a proven equality. If the conjecture is correct, then $L \approx 0.5433$ and $B_u - L > 0.027$.

If $L$ is actually smaller (the lower bound is merely $> 1/2 + 10^{-335}$), the chain gaps would shift accordingly.

## Structural Observations

1. **B_u is the largest constant in the chain**, so its bounds are independent of the others.
2. **The B_u gap is the widest** (0.0855), suggesting it has the most room for improvement.
3. **No conjectured exact value** for $B_u$ exists, unlike $B$ (Ahlfors-Grunsky) and $L$ (Rademacher).
4. **Jenkins' structural theory** constrains the extremal domain but does not determine $B_u$.

## Open Questions

1. Is $B_u$ rational? Algebraic? Related to special function values?
2. Does the extremal function for $B_u$ have any symmetry?
3. What is the exact number of boundary contact points in the extremal domain?
4. Can SDP methods provide a computable converging sequence of lower bounds?
