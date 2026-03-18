# Citation Audit

## Review Round

- `review_round_1`

## Scope

- Audited inputs: `research_paper.tex`, `sources.bib`, `results/research_context.md`, and `results/literature/semantic_scholar_manifest.json`.
- Supporting traceability checks: `results/research_context.json`, `results/literature/seed_search.json`, `results/literature/literature_snapshot.json`, `results/artifacts/seed_668_mod64.json`, `results/experiments/h2_seed_attempt.json`, `results/analysis/paper_metrics.json`, `hadamard668/experiments.py`, `results/concept_evolve/recurrent_state.json`, and `results/concept_evolve/bridge_candidates.json`.
- Budget focus: evidence traceability and citation support only. No style pass except where wording changes are needed to explain unsupported claims.

## Overall Assessment

- The narrow manuscript claim is supportable. The load-bearing external anchors are appropriate and real: `constantine2025cyclic` for the exact `H1` obstruction and `eliahou2025mod64` for the exact `H2` seed.
- The main citation risk is not a fabricated core source. It is that several sentences use bibliography entries to support claims that are actually about repository search logs, repository provenance, or repository-derived computations.
- Mechanical key integrity is good: every in-text citation key resolves in `sources.bib`. One bibliography entry is unused noise residue: `khatoon2019tutoring`.

## Claim Support Snapshot

| Claim cluster | Status | Evidence |
| --- | --- | --- |
| Exact `H1` anchor (`research_paper.tex:84`, `103`, `137`, `425`) | Supported | `constantine2025cyclic` is the right external anchor. The instantiated object is mirrored in `results/artifacts/target_167_weight_80.json` and summarized in `results/analysis/paper_metrics.json:12-105`. |
| Exact `H2` anchor (`research_paper.tex:84`, `103`, `127`) | Supported | `eliahou2025mod64` is the right external anchor. The instantiated seed is mirrored in `results/artifacts/seed_668_mod64.json:1007-1012` and `results/analysis/paper_metrics.json:106-164`. |
| Derived `H2` seed facts (`research_paper.tex:195`, `425`) | Partially supported / over-attributed | The external paper supports the existence of the published `64`-modular seed. The manuscript's derived facts about `13` nonzero defects and the deterministic `s_41` degradation to modulus `16` are repository computations, traceable to `results/analysis/paper_metrics.json:106-164`, `hadamard668/experiments.py:254-285`, and `results/experiments/h2_seed_attempt.json:68-110`. |
| Core negative result (`research_paper.tex:80`, `436-522`, `554`) | Supported internally | The decisive numbers are traceable to `results/analysis/paper_metrics.json:179-240`, `results/analysis/paper_metrics.json:648-730`, and `results/analysis/paper_metrics.json:1377-1448`. This is an internal-evidence issue, not a bibliography gap. |
| Search-drift / lexical-noise paragraph (`research_paper.tex:114-115`) | Weak / miscited | The cited papers identify the noisy hits, but the claim that the automated search surfaced them is supported by `results/literature/seed_search.json:1-120`, `results/literature/literature_snapshot.json:245-332`, and `results/literature/semantic_scholar_manifest.json:3-24`, not by those papers themselves. |
| Prompt-history / literal-cellar provenance (`research_paper.tex:76`, `86`, `258`, `432`, `541`, `556`) | Traceability gap | These are not literature claims. They need explicit repository-artifact support such as `results/research_context.json:5`, `results/concept_evolve/recurrent_state.json:2-16`, and `results/concept_evolve/bridge_candidates.json:3-7`. |
| Broad novelty boundary (`research_paper.tex:88`, `105`, `110-112`) | Partially supported | The current citations show prior CA/design work and prior Hadamard heuristics. They do not by themselves prove the stronger comparisons and novelty-boundary language now attached to them. |

## Findings

1. **High: the lexical-noise paragraph is supported by the wrong kind of citation.**
   - `research_paper.tex:114-115` says the automated search surfaced the shortest-path, elevator, Ebola, and agents-world papers.
   - The current citations only prove those papers exist.
   - The actual support is internal: `results/literature/seed_search.json:1-120`, `results/literature/literature_snapshot.json:245-332`, and `results/literature/semantic_scholar_manifest.json:3-24` show the noisy query and the watchlist promotion.
   - Recommended fix: add an explicit repository-source pointer in the prose or appendix for the search-drift claim, and keep the paper citations only as identifiers of the noisy hits.

2. **Medium: the opening order-668 status sentence needs a direct citation on the status clause itself.**
   - `research_paper.tex:84` opens with "The existence of a Hadamard matrix of order `668` remains a difficult search target" and only then cites the cyclic and modular anchors.
   - The supporting source already exists in the bibliography: `eliahou2025mod64` is the cleanest in-scope citation for the order-`668` status/context sentence.
   - Recommended fix: attach `eliahou2025mod64` directly to the first clause, or add an independent modern Hadamard-status table if the paper wants a separate status citation.

3. **Medium: provenance claims about the prompt history and later literal-cellar reinterpretation are factual history, but they are not citation-bound yet.**
   - `research_paper.tex:76`, `86`, `258`, `432`, `541`, and `556` describe the original user prompt, the initial cellular-automata interpretation, and the later promotion of a pushdown-style reserve branch.
   - Those claims are supportable in the repo, but not by literature citations. The current best evidence is internal: `results/research_context.json:5`, `results/research_context.json:33-40`, `results/concept_evolve/recurrent_state.json:2-16`, and `results/concept_evolve/bridge_candidates.json:3-7`.
   - Recommended fix: add repository-artifact references or an appendix note for these provenance claims instead of leaving them as unsupported narrative reconstruction.

4. **Medium: the manuscript partially over-attributes repository-derived `H2` seed facts to the external seed paper.**
   - `research_paper.tex:195` and `research_paper.tex:425` attribute the `13` nonzero defects and the `s_41` degradation to the same citation chain as the published seed itself.
   - The external paper is the right anchor for the seed. The derived defect count and degraded-start modulus are repository computations.
   - Recommended fix: keep `eliahou2025mod64` for the seed provenance, but add explicit artifact support from `results/artifacts/seed_668_mod64.json:1007-1012`, `results/analysis/paper_metrics.json:106-164`, `hadamard668/experiments.py:254-285`, and `results/experiments/h2_seed_attempt.json:68-110`.

5. **Medium: the novelty-framing sentence is broader than the cited sources strictly support.**
   - `research_paper.tex:88` concludes that a broad statement such as "cellular automata for Hadamard search is untried" is indefensible.
   - The cited bundle does support two narrower propositions: CA already appears in adjacent design/search settings, and heuristic Hadamard search already has a literature.
   - It does not directly supply a prior source showing an executed CA-based search for a real Hadamard matrix of order `668`, or even a generic paper saying CA had already been tried for Hadamard search in the exact sense the sentence suggests.
   - Recommended fix: narrow the sentence to what the citations really prove, or label it explicitly as a scoped literature-search conclusion.

6. **Medium: some uncited comparisons are defensible author inferences, but they are not source-bound as written.**
   - `research_paper.tex:105` says the cited exact-search papers "define the novelty boundary."
   - `research_paper.tex:112` says matched same-representation baselines are "indispensable" and that otherwise the CA label contributes little more than a scheduling choice.
   - These are reasonable methodological conclusions, but they are not facts established by the cited technical papers alone.
   - Recommended fix: either mark them as authorial inferences or add benchmarking/methodology support if the venue expects those claims to read as sourced statements.

7. **Low-to-medium: two cited CA-side precedents are much weaker comparators than the rest of the paragraph.**
   - `research_paper.tex:110` cites `bagnoli2025controllability` and `herold2014decoder` alongside direct CA/design papers.
   - Those sources are legitimate local-dynamics precedents, but they are not close Hadamard or combinatorial-design comparators in the same way as `mariot2016ols`, `gadouleau2020bent`, and `mariot2021semibent`.
   - Recommended fix: keep them only if the text explicitly labels them as analogical precedents, or replace one of them with a more direct CA/design citation.

8. **Low: the modular-Hadamard definition could cite the standard background already present in the bibliography.**
   - `research_paper.tex:126-128` defines the modular Hadamard surrogate without citing `eliahoukervaire2005survey` or `horadam2007applications`.
   - This is not a claim failure, but a direct citation there would improve traceability for a nonstandard term.

9. **Low: the scientific-process paragraph reads as empirical generalization without support.**
   - `research_paper.tex:551` makes a broad claim about AI-assisted search changing terminology faster than mathematics.
   - That is acceptable as explicit authorial perspective. It is weak if presented as a sourced empirical claim.
   - Recommended fix: either soften it as perspective or add literature on evaluation/benchmarking in AI-assisted discovery.

## Bibliography Integrity Issues

- `sources.bib:9-18` (`eliahou2025mod64`):
  - Real and load-bearing, but the page range is wrong. The journal article runs `422--427`, not `422--429`.
- `sources.bib:41-48` (`manzoni2025survey`):
  - The entry mixes an arXiv DOI with a journal URL. Choose one version of record and normalize the year/venue/DOI consistently.
- `sources.bib:66-73` (`mariot2021semibent`):
  - The key/year says `2021`, but the DOI corresponds to the later `Natural Computing` journal publication. Normalize the year if the journal version is intended.
- `sources.bib:75-82` (`bagnoli2025controllability`):
  - The entry currently mixes preprint-era keying with journal metadata. Pick either the preprint or the journal version and normalize the metadata consistently.
- `sources.bib:159-165` (`djokovic2018goethalsseidel`):
  - The journal title is inaccurate, the DOI is missing, and the URL is noncanonical. This is the clearest metadata-quality problem among the exact-search comparators.
- `sources.bib:212-217` (`khatoon2019tutoring`):
  - Unused watchlist residue. Remove it unless it will be cited for a specific reason.
- `sources.bib` overall:
  - `16` of `24` entries use Semantic Scholar landing pages instead of DOI, publisher, journal, or arXiv URLs. This does not invalidate the narrow claim, but it weakens traceability and downstream citation export.

## Likely Citation Hallucinations

- I did **not** find a likely fabricated load-bearing citation among the papers actually cited in `research_paper.tex`.
- The stronger risk is miscitation and metadata drift:
  - using literature citations where the real support comes from repository artifacts,
  - over-attributing repository-derived computations to external papers,
  - and keeping weak or stale bibliography metadata for otherwise real sources.

## Most Important Concrete Sources To Add Or Replace

1. **No new external source is strictly required for `research_paper.tex:84`; move or repeat `eliahou2025mod64` there.**
   - This is the cleanest fix for the opening order-`668` status clause.

2. **Add repository-artifact support for the search-drift and provenance claims.**
   - Search drift: `results/literature/seed_search.json`, `results/literature/literature_snapshot.json`, and `results/literature/semantic_scholar_manifest.json`.
   - Prompt / reserve-branch provenance: `results/research_context.json`, `results/concept_evolve/recurrent_state.json`, and `results/concept_evolve/bridge_candidates.json`.

3. **If line 110 is intended to emphasize close CA/design prior art, add a more direct source.**
   - Best candidate: `Mutually Orthogonal Latin Squares based on Cellular Automata`, `Designs, Codes and Cryptography` 88 (2020), `391--411`, DOI `10.1007/s10623-019-00689-8`.

4. **If an independent modern Hadamard-status table is desired, add one explicitly rather than forcing that load onto adjacent citations.**
   - Best candidate: `A database of constructions of Hadamard matrices`.
   - This is optional; the immediate paper can already repair line `84` with `eliahou2025mod64`.

5. **Replace Semantic Scholar URLs with canonical source URLs for the load-bearing entries.**
   - Prioritize `bright2018satcas`, `mariot2016ols`, `mariot2021semibent`, `suksmono2016sa`, `suksmono2018sqa`, `suksmono2019`, `suksmono2022quantum`, `eliahoukervaire2005survey`, and `djokovic2018goethalsseidel`.

## Bottom Line

- The manuscript's branch-specific no-go claim is citation-supportable.
- The highest-priority fixes are:
  - correct the miscited search-process paragraph at `research_paper.tex:114-115`,
  - attach a direct citation to the opening order-`668` status clause at `research_paper.tex:84`,
  - add repository-artifact support for the prompt-history / literal-cellar provenance claims,
  - separate external seed provenance from repository-derived `H2` seed facts,
  - and repair the highest-value metadata problems in `sources.bib`.
