# Unresolved Exact-Verifier Gate

Status: unresolved question

Trace-back artifact:

- `results/experiments/h1_tiny_grid_report.md`

Phase-5 synthesis:

- The dominant open question at closeout is still infrastructural, not architectural.
- No exact H1 families ran, no controls ran, and no complexity sweep ran because the exact verifier never appeared.
- This blocker is the reason the run ends in a pivot instead of a go decision.

Why this remains unresolved:

- `results/verification/verification_summary.md` still records no exact decoder or verifier in the repo snapshot or targeted public checks.
- Every surviving bridge depends on the same evaluator.

Dependency for follow-up:

- build or recover the exact integer verifier first; only then reopen witness search, controls, or bridge comparison.
