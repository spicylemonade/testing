# Phase 6 H4 Typed Residue Interfaces

## Protocol

- Frozen low-height asymmetric family: `asym_a` with `X = [[0, 0], [1, 0], [0, 1], [1, 1], [2, -1]]`.
- Frozen interface alphabet: `['closed', 'top', 'bottom', 'gate_up', 'gate_down']`.
- Symmetry quotient: canonicalize width-4 interface words by horizontal reversal and the row-swap involution top<->bottom, gate_up<->gate_down.
- Unchanged extractor: Each interface symbol maps to a fixed two-row connector pattern over the frozen X: closed->(0,0), top->(a,0), bottom->(0,b), gate_up->(c,d), gate_down->(d,c). The vertical profile is fixed to c on every column.
- Level-1 search space: canonical width-4 interface words of length 3, exact forcing check with the same extractor and no repair.
- Level-2 composition rule: concatenate two forcing width-4 witnesses with one bridge symbol from the same alphabet; seeds and initial solved vertices are copied verbatim into the left and right halves with no new symbols and no repair pass.

## Results

- Level-1 canonical words checked: `39`.
- Level-1 forcing words: `0`.
- Level-2 compositions checked: `0`.
- Level-2 forcing hit rate: `0.0000`.
- Matched direct width-8 hit rate: `0.0000` over `60` exact trials.
- Best composed level-2 certificate: `none`.
- Best matched direct width-8 certificate: `none`.

## Decision

- Passed: `False`.
- Reason: The frozen interface grammar produces no width-4 forcing word under the matched boundary-seed budget, so the route never reaches a nontrivial no-repair level-2 comparison.

## Novelty Position

- The current prior-art gap log covers bootstrap-percolation and macrocell folklore only at the metaphor level. It does not contain an exact verifier-backed audit where a fixed finite interface alphabet is frozen first, actual width-4 legal certificates are composed without repair, and the composed width-8 family is then benchmarked against matched direct no-CA search.
- This is not bootstrap-percolation folklore in new words because the object under test is an exact verifier-facing certificate family, not an infection threshold or fill time.
- It is not just macrocell folklore in new words because the experiment freezes the interface alphabet first and then asks whether exact legal witnesses compose across levels without any repair or hidden extractor change.
