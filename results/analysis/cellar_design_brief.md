# Cellar Design Brief

Prepared for rubric `item_026`.

## Canonical tokenization

- Search domain: canonical dihedral representatives of binary supports with fixed length and weight.
- Exact panel form: fix a canonical base prefix of length `B > floor(n / 2)` and leave a contiguous suffix of length `m` free.
- Tokenization: scan the free suffix left-to-right as `0/1` symbols; after each appended bit, apply the dyadic carry schedule that merges equal-size trailing blocks.
- Rationale: this gives a reproducible visibly-pushdown-style cellar discipline without changing the exact completion task.

## Control state

The matched non-stack control state is the **boundary-debt summary**:

- free-prefix length and assigned length
- assigned and remaining weight
- assigned cyclic half-autocorrelation vector with unread suffix bits masked to `0`
- fixed left-boundary bit pattern of width `floor(n / 2)`
- current right-boundary bit pattern of width `floor(n / 2)`

This is the load-bearing exact state used by the static comparator.

Current caveat:

- on the recorded tail panels this state is strong enough to be effectively prefix-identifying, so it already kills the literal cellar branch under this encoding
- that is a valid no-go for this exact formulation, but it is not yet evidence that every weaker static summary would behave the same way

## Stack alphabet and update law

- Stack frame: one dyadic block summary with block length, block weight, block bit string, block prefix bits, block suffix bits, and the block's internal linear pair vector.
- Push rule: each new suffix bit starts as a length-`1` cellar.
- Merge rule: whenever the top two cellars have equal length, pop both and push their merged parent summary.
- Deferred debt law: merged block summaries preserve the local pair contribution already realized inside the free suffix while deferring unresolved cross-boundary obligations to the fixed boundary-debt control state.

## Acceptance condition

- A prefix is accepted exactly when its boundary-debt control state remains in an extendable class under the exact tail-completion oracle.
- The cellar stack refines the representation of the free suffix but does not change the matched oracle, tokenization, or equivalence accounting.

## Matched static comparator

- Same canonical tokenization
- Same exact tail-completion oracle
- Same fixed prefix panel
- Same canonical equivalence accounting
- Same budget

The only difference is memory discipline: the comparator keeps only the boundary-debt control state and discards the cellar stack.

## Exact control verification

Artifact: `results/experiments/cellar_phase6.json`

Solved same-template control:

- panel: `control_4x79_tail12`
- length: `79`
- fixed base prefix length: `67`
- free suffix length: `12`
- exact completions at the root: `1`
- total weight-feasible prefixes: `2001`
- exact extendable prefixes: `13`

Verification result:

- boundary-debt comparator frontier: `13`
- cellar-stack frontier: `13`
- witness retention: `13 / 13`
- false negatives on the solved control: `0`

So the canonical cellar automaton is well-defined and sound on the exact `4 x 79` control, but the matched static comparator already retains the same exact witness-prefix family.
