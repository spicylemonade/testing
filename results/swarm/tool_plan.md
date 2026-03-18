# Tool Plan

## Global Routing Rules

1. Repo-first only. Start from the local scout artifacts and any existing exact verifier or helper-script entry points.
2. Run `H1` first, `H2` only if `H1` fails a mandatory gate, and `H3` only as a one-shot reserve triage.
3. Do not spend budget on broad literature refresh unless the citation auditor identifies a missing primary-source anchor for a concrete claim.
4. No proxy-only wins. Every claim must survive exact decoding into `(X,G,R,T)` and exact score accounting over `Z`.
5. Modular or finite-field tasks may be used only as curriculum. They do not count as evidence.

## Role Routing And Budget Envelopes

| Role | Tool routing | Budget envelope | Hard gates |
| --- | --- | --- | --- |
| Orchestrator | Read `results/research_context.md`, the literature gap files, `results/swarm/gap_map.md`, `results/swarm/hypothesis_bridge.md`, `results/swarm/hypothesis_negative_space.md`, `results/swarm/falsifier.md`, then `results/swarm/hypotheses.json` and `results/swarm/director_brief.md`. Keep only one active hypothesis lane at a time. | One repo synthesis pass. Zero broad searches. At most one narrow citation-recovery pass if blocked. | Stop the lane on missing exact verifier, label-shuffle failure, decoder leakage, or compute mismatch. |
| Researcher | Use existing verifier and helper scripts through the shell. If no exact evaluator exists, log the blocker instead of inventing a new frontier-search stack. Run exact decode and score loops only on the active lane. | Phase 1 only: at most 3 local-rule families and `10^3` exact decodes per family on tiny legal grids. No phase 2 until review. | No repair heuristics, no modular evidence, no fixed-`X` only reporting, no promotion without exact score improvement. |
| Falsifier | Re-run only the mandatory controls on each promoted family using the same exact decoder and score function. | One X-label shuffle sweep, one matched-budget non-CA baseline sweep, and one held-out size or aspect-ratio sweep per promoted family. | Kill on exact-score collapse, shuffle survival, OOD failure, or evidence that the decoder is doing the hard work. |
| Writer | Write only after a family passes the exact-verification gate. Pull claims from the verified logs and the selected primary-source anchors only. | No new search except citation fixes explicitly requested by the citation auditor. | Must report blocker status, controls, hit rate, and score distribution. No proxy metrics or best-of-many storytelling as primary evidence. |
| Reviewer | Inspect the write-up and research logs for score accounting, control coverage, and claim scope. | One review pass per milestone. | Reject if full `m(G)+|R|` over `n(G)-|T|` accounting, matched baselines, or negative results are omitted. |
| Citation auditor | Verify only the concrete anchors used in the selected hypothesis and write-up. Keep searches narrow and primary-source-driven. | At most 5 targeted source checks. No broad survey pass. | Must clear the Tao bounded-slope warning, Green-Ruzsa finite-field distinction, Cowen-Breen adjacency, Pohoata-Zakharov adjacency, and any abelian-network or CA-method citation used. |
| Benchmark auditor | Define the baseline matrix before large runs, then audit compute parity and reporting after the first exact-verification pass. | One pre-run benchmark-spec pass and one post-run audit pass. | Enforce matched exact-decode budget, matched `|X|` and edge-density budget, decoder-matched baselines, OOD checks, and distribution reporting rather than best-of-many only. |

## Hypothesis-Specific Routing

- `H1` is the only champion lane. Its first gate is exact verification plus X-label-shuffle collapse.
- `H2` opens only if `H1` is killed cleanly or stalls after the first exact gate.
- `H3` is reserve-only. It gets one small predictive triage slice, not a full search campaign.

## Immediate Blocker Check

- The current repo snapshot does not expose an obvious exact verifier or helper-script entry point.
- If the researcher cannot identify that evaluator immediately, the orchestrator should stop and record the blocker before any CA search expands.
