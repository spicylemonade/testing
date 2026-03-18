# Phase 1 Planning Note

- Exact target: produce a legal verifier-compatible certificate `(X; d_i; f_i; T; R)` with score `<= 1.675`, or else document a constrained no-go after exact search and verification.
- Route order confirmed after reading `results/swarm/hypotheses.json` and `results/swarm/tool_plan.md` before implementation:
  - Champion: `H1_macrocell_substitution`
  - Backup only: `H2_target_direction_abelian`
  - Reserve only: `H3_slope_bloom`
- Frozen blockers from `results/swarm/director_brief.md` that must exist before experiments:
  - one exact certificate grammar for `(X; d_i; f_i; T; R)`
  - one matched baseline matrix
  - one symmetry-quotient policy
- Consequence for this run:
  - no broad CA search or optimizer is allowed before the grammar, baselines, and quotient rules are explicit;
  - every candidate must be compiled directly to legal certificate data and judged on exact extracted score, not occupancy or fill-time proxies;
  - the most likely honest outcome is either a narrow CA-guided search contribution or a documented failure of the CA framing to beat matched arithmetic baselines.
