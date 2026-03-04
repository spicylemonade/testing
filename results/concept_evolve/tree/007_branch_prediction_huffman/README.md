# Branch Prediction & Huffman Decode

## Topic Context

The serial dependency in Huffman decoding is fundamentally about determining codeword
boundaries: you must know the length of codeword N to find the start of codeword N+1.
On modern out-of-order CPUs, this manifests as a branch prediction problem: the decode
loop must branch based on the codeword length, and the CPU must predict this branch
to keep the pipeline full.

The key observation is that Huffman codeword lengths are NOT uniformly distributed.
For natural language text, the most common symbols ('e', 't', 'a', space) get short
codes (5-7 bits), and these account for >60% of all symbols. The branch predictor
(TAGE, perceptron) can learn this pattern and achieve >95% accuracy.

This means the serial dependency is partially hidden by the CPU pipeline: even though
each symbol depends on the previous, the branch predictor correctly guesses the length
most of the time, allowing speculative execution to proceed. The decode loop becomes
branch-prediction-bound rather than data-dependency-bound.

Optimization focus: structure the decode loop to maximize branch predictor accuracy.

## Key Challenges

- Random/high-entropy data has uniform length distribution -> unpredictable branches
- Context switches and code sharing may pollute branch predictor state
- CMOV (branchless) trades misprediction cost for guaranteed latency
- Interaction with bit buffer refill branches adds complexity

## Implementation Backlog

1. [ ] Measure branch misprediction rates in zlib/libdeflate decode loops
2. [ ] Implement multi-way switch decode loop with sorted-by-frequency cases
3. [ ] Implement branchless CMOV decode and compare to branchy version
4. [ ] Profile with perf stat and toplev on Zen4 and SPR
5. [ ] Test PGO (profile-guided optimization) impact on branch prediction
6. [ ] Measure throughput across entropy ranges (1 bit/sym to 8 bits/sym)
7. [ ] Compare single-stream optimized decode to multi-stream ILP decode
8. [ ] Analyze interaction between Huffman branch and bit-buffer refill branch
