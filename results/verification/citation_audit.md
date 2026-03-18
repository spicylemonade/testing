# Citation Audit

Phase: `post_deepen`

## Scope

Read:

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`

Spot-checked the main supporting artifacts referenced by the manuscript:

- `results/frontier/order_668_64m/seed_manifest.json`
- `results/frontier/order_668_64m/source_excerpt.txt`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/summary.json`
- `results/analysis/frontier_locality_scan.json`
- `results/analysis/composite_packet_locality_atlas.json`
- `results/analysis/composite_packet_retained_library.json`
- `results/verification/radius_limited_locality_barrier.json`
- `results/experiments/order_668_hypergraph_ca/summary.json`
- `results/experiments/order_668_lattice_gas/summary.json`
- `results/experiments/order_668_orbit_ca/summary.json`
- `results/experiments/order_668_population_ca/summary.json`
- `results/analysis/frontier_population_phase_map.json`
- `results/verification/family_leakage_audit.json`

Used targeted web and Semantic Scholar checks for citation identity / source-suggestion gaps.

## Overall Verdict

- The core quantitative story is well supported by saved repo artifacts.
- The main citation problems are not broken `\cite{}` keys. They are:
  - unsupported or weakly sourced comparative framing,
  - missing point-of-use provenance citations,
  - named method/family terminology introduced without literature support,
  - one unsafe literature claim about the phrase `cellar automata`,
  - and a small amount of bibliography metadata noise.
- I did not find an obvious hallucinated paper among the 12 keys actually cited in `research_paper.tex`.

## Support Map For Key Claims

| Claim cluster | Support status | Main support |
| --- | --- | --- |
| Eliahou 2025 is the frontier anchor; recovered seed has 13 exceptional coefficients and seed tuple `13/2880/512`. | Strong | `eliahou2025_64mod668`; `results/frontier/order_668_64m/seed_manifest.json` |
| H1 is executable on the tiny controls but negative on the canonical frontier. | Strong | `results/experiments/controls/summary.json`; `results/experiments/order_668_64m/summary.json` |
| No depth-1 actuator in the checked class improves the canonical seed. | Strong | `results/analysis/frontier_locality_scan.json`; `results/analysis/composite_packet_retained_library.json`; `results/verification/radius_limited_locality_barrier.json` |
| First certified retained depth-2 counterexample is edge `[3,7]` leading to `13/2744/480`. | Strong | `results/verification/radius_limited_locality_barrier.json`; `results/experiments/order_668_hypergraph_ca/summary.json` |
| Lattice-gas branch reproduces the same improved state. | Strong | `results/experiments/order_668_lattice_gas/summary.json` |
| Population branch does not separate from zero-coupling at the selected operating point. | Strong | `results/experiments/order_668_population_ca/summary.json`; `results/analysis/frontier_population_phase_map.json` |
| Literature-positioning / novelty-boundary language. | Mixed | Broadly plausible, but several sentences are author synthesis with too little clause-level citation support. |

## Findings

### 1. Unsafe literature claim about `cellar automata`

Affected text:

- `research_paper.tex:60`
- `research_paper.tex:92`

Issue:

- The manuscript currently states or strongly implies that there is no distinct literature meaning for `cellar automata`.
- That is not safe as a literature claim. Targeted web search finds published work explicitly using the phrase `cellar automata`, albeit in a different domain.

Why it matters:

- This is the clearest citation-risk item because it is not just under-cited; it is factually over-strong.

Recommended fix:

- Rephrase as a repository-interpretation statement, e.g. "No distinct meaning was evidenced in the repo materials and literature snapshot used for this run, so this manuscript interprets the user phrase as cellular automata."
- Do not state that the phrase has no literature usage unless you cite and scope that claim carefully.

Concrete source to add if you keep a literature remark:

- *Cellar automata models for reservoir computing in single-walled carbon nanotube network complexed with polyoxometalate* (2024)

### 2. Literature-positioning paragraphs rely on synthesis more than citations

Affected text:

- `research_paper.tex:88`
- `research_paper.tex:117-131`

Issue:

- These paragraphs combine multiple claims in one sentence: open-order framing, modular-history framing, exact-search comparison, heuristic-search comparison, and CA-design comparison.
- The cited papers are real, but the sentence-level bundles are doing more argumentative work than the local citations support.

Examples:

- `research_paper.tex:88` would be better split. `cati2024` and `eliahou2005` support catalogue/modular-history context, but the specific order-668 open-case framing is better anchored by `eliahou2025_64mod668`.
- `research_paper.tex:131` is the most citation-thin comparative sentence in the manuscript. It compares the paper against Eliahou, Tsompanas, Suksmono, Bright, and CA-design papers, but the comparison sentence itself carries no citation cluster.

Recommended fix:

- Either add clause-level citation clusters to the comparison sentences, or explicitly mark them as author synthesis (`in our reading`, `relative to these sources, we position this work as ...`).

Most important concrete sources to add or reuse:

- Reuse existing keys locally: `eliahou2025_64mod668`, `tsompanas2017`, `suksmono2018`, `suksmono2019`, `suksmono2022`, `bright2018`, `bright2019`, `mariot2019_mols`, `gadouleau2020`
- Optional broader CA-design anchor: *Combinatorial designs and cellular automata: A survey* (2025)

### 3. Point-of-use provenance citations are missing for Eliahou-derived seed facts

Affected text:

- `research_paper.tex:142`
- `research_paper.tex:161`
- `research_paper.tex:208`
- `research_paper.tex:748`

Issue:

- The paper correctly cites Eliahou 2025 in the introduction / related-work section, but then reuses seed-provenance facts later as if they were fully internal facts:
  - decoded from Eliahou's run-length encoding,
  - reproduced exceptional coefficients,
  - figure caption describing the recovered seed,
  - experimental input naming the canonical frontier seed from Eliahou's paper.

Why it matters:

- These are load-bearing provenance statements. They should carry the frontier-anchor citation at the point of use, not only earlier in the paper.

Recommended fix:

- Add `\citep{eliahou2025_64mod668}` in each local context above.

### 4. Named-family leakage audit is uncited as literature

Affected text:

- `research_paper.tex:77`
- `research_paper.tex:914`

Issue:

- The manuscript names Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant families as if their relevance is self-evident, but it gives no literature citation for those family labels.
- The artifact itself (`results/verification/family_leakage_audit.json`) supports that a repo-side audit was run. It does not substitute for citations defining the compared families.

Recommended fix:

- Keep the artifact reference for the pass/fail result.
- Add at least one literature source for the family taxonomy and one cocyclic-specific source if that check remains named explicitly.

Most important concrete sources to add:

- Horadam, *Hadamard Matrices and Their Applications* (umbrella family reference)
- *Constructing cocyclic Hadamard matrices of order 4p* (cocyclic-specific anchor)

### 5. Population-branch method terms are introduced without standard citations

Affected text:

- `research_paper.tex:453-470`
- `research_paper.tex:943`

Issue:

- The manuscript uses `Gumbel-softmax distribution` and `self-organizing` / `self-stabilizing` language without citing the underlying method or background literature.

Why it matters:

- These are recognizable external method terms, not purely internal repo inventions.

Recommended fix:

- Add one standard Gumbel-softmax citation.
- If the paper keeps the stronger self-organization framing, add one CA-control / self-organization comparator as well.

Most important concrete sources to add:

- Jang, Gu, and Poole, *Categorical Reparameterization with Gumbel-Softmax* (ICLR 2017)
- Maddison, Mnih, and Teh, *The Concrete Distribution: A Continuous Relaxation of Discrete Random Variables* (alternative standard citation)
- Reuse existing `sudhakaran2022` if the self-organizing/control framing stays

### 6. One comparative sentence is stronger than the saved evidence

Affected text:

- `research_paper.tex:882`

Issue:

- The figure caption says "Orbit CA matches or exceeds the same outcomes with far fewer lookups."
- The saved orbit summary does not fully support that wording. On `barrier_ladder_01`, `orbit_quotient_ca` ends at `13/2880/512`, while the hypergraph branch reaches `13/2744/480`.

Why it matters:

- This is an unsupported comparison, even though the broader claim that orbit improves frontier-ladder states is still largely supported.

Recommended fix:

- Rewrite the caption to something narrower, for example:
  - "Orbit CA improves all six states and often reaches the same improved frontier state with fewer lookups."
  - or explicitly separate the canonical-seed claim from the ladder claim.

Support file:

- `results/experiments/order_668_orbit_ca/summary.json`

### 7. Several true setup / robustness claims point at the wrong artifact or at no artifact

Affected text:

- `research_paper.tex:387`
- `research_paper.tex:761`
- `research_paper.tex:937`
- `research_paper.tex:943-948`

Issue:

- These statements are mostly numerically correct, but the manuscript does not always name the artifact that actually supports them.

Examples:

- `research_paper.tex:387` gives the exact count of `56` ordered causal cones. I did not find that count surfaced in the saved JSON summaries; it appears to be derivable from `hadamard_ca/retained_state_graph.py`, which makes the claim plausible but weakly artifact-backed.
- `research_paper.tex:761` names the orbit rule-table file, but the population `133`-signature control-only table and its parameter bundle live in `results/experiments/order_668_population_ca/summary.json` and `results/experiments/order_668_population_ca/rule_table.json`.
- `research_paper.tex:937` says the orbit rule table was trained without the canonical frontier seed. That is supported by the orbit training manifest in `results/experiments/order_668_orbit_ca/summary.json`, not by the rule-table file alone.
- `research_paper.tex:943-948` makes the key robustness comparison (`3/5`, `0/5`, diffusion-only phase map), but neither `results/experiments/order_668_population_ca/summary.json` nor `results/analysis/frontier_population_phase_map.json` is named in the local text.

Recommended fix:

- Add the actual supporting artifact path wherever these claims are made.
- If the `56`-cone count is important, export it into a saved result artifact instead of leaving it as an implicit code-derived quantity.

### 8. Bibliography hygiene: low severity, but worth cleaning before final assembly

Affected entries:

- `sources.bib:62-68` (`suksmono2024`)
- Unused watchlist/noise entries: `ghaleb2019`, `ghaemi2022`, `leeuwen2000`

Issue:

- `suksmono2024` appears to have the wrong year for the cited Scientific Reports article and is currently unused in the manuscript.
- The off-topic watchlist entries are not hurting the current paper because they are uncited, but they remain risky if later pulled into the writeup without revalidation.

Recommended fix:

- Correct `suksmono2024` before citing it.
- Keep the watchlist-noise entries out of the manuscript argument unless manually revalidated.

## Likely Citation Hallucinations

- None found among the 12 keys actually cited in `research_paper.tex`.
- The current risk profile is instead:
  - real sources used too broadly,
  - missing point-of-use citations,
  - uncited comparative language,
  - and bibliography/watchlist noise.

## Most Important Sources To Add

1. `eliahou2025_64mod668` at every local seed-provenance reuse point (`research_paper.tex:142`, `:161`, `:208`, `:748`).
2. Jang et al., *Categorical Reparameterization with Gumbel-Softmax* for `research_paper.tex:465`.
3. Horadam, *Hadamard Matrices and Their Applications* for the Williamson / Turyn / Goethals-Seidel / block-circulant family names.
4. A cocyclic-specific source such as *Constructing cocyclic Hadamard matrices of order 4p* if `cocyclic` remains named explicitly.
5. `sudhakaran2022` if the paper keeps the `self-organizing` framing.
6. *Combinatorial designs and cellular automata: A survey* if the CA-design positioning in `research_paper.tex:127-131` stays broad.
7. `suksmono2024` after metadata repair, if the heuristic-comparator sentence at `research_paper.tex:123` continues to say "related optimization formulations."

## Bottom Line

- The paper's central quantitative claims are evidence-traceable.
- The writeup still needs a citation pass in four places: `cellar automata`, comparison-heavy related work, local Eliahou seed provenance, and external method/family terminology.
- Fixing those items should materially reduce the remaining citation risk without changing the core scientific story.
