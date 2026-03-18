# Peer Review

## Scores

- Completeness: **5/5**. The draft contains an abstract, introduction, related work, background/preliminaries, method, experimental setup, results, discussion, conclusion, and references.
- Technical Rigor: **4/5**. The corridor compiler/verifier are formalized cleanly, proofs are explicit, and reproducibility commands are included, but the benchmark program remains narrower and more confounded than the prose sometimes suggests.
- Results Integrity: **3/5**. The core frontier, H2, ablation, and appendix certificate numbers mostly match saved artifacts, but provenance is overstated and one reported figure bar is hard-coded rather than traced through the cited ablation artifact.
- Citation Accuracy: **1/5**. Multiple external entries contain real metadata errors, one web citation is broken/outdated, and all `archivara_*` entries fail the required web-verification standard because they are local repo artifacts rather than public sources.
- Compilation: **4/5**. `research_paper.tex` compiled successfully via `pdflatex -> bibtex -> pdflatex -> pdflatex`, and `research_paper.pdf` exists, but the build still reports underfull boxes and font-substitution warnings.
- Writing Quality: **4/5**. The paper is clear, professional, and unusually honest about negative results.
- Figure Quality: **2/5**. Several figures are plain/basic slide-style schematics, one panel contains a hard-coded unsupported data bar, and some labeling/layout choices are not publication-grade.
- Novelty & Creative Contribution: **2/5**. The surviving contribution is narrow and mostly negative: a corridor-local verifier theorem, a corridor-local obstruction theorem, and a careful falsification workflow. That is real, but it is not a strong or surprising new arithmetic-Kakeya contribution.

## Major Findings

1. **Citation accuracy is below publication standard.**
   `sources.bib` contains multiple incorrect scholarly entries and many non-web-verifiable local artifact entries. Concrete external errors include `katz2001` (journal year mismatch), `green2017` (wrong volume/pages), `pohoata2024` (wrong first author name), `lemm2014` (wrong author), `bollobas2014` (wrong DOI/year/volume/pages), `hartarsky2018` (wrong page range), `leng2024` (wrong author), and `epochai2025arithmetickakeya` (broken/outdated URL and metadata). Under the stated zero-tolerance rule, the 11 `archivara_*` entries also fail because exact-title web search does not verify them as public sources.

2. **The core numerical results look mostly real, but the manuscript overstates provenance.**
   The main frontier table, H2 table, ablation table, and appendix certificate strings are largely consistent with the saved JSON artifacts. However, the paper says every quantitative claim is traced to cited saved artifacts (`research_paper.tex:487`), yet the width-8 boundary-stress `0/16` claim (`research_paper.tex:638`) is not present in `results/phase4_ablations.md` or `results/phase4_ablations.json`; it is hard-coded in `scripts/generate_paper_figures.py:619-623`. The appendix also says all figures were generated from saved local JSON artifacts (`research_paper.tex:812-814`), but `scripts/generate_paper_figures.py:142-170`, `scripts/generate_paper_figures.py:324-333`, and neighboring code show that several figures are hand-authored schematics rather than direct artifact plots.

3. **The novelty claim is too narrow for acceptance.**
   The paper is strongest when read as a negative operational benchmark inside an existing finite-certificate arithmetic-Kakeya program. The genuinely distinct pieces are limited to the width-2 corridor verifier/correctness theorem and the one-seed obstruction theorem. The larger bridge story does not survive: H1 dies before scoring, H2 adds no screening lift, and H3 never activates. This is exactly the novelty position described in `results/verification/novelty_report.md`, and it lands closer to an internally valuable falsification note than to a broadly interesting new research advance.

4. **Concept-evolution evidence does not support a stronger creativity claim.**
   `results/concept_evolve/semantic_bridge.json` contains no active bridges, and all 32 `results/concept_evolve/tree/*/concept.json` files have missing `experimental_result` fields. That strongly suggests ConceptEvolve helped narrow the route set, but did not materially produce tested, nontrivial new experimental contributions in the final paper. Under the stated rubric, that pushes the novelty score down rather than up.

5. **Figure quality is below publication standard.**
   Figures 4 and 7 are the best of the set, but Figures 1-3 read as presentation schematics more than paper figures, Figure 5 has awkward/overlapping labeling, and Figure 6 mixes real ablation counts with a hard-coded unsupported boundary-stress bar. The figure package is clean enough technically, but not strong enough stylistically or evidentially for a top-tier venue.

## Citation Verification Report

All 24 distinct in-text citation keys are present in `sources.bib`. Five bibliography entries are unused in the paper: `bourgain1999`, `epochai2025arithmetickakeya`, `katz2001`, `lemm2014`, and `leng2024`.

- `katz1999`: **Verified via web search.** DOI resolves to the Intl Press / Mathematical Research Letters article; title, journal, and year match.
- `katz2001`: **Incorrect.** DOI resolves to the Springer journal article `New Bounds for Kakeya Problems`, but the journal publication year is **2002**, not **2001**.
- `bourgain1999`: **Verified via web search.** DOI resolves to the GAFA article; title, journal, and year match.
- `green2017`: **Incorrect.** Web search verifies the paper exists, but the bibliography gives the wrong journal metadata; the Springer listing is **Periodica Mathematica Hungarica 78, 135-151**, not **79(2), 147-168**.
- `cowenbreen2020`: **Verified via web search.** The arXiv record exists; title, authors, and year match.
- `pohoata2024`: **Incorrect.** The arXiv record lists **Cosmin Pohoata**, not **Cristian Pohoata**.
- `tao2025`: **Verified via web search.** The arXiv record exists; title, author, and year match.
- `lemm2014`: **Incorrect.** DOI/arXiv verification shows the author is **Marius Lemm**, not **Morten Lemm**.
- `bond2013`: **Verified via web search.** The SIAM Journal on Discrete Mathematics article exists; DOI redirects to the correct paper and the journal/year metadata match.
- `bond2014`: **Verified via web search.** The Selecta Mathematica article exists; DOI resolves and the journal/year metadata match.
- `bond2015`: **Verified via web search.** The Journal of Algebraic Combinatorics article exists; DOI resolves and the journal/year metadata match.
- `bollobas2014`: **Incorrect.** Web search verifies the paper exists, but the bibliography gives the wrong DOI and journal metadata. The paper is listed under **Proceedings of the London Mathematical Society 126(2), 620-703 (2023), DOI 10.1112/plms.12497**, not the 2015 metadata currently in the file.
- `hartarsky2018`: **Incorrect.** The paper exists, but the bibliography gives the wrong page range; web search shows **1444-1459**, not **1449-1483**.
- `kubica2018`: **Verified via web search.** The Physical Review Letters article exists; DOI redirects to APS and the journal/year metadata match.
- `hemenway2013`: **Verified via web search.** The Information and Computation article exists; DOI resolves and the year/journal metadata match.
- `sipser1996`: **Verified via web search.** The IEEE Transactions on Information Theory article exists; DOI redirects to IEEE and the journal/year metadata match.
- `leng2024`: **Incorrect.** The arXiv record lists **Ashwin Sah**, not **Ankit Sah**.
- `epochai2025arithmetickakeya`: **Incorrect.** The stored URL returns **404**, and web search surfaces a different current Epoch AI / FrontierMath task page with changed title/year/path.
- `archivara_certificate_grammar`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact, not a web-verifiable citation.
- `archivara_h1_program`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_search_script`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository script.
- `archivara_h1_obstruction`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_h1_frontier`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_width4`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_width6`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_width8`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_h2`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_ablations`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.
- `archivara_verification`: **Incorrect under strict audit.** Exact-title web search did not verify a public source; this is a local repository artifact.

## Novelty Assessment

The paper does contribute something real, but it is not a strong creative advance. What is genuinely novel is narrow: a width-2 corridor compiler/verifier correctness theorem and a one-seed obstruction theorem that kills the frozen H1 route before scoring. What is **not** novel, and should not be sold as such, is any broader arithmetic-Kakeya theorem, new formulation, successful cellular-automaton mechanism, successful abelian-network mechanism, or ConceptEvolve-driven discovery story. The repository’s own novelty artifacts already say this. The final contribution surface is a disciplined negative result plus route-local theory, not a surprising new idea likely to shift expert opinion in arithmetic combinatorics.

The CE trail is especially weak as evidence of creative contribution. `results/concept_evolve/concept_delta.md` shows route narrowing and methodological steering, but `results/concept_evolve/semantic_bridge.json` has no bridge payload and all 32 `results/concept_evolve/tree/*/concept.json` files lack `experimental_result`. That looks much more like brainstorming and pruning than like tested cross-domain innovation. Under the review rubric, that is a **2/5** novelty outcome, not a 3+.

## Overall Verdict

**DEEPEN**

This is not an `ACCEPT` because citation accuracy fails, figure quality is below standard, and the surviving contribution is too narrow. It is not merely a `REVISE` because the central limitation is not just paper polish. Even after citation repair and provenance cleanup, the work would still read as a corridor-local falsification note rather than a genuinely creative advance. The right next cycle is a deepening cycle that includes quality repairs.

## Deepening Instructions

1. **Repair the bibliography completely before re-submission.**
   Correct the external metadata errors listed above. Remove the `archivara_*` entries from the formal bibliography or clearly reclassify them as repository artifacts in a separate appendix/table rather than as literature citations. Replace the broken Epoch AI entry with the current public task page if task-context citation is still needed.

2. **Fix provenance errors and unsupported claims.**
   Remove or properly summarize the width-8 boundary-stress `0/16` claim unless it is backed by a saved cited artifact. Rewrite `research_paper.tex:487` and `research_paper.tex:812-814` so the manuscript no longer claims stronger artifact provenance than actually exists. Cite the real source of the H1 identity-word example, or weaken the prose.

3. **Regenerate the figures to publication quality.**
   Separate schematic illustrations from data figures, explicitly label schematics as conceptual diagrams, remove the hard-coded unsupported Figure 6 bar, fix label collisions in Figure 5, and generally move away from slide-style rounded-box figures toward more compact, publication-grade layouts.

4. **Deepen the research contribution beyond the current corridor-local negative result.**
   A stronger paper would need at least one of the following:
   - a genuinely broader theorem or obstruction beyond the frozen width-2 corridor family;
   - a new exact certificate-search mechanism that beats matched direct arithmetic baselines on a nontrivial broader family;
   - a result that survives matched width/seed-budget controls and moves meaningfully closer to the `1.675` target;
   - a broader exact search over constructible-graph families, not just corridor variants.

5. **If ConceptEvolve is claimed as part of the creative engine, actually turn it into evidence.**
   Populate `experimental_result` in the concept tree, execute bridge-derived experiments, and make `semantic_bridge.json` reflect real tested bridge chains. Right now the CE artifacts document narrowing and rejection, not realized creative contribution.

6. **Close the benchmark gaps if you want a stronger empirical claim.**
   Run the missing matched width-8 direct control, execute the pre-registered non-CA baselines, and rerun the frozen-`X` scaling tests under matched budgets. Those steps will not solve the novelty problem by themselves, but they are necessary if the benchmark claims are to be stronger than a narrow negative note.
