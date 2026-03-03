# FPGA Pipelined Dual-Path Decode

## Topic Context

FPGA-based DEFLATE decompression offers a unique advantage: custom hardware can implement deep pipelines and parallel speculative paths that are impossible in software. The IEEE VLSI Circuits 2019 paper demonstrated a 14nm ASIC GZIP decompressor achieving 20.5 Gbps using a dual-path out-of-order speculative Huffman decoder.

The A-SSCC 2024 paper (Zhang et al.) advanced this with multiple checkpoints and optimized end-of-block control, achieving 43.3 bits/cycle throughput -- the highest reported for a single inflate accelerator.

## Key Insight

Hardware can speculatively decode from TWO positions simultaneously: the known-correct primary position and a predicted secondary position (estimated from average code lengths). When the primary catches up and confirms the secondary's starting point was correct, the secondary's output is committed directly. This achieves up to 2x throughput with minimal additional hardware cost.

## Implementation Backlog

1. **Primary decode pipeline**: 8-stage pipeline with Huffman ROM lookup, LZ77 BRAM-based copy engine
2. **Speculative secondary pipeline**: Independent pipeline with predicted start position
3. **Checkpoint mechanism**: Store decoder state at predicted sync points in BRAM for validation
4. **Multi-checkpoint optimization**: Use 4 checkpoints per block instead of 1, increasing speculation success rate
5. **EOB handling**: Optimized end-of-block detection that doesn't stall the speculative thread
6. **LZ77 multi-bank memory**: Partition history buffer across BRAM banks for parallel read access
7. **PCIe/CXL interface**: Integrate with host system via PCIe for use as acceleration card
8. **Multi-instance design**: Instantiate 4-8 decode engines on a single FPGA for aggregate throughput
