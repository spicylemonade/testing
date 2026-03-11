# Beatty Model Complete Obstruction

## Topic context
Several Beatty expansions of the additive integers are now axiomatized or model-complete, which sharply constrains how sparse definable subsets can look. This card uses those tame theories as an obstruction engine: if every definable sparse set in a given Beatty structure is trivial or tightly structured, then a hidden LRS subsequence should force r into a narrow algebraic corridor.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Work in structures such as (Z,+,P_r) or (Z,+,f_r), where P_r(n) iff n belongs to B_r and f_r(x) = floor(r*x). If an infinite LRS subsequence Y subset B_r is definable, or selector-definable, inside a tame theory with quantifier elimination or model-completeness, derive necessary forms for Y from the classified definable sets and compare them with sparse recurrence-value growth.

## Cross-domain analogies
- Model-completeness acts like a no-room theorem for exotic sparse sets.
- Beatty arithmetic becomes a tame language that rejects irregular hidden melodies.
- Definable sparsity works like a phase diagram for admissible subsequences.

## Novel move
Model theory is used as a classification obstruction for subsequences, not just as a decidability result about the ambient Beatty structure.

## Why this is not just a reimplementation
Existing papers classify definable sets or prove model-completeness of Beatty expansions. This proposal targets the specific sparse-LRS phenomenon and turns tameness into a nonexistence heuristic.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Extract quantifier-free normal forms from known Beatty theories and test whether candidate LRS value sets or selector sets fit them. Where the normal forms only yield finite unions of dense arithmetic pieces, rule out genuine sparse LRS subsequences.
2. Run the first experiment: Compare quadratic, transcendental-axiomatized, and golden-ratio-floor structures. Ask whether Fibonacci or Pell value sets can be defined or approximated in each setting.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Expansions of the group of integers by Beatty sequences (71157b4e3492593ee91953f91f660c81f13b388c, 2020, Annals of Pure and Applied Logic): Beatty-predicate expansions with quantifier-elimination flavor.
- Model-completeness and decidability of the additive structure of integers expanded with a function for a Beatty sequence (e2ab0ff0760958d37dcde2ddb5292d9784a74f0b, 2021, Annals of Pure and Applied Logic): Model-complete theory for an additive integer structure with a Beatty floor function.
- Fibonacci Numbers and Model-Complete Axiomatization of Presburger Arithmetic Expanded with a Beatty Sequence (c87d7b645610c9b9412dafe492d673424efbd0d0, 2025, arXiv.org): Recent golden-ratio floor axiomatization relevant to sparse definability tests.
- Beatty Sequences for a Quadratic Irrational: Decidability and Applications (74492951ce0e23319ffde058fc107cefc4488d0e, 2024, arXiv.org): Connects model-theoretic Beatty structure to synchronized quadratic presentations.

