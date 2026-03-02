#!/usr/bin/env python3
"""
Computational search for Goethals-Seidel difference families in Z_167
to construct a Hadamard matrix of order 668 = 4 * 167.

A GS-difference family consists of four subsets X0, X1, X2, X3 of Z_167
such that for every nonzero d in Z_167:
    sum_{i=0}^{3} |Xi ∩ (Xi + d)| = sum |Xi| - 167

Equivalently, define ±1 sequences a_i of length 167 from Xi
(a_i[j] = -1 if j in Xi, +1 otherwise), build circulant matrices,
and check the power spectral density condition:
    sum |â_i(k)|^2 = 668 for all k = 0, ..., 166

Strategy: Use multiplier-based search as in Djoković-Kotsireas (2018).
A multiplier μ is an element of Z*_167 such that μ*Xi is a permutation 
of the Xi's. This drastically reduces the search space.

For Z*_167 of order 166 = 2 × 83:
- Subgroups of order 1, 2, 83, 166
- No elements of order 3 (spin structure impossible)
- Generator g such that g^166 ≡ 1 (mod 167)

We'll search for GS-families with various structural constraints.
"""

import numpy as np
from itertools import combinations
import time
import sys
import json

p = 167

def legendre(a, p):
    if a % p == 0:
        return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

def find_generator(p):
    """Find a primitive root mod p."""
    for g in range(2, p):
        seen = set()
        val = 1
        for _ in range(p-1):
            val = (val * g) % p
            seen.add(val)
        if len(seen) == p - 1:
            return g
    return None

def check_gs_family_fft(seqs):
    """Check if four ±1 sequences satisfy the GS power spectral condition."""
    target = 4 * p
    spectra = [np.fft.fft(s.astype(np.complex128)) for s in seqs]
    power_sum = sum(np.abs(sp)**2 for sp in spectra)
    error = np.max(np.abs(power_sum - target))
    return error < 0.5, error

def check_gs_family_direct(sets):
    """Check the SDS condition directly."""
    total = sum(len(S) for S in sets)
    target = total - p
    for d in range(1, p):
        count = 0
        for S in sets:
            S_shifted = frozenset((s + d) % p for s in S)
            count += len(S & S_shifted)
        if count != target:
            return False, d
    return True, -1

def sets_to_seqs(sets):
    """Convert subsets of Z_p to ±1 sequences."""
    seqs = []
    for S in sets:
        seq = np.array([1 if j not in S else -1 for j in range(p)], dtype=np.int8)
        seqs.append(seq)
    return seqs

def build_gs_hadamard(seqs):
    """Build 4p × 4p Hadamard matrix from four ±1 sequences using Goethals-Seidel array."""
    n = len(seqs[0])
    
    # Build circulant matrices
    def circulant(seq):
        n = len(seq)
        C = np.zeros((n, n), dtype=np.int8)
        for i in range(n):
            for j in range(n):
                C[i, j] = seq[(j - i) % n]
        return C
    
    # Back-circulant matrix R
    R = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        R[i, (n - i) % n] = 1
    
    A = circulant(seqs[0])
    B = circulant(seqs[1])
    C = circulant(seqs[2])
    D = circulant(seqs[3])
    
    BR = B @ R
    CR = C @ R
    DR = D @ R
    
    H = np.block([
        [ A,    BR,    CR,    DR   ],
        [-BR,   A,     DR.T, -CR.T ],
        [-CR,  -DR.T,  A,     BR.T ],
        [-DR,   CR.T, -BR.T,  A    ]
    ])
    
    return H.astype(np.int8)

def verify_hadamard(H):
    """Verify H is a Hadamard matrix."""
    n = H.shape[0]
    if H.shape != (n, n):
        return False, "Not square"
    if not set(np.unique(H)).issubset({-1, 1}):
        return False, f"Not ±1 entries: {np.unique(H)}"
    
    HHt = H.astype(np.int64) @ H.T.astype(np.int64)
    expected = n * np.eye(n, dtype=np.int64)
    if np.array_equal(HHt, expected):
        return True, "Valid Hadamard matrix"
    else:
        max_err = np.max(np.abs(HHt - expected))
        diag_ok = np.all(np.diag(HHt) == n)
        return False, f"H*H^T ≠ nI, max_error={max_err}, diag_ok={diag_ok}"


# ============================================================
# APPROACH 1: Multiplier-based search with cyclic structure
# ============================================================

def approach_multiplier_search():
    """
    Search for GS-families using multipliers from Z*_167.
    
    The group Z*_167 has order 166 = 2 × 83.
    A primitive root g generates the entire group.
    
    Subgroups:
    - H_83 = <g^2> of order 83 (index 2) — the quadratic residues
    - H_2 = <g^83> = {1, g^83} of order 2
    - {1} trivial
    
    For a multiplier μ of order m in Z*_167:
    μ acts on subsets of Z_167 by multiplication.
    If μ*Xi = X_{σ(i)} for some permutation σ of {0,1,2,3},
    then the family has a μ-multiplier.
    
    For m = 2 (μ = g^83 = p-1 = 166 ≡ -1):
    The multiplier -1 acts by negation: -Xi = {p - x : x in Xi}.
    A set is "symmetric" if -Xi = Xi, and "skew" if Xi ∩ (-Xi) = ∅.
    
    For m = 83 (μ = g^2, a QR):
    The multiplier squares all elements. A set is closed under 
    QR-multiplication if μ*Xi = Xi.
    """
    g = find_generator(p)
    print(f"Primitive root mod {p}: {g}")
    
    # The element of order 2 is g^83 = -1 mod p
    neg1 = pow(g, 83, p)
    print(f"Element of order 2: g^83 = {neg1} (should be {p-1})")
    assert neg1 == p - 1
    
    # Elements of order 83: g^2 (generates H_83 = QR set)
    mu83 = pow(g, 2, p)
    print(f"Element of order 83 (QR generator): g^2 = {mu83}")
    
    # QR and QNR sets
    QR = set()
    QNR = set()
    for j in range(1, p):
        if legendre(j, p) == 1:
            QR.add(j)
        else:
            QNR.add(j)
    
    print(f"|QR| = {len(QR)}, |QNR| = {len(QNR)}")
    
    # The orbits of <g^2> on Z*_167 are exactly {QR, QNR} (2 orbits of size 83).
    # Adding 0: the orbits on Z_167 are {0}, QR, QNR (3 orbits).
    
    # For a GS-family closed under the multiplier μ = g^2 of order 83:
    # Each Xi must be a union of orbits of <μ>.
    # The orbits are: {0}, QR, QNR.
    # So each Xi is one of: ∅, {0}, QR, QNR, QR∪{0}, QNR∪{0}, QR∪QNR, QR∪QNR∪{0}, Z_p.
    # That's only 8 possibilities per Xi, giving 8^4 = 4096 combinations.
    
    orbit_subsets = [
        frozenset(),           # ∅
        frozenset([0]),        # {0}
        frozenset(QR),         # QR
        frozenset(QNR),        # QNR
        frozenset(QR | {0}),   # QR ∪ {0}
        frozenset(QNR | {0}),  # QNR ∪ {0}
        frozenset(QR | QNR),   # Z*_p
        frozenset(QR | QNR | {0}),  # Z_p
    ]
    
    print(f"\nSearching {len(orbit_subsets)}^4 = {len(orbit_subsets)**4} orbit-based families...")
    
    best_error = float('inf')
    best_family = None
    
    count = 0
    for i0 in range(len(orbit_subsets)):
        for i1 in range(len(orbit_subsets)):
            for i2 in range(len(orbit_subsets)):
                for i3 in range(len(orbit_subsets)):
                    sets = [orbit_subsets[i0], orbit_subsets[i1], 
                           orbit_subsets[i2], orbit_subsets[i3]]
                    
                    # Quick size check: total size should make sense
                    total = sum(len(S) for S in sets)
                    if total < p or total > 4*p:
                        continue
                    
                    # Check using FFT
                    seqs = sets_to_seqs(sets)
                    ok, err = check_gs_family_fft(seqs)
                    
                    if ok:
                        print(f"\n*** FOUND VALID GS-FAMILY! ***")
                        print(f"  Sizes: {[len(S) for S in sets]}")
                        return seqs
                    
                    if err < best_error:
                        best_error = err
                        best_family = [len(S) for S in sets]
                    
                    count += 1
    
    print(f"Searched {count} orbit-based families. Best error: {best_error:.2f}")
    print(f"Best family sizes: {best_family}")
    return None


# ============================================================
# APPROACH 2: Finer orbit decomposition using negation multiplier
# ============================================================

def approach_negation_orbits():
    """
    Use the multiplier μ = -1 (of order 2) to decompose Z_167.
    
    The orbits of {1, -1} on Z*_167 are pairs {j, p-j} for j = 1, ..., 83.
    Plus the singleton {0}.
    So we have 84 orbits: {0}, {1,166}, {2,165}, ..., {83,84}.
    
    Each Xi is a union of these orbits. 
    A set is "symmetric" if it's a union of these orbits.
    A set is "skew" if for each orbit, exactly one element is chosen.
    
    With 84 orbits, each Xi can be specified by a 84-bit vector.
    2^84 is too large for brute force, but we can use:
    1. DFT analysis to constrain choices
    2. Random/heuristic search
    3. SAT/constraint solving
    """
    print("Approach 2: Negation-orbit decomposition with heuristic search")
    
    # Build negation orbits
    orbits = [{0}]  # orbit of 0
    for j in range(1, (p+1)//2):
        orbits.append(frozenset({j, p - j}))
    
    print(f"Number of negation orbits: {len(orbits)} (1 singleton + {len(orbits)-1} pairs)")
    
    # For a GS-family with all symmetric blocks:
    # Each Xi is a union of negation orbits.
    # The circulant matrix from a symmetric sequence is a symmetric circulant.
    # Williamson's theorem applies: A^2 + B^2 + C^2 + D^2 = 4pI
    # (since symmetric circulants commute and CC^T = C^2 for symmetric C).
    
    # In the DFT domain, for a real symmetric sequence x (x_j = x_{p-j}):
    # x̂(k) is real for all k.
    # We need: â(k)^2 + b̂(k)^2 + ĉ(k)^2 + d̂(k)^2 = 4p for all k.
    
    # This is the Williamson condition.
    # The DFT values of symmetric ±1 sequences are real.
    # For each k, we need four real numbers summing to 668.
    
    # For p = 167, the DFT indices k and p-k give conjugate values.
    # Since the sequences are real and symmetric, x̂(k) = x̂(p-k) is real.
    # So we have (p+1)/2 = 84 independent DFT values: k = 0, 1, ..., 83.
    
    # Let's try a random/stochastic search.
    return stochastic_williamson_search(orbits)


def stochastic_williamson_search(orbits, max_iter=100000, seed=42):
    """
    Stochastic local search for Williamson-type matrices of order 167.
    
    Strategy: Start with random symmetric ±1 sequences and use 
    simulated annealing to minimize the spectral deviation.
    """
    np.random.seed(seed)
    
    # Initialize four random symmetric ±1 sequences
    def random_symmetric_seq():
        seq = np.ones(p, dtype=np.int8)
        # Set value for each orbit
        for orb in orbits:
            val = np.random.choice([-1, 1])
            for j in orb:
                seq[j] = val
        return seq
    
    def spectral_cost(seqs):
        """Cost = sum of squared deviations from 4p in power spectrum."""
        target = 4 * p
        power = np.zeros(p, dtype=np.float64)
        for s in seqs:
            fft_s = np.fft.fft(s.astype(np.float64))
            power += np.abs(fft_s)**2
        return np.sum((power - target)**2)
    
    def flip_orbit(seq, orbit):
        """Flip all entries in an orbit."""
        new_seq = seq.copy()
        for j in orbit:
            new_seq[j] = -new_seq[j]
        return new_seq
    
    best_cost = float('inf')
    best_seqs = None
    
    print(f"Stochastic search with {max_iter} iterations...")
    
    # Multiple restarts
    n_restarts = 10
    iters_per_restart = max_iter // n_restarts
    
    for restart in range(n_restarts):
        seqs = [random_symmetric_seq() for _ in range(4)]
        cost = spectral_cost(seqs)
        
        temperature = 100.0
        cooling = 0.9999
        
        local_best = cost
        
        for it in range(iters_per_restart):
            # Pick a random sequence and orbit to flip
            seq_idx = np.random.randint(4)
            orb_idx = np.random.randint(len(orbits))
            
            new_seq = flip_orbit(seqs[seq_idx], orbits[orb_idx])
            new_seqs = seqs.copy()
            new_seqs[seq_idx] = new_seq
            new_cost = spectral_cost(new_seqs)
            
            delta = new_cost - cost
            if delta < 0 or np.random.random() < np.exp(-delta / max(temperature, 1e-10)):
                seqs = new_seqs
                cost = new_cost
            
            temperature *= cooling
            
            if cost < local_best:
                local_best = cost
            
            if cost < best_cost:
                best_cost = cost
                best_seqs = [s.copy() for s in seqs]
            
            if cost < 0.5:
                print(f"  SOLUTION FOUND at restart {restart}, iteration {it}!")
                return best_seqs
        
        print(f"  Restart {restart}: best cost = {local_best:.1f}")
    
    print(f"\nBest cost found: {best_cost:.1f}")
    if best_seqs is not None:
        # Analyze the best solution
        target = 4 * p
        power = np.zeros(p, dtype=np.float64)
        for s in best_seqs:
            fft_s = np.fft.fft(s.astype(np.float64))
            power += np.abs(fft_s)**2
        print(f"  Power spectrum range: [{power.min():.1f}, {power.max():.1f}] (target: {target})")
    
    return None


# ============================================================
# APPROACH 3: Non-symmetric (skew) base blocks
# ============================================================

def approach_skew_blocks():
    """
    Search with skew (anti-symmetric) base blocks.
    
    A sequence is "skew" if x_0 = 1 and x_{p-j} = -x_j for j = 1, ..., (p-1)/2.
    This is the most common type for Goethals-Seidel constructions.
    
    The first row is determined by (p-1)/2 = 83 free ±1 choices.
    Total search space per block: 2^83, way too large.
    
    But with multiplier structure, we can reduce dramatically.
    """
    print("Approach 3: Mixed symmetric/skew blocks with stochastic search")
    
    # For a skew sequence: x_0 = 1, x_j = -x_{p-j}
    # In the DFT domain: x̂(k) is purely imaginary for k ≠ 0, and x̂(0) = 1 + sum x_j.
    # Since sum x_j = x_0 + sum_{j=1}^{(p-1)/2} (x_j + x_{p-j}) = 1 + 0 = 1.
    # So x̂(0) = 1 for a skew sequence.
    
    # For a symmetric sequence: x̂(k) is real.
    # For a skew sequence: x̂(k) is purely imaginary for k ≠ 0.
    
    # Power spectrum for symmetric: |x̂(k)|^2 = x̂(k)^2 (real^2)
    # Power spectrum for skew: |x̂(k)|^2 = -x̂(k)^2 (imaginary^2, so positive)
    
    # Let's try various combinations of symmetric and skew blocks.
    
    np.random.seed(42)
    
    def random_skew_seq():
        """Generate a random skew ±1 sequence of length p."""
        seq = np.ones(p, dtype=np.int8)
        half = (p - 1) // 2  # = 83
        for j in range(1, half + 1):
            val = np.random.choice([-1, 1])
            seq[j] = val
            seq[p - j] = -val
        return seq
    
    def random_symmetric_seq():
        """Generate a random symmetric ±1 sequence of length p."""
        seq = np.ones(p, dtype=np.int8)
        seq[0] = np.random.choice([-1, 1])
        half = (p - 1) // 2
        for j in range(1, half + 1):
            val = np.random.choice([-1, 1])
            seq[j] = val
            seq[p - j] = val
        return seq
    
    def spectral_cost(seqs):
        target = 4 * p
        power = np.zeros(p, dtype=np.float64)
        for s in seqs:
            fft_s = np.fft.fft(s.astype(np.float64))
            power += np.abs(fft_s)**2
        return np.sum((power - target)**2)
    
    # Try combinations: (n_symmetric, n_skew)
    configs = [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]
    
    for n_sym, n_skew in configs:
        print(f"\n  Config: {n_sym} symmetric + {n_skew} skew blocks")
        
        best_cost = float('inf')
        for trial in range(2000):
            seqs = []
            for _ in range(n_sym):
                seqs.append(random_symmetric_seq())
            for _ in range(n_skew):
                seqs.append(random_skew_seq())
            
            cost = spectral_cost(seqs)
            if cost < best_cost:
                best_cost = cost
        
        print(f"    Best random cost: {best_cost:.1f} (target: 0)")
    
    return None


# ============================================================
# APPROACH 4: Large-scale SA with mixed orbit structure
# ============================================================

def approach_large_sa(max_iter=500000, seed=42):
    """
    Large-scale simulated annealing search for GS-families.
    Uses general (not necessarily symmetric) ±1 sequences.
    """
    print("Approach 4: Large-scale simulated annealing (general sequences)")
    np.random.seed(seed)
    
    def spectral_cost(seqs):
        target = 4 * p
        power = np.zeros(p, dtype=np.float64)
        for s in seqs:
            fft_s = np.fft.fft(s.astype(np.float64))
            power += np.abs(fft_s)**2
        return np.sum((power - target)**2)
    
    # Start with Legendre-based sequences (good starting point)
    chi = np.array([legendre(j, p) for j in range(p)], dtype=np.int8)
    chi[0] = 1
    
    seqs = [chi.copy(), chi.copy(), chi.copy(), np.ones(p, dtype=np.int8)]
    
    cost = spectral_cost(seqs)
    best_cost = cost
    best_seqs = [s.copy() for s in seqs]
    
    temperature = 500.0
    cooling = 1 - 5.0/max_iter
    
    for it in range(max_iter):
        # Flip a random entry in a random sequence
        seq_idx = np.random.randint(4)
        pos = np.random.randint(p)
        
        old_val = seqs[seq_idx][pos]
        seqs[seq_idx][pos] = -old_val
        
        new_cost = spectral_cost(seqs)
        delta = new_cost - cost
        
        if delta < 0 or np.random.random() < np.exp(-delta / max(temperature, 1e-10)):
            cost = new_cost
        else:
            seqs[seq_idx][pos] = old_val
        
        temperature *= cooling
        
        if cost < best_cost:
            best_cost = cost
            best_seqs = [s.copy() for s in seqs]
        
        if cost < 0.5:
            print(f"  SOLUTION FOUND at iteration {it}!")
            return best_seqs
        
        if it % 50000 == 0:
            print(f"  Iteration {it}: cost = {cost:.1f}, best = {best_cost:.1f}, temp = {temperature:.2f}")
    
    print(f"\nBest cost: {best_cost:.1f}")
    return None


def main():
    t0 = time.time()
    
    print("="*60)
    print("SEARCHING FOR GS-DIFFERENCE FAMILY IN Z_167")
    print(f"Target: Hadamard matrix of order 4×{p} = {4*p}")
    print("="*60)
    
    # Approach 1: Orbit-based (exhaustive over coarse orbits)
    print("\n" + "="*60)
    print("APPROACH 1: QR/QNR orbit-based search")
    print("="*60)
    result = approach_multiplier_search()
    if result is not None:
        H = build_gs_hadamard(result)
        valid, msg = verify_hadamard(H)
        print(f"Verification: {msg}")
        if valid:
            np.savetxt("hadamard_668.csv", H, delimiter=",", fmt="%d")
            print("SAVED to hadamard_668.csv")
            return
    
    # Approach 2: Williamson stochastic search  
    print("\n" + "="*60)
    print("APPROACH 2: Williamson stochastic search")
    print("="*60)
    result = approach_negation_orbits()
    if result is not None:
        H = build_gs_hadamard(result)
        valid, msg = verify_hadamard(H)
        print(f"Verification: {msg}")
        if valid:
            np.savetxt("hadamard_668.csv", H, delimiter=",", fmt="%d")
            print("SAVED to hadamard_668.csv")
            return
    
    # Approach 4: Large-scale SA
    print("\n" + "="*60)
    print("APPROACH 4: Large-scale simulated annealing")
    print("="*60)
    result = approach_large_sa(max_iter=200000)
    if result is not None:
        ok, err = check_gs_family_fft(result)
        if ok:
            H = build_gs_hadamard(result)
            valid, msg = verify_hadamard(H)
            print(f"Verification: {msg}")
            if valid:
                np.savetxt("hadamard_668.csv", H, delimiter=",", fmt="%d")
                print("SAVED to hadamard_668.csv")
                return
    
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"All approaches exhausted in {elapsed:.1f}s")
    print(f"No GS-difference family found for Z_167")
    print(f"This is consistent with the open problem status of H(668)")
    
    return None

if __name__ == "__main__":
    main()
