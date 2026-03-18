# Novelty Citation Note

## Support Map For The Named-Paper Comparisons

### 1. Cellular Automata Applications in Shortest Path Problem (2017)

- BibTeX support:
  - `tsompanas2017` in `sources.bib`
- Repo-artifact support:
  - `results/problem_statement.md`
  - `results/branches/H1_defect_syndrome_ca_64m.md`
  - `results/branches/H1_precheck.md`
  - `results/verification/novelty_precheck.md`
  - `results/literature/prior_art_gap.md`

### 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)

- BibTeX support:
  - `ghaleb2019` in `sources.bib`
- Repo-artifact support:
  - `results/literature/literature_snapshot.json`
  - `results/problem_statement.md`
  - `results/verification/novelty_precheck.md`
  - `results/literature/prior_art_gap.md`

### 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)

- BibTeX support:
  - `ghaemi2022` in `sources.bib`
- Repo-artifact support:
  - `results/literature/literature_snapshot.json`
  - `results/verification/novelty_precheck.md`
  - `results/literature/prior_art_gap.md`

### 4. Engineering Societies in the Agents World (2000)

- BibTeX support:
  - `leeuwen2000` in `sources.bib`
- Repo-artifact support:
  - `results/literature/literature_snapshot.json`
  - `results/branches/H3_gate.md`
  - `results/verification/novelty_precheck.md`
  - `results/literature/prior_art_gap.md`

### 5. A 64-Modular Hadamard Matrix of Order 668 (2025)

- BibTeX support:
  - `eliahou2025_64mod668` in `sources.bib`
- Repo-artifact support:
  - `results/problem_statement.md`
  - `results/frontier/order_668_64m/seed_manifest.json`
  - `results/branches/H1_defect_syndrome_ca_64m.md`
  - `results/branches/H1_precheck.md`
  - `results/concept_evolve/probe_result.json`
  - `results/verification/novelty_precheck.md`
  - `results/literature/prior_art_gap.md`

## Unsupported Or Weak Wording To Avoid

- Do not say cellular automata are new for Hadamard matrices in general.
- Do not say automata are untried here.
- Do not say H1 is already a distinct CA repair method; the current evidence only supports a narrow, still-testable hypothesis.
- Do not call H2 novel before the family-leakage audit is passed.
- Do not call H3 a live order-668 solver branch before the reserve gate opens and the direct CA-construction overlap check is cleared.

## Bibliography Quality Flags

- `tsompanas2017`
  - The current entry mixes `journal={arXiv.org}` with a Springer DOI. If this paper is cited directly in the writeup, replace it with the actual conference-chapter or proceedings metadata.
- `ghaleb2019`
  - The DOI is plausible, but the entry would be stronger with booktitle / pages / editors if it is cited directly.
- `leeuwen2000`
  - The current DOI appears to be for the LNCS volume rather than a chapter-level reference. If used directly, strengthen the metadata.
- `eliahou2025_64mod668`
  - Strong enough for the current run and should remain the primary frontier anchor.

## Important Source To Add Before Any H3 Expansion

- Add at least one direct CA-construction source touching Hadamard-adjacent objects, such as a linear bipermutive CA / orthogonal-array / bent-function pipeline paper, before any substantial H3 build-out.
  - Right now H3 overlap warnings are conceptually correct, but `sources.bib` does not yet contain a strong direct CA-construction citation to anchor that comparison.
