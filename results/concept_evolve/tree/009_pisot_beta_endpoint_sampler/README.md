# Pisot Beta Endpoint Sampler

## Topic context
Known generalized-polynomial constructions show that some Pisot or Salem linear-recurrence value sets are definable by floor expressions. This card reverses the arrow: choose indices from beta-endpoint numeration systems and test whether Beatty values sampled on those endpoints become exact LRS, potentially exposing a Pisot-only extension beyond the quadratic or Ostrowski world.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Let beta > 1 be a Pisot unit with associated linear-recurrence numeration G_n. Choose indices n_k whose greedy beta-expansion terminates in a fixed endpoint or cylinder pattern, or whose Rauzy address lies on a fixed face. Study y_k = floor(r*n_k) and test whether y_k satisfies the characteristic polynomial of G_n or a factor of it.

## Cross-domain analogies
- Use beta-endpoints as crystal defects that amplify hidden recurrence.
- Treat Pisot numeration as a non-quadratic cousin of Ostrowski coding.
- Sample along self-similar faces of a quasicrystal.

## Novel move
Endpoint-conditioned Beatty sampling is proposed as a way to discover higher-degree algebraic special numbers.

## Why this is not just a reimplementation
Existing Pisot and generalized-polynomial work shows that some LRS value sets are floor-definable. This card asks whether such numeration endpoints can generate exact subsequences inside an external Beatty sequence.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Generate G_n and greedy beta expansions for small Pisot units, enumerate endpoint-constrained indices, and test the resulting Beatty values with exact Hankel and companion-matrix checks. If a recurrence candidate appears, search for a symbolic explanation via tile addresses.
2. Run the first experiment: Try beta in {phi, 1+sqrt(2), plastic constant}. Compare endpoint-conditioned samples with random beta-digit samples as a control.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Pisot numbers, Salem numbers, and generalised polynomials (945bf0b906b8a3273f821db634b506879566566f, 2023, arXiv.org): Key evidence that Pisot recurrence-value sets can be generalized polynomial.
- Generalized Rauzy tilings and linear recurrence sequences (0354e145b397be098c4ddcecd337be8455e59486, 2021, Chebyshevskii Sbornik): Supplies endpoint and tile-face geometry tied to linear-recurrence numeration.
- Sparse generalised polynomials (352a36ff547769f41b9a06e2a153f14869312eb8, 2016, Transactions of the American Mathematical Society): Provides sparsity obstructions that can separate real hits from accidental ones.
- Beatty Sequences for a Quadratic Irrational: Decidability and Applications (74492951ce0e23319ffde058fc107cefc4488d0e, 2024, arXiv.org): Acts as the quadratic baseline before extending to higher-degree numeration.

## Current decision
- Alignment: `H2`
- Promotion status: promoted as the live higher-degree backup experiment.
- Evidence links: `results/core/h2_pisot_backup.md`, `results/concept_evolve/probe_result.json`, `results/concept_evolve/steering_notes.md`
- Current experiment status: executed and currently negative. `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/results.json` shows no exact low-order recurrence for the suffix-`10` endpoint selector on `phi`, `1 + sqrt(2)`, `plastic`, or the matched controls.
- Decision: invalidate this concrete endpoint proxy as the missing higher-degree rescue mechanism; keep the geometric idea only as a possible future refinement.
