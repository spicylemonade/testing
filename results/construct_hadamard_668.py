#!/usr/bin/env python3
"""
Construct a Hadamard matrix of order 668 = 4 * 167.

Since 167 is prime and 167 ≡ 3 (mod 4), we use the following approach:

Method: Paley Type I gives H(168). We need H(668) = H(4*167).

For order 4p where p is an odd prime with p ≡ 3 (mod 4):
We use the construction based on the Jacobsthal matrix and a specific
block structure that produces a Hadamard matrix of order 4p.

The key construction (due to Paley, with refinements by Williamson and others):

1. Compute the Jacobsthal matrix Q of order p (from quadratic residues of GF(p)).
   Q has entries Q[i,j] = chi(i-j) where chi is the Legendre symbol mod p.
   Q is skew-symmetric (Q^T = -Q) since p ≡ 3 (mod 4).
   Q satisfies Q*Q^T = pI - J where J is the all-ones matrix.

2. Form the 4p × 4p Hadamard matrix using a specific block construction.

Actually, let's use the most well-known and reliable method:

The Paley Type I construction gives H(p+1) = H(168) for p=167.
Then H(4) ⊗ H(168) gives order 672, not 668.

For order 668 = 4*167 exactly, we use the construction of 
Goethals-Seidel type with the conference/Jacobsthal matrix of order 167.

The construction uses the fact that for p prime, p ≡ 3 (mod 4),
we can construct a Hadamard matrix of order 2(p+1) using the Paley Type II
construction (giving 336), and one of order p+1 using Paley Type I (giving 168).

For 668 = 4*167, we use the following known result:
A Hadamard matrix of order 4p exists for every prime p ≡ 3 (mod 4).
This uses the "quadratic residue" construction with supplementary 
difference sets derived from the quadratic residues and non-residues of GF(p).

Specifically, we use the Goethals-Seidel array construction:
H = [[A*R, B*R, C*R, D*R],
     [-B*R, A*R, D*R, -C*R],  (with appropriate signs)
     [-C*R, -D*R, A*R, B*R],
     [-D*R, C*R, -B*R, A*R]]

where A, B, C, D are circulant ±1 matrices of order p=167 satisfying:
A*A^T + B*B^T + C*C^T + D*D^T = 4p*I

and R is the back-circulant matrix (reversal permutation).

For primes p ≡ 3 (mod 4), the four matrices can be constructed from
the quadratic residues of GF(p) using supplementary difference sets.
"""

import numpy as np
import sys
import time


def legendre_symbol(a, p):
    """Compute the Legendre symbol (a/p)."""
    if a % p == 0:
        return 0
    val = pow(a, (p - 1) // 2, p)
    return val if val == 1 else -1


def jacobsthal_matrix(p):
    """
    Construct the p×p Jacobsthal matrix Q for prime p.
    Q[i,j] = chi(j - i) where chi is the Legendre symbol mod p.
    """
    Q = np.zeros((p, p), dtype=np.int8)
    for i in range(p):
        for j in range(p):
            Q[i, j] = legendre_symbol((j - i) % p, p)
    return Q


def back_circulant_matrix(n):
    """
    Construct the n×n back-circulant (reversal) permutation matrix R.
    R[i,j] = 1 if (i+j) ≡ 0 (mod n), else 0.
    This is the matrix that reverses the order of elements.
    """
    R = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        R[i, (n - i) % n] = 1
    return R


def circulant_from_first_row(first_row):
    """Build a circulant matrix from its first row."""
    n = len(first_row)
    C = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            C[i, j] = first_row[(j - i) % n]
    return C


def construct_goethals_seidel_quadruple_from_qr(p):
    """
    For prime p ≡ 3 (mod 4), construct four ±1 sequences of length p
    whose circulant matrices satisfy AA^T + BB^T + CC^T + DD^T = 4p*I.
    
    Uses the classical construction based on quadratic residues.
    
    Let Q be the set of non-zero quadratic residues mod p.
    Let N be the set of quadratic non-residues mod p.
    
    We define the first rows of A, B, C, D as follows.
    
    For p ≡ 3 (mod 4), the Legendre symbol chi satisfies chi(-1) = -1,
    so the QR set is "skew" (if r is a QR, -r is a non-residue).
    
    The classical supplementary difference set construction:
    - a_j = chi(j) for j ≠ 0, a_0 = 1  (first row of A)
    - b_j = chi(j) for j ≠ 0, b_0 = 1  (first row of B) 
    - c_j = chi(j) for j ≠ 0, c_0 = 1  (first row of C)
    - d_j = 1 for all j                  (first row of D)
    
    This doesn't work directly. We need a more sophisticated construction.
    """
    # The standard 4-{p; p; p; p; 2(p-1)} supplementary difference sets
    # For p ≡ 3 (mod 4), one known construction uses:
    #   D1 = Q (quadratic residues)
    #   D2 = Q  
    #   D3 = Q
    #   D4 = Z_p \ {0}  (all nonzero elements)
    # But this doesn't directly give ±1 circulant matrices satisfying the condition.
    
    # Let's use a different, well-established approach.
    pass


def construct_hadamard_4p_direct(p):
    """
    Direct construction of a Hadamard matrix of order 4p for prime p ≡ 3 (mod 4).
    
    Uses the construction from:
    R.E.A.C. Paley, "On orthogonal matrices" (1933)
    Combined with the Goethals-Seidel array.
    
    The construction:
    1. Build the Jacobsthal matrix Q of order p.
       Q is skew-symmetric: Q^T = -Q
       Q*Q^T = pI - J (where J = all-ones matrix)
       
    2. Let e be the all-ones column vector of length p.
    3. Construct the (p+1)×(p+1) skew conference matrix S:
       S = [[0, e^T], [-e, Q]]
       (adjusted sign convention to make it skew: S^T = -S)
       S satisfies S*S^T = pI_{p+1}... no, S*S^T = (p+1)I - J for conference matrix.
    
    Actually, for the 4p construction, let's use a well-known explicit method.
    
    Method (Mukhopadhyay / Wallis):
    For p prime, p ≡ 3 (mod 4), define the 4p × 4p matrix using blocks based on
    the Jacobsthal matrix.
    """
    
    # For p ≡ 3 (mod 4), the Jacobsthal matrix Q is skew-symmetric
    Q = jacobsthal_matrix(p)
    
    # Verify skew symmetry
    assert np.allclose(Q, -Q.T), "Q should be skew-symmetric for p ≡ 3 mod 4"
    
    # Q satisfies Q*Q^T = pI - J where J is all-ones
    I_p = np.eye(p, dtype=np.int64)
    J_p = np.ones((p, p), dtype=np.int64)
    QQt = Q.astype(np.int64) @ Q.T.astype(np.int64)
    expected = p * I_p - J_p
    assert np.allclose(QQt, expected), "Q*Q^T should equal pI - J"
    
    print(f"Jacobsthal matrix Q of order {p} constructed and verified.")
    print(f"  Q is skew-symmetric: True")
    print(f"  Q*Q^T = {p}*I - J: True")
    
    # Now use the Goethals-Seidel construction with four circulant matrices.
    # For p ≡ 3 (mod 4), the first rows are defined by:
    # 
    # a = [1, chi(1), chi(2), ..., chi(p-1)]  (Legendre symbols, a_0 = 1)
    # b = [1, chi(1), chi(2), ..., chi(p-1)]  (same as a)
    # c = [1, chi(1), chi(2), ..., chi(p-1)]  (same as a)  
    # d = [1, 1, 1, ..., 1]                    (all ones)
    #
    # But this gives the same matrix 3 times plus J, which has:
    # 3*A*A^T + J*J^T = 3(pI - J + I_adjusted) + pJ
    # This doesn't immediately work. Let me use the correct construction.
    
    # The correct Williamson-type construction for p ≡ 3 (mod 4):
    # We need four symmetric circulant matrices. But for p ≡ 3 (mod 4),
    # chi(-1) = -1, so the Legendre-symbol-based circulant is SKEW, not symmetric.
    
    # For the Goethals-Seidel array (which doesn't require symmetry):
    # H = [[ A,  BR,  CR,  DR],
    #      [-BR,  A, -D^TR, C^TR],
    #      [-CR, D^TR,  A, -B^TR],
    #      [-DR, -C^TR, B^TR, A]]
    # where R is the back-circulant matrix.
    # For circulant matrices, C*R = R*C^T, so CR is symmetric.
    
    # The key: we need AA^T + BB^T + CC^T + DD^T = 4pI
    
    # For the specific case of p ≡ 3 (mod 4) prime, use:
    # Let chi be the Legendre symbol, and define first rows:
    #   a_0 = 1,  a_j = chi(j) for j=1,...,p-1
    #   b_0 = -1, b_j = chi(j) for j=1,...,p-1  
    #   c_0 = -1, c_j = chi(j) for j=1,...,p-1
    #   d_0 = -1, d_j = -chi(j) for j=1,...,p-1
    
    # Actually, let me use a cleaner and more standard approach.
    # The following is based on the Paley construction of order 4p.
    
    return _construct_via_block_paley(p, Q)


def _construct_via_block_paley(p, Q):
    """
    Construct H(4p) using a block matrix approach with the Jacobsthal matrix.
    
    This uses the construction where:
    - We have the p×p Jacobsthal matrix Q (skew-symmetric for p ≡ 3 mod 4)
    - We form a 4p×4p matrix using a 4×4 block structure with p×p blocks
    
    The construction is based on:
    
    Let I = identity, J = all-ones, Q = Jacobsthal matrix.
    Define:
      A = I + Q    (has 1 on diagonal, chi(j-i) elsewhere)
      B = I - Q    (has 1 on diagonal, -chi(j-i) elsewhere)
    
    Note: A + B = 2I, A - B = 2Q
    For p ≡ 3 mod 4: A^T = I + Q^T = I - Q = B, so B = A^T.
    
    A*A^T = (I+Q)(I-Q) = I - Q^2 = I - (J-pI) = (p+1)I - J
    (using Q*Q^T = Q*(-Q) = -Q^2, and Q^2 = -(Q*Q^T) = -(pI-J) = -pI+J,
     actually Q^T = -Q so Q*Q^T = Q*(-Q) = -Q^2,
     and Q^2: since Q is skew-symmetric, Q^2 is symmetric negative semi-definite.
     Q*Q^T = -Q^2, and Q*Q^T = pI - J, so Q^2 = -(pI - J) = J - pI.)
    
    So A*A^T = (I+Q)(I+Q)^T = (I+Q)(I-Q) = I - Q^2 = I - (J-pI) = (1+p)I - J.
    And A*A^T has eigenvalue (1+p) with multiplicity (p-1) and eigenvalue 1 for the all-ones vector.
    
    Now, define the 4p × 4p matrix:
    
    H = [[ j⊗I+i⊗Q,   j⊗I-i⊗Q,   j⊗I+i⊗Q,   j⊗I-i⊗Q  ],
         [...                                                   ]]
    
    Hmm, this is getting complicated. Let me use a more direct approach.
    
    The simplest known construction for H(4p), p ≡ 3 (mod 4) prime:
    
    We use the (p+1)×(p+1) Paley conference matrix and double it.
    
    Actually, the simplest path: 
    Paley Type I gives H(p+1) = H(168).
    H(4) is trivial.
    668 = 4 × 167. Since 167 is NOT a valid Hadamard order (not divisible by 4 for n>2),
    we can't use simple Kronecker.
    
    But: 668 = 2 × 334 = 2 × 2 × 167. Again 167 is not a Hadamard order.
    
    The correct approach: use the DIRECT construction for order 4p.
    
    The Paley graph on p vertices gives us the Jacobsthal/QR matrix Q.
    From Q, we build a Hadamard matrix of order 4p using:
    
    H = [[S, S, S, -S],
         [S, S, -S, S],
         [S, -S, S, S],
         [-S, S, S, S]]    (Hadamard matrix of order 4 tensored structure)
    
    But S needs to be (somehow) a p×p matrix... This is not quite right either.
    
    OK, let me just implement the classical construction properly.
    """
    
    # THE CORRECT CLASSICAL CONSTRUCTION for H(4p), p prime, p ≡ 3 (mod 4):
    #
    # We use the Goethals-Seidel array with four circulant matrices derived
    # from the Legendre symbol.
    #
    # Define sequences of length p:
    #   x_j = Legendre(j, p) for j = 0, 1, ..., p-1  (x_0 = 0)
    #
    # Then define four ±1 sequences:
    #   a_j = 1                    for all j  (all-ones)
    #   b_j = x_j if j≠0, else 1  (Legendre with center 1)
    #   c_j = x_j if j≠0, else 1  (same)
    #   d_j = x_j if j≠0, else -1 (Legendre with center -1)
    #
    # Hmm, let me look at this more carefully with the NFFT condition.
    #
    # For circulant matrices C_a, C_b, C_c, C_d with first rows a, b, c, d:
    # C_a * C_a^T + C_b * C_b^T + C_c * C_c^T + C_d * C_d^T = 4p * I_p
    #
    # In the Fourier domain (using DFT):
    # |â(k)|^2 + |b̂(k)|^2 + |ĉ(k)|^2 + |d̂(k)|^2 = 4p for all k
    #
    # For the all-ones sequence a: â(0) = p, â(k) = 0 for k≠0. So |â(k)|^2 = p^2 for k=0, 0 otherwise.
    # For the Legendre-based sequence b (with b_0 = s):
    #   b̂(k) = s + sum_{j=1}^{p-1} chi(j) * omega^{jk}
    #   For k≠0: b̂(k) = s + chi(k)*G where G = sum_{j=1}^{p-1} chi(j)*omega^j is the Gauss sum
    #   |G|^2 = p, and for p ≡ 3 mod 4, G = i*sqrt(p)
    #   So |b̂(k)|^2 = |s + chi(k)*i*sqrt(p)|^2 = s^2 + p (when s = ±1)
    #
    # For k=0: b̂(0) = s + sum chi(j) = s + 0 = s. So |b̂(0)|^2 = 1.
    #
    # With a = all-ones, b = c = (1, chi(1),...,chi(p-1)), d = (-1, chi(1),...,chi(p-1)):
    # k=0: p^2 + 1 + 1 + 1 = p^2 + 3 ≠ 4p for most p.
    # k≠0: 0 + (1+p) + (1+p) + (1+p) = 3(1+p) ≠ 4p for most p.
    #
    # So this naive assignment doesn't work. Let me find the correct one.
    
    # CORRECT APPROACH: Use a known construction that actually works.
    # 
    # For p ≡ 3 (mod 4), the following quadruple works for Goethals-Seidel:
    # (From Wallis, "Combinatorics: Room Squares, Sum-Free Sets, Hadamard Matrices")
    #
    # Define T-matrices or use the "two circulant" Hadamard construction.
    #
    # Actually, the most reliable known construction for H(2(q+1)) where q is 
    # a prime power ≡ 1 (mod 4) uses Paley Type II.
    # For H(q+1) where q ≡ 3 (mod 4), Paley Type I.
    #
    # For H(4p) with p ≡ 3 (mod 4) prime, we can use:
    # H(4) ⊗ H(p+1) gives order 4(p+1) = 4*168 = 672 ≠ 668.
    #
    # So we genuinely need the Goethals-Seidel or Williamson construction
    # with four circulants of order 167.
    #
    # Let me implement the CORRECT four-circulant construction.
    pass


def construct_hadamard_668():
    """
    Construct a Hadamard matrix of order 668 using the Goethals-Seidel construction
    with four circulant matrices of order 167.
    
    For p = 167 (prime, p ≡ 3 mod 4), we need to find four ±1 sequences
    a, b, c, d of length 167 such that the four circulant matrices satisfy:
    
    C_a C_a^T + C_b C_b^T + C_c C_c^T + C_d C_d^T = 668 I_{167}
    
    In the DFT domain, this means for each frequency k:
    |â(k)|² + |b̂(k)|² + |ĉ(k)|² + |d̂(k)|² = 668
    
    For p = 167, this equals 4 * 167 = 668.
    """
    p = 167
    
    # Compute Legendre symbols
    chi = np.zeros(p, dtype=int)
    for j in range(1, p):
        chi[j] = legendre_symbol(j, p)
    # chi[0] = 0
    
    # Compute the Gauss sum G = sum_{j=1}^{p-1} chi(j) * omega^j
    # For p ≡ 3 (mod 4): G = i * sqrt(p)
    
    # The key insight for 4-{p} supplementary difference sets:
    # 
    # We need four subsets S1, S2, S3, S4 of Z_p such that
    # for every nonzero d in Z_p:
    # sum_{i=1}^{4} |{(s1,s2) in Si×Si : s1-s2=d}| = 4p - 4|Si|... 
    # (this is the SDS condition)
    #
    # For p ≡ 3 mod 4 prime, the following works:
    # S1 = S2 = S3 = Q (quadratic residues, |Q| = (p-1)/2 = 83)
    # S4 = Z_p* = {1,...,p-1} (all nonzero elements, |S4| = p-1 = 166)
    #
    # Convert to ±1 sequences: +1 if j in Si, -1 if j not in Si.
    # For S1=S2=S3=Q: a_j = chi(j) for j≠0, a_0 = -1 (0 not in Q)
    # For S4=Z_p*:    d_j = 1 for j≠0, d_0 = -1
    
    # Let's verify this gives the right row sums in the power spectral condition.
    # Build the ±1 sequences
    
    # Quadratic residues
    QR = set()
    for j in range(1, p):
        if chi[j] == 1:
            QR.add(j)
    
    print(f"Number of quadratic residues mod {p}: {len(QR)}")
    print(f"Expected: {(p-1)//2} = {(p-1)//2}")
    
    # Method: Try the construction where we use supplementary difference sets.
    # For the Goethals-Seidel array, we need:
    # For each nonzero d mod p:
    #   N_A(d) + N_B(d) + N_C(d) + N_D(d) = 4k - (4p - 4·1)/something...
    
    # Actually, let me just try multiple candidate quadruples and verify numerically.
    
    # APPROACH 1: Three copies of Legendre + all-ones
    # a_j = b_j = c_j = chi(j) for j≠0, = -1 for j=0
    # d_j = 1 for all j
    
    a = np.array([-1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    b = np.array([-1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    c = np.array([-1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    d = np.ones(p, dtype=np.int8)
    
    if check_quadruple(a, b, c, d, p):
        print("APPROACH 1 works!")
        return build_goethals_seidel(a, b, c, d, p)
    
    # APPROACH 2: Three copies of Legendre (center +1) + all-ones
    a2 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    b2 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    c2 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    d2 = np.ones(p, dtype=np.int8)
    
    if check_quadruple(a2, b2, c2, d2, p):
        print("APPROACH 2 works!")
        return build_goethals_seidel(a2, b2, c2, d2, p)
    
    # APPROACH 3: Two Legendre (center +1) + one Legendre (center -1) + all-ones
    a3 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    b3 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    c3 = np.array([-1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    d3 = np.ones(p, dtype=np.int8)
    
    if check_quadruple(a3, b3, c3, d3, p):
        print("APPROACH 3 works!")
        return build_goethals_seidel(a3, b3, c3, d3, p)
    
    # APPROACH 4: One Legendre + one neg-Legendre + all ones + all ones
    a4 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    b4 = np.array([-1] + [-chi[j] for j in range(1, p)], dtype=np.int8)
    c4 = np.ones(p, dtype=np.int8)
    d4 = np.ones(p, dtype=np.int8)
    
    if check_quadruple(a4, b4, c4, d4, p):
        print("APPROACH 4 works!")
        return build_goethals_seidel(a4, b4, c4, d4, p)
    
    # APPROACH 5: Based on the Szekeres difference sets
    # For p ≡ 3 (mod 4), define:
    # C0 = {0}
    # C+ = quadratic residues (QR) 
    # C- = quadratic non-residues (QNR)
    # Then construct:
    # a: +1 on C+ ∪ {0}, -1 on C-
    # b: +1 on C+ ∪ {0}, -1 on C-  (same as a)
    # c: +1 on C- ∪ {0}, -1 on C+  (negated non-zero part)
    # d: -1 on {0}, +1 elsewhere
    
    a5 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    b5 = np.array([1] + [chi[j] for j in range(1, p)], dtype=np.int8)
    c5 = np.array([1] + [-chi[j] for j in range(1, p)], dtype=np.int8)
    d5 = np.array([-1] + [1]*(p-1), dtype=np.int8)
    
    if check_quadruple(a5, b5, c5, d5, p):
        print("APPROACH 5 works!")
        return build_goethals_seidel(a5, b5, c5, d5, p)
    
    # APPROACH 6: Systematic search using DFT condition
    # For each frequency k, |â(k)|² + |b̂(k)|² + |ĉ(k)|² + |d̂(k)|² = 4p
    # Use the Legendre-based structure with different center values
    print("\nStarting systematic DFT-based search...")
    return systematic_dft_search(chi, p)


def check_quadruple(a, b, c, d, p):
    """Check if four sequences satisfy the circulant orthogonality condition."""
    # Build circulant matrices and check
    n = len(a)
    
    # Use DFT for efficiency
    a_hat = np.fft.fft(a.astype(np.complex128))
    b_hat = np.fft.fft(b.astype(np.complex128))
    c_hat = np.fft.fft(c.astype(np.complex128))
    d_hat = np.fft.fft(d.astype(np.complex128))
    
    power_sum = np.abs(a_hat)**2 + np.abs(b_hat)**2 + np.abs(c_hat)**2 + np.abs(d_hat)**2
    target = 4 * p
    
    error = np.max(np.abs(power_sum - target))
    print(f"  Max power spectral error: {error:.6f} (target: {target})")
    
    if error < 0.01:
        return True
    
    # Print the power spectrum for debugging
    print(f"  Power spectrum at k=0: {power_sum[0]:.1f} (target: {target})")
    if n > 1:
        print(f"  Power spectrum at k=1: {power_sum[1]:.1f} (target: {target})")
        print(f"  Min power: {np.min(power_sum.real):.1f}, Max power: {np.max(power_sum.real):.1f}")
    
    return False


def systematic_dft_search(chi, p):
    """
    Systematic search for the correct quadruple using DFT analysis.
    
    For p prime, p ≡ 3 mod 4, the Gauss sum G = sum chi(j)*omega^j satisfies:
    G = i*sqrt(p) (up to sign).
    
    For a Legendre-based sequence x with x_0 = s (±1) and x_j = chi(j) for j≠0:
    x̂(0) = s + 0 = s  (since sum of chi(j) for j=1..p-1 is 0)
    x̂(k) = s + chi(k)*G for k≠0  (using multiplicative property of Gauss sums)
    |x̂(k)|² = s² + p + 2s*Re(chi(k)*G) for k≠0
    
    Since G = i*sqrt(p) (for p ≡ 3 mod 4):
    Re(chi(k)*G) = Re(chi(k)*i*sqrt(p))
    If chi(k) = 1: Re(i*sqrt(p)) = 0
    If chi(k) = -1: Re(-i*sqrt(p)) = 0
    
    So |x̂(k)|² = 1 + p for k≠0 (regardless of s and chi(k))!
    And |x̂(0)|² = 1.
    
    For the all-ones sequence j:
    ĵ(0) = p, ĵ(k) = 0 for k≠0.
    |ĵ(k)|² = p² for k=0, 0 for k≠0.
    
    For the negated Legendre sequence y = -x (negated):
    |ŷ(k)|² = |x̂(k)|² (same power spectrum).
    
    So with m copies of Legendre-type sequences and (4-m) copies of all-ones:
    k=0: m*1 + (4-m)*p² = 4p needed
    k≠0: m*(1+p) + 0 = 4p needed → m(1+p) = 4p → m = 4p/(1+p)
    
    For p=167: m = 668/168 = 3.976... ≈ 4 but not exactly 4.
    With m=4: k≠0 gives 4(1+167) = 672 ≠ 668. Off by 4!
    With m=3: k≠0 gives 3*168 = 504 ≠ 668.
    
    So simple combinations of Legendre sequences and all-ones DON'T work.
    We need a more sophisticated construction.
    """
    print("Simple Legendre/all-ones combinations insufficient (DFT analysis).")
    print("Need a different construction method.")
    print()
    
    # The issue is that 4p/(p+1) is not an integer for p=167.
    # We need sequences whose power spectra are NOT simply p+1 or p².
    # This means we need to go beyond simple Legendre-based sequences.
    
    # ALTERNATIVE: Use the Paley Type I construction to get H(168),
    # then use a product construction or other method.
    
    # Actually, let me reconsider. The Kronecker product of Hadamard matrices
    # of orders a and b gives a Hadamard matrix of order ab.
    # 
    # 668 = 4 * 167
    # But 167 is prime and NOT a multiple of 4 (except trivially), 
    # so no Hadamard matrix of order 167 exists by the Hadamard conjecture prerequisites.
    # (The only orders not divisible by 4 that could work are 1 and 2.)
    #
    # 668 = 2 * 334 = 2 * 2 * 167
    # Same problem: 167 is not a valid Hadamard order > 2.
    #
    # So we MUST use a direct construction, not Kronecker.
    #
    # Let me think about what other constructions are available...
    
    # THE REAL SOLUTION: For p ≡ 3 (mod 4) prime, a Hadamard matrix of order 
    # 2(p+1) ALWAYS exists via Paley Type II. That gives order 336 for p=167.
    # 
    # And Paley Type I gives order p+1 = 168.
    #
    # 336 * 2 = 672 (not 668)
    # 168 * 4 = 672 (not 668)
    # 
    # We need EXACTLY 668. Let's see:
    # 668 = 4 * 167
    # 
    # The question is: does a Hadamard matrix of order 668 exist?
    # By the Hadamard conjecture, it should (668 is divisible by 4).
    # 
    # Known constructions that produce H(4p) for p prime, p ≡ 3 mod 4:
    # - The Williamson construction IF Williamson-type matrices of order p exist
    # - The Goethals-Seidel construction IF suitable sequences exist
    # - The Turyn construction
    # - Supplementary difference sets
    #
    # For p = 167, we need to find specific combinatorial objects.
    # This is a HARD computational problem in general.
    
    # Let me try the Turyn/Goethals-Seidel approach with a more careful
    # construction of the four sequences.
    
    return try_turyn_construction(chi, p)


def try_turyn_construction(chi, p):
    """
    Try the Turyn construction for H(4p).
    
    Turyn showed that if T-sequences of lengths (p, p, p, p) exist 
    (or more generally compatible lengths), one can build H(4p).
    
    For p prime, p ≡ 3 (mod 4), we can use the quadratic residue 
    approach combined with "negaperiodic" sequences.
    
    Alternative: Use the result that for EVERY prime p ≡ 3 (mod 4),
    a Hadamard matrix of order 4p exists. This is proven via the
    "Paley-type construction" which is different from Paley I and II.
    
    The proof-construction uses supplementary difference sets
    (SDS) in Z_p with parameters 4-{p; k1, k2, k3, k4; lambda}.
    """
    print("Attempting construction via supplementary difference sets...")
    
    # For p ≡ 3 mod 4, the following 4-{p; (p-1)/2, (p-1)/2, (p-1)/2, (p+1)/2; 2(p-1)}
    # supplementary difference sets are known to exist:
    #
    # D1 = D2 = Q (quadratic residues)
    # D3 = Q  
    # D4 = Q ∪ {0} (quadratic residues plus zero)
    #
    # Verification: for each nonzero d:
    # sum |D_i ∩ (D_i + d)| = lambda = ?
    #
    # For QR set Q: |Q ∩ (Q+d)| depends on the character sum.
    # For d ≠ 0: |Q ∩ (Q+d)| = (p - 4*chi(d) - 3)/4  ... no, let me compute this correctly.
    
    # Actually, for the SDS approach, we need:
    # sum_{i=1}^{4} |D_i ∩ (D_i + d)| = sum |D_i| - p for each nonzero d
    # (This is the condition for the corresponding ±1 matrices to satisfy 
    #  the Goethals-Seidel condition.)
    
    # Let me just compute it numerically for p = 167.
    
    QR = set()
    QNR = set()
    for j in range(1, p):
        if chi[j] == 1:
            QR.add(j)
        else:
            QNR.add(j)
    
    print(f"|QR| = {len(QR)}, |QNR| = {len(QNR)}")
    
    # Test various SDS candidates
    candidates = [
        ("3QR + QR∪{0}", [QR, QR, QR, QR | {0}]),
        ("3QR + Z*", [QR, QR, QR, QR | QNR]),  # Z* = {1,...,p-1}
        ("2QR + QNR + QR∪{0}", [QR, QR, QNR, QR | {0}]),
        ("2QR + QNR + QNR∪{0}", [QR, QR, QNR, QNR | {0}]),
        ("QR + QNR + QR + QNR∪{0}", [QR, QNR, QR, QNR | {0}]),
        ("QR + QNR + QR∪{0} + QNR∪{0}", [QR, QNR, QR | {0}, QNR | {0}]),
        ("2(QR∪{0}) + 2QNR", [QR | {0}, QR | {0}, QNR, QNR]),
        ("2QR + 2(QNR∪{0})", [QR, QR, QNR | {0}, QNR | {0}]),
    ]
    
    for name, sets in candidates:
        if check_sds(sets, p):
            print(f"SDS candidate '{name}' WORKS!")
            # Convert to ±1 sequences
            seqs = []
            for S in sets:
                seq = np.array([-1 if j not in S else 1 for j in range(p)], dtype=np.int8)
                seqs.append(seq)
            return build_goethals_seidel(seqs[0], seqs[1], seqs[2], seqs[3], p)
        else:
            print(f"SDS candidate '{name}' does not work.")
    
    print("\nNone of the simple SDS candidates worked. Trying advanced construction...")
    return try_advanced_construction(chi, p, QR, QNR)


def check_sds(sets, p):
    """
    Check if the given sets form supplementary difference sets in Z_p.
    The condition: for every nonzero d in Z_p,
    sum_{i} |S_i ∩ (S_i + d)| = sum |S_i| - p
    (where S_i + d means {s + d mod p : s in S_i})
    """
    total_size = sum(len(S) for S in sets)
    target = total_size - p
    
    for d in range(1, p):
        count = 0
        for S in sets:
            S_shifted = {(s + d) % p for s in S}
            count += len(S & S_shifted)
        if count != target:
            return False
    return True


def try_advanced_construction(chi_arr, p, QR, QNR):
    """
    Try more advanced constructions for H(4*167).
    
    Use the Szekeres construction which works for all primes p ≡ 3 mod 4.
    
    Szekeres (1969) showed that for p ≡ 3 (mod 4) prime, there exist
    supplementary difference sets that yield H(4p).
    
    The Szekeres construction uses:
    - Write p = 2m + 1 (so m = 83 for p = 167)
    - The two Szekeres difference sets are:
      A = {a ∈ QR : a-1 ∈ QR or a-1=0} ∪ {some adjustment}
      B = similar
    - These satisfy |A| + |B| = p - 1 and specific intersection properties.
    
    Actually, the clean modern formulation:
    For p ≡ 3 mod 4, define (following Whiteman 1971):
    
    The cyclotomic classes C0 = QR, C1 = QNR.
    The "Szekeres difference sets" are:
      S+ = {x ∈ Z_p* : x ∈ C0 and x+1 ∈ C0} ∪ {x ∈ Z_p* : x ∈ C1 and x+1 ∈ C1}
      S- = {x ∈ Z_p* : x ∈ C0 and x+1 ∈ C1} ∪ {x ∈ Z_p* : x ∈ C1 and x+1 ∈ C0}
    
    Hmm, this is getting complicated. Let me just compute things directly.
    """
    
    # Actually, I realize the most straightforward proven method is:
    # 
    # THEOREM (Paley): For q prime power, q ≡ 3 (mod 4), there exists a 
    # Hadamard matrix of order q + 1 (Paley Type I).
    #
    # THEOREM (Paley): For q prime power, q ≡ 1 (mod 4), there exists a
    # Hadamard matrix of order 2(q + 1) (Paley Type II).
    #
    # Now 668 = 4 * 167. Since 167 is prime and ≡ 3 mod 4:
    # - Paley I gives H(168) 
    # - For H(668), we note that 668/168 = 3.976... not integer.
    #
    # But we can use the following:
    # 668 = 4 * 167
    # H(4) exists trivially.
    # If H(167) existed, we'd use Kronecker. But H(167) doesn't exist.
    #
    # KEY REALIZATION: Let me use a COMPLETELY DIFFERENT approach.
    # 
    # 668 = 2 * 334 = 2 * 2 * 167
    # 
    # We can write the construction as follows:
    # - Build a Hadamard matrix of order 2(q+1) where q = 333?
    #   No, q must be a prime power ≡ 1 mod 4. 333 = 3 * 111 = 3 * 3 * 37, 
    #   and 333 ≡ 1 mod 4. But 333 is not a prime power.
    #
    # - 668 = 4 * 167. Let me check if there's a construction that gives
    #   H(4p) directly for prime p.
    #
    # YES! The Williamson method DOES give H(4n) for every n for which 
    # Williamson-type matrices exist. And Williamson matrices of order p 
    # are known to exist for many primes, but NOT all. For p = 167, 
    # it's not guaranteed a priori.
    #
    # However, the Goethals-Seidel construction is more flexible:
    # it uses four circulant matrices but they don't need to be symmetric.
    #
    # For p prime, p ≡ 3 mod 4, we can ALWAYS construct four suitable
    # circulant matrices using the following result:
    #
    # THEOREM (Wallis, 1971): For every prime p ≡ 3 (mod 4), there exists
    # a Hadamard matrix of order 4p.
    #
    # The construction uses the concept of "supplementary difference sets"
    # or equivalently "T-matrices".
    
    # Let me implement the Wallis construction directly.
    return wallis_construction(chi_arr, p, QR, QNR)


def wallis_construction(chi_arr, p, QR, QNR):
    """
    Wallis construction for H(4p), p prime, p ≡ 3 (mod 4).
    
    Based on: Jennifer Seberry Wallis, "Hadamard matrices of order 28m, 36m, 44m" (1972)
    and related papers.
    
    The construction uses T-matrices: four {0, ±1} matrices T1, T2, T3, T4
    of order p such that:
    - T_i * T_i^T is a linear combination of I and J
    - sum T_i * T_i^T = 4p * I - J ... (approximately)
    
    Actually, for the cleanest approach, let me use:
    
    FACT: For p ≡ 3 mod 4 prime, the CONFERENCE MATRIX approach gives us everything.
    
    Step 1: Build the (p+1) × (p+1) Paley conference matrix C.
            C = [[0, j^T], [-j, Q]] where Q is the Jacobsthal matrix.
            C is skew-symmetric: C^T = -C.
            C * C^T = p * I_{p+1}.
    
    Step 2: Form the Paley Type I Hadamard matrix: H_{p+1} = C + I_{p+1}.
    
    Step 3: Now we need to go from order 168 to order 668.
            668/168 is not an integer, so direct Kronecker won't work.
    
    Alternative: Use the "doubling construction" differently.
    
    H(2n) from H(n): [[H, H], [H, -H]] gives order 2n from order n.
    H(168) → H(336) → H(672). But 672 ≠ 668.
    
    NONE of these standard approaches give exactly 668.
    
    ===== BREAKTHROUGH INSIGHT =====
    
    The existence of H(4p) for p ≡ 3 mod 4 (prime) follows from:
    
    1. p ≡ 3 mod 4, so there exists a skew-type Hadamard matrix of order p+1.
       Specifically, H = I + C where C is a skew conference matrix of order p+1.
       This means C + C^T = -2I + H + H^T = ... Actually:
       H = I + C, H^T = I + C^T = I - C (since C is skew).
       H * H^T = (I+C)(I-C) = I - C^2 = I + p*I - ... 
       
       Let me recalculate: C*C^T = pI (for a conference matrix).
       Since C is skew, C^T = -C, so C*C^T = -C^2 = pI, i.e., C^2 = -pI.
       H*H^T = (I+C)(I-C) = I - C^2 = I + pI = (p+1)I. ✓
       
    2. Since H(168) is of skew type (H = I + S where S is skew, S^T = -S),
       and 668 = 4 × 167 = 4 × (168 - 1):
       
       We can't directly relate this. Let me think again...
    
    ===== THE ACTUAL CONSTRUCTION =====
    
    I'll use a construction that is guaranteed to work:
    The DOUBLING of the SKEW-TYPE Hadamard matrix.
    
    For a skew-Hadamard matrix H of order n (meaning H + H^T = 2I):
    The Goethals-Seidel doubling gives H(2(n-1)) ... no, that's also not right.
    
    Let me try yet another approach. Let me look at this from the perspective
    of what's computationally feasible.
    """
    print("Attempting Wallis/SDS construction...")
    
    # COMPUTATIONAL APPROACH: 
    # Build four circulant ±1 matrices of order p=167 satisfying the PSD condition.
    # Use the DFT domain to construct sequences with the right power spectrum.
    
    # We need: |â(k)|² + |b̂(k)|² + |ĉ(k)|² + |d̂(k)|² = 4p = 668 for all k.
    
    # Strategy: Use TWO distinct sequence types.
    # Type X: Legendre-based with x̂(0) = s, |x̂(k)|² = 1+p = 168 for k≠0.
    # Type Y: All-ones with ŷ(0) = p, ŷ(k) = 0 for k≠0.
    # Type Z: Other constructions.
    
    # From our analysis: 
    # For k≠0: we need the sum to be 668.
    # With Legendre type: each contributes 168 to k≠0.
    # 668/168 = 3.976..., so we need approximately 4 Legendre types.
    # With exactly 4 Legendre types: k≠0 sum = 4*168 = 672. Off by +4.
    # With 3 Legendre + 1 all-ones: k≠0 sum = 3*168 + 0 = 504. Off by -164.
    
    # We need a sequence type with |ẑ(k)|² = 668 - 3*168 = 164 for k≠0,
    # or sequences where the power spectrum is not constant at 168.
    
    # IDEA: Use Legendre-like sequences but with SEVERAL adjusted positions.
    # If we flip some positions in the Legendre sequence, the DFT changes.
    
    # Actually, there's a much simpler approach I've been overcomplicating:
    # USE THE KNOWN RESULT THAT FOR p ≡ 3 (mod 4) PRIME,
    # SUPPLEMENTARY DIFFERENCE SETS 4-{p; k,k,k,k; λ} EXIST.
    #
    # Specifically, for p ≡ 3 (mod 4):
    # D1 = D2 = C0 ∪ {0} (QR ∪ {0}), |Di| = (p+1)/2 = 84
    # D3 = D4 = C1 (QNR), |Di| = (p-1)/2 = 83
    #
    # Check: For nonzero d, we need:
    # sum |Di ∩ (Di+d)| = (sum |Di|) - p = (84+84+83+83) - 167 = 334 - 167 = 167
    
    # Let's verify this
    D1 = QR | {0}  # QR ∪ {0}, size (p+1)/2
    D2 = QR | {0}  # same
    D3 = QNR.copy()  # QNR, size (p-1)/2
    D4 = QNR.copy()  # same
    
    sets = [D1, D2, D3, D4]
    total = sum(len(S) for S in sets)
    target = total - p
    print(f"Testing SDS: sizes = {[len(S) for S in sets]}, total = {total}, target per d = {target}")
    
    if check_sds(sets, p):
        print("SDS with 2×(QR∪{0}) + 2×QNR WORKS!")
        seqs = []
        for S in sets:
            seq = np.array([1 if j in S else -1 for j in range(p)], dtype=np.int8)
            seqs.append(seq)
        return build_goethals_seidel(seqs[0], seqs[1], seqs[2], seqs[3], p)
    
    # Try more candidates
    more_candidates = [
        ("QR∪{0}, QR∪{0}, QR, QNR∪{0}", [QR | {0}, QR | {0}, QR, QNR | {0}]),
        ("QR∪{0}, QNR∪{0}, QR∪{0}, QNR∪{0}", [QR | {0}, QNR | {0}, QR | {0}, QNR | {0}]),
        ("QR∪{0}, QR∪{0}, QNR∪{0}, QNR∪{0}", [QR | {0}, QR | {0}, QNR | {0}, QNR | {0}]),
    ]
    
    for name, sets in more_candidates:
        if check_sds(sets, p):
            print(f"SDS '{name}' WORKS!")
            seqs = []
            for S in sets:
                seq = np.array([1 if j in S else -1 for j in range(p)], dtype=np.int8)
                seqs.append(seq)
            return build_goethals_seidel(seqs[0], seqs[1], seqs[2], seqs[3], p)
        else:
            print(f"SDS '{name}' failed.")
    
    print("\nAll SDS attempts failed. Trying direct block construction from conference matrix...")
    return build_from_conference_matrix(chi_arr, p, QR, QNR)


def build_from_conference_matrix(chi_arr, p, QR, QNR):
    """
    Build H(4p) from the conference matrix of order p+1.
    
    There is a classical result (Paley, enhanced by others) that shows:
    If C is a skew-symmetric conference matrix of order n = p+1,
    then one can build a Hadamard matrix of order 2n = 2(p+1).
    
    But we need order 4p, not 2(p+1).
    
    KEY INSIGHT: There is a construction that uses the Jacobsthal matrix Q
    of order p (not the conference matrix of order p+1) to directly build
    a Hadamard matrix of order 4p.
    
    This is the "quadratic double" or "Paley graph construction" for order 4p.
    
    THE CONSTRUCTION (explicit):
    
    Let Q be the p×p Jacobsthal matrix (Q[i,j] = chi(j-i), Q[0,j] = chi(j)).
    Since p ≡ 3 mod 4: Q is skew (Q^T = -Q), and Q^2 = J - pI.
    
    Let I be the p×p identity, J = all-ones matrix, e = all-ones vector.
    
    Define the 4p × 4p matrix H using 4×4 blocks of p×p matrices:
    
    Let's use the notation: ⊗ for Kronecker product, ⊕ for direct sum.
    
    H_4 = [[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]  (Hadamard of order 4)
    
    NOT a simple Kronecker product with Q.
    
    Instead, the construction from Miyamoto (2001) / Seberry:
    
    The following ALWAYS works for p ≡ 3 mod 4:
    Build the (p+1)×(p+1) skew-type Hadamard matrix H_{p+1} = I + C where
    C = [[0, -e^T], [e, Q]] (conference matrix, adjusted signs for skew type).
    
    Then H_{p+1} is "skew-type": H + H^T = 2I.
    
    Now use the Seberry-Whiteman result: if a skew-Hadamard matrix of order m exists,
    then a Hadamard matrix of order m(m-1) exists via a specific construction.
    For m = p+1 = 168: m(m-1) = 168*167 = 28056. Way too big.
    
    That's not what we want. Let me try a completely different approach.
    """
    
    print("Using direct algebraic construction...")
    
    # FINAL CORRECT APPROACH: 
    # Use the Kronecker product of known Hadamard matrices.
    # 
    # Factor 668:
    # 668 = 4 * 167
    # 668 = 2 * 2 * 167
    # 
    # Since 167 is prime and odd, the only factorizations into Hadamard orders are:
    # 668 = 1 * 668 (need H(668) directly)
    # 668 = 2 * 334 (need H(2) and H(334); H(334) exists iff H(334) can be constructed)
    # 668 = 4 * 167 (need H(167), doesn't exist since 167 mod 4 = 3 ≠ 0)
    # 
    # For H(334): 334 = 2 * 167. Again need H(167).
    # 
    # So Kronecker product is NOT viable for 668.
    #
    # WE MUST USE A DIRECT CONSTRUCTION.
    #
    # The existence of H(4p) for all p ≡ 3 mod 4 is actually a THEOREM,
    # proven constructively. Let me implement the actual proof construction.
    
    # FROM SEBERRY-YAMADA (Hadamard Matrices, Sequences, and Block Designs, 1992):
    # Theorem: For q prime, q ≡ 3 (mod 4), there exists a Hadamard matrix of order 2(q+1).
    # This is Paley Type II, giving order 2*168 = 336 for q=167.
    
    # FROM CRAIGEN (1996) and earlier TURYN:
    # Theorem: Hadamard matrix of order 4p exists for p prime via the following:
    # Use the "direct sum" approach with four supplementary difference sets.
    
    # I think the issue is that the SDS construction requires more careful 
    # selection. Let me try to computationally search for valid quadruples.
    
    # Actually, before going further into increasingly complex approaches,
    # let me verify: for the two SDS candidates that use QR/QNR sets,
    # what is the actual discrepancy? This will guide us.
    
    D_qr = QR
    D_qnr = QNR
    
    # Check the difference function for QR
    delta_qr = np.zeros(p, dtype=int)
    for d in range(1, p):
        D_shifted = {(s + d) % p for s in D_qr}
        delta_qr[d] = len(D_qr & D_shifted)
    
    # For QR set with p ≡ 3 mod 4:
    # |QR ∩ (QR+d)| = (p-3)/4 if d ∈ QR, (p+1)/4 if d ∈ QNR
    # For p = 167: (167-3)/4 = 41, (167+1)/4 = 42
    print(f"QR intersection counts:")
    qr_counts = set()
    qnr_counts = set()
    for d in range(1, p):
        D_shifted = {(s + d) % p for s in D_qr}
        val = len(D_qr & D_shifted)
        if d in QR:
            qr_counts.add(val)
        else:
            qnr_counts.add(val)
    print(f"  d ∈ QR: counts = {qr_counts}")
    print(f"  d ∈ QNR: counts = {qnr_counts}")
    
    # So for QR: intersection is 41 when d ∈ QR, 42 when d ∈ QNR.
    # For QNR: intersection is 42 when d ∈ QR, 41 when d ∈ QNR.
    # (By symmetry of the cyclotomic scheme.)
    
    # Now for 4 copies of QR:
    # Sum for d ∈ QR: 4*41 = 164
    # Sum for d ∈ QNR: 4*42 = 168
    # Target: 4*83 - 167 = 332 - 167 = 165
    # So the counts are 164 and 168, but we need a CONSTANT 165.
    
    # For 2×QR + 2×QNR:
    # d ∈ QR: 2*41 + 2*42 = 82 + 84 = 166
    # d ∈ QNR: 2*42 + 2*41 = 84 + 82 = 166
    # Target: 2*83 + 2*83 - 167 = 332 - 167 = 165
    # Count = 166 ≠ 165. Off by 1.
    
    # For 2×(QR∪{0}) + 2×QNR: sizes are 84+84+83+83 = 334, target = 334-167 = 167
    # d ∈ QR: 2*(41 + ?) + 2*42
    # Need to compute |{QR∪{0}} ∩ {QR∪{0}+d}| for d ∈ QR.
    # QR∪{0} + d = {(s+d) mod p : s ∈ QR∪{0}} = {(s+d) mod p : s ∈ QR} ∪ {d}
    # |(QR∪{0}) ∩ ({shifted QR} ∪ {d})| = |QR ∩ shiftedQR| + |{0} ∩ shiftedQR| + |QR ∩ {d}| + |{0} ∩ {d}|
    # Wait, we need |(QR∪{0}) ∩ ((QR∪{0})+d)|
    # = |(QR∪{0}) ∩ (QR+d ∪ {d})|
    # = |QR ∩ (QR+d)| + |{0} ∩ (QR+d)| + |QR ∩ {d}| + |{0} ∩ {d}|
    # - |{0} ∩ (QR+d) ∩ QR ∩ {d}|  (inclusion-exclusion, but these are disjoint cases)
    # Actually, simpler: |(A∪B) ∩ (C∪D)| = |A∩C| + |A∩D| + |B∩C| + |B∩D| - overlaps
    # Since 0 ∉ QR and d ≠ 0:
    # |QR ∩ (QR+d)| + |QR ∩ {d}| + |{0} ∩ (QR+d)| + |{0} ∩ {d}|
    # = |QR ∩ (QR+d)| + [1 if d ∈ QR else 0] + [1 if -d ∈ QR, i.e., p-d ∈ QR else 0] + 0
    # (0 ∈ QR+d iff -d mod p = p-d ∈ QR)
    
    # For d ∈ QR and p ≡ 3 mod 4: chi(-1) = -1, so chi(-d) = -chi(d) = -1, meaning -d ∈ QNR.
    # So |{0} ∩ (QR+d)| = 0 for d ∈ QR (since -d ∈ QNR, meaning 0 ∉ QR+d).
    
    # For d ∈ QR: |(QR∪{0}) ∩ ((QR∪{0})+d)| = 41 + 1 + 0 + 0 = 42
    # For d ∈ QNR: chi(-d) = -chi(d) = 1, so -d ∈ QR, meaning 0 ∈ QR+d.
    # |(QR∪{0}) ∩ ((QR∪{0})+d)| = 42 + 0 + 1 + 0 = 43
    
    # Similarly for QNR:
    # |QNR ∩ (QNR+d)|: for d ∈ QR: 42, for d ∈ QNR: 41
    # (By symmetry with QR, using chi(-1) = -1)
    
    # Now test 2×(QR∪{0}) + 2×QNR:
    # d ∈ QR: 2*42 + 2*42 = 168. Target = 167. Off by +1.
    # d ∈ QNR: 2*43 + 2*41 = 168. Target = 167. Off by +1.
    
    # CLOSE! Off by exactly 1 everywhere. This means we need to adjust
    # the sizes slightly.
    
    # What if we use 2×(QR∪{0}) + QNR + (QNR∪{0})?
    # sizes: 84 + 84 + 83 + 84 = 335, target = 335 - 167 = 168
    # d ∈ QR: 2*42 + 42 + ? ... need |(QNR∪{0}) ∩ ((QNR∪{0})+d)| for d ∈ QR
    # |(QNR∪{0}) ∩ ((QNR∪{0})+d)| = |QNR∩(QNR+d)| + |QNR∩{d}| + |{0}∩(QNR+d)| + |{0}∩{d}|
    # For d ∈ QR: |QNR∩(QNR+d)| = 42, |QNR∩{d}| = 0 (d ∈ QR), 
    #   |{0}∩(QNR+d)| = 1 if -d ∈ QNR, i.e., chi(-d) = -chi(d) = -1, so yes if d ∈ QR.
    #   So = 42 + 0 + 1 + 0 = 43.
    # d ∈ QR: 2*42 + 42 + 43 = 169. Target = 168. Off by +1.
    # 
    # Hmm, still off.
    
    # Let me try a fundamentally different approach.
    print("\nSwitching to a completely different construction method.")
    print("Using the 'two-circulant core' Hadamard construction.\n")
    
    return None  # Signal to try a different method


def build_goethals_seidel(a, b, c, d, n):
    """
    Build a Hadamard matrix of order 4n using the Goethals-Seidel array:
    
    H = [[ A,  BR,  CR,  DR],
         [-BR,  A,  D^TR, -C^TR],
         [-CR, -D^TR, A,  B^TR],
         [-DR,  C^TR, -B^TR, A]]
    
    where A, B, C, D are circulant matrices with first rows a, b, c, d,
    and R is the back-circulant (reversal) permutation matrix.
    """
    A = circulant_from_first_row(a)
    B = circulant_from_first_row(b)
    C = circulant_from_first_row(c)
    D = circulant_from_first_row(d)
    R = back_circulant_matrix(n)
    
    # For circulant matrices: X*R = R*X^T (since R reverses and circulant 
    # transposition corresponds to reversal of the first row).
    # So XR is symmetric: (XR)^T = R^T X^T = R X^T = X R ... 
    # Actually R^T = R (R is symmetric), so (XR)^T = R^T X^T = R X^T.
    # And XR = R X^T only if X commutes with R, which circulant matrices do
    # since RX = X^T R for circulants. So (XR)^T = R X^T and XR = ... 
    # Let's not worry about this and just build the block matrix.
    
    BR = B @ R
    CR = C @ R
    DR = D @ R
    
    H = np.block([
        [A,    BR,    CR,    DR   ],
        [-BR,  A,     DR.T, -CR.T ],
        [-CR, -DR.T,  A,     BR.T ],
        [-DR,  CR.T, -BR.T,  A    ]
    ])
    
    return H.astype(np.int8)


if __name__ == "__main__":
    t0 = time.time()
    H = construct_hadamard_668()
    elapsed = time.time() - t0
    
    if H is not None:
        print(f"\nConstruction completed in {elapsed:.2f}s")
        print(f"Matrix shape: {H.shape}")
        
        # Verify
        n = H.shape[0]
        assert H.shape == (n, n), f"Not square: {H.shape}"
        assert set(np.unique(H)).issubset({-1, 1}), f"Not ±1: {np.unique(H)}"
        
        HHt = H.astype(np.int64) @ H.T.astype(np.int64)
        expected = n * np.eye(n, dtype=np.int64)
        if np.array_equal(HHt, expected):
            print("VERIFIED: H * H^T = 668 * I")
            np.savetxt("results/hadamard_668.csv", H, delimiter=",", fmt="%d")
            print("Saved to results/hadamard_668.csv")
        else:
            error = np.max(np.abs(HHt - expected))
            print(f"FAILED: max error in H*H^T = {error}")
    else:
        print(f"\nConstruction FAILED after {elapsed:.2f}s")
        print("Need to try a different approach.")
