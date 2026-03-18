# Phase 3 Hypothesis Selection

Prepared for rubric `item_015`.

## Verdict

No CA branch remains active after the fairness-corrected evidence review.

- `H1` is rejected because the matched `direct_greedy` baseline beats `parallel_gain_ca` on both the solved `4 x 79` control and the exact `167/80` target sweep.
- `H2` is rejected because the real degraded order-`668` seed attempt ties the matched non-CA baseline on every decisive verifier metric.
- `H3` remains reserve-only. It is not supported by experiment evidence and cannot inherit credit from the failed `H1/H2` runs.

## Specialist synthesis

- Research-direction constraint:
  - the only defensible next step is a materially different reserve branch with a new design brief and new matched baselines;
  - more budget on the current support-swap and `s`-flip CA rules is out of scope.
- Falsifier outcome:
  - `H1.1` fired exactly as registered;
  - `H1.2` is also supported by the control sweep;
  - `H2.2` fired on the real `668` seed attempt;
  - no `H3` rule fired because no reserve branch was promoted.
- Reserve-branch scout outcome:
  - `R1` orbit-representative / canonical-support search stays reserve;
  - `R2` literal `cellar` reading resolves to `autocorrelation_debt_pushdown`, a pushdown-style prefix filter over the `167/80` obstruction;
  - `R3` `sat_user_propagator_ca` stays reserve as a hybrid symbolic-feedback branch;
  - `R4` `convolution_slice_ca` stays reserve as the cleanest genuinely different state representation;
  - `density_classifier_support_repair` is retired as too close to the losing `H1` family.

## Active branch memo

There is no active branch for the current CA program.

If a reserve branch must be named as the best reopen candidate, it is `R2` plus `R4`:

- `R2` because the literal `cellar automata` reading is materially different from the implemented CA dynamics and now has an explicit formal sketch in the concept tree.
- `R4` because it changes the state representation from raw support bits to local convolution liabilities, which is the cleanest way to avoid simply rerunning the failed `H1` neighborhood.

Neither reserve branch is promoted in this run.

## Dependencies to reopen a branch

Under this repo's evidence gate, any reopened branch must satisfy all of the following before experiments:

- a new design brief that names the changed state representation and why it is not a restatement of the current `H1/H2` rules;
- a matched non-CA comparator on the same representation;
- one solved positive control in the same representation;
- the same equivalence accounting and exact verifier contract used elsewhere in the repo;
- an explicit novelty note against the exact Hadamard anchors and the CA/design anchors.

## Rejection reasons by branch

- `H1`: loses on control, loses on target, reaches fewer unique orbits, and therefore provides no reachability or exact-hit justification for more budget.
- `H2`: the toy ladder is only a weak sanity check, while the real order-`668` attempt ties the non-CA baseline exactly.
- `H3`: still logically possible, but untested and highly vulnerable to collapsing into SAT+CAS or representation-only pruning.

## Decision

Phase 3 closes with no promoted branch. The program advances only as a documented no-go plus a reserve-branch shortlist.
