# Concept: butterfly_permutation_network

- Topic Context: Research Task: SIMD-Accelerated Base64 Decoding - Design and implement a Base64 decoder for RFC 4648-compliant streams that significantly outperforms the current best implementations on both x86-64 (AVX2/AVX-512) and ARM64 (NEON/SVE) hardware. The core opportunity is that standard Base64 decode is embarrassingly parallel — every 4 input characters map independently to 3 output bytes — yet most production implementations (OpenSSL, glibc, Chrome base64) still decode scalar byte-by-byte, leaving massive SIMD throughput on the table. Target 5x over the best widely-deployed scalar implementation across realistic payload sizes (1 KB-10 MB), with full validation of invalid characters and padding, and benchmark against Lemire existing simdbase64/fastbase64 work to establish whether further gains are achievable through wider vectors, improved shuffle masks, or streaming-friendly pipeline design.
- Domains: signal processing, network routing, SIMD vectorization

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.