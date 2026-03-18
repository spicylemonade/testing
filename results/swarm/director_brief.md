# Director Brief

- Date: 2026-03-18
- Mode: synthesis-only reopen planning after the repo's flat-CA no-go
- Decision rule: maximize genuine novelty, penalize overlap with the retired `H1/H2` families and the falsifier memo, and prefer directions with a fast same-representation kill test

## Champion

`autocorrelation_debt_pushdown`

Choose the canonical-path cellar automaton with deferred autocorrelation debt as the champion direction.

Why this is the right reopen:

- It is the clearest literal reading of `cellar automata` that the repo's reserve packet still treats as materially different from the retired flat CA loops.
- It stays tied to the exact `167/80` cyclic obstruction that actually matters for order `668`, rather than drifting into a generic Hadamard heuristic claim.
- It has the cleanest early falsifier: a same-tokenization non-automaton prefix search with the same exact-completion oracle and the same equivalence accounting.

Why it is still risky:

- Canonicalization and compression can look stronger than the automaton itself.
- If deferred debt does not add information beyond static prefix pruning or exact filtering, the branch collapses into branch-and-bound or SAT+CAS packaging.

Champion stop/go gate:

1. Lock one canonical path or run-length encoding for weight-`80` supports in `Z_167`.
2. Prove zero false negatives on one solved same-template positive control.
3. Compare against a non-automaton prefix search on the exact same representation and oracle budget.
4. Stop unless the automaton preserves witnesses and improves frontier reduction or certificate rate under that matched comparator.

## Backup

`sat_user_propagator_ca`

Keep the proof-carrying cellar frontier as the backup, not as a co-equal start.

Why this is the right backup:

- It adds a new information channel on top of the champion branch instead of reopening the failed raw-support or flat defect-transport families.
- It is more novel than the liability-field reserve because it tries to convert exact failures into reusable local guards rather than just relabeling the H1-side state.
- It remains quickly falsifiable with a static-pushdown baseline on the same canonical representation.

Why it is not the champion:

- The collapse risk into ordinary SAT+CAS is real and already flagged by the falsifier.
- It depends on the static pushdown branch surviving first; otherwise there is no clean base representation to compare against.

Backup stop/go gate:

1. Promote only if `autocorrelation_debt_pushdown` survives the solved-control and matched-baseline checks.
2. Hold the canonical representation fixed and compare only against a static pushdown baseline with the same completion oracle.
3. Stop immediately if the learned feedback is global, one-off, or reduces solver calls only by losing witness retention.

## Held In Reserve

`convolution_slice_ca` stays third.

It is the cleanest alternate H1-side state representation, but it sits too close to the retired support-space family and is therefore the easiest branch to over-credit for mere relabeling. Keep it available only if both cellar branches fail for reasons specific to prefix-state design rather than for lack of reachability.

## Blockers Before Spend

- The repo does not yet have a locked machine-usable positive control in the exact canonical representation required by the cellar branch.
- The same-representation non-automaton comparator must be specified before any researcher is allowed to claim progress.
- The phrase `cellar automata` still cannot carry novelty by itself. The method has to be described as a pushdown or prefix-debt automaton over the exact `167/80` obstruction.

## Exact Next Experiment For The Researcher

1. Extract one canonical representation for weight-`80` supports of `Z_167` and formalize the deferred-debt state fields.
2. Build one solved same-template positive control in that exact representation.
3. Implement the matched non-automaton prefix comparator and freeze the oracle and equivalence-accounting contract.
4. Only then run one small control-budget comparison between the cellar automaton and the matched comparator.
