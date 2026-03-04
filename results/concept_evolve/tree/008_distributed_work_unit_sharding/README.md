# Distributed Work Unit Sharding

## Topic Context

Collatz verification is embarrassingly parallel but requires careful work-unit design for distributed execution. Barina's project (pcbarina.fit.vutbr.cz) uses interval-based sharding: each work unit is 2^40 consecutive integers, taking ~10 seconds on a modern GPU. This has verified all numbers below 2^71.

Angeltveit's algorithm naturally shards by residue class: the recursive step produces ~278,699 independent cases (for suitable parameters), each taking similar time. This is harder to distribute sequentially but offers better load balance.

## Cross-Domain Bridges

- **MapReduce**: Key-based partitioning for balanced parallel processing
- **Volunteer computing**: BOINC/GIMPS models for distributed mathematical verification
- **Consistent hashing**: Uniform work distribution across heterogeneous workers

## Implementation Backlog

- [ ] Design work-unit protocol compatible with both sharding strategies
- [ ] Implement coordinator server with progress tracking and fault tolerance
- [ ] Add checksum verification for result integrity
- [ ] Support heterogeneous GPU fleet (different work-unit sizes by GPU capability)
- [ ] Implement hybrid sharding: Angeltveit for recursive phase, Barina for Step 3
- [ ] Estimate total compute cost for N=72, 75, 77
