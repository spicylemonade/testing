# Novelty Report

Snapshot date: 2026-03-18 UTC
Review round: review_round_1

## Executive Judgment

The current paper is not materially distinct from known prior art at the mathematical-result level. The repo contains no new arithmetic-Kakeya witness, no verified score improvement toward `<= 1.675`, no exact verifier-backed benchmark block, and no theorem beyond target formalization plus internal decoder-contract claims.

The only potentially distinct contribution is narrower: a verifier-coupled, no-repair, witness-faithful cellular-automata search design for the exact six-line witness object `(X,G,R,T)`. Even that distinction is design-level only. The code artifacts do not implement an exact witness verifier or a CA experiment runner, and the phase-4 reports record `0` exact decodes and `0` verified witnesses.

The safest framing is therefore not "novel CA method for arithmetic Kakeya." It is "audited design and blocker report for a verifier-coupled search program." That is a real but modest distinction.

## Real Prior-Art Boundary

- Mathematical direct pressure: Katz-Tao (1999), Green-Ruzsa (2017), and Tao (2025). These papers define the target object, equivalent-form warning signs, and low-complexity objections that any genuine progress must clear.
- Mathematical adjacent pressure: Cowen-Breen et al. (2020), Pohoata-Zakharov (2024), and Hickman-Wright (2018). These papers show how easy it is to drift into nearby pattern problems, generalized formulations, or modular shadows without improving the stated forcing-pair task.
- Methodological direct pressure: Novikov et al. (2025) and Georgiev et al. (2025). These remove any novelty claim based only on "an automated system searched a mathematical object."
- Methodological adjacent pressure: Bond-Levine (2013, 2014), Dennunzio-Formenti-Margara (2023), and Faldor-Cully (2024). These cover local symbolic dynamics, additive/group CA structure, and CA-search or quality-diversity exploration.
- False-overlap cleanup: the malformed watchlist entries in `results/literature/prior_art_watchlist.md` are token-collision junk, not real neighbors.
- Search result boundary: the local literature pass plus targeted web search did not surface a paper directly using cellular automata to search arithmetic-Kakeya constructible witnesses. That helps only a little. Absence of a direct title match does not establish material novelty if the work still overlaps broader automated-discovery and CA-search lines.

## Closest Prior Art By Major Claim

| Manuscript claim | Closest paper or line of work | Concrete overlap signal | What is actually different | Novelty judgment |
| --- | --- | --- | --- | --- |
| Contribution 1: formalize `H1` as a CA search program over the original six-line witness object instead of a proxy task. | Katz-Tao (1999); Green-Ruzsa (2017); Cowen-Breen et al. (2020); Pohoata-Zakharov (2024) | Same arithmetic-Kakeya target object, or nearby formulations that can easily be mistaken for progress on the forcing-pair task. | `H1` keeps the state space aligned with the six-line witness grammar and rejects drift to proxy pattern tasks. | This is target-faithfulness, not material novelty. Without a new witness, score improvement, or transfer argument, it is an admissibility condition rather than a contribution that clears prior art. |
| Major method claim: `H1` is a proof-carrying, stage-indexed symbolic CA rather than generic search over serialized witnesses. | Novikov et al. (2025); Georgiev et al. (2025); Faldor-Cully (2024); Dennunzio-Formenti-Margara (2023) | Automated mathematical search, CA-local-rule exploration, and rich finite-state search spaces already exist. The repo itself admits that "we used a CA" is not enough. | `H1` uses witness-aware typed fibers, a fixed decoder, and a no-repair rule. | Partial design differentiation only. No matched exact comparison against non-CA or decoder-matched search was run, so there is no evidence that the CA family contributes anything beyond a constrained proposal language. |
| Contribution 2: the paper "proves" system-level correctness claims about accepted states, no-repair score faithfulness, and confounder-excluding controls. | Specification-level decoder/evaluator correctness as a line of work; nearest cited comparators are evaluator-centered search systems and local symbolic-processing analogies in Bond-Levine (2013, 2014) | The Section 5 theorems are immediate consequences of Algorithm 1 and the lane-gate definitions in the repo. They certify the author's own contract, not a new external result. | The manuscript writes these contracts as formal lemmas and theorems. | Weak differentiation. These are internal consistency statements, not evidence of a new mathematical or methodological gap over prior work. Treat them as hygiene, not novelty. |
| Contribution 3: the negative empirical outcome and pivot to verifier recovery are methodologically significant. | Novikov et al. (2025); Georgiev et al. (2025); benchmark-audit and falsifier practice in the repo | Evaluator-backed evidence discipline and honest negative-result reporting are part of normal rigorous search practice, not a new result class. | The repo explicitly refuses to substitute proxy metrics when the exact verifier is missing. | Good practice, not material novelty by itself. The distinctive part is the strictness of the refusal, but there is no comparative evidence that this protocol changes outcomes relative to prior systems. |
| Major defense claim: the planned control suite clears bounded-slope, modular-mirage, decoder-leakage, and geometry-only confounders. | Tao (2025); Green-Ruzsa (2017); Hickman-Wright (2018); `results/swarm/falsifier.md` | These are exactly the objections already identified in the literature and falsifier memo. | The repo encodes them as explicit kill gates and matched-baseline requirements. | Not cleared. Planned controls are not gap evidence until they run. Right now this is a well-specified defense plan, not demonstrated differentiation. |
| Contribution 4: the ConceptEvolve narrowing process and promoted bridge set add novelty. | AlphaEvolve-style discovery workflows; Bond-Levine bridge language; uncited SAT/egraph-style bridge ideas | Bridge generation and narrowing are generic discovery mechanics, and several promoted bridges remain uncited or unevaluated. | The retained bridges are filtered through the no-repair exact-decoder discipline. | Hypothesis inventory only. The bridge list is useful for restart triage, but it is not evidence of distinction from prior art. |

## Strongest Novelty Illusions

### 1. Witness-faithfulness mistaken for novelty

Staying on the original Katz-Tao witness object is necessary, but it does not itself beat Katz-Tao, Green-Ruzsa, Cowen-Breen et al., or Pohoata-Zakharov. It only shows that the search did not drift into an easier neighboring formulation.

### 2. "CA" mistaken for methodological separation

The nearest methodological pressure is not a direct arithmetic-Kakeya CA paper. It is the broader combination of CA-search literature and automated-discovery systems. Without exact baseline wins, calling the generator a cellular automaton does not separate it from existing CA or agentic-search practice.

### 3. Definitions-level theorems mistaken for research contribution

The Section 5 results are mostly unpackings of the manuscript's own decoder and gate definitions. They do not solve a recognized open problem in CA theory, automated discovery, or arithmetic Kakeya. Presenting them as formal theorems may create a novelty aura larger than the substance.

### 4. Planned controls mistaken for cleared objections

The paper repeatedly invokes label shuffling, decoder-matched baselines, held-out geometries, and complexity sweeps as if they already separate the method from Tao-style bounded-slope or Hickman-Wright-style modular concerns. They do not. The repo's own experiment artifacts record that none of these controls executed.

### 5. Negative-result honesty mistaken for new methodology

The refusal to overclaim is important and should stay. But it is better described as good scientific governance than as a novel search method. The paper should not lean on rigor alone as if rigor itself creates a strong novelty gap over AlphaEvolve-style or other evaluator-centered systems.

### 6. No direct title match mistaken for material novelty

A targeted search failing to find "cellular automata for arithmetic Kakeya witness search" is useful negative evidence, but only weakly so. The stronger overlaps are structural: automated search over mathematical objects, local-dynamics search, and exact-target drift already have well-populated prior art.

## Missing Gap Evidence

1. No exact verifier or shared exact decoder implementation exists in the code artifacts. The visible scripts are orchestration and literature utilities, not witness-verification code.
2. No exact comparison was run against Random Local Search, Whole-Witness Mutation, or Decoder-Matched Search, so the CA-specific claim is unmeasured.
3. No label-shuffle, held-out-geometry, held-out-`X`, or complexity-sweep control executed, so the paper has not actually cleared the objections raised by Tao (2025), Green-Ruzsa (2017), Hickman-Wright (2018), or the falsifier memo.
4. No evidence shows that the proof-carrying fields (`proof_tag`, `mask_tag`, provenance state) predict or generate forcing success better than simpler non-CA parameterizations.
5. No external gap evidence shows that the Section 5 correctness lemmas answer a known need in prior automated-discovery or CA-search systems. They currently certify only the author's own specification.
6. No exact-valid witness family exists, so there is no bridge from design novelty to mathematical or empirical novelty.
7. The promoted bridge ideas remain below both citation level and verification level; they should not be counted as novelty support.

## Bottom Line

The claimed contribution is materially distinct from the malformed watchlist only. Against the real prior-art boundary, it is:

- not materially distinct in mathematical results;
- only partially distinct in methodological design;
- strongest as an audited blocker-aware research protocol, not as a demonstrated new CA method.

A revised manuscript could survive if it narrows itself to that exact claim boundary and stops implying stronger methodological separation than the evidence supports. In its current form, the differentiation is real but too weakly evidenced to count as a strong novelty win.

REVISE
