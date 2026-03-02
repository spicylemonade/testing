# Ablation Study: Modular Sieve Prime Set

## Filtering Rate by Number of Primes

| Primes | Sieve Rate | Exact Checks | Time (s) | Speedup vs 5 primes |
|--------|-----------|-------------|----------|-------------------|
| 5 | 97.6% | 51300 | 0.392 | 1.00x |
| 10 | 100.0% | 105 | 0.527 | 0.74x |
| 15 | 100.0% | 23 | 0.537 | 0.73x |
| 20 | 100.0% | 23 | 0.541 | 0.72x |
| 25 | 100.0% | 23 | 0.542 | 0.72x |

## Diminishing Returns

Adding primes beyond ~15 provides minimal additional filtering benefit.
The sieve rate approaches 100% quickly since early primes (especially 2, 3, 5)
eliminate the vast majority of candidates. However, more primes do reduce
the number of false positives reaching the exact check stage.

## Individual Prime Filtering Power

The primes with the most filtering power for the perfect cuboid problem are:
- **p=2**: Eliminates ~50% (parity constraint)
- **p=3**: Eliminates ~33% of survivors (QR mod 3 = {0, 1})
- **p=5**: Eliminates ~20% of survivors
- **p=7**: Eliminates ~14% of survivors
- Primes p > 20 individually eliminate < 5% each

## Interaction Effects

The modular constraints from different primes are approximately independent
(by Chinese Remainder Theorem), so the combined filtering rate is roughly
the product of individual rates. However, exact independence fails because
the Pythagorean triple structure creates correlations between residue classes.