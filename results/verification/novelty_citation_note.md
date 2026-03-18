# Novelty Citation Note

## Scope

This note audits the citation and evidence support behind `results/verification/novelty_precheck.md` using the artifacts requested for item 015:

- `results/branches/H1_defect_syndrome_ca_64m.md`
- `results/branches/H1_precheck.md`
- `results/branches/H2_gate.md`
- `results/branches/H3_gate.md`
- `results/literature/prior_art_gap.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/literature_snapshot.json`
- `results/verification/benchmark_spec.md`
- `results/verification/benchmark_gate.md`
- `sources.bib`

`results/verification/novelty_precheck.md` was also read as the target artifact under audit.

## Support Map For The Named-Paper Comparisons

### 1. Cellular Automata Applications in Shortest Path Problem (2017)

- BibTeX support:
  - `tsompanas2017`
- Artifact support:
  - `results/literature/prior_art_watchlist.md`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/branches/H1_defect_syndrome_ca_64m.md`
  - `results/branches/H1_precheck.md`
  - `results/verification/benchmark_spec.md`
  - `results/verification/benchmark_gate.md`
  - `results/verification/novelty_precheck.md`
- What those artifacts actually support:
  - The paper is real CA-for-search prior art, not just lexical noise.
  - H1 is differentiated only narrowly: compact q/s plus lag-syndrome state, fixed order-668 seed, matched non-CA controls, and exact-hit gating.
  - `results/branches/H1_precheck.md` is load-bearing because it explicitly warns that H1 can collapse into packetwise local search with CA vocabulary.
- Support status:
  - Adequate for the narrow comparison in `novelty_precheck.md`.
  - Not adequate for any broad claim that CA-based search here is categorically new.

### 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)

- BibTeX support:
  - `ghaleb2019`
- Artifact support:
  - `results/literature/prior_art_watchlist.md`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/verification/benchmark_spec.md`
  - `results/verification/benchmark_gate.md`
  - `results/verification/novelty_precheck.md`
- What those artifacts actually support:
  - This is an automata-based optimization paper on a control/scheduling problem, so it is a language-discipline comparator rather than substantive CA/Hadamard prior art.
  - The benchmark documents support the exact-feasibility and matched-control differences that separate this repo's branch claims from generic optimization rhetoric.
- Support status:
  - Adequate only for the negative claim that the overlap is lexical/method-shape, not domain or certification overlap.
  - Metadata quality is weaker than it should be: the snapshot entry has the single-elevator title but an abstract describing the multi-elevator extension, so do not paraphrase its contents beyond "learning-automata elevator optimization" until the entry is revalidated.

### 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)

- BibTeX support:
  - `ghaemi2022`
- Artifact support:
  - `results/literature/prior_art_watchlist.md`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/verification/novelty_precheck.md`
- What those artifacts actually support:
  - This paper entered through broad `automata` matching and serves only as a documented false positive.
  - The repo support is sufficient to say there is no shared problem domain, state representation, objective, or verification regime.
- Support status:
  - Strong enough for "watchlist noise" and nothing more.

### 4. Engineering Societies in the Agents World (2000)

- BibTeX support:
  - `leeuwen2000`
- Artifact support:
  - `results/literature/prior_art_watchlist.md`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/branches/H3_gate.md`
  - `results/verification/novelty_precheck.md`
- What those artifacts actually support:
  - The overlap is rhetorical only: distributed-agent language, not CA/Hadamard search.
  - `results/branches/H3_gate.md` is the main branch artifact that keeps the work from drifting into broader distributed-rule rhetoric.
- Support status:
  - Adequate for a false-positive comparison.
  - Not adequate for any detailed claim about the paper beyond that high-level distinction.

### 5. A 64-Modular Hadamard Matrix of Order 668 (2025)

- BibTeX support:
  - `eliahou2025_64mod668`
- Artifact support:
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/branches/H1_defect_syndrome_ca_64m.md`
  - `results/branches/H1_precheck.md`
  - `results/branches/H2_gate.md`
  - `results/branches/H3_gate.md`
  - `results/verification/benchmark_spec.md`
  - `results/verification/benchmark_gate.md`
  - `results/verification/novelty_precheck.md`
- What those artifacts actually support:
  - This is the true frontier anchor and the source of the recovered seed the branch work is built on.
  - The only repo-supported differentiation is narrow: seeded exact-repair/search on top of the published 64-modular object, compared under matched non-CA budgets and exact-hit reporting.
  - The H2/H3 gate files matter here because they show the repo is intentionally refusing to widen the claim before H1 proves anything.
- Support status:
  - Strongest supported comparison in the repo.
  - Still conditional: the evidence does not support claiming a distinct method contribution beyond a gated seeded-repair program.

## Unsupported Or Weak Wording To Avoid

- Avoid `cellular automata are new for Hadamard matrices`.
- Avoid `automata are untried here`.
- Avoid `H1 is already a distinct CA repair method`.
- Avoid `H1 is materially different from generic local search` before matched frontier evidence shows more than packetwise scoring plus light neighborhood control.
- Avoid `H2 is a new lag-space search dynamic` before the locality-failure trigger is met and the family-leakage audit is passed.
- Avoid `H3 is a fresh order-668 direction` or `H3 is a live solver branch` before the reserve gate opens and the direct CA-construction overlap check is anchored by sources.
- Avoid using the stale sentence in `results/verification/benchmark_spec.md` that says H1 had not yet been implemented as if it were current-status evidence. That file supports fairness constraints, not present branch readiness.
- Avoid detailed content claims about `ghaleb2019` beyond the elevator-learning-automata level until the title/abstract mismatch in the snapshot is rechecked.

## Bibliography Quality Flags

- `tsompanas2017`
  - The title, DOI, and paper ID align with the watchlist and snapshot, so the paper itself is not a hallucination.
  - The current BibTeX is weak because it mixes `journal={arXiv.org}` with a Springer chapter DOI.
- `ghaleb2019`
  - The title and DOI align with the watchlist and snapshot, but the snapshot abstract appears to describe the multi-elevator extension rather than a clean single-elevator abstract.
  - Treat this entry as existence support for the watchlist comparison, not as a trustworthy source for detailed paraphrase until it is revalidated.
- `ghaemi2022`
  - Sufficient for the current false-positive watchlist role.
- `leeuwen2000`
  - Likely a proceedings-volume level entry rather than a chapter-specific citation.
  - Adequate for the current false-positive warning, weak for direct substantive citation.
- `eliahou2025_64mod668`
  - Strong and internally consistent with the frontier anchor block in `results/literature/literature_snapshot.json`.
- Watchlist gap outside the named five:
  - `results/literature/prior_art_gap.md` has a section for `Learning Automata-Based Solutions to the Multi-Elevator Problem (2019)`, but there is no matching BibTeX key in `sources.bib`.
  - Either add that entry before citing it in formal verification artifacts or keep it out of citation-bearing novelty claims.

## Evidence-Link Recommendations For `results/literature/prior_art_gap.md`

- Section 1, `Cellular Automata Applications in Shortest Path Problem (2017)`:
  - Append `results/literature/prior_art_watchlist.md`.
  - Append `results/literature/literature_snapshot.json`.
  - Append `results/verification/benchmark_spec.md`.
  - Append `results/verification/benchmark_gate.md`.
- Section 2, `Learning Automata-Based Solutions to the Single Elevator Problem (2019)`:
  - Append `results/literature/prior_art_watchlist.md`.
  - Append `results/verification/benchmark_spec.md`.
  - Append `results/verification/benchmark_gate.md`.
  - Add a short note that the current snapshot metadata should be revalidated before any detailed paraphrase of this paper.
- Section 3, `On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)`:
  - Append `results/literature/prior_art_watchlist.md`.
  - Keep the comparison restricted to lexical false-positive status.
- Section 4, `Engineering Societies in the Agents World (2000)`:
  - Append `results/literature/prior_art_watchlist.md`.
  - Keep `results/branches/H3_gate.md` as the branch-side support for the rhetorical-drift warning.
- Section 6, `A 64-Modular Hadamard Matrix of Order 668 (2025)`:
  - Append `results/verification/benchmark_spec.md`.
  - Append `results/verification/benchmark_gate.md`.
  - Append `results/branches/H2_gate.md`.
  - Append `results/branches/H3_gate.md`.
  - Use those links to make the narrow claim explicit: seeded repair on the 2025 frontier object under matched exactness constraints, not a broader novelty claim.
