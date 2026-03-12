# multiplicative_automatic_obstruction

## Context
Automatic-sequence theory can also be used negatively: any automatic model that directly encodes prime-side membership is likely too rigid. This card turns classification theorems for multiplicative automatic sequences into a falsifier for overly simplistic conjectures about T.

## Mathematical Sketch
Define a candidate sign map \chi(p)\in\{\pm1\} by whether prime p first appears on row 1 or column 1, and extend completely multiplicatively. If \chi were k-automatic, classification results force eventual character-like rigidity incompatible with observed composite leader placement; therefore any finite-state model must act on frontier states, not on \chi alone.

## Why This Bridge Might Matter
The new move is to use automatic-sequence rigidity as a conjecture filter for the prime-separator frontier, not as a direct generative model.

## Implementation Backlog
- experiments/automatic_shadow_sat.py
- notes/negative_model_tests.md
- data/prime_side_constraints.json

## Starting Experiment
Run a SAT/SMT search over k-automatic sign models with a small state budget using the first few hundred assigned primes and border composites as constraints.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- Multiplicative automatic sequences (openalex:W2947108435)
- On completely multiplicative automatic sequences (openalex:W3002877276)
- Automatic proofs in combinatorial game theory (openalex:W4414338337)
