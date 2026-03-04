# Citation Cross-Reference Check

## 1. Summary

| Metric | Value |
|--------|-------|
| Total BibTeX entries in `sources.bib` | 30 |
| Unique citation keys referenced in `.md` files | 22 |
| Orphan citations (in `.md` but not in `.bib`) | **0** |
| Unused bib entries (in `.bib` but never cited) | **8** |
| Citation pattern used | `\cite{...}` (LaTeX style) |

## 2. All BibTeX Keys in sources.bib

1. `skinner2009` — Skinner (2009), lower bound $B_u > 0.5708858$
2. `yanagihara1995` — Yanagihara (1995), lower bound for $B_l$ and $L$
3. `bhowmiksen2023` — Bhowmik-Sen (2023), meromorphic Bloch/Landau constants
4. `carrollortegacerda2009` — Carroll-Ortega-Cerdà (2009), upper bound $B_u \leq 0.6564$
5. `bellerhummel1985` — Beller-Hummel (1985), Bloch constant for planar domains
6. `chenshiba2004` — Chen-Shiba (2004), locally univalent Bloch constant
7. `goodman1945` — Goodman (1945), original slit domain construction
8. `robinson1935` — Robinson (1935), early lower bound for $B_u$
9. `landau1929` — Landau (1929), formalization of Bloch's theorem
10. `ahlforsgrunsky1937` — Ahlfors-Grunsky (1937), conjectured exact value of $B$
11. `fedorov1985` — Fedorov (1985), Polya-Chebotarev solution
12. `bonk1990` — Bonk (1990), improved Bloch constant lower bound
13. `baernsteinvinson1998` — Baernstein-Vinson (1998), local minimality of hexagonal lattice
14. `minda1986` — Minda (1986), hyperbolic metric in geometric function theory
15. `jenkins1992` — Jenkins (1992), extremal domain characterization
16. `jenkins1998` — Jenkins (1998), variational methods
17. `carroll2008` — Carroll (2008), structural constraints on extremal domains
18. `chengauthier1996` — Chen-Gauthier (1996), $B > 0.4332$
19. `reich1956` — Reich (1956), Bloch-Landau constant
20. `toppila1969` — Toppila (1969), early lower bound
21. `yamada1986` — Yamada (1986), branch point variation
22. `bishop2007` — Bishop (2007), conformal welding techniques
23. `banuelos1994` — Bañuelos (1994), Brownian motion and inradius
24. `bonkeremenko2000` — Bonk-Eremenko (2000), covering theorems
25. `kudryavtsevasolodov2022` — Kudryavtseva-Solodov (2022), sharp invertibility domains
26. `hamada2024` — Hamada et al. (2024), Bloch in infinite dimensions
27. `hamada2019` — Hamada (2019), distortion theorem for $\mathbb{C}^N$
28. `betsakos1999` — Betsakos (1999), bounded univalent functions
29. `colonna1991` — Colonna (1991), Bloch constant for bounded functions
30. `grahamhamadakohr2020` — Graham-Hamada-Kohr (2020), Loewner chains and Bloch

## 3. Citations Found in Markdown Files

### Frequently cited (5+ occurrences):
- `skinner2009` — 10 occurrences across 6 files
- `carrollortegacerda2009` — 8 occurrences across 6 files
- `jenkins1992` — 8 occurrences across 6 files
- `carroll2008` — 7 occurrences across 5 files

### Moderately cited (2-4 occurrences):
- `bhowmiksen2023` — 4 occurrences
- `landau1929` — 4 occurrences
- `bonk1990` — 5 occurrences
- `chengauthier1996` — 4 occurrences
- `jenkins1998` — 3 occurrences
- `baernsteinvinson1998` — 3 occurrences
- `yanagihara1995` — 3 occurrences
- `banuelos1994` — 3 occurrences
- `minda1986` — 2 occurrences

### Cited once:
- `robinson1935`, `goodman1945`, `toppila1969`, `bellerhummel1985`
- `ahlforsgrunsky1937`, `fedorov1985`, `bishop2007`
- `chenshiba2004`, `bonkeremenko2000`

## 4. Unused Bibliography Entries

The following 8 entries in `sources.bib` are never cited in any `.md` file:

| Key | Reason for inclusion | Should keep? |
|-----|---------------------|-------------|
| `reich1956` | Historical reference on Bloch-Landau constant | Yes (completeness) |
| `yamada1986` | Branch point variation technique | Yes (future work) |
| `kudryavtsevasolodov2022` | Sharp invertibility domains | Yes (identified in probe) |
| `hamada2024` | Recent work on Bloch in infinite dimensions | Yes (literature coverage) |
| `hamada2019` | Distortion theorem for $\mathbb{C}^N$ | Yes (literature coverage) |
| `betsakos1999` | Bounded univalent functions | Yes (context) |
| `colonna1991` | Bloch constant for bounded functions | Yes (context) |
| `grahamhamadakohr2020` | Loewner chains and Bloch mappings | Yes (recent work) |

**Assessment**: All 8 unused entries were collected during the Phase 1 literature search and are relevant to the broader context. They represent papers consulted but not directly cited in the mathematical arguments. This is normal for a research bibliography — one reads more papers than one cites.

## 5. Orphan Citation Check

**Result: PASS** — Every `\cite{key}` appearing in any `.md` file under `results/` has a corresponding entry in `sources.bib`. Zero orphan citations.

## 6. Overall Assessment

- **Bib completeness**: 30 entries, well above the 20-entry minimum
- **Coverage**: All required papers (per item_003 acceptance criteria) are present
- **Consistency**: All citations resolve correctly
- **Unused entries**: 8 entries are referenced in `sources.bib` but not cited; all are justified as contextual references

**Overall**: PASS (with the note that 8 entries are uncited but intentionally retained for completeness).
