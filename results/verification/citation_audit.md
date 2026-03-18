# Citation Audit

## Scope

Reviewed:

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`
- `results/literature/literature_snapshot.json`

Checked cited repo support where needed:

- `results/phase2_certificate_grammar.md`
- `results/phase3_h1_program.md`
- `results/phase3_h2_program.md`
- `results/phase3_h3_hedge.md`
- `results/phase4_h1_frontier.md`
- `results/phase4_h1_obstruction.json`
- `results/phase4_width4_seed601.json`
- `results/phase4_width6_seed602.json`
- `results/phase4_width8_seed501.json`
- `results/phase4_sparse_unrestricted_seed502.json`
- `results/phase4_h2_screen.md`
- `results/phase4_h2_screen.json`
- `results/phase4_ablations.md`
- `results/phase4_ablations.json`
- `results/phase1_planning_note.md`
- `results/phase4_experiment_matrix.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/verification/verification_summary.md`
- `results/verification/benchmark_report.md`
- `scripts/ca_kakeya_search.py`
- `scripts/phase4_ablations.py`
- `scripts/phase4_h2_screen.py`
- `scripts/generate_paper_figures.py`

Focus:

- whether key paper claims have traceable support;
- missing citations;
- weak citations;
- likely citation hallucinations or claim-to-source mismatches;
- uncited comparisons.

## Bottom Line

The narrow negative result is mostly supportable:

- exact H1 failure before scoring is well supported;
- width-4 and width-6 exact best scores of `2.0` are well supported;
- the H2 "no lift" claim is supportable on the tiny four-family screen;
- the width-4 ablation story is locally supportable.

The main citation risk is not fabricated outside literature. It is claim-to-source mismatch inside the repo:

- the benchmark target / threshold provenance is uncited;
- the `0/16` width-8 boundary-stress claim is not present in the cited ablation artifacts;
- the exact H1 identity-word / extracted-instance description is cited to the wrong artifacts;
- the false-positive prior-art paragraph cites the wrong repo artifact.

I did not find an obviously nonexistent external paper in `sources.bib`, but I did find at least one concrete metadata error:

- `sources.bib:54-59` lists `Cristian Pohoata`; the saved literature snapshot records `C. Pohoata`.

## Key Claim Support

| Claim in paper | Status | Best supporting source(s) | Notes |
| --- | --- | --- | --- |
| H1 fails before scoring by an exact one-seed obstruction | supported | `results/phase4_h1_obstruction.json`; `results/phase4_h1_frontier.md` | good citation boundary |
| Best verified direct controls are `2.0` at widths 4 and 6 | supported | `results/phase4_width4_seed601.json`; `results/phase4_width6_seed602.json` | exact scores and certificate lines match |
| Width-8 witnesses are worse than width-4/6 controls | supported locally | `results/phase4_width8_seed501.json`; `results/phase4_sparse_unrestricted_seed502.json` | true numerically, but not a matched baseline comparison |
| H2 adds no screening value on the tested family set | supported locally | `results/phase4_h2_screen.json`; `results/phase4_h2_screen.md` | only four family IDs |
| Width-4 witness is fragile under ablation | supported locally | `results/phase4_ablations.json`; `results/phase4_ablations.md` | sample sizes are tiny |
| Direct controls do not scale under frozen `X` | weak / overstated | `results/phase4_ablations.json`; `scripts/phase4_ablations.py`; `results/verification/benchmark_report.md` | saved scale test changes search parameters |
| Benchmark target `1.675` and `1.70` plan threshold | missing / uncited | `results/phase1_planning_note.md`; `results/phase4_experiment_matrix.md`; existing `epochai2025arithmetickakeya` bib entry | paper currently gives no source |

## Findings

### 1. Missing source for the benchmark formalism and the `1.675` / `1.70` thresholds

Severity: high

Affected paper locations:

- `research_paper.tex:65`
- `research_paper.tex:81`
- `research_paper.tex:145`
- `research_paper.tex:565-570`

Problem:

- The paper repeatedly uses the FrontierMath-style benchmark, the exact target `<= 1.675`, and the broader `1.70` plausibility threshold without citing any source for them.

What exists in-repo:

- `results/phase1_planning_note.md:3` gives the exact `<= 1.675` target.
- `results/phase4_experiment_matrix.md:88-89` gives the `1.70` neighborhood decision rule.
- `sources.bib` already contains `epochai2025arithmetickakeya`, but the paper never cites it.

Why this matters:

- These numbers are not self-justifying. They are part of the benchmark framing.
- Without a citation, readers cannot tell whether `1.675` is a repo-local target, a FrontierMath task threshold, or a theorem frontier number.

Recommended repair:

- Cite `epochai2025arithmetickakeya` for FrontierMath task context.
- Add repo bibliography entries for `results/phase1_planning_note.md` and `results/phase4_experiment_matrix.md` if the paper wants to document local planning provenance for `1.675` and `1.70`.

### 2. The `0/16` width-8 boundary-stress claim is not supported by the cited ablation artifacts

Severity: high

Affected paper locations:

- `research_paper.tex:519`
- `research_paper.tex:638-643`

Problem:

- The paper states that the width-8 boundary-stress archive contains `0/16` successes and gives a Wilson upper bound of about `0.19`.
- The only citation attached to this discussion is `archivara_ablations`, but neither `results/phase4_ablations.md` nor `results/phase4_ablations.json` contains that boundary-stress row.

What the cited artifact actually contains:

- `results/phase4_ablations.json:43-182` has randomized `R/T/X`, isotropic variants, boundary-seed removal, and two frozen-`X` scale rows.
- `results/phase4_ablations.md:19-30` matches that same set of rows.

Where the `0/16` number actually comes from:

- there are 16 raw files matching `results/phase4_sparse_boundary*.json`;
- all 16 have `best: null`;
- `scripts/generate_paper_figures.py:619-624` hard-codes `("boundary\nwidth-8 stress": (0, 16))`.

Why this matters:

- As written, this is a claim-level citation hallucination: the cited source does not contain the quoted evidence.
- It also makes `research_paper.tex:487` false, because not every quantitative claim in Results/Discussion is traced to a cited JSON/markdown artifact.

Recommended repair:

- package the 16 `phase4_sparse_boundary*.json` files into one summary artifact and cite that; or
- add a bibliography entry for `results/verification/benchmark_report.md`, which documents the 16-file archive; or
- remove the `0/16` claim from the paper until a proper artifact is cited.

### 3. The exact H1 identity-word / extracted-instance narrative is cited to the wrong source

Severity: high

Affected paper locations:

- `research_paper.tex:273-276`
- `research_paper.tex:531`

Problem:

- The paper describes a specific representative H1 family:
  - identity-style word built from `L_a`, `M_a`, and `R_a`;
  - top row carries `u`;
  - bottom row is zero;
  - vertical edges carry `z`;
  - exactly one singleton seed at the left boundary.
- The citations given are `archivara_h1_program` and `archivara_h1_obstruction`.
- Those artifacts support the template family, one-seed/empty-`T` obstruction, and extractor rules in general, but not that exact representative identity instance.

Where the exact representative is actually encoded:

- `scripts/phase4_h2_screen.py:38-68`
  - `h1_identity_word`
  - `h1_identity_instance`

Why this matters:

- The paper is not only using the H1 family definition. It is pointing to one specific representative extraction.
- That specific representative needs its own source, or the prose should be weakened.

Recommended repair:

- add a bibliography entry for `scripts/phase4_h2_screen.py`; or
- export the representative H1 identity instance to a small saved artifact and cite that; or
- rewrite the prose to stay at the level actually supported by `archivara_h1_program` and `archivara_h1_obstruction`.

### 4. The false-positive prior-art paragraph cites the wrong repo artifact

Severity: medium

Affected paper location:

- `research_paper.tex:116`

Problem:

- The paragraph about spurious watchlist items and token overlap cites `archivara_verification`.
- `results/verification/verification_summary.md` does not record the specific false-positive titles or the token-overlap explanation.

Where the support actually is:

- `results/literature/prior_art_watchlist.md:1-40`
- `results/literature/prior_art_gap.md:1-55`

Why this matters:

- The claim is true in the repo, but the citation target is wrong.
- This is another claim-to-source mismatch, not a missing fact.

Recommended repair:

- add a bibliography entry for `results/literature/prior_art_gap.md` or `results/literature/prior_art_watchlist.md`;
- keep `archivara_verification` for high-level framing, not for the specific watchlist titles.

### 5. Setup and uncertainty statements are weakly traced or uncited

Severity: medium

Affected paper locations:

- `research_paper.tex:515`
- `research_paper.tex:519`
- `research_paper.tex:304`

Problems:

- hardware/software environment (`Linux x86_64`, `20` logical cores, `1.0 TiB`, exact package versions) is uncited;
- the ablation RNG seed `1901` is not cited in the paper and appears only in `scripts/phase4_ablations.py`;
- the uncertainty paragraph mixes supported saved rows with the unsupported width-8 boundary-stress count;
- "runtime remained negligible on a commodity multi-core server" is an uncited performance claim.

What I found:

- `scripts/phase4_ablations.py:214` sets the default RNG seed to `1901`;
- I did not find a saved environment artifact supporting the exact OS / CPU / RAM / package-version paragraph.

Recommended repair:

- if the setup paragraph stays, add a saved environment artifact and cite it;
- if the `1901` seed stays, add a bibliography entry for `scripts/phase4_ablations.py` or a run log that records it;
- otherwise trim these details.

### 6. Some comparisons are true only in a narrow or interpretive sense

Severity: medium

Affected paper locations:

- `research_paper.tex:102`
- `research_paper.tex:615-638`
- `research_paper.tex:686`

Problems:

- `tao2025` is the right barrier paper for bounded slopes / rational complexity, but the line
  "it identifies a natural basin in which small, low-complexity certificate families can stagnate"
  is interpretive rather than directly measured here;
- the "frozen-`X` non-transfer" claim is stronger than the saved ablation actually warrants.

Why the frozen-`X` claim is weak:

- `scripts/phase4_ablations.py:193-205` runs the scale rows with `seed_budget=6` and `boundary_band=2`;
- this differs from the base saved direct-search settings reported in the paper;
- `results/verification/benchmark_report.md` already flags that confound.

Recommended repair:

- keep the Tao comparison as "consistent with" / "interpretive";
- rewrite the ablation conclusion as:
  - "no forcing witness was found under the saved fixed-motif frozen-`X` stress test"
  instead of
  - "the direct controls do not improve with width under frozen-`X` scaling."

### 7. The H2 and ablation claims are supportable, but only with the paper's current local qualifiers

Severity: medium

Affected paper locations:

- `research_paper.tex:585-609`
- `research_paper.tex:615-643`

Assessment:

- The H2 screen is supportable only "on the tested family set," which is four family IDs total.
- The ablation story is supportable only for the one saved width-4 base witness and tiny randomized samples (`0/4`, `0/4`, `3/4`).

Recommended repair:

- keep the local qualifiers already present;
- do not widen those claims beyond the saved family set and saved samples.

### 8. The bootstrap / abelian / decoder citations are weak only if they are read as direct prior art

Severity: low

Affected paper locations:

- `research_paper.tex:81`
- `research_paper.tex:108`
- `research_paper.tex:112`

Assessment:

- I did not find evidence that these are fabricated references.
- The issue is framing: these are analogy / nearby-language citations, not direct arithmetic-Kakeya support.

Recommended repair:

- leave them in only as conceptual-overlap citations;
- avoid wording that implies these papers directly motivate or validate the corridor benchmark.

### 9. Bibliography hygiene: one concrete metadata error, plus some version-mixing

Severity: medium

Concrete error:

- `sources.bib:54-59` gives `Cristian Pohoata`.
- `results/literature/literature_snapshot.json:155-160` records the same paper with author `C. Pohoata`.

Likely intended fix:

- verify the preferred author spelling from the primary source and update `pohoata2024`.

Lower-priority style issue:

- several entries mix preprint-year naming with later journal metadata.
- This is sloppy, but it is weaker than the claim-to-source mismatches above.

## Likely Citation Hallucinations Or Misattributions

These are the main claim-level hallucination risks I found:

1. `archivara_ablations` cited as support for the width-8 boundary-stress `0/16` claim.
   - The cited artifact does not contain that row.

2. `archivara_h1_program` plus `archivara_h1_obstruction` cited as support for the exact H1 identity representative.
   - The exact identity representative is actually encoded in `scripts/phase4_h2_screen.py`.

3. `archivara_verification` cited as support for the specific false-positive watchlist titles and token-overlap explanation.
   - Those specifics live in the prior-art files, not the verification summary.

No obvious nonexistent external paper was detected in `sources.bib`.

## Most Important Concrete Sources To Add

1. `epochai2025arithmetickakeya`
   - already present in `sources.bib`, but currently unused;
   - best immediate source for the FrontierMath-style task context.

2. A new bibliography entry for `results/phase1_planning_note.md`
   - supports the local `<= 1.675` target as a planned repo objective.

3. A new bibliography entry for `results/phase4_experiment_matrix.md`
   - supports the local `1.70` plausibility threshold and decision rule.

4. A new bibliography entry for `results/literature/prior_art_gap.md`
   - best repo-local support for the false-positive watchlist discussion.

5. A new bibliography entry for `scripts/phase4_h2_screen.py`
   - needed if the paper keeps the exact H1 identity representative in prose or figure captions.

6. A new summary artifact for the 16 `results/phase4_sparse_boundary*.json` files
   - needed if the paper keeps the `0/16` width-8 boundary-stress claim.

7. A saved environment artifact
   - needed only if the hardware/software paragraph stays.

8. Keep `tao2025`
   - good support for the bounded-slopes / rational-complexity caution and for the "best upper bound is about `1.67513...`" frontier note;
   - not enough by itself for the local `1.675` benchmark target or `1.70` plan threshold.

## Publication-Safe Position Right Now

With current evidence and citations, the paper can safely claim only:

- exact H1 failure before scoring;
- exact direct controls at `2.0` for widths 4 and 6;
- exploratory width-8 rows are worse than those saved width-4/6 controls;
- H2 adds no visible screening lift on the tiny four-family screen;
- the width-4 direct witness is locally fragile under the saved ablations.

The paper is not yet citation-clean on:

- the provenance of the `1.675` target and `1.70` threshold;
- the `0/16` width-8 boundary-stress count;
- the exact representative H1 identity narrative;
- the false-positive prior-art paragraph;
- the hardware/software setup paragraph.
