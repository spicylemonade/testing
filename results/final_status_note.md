# Final Status Note

## Outcome

**Sharper evidence only.** The bounded-difference question for the first row of the
prime-separator array remains unresolved.

## Claim-to-Evidence Ledger

| claim | status | evidence | blocker |
|---|---|---|---|
| The first-row difference sequence is bounded. | unsupported | The original H1 certificate claim was rejected on the current corpus, and H2 added no explanatory mechanism. | No horizon-independent invariant or proof bridge from the witness data to a global upper bound. |
| The first-row difference sequence is unbounded. | unsupported | The validated baseline reaches record gaps `25`, `28`, and `30`; a nearby perturbation reaches `31`. | Finite record growth does not imply asymptotic unboundedness. |
| Large record gaps can be composite-only. | supported | Million-step baseline: gaps `28` and `30` are composite-only. `column_immediate` also has late composite-only records. | None for the empirical claim. |
| The raw witness layer yields a compact T-specific certificate language. | rejected on the current corpus | `results/claims/h1_frontier_witness_certificate.md`, `results/experiments/run_1000000/experiment_note.md`, and the late-gap hypergraph export all show heterogeneous mostly-singleton coverage. | Only a stronger full-hypergraph invariant could rescue this line. |
| Prime-support observables explain record-gap growth better than direct witnesses. | rejected on the current corpus | `results/claims/h2_prime_support_fixed_point.md` shows no added explanatory power and many composite-only record gaps. | None; this line is closed unless a genuinely new support observable appears. |

## Strongest Supported Mechanism

The strongest supported mechanism is weak and local:

- each large record gap contains a single endogenous axis-1 boundary marker at the
  previous column term;
- the rest of the interval is covered by heterogeneous mostly-singleton factor pairs;
- the balanced-factor share grows at larger record gaps.

That is enough to sharpen the negative-result picture. It is not enough to settle
boundedness.

## Exact Remaining Blockers

- A proof-level invariant extracted from the witness or hypergraph data.
- A theorem converting finite-horizon record growth into an unboundedness result, if
  such a theorem is even true.
- A decisive argument that distinguishes the array's mex-coupled structure from generic
  divisor/product coverage strongly enough to support a positive mechanism claim.

## Sources

See `results/verification/claim_source_matrix.md` and `sources.bib`.
