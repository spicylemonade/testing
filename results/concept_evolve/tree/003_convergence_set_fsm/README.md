# Convergence Set FSM Parallelization

## Context

Huffman decoding is a finite-state machine computation: the "state" is the current bit position in the compressed stream, and each transition decodes one symbol and advances by its code length. Parallelizing FSMs is famously difficult due to the inherent serial state dependency.

The Convergence Set Enumeration (CSE) approach from Zhuo et al. (MICRO 2018) offers a more efficient alternative to naive state enumeration. Instead of tracking individual state-to-state transitions for all possible starting states, CSE groups states into "convergence sets" - sets of states that will converge to the same state after processing enough input.

## Key Insight for DEFLATE

DEFLATE Huffman codes have a maximum code length of 15 bits. This means there are at most 15 possible "starting states" (bit offsets mod 15) to enumerate. The convergence set approach can dramatically reduce this: in practice, most of these states converge within 20-40 symbols of input, meaning that for a segment of 100+ symbols, we almost always need to execute only once.

## Comparison with Probe-Based Sync (Concept 002)

The probe-based sync approach (concept 002) finds a single synchronization point. CSE is more general: it tracks which states have converged and can handle partial convergence. This makes CSE more suitable for GPU-like massive parallelism where we need to split into many segments, while probe-based sync is simpler for 2-4 way splitting.

## Implementation Backlog

- [ ] Implement DEFLATE Huffman FSM model
- [ ] Profile convergence rates for different file types and compression levels
- [ ] Implement CSE-based parallel decode for 4-16 segments
- [ ] Compare efficiency against probe-based sync point method
- [ ] Measure overhead of set tracking vs benefit of avoiding re-execution
- [ ] Test on GPU (CUDA) for massive parallelism (>1000 threads)
