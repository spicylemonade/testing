# Director Brief

## Decision

- Champion: `H1_frontier_witness_certificate`
- Backup: `H2_prime_support_fixed_point`
- De-prioritized: `H3_near_minimal_multiplicative_basis`

## Why This Is The Right Split

The strongest scout signal is that novelty lives or dies at the frontier itself. Long first-row jumps are created by consecutive integers just below the mex already being covered, and the falsifier correctly warns that this becomes trivial or derivative unless the explanation uses the self-generated border sets in an essential way. That makes the witness-carrying frontier-certificate line the best champion: it attacks the actual boundedness event, it can be falsified quickly, and it has a clear novelty bar.

The best backup is the coupled prime-index support line. It is structurally sharper than generic prime-gap talk because it uses the OEIS-noted odious-exponent and recursive prime-support description, but it should remain secondary until it proves that the support layer explains something the frontier witness layer cannot. Prime assignment by itself is not sufficient; the falsifier already records a record gap with no skipped primes at all.

The near-minimal multiplicative-basis framing stays out of the active lane. It overlaps too directly with Ford-style multiplication-table and divisor-in-an-interval literature, and the current scout evidence does not yet isolate a T-specific invariant that would make that framing more than a rebranding exercise.

## Main Blocker

The current scout outputs are enough to choose directions, but not enough to claim a mechanism. The missing proof-oriented artifact is a witness-carrying corpus for record gaps under a recurrence implementation whose update order has been validated. Without that corpus, both the champion and the backup risk collapsing into language rather than mathematics.

## Exact Next Experiment For The Researcher

Run one correct baseline generator only far enough to refind and extend beyond the known record-gap horizon already surfaced in the swarm notes. For every skipped integer in every new record interval, log:

- one valid witness `u * v` with `u` on the row border and `v` on the column border;
- witness multiplicity, if cheaply available;
- skipped-prime versus skipped-composite status;
- row/column offset at that step;
- if the backup line is still active, the relevant prime-support observables for the same interval.

The go/no-go test is simple. If the record-gap corpus yields a compact witness taxonomy or a sharp obstruction language, continue with the champion. If it does not, but prime-support observables explain the failures, promote the backup. If neither happens, stop and record that the current hypothesis family is unsupported rather than widening the search blindly.
