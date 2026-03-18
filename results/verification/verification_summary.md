# Verification Summary

Snapshot date: 2026-03-18 UTC

Inputs synthesized:

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`

## Decision

`REVISE`

The current work is not ready for `ACCEPT`. The artifact set does show strong blocker-handling discipline: no proxy score replaced the exact objective, no repaired witness was smuggled in, and negative results were preserved honestly. But the three audits agree that the surviving contribution is only a narrow design-level story. It does not yet support claims of mathematical progress on arithmetic Kakeya, a demonstrated CA-method advance, or empirical superiority over matched baselines.

The right next step is revision, not deepening. Do not widen the search program or add more reframing domains until the missing verifier, benchmark evidence, and citation gaps are addressed.

## Must-Fix Issues

1. Recover or implement a shared exact decoder and verifier for six-line arithmetic-Kakeya witnesses `(X,G,R,T)` over `\mathbb{Z}`.
Keep the fixed no-repair decoder contract. Record candidate-level rejection counts and failure reasons directly at decode and verification time.

2. Run one matched benchmark block before making any empirical claim.
Compare one CA family against Random Local Search, Whole-Witness Mutation, and Decoder-Matched Search on the same grid block with identical `X` or `|X|`, density band, decoder, and exact-decode budget. Report legality hit rate, forcing hit rate, full score distributions, and failure-reason counts for every family.

3. Execute the mandatory controls already specified in the repo.
Run `X`-label shuffle, decoder ablation or randomization, held-out geometry, held-out `X`, small/medium/unrestricted complexity sweeps, and any modular-to-integer lift check used by the lane. Apply the existing kill thresholds verbatim. If the effect survives label shuffle, disappears under decoder matching, vanishes on held-out settings, or only appears in the `small` regime, reject the CA-specific claim.

4. Narrow the claim set to what the current evidence actually supports.
Do not claim mathematical progress, CA-method novelty, benchmark wins, bounded-slope escape, or modular-to-integer transfer. The safe claim is narrower: a verifier-coupled search design with a fixed no-repair decoder contract and explicit anti-overclaim gates.

5. Repair citation readiness before any manuscript-style writeup.
Add the missing background sources for the repeated mathematical introduction, especially Bourgain and the exact Leng-Sah-Sawhney source being relied on. Treat the `11` reframing domains and current bridge ideas as hypotheses unless they are directly sourced. Build a claim-to-citation map instead of relying on title-level prose comparisons.

6. Canonicalize the bibliography entries that are currently weak or inconsistent.
Normalize publication state, metadata, and author encoding for the arithmetic-Kakeya adjacency papers and the AI-system references before those entries are used in any paper draft.

## Optional Improvements

- Split the control report into explicit rows for each baseline family and each stress test so later audits do not need to reconstruct the comparison matrix.
- Add a task-provenance source if the FrontierMath wording or the `<= 1.675` target will appear in a writeup.
- Keep uncited bridge concepts such as `proof_carrying_exact_decoder_bridge`, `spatially_coupled_peeling_ladders`, and `sat_egraph_symbolic_backbone` inside ideation artifacts only until they have direct evidence or direct sources.

## Acceptance Condition

Move from `REVISE` to `ACCEPT` only after all of the following are true:

- the shared exact decoder and verifier exist and are used by every comparison run;
- at least one fully matched benchmark block and the required controls have been executed and logged;
- stronger novelty and benchmark claims are either supported by data or removed;
- citation support is upgraded from blocker-level notes to manuscript-level traceability.
