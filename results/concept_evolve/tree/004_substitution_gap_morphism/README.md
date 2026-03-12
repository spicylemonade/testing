# substitution_gap_morphism

## Context
The raw gap sequence may hide a much lower-complexity symbolic process if gaps are encoded by the divisor-witness type that explains them. This card proposes learning a substitution or morphic law on those witness symbols rather than on the numeric gaps themselves.

## Mathematical Sketch
Choose a finite signature map \sigma_n = \Sigma(\text{local witness pattern around } r_n). Seek a morphism \varphi: \mathcal{A}\to \mathcal{A}^* and coding \tau such that \sigma = \tau(\varphi^\omega(a_0)) and d_n = f(\sigma_n) for a low-complexity observable f.

## Why This Bridge Might Matter
The new ingredient is to symbolically encode multiplicative witness geometry instead of raw gap magnitudes, creating a bridge from arithmetic coverage to substitution dynamics.

## Implementation Backlog
- experiments/witness_symbol_encoder.py
- analysis/substitution_mining.ipynb
- data/gap_symbol_sequences.json

## Starting Experiment
Train a symbolic encoder on the first 4000 row gaps, fit candidate substitutions, and test predictive cross-entropy on the next 2000 gaps against iid and Markov baselines.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- On Cloitre’s hiccup sequences (openalex:W7125781376)
- Sumsets of Wythoff sequences, Fibonacci representation, and beyond (openalex:W3032930491)
- Gap Sequence of Cutting Sequence with Slope θ=[0; ḋ] (openalex:W4394662162)
- Dynamics and topology of S-gap shifts (openalex:W2963952529)
