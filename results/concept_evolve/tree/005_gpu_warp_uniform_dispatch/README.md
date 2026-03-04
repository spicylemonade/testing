# GPU Warp-Uniform Dispatch

## Topic Context

GPU architectures execute threads in groups of 32 (warps on NVIDIA). When threads within a warp take different code paths or require different iteration counts, utilization drops. In Collatz verification Step 3, threads verify different starting numbers that may require anywhere from 0 to thousands of iterations — a recipe for severe warp divergence.

Angeltveit's solution groups starting numbers by their f value (number of odd Collatz steps in the first N-A iterations), ensuring threads within a kernel invocation process similar-complexity work items.

## Cross-Domain Bridges

- **Task-parallel runtimes**: Work-stealing balances irregular workloads
- **Network processing**: Packet batching by header type for uniform pipeline processing
- **Machine learning**: Batch normalization ensures uniform statistics within each batch

## Implementation Backlog

- [ ] Profile warp utilization with naive (unsorted) dispatch on RTX 3060
- [ ] Implement f-grouped sorting of recursive step outputs
- [ ] Benchmark f-grouped dispatch vs naive on same hardware
- [ ] Test cooperative groups for dynamic thread regrouping mid-kernel
- [ ] Explore persistent thread model for load balancing within a kernel
- [ ] Compare with Barina's 2^40-interval approach on same GPU
