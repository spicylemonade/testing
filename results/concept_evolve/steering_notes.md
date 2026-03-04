# ConceptEvolve Steering Notes

## Three Concrete Steering Directions

### Direction 1: Delay-Record-Specific Sieve with Trajectory Height Preservation (PRIORITIZED)
- **Description**: Invert the standard sieving philosophy — instead of eliminating numbers with short stopping times, identify residue classes mod 2^k whose trajectories are predicted to have anomalously long non-descent periods. Build a "positive sieve" that prioritizes high-delay candidates.
- **Rubric items informed**: item_008 (sieve implementation), item_011 (tail predictor), item_012 (probabilistic model), item_013 (search engine), item_016 (systematic search)
- **Why prioritized**: This directly addresses the core research problem (finding delay records, not just convergence verification). Existing sieving literature focuses on convergence verification; a delay-record-specific sieve is a genuine novel contribution. The concept tree path `information_directed_branch_prune → recursive_bit_tree_sieve → bitvector_lookahead_compression` supports this direction.

### Direction 2: Probabilistic Anomaly-Guided Search
- **Description**: Use the Lagarias-Kontorovich-Tao probabilistic framework to estimate expected stopping times for each number, then focus search on numbers that are statistically predicted to be anomalous. Combine the random walk model (expected stopping time ≈ 6.95 × log₂(n)) with binary-prefix analysis to prioritize candidates.
- **Rubric items informed**: item_012 (probabilistic model), item_013 (search engine), item_014 (trajectory fingerprinting), item_016 (systematic search)
- **Why considered**: Strong theoretical foundation in Tao (2019) and Sinai (2003). Polli et al. (2024) showed Collatz orbits have geometric Brownian motion properties with detectable correlations. This is practically implementable.

### Direction 3: Trajectory Fingerprinting via Binary Encoding
- **Description**: Encode Collatz trajectories as binary strings (0=even step, 1=odd step) and identify motifs that correlate with long stopping times. Use suffix arrays or rolling hash techniques to build a fingerprint database. This connects to the concept tree's `bitvector_lookahead_compression` and `memoized_3f_lookup_table` concepts.
- **Rubric items informed**: item_014 (trajectory fingerprinting), item_019 (ablation study), item_023 (visualization)
- **Why considered**: Novel cross-domain bridge from string algorithms to number theory. The observation that many delay records share similar residues (Roosendaal) suggests common trajectory substructure that fingerprinting could exploit.

## Priority Decision
**Direction 1 is prioritized** because:
1. It produces the highest-impact novel contribution (a new type of sieve for delay records)
2. It directly feeds the most rubric items (5 out of 25)
3. It builds on the concept tree's strongest path: `adaptive_sieve_depth_scaling → recursive_bit_tree_sieve → descent_ratio_pruning`
4. The "positive sieve" approach is absent from existing literature (all current sieves are "negative" — they eliminate easy cases)
5. Combined with Direction 2 (probabilistic guidance), it forms a complete novel search methodology

Direction 2 and 3 will be implemented as complementary techniques within the search engine (item_013).
