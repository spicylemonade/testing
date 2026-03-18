# Tool Plan

## Global Routing Rules

1. Repo-first only. Start from the local scout artifacts, benchmark spec, verification summary, and any existing exact verifier or helper-script entry points.
2. Treat the malformed watchlist and the `research_context.md` closest-prior-art block as non-authoritative for novelty. Real pressure comes from the prior-art gap memo, the falsifier, and the verification artifacts.
3. No broad literature or web refresh. The citation auditor may request one narrow primary-source recovery pass only if a live claim lacks an anchor.
4. Keep one active hypothesis lane at a time: `H1` first, `H2` only after an `H1` outcome, and `H3` reserve-only.
5. No proxy-only or modular-only wins. Every promoted result must survive exact no-repair decoding into `(X,G,R,T)` with full score accounting.
6. Hard-stop conditions are unchanged: missing exact verifier, decoder leakage, `X`-label-shuffle survival, unmatched compute, or gains confined to the small-complexity regime.

## Role Routing And Budget Envelopes

### Orchestrator

- Tool routing: repo reads, shell access, benchmark-spec checks, and narrow agent coordination only.
- Allowed actions: confirm blocker state, keep one active lane, dispatch only existing scripts or helper entry points, and request citation recovery only if the citation auditor flags a gap.
- Forbidden actions: parallel frontier exploration across multiple hypotheses, broad search refresh, proxy-metric promotion, or using malformed watchlist hits as novelty evidence.
- Budget envelope: one blocker check plus one first-gate comparison block.
- Exit criterion: either the exact evaluator is found and `H1` launches, or the blocker is logged and the run stops.

### Researcher

- Tool routing: existing exact verifier and helper scripts through the shell; if absent, verifier recovery only.
- Allowed actions: locate an existing exact decoder or verifier, implement only that missing evaluator if explicitly assigned, then run `H1` on tiny legal grids with exact logging.
- Forbidden actions: solver improvisation, repair heuristics, modular-only evidence, or opening `H2` or `H3` early.
- Budget envelope: phase 0 verifier recovery or lookup; then one `H1` block with one SAT-constrained schema, up to `3` rule families, and `10^3` exact decodes per family.
- Exit criterion: exact-valid-yield and verified-score report with all mandatory controls, or a blocker log if the evaluator is missing.

### Falsifier

- Tool routing: the same exact decoder and score function used by the researcher; no alternate evaluator.
- Allowed actions: rerun only kill tests on promoted families, including the decoder-matched non-CA baseline, canonicalization ablation, `X`-label shuffle, held-out geometry, held-out `X`, and the complexity split.
- Forbidden actions: new generator ideas, proxy metrics, or fairness changes.
- Budget envelope: one kill pass per promoted family; add uncoupled repetition and template randomization for `H2`, and independent interface matching for `H3`.
- Exit criterion: explicit keep or kill judgment tied to exact-valid yield or verified score.

### Writer

- Tool routing: repo-first synthesis from frozen logs and audits; limited citation follow-up only if requested by the citation auditor.
- Allowed actions: write blocker-aware summaries, benchmark tables, and exact-result narratives that match the logs.
- Forbidden actions: "solved" language, best-of-many storytelling, proxy claims, or omitted negative results.
- Budget envelope: one short milestone write-up after blocker resolution, or one blocker report if resolution fails.
- Exit criterion: claim boundary matches the verification summary and benchmark audit.

### Reviewer

- Tool routing: repo audit against `results/verification/verification_summary.md` and `results/baselines/benchmark_spec.md`.
- Allowed actions: inspect score accounting, control coverage, baseline parity, and scope discipline.
- Forbidden actions: relaxing matched-budget rules or omitting `m(G)`, `|R|`, `n(G)`, or `|T|`.
- Budget envelope: one review pass per milestone.
- Exit criterion: approve only if exact-decode parity, control coverage, and full distribution reporting are present.

### Citation Auditor

- Tool routing: primary-source-only recovery for the exact claims that survive into the write-up.
- Allowed actions: targeted checks for Katz-Tao task framing, Green-Ruzsa's finite-field caution, Cowen-Breen adjacency, Tao's bounded-slope warning, and the specific methodological anchors actually cited for `H1`, `H2`, or `H3`.
- Forbidden actions: broad novelty surveys, use of malformed watchlist items as real overlap, or secondary-source padding.
- Budget envelope: at most `5` targeted source checks.
- Exit criterion: every live claim has a direct anchor or is deleted.

### Benchmark Auditor

- Tool routing: pre-run fairness audit plus post-run parity audit.
- Allowed actions: freeze the comparison matrix, enforce exact-decode budget parity, check `|X|` and density parity, and require distribution-level reporting.
- Forbidden actions: aggregating baselines into one weak comparator, best-of-many reporting, or proxy-only wins.
- Budget envelope: one pre-run spec pass and one post-run audit pass.
- Exit criterion: the block is either benchmark-cleared or explicitly marked blocked or not evaluable.

## Hypothesis Routing

- `H1` is the only active lane at launch.
- `H2` opens only after verifier recovery plus either an `H1`-cleared micro-gadget bank or a narrow unresolved coupling question.
- `H3` stays reserve-only unless `H1` and `H2` are both killed cleanly and the remaining blocker is representation mismatch rather than search quality.

## Immediate Handoff

- If no shared exact verifier or decoder entry point is visible, the researcher's next task is verifier recovery, not CA search.
- If the verifier exists, the first run is the `H1` first-gate block and nothing broader.
