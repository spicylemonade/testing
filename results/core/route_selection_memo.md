# Route Selection Memo

This memo synthesizes the delegated comparison pass for rubric item `item_014`.

## H1 - Modular shadow / p-adic semilinearity barrier
- Verdict: `go`
- Strongest evidence for:
  - `results/core/h1_modular_shadow_memo.md` already contains a theorem-backed core for arithmetic progressions and finite unions of arithmetic progressions.
  - `results/baseline/modular_shadow_smoke.json` matches that split: rational `3/2` on `ap_2_0` is `exact_recurrence`, while plastic on `ap_2_0` is a `selector_shadow_failure` and plastic on `union_mod3_01` is only `prefix_fit`.
- Strongest evidence against:
  - H1 does not by itself settle the sparse selector lane.
  - `phi` on `fib_indices` survives the modular screen but remains only a screened survivor, not a theorem-backed exact recurrence.

## H2 - Pisot backup
- Verdict: `conditional_go`
- Strongest evidence for:
  - `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` gives exact holdout success for `phi` and `1 + sqrt(2)` under the frozen even-convergent construction.
- Strongest evidence against:
  - `results/core/h2_pisot_backup.md` shows the mechanism is not Pisot-only: non-Pisot `sqrt(2)` also survives, while cubic Pisot `plastic` fails on exact holdout.
  - Salem and transcendental controls fail in the same construction, so the live evidence is a narrow quadratic survivor set rather than a broad Pisot mechanism; that survivor set still remains empirical.

## H3 - Generalized-polynomial / LRS intersection rigidity
- Verdict: `no_go`
- Strongest evidence for:
  - The literature map and probe both say the generalized-polynomial branch is the right language for explaining any genuine higher-degree exception.
- Strongest evidence against:
  - `results/swarm/hypotheses.json` and `results/swarm/director_brief.md` both keep H3 explicitly in reserve until real irrational survivors are isolated and the prior-art gap is stronger.

## Decision
- Primary route: `H1`
- Write theorem language only for the H1 obstruction core: arithmetic progressions and finite AP unions.
- Keep zero-density selector results explicit as screened survivor or leakage lanes for H2/H3 follow-up, not as part of the main theorem.

## Flip condition

The route changes only if one predeclared higher-degree Pisot endpoint or cylinder selector survives exact holdout plus the modular shadow panel while matched non-Pisot or Salem controls fail, or if a survivor class receives a clean generalized-polynomial reduction that H1 cannot absorb.
