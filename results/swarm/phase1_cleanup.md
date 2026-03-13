# Phase 1 Literature And Novelty Cleanup

Date: 2026-03-13
Rubric item: `item_005`

## Lexical Noise Removed From The Active Prior-Art Set

The original seed query over-weighted the words `improve` and `number`. The following papers are excluded from the active Ramsey corpus, baseline tables, and novelty guard:

- `Senolytics Improve Physical Function and Increase Lifespan in Old Age`
- `Leveraging polygenic functional enrichment to improve GWAS power`
- `Using Simulation and Domain Adaptation to Improve Efficiency of Deep Robotic Grasping`
- `The EPR effect and beyond: Strategies to improve tumor targeting and cancer nanomedicine treatment efficacy`
- `Automatic Number Plate Recognition`
- `Number Cookbook: Number Understanding of Language Models and How to Improve It`
- The remaining lexical false positives in the saved watchlist and `top_papers` cache

These entries remain in the repo only as evidence that the initial lexical search was noisy. They are not substantive prior art for `R(5,5)`.

## Fixed Ramsey Corpus And Ranked Reading Order

Do not widen literature search again until this packet is exhausted.

1. `Small Ramsey Numbers Dynamic Survey 1` for the live frontier and citation map.
2. Exoo 1989 for the lower-bound construction line.
3. Ge et al. 2022 for the modern study of Exoo's `R(5,5) >= 43` witness family.
4. Lehavi 2024 for one-vertex extension checking and the closest `H1` overlap surface.
5. Angeltveit-McKay 2024, `R(5,5) <= 46`, for the current best published upper bound.
6. Angeltveit-McKay 2018, `R(5,5) <= 48`, for the preceding exact upper-bound baseline.
7. McKay-Radziszowski 1992 for the foundational case-analysis line.
8. Aija'am 2010, but only as an overlap-kill check for generic GA claims.
9. Gauthier 2025 only if `H2` remains alive.
10. Gauthier-Brown 2024 and Barakeel-Gauthier-Commelin 2025 only for `H3` or certificate packaging.

Broader adjacent reads stay deferred until the direct packet above is exhausted.

## Overlap Risks By Route

- `H1`: the closest unmodeled overlap is Lehavi's one-vertex extension and counterexample-checking line. `H1` is novelty-safe only when framed as a cross-family canonical obstruction atlas for failed `42 -> 43` extensions, with held-out transfer and witness-safety audits.
- `H2`: the main failure mode is becoming the split-vertex and transverse-edge gluing line with a stronger solver or a different branching order. No `H2` benchmark is worth running unless the primitive is non-equivalent and wins on verified residue size, proof bytes, or checker runtime under matched conditions.
- `H3`: this is attachment-only. If it does not attach to an `H1` or `H2` structural object and survive cross-branch or cross-family reuse tests, it is infrastructure rather than novelty.
- Global framing: avoid generic `improve` and `number` language. The first sentence of outward-facing text must contain `R(5,5)` and the concrete Ramsey object.

## Concrete Plan Changes Caused By The Synthesis

1. Replace the open-ended literature refresh with the fixed Ramsey corpus above.
2. Insert `Rung 0` before any `H1` atlas or transfer experiment: reconstruct the Exoo/Ge/Lehavi one-vertex-extension setting and materialize the canonical `frontier_parent`, `extension_case`, and `failure_witness` schema.
3. Add Lehavi 2024 as a mandatory comparison row, and demote Aija'am 2010 to overlap-only status.
4. Gate Gauthier 2025 and formal-proof work behind `H1` failure or proof-packaging needs rather than parallel mainline work.
5. Add an `H2` non-equivalence gate before any benchmark and a lexical scrub gate before any outward-facing title, abstract, or comparison table.

## Immediate Next Actions

- Materialize the `frontier_parent` corpus and the orbit-distinct `42 -> 43` extension schema before claiming any `H1` mechanism.
- Use the fixed corpus to drive Phase 2 and Phase 3 baseline work, rather than reopening broad literature search.
- Keep `H1` as champion, `H2` as backup, and `H3` as reserve unless a documented kill condition fires.
