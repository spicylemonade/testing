# Novelty Report

Verification phase: `post_deepen`

## Scope

This audit evaluates the claims actually made in `research_paper.tex` after the deepen pass, using:

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/swarm/falsifier.md`
- `results/analysis/novelty_collapse_audit.md`
- `results/analysis/cellar_design_brief.md`
- `results/analysis/cellar_prefix_complexity.md`
- `results/analysis/cellar_no_go.md`
- `results/analysis/phase2_baseline_review.md`
- `results/analysis/experiment_readout.md`
- `results/experiments/cellar_phase6.json`
- `results/analysis/cellar_paper_metrics.json`
- `hadamard668/h1.py`
- `hadamard668/h2.py`
- `hadamard668/cellar.py`
- `research_paper.tex`

The novelty question has narrowed since the earlier review. The manuscript is no longer strongest when read as a positive CA-method paper. It is strongest when read as a narrow formal-and-empirical no-go for one exact literal-cellar encoding.

## Executive Call

- Positive solver novelty: fail.
- Broad `CA for Hadamard search` novelty: fail.
- Narrow encoding-specific no-go novelty: pass.

The current manuscript is materially distinct from prior art only in the following narrow sense:

- it formalizes one exact tail-panel / pushdown-style encoding tied to the actual order-`668` anchors;
- it proves that the matched static boundary-debt state is already sufficient for exact completion on that encoding;
- it shows empirically that the stack gives no surviving advantage on the solved same-template controls or on the recorded real-anchor panels;
- it retires that encoding cleanly.

That is a real contribution. It is not a new Hadamard construction, not a new general CA search paradigm, and not a validated new positive solver.

## Major-Claim Audit

### 1. Exact order-`668` anchors and precursor benchmark framing

- Closest paper or line of work:
  - Constantine and Constantine, *Convolution Numbers: The Cyclic Case* (2025).
  - Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025).
  - The heuristic Hadamard-search line around Suksmono's simulated annealing / simulated quantum annealing / quantum-search papers.
- Distinctness call:
  - weak but acceptable as context.
- Concrete overlap signal:
  - `research_paper.tex` now states explicitly that the exact `167/80` obstruction and the mod-`64` seed are imported anchors rather than new mathematical objects.
  - In `hadamard668/h1.py`, both `parallel_gain_ca` and `direct_greedy` are built from the same `candidate_swaps(...)` pool and the same distance objective; the method difference is move selection, not search space or verifier.
  - In `hadamard668/h2.py`, both methods are built from the same `candidate_operations(...)` pool, same modular objective, same phase schedule, and same move cap; again the main delta is move selection.
- Weak differentiation:
  - the paper does not discover a new reduction of order `668`;
  - the paper does not discover a new modular construction;
  - the precursor `H1/H2` packet is not a new heuristic family once the code is inspected.
- Missing gap evidence:
  - none if this section remains context only;
  - fatal if the manuscript starts selling `H1` or `H2` as surviving positive algorithmic contributions.

### 2. Literal cellar formalization as a canonical tail-panel automaton

- Closest paper or line of work:
  - Alur and Madhusudan, *Visibly Pushdown Languages* (2004), for the formal-language vocabulary.
  - Bright, Kotsireas, and Ganesh, *A SAT+CAS Method for Enumerating Williamson Matrices of Even Order* (2018), plus Williamson / Goethals--Seidel exact-search lines, for the collapse risk into symbolic pruning.
- Distinctness call:
  - pass, but only at the representation level.
- Concrete overlap signal:
  - `hadamard668/cellar.py` defines the cellar state as `boundary_debt_state(...)` plus a dyadic stack; the stack is not an independent oracle.
  - `panel_report(...)` evaluates both the static and stack signatures on the same exact completion records, same canonical prefixes, and same panel family. The only intended method difference is memory discipline.
- Weak differentiation:
  - the phrase `cellar automata` carries no novelty by itself;
  - the novelty lives in the exact executed encoding, not in the label or in general pushdown rhetoric.
- Missing gap evidence:
  - none for the narrow claim;
  - large if the paper tried to market this as a general new automata-theoretic method for Hadamard search.

### 3. Boundary-debt sufficiency and finite-state collapse on the implemented encoding

- Closest paper or line of work:
  - the visibly pushdown / finite-state automata line as formal backdrop;
  - structured exact-search lines as the nearest methodological neighbor once the stack is shown unnecessary.
- Distinctness call:
  - strongest surviving claim.
- Concrete overlap signal:
  - the code-level state in `hadamard668/cellar.py` matches the theorem objects directly: assigned pair vector, left and right boundary windows, remaining weight, and the augmented dyadic stack.
  - `results/literature/prior_art_gap.md` already anticipated that the cellar branch would survive only if stack state carried information unavailable to the matched static residual state. The deepen-pass paper now proves the opposite for the executed encoding.
- Weak differentiation:
  - this is not a new theorem about Hadamard matrices in general;
  - this is not a new theorem about visibly pushdown languages in general;
  - it is an encoding-specific sufficiency / collapse result.
- Missing gap evidence:
  - still no evidence about weaker static summaries;
  - still no evidence about other tokenizations;
  - still no evidence about cross-panel transfer or proof reuse.

This is acceptable because the paper now states those limits explicitly instead of implying a universal theorem.

### 4. Exact no-go on solved controls and real-anchor panels

- Closest paper or line of work:
  - Constantine and Constantine (2025) for the exact cyclic anchor.
  - Eliahou (2025) for the seed-derived anchor family.
  - Structured exact-search literature only as a collapse guardrail, not as direct duplicate prior art.
- Distinctness call:
  - pass as a narrow negative benchmark on the executed encoding.
- Concrete overlap signal:
  - `results/analysis/cellar_paper_metrics.json` shows the solved control family already saturates under the static summary:
    - tail `10`: exact frontier `11`, boundary frontier `11`, boundary groups `494 / 494`;
    - tail `12`: exact frontier `13`, boundary frontier `13`, boundary groups `2001 / 2001`;
    - tail `14`: exact frontier `15`, boundary frontier `15`, boundary groups `4367 / 4367`.
  - `results/experiments/cellar_phase6.json` shows the recorded real-anchor panels all collapse the same way:
    - four `H1`-best target panels and four seed projections;
    - exact completions `0`;
    - boundary frontier `0`;
    - cellar frontier `0`.
- Weak differentiation:
  - the empirical packet does not show a new solver endpoint;
  - it shows that one candidate representation has no surviving reason to continue.
- Missing gap evidence:
  - the real-anchor family is enough to retire the executed encoding, not enough to rule out all alternate representations;
  - the seed-projection family is diagnostic, not a proof that every future order-`668` reopen is dead.

### 5. What remains open

- Closest paper or line of work:
  - reserve symbolic / exact-search ideas closest to SAT+CAS and family-parameter search;
  - CA-design literature as the main blocker on broad novelty rhetoric.
- Distinctness call:
  - discussion only, not contribution-grade novelty.
- Concrete overlap signal:
  - `results/analysis/reserve_concept_audit.md` and `results/analysis/phase3_hypothesis_selection.md` still treat weaker summaries, proof reuse, and alternate tokenizations as reserve hypotheses only.
- Weak differentiation:
  - none of those branches has earned novelty credit yet;
  - they cannot inherit credit from the executed cellar no-go.
- Missing gap evidence:
  - no matched non-automaton comparator;
  - no solved same-template positive control in those alternate representations;
  - no demonstrated stateful gain beyond compression or pruning.

## Closest-Prior-Art Summary By Claim

- Imported exact objects:
  - closest papers are Constantine and Constantine (2025) and Eliahou (2025);
  - the manuscript is distinct only as a benchmark / retirement layer on their objects.
- Precursor local-search methods:
  - closest line is heuristic Hadamard search plus same-space direct local search;
  - the manuscript is not distinct as a new surviving optimizer because the matched baseline wins or ties.
- Literal cellar formalization:
  - closest lines are visibly pushdown automata and symbolic exact-search / pruning methods;
  - the manuscript is distinct because it defines and audits one concrete exact encoding instead of claiming a general stack-based solver.
- Main theorem:
  - closest line is finite-state / exact-pruning collapse rather than any existing Hadamard theorem;
  - the manuscript is distinct because the collapse proof is specific to the executed boundary-debt encoding.
- Empirical packet:
  - closest line is anchor-specific benchmark work on the exact `167/80` and mod-`64` order-`668` objects;
  - the manuscript is distinct as a negative result showing that the stack adds nothing on the executed panels.

## Novelty Illusions That Still Need To Stay Dead

- `Cellar automata` is not a novelty claim. It is only a branch label unless tied to the exact tail-panel encoding and the exact no-go result.
- The exact `167/80` obstruction and the mod-`64` seed are not new mathematical objects discovered here. They are imported anchors.
- `H1` and `H2` are not surviving new algorithm families. The repo code shows same-state, same-neighborhood, same-objective comparisons whose main delta is move selection.
- The paper does not show that pushdown memory is broadly useless for Hadamard search. It shows that one implemented encoding collapses to a finite residual state.
- The paper does not establish broad novelty for `CA meets combinatorial design`. That claim is already blocked by the CA-design survey and CA-based bent / semi-bent / Latin-square work.
- The paper does not become a new exact-search framework merely by using automata-theoretic vocabulary. Any future symbolic reopen still has to beat the SAT+CAS / Williamson / Goethals--Seidel collapse test.

The deepen pass mostly fixes these illusions. The remaining requirement is to keep the prose narrow.

## Missing Gap Evidence That Still Blocks Broader Claims

- No evidence that a weaker static summary would fail where the current boundary-debt state succeeds.
- No evidence that another tokenization would preserve the same collapse result.
- No evidence that proof reuse, transfer, or feedback survives once the current exact static frontier is already saturated.
- No evidence that any reserve symbolic branch beats a matched non-automaton comparator.
- No evidence that the precursor `H1/H2` packet supports a broader benchmark paper:
  - `H1` exact-hit rate remains `0`;
  - `H2` decisive real-seed evidence remains one degraded start.

These are not fatal for the current paper because the current paper no longer needs them. They become fatal immediately if the claim expands beyond the literal-cellar no-go.

## Final Assessment

`results/literature/prior_art_gap.md` already had the right structure: the literal cellar branch was differentiated enough to test, but it did not survive as a positive method claim under the executed encoding. The deepen-pass manuscript now aligns with that reality. It no longer tries to sell the branch as an untried solver family. It sells the stronger and more defensible result: the exact encoding collapses, the stack adds no surviving information channel, and the branch should be retired.

That is materially distinct from the named prior art because none of the cited Hadamard, CA-design, heuristic Hadamard-search, or automata papers already makes this exact encoding-specific retirement call. It remains narrow, but it is no longer a novelty illusion.

VERDICT: ACCEPT
