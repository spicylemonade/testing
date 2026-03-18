# Concept Delta

## Suggestion

Treat the literal `cellar automata` branch as an exact tail-panel pushdown experiment rather than as another flat CA rule.

- Promoted experiment frame: canonical tail-panel cellar automaton with boundary-debt control state
- Competing matched baseline: static boundary-debt residual-state search on the same tokenization and exact oracle
- Guardrail: retire the branch immediately if the stack carries no extra information beyond the static residual state

## Implementation

- Ran `probe` on the exact question of whether any `4x79` or `167/80` tail panel really needs stack memory beyond a static boundary-debt summary.
- Ran `reframe` after the exact panel experiments had started so the branch could be evaluated as a formal-language/no-go question instead of generic CA optimism.
- Implemented `hadamard668/cellar.py` with:
  - canonical tail-panel tokenization
  - dyadic cellar stack summaries
  - matched static boundary-debt control state
  - exact tail-completion oracle panels for the `4x79` control, `167/80` target panels, and degraded `668`-anchored projections
- Wrote the supporting analysis in:
  - `results/analysis/cellar_design_brief.md`
  - `results/analysis/cellar_prefix_complexity.md`
  - `results/analysis/cellar_no_go.md`

## Result

- The solved `4x79` control tail panels close exactly under the static boundary-debt frontier, so the cellar stack has no surviving witness-retention advantage on the same-template control family.
- The recorded `167/80` exact tail panels and the degraded `668`-anchored projections produce no exact completion and no stack-only frontier win.
- The branch therefore ends as a constrained no-go under the implemented encoding, not as a promoted method for solving order `668`.

## Novelty Delta

- Relative to the retired `H1/H2` CA branches, the Phase 6 work did add a materially different information channel: canonical exact tail panels with stack-style residual bookkeeping.
- Relative to the stronger prior-art burden, that novelty does not survive because the matched static residual-state baseline already closes the solved control exactly under the same encoding.
- The only surviving novelty claim is methodological and negative: the literal `cellar` / pushdown interpretation was executed fairly and retired under an exact matched comparator instead of being left as vague future work.
