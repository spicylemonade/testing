# Novelty Report

## Scope

This report evaluates the post-research novelty status of:

- the executed branch `H1_defect_syndrome_ca_64m`
- the gated follow-on branch `H2_lag_space_ca_167`
- the reserve branch `H3_spacetime_row_emission_ca`

Primary repo evidence:

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/writeup/claims_table.md`
- `results/writeup/methods_brief.md`
- `results/branches/H1_defect_syndrome_ca_64m.md`
- `results/branches/H2_gate.md`
- `results/branches/H3_gate.md`
- `results/experiments/order_668_64m/summary.md`
- `results/analysis/prior_work_comparison.md`
- `results/verification/benchmark_report.md`
- `results/verification/citation_audit.md`
- `hadamard_ca/h1_ca.py`

Primary named papers already in-repo:

- Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025)
- Tsompanas et al., *Cellular Automata Applications in Shortest Path Problem* (2017)
- Suksmono, *Finding a Hadamard Matrix by Simulated Quantum Annealing* (2018)
- Suksmono and Minato, *Finding Hadamard Matrices by a Quantum Annealing Machine* (2019)
- Bright et al., *The SAT+CAS method for combinatorial search with applications to best matrices* (2019)

Direct CA/design overlap found in the literature spot-check but not yet represented in `sources.bib`:

- Mariot et al., *Mutually Orthogonal Latin Squares based on Cellular Automata* (2020)
- Gadouleau, Mariot, and Picek, *Bent Functions from Cellular Automata* (2020)
- Garcia Sandoval et al., *Cellular Automata-Based Methods for the Construction of Mutually Unbiased Bases* (2025)
- Manzoni, Mariot, and Menara, *Combinatorial designs and cellular automata: A survey* (recent survey)

## Claim-by-Claim Assessment

### 1. Claim: the work is materially distinct because it operates on the order-668 frontier object

- Closest paper or line of work:
  - Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025)
- Assessment:
  - Only weakly distinct, and only as a downstream experiment on top of Eliahou's object.
  - It is not distinct as a new frontier construction, a new seed, or a new exact order-668 witness.
- Overlap signals:
  - `results/writeup/claims_table.md` already limits this to seed provenance.
  - `results/verification/benchmark_report.md` and `results/writeup/methods_brief.md` state that every order-668 run uses the same frontier seed and the same compact q/s representation.
  - `results/experiments/order_668_64m/summary.md` shows no exact improvement over that seed.

### 2. Claim: H1 is a materially distinct cellular-automaton repair method

- Closest paper or line of work:
  - Tsompanas et al. (2017) for CA-as-search method shape
  - Suksmono (2018, 2019) for heuristic Hadamard search on the same broad objective class
- Assessment:
  - This is the main weak point.
  - H1 is distinct only as a narrowly framed seeded CA hypothesis, not as a materially differentiated method after execution.
  - In the executed branch, the distinction from generic local heuristic search is weak.
- Overlap signals:
  - `hadamard_ca/h1_ca.py` computes exact packet deltas in `_packet_delta_vector` and then scores every packet by updating the full coefficient vector inside `_packet_pressures` before any neighborhood smoothing happens.
  - `results/analysis/prior_work_comparison.md` already states that H1 is "still driven by full packetwise defect deltas."
  - `results/experiments/order_668_64m/summary.md` shows H1 never improves the seed objective and diffuses support on every frontier restart.
  - `results/verification/citation_audit.md` already warns that broad "automata are untried here" wording is unsupported.

### 3. Claim: H1 advances the exact order-668 frontier

- Closest paper or line of work:
  - Eliahou (2025) for the actual frontier object
  - Bright et al. (2019) for the exact-search / certification standard
- Assessment:
  - Not supported.
  - The executed work is not materially distinct as a frontier advance because it contributes no exact witness, no exact seed improvement, and no proof artifact.
- Overlap signals:
  - `results/experiments/order_668_64m/summary.md` records `exact_hit = false` for every method.
  - H1's best frontier state remains the seed objective `13/2880/512`.
  - `results/verification/verification_summary.md` and `results/writeup/claims_table.md` already frame the exactness statement as negative.

### 4. Claim: the benchmark supports a broader literature-level method claim

- Closest paper or line of work:
  - Suksmono (2018, 2019)
  - Bright et al. (2019)
  - Artacho, Borwein, and Tam (2013)
- Assessment:
  - Not supported.
  - The benchmark is fair enough for branch elimination, but it is too narrow to support a broader competitiveness or method-level superiority claim.
- Overlap signals:
  - `results/verification/benchmark_report.md` limits the pilot to one shared seed, one representation, budget `80`, and restart count `3`.
  - `results/writeup/claims_table.md` already says the benchmark is not evidence of competitiveness with annealing or SAT+CAS literature.

### 5. Claim: H2 is the next materially distinct novelty-bearing branch

- Closest paper or line of work:
  - Goethals-Seidel / Williamson / Turyn / cocyclic / block-circulant structured-family search
- Assessment:
  - Unproven.
  - H2 is only potentially distinct if it survives the family-leakage audit; right now it is a gated backup, not an earned contribution.
- Overlap signals:
  - `results/branches/H2_gate.md` already states that H2 must be rejected or relabeled if it re-enters any of those known families.
  - `results/literature/prior_art_gap.md` and `results/swarm/gap_map.md` already warn that H2 can collapse into optimizer-over-known-family.

### 6. Claim: H3 would open a fresh CA direction for Hadamard search

- Closest paper or line of work:
  - CA-based combinatorial-design construction, especially:
    - Mariot et al. (2020) on CA-generated mutually orthogonal Latin squares
    - Gadouleau, Mariot, and Picek (2020) on bent functions and Hadamard-adjacent constructions from CA
    - Garcia Sandoval et al. (2025) on CA-based mutually unbiased bases
- Assessment:
  - High overlap risk.
  - H3 is not fresh by default; it sits close to existing CA-construction literature and should remain reserve-only.
- Overlap signals:
  - `results/branches/H3_gate.md` already warns against direct overlap with linear bipermutive CA, orthogonal-array / Latin-square pipelines, and bent-function / MUB constructive regimes.
  - The current in-repo watchlist under-covers this overlap line, which makes H3 easier to overclaim than H1.

## Strongest Novelty Illusions

- "Cellular automata are new for Hadamard matrices."
  - This is not defensible. The safer claim is much narrower: CA are not established here as a successful exact-search repair dynamic for the specific order-668 frontier object.

- "H1 is genuinely local because it uses lag masks and packet neighborhoods."
  - Weak. The implementation still uses globally informed packet scoring before local coupling. That makes H1 look closer to globally scored local search with CA-style scheduling than to a materially new CA method.

- "Lower `l1` or `max_abs` on a restart means real frontier progress."
  - False in this pilot. H1 lowers those quantities only by diffusing support above the seed support, and it never improves the seed's lexicographic objective.

- "Operating on the new 2025 frontier seed is itself a method contribution."
  - Weak. The seed is the frontier contribution; the repo contributes only a seeded optimizer / falsification scaffold on top of it.

- "A representation change automatically creates novelty."
  - False. H2 can collapse into known structured-family search, and H3 can collapse into known CA-construction work.

- "The matched pilot shows competitiveness with the broader Hadamard-search literature."
  - False. The saved pilot is good enough to reject H1 continuation, not to compare against literature-scale annealing or certificate-rich exact search.

## Missing Gap Evidence

- Direct bibliography gap:
  - The novelty pack leans too heavily on `tsompanas2017` plus lexical false positives.
  - It still lacks named CA/design overlap papers in `sources.bib` and in the written watchlist, especially for the H3 risk surface.

- Locality ablation gap:
  - There is no explicit ablation showing that neighborhood coupling, rather than global packet scoring, is the operative source of H1 behavior.
  - Without that, H1 can be relabeled as globally scored local search.

- Gap-to-claim mismatch:
  - The highest-risk overlap for H3 is direct CA-construction literature, but the current watchlist is dominated by irrelevant `automata` matches instead.

- Family-leakage gap:
  - H2 has a clear guardrail document, but no executed family-leakage audit artifact yet.

- Generalization gap:
  - The novelty case rests on one frontier seed plus toy solved controls.
  - There is no evidence of transfer across alternate frontier seeds, held-out near-solutions, or varied compressed representations.

- Certification gap:
  - There is no exact witness, no proof artifact, and no reason yet to claim parity with exact-search literature except as a ceiling the current work does not reach.

- Frontier-status gap:
  - The repo's novelty framing is still anchored almost entirely to Eliahou (2025).
  - Before any broader paper claim, the exact order-668 frontier should be refreshed against current primary sources.

## Surviving Contribution

The only contribution that remains materially distinct after the first frontier batch is:

- a seeded CA falsification attempt on the published 64-modular order-668 frontier object, under matched non-CA controls, with a negative result at the first continuation gate

Anything stronger than that currently reads as novelty inflation.

## Recommendation

- Rewrite H1 as a negative result / falsification scaffold, not as a new CA repair method.
- Open H2 only if the work is willing to relabel any family leakage as optimizer-over-known-family.
- Keep H3 reserve-only until the missing CA-construction bibliography is added and cleared explicitly.

VERDICT: REVISE
