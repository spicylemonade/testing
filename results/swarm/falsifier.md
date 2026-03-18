# Falsifier Memo: Hadamard 668 via "cellar"/cellular automata

Scope:
- Required reads completed: `results/research_context.md`, `results/literature/prior_art_watchlist.md`, and `results/literature/prior_art_gap.md`.
- Repo-grounded evidence also reviewed from `results/experiments/order_668_64m/summary.json`, `results/analysis/frontier_locality_scan.md`, `results/branches/H1_precheck.md`, `results/branches/H1_frontier_sensitivity_probe.json`, `results/verification/benchmark_report.md`, `results/verification/verification_summary.md`, and `hadamard_ca/h1_ca.py`.
- Budget note: this memo does not propose fresh solver branches. It only lists the easiest ways the current CA-shaped hypotheses fail, rehash prior art, or collapse under missing controls.

Terminology note:
- `cellar automata` does not surface here as a recognized Hadamard-search family. Treat it as `cellular automata` or correct it explicitly. Leaving the phrase uncorrected is an avoidable credibility hit.

## Executive Kill Shot

- The order-`668` frontier object is already supplied by Eliahou's 2025 `64`-modular near-solution. The repo does not contribute a new seed, a new defect profile, or a new exact witness.
- The repo has already run the strongest obvious CA hypothesis, `H1_defect_syndrome_ca_64m`, on that published frontier seed.
- Outcome: no exact hit, no improvement over the seed objective `13 / 2880 / 512`, and every H1 restart exceeds the seed support `13`.
- The easiest external accusation is therefore not "CA can never help." It is: this exact H1 implementation is a seed-specific global packet scorer with local smoothing, run on top of a published near-solution, and it failed the first matched kill test.

## Easiest Failure Or Rehash Paths

### 1. "This is new because CA has not been tried here" dies immediately

Broad CA novelty is already occupied by multiple orthogonality-adjacent branches:

- `Constructing Orthogonal Latin Squares from Linear Cellular Automata` (2016, `arXiv:1610.00139`)
- `Mutually orthogonal latin squares based on cellular automata` (2019, DOI `10.1007/s10623-019-00689-8`)
- `Bent Functions from Cellular Automata` (2020, `IACR ePrint 2020/1272`)
- `Building Correlation Immune Functions from Sets of Mutually Orthogonal Cellular Automata` (2023, DOI `10.1007/978-3-031-42250-8_11`)
- `Self-Orthogonal Cellular Automata` (2025, `arXiv:2504.09173`)
- `Cellular Automata-Based Methods for the Construction of Mutually Unbiased Bases` (2025, DOI `10.3390/math13162600`)
- `Combinatorial Designs and Cellular Automata: A Survey` (2026, DOI `10.1016/j.dam.2025.10.014`)

That cluster already covers orthogonal Latin squares, MOLS, bent/Hadamard-form constructions, self-orthogonality, OA-style pipelines, and MUB construction. So the only defensible novelty claim is narrow:

- CA as one seeded repair or falsification heuristic on the specific published order-`668` frontier object.

### 2. H1 is easy to relabel as globally rescored local search, not a distinct CA method

The saved implementation makes this accusation easy:

- `hadamard_ca/h1_ca.py` computes exact deltas for all `334` packets in `_packet_pressures(...)`.
- Only after that dense rescoring step does it apply local coupling and refractory modifiers.
- The saved frontier config sets `max_active_packets = 1`.
- `fallback_best_packet = true` means the method can still fire the globally best positive-pressure packet when no local winner clears threshold.

The branch's own precheck already states the failure mode plainly: at that point H1 is closer to greedy/tabu-style move evaluation with CA vocabulary than to a distinct CA repair dynamic.

Fast invalidator:
- run matched CA-off ablations:
  - zero coupling
  - zero refractory
  - scorer-only / fallback disabled
- If full H1 does not beat those variants, the CA-mechanism claim is dead.

### 3. The supposed locality is already broken on the actual frontier representative

The saved one-packet scan is brutal:

- improving packets: `0`
- neutral packets: `1`
- worsening packets: `333`
- median changed-lag footprint per one-packet move: `51` of `166`

So the current packet basis is local in syntax but nonlocal in effect.

The saved sensitivity probe is equally hostile:

- eight small parameter variants
- all stay pinned to the seed objective `13 / 2880 / 512`

Fast accusation:
- the current frontier failure is basis-specific and representative-specific, not evidence that any CA principle has been validated or invalidated cleanly.

### 4. The pilot is fair in coordinate system, not in work accounting

The same-coordinate comparison is real:

- same q/s seed interface
- same published frontier seed
- same nominal `evaluation_budget = 80`
- same requested `restart_count = 3`
- same `restart_packet_flips = 2`

But equal-budget language is still vulnerable because H1's internal work is not charged the same way:

- H1 run: `objective_evaluations = 32`, `ca_field_evaluations = 10354`, `wall_seconds = 2.129`
- greedy run: `objective_evaluations = 80`, `wall_seconds = 0.079`
- tabu run: `objective_evaluations = 80`, `wall_seconds = 0.090`
- simulated annealing run: `objective_evaluations = 80`, `wall_seconds = 0.144`

Fast accusation:
- accepted-state objective counts are not a fair work metric for H1 because the method rescans the whole packet basis at each view.

### 5. The branch can overclaim from approximate movement while getting farther from exactness

H1's saved frontier batch is negative in the most damaging way:

- best objective stays equal to the seed objective `13 / 2880 / 512`
- restart terminals move to:
  - `33 / 2368 / 384`
  - `40 / 2356 / 408`
  - `23 / 2216 / 384`
- every restart exceeds the seed support `13`
- exact hit rate stays zero

So H1 only lowers `l1` or `max_abs` by diffusing support beyond the seed support.

Fast accusation:
- this is approximate defect reshaping, not progress on order `668`.

### 6. H2 is primed to collapse into known structured-family search

The repo already has the right warning language, and the falsifier view is harsher:

- H2 must not collapse into Williamson, Turyn, Goethals-Seidel, cocyclic, or block-circulant structure.
- That risk is especially high because the order is `4p` with `p = 167 ≡ 3 mod 4`, where cocyclic order-`4p` structure is already tightly constrained in the literature.
- The repo already uses a fixed Goethals-Seidel lift, so a lag-space success can easily turn into "another optimizer over a known family."

Fast accusation:
- if H2 only works after hidden family structure enters, the structure gets the novelty credit, not the CA.

### 7. H3 is the cleanest direct-overlap trap

Generative spacetime CA is the branch most likely to be accused of rehashing prior art:

- linear or bipermutive CA construction lines
- orthogonal-array and Latin-square pipelines
- bent-function and MUB constructive regimes
- compact rule-table search in already-familiar CA territory

Fast accusation:
- if H3 only gains traction in those regimes, it is not a fresh order-`668` direction. It is a replay of known CA construction machinery in a new sales pitch.

## Missing Controls That Would Invalidate Weak Claims

### 1. CA-off mechanism controls

Still missing:

- zero coupling
- zero refractory
- scorer-only
- fallback disabled

Without those, H1 can be criticized as under-identified local search rather than a CA method.

### 2. Equal-work accounting

Still missing:

- a metric that charges H1's dense rescoring work
- or an explicitly wall-clock-normalized comparison

Without that, any budget-matched competitiveness language is weak.

### 3. Equal executed restart coverage

Current frontier batch:

- H1: `3 / 3`
- stochastic hillclimb: `3 / 3`
- greedy: `1 / 3`
- tabu: `1 / 3`
- simulated annealing: `1 / 3`

This is good enough to kill H1 internally.
It is not good enough for restart-robust method ordering.

### 4. Held-out tuning control

Still missing:

- parameter choice frozen on a held-out control family before frontier evaluation

Right now frontier sensitivity observations also shape the H1 mechanism story.

### 5. Frontier perturbation and symmetry control

Still missing:

- nearby q/s perturbations around the canonical frontier seed
- symmetry-equivalent representatives
- stronger equivalence handling than the current q/s global sign-flip fingerprint

Right now the locality story is about one chosen representative.

### 6. Alternative actuator-basis control

Still missing:

- a matched experiment with a different packet library under the same harness

Current evidence only says the present one-packet basis looks frozen on the current representative.

### 7. Family-leakage audit for H2 and H3

Still missing:

- an executed, saved audit that rejects or relabels successful runs when they fall into known families

Without that, H2 and H3 are exposed to optimizer-over-known-family criticism.

### 8. Exactness or certificate control

Still missing:

- an exact order-`668` witness
- or any certificate-grade exact-search artifact

Without that, the work stays in heuristic branch elimination, not exact Hadamard search.

## Benchmark Traps

- `Toy-order trap`: length-`5` and length-`7` q0-flip controls mostly prove harness sanity, not frontier relevance.
- `Single-seed trap`: one frontier representative, one RNG seed, one restart perturbation setting.
- `Global-information trap`: the method is sold as CA while every view rescans the whole packet basis exactly.
- `Work-metric trap`: accepted-state objective counts are compared against baseline candidate-evaluation counts.
- `Support-diffusion trap`: lower `l1` or `max_abs` can look better while support and exactness get worse.
- `Restart-cherry-picking trap`: requested restarts are matched, executed restarts are not.
- `Equivalence trap`: packet neighborhoods depend on raw index placement of the chosen q/s representative.
- `Literature-scale trap`: a same-coordinate internal kill test is not a publication-grade benchmark against annealing or SAT+CAS lines.

## Literature Branches That Invalidate Weak Claims

### Frontier anchor

- Shalom Eliahou, `A 64-Modular Hadamard Matrix of Order 668` (2025)

This is the true frontier source.
Any CA work on the q/s seed or its defect pattern is downstream of this paper.

### Direct Hadamard-search baselines

- A. B. Suksmono, `Finding a Hadamard Matrix by Simulated Quantum Annealing` (2018)
- A. B. Suksmono and Y. Minato, `Finding Hadamard Matrices by a Quantum Annealing Machine` (2019)
- A. B. Suksmono, `A quantum approximate optimization method for finding Hadamard matrices` (2024)

These lines already occupy the "heuristic optimization for Hadamard search" slot.
If the CA branch is just another optimizer over the same broad objective, novelty is weak.

### Exact-search or certification ceiling

- Curtis Bright et al., `A SAT+CAS Method for Enumerating Williamson Matrices of Even Order` (2018)
- Curtis Bright et al., `The SAT+CAS method for combinatorial search with applications to best matrices` (2019)

These are the exact-search standard.
Without an exact witness or proof artifact, the current CA work is nowhere near that ceiling.

### Structured-family collapse risk

- Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant lines
- cocyclic order-`4p` restrictions, especially for `p ≡ 3 mod 4`

If CA only works inside those envelopes, the structure gets the credit.

### Generic CA-as-search prior art

- Tsompanas et al., `Cellular Automata Applications in Shortest Path Problem` (2017)

This is enough to kill any broad claim that CA as local search or propagation is new.

### CA-to-orthogonality or Hadamard-adjacent construction line

- `Constructing Orthogonal Latin Squares from Linear Cellular Automata` (2016)
- `Mutually orthogonal latin squares based on cellular automata` (2019)
- `Bent Functions from Cellular Automata` (2020)
- `Building Correlation Immune Functions from Sets of Mutually Orthogonal Cellular Automata` (2023)
- `Self-Orthogonal Cellular Automata` (2025)
- `Cellular Automata-Based Methods for the Construction of Mutually Unbiased Bases` (2025)
- `Combinatorial Designs and Cellular Automata: A Survey` (2026)

This entire cluster invalidates any broad "CA plus orthogonality or combinatorial design is new" narrative.

## Terminology And Credibility Risks

- `cellar automata` is not the right label for the literature branch under discussion.
- `canonical frontier seed` must be used carefully: canonical for this run package is not the same as canonical over the full equivalence class.
- `near-exact` or `better defect statistics` must never be allowed to drift into `almost solved order 668`.

## Adversarial Decision Rules

- Kill any broad CA novelty claim unless it is narrowed to seeded repair or falsification on the published order-`668` frontier object.
- Kill any CA-mechanism claim unless full H1 beats zero-coupling, zero-refractory, and scorer-only variants under equal-work accounting.
- Kill any order-`668` progress claim unless an exact Hadamard witness is produced.
- Relabel any H2 or H3 success as optimizer-over-known-family if it enters structured-family or LBCA-style constructive regimes.
- Do not spend new solver budget on fresh CA branches until the missing controls above are satisfied.

## Bottom Line

The easiest way this program fails is not that CA are useless in general.
It is that the current order-`668` proposal is accused of rehashing two existing things at once:

1. a published frontier seed from Eliahou 2025, and
2. a long-standing CA-to-orthogonality literature covering Latin squares, MOLS, bent/Hadamard forms, self-orthogonal CA, OA-style pipelines, and MUB construction.

The repo's saved evidence already supports one narrow negative result:

- `H1_defect_syndrome_ca_64m` is a seed-matched falsification attempt that did not beat the frontier seed and did not isolate a CA-specific advantage.

Anything broader is currently easier to falsify than to defend.
