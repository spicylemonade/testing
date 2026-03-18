# Novelty Report

## Scope

This review-round-1 novelty check reads the current claim surface from:

- `research_paper.tex`
- `results/writeup/claims_table.md`
- `results/writeup/methods_brief.md`
- `results/branches/H1_defect_syndrome_ca_64m.md`
- `results/branches/H1_precheck.md`
- `results/branches/H2_gate.md`
- `results/branches/H3_gate.md`
- `results/experiments/order_668_64m/summary.md`
- `results/experiments/order_668_64m/summary.json`
- `results/experiments/controls/summary.md`
- `results/analysis/frontier_locality_scan.md`
- `results/analysis/prior_work_comparison.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/verification/benchmark_report.md`
- `results/verification/verification_summary.md`
- `hadamard_ca/h1_ca.py`
- `hadamard_ca/harness.py`

Primary named prior-art anchors available in-repo:

- Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025)
- Tsompanas et al., *Cellular Automata Applications in Shortest Path Problem* (2017)
- Suksmono, *Finding a Hadamard Matrix by Simulated Quantum Annealing* (2018)
- Suksmono and Minato, *Finding Hadamard Matrices by a Quantum Annealing Machine* (2019)
- Bright et al., *The SAT+CAS method for combinatorial search with applications to best matrices* (2019)
- Artacho, Borwein, and Tam, *Douglas-Rachford feasibility methods for matrix completion problems* (2013)
- Mariot et al., *Mutually orthogonal latin squares based on cellular automata* (2019)
- Gadouleau, Mariot, and Picek, *Bent Functions from Cellular Automata* (2020)

## Overall Assessment

The claimed contribution is only narrowly distinct from prior art.

What survives as materially distinct is not a new CA repair method for order `668`, and not a Hadamard-frontier advance. What survives is a seeded falsification attempt on top of Eliahou's 2025 order-`668` frontier object, run under one shared same-representation benchmark pack, with a direct negative result.

The strongest novelty constraint is Eliahou (2025), because the entire order-`668` branch inherits its seed, compact q/s representation, and defect profile from that paper. The strongest method-shape constraint is Tsompanas et al. (2017), because it is real prior art for CA as a local search or propagation mechanism. The strongest exactness ceiling is Bright et al. (2019), because it represents certificate-rich exact combinatorial search, which the present branch does not approach.

## Claim-By-Claim Assessment

### 1. Claim: operating on the order-668 frontier object is itself a materially novel contribution

- Closest paper or line of work:
  - Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025)
- Assessment:
  - Weakly distinct at best.
  - The repo does not contribute a new seed, a new modular construction, or a new exact order-`668` witness.
  - The distinct part is downstream experimentation on a published frontier object, not the frontier object itself.
- Concrete overlap signals:
  - `results/frontier/order_668_64m/seed_manifest.json` and `results/frontier/order_668_64m/source_excerpt.txt` show the canonical q/s seed and the `13` exceptional coefficients come directly from Eliahou's paper.
  - `results/writeup/claims_table.md` already limits the provenance claim to "anchored to the published 64-modular near-solution."
  - `results/experiments/order_668_64m/summary.json` shows no exact improvement over the published seed objective `13 / 2880 / 512`.
- Novelty verdict for this claim:
  - Distinct only as a seeded test harness on top of the 2025 frontier object.

### 2. Claim: `H1_defect_syndrome_ca_64m` is a materially distinct CA repair method

- Closest paper or line of work:
  - Tsompanas et al. (2017) for CA-as-search methodology
  - Suksmono (2018, 2019) for heuristic Hadamard search on the same broad objective class
- Assessment:
  - This is the weakest differentiation point.
  - H1 is distinct only as a narrowly framed seeded hypothesis, not as an earned method contribution after execution.
  - In the executed code path, the CA framing is weakened by exact global packet scoring over the whole packet basis before local coupling is applied.
- Concrete overlap signals:
  - `hadamard_ca/h1_ca.py` computes exact packet deltas in `_packet_delta_vector(...)` and scores all `334` packets in `_packet_pressures(...)` before `_coupled_pressure(...)` and `_select_packets(...)` add neighborhood and refractory behavior.
  - `results/branches/H1_precheck.md` explicitly warns that H1 collapses into generic local search if it becomes "exact per-packet move scoring over all `334` packets" with CA terms acting mainly as tie-breakers.
  - `results/analysis/frontier_locality_scan.md` reports `0` improving packets, `1` neutral packet, `333` worsening packets, and median changed-lag footprint `51 / 166`, which means the one-packet actuator basis is syntactically local but nonlocal in effect.
  - `results/verification/benchmark_report.md` notes there is no CA-off or scorer-only ablation, so the current pack does not isolate whether CA-specific coupling matters.
- Novelty verdict for this claim:
  - Weakly differentiated and not yet material.
  - The honest label is closer to "seeded local-search falsification scaffold with CA vocabulary" than to "new CA repair method."

### 3. Claim: H1 advances the exact order-668 frontier

- Closest paper or line of work:
  - Eliahou (2025) for the actual frontier object
  - Bright et al. (2019) for the exact-search / certification standard
- Assessment:
  - Not supported.
  - The executed branch contributes no exact witness, no proof artifact, and no best-objective improvement over the published seed.
- Concrete overlap signals:
  - `results/experiments/order_668_64m/summary.md` records `exact_hit = false` for every saved method.
  - The same artifact reports H1 best objective `13 / 2880 / 512`, identical to the seed.
  - H1's terminal restarts move to `33 / 2368 / 384`, `40 / 2356 / 408`, and `23 / 2216 / 384`, which means lower magnitude only after support diffusion beyond the seed support `13`.
  - `results/verification/verification_summary.md` already requires exactness statements to remain explicitly negative.
- Novelty verdict for this claim:
  - No material distinctness as a frontier advance.
  - The contribution is negative evidence about one failed repair branch, not progress on the existence question.

### 4. Claim: the saved benchmark supports a broader method or competitiveness claim

- Closest paper or line of work:
  - Suksmono (2018, 2019)
  - Bright et al. (2019)
  - Artacho et al. (2013) as a non-CA matrix-feasibility comparator
- Assessment:
  - Not supported.
  - The saved pack is fair enough for internal branch elimination, but too narrow for any broader literature-level method claim.
- Concrete overlap signals:
  - `results/verification/benchmark_report.md` limits the current evidence to one canonical seed, one RNG seed, budget `80`, and a same-representation roster.
  - Executed restart coverage is unequal: H1 and stochastic hillclimb complete `3 / 3`, while greedy, tabu, and simulated annealing complete `1 / 3`.
  - The only solved controls are the tiny deterministic `n = 5` and `n = 7` q0-flip cases.
  - `results/writeup/claims_table.md` already states the benchmark is not evidence of competitiveness with annealing or SAT+CAS literature.
- Novelty verdict for this claim:
  - The benchmark can kill H1 continuation.
  - It cannot support a materially distinct broad method claim.

### 5. Claim: `H2_lag_space_ca_167` is the next materially distinct novelty-bearing branch

- Closest paper or line of work:
  - Structured-family Hadamard search: Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant lines
- Assessment:
  - Unproven.
  - H2 is only potentially distinct if it stays a lag-space locality experiment and survives the family-leakage audit.
- Concrete overlap signals:
  - `results/branches/H2_gate.md` explicitly says H2 must be rejected or relabeled if it collapses into Williamson, Turyn, Goethals-Seidel, cocyclic, or block-circulant search.
  - `results/literature/prior_art_gap.md` already frames H2 as a possible optimizer-over-known-family failure mode.
  - `results/verification/verification_summary.md` keeps H2 blocked until a family-leakage audit artifact exists.
- Novelty verdict for this claim:
  - Hypothetical only.
  - No material distinctness has been earned yet.

### 6. Claim: `H3_spacetime_row_emission_ca` would open a fresh CA direction for Hadamard search

- Closest paper or line of work:
  - CA-based combinatorial-design construction, as represented here by:
    - Mariot et al. (2019), mutually orthogonal Latin squares from CA
    - Gadouleau, Mariot, and Picek (2020), bent functions from CA
- Assessment:
  - High overlap risk.
  - H3 is not fresh by default; it is the branch most exposed to direct CA-construction prior art.
- Concrete overlap signals:
  - `results/branches/H3_gate.md` warns against overlap with linear bipermutive CA, orthogonal-array / Latin-square pipelines, and bent-function / MUB-style constructive regimes.
  - `research_paper.tex` already cites `mariot2019_mols` and `gadouleau2020` to rule out any broad claim that CA are new in combinatorial design.
  - `results/swarm/director_brief.md` and `results/swarm/explorer_alignment_note.md` both keep H3 reserve-only because it is novelty-fragile.
- Novelty verdict for this claim:
  - Not materially distinct on the present evidence.
  - Reserve-only is the correct status.

## Strongest Novelty Illusions

- "Cellular automata are new for Hadamard matrices."
  - Not defensible against Tsompanas-style CA-as-search work and CA-based design-generation work such as `mariot2019_mols` and `gadouleau2020`.

- "H1 is genuinely local because it uses lag masks and packet neighborhoods."
  - Weak.
  - The code still performs exact all-packets scoring first, and the locality scan shows large lag footprints per one-packet move.

- "Lower `l1` or `max_abs` means H1 is advancing the frontier."
  - False in the current run.
  - H1 lowers those values only by diffusing support above the seed support and never improves the seed's lexicographic objective.

- "Using the 2025 frontier seed is itself a new method contribution."
  - Weak.
  - The seed belongs to Eliahou (2025); the repo contributes only a seeded test and falsification scaffold on top of it.

- "A representation change automatically creates novelty."
  - False.
  - H2 can collapse into optimizer-over-known-family, and H3 can collapse into known CA-construction lines.

- "The matched pilot shows broader method competitiveness."
  - False.
  - The pack supports branch elimination, not literature-scale comparison.

## Missing Gap Evidence

- CA-mechanism ablation is missing.
  - There is no direct comparison of full H1 against zero-coupling, zero-refractory, scorer-only, or fallback-disabled variants.
  - Without that, the CA-specific mechanism claim is unearned.

- Actuator-basis evidence is missing.
  - The one-packet basis looks frozen, but there is no matched alternative-basis experiment proving the failure is representation-level rather than rule-level.

- H2 family-leakage evidence is missing.
  - The guardrail exists, but no executed audit artifact exists yet.

- H3 overlap evidence is under-surfaced in the written watchlist.
  - The strongest H3 prior-art pressure comes from CA-design construction, but `results/literature/prior_art_watchlist.md` is still dominated by lexical noise rather than those direct overlap lines.

- Robustness evidence is missing.
  - The novelty case rests on one frontier seed, one RNG seed, and tiny solved controls.
  - There is no seed-robustness or perturbation evidence strong enough to support a wider method claim.

- Exactness / certification evidence is missing.
  - There is no exact order-`668` witness and no proof artifact, so the work remains far from the exact-search standard represented by Bright et al. (2019).

## Surviving Contribution

The only contribution that remains materially distinct after the closest-prior-art comparison is:

- a seeded CA falsification attempt on the published `64`-modular order-`668` frontier object, under matched same-representation non-CA controls, with a direct negative result

That is a real contribution because it closes off one concrete branch honestly. It is not a distinct CA repair method contribution, not a frontier advance, and not a broad CA-for-Hadamard novelty claim.

VERDICT: REVISE
