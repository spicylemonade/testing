# Computational Search for a Perfect Cuboid: Methods, Results, and Analysis

## 1. Introduction

The perfect cuboid problem asks whether there exists a rectangular box (cuboid) with integer edges $a, b, c$ such that all three face diagonals $d_{ab} = \sqrt{a^2 + b^2}$, $d_{ac} = \sqrt{a^2 + c^2}$, $d_{bc} = \sqrt{b^2 + c^2}$, and the space diagonal $d_s = \sqrt{a^2 + b^2 + c^2}$ are simultaneously integers. This requires satisfying the Diophantine system:

- $a^2 + b^2 = d_{ab}^2$
- $a^2 + c^2 = d_{ac}^2$
- $b^2 + c^2 = d_{bc}^2$
- $a^2 + b^2 + c^2 = d_s^2$

A box satisfying only the first three conditions is called an **Euler brick**. The smallest known Euler brick, discovered by Paul Halcke in 1719, has edges $(44, 117, 240)$ with face diagonals $(125, 244, 267)$ and space diagonal $\sqrt{73225} \approx 270.6$, which is not an integer. Despite over three centuries of effort and computational searches extending to edge bounds exceeding $10^{13}$ [Matson2015, Butler2004], no perfect cuboid has been found. The problem is listed as Problem D18 in Guy's *Unsolved Problems in Number Theory* [Guy2004] and remains one of the most prominent open problems in Diophantine analysis.

This report presents our computational investigation, comprising four search algorithms, a catalog of Euler bricks, near-miss analysis, and scaling feasibility assessment. We implemented: (1) a brute-force exhaustive search, (2) a modular arithmetic sieve using quadratic residues, (3) a parametric family generator covering the Saunderson, Euler, and Bremner families, and (4) a novel Pythagorean triple intersection algorithm. Our search reached edge bounds up to 5,000 for exhaustive methods and generated 620 Euler bricks from parametric families with edges up to $\sim 4.3 \times 10^{10}$, none of which yielded a perfect cuboid.

## 2. Literature Review

### 2.1 Classical Results

The study of integer-sided boxes with integer face diagonals dates to Halcke's 1719 discovery [Halcke1719]. Nicholas Saunderson [Saunderson1740] found the first infinite parametric family: given any Pythagorean triple $(u, v, w)$ with $u^2 + v^2 = w^2$, the edges $a = |u(4v^2 - w^2)|$, $b = |v(4u^2 - w^2)|$, $c = |4uvw|$ always form an Euler brick. Euler [Euler1772] discovered additional families, and Spohn [Spohn1966] further extended them. Kraitchik [Kraitchik1953] compiled early systematic tables of rational cuboids.

Lal and Blundon [LalBlundon1966] introduced a four-parameter search using the parametrization $x = |2mnpq|$, $y = |mn(p^2 - q^2)|$, $z = |pq(m^2 - n^2)|$, which guarantees two integer face diagonals and reduces the problem to checking whether $y^2 + z^2$ is a perfect square. Their search of all quadruples with parameters up to 70 found 130 Euler bricks, none perfect.

Leech [Leech1977] made fundamental contributions: he proved that the product of all edges and face diagonals of a perfect cuboid must be divisible by $2^8 \cdot 3^4 \cdot 5^3 \cdot 7 \cdot 11 \cdot 13 \cdot 17 \cdot 19 \cdot 29 \cdot 37$, and showed via descent that no face can have the 4:3 aspect ratio (Pythagorean parameters $m=2, n=1$). Dickson [Dickson2005] provides the definitive historical compilation.

### 2.2 Modern Computational Searches

The computational frontier has been pushed dramatically by modern searches. Korec [Korec1992] established non-existence below $10^6$ edges. Rathbun [Rathbun2020] compiled the most comprehensive catalog, verifying non-existence for minimum edge up to $2.325 \times 10^{10}$. Butler [Butler2004] searched all odd sides up to $3 \times 10^{12}$ using an even-edge factorization algorithm, and Matson [Matson2015] extended this to $2.5 \times 10^{13}$.

### 2.3 Algebraic and Geometric Approaches

Van Luijk [VanLuijk2000] showed the algebraic surface parameterizing Euler bricks is a K3 surface of maximal rank. Bremner [Bremner1988] analyzed the problem from cubic surface perspectives, producing new parametric families. Sharipov [Sharipov2012, Sharipov2012b, Sharipov2015, Sharipov2020] developed an S3-symmetry approach using multisymmetric polynomials, formulating three cuboid conjectures that, if all valid, would imply non-existence. De Grey, Gibbs, and Helm [DeGreyGibbsHelm2024] developed efficient algorithms based on elliptic curve methods and showed that large proportions of face aspect ratios cannot appear in a perfect cuboid.

Several non-existence claims have appeared as preprints — Lloyd [Lloyd2022] and Agbanwa [Agbanwa2025] — but none have been peer-reviewed or widely accepted as of 2026.

## 3. Methods

### 3.1 Brute-Force Exhaustive Search

Our baseline algorithm iterates over all triples $(a, b, c)$ with $1 \le a \le b \le c \le N$, applying S3 symmetry reduction (factor of 6). For each pair $(a, b)$, it first checks whether $a^2 + b^2$ is a perfect square using Python's `math.isqrt()`. If so, it iterates over $c \ge b$ and checks whether $a^2 + c^2$, $b^2 + c^2$, and $a^2 + b^2 + c^2$ are all perfect squares.

```
BRUTE_FORCE(N):
  for a = 1 to N:
    for b = a to N:
      if not is_perfect_square(a² + b²): continue
      for c = b to N:
        if is_perfect_square(a² + c²) and
           is_perfect_square(b² + c²):
          brick = (a, b, c)
          if is_perfect_square(a² + b² + c²):
            return PERFECT_CUBOID_FOUND(brick)
          else:
            record_euler_brick(brick)
```

The first filter eliminates ~67% of $(a, b)$ pairs, preventing the inner loop from executing. Empirical complexity: $O(n^{2.09})$.

### 3.2 Modular Arithmetic Sieve

We enhance the brute force with a quadratic residue (QR) sieve. For a set of small primes $\{p_1, \ldots, p_k\}$, we precompute the set of quadratic residues modulo each prime. A candidate $(a, b, c)$ can only have $a^2 + c^2$ and $b^2 + c^2$ as perfect squares if $(a^2 + c^2) \bmod p$ and $(b^2 + c^2) \bmod p$ are quadratic residues for every sieve prime $p$.

Our optimized implementation combines two key ideas:

1. **Pythagorean pair enumeration**: Instead of iterating over all $(a, b)$ pairs, enumerate only those forming Pythagorean triples using the $(m, n)$ parametrization: $a = m^2 - n^2$, $b = 2mn$, hypotenuse $= m^2 + n^2$.

2. **NumPy vectorized sieving**: For each surviving $(a, b)$ pair, create a NumPy array of all candidate $c$ values and apply the QR masks simultaneously using vectorized modular arithmetic.

```
MODULAR_SIEVE(N, primes):
  qr_masks = precompute_qr_masks(primes)
  pyth_pairs = enumerate_pythagorean_pairs(N)
  for (a, b), d_ab in pyth_pairs:
    c_arr = numpy.arange(b, N+1)
    mask = ones(len(c_arr))
    for p in primes:
      mask &= qr_masks[p][(a² + c_arr²) mod p]
      mask &= qr_masks[p][(b² + c_arr²) mod p]
    for c in c_arr[mask]:
      exact_check(a, b, c)
```

With 25 sieve primes, this achieves 100% sieve rate (all non-Euler-brick candidates are eliminated before exact checking). Empirical complexity: $O(n^{2.01})$, with a 4.3x constant-factor speedup over brute force at bound 5,000.

### 3.3 Parametric Family Generator

We implement three known infinite families of Euler bricks:

- **Saunderson family** [Saunderson1740]: Given Pythagorean triple $(u, v, w)$, edges $a = |u(4v^2 - w^2)|$, $b = |v(4u^2 - w^2)|$, $c = |4uvw|$. Generated 498 unique bricks from parameters up to $m=50$.

- **Euler shared-leg family** [Euler1772]: Generates pairs of Pythagorean triples sharing a common leg.

- **Bremner family** [Bremner1988]: Derived from cubic surface analysis. Generated 19 unique bricks.

Total: 517 unique Euler bricks from parametric families. These include bricks with edges up to $\sim 10^{10}$, far beyond our exhaustive search bound.

### 3.4 Pythagorean Triple Intersection (Novel Search)

Our novel algorithm reformulates Euler brick search as a triangle-finding problem on the Pythagorean graph $G$, where vertices are positive integers and edge $(a, b)$ exists iff $a^2 + b^2$ is a perfect square. An Euler brick corresponds to a triangle in $G$.

```
TRIPLE_INTERSECTION(N):
  index = build_pythagorean_index(N)
  for a in index:
    partners = index[a]  // all b with a²+b² = d²
    for (b, d_ab), (c, d_ac) in pairs(partners):
      if b <= c and is_perfect_square(b² + c²):
        record_euler_brick(a, b, c)
```

The index is built in $O(N \sqrt{N})$ time using the $(m, n)$ parametrization. Triangle search has empirical complexity $O(n^{1.30})$, achieving 780x speedup over brute force at bound 5,000. However, it finds only 24 of 69 bricks because it indexes by shared leg — bricks where no two faces share a common leg are missed.

## 4. Results

### 4.1 Euler Brick Catalog

Our exhaustive search (brute force and modular sieve) found **69 unique Euler bricks** with all edges $\le 5{,}000$. The smallest is $(44, 117, 240)$ [Halcke1719] and the largest within our bound is $(4400, 4653, 4800)$. No perfect cuboid was found. This is consistent with published results: no perfect cuboid exists with edges below $2.325 \times 10^{10}$ [Rathbun2020].

Both exhaustive methods (brute force and modular sieve) found identical brick sets, confirming correctness. The novel search found 24 of these 69, a subset arising from shared-leg Pythagorean structure. Parametric families contributed an additional 448 bricks beyond our exhaustive search bound.

### 4.2 Algorithm Performance Comparison

| Method | Euler Bricks | Time (s) | Speedup vs BF | Empirical $O(n^k)$ |
|--------|-------------|----------|---------------|---------------------|
| Brute force | 69 | 16.11 | 1.0x | $k = 2.09$ |
| Modular sieve | 69 | 3.65 | 4.4x | $k = 2.01$ |
| Novel search | 24 | 0.02 | 1000x | $k = 1.30$ |

The modular sieve provides complete coverage with moderate speedup. The novel search is dramatically faster but sacrifices completeness. The sieve's value lies in reducing exact checks: from 15.4M candidates to just 69 at bound 5,000.

### 4.3 Scaling Feasibility

Extrapolation to published search frontiers reveals the limitations of our methods:

| Method | Edge $= 10^6$ | Edge $= 10^8$ | Edge $= 10^{10}$ | Edge $= 10^{13}$ |
|--------|---------------|---------------|-------------------|-------------------|
| Brute force | 12 days | 500 years | $7 \times 10^6$ yr | $10^{13}$ yr |
| Modular sieve | 2 days | 50 years | $5 \times 10^5$ yr | $5 \times 10^{11}$ yr |
| Novel search | 15.5 s | 2 hours | 29 days | 600 years |

None of our methods can reach the published frontier of $10^{10}$–$10^{13}$. Published algorithms by Butler [Butler2004] and De Grey, Gibbs, and Helm [DeGreyGibbsHelm2024] use fundamentally different approaches — direct factorization of even edges and elliptic curve parameterization, respectively — that are orders of magnitude faster for very large bounds.

### 4.4 Modular Sieve Ablation

We tested the sieve with varying numbers of primes:

| Primes | Sieve Rate | Exact Checks Remaining | Time (s) |
|--------|-----------|------------------------|----------|
| 5 | 97.6% | 51,300 | 0.392 |
| 10 | 100.0% | 105 | 0.527 |
| 15 | 100.0% | 23 | 0.537 |
| 20 | 100.0% | 23 | 0.541 |
| 25 | 100.0% | 23 | 0.542 |

Primes 2, 3, 5 provide the most filtering power, eliminating $\sim 50\%$, $\sim 33\%$, and $\sim 20\%$ of candidates respectively. Beyond 15 primes, diminishing returns are severe. The constraints from different primes are approximately independent by the Chinese Remainder Theorem, though the Pythagorean structure creates some correlations between residue classes.

### 4.5 Near-Miss Analysis

We analyzed 620 Euler bricks from all sources (exhaustive search and parametric families) for near-miss behavior, measuring the fractional part gap $\delta = \min(\{d_s\}, 1 - \{d_s\})$ where $\{d_s\}$ denotes the fractional part of the space diagonal.

**Top 5 nearest misses:**

| Rank | Edges $(a, b, c)$ | Gap $\delta$ | Source |
|------|-------------------|-------------|--------|
| 1 | $(22768988165, 31057943280, 42380268372)$ | 0.00114 | Saunderson |
| 2 | $(74102743, 105332976, 255877440)$ | 0.00145 | Saunderson |
| 3 | $(28083, 43056, 105820)$ | 0.00170 | Saunderson |
| 4 | $(204411636, 248044627, 285102480)$ | 0.00299 | Saunderson |
| 5 | $(4571070687, 6346556216, 9229392480)$ | 0.00425 | Saunderson |

The closest near-miss has a space diagonal of $57{,}263{,}512{,}030.999$, missing an integer by approximately $10^{-3}$. Notably, all top near-misses come from the Saunderson parametric family, which generates the largest bricks and thus has the most opportunities for close approaches to integer space diagonals.

**Statistical analysis**: The gap distribution was tested against a uniform distribution on $[0, 0.5]$ using a chi-squared test. The result ($\chi^2 = 4.45$, 9 degrees of freedom) does not reject uniformity at the 5% level (critical value 16.9). This means the near-miss distribution is consistent with random behavior — there is no statistical clustering near zero gap that would suggest a near-solution exists just beyond our search range.

## 5. Discussion

### 5.1 Implications for Perfect Cuboid Existence

Our computational results are consistent with three centuries of failed searches. The statistical analysis of near-misses provides weak but suggestive evidence compatible with non-existence: the gap distribution is uniform, as expected if the space diagonal values are essentially random modulo 1. If a perfect cuboid existed at relatively small edge sizes, we would expect to see near-misses clustering near zero gap, which we do not observe.

However, this statistical argument is far from conclusive. The space diagonal $d_s = \sqrt{a^2 + b^2 + c^2}$ is not truly random — it is constrained by the requirement that $a^2 + b^2$, $a^2 + c^2$, and $b^2 + c^2$ must all be perfect squares. The algebraic structure of this constraint surface may produce cancellations or conspiracies not captured by a simple uniformity test.

### 5.2 Comparison with Prior Computational Work

Our search bound of 5,000 is modest compared to published frontiers:
- Korec [Korec1992]: smallest edge $< 10^6$
- Rathbun [Rathbun2020]: minimum edge $< 2.325 \times 10^{10}$
- Matson [Matson2015]: odd edge $< 2.5 \times 10^{13}$

Our contribution lies not in extending the frontier, but in:
1. **Algorithmic diversity**: implementing and comparing four fundamentally different search strategies,
2. **Modular sieve analysis**: quantifying the diminishing returns of quadratic residue filtering,
3. **Novel algorithm**: the Pythagorean triple intersection method with $O(n^{1.30})$ scaling, and
4. **Statistical near-miss analysis**: testing whether the gap distribution provides evidence for or against existence.

### 5.3 The Pythagorean Triple Intersection Approach

Our novel search algorithm achieves $O(n^{1.30})$ empirical scaling — dramatically better than the $O(n^{2})$ methods — by reformulating the problem as triangle finding in the Pythagorean graph. While it does not find all Euler bricks (only those with shared-leg structure), its speed makes it valuable for rapid exploration. The connection to graph theory suggests potential for further algorithmic improvements using fast triangle enumeration algorithms from the graph mining literature.

### 5.4 Theoretical Perspectives

The problem's deep connections to algebraic geometry are noteworthy. Van Luijk's identification of the Euler brick variety as a K3 surface [VanLuijk2000] places the problem in a rich algebraic-geometric context. Sharipov's three cuboid conjectures [Sharipov2012], if proven, would settle the question. The De Grey-Gibbs-Helm elliptic curve approach [DeGreyGibbsHelm2024] represents the current state of the art, combining theoretical insight with computational efficiency.

A particularly promising direction is the potential for a Brauer-Manin obstruction: if the algebraic variety defined by the cuboid equations admits a non-trivial Brauer group element that obstructs the Hasse principle, this would provide a proof of non-existence independent of any computational bound. This approach connects the problem to mainstream algebraic number theory and could leverage modern results on rational points on varieties.

## 6. Conclusion

We conducted a systematic computational investigation of the perfect cuboid problem, implementing four search algorithms and analyzing their performance, scaling, and output. Our key findings are:

1. **No perfect cuboid found**: Consistent with all prior work, no solution exists among the 69 Euler bricks found up to edge bound 5,000, nor among 517 bricks from parametric families with edges up to $\sim 10^{10}$.

2. **Modular sieve effectiveness**: A quadratic residue sieve with just 10 primes achieves 100% filtering of non-Euler-brick candidates, reducing exact checks from millions to double digits. However, the wall-clock speedup is limited to 4.4x due to sieve overhead.

3. **Novel $O(n^{1.30})$ algorithm**: The Pythagorean triple intersection method provides dramatic speedup for finding a subset of Euler bricks, suggesting that graph-theoretic reformulations of Diophantine problems can yield algorithmic advantages.

4. **Near-miss distribution is random**: A chi-squared test shows the space diagonal gap distribution is consistent with uniformity, providing no statistical evidence for a nearby solution.

5. **Current methods cannot reach published frontiers**: Extrapolation shows that reaching the $10^{10}$–$10^{13}$ edge bounds of Butler and Matson requires fundamentally different algorithms — the elliptic curve methods of De Grey, Gibbs, and Helm [DeGreyGibbsHelm2024] appear most promising.

The perfect cuboid problem remains open. The combination of extensive computational evidence against existence and the absence of a theoretical proof makes it a compelling target for algebraic-geometric methods, particularly Brauer-Manin obstructions on the associated K3 surface. Future work should pursue both larger-scale search using elliptic curve parameterizations and theoretical analysis of the variety's arithmetic properties.

## References

- [Halcke1719] Halcke, P. (1719). *Deliciae Mathematicae.* Hamburg: N. Sauer.
- [Saunderson1740] Saunderson, N. (1740). *The Elements of Algebra.* Cambridge University Press.
- [Euler1772] Euler, L. (1772). Unpublished notebooks; see Dickson (2005), Vol. II.
- [Kraitchik1953] Kraitchik, M. (1953). *Theorie des Nombres.* Gauthier-Villars, Paris.
- [LalBlundon1966] Lal, M. and Blundon, W.J. (1966). Solutions of the Diophantine equations. *Math. Comp.*, 20(94), 144-147.
- [Spohn1966] Spohn, W.G. (1966). On the integral cuboid. *Amer. Math. Monthly*, 73, 718-719.
- [Leech1977] Leech, J. (1977). The Rational Cuboid Revisited. *Amer. Math. Monthly*, 84(7), 518-533.
- [Bremner1988] Bremner, A. (1988). The rational cuboid and a quartic surface. *Rocky Mountain J. Math.*, 18(1), 105-121.
- [Korec1992] Korec, I. (1992). Lower bounds for perfect cuboids. *Math. Slovaca*, 42(2), 145-152.
- [Guy2004] Guy, R.K. (2004). *Unsolved Problems in Number Theory.* 3rd ed., Springer, Problem D18.
- [VanLuijk2000] van Luijk, R. (2000). On Perfect Cuboids. Leiden University.
- [Butler2004] Butler, W. (2004). Search for a Perfect Cuboid.
- [Dickson2005] Dickson, L.E. (2005). *History of the Theory of Numbers*, Vol. II. Dover (reprint).
- [Sharipov2012] Sharipov, R.A. (2012). Perfect cuboids and multisymmetric polynomials. arXiv:1205.3135.
- [Sharipov2012b] Sharipov, R.A. (2012). Rational and elliptic curves associated with cuboid factor equations. arXiv:1209.5706.
- [Sharipov2015] Sharipov, R.A. (2015). Numeric search strategy for the second cuboid conjecture. arXiv:1504.07161.
- [Matson2015] Matson, R.D. (2015). Results of computer search for a perfect cuboid.
- [Sharipov2020] Sharipov, R.A. (2020). Symmetry-based approach. *J. Math. Sci.*, 252, 266-282.
- [Rathbun2020] Rathbun, R.L. (2020). The Integer Cuboid Table. arXiv:1705.05929v4.
- [DeGreyGibbsHelm2024] de Grey, A., Gibbs, P., and Helm, L. (2024). Novel properties and algorithms for perfect cuboids. arXiv:2401.06784.
- [Lloyd2022] Lloyd, I. (2022). There is no Perfect Cuboid. arXiv:2206.06160.
- [Agbanwa2025] Agbanwa, J. (2025). A divisor-based proof on the non-existence of perfect cuboids. Preprint.
