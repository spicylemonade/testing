# Path-Merging Deduplication

## Topic Context

The Path-Merging Sieve identifies integers whose Collatz trajectory merges with that of a smaller integer at some point, without necessarily descending below the starting value first. This is a strictly stronger condition than descent: it can prune n even when T^k(n) > n for all k up to the merge point.

The efficient implementation avoids mod-3 division by using Lemma 2.8: T^k(n) is congruent to 2 mod 3 if and only if there are an even number of even steps after the last odd step. This can be tracked with a simple counter.

## Cross-Domain Bridges

- **Compilers**: CSE detects when two expressions compute the same value
- **Distributed storage**: Content-addressable deduplication identifies identical data blocks
- **DAG processing**: Once two paths merge, downstream computation is shared

## Implementation Backlog

- [ ] Implement mod-3 counter (2-bit state machine) in recursive traversal
- [ ] Validate path-merging detections against known trajectory data
- [ ] Measure marginal pruning rate beyond Descent Sieve
- [ ] Incorporate into bitvector precomputation (Definition 4.3)
- [ ] Test mod-9 extension of path-merging (m congruent to 4 mod 9)
