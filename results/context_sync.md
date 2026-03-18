# Context Sync

Snapshot date: 2026-03-18 UTC

## Active Lane

- Active hypothesis: `H1` from [results/swarm/director_brief.md](/home/archivara/work/repo/results/swarm/director_brief.md)
- Full name: Proof-Carrying Symbolic Forcing-Front CA
- Why it is active:
  - It matches the product-grid witness representation directly.
  - It is the only lane explicitly promoted by the director brief.
  - Its falsification gate is crisp: exact integer verification, label-shuffle collapse, and out-of-distribution failure checks.

## Core Constraints

- The current repo snapshot does not expose an exact verifier or decoder for six-line `(X,G,R,T)` witnesses.
- The director brief and tool plan both say not to improvise a replacement search stack if that evaluator is absent.
- Therefore the current run is verifier-gated:
  - phase-1 and phase-2 documentation can proceed;
  - phase-3 design can proceed only as a verifier-coupled proposal;
  - phase-4 search claims remain blocked unless a real exact evaluator is found.

## Malformed-Watchlist Caveat

- The saved watchlist and novelty guard were seeded from LaTeX-token noise rather than topic-aware retrieval.
- Their top hits are unrelated papers with superficial token overlap such as `2x2-Convexifications...` and `Hopf hypersurfaces...`.
- These files are still useful as a negative reminder not to trust the initial automated watchlist, but they are not reliable bibliography inputs.
- `results/literature/prior_art_gap.md` already notes this, and the current run should continue to treat it as a standing caveat.

## Saved-Artifact Inconsistencies

- `results/swarm/director_brief.md` exists and is authoritative for lane selection.
- One older note in `results/literature/prior_art_gap.md` says the director brief is absent; that statement is stale.
- `results/research_context.md` still reports rubric progress as `0/25 completed`; this is also stale after the present run starts landing artifacts.
- The right interpretation is: keep the director brief, hypotheses, tool plan, and falsifier memo as the live control documents, and treat the older absence claims as historical residue.

## Phase Dependencies

1. Phase 1 depends on saved context plus targeted literature recovery. It does not depend on an exact verifier.
2. Phase 2 depends on either locating the exact verifier or formally logging the blocker. The witness spec and baseline matrix can still be written from the problem statement.
3. Phase 3 depends on keeping `H1` verifier-coupled. Core design is allowed, but only if it compiles directly to legal witnesses with no repair step.
4. Phase 4 depends on the verifier gate. If the exact evaluator remains absent, experiment reports must become blocker reports and later claims stay closed.
5. Phase 5 depends on honest blocker accounting. If no exact verifier is found, the final assessment must recommend stop or pivot rather than claiming CA progress toward score `<= 1.675`.

## Immediate Operational Decision

- Proceed with literature, specs, baseline planning, and CA design documents.
- Keep `H2` closed unless `H1` is killed or stalls after a real exact-verification gate.
- Treat the missing verifier as the primary blocker to any actual search claim.
