"""Information-theoretic upper bound on gamma_2 via entropy arguments.

Key insight: If we view the LCS matching positions as a "code" that encodes
information about the alignment between two random strings, information-theoretic
limits constrain how long the LCS can be.

Approach 1: Kolmogorov complexity / source coding bound
  Given strings X and Y of length n with LCS of length L:
  - The matching (alignment) requires specifying:
    (a) Which L positions in X participate (requires log C(n,L) bits)
    (b) Which L positions in Y participate (requires log C(n,L) bits)  
    (c) The actual matched symbols (but these are determined by X at the matched positions)
  - Given the alignment, Y can be recovered from X plus the non-matched bits of Y
  - Since Y is random, K(Y|X) >= n - O(log n)
  - The encoding gives K(Y|X) <= (n-L) + L*H(L/n) + O(log n)
  - This yields gamma_2 <= c where c satisfies c*log(1/c) + (1-c)*log(1/(1-c)) >= c

Approach 2: Deletion channel connection
  The LCS of X and Y can be viewed as a message that passes through a 
  deletion channel from X to Y: each bit of X is either kept (in the LCS)
  or deleted, and then random bits are inserted to form Y.
  The capacity of the binary deletion channel bounds the rate.

Approach 3: Direct entropy bound on LCS distribution
  For each n, compute the exact distribution of LCS(X,Y) for random X,Y.
  Use entropy bounds to constrain the growth rate.

This script implements all three approaches for small n.
"""

import numpy as np
from math import comb, log2, log, factorial
from scipy.special import comb as comb_float
from scipy.optimize import brentq
import json
import time
from pathlib import Path


def h_binary(p):
    """Binary entropy function H(p) = -p*log2(p) - (1-p)*log2(1-p)."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * log2(p) - (1-p) * log2(1-p)


def kolmogorov_upper_bound():
    """Kolmogorov complexity / source coding upper bound.
    
    The argument (following the structure of DP1995, Section 2):
    
    Given X, Y of length n with LCS L:
    - To reconstruct Y from X, we need to specify:
      1. The positions i_1 < i_2 < ... < i_L in X that participate in the LCS
      2. The positions j_1 < j_2 < ... < j_L in Y that participate in the LCS
      3. The n-L bits of Y not in the LCS
    
    This requires at most:
      log2(C(n,L)) + log2(C(n,L)) + (n-L) bits
    
    Since Y is a random string, K(Y) >= n - O(log n) on average.
    Also K(Y|X, alignment) = n - L (the non-matched bits).
    And K(alignment) <= 2*log2(C(n,L)).
    
    By the chain rule: n <= K(alignment) + K(Y|X,alignment) + O(log n)
                        n <= 2*log2(C(n,L)) + (n-L) + O(log n)
    
    So: L <= 2*log2(C(n,L)) + O(log n)
        L/n <= 2*log2(C(n,L/n*n)) / n + O(log n / n)
    
    Using Stirling: log2(C(n,c*n)) / n ≈ H(c) where H is binary entropy
    
    So: c <= 2*H(c) + o(1) where c = L/n = gamma_2
    
    Solving c <= 2*H(c): c - 2*H(c) <= 0
    """
    def f(c):
        return c - 2 * h_binary(c)
    
    # f(0) = 0, f(1) = 1 - 0 = 1, f decreasing then increasing
    # We need the largest c where f(c) <= 0
    
    # Check: f(0.5) = 0.5 - 2*1 = -1.5 < 0
    # f(0.9) = 0.9 - 2*H(0.9) = 0.9 - 2*0.469 = 0.9 - 0.938 = -0.038 < 0
    # f(0.95) = 0.95 - 2*H(0.95) = 0.95 - 2*0.286 = 0.95 - 0.572 = 0.378 > 0
    
    # Find the zero crossing
    c_upper = brentq(f, 0.5, 0.999)
    
    return c_upper


def refined_kolmogorov_bound():
    """Refined Kolmogorov bound using monotone alignment structure.
    
    The alignment (i_1,...,i_L), (j_1,...,j_L) must satisfy:
    - i_1 < i_2 < ... < i_L (monotone increasing in X)
    - j_1 < j_2 < ... < j_L (monotone increasing in Y)
    
    Moreover, the alignment is a monotone lattice path in the n x n grid.
    The number of such paths is C(2n, n) / (n+1) (Catalan number) for paths
    from (0,0) to (n,n). But the LCS path is more constrained.
    
    A tighter encoding: specify the alignment as a monotone path in the DP grid.
    The path has 2n-L steps (n-L down-right steps from X, n-L right-down from Y,
    and L diagonal match steps). The path is a word over {D, R, M} of specific lengths.
    
    Number of such words: (2n-L)! / ((n-L)! * (n-L)! * ... ) -- more precisely,
    the multinomial count but with the monotonicity constraint.
    
    The key insight: the number of monotone alignments with L matches is
    C(n,L)^2 * C(L,L) = C(n,L)^2 (choosing positions in X and Y separately).
    But this over-counts because not all such choices lead to valid alignments
    (we need x_{i_k} = y_{j_k} for all k, which is automatically satisfied for
    the LCS but restricts the encoding).
    
    Refined bound: Given the alignment positions, we DON'T need to specify the
    matched characters (they're determined by X). So:
    
    K(Y|X) = (n-L) bits (the non-matched bits of Y)
    K(alignment) <= 2*log2(C(n,L)) bits
    
    But the alignment is also constrained by the monotonicity. If we encode it
    as a sequence of moves {skip_X, skip_Y, match}, the number of such sequences is:
    
    (2n-L)! / ((n-L)! * (n-L)! * 0!) -- no, this isn't right either.
    
    The walk from (0,0) to (n,n) consists of:
    - L diagonal (match) steps
    - (n-L) right (skip_X) steps
    - (n-L) down (skip_Y) steps
    Total steps: L + (n-L) + (n-L) = 2n - L
    
    Number of such walks: (2n-L)! / (L! * (n-L)! * (n-L)!)
    
    So K(alignment) <= log2((2n-L)! / (L! * (n-L)!^2))
    
    Using Stirling: K(alignment)/n <= (2-c)*H_3(c/(2-c), (1-c)/(2-c), (1-c)/(2-c))
    where c = L/n and H_3 is the ternary entropy.
    """
    def encoding_rate(c):
        """Bits per character for the alignment encoding."""
        if c <= 0 or c >= 1:
            return 0.0
        # Walk length per n: (2-c)
        # Proportions: match = c/(2-c), skip_x = (1-c)/(2-c), skip_y = (1-c)/(2-c)
        p_m = c / (2 - c)
        p_sx = (1 - c) / (2 - c)
        p_sy = (1 - c) / (2 - c)
        # Entropy of the walk (per step) times steps per character
        walk_entropy = -p_m * log2(p_m) - p_sx * log2(p_sx) - p_sy * log2(p_sy)
        return (2 - c) * walk_entropy
    
    def f(c):
        """c = gamma_2. We need:
        n >= K(alignment) + K(Y|X,alignment)
        n >= encoding_rate(c) * n + (1-c) * n
        1 >= encoding_rate(c) + (1-c)
        c >= encoding_rate(c)
        """
        return c - encoding_rate(c)
    
    # Find the largest c where f(c) <= 0 (i.e., the bound is satisfied)
    # f(0.5) = 0.5 - encoding_rate(0.5)
    # encoding_rate(0.5) = 1.5 * H_3(1/3, 1/3, 1/3) = 1.5 * log2(3) ≈ 2.377 -- too large!
    # 
    # Wait, f(c) should be: c <= encoding_rate(c) fails, so the upper bound is where
    # encoding_rate(c) <= c first fails... Actually, the information inequality is:
    # 
    # n >= K(Y) >= K(Y|X) >= K(Y|X, alignment) = n - L (non-matched bits of Y)
    # And: K(Y) <= K(alignment, Y|X,alignment) + O(log n) = K(alignment) + (n-L) + O(log n)
    # So: n <= K(alignment) + (n-L) + O(log n)
    #     L <= K(alignment) + O(log n)
    #     c <= encoding_rate(c) / n ... no, encoding_rate gives bits/character
    
    # Let me redo this. K(alignment) <= encoding_rate(c) * n (total bits for alignment).
    # Then: L <= K(alignment) + O(log n)  =>  c*n <= encoding_rate(c) * n + O(log n)
    # So: c <= encoding_rate(c) + o(1)
    # The upper bound is the largest c where c <= encoding_rate(c)
    
    # Check numerical values
    for c in [0.5, 0.7, 0.8, 0.85, 0.9, 0.95]:
        er = encoding_rate(c)
        print(f"  c={c}: encoding_rate={er:.6f}, c-encoding_rate={c-er:.6f}")
    
    # Find zero of c - encoding_rate(c)
    try:
        c_upper = brentq(lambda c: c - encoding_rate(c), 0.9, 0.999)
    except ValueError:
        # If encoding_rate > c for all c < 1, the bound is trivial
        c_upper = 1.0
    
    return c_upper, encoding_rate


def deletion_channel_bound():
    """Upper bound via deletion channel capacity.
    
    Connection: Consider a binary deletion channel with deletion probability d.
    A transmitted bit survives with probability (1-d). For d=1/2:
    
    If X is a random binary string and Y is obtained by deleting each bit of X
    independently with probability 1/2, then the LCS(X, Y) >= length(Y) trivially
    (since Y is a subsequence of X).
    
    For two INDEPENDENT random strings X, Y: the situation is different.
    The LCS(X,Y) corresponds to the longest sequence that could be transmitted
    through a deletion channel from X to Y and from Y to X.
    
    The precise connection (Kash et al. 2011):
    If we have a code C ⊂ {0,1}^n that is zero-error decodable after 
    p*n adversarial deletions, then for any two codewords c, c':
    LCS(c, c') <= (1-2δ)*n for some δ depending on the code rate.
    
    Contrapositive: if gamma_2 > 1/2 + δ for some δ, then there exist long
    binary strings whose LCS is > (1/2 + δ)*n, which limits the zero-error
    capacity of the deletion channel.
    
    The known bound (Guruswami-He-Li 2021):
    The zero-rate threshold for adversarial deletions is < 1/2.
    This means gamma_2 > 1/2 (which we already know).
    
    For the random (not adversarial) deletion channel with d=1/2:
    Capacity C(1/2) <= 0.4943 (Cheraghchi 2019)
    
    The relationship gamma_2 <= f(C(1/2)) where f needs to be derived.
    
    Key insight: For random X of length n, the number of distinct subsequences
    of X of length L is at most C(n, L). But actually it's at most 2^L.
    If gamma_2 * n characters of X and Y agree, this means there's a common
    subsequence of length gamma_2 * n. The probability that a random Y has
    an LCS of length L with a fixed X is related to the capacity.
    
    A simple bound: C(1/2) >= I(X; LCS) / n. If we can bound I(X; LCS) from
    below in terms of gamma_2, we get an upper bound.
    
    For now, let's compute I(X; LCS) for small n numerically.
    """
    # Compute mutual information I(X; LCS(X,Y)) for small n
    results = {}
    
    for n in range(1, 13):
        # Enumerate all X, Y pairs
        num_strings = 1 << n
        
        # For each X, compute the distribution of LCS(X, random Y)
        # Then compute I(X; LCS(X,Y))
        
        # P(LCS=l | X=x) for each x and l
        lcs_dist_given_x = {}
        
        for x in range(num_strings):
            x_bits = [(x >> i) & 1 for i in range(n)]
            lcs_counts = {}
            
            for y in range(num_strings):
                y_bits = [(y >> i) & 1 for i in range(n)]
                
                # Compute LCS length
                prev = [0] * (n + 1)
                for i in range(n):
                    curr = [0] * (n + 1)
                    for j in range(n):
                        if x_bits[i] == y_bits[j]:
                            curr[j+1] = prev[j] + 1
                        else:
                            curr[j+1] = max(prev[j+1], curr[j])
                    prev = curr
                
                l = prev[n]
                lcs_counts[l] = lcs_counts.get(l, 0) + 1
            
            lcs_dist_given_x[x] = lcs_counts
        
        # P(LCS=l) marginal distribution
        lcs_marginal = {}
        for x, counts in lcs_dist_given_x.items():
            for l, c in counts.items():
                lcs_marginal[l] = lcs_marginal.get(l, 0) + c
        total = sum(lcs_marginal.values())
        for l in lcs_marginal:
            lcs_marginal[l] /= total
        
        # H(LCS)
        H_lcs = -sum(p * log2(p) for p in lcs_marginal.values() if p > 0)
        
        # H(LCS | X) = E_x[H(LCS | X=x)]
        H_lcs_given_x = 0
        for x in range(num_strings):
            counts = lcs_dist_given_x[x]
            total_x = sum(counts.values())
            h_x = -sum((c/total_x) * log2(c/total_x) for c in counts.values() if c > 0)
            H_lcs_given_x += h_x / num_strings
        
        I_x_lcs = H_lcs - H_lcs_given_x
        
        results[n] = {
            "n": n,
            "H_LCS": round(H_lcs, 8),
            "H_LCS_given_X": round(H_lcs_given_x, 8),
            "I_X_LCS": round(I_x_lcs, 8),
            "I_X_LCS_per_n": round(I_x_lcs / n, 8),
            "lcs_distribution": {str(l): round(p, 8) for l, p in sorted(lcs_marginal.items())}
        }
    
    return results


def main():
    print("Information-Theoretic Upper Bound Analysis")
    print("=" * 60)
    
    # 1. Basic Kolmogorov bound
    print("\n1. Kolmogorov complexity bound:")
    kol_bound = kolmogorov_upper_bound()
    print(f"   gamma_2 <= {kol_bound:.8f} (from c <= 2*H(c))")
    print(f"   Compare: Lueker's 0.826280")
    
    # 2. Refined bound using monotone alignment encoding
    print("\n2. Refined Kolmogorov bound (monotone alignment):")
    ref_bound, enc_rate = refined_kolmogorov_bound()
    print(f"   gamma_2 <= {ref_bound:.8f}")
    
    # 3. Deletion channel connection
    print("\n3. Deletion channel / mutual information analysis:")
    mi_results = deletion_channel_bound()
    for n in sorted(mi_results.keys()):
        r = mi_results[n]
        print(f"   n={n:>2d}: I(X; LCS)/n = {r['I_X_LCS_per_n']:.6f}")
    
    # Check if I(X;LCS)/n converges and what it implies
    # If I(X;LCS)/n -> c, then by data processing inequality applied to the
    # deletion channel, c <= C_del(gamma_2) where C_del is the capacity
    # of the deletion channel with deletion probability (1-gamma_2).
    # This gives: gamma_2 <= C_del^{-1}(c)
    
    # 4. Novel bound attempt: entropy of alignment
    # For each n, compute the entropy of the alignment (not just the LCS length)
    print("\n4. Alignment entropy analysis (novel):")
    for n in [4, 5, 6, 7, 8]:
        num_strings = 1 << n
        total_alignments = 0
        alignment_counts = {}
        
        for x in range(num_strings):
            x_bits = [(x >> i) & 1 for i in range(n)]
            for y in range(num_strings):
                y_bits = [(y >> i) & 1 for i in range(n)]
                
                # Compute LCS and count optimal alignments
                dp = [[0]*(n+1) for _ in range(n+1)]
                for i in range(1, n+1):
                    for j in range(1, n+1):
                        if x_bits[i-1] == y_bits[j-1]:
                            dp[i][j] = dp[i-1][j-1] + 1
                        else:
                            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                
                L = dp[n][n]
                # Number of optimal alignments (count paths in DP table)
                cnt = [[0]*(n+1) for _ in range(n+1)]
                cnt[0][0] = 1
                for i in range(n+1):
                    for j in range(n+1):
                        if i == 0 and j == 0:
                            continue
                        if i > 0 and j > 0 and x_bits[i-1] == y_bits[j-1] and dp[i][j] == dp[i-1][j-1] + 1:
                            cnt[i][j] += cnt[i-1][j-1]
                        if i > 0 and dp[i][j] == dp[i-1][j]:
                            cnt[i][j] += cnt[i-1][j]
                        if j > 0 and dp[i][j] == dp[i][j-1]:
                            cnt[i][j] += cnt[i][j-1]
                        # Avoid double counting diagonal + horizontal/vertical
                        if i > 0 and j > 0 and dp[i-1][j] == dp[i][j-1] == dp[i][j]:
                            cnt[i][j] -= cnt[i-1][j-1]
                
                num_opt = cnt[n][n]
                total_alignments += num_opt
                alignment_counts[num_opt] = alignment_counts.get(num_opt, 0) + 1
        
        avg_log_alignments = 0
        for x in range(num_strings):
            x_bits = [(x >> i) & 1 for i in range(n)]
            for y in range(num_strings):
                y_bits = [(y >> i) & 1 for i in range(n)]
                dp = [[0]*(n+1) for _ in range(n+1)]
                for i in range(1, n+1):
                    for j in range(1, n+1):
                        if x_bits[i-1] == y_bits[j-1]:
                            dp[i][j] = dp[i-1][j-1] + 1
                        else:
                            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                cnt = [[0]*(n+1) for _ in range(n+1)]
                cnt[0][0] = 1
                for i in range(n+1):
                    for j in range(n+1):
                        if i == 0 and j == 0: continue
                        if i > 0 and j > 0 and x_bits[i-1] == y_bits[j-1] and dp[i][j] == dp[i-1][j-1] + 1:
                            cnt[i][j] += cnt[i-1][j-1]
                        if i > 0 and dp[i][j] == dp[i-1][j]:
                            cnt[i][j] += cnt[i-1][j]
                        if j > 0 and dp[i][j] == dp[i][j-1]:
                            cnt[i][j] += cnt[i][j-1]
                        if i > 0 and j > 0 and dp[i-1][j] == dp[i][j-1] == dp[i][j]:
                            cnt[i][j] -= cnt[i-1][j-1]
                num_opt = max(1, cnt[n][n])
                avg_log_alignments += log2(num_opt)
        
        avg_log_alignments /= (num_strings ** 2)
        
        # The entropy of the alignment is a measure of how much information
        # the LCS carries. Upper bound on gamma_2 requires:
        # encoding_bits = n + avg_log_alignments must be >= n (trivially true)
        # More useful: avg_log_alignments/n is the excess information per character
        
        print(f"   n={n}: avg log2(#optimal alignments) = {avg_log_alignments:.4f}, per char = {avg_log_alignments/n:.4f}")
    
    # Compile results
    output = {
        "description": "Information-theoretic upper bounds on gamma_2",
        "bounds": {
            "kolmogorov_basic": {
                "bound": round(kol_bound, 10),
                "method": "c <= 2*H(c), solving for largest c",
                "rigorous": True,
                "comparison_to_lueker": "weaker" if kol_bound > 0.826280 else "tighter"
            },
            "kolmogorov_refined": {
                "bound": round(ref_bound, 10),
                "method": "c <= (2-c)*H_3(c/(2-c), (1-c)/(2-c), (1-c)/(2-c))",
                "rigorous": True,
                "comparison_to_lueker": "weaker" if ref_bound > 0.826280 else "tighter"
            }
        },
        "mutual_information_analysis": {str(n): mi_results[n] for n in mi_results},
        "proof_document": "See entropy_upper_proof.md for detailed argument"
    }
    
    outpath = Path(__file__).parent / "entropy_upper_results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
