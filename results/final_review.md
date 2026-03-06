# Final Review

## Writer Pass

1. Confirmed the headline claim stays `audit-first deterministic reference kernel` instead of drifting back to `we built a minimal gravity simulator`.
2. Tightened the main novelty statement so the encounter queue, micro-step wrapper, and machine-readable trust outputs are the contribution, not a vague claim of better integration.
3. Kept the negative result about round-trip error in the analysis because it is scientifically sharper than pretending reversibility alone proves fidelity.
4. Kept REBOUND as the explicit accuracy anchor and avoided any wording that implies a replacement or performance challenge.
5. Kept resolution-coupled softening framed as a failed or deferred branch rather than a hidden rescue mechanism.

## Reviewer Pass

- Director-brief alignment: yes. The final write-up keeps `H1` as champion, `H2` as backup, and avoids new-integrator, large-N, and UI-novelty overclaiming.
- Literature alignment: yes. The final comparisons explicitly reference REBOUND, TRACE, JANUS, poliastro, PhET, and the named watchlist false positives from Phase 1.
- Red-team confirmations:
  1. The contribution is not presented as a generic classroom toy.
  2. The benchmark report makes the direct kernel losses on star-grazing explicit.
  3. The encounter-microstep branch is defended with measured safe-regime evidence rather than aesthetics.
  4. Cross-runtime replay is presented as bounded tolerance, not exact determinism.
  5. Negative results are preserved, which strengthens credibility.
