# tile_assembly_slope_bloom

## Topic context
Use seeded active tile self-assembly as a disciplined route to macrocell growth with evolving interfaces. The target is a local growth system whose extracted effective slope set or rational complexity increases with scale, escaping the bounded-slope basin flagged by recent arithmetic Kakeya work.

Primary domains: self_assembly, cellular_automata, additive_combinatorics.

Mathematical sketch:
Let each supertile carry an interface label \iota\in\mathcal{I} and an effective slope set R(\iota). Growth applies a local composition rule F so that R_{k+1}=F(R_k). Seek families with complexity c(R_k)\to\infty under scale while extracted scores S_k remain below bounded-slope controls.

Closest prior art:
- Intrinsic Universality in Seeded Active Tile Self-Assembly (arXiv:2407.11545)
- Generalized Arithmetic Kakeya (arXiv:2411.13395)
- Sum-difference exponents for boundedly many slopes, and rational complexity (arXiv:2511.15135)

Novelty claim:
The new claim is that self-assembly-style interface growth may generate scale-dependent rational complexity that remains exact-certificate compatible.

Differentiation:
This is not generic self-assembly universality and not another bounded-slope retuning. It matters only if scale growth creates genuinely new extracted slope complexity with competitive score.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
