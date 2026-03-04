# Final Literature Check: 2024-2026

## 1. Search Methodology

Searches conducted via:
- Web search for "univalent Bloch constant" 2024-2026
- Web search for "Bloch constant" new bounds 2024-2026
- Web search for "Landau constant" improved 2024-2026
- Semantic Scholar search for Bloch-Landau constant bounds
- ArXiv search for recent preprints
- MathOverflow and Wikipedia checks for community updates

## 2. Papers Found (2024-2026)

### A. Papers Closest to Classical Bloch/Landau Constants

| Title | Authors | Year | Venue | Relevance to $B_u$ |
|-------|---------|------|-------|---------------------|
| Bieberbach conjecture, Bohr radius, Bloch constant in infinite dimensions | Hamada, Kohr, Kohr | 2024 | arXiv:2409.04028 | Studies Bloch constant for mappings on unit balls of Banach spaces. Does **not** improve classical one-variable bounds. |
| Sharp univalent covering domain for holomorphic self-maps with fixed points | Kudryavtseva, Solodov | 2024 | Sbornik: Mathematics 215(2) | Sharp covering domains for specific classes. Related to Landau-type problems but does **not** improve $L$ or $B_u$. |
| Inverse function theorem on holomorphic self-maps with two fixed points | Kudryavtseva, Solodov | 2022 | Russian Math. Surveys 77(1) | Discusses Landau's approach to Bloch constant. Does **not** produce new numerical bounds. |
| Iterates of holomorphic maps, fixed points, and domains of univalence | Goryainov, Kudryavtseva, Solodov | 2023 | Russian Math. Surveys 77(6) | Survey referencing Bloch constant without improving it. |

### B. Papers on Bloch/Landau for Generalized Function Classes

| Title | Authors | Year | Venue | Notes |
|-------|---------|------|-------|-------|
| Improved Bloch and Landau constants for meromorphic functions | Bhowmik, Sen | 2023 | Canad. Math. Bull. 66(4) | Meromorphic functions only |
| Bounds for meromorphic Bloch-type functions | Bhowmik, Sen | 2024 | Czech. Math. J. 74(2) | Meromorphic, not classical |
| Landau-type Theorem for elliptic harmonic mappings | Bhowmik, Sen | 2024 | arXiv:2404.04596 | Elliptic harmonic class |
| Bloch-Landau type theorems for holomorphic/pluriharmonic mappings in $\mathbb{C}^n$ | Allu, Kumar | 2024 | arXiv:2308.15913v4 | Higher-dimensional |
| Landau-Type Theorems for Poly-Analytic Functions | Allu, Kumar | 2024 | arXiv:2409.08029 | Poly-analytic class |
| Landau-type theorems for bounded poly-analytic functions | Allu, Biswas, Mandal, Yanagihara | 2025 | arXiv:2508.17020 | Poly-analytic class |
| Landau-type theorems for logharmonic Laplacian functions | (various) | 2025 | arXiv:2502.08390 | Logharmonic class |
| Bohr phenomenon for harmonic Bloch functions | Allu, Halder | 2025 | Analysis Math. 51 | Bohr-type, not about $B$ |
| Composition operators in pluriharmonic Bloch spaces | Huang, Das, Rasila | 2025 | arXiv:2504.07581 | Operator theory, not constant |
| Weighted sum of squares of coefficients of Bloch functions | Khasianov | 2026 | Anal. Math. Phys. 16(1) | Coefficient estimates |
| Bloch constant estimate for harmonic mappings under differential operator | Chen, Liu | 2024 | Acta Math. Sci. | Harmonic mappings |

### C. Reference Works Updated

| Source | Status |
|--------|--------|
| Finch, *Mathematical Constants* errata (2024 update) | No changes to Bloch/Landau sections |
| Wikipedia: *Bloch's theorem (complex analysis)* (Feb 2026) | Bounds unchanged |
| MathOverflow: Bloch constant status | Eremenko's 2012 answer remains definitive; no new updates |

## 3. Key Finding

**No paper from 2024-2026 improves the known bounds on any of the four classical constants:**

| Constant | Best Lower | Best Upper | Status (2024-2026) |
|----------|-----------|-----------|---------------------|
| $B$ (Bloch) | $\geq 0.4332$ (Chen-Gauthier 1996) | $\leq 0.4719$ (Ahlfors-Grunsky conj.) | **Unchanged** |
| $B_l$ (locally univ. Bloch) | Known | Known | **Unchanged** |
| $L$ (Landau) | $> 0.5$ (Yanagihara 1995) | $\leq 0.5433$ (Rademacher conj.) | **Unchanged** |
| $B_u$ (univ. Bloch) | $> 0.5708858$ (Skinner 2009) | $\leq 0.6564$ (Carroll-OC 2009) | **Unchanged** |

All recent activity in 2024-2026 focuses on:
- Generalizations to harmonic, pluriharmonic, poly-analytic, meromorphic, or higher-dimensional settings
- Related but distinct problems (domains of univalence with fixed points, Bohr phenomena)
- Coefficient estimates and operator theory on Bloch spaces

## 4. Consistency of Our Results

Our numerical certificate $B_u > 0.5708859$ is **fully consistent** with the latest literature:

1. **No conflict**: No paper contradicts our claim
2. **Not superseded**: The best published lower bound remains Skinner's $0.5708858$ from 2009
3. **Gap confirmed**: The gap $0.5709 < B_u < 0.6564$ remains the state of the art
4. **Our contribution**: If verified rigorously, our $10^{-7}$ improvement would be the first progress on $B_u$ bounds since 2009

## 5. Notable Trends

1. **Active generalization**: The community is actively extending Bloch/Landau theory to new function classes (harmonic, poly-analytic, higher-dimensional), but the classical one-variable problem appears dormant.

2. **Kudryavtseva-Solodov program**: This group (2022-2024) is producing sharp invertibility results for specific classes of self-maps. They explicitly mention applicability to Landau's constant but have not yet produced improved numerical bounds.

3. **No SDP approach found**: Despite the natural SDP formulation via Grunsky matrices (our steering direction 1), no paper in the literature attempts this approach. This remains a genuinely unexplored avenue.

4. **17+ year stalemate**: No improvement to either bound of $B_u$ has been published since 2009.

## 6. Conclusion

Our results are state-of-the-art (modulo the non-rigorous nature of the $10^{-7}$ improvement). The classical Bloch/Landau constant problem for holomorphic functions on the disk has seen no new results in the 2024-2026 period. The field is ripe for new methods, particularly the SDP/Grunsky approach we identified.
