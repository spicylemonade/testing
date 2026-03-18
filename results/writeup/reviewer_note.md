# Reviewer Note

Role fallback: the rubric asked for `writer` / `reviewer` / `integrator`, but only `worker`, `falsifier`, and `integrator` are available in this environment. This note records the required review flags explicitly.

## Overclaim Flags

- Flag: do not write or imply that Hadamard order `668` was solved.
  - Why: `results/verification/verification_summary.md` states no exact order-668 witness was found.
- Flag: do not write or imply that H1 established a new CA repair method for Hadamard matrices.
  - Why: `results/verification/novelty_report.md` and `results/verification/citation_audit.md` narrow the claim to a tested seeded-CA hypothesis that failed the frontier gate.
- Flag: do not write or imply that the current benchmark is competitive with the broader annealing or SAT+CAS literature.
  - Why: `results/verification/benchmark_report.md` explicitly limits the benchmark to a branch-elimination pilot relative to `suksmono2018`, `suksmono2019`, and `bright2019`.

## Review Result

- `results/writeup/methods_brief.md` is acceptable because it says `pivot to H2`, not `continue H1`.
- `results/writeup/claims_table.md` is acceptable because every claim points to either a verification artifact or a BibTeX key.
- Keep the writeup language narrow and negative-result oriented.
