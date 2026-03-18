# Stage-Indexed Macrocell Fragments

Status: promoted baseline-compatible encoding

## Source Inspiration

- `results/concept_evolve/tree/007_macrocell_curriculum_nca/concept.json`
- `results/concept_evolve/tree/010_egraph_linear_span_rewriting/concept.json`

## Encoding

Each cell stores a small legal witness fragment rather than a raw slope label: local `f_i` intent, a seed/not-seed marker for `R`, a `T` mask bit, and a compact symbolic provenance tag. The board is stage-indexed, so legality information is native to the encoding instead of being repaired after generation.

## Why It Is Promoted

- It is compatible with the benchmark matrix because non-CA baselines can mutate the same fragment alphabet directly.
- It keeps the decoder burden small enough that decoder-matched baselines remain meaningful.
- It is the cleanest bridge between CA generation and exact witness syntax.

## Main Tradeoff

The alphabet is larger and less elegant than particle-style encodings, but it preserves the proof-carrying structure that the verifier gate requires.
