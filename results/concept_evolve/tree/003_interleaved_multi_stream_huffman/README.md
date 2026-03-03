# Interleaved Multi-Stream Huffman Decoding

## Topic Context

Modern superscalar CPUs can execute 4-8 independent operations per cycle, but a single Huffman decode stream has a critical dependency chain: each symbol's bit position depends on the previous symbol's code length. This chain limits throughput to ~1 symbol per ~3-4 cycles regardless of the CPU's parallel execution capability.

Fabian Giesen's work on Oodle Data (RAD Game Tools) showed that splitting Huffman data into K independent streams and interleaving their decoding breaks this dependency. With K=3 streams, the decoder achieves nearly 3x throughput because the CPU can overlap table lookups across streams. With K=6 and careful register allocation, throughput approaches the memory bandwidth limit.

## Key Insight

The bottleneck is not the Huffman decode operation itself (a single table lookup), but the **serial dependency chain** between consecutive decodes within one stream. Multiple streams provide independent chains that a superscalar CPU can execute in parallel.

## Implementation Backlog

1. **Multi-stream encoder**: Partition symbols round-robin into K streams, encode each independently
2. **3-stream decoder**: Implement Giesen's 3-stream interleaved pattern with BMI2 PEXT/PDEP
3. **6-stream decoder**: Extend to 6 streams, measure register pressure and L1 cache contention
4. **Auto-tuning**: Detect optimal K at runtime based on CPU microarchitecture (Zen4 vs Golden Cove vs Gracehopper)
5. **Integration with LZ77**: Feed multi-stream Huffman output into LZ77 copy execution pipeline
6. **Backward compatibility wrapper**: Old decoders see a single stream; new decoders detect multi-stream marker
7. **Throughput profiling**: Use Intel VTune / AMD uProf to measure IPC, port utilization, and stall cycles
