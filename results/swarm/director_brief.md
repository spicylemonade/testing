# Director Brief

## Decision

- Champion: `H1` - Proof-Carrying Symbolic Forcing-Front CA.
- Backup: `H2` - Sparse-Defect Amplifier CA on a Recursive Background.
- Reserve only: `H3` - Flow-Firing Exact Forcing Decoder.

## Why H1 Wins

`H1` is the least derivative direction in the current scout set. It matches the verifier's actual product-grid and recursive-constructibility structure, forces the CA state to carry exact symbolic proof data, and has the cleanest fast-kill tests: exact integer verification, X-label shuffling, and out-of-distribution size or aspect-ratio checks. It also directly addresses the main structural warning in the gap map, namely that flat-lattice or heuristic local dynamics forget legality and produce false positives.

## Why H2 Survives as Backup

`H2` keeps the same exact-verifier discipline but explores a different regime: mostly cheap recursive background plus a very small number of proof-relevant defects. That is more novel than number-conserving, modular-shadow, reversible, or generic neural-CA branches, and it can be disproved quickly with density-matched random-defect controls.

## Directions to Deprioritize

- Number-conserving or fixed-small-alphabet CA as the main story. The falsifier is explicit that this is the bounded-slope and rational-complexity trap.
- Neural CA as a primary line. Without proof-aware symbolic state and exact decoding, it collapses into generic automated search.
- Reversible or bipermutive CA. The likely failure mode is attractive periodic structure with no verifier-visible forcing gain.
- Modular-shadow-first programs. Modular tasks are acceptable curriculum only; they are not evidence for the integer target.

## Unresolved Blocker

No scout output shows that any CA family actually survives exact integer verification while moving the verified score toward `<= 1.675`. There is also no visible exact verifier or helper-script entry point in the current repo snapshot. If the researcher cannot identify an existing exact evaluator immediately, the correct action is to record that blocker rather than improvising a frontier-search stack in this lane.

## Exact Next Experiment

1. Use the existing exact verifier if one is available outside the current snapshot; if none exists, stop and log the blocker.
2. Run only `H1` first on tiny legal product grids, decoding every candidate directly into `(X,G,R,T)` with no repair step.
3. Apply the three mandatory controls immediately: X-label shuffle at fixed geometry, a matched-budget non-CA baseline, and held-out larger or different-aspect-ratio grids.
4. Promote `H1` only if the exact verified score distribution improves and the signal collapses under label shuffling.
5. Open `H2` only if `H1` is killed cleanly or stalls after the first exact-verification gate.
