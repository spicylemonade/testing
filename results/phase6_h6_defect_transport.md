# Phase 6 H6 Defect Transport

## Frozen Family

- Family: `asym_a` with `X = [[0, 0], [1, 0], [0, 1], [1, 1], [2, -1]]`.
- Typed motifs on H=2: `{'S': [[1, 1], [1, 1]], 'D': [[2, -1], [1, 0]], 'P': [[1, 0], [1, 1]]}`.
- Periodic word: `SDS`; aperiodic word: `SDP`; reversed word: `PDS`.
- Seed budget: `3`; thinned seed budget: `2`; initial-T budget: `1`.

## Results

- H=2 periodic: forcing=`False`, score=`None`.
- H=2 aperiodic: forcing=`True`, score=`1.8571428571428572`, forced-vertices-per-seed=`2.3333333333333335`.
- H=2 aperiodic after boundary thinning: forcing=`False`.
- H=2 aperiodic after reversal: forcing=`False`.
- H=3 periodic: forcing=`False`.
- H=3 aperiodic: forcing=`False`.
- H=2 matched direct control equals the aperiodic schedule: `True`.
- H=3 matched direct hit rate: `0.0`.

## Falsification

- The only apparent aperiodic gain is the exact H=2 word SDP, but that schedule is already an archived direct certificate, dies under boundary thinning and reversal, and does not survive the H=3 lift. The gain therefore collapses to boundary programming rather than phase-coded defect transport.
- Overlap-trap note: This falls into the local-decoder and chip-firing overlap traps: the successful word behaves like a boundary-scripted sweep on one orientation, not like a transport mechanism that remains visible after seed thinning, orientation changes, or a modest geometry lift.
