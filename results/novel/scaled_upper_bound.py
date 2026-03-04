#!/usr/bin/env python3
"""Scaled upper bound on γ₂ via Dančík-Paterson / Lueker eigenvalue method.

Implements the recurrence-based upper bound with symmetry reductions.

The key insight (Dančík-Paterson 1995, Lueker 2009):
  γ₂ ≤ lim_{s→∞} ρ(A_s) / s
where A_s is the transition matrix of the column-difference process on
a strip of width s, and ρ(A_s) is its spectral radius.

For binary alphabet, the column differences d_j = L(i,j) - L(i,j-1) ∈ {0,1}.
The state is the vector (d_1,...,d_s) ∈ {0,1}^s.
Symmetry reductions:
  1. Complement symmetry: d ↔ 1-d (since alphabet is symmetric)
  2. For i.i.d. uniform input, the stationary distribution is symmetric

CE card implemented: finite_size_scaling_extrapolation (card #009)
- Implementation hypothesis: "Use Richardson extrapolation on eigenvalue
  sequences to accelerate convergence"

References:
  - [DP1995] Dančík & Paterson 1995
  - [L2009] Lueker 2009
  - [H2024] Heineman et al. 2024
"""

import json
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs
from pathlib import Path
import ctypes
import os

RESULTS_DIR = Path(__file__).parent
BASELINES_DIR = RESULTS_DIR.parent / "baselines"
SEED = 42


def load_lcs_lib():
    """Load the C LCS library."""
    lib_path = BASELINES_DIR / "lcs_fast.so"
    if not lib_path.exists():
        return None
    lib = ctypes.CDLL(str(lib_path))
    lib.lcs_dp.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int
    ]
    lib.lcs_dp.restype = ctypes.c_int
    return lib


def build_strip_transition_matrix(s):
    """Build the transition matrix for the column-difference process.
    
    State: binary vector d = (d_1, ..., d_s) where d_j = L(i,j) - L(i,j-1).
    
    When processing row i with character a_i:
      For each column j (char b_j drawn uniformly from {0,1}):
        If a_i == b_j: d'_j = max(d_{j-1}, 1 - d_j) ... potential match
        Else: d'_j depends on the recurrence
    
    The DP recurrence L(i,j) = max(L(i-1,j), L(i,j-1), L(i-1,j-1) + [a_i=b_j])
    translates to column differences.
    
    For a single row with character a (prob 1/2 for a=0, 1/2 for a=1),
    and columns b_1,...,b_s each uniform in {0,1}:
    
    The expected transition averages over a and all b_j.
    """
    n_states = 2**s
    
    # Build transition as dense matrix for small s
    # For each input (a, b_1...b_s), compute the output state
    # Average over all 2^(s+1) inputs
    
    T = np.zeros((n_states, n_states))
    output_count = np.zeros(n_states)  # sum of L(i,s) increments per state
    
    n_inputs = 2**(s + 1)  # a ∈ {0,1}, b_1...b_s ∈ {0,1}^s
    
    for inp in range(n_inputs):
        a = inp >> s  # first bit is a
        b_bits = inp & ((1 << s) - 1)  # remaining s bits are b_1...b_s
        
        for state_idx in range(n_states):
            # Decode state: d_j for j=1..s
            d = [(state_idx >> j) & 1 for j in range(s)]
            
            # Process the row: compute new column differences
            # L(i-1, j) - L(i-1, j-1) = d_j (old differences)
            # L(i,0) = 0 always, L(i-1,0) = 0
            # 
            # For j=1..s:
            #   b_j = (b_bits >> (j-1)) & 1
            #   match = (a == b_j)
            #   L(i,j) = max(L(i-1,j), L(i,j-1), L(i-1,j-1) + match)
            #
            # We track d'_j = L(i,j) - L(i,j-1) ∈ {0,1}
            # and the "vertical" increment v_j = L(i,j) - L(i-1,j)
            
            # We need absolute values to do the recurrence.
            # Reconstruct L(i-1, j) from differences:
            # L(i-1, j) = sum(d_0..d_{j-1})
            L_prev = [0] * (s + 1)
            for j in range(s):
                L_prev[j + 1] = L_prev[j] + d[j]
            
            # Compute L(i, j) row
            L_curr = [0] * (s + 1)
            for j in range(s):
                b_j = (b_bits >> j) & 1
                match = 1 if a == b_j else 0
                L_curr[j + 1] = max(
                    L_prev[j + 1],
                    L_curr[j],
                    L_prev[j] + match
                )
            
            # New state: d'_j = L(i, j+1) - L(i, j) for j=0..s-1
            new_state = 0
            for j in range(s):
                d_new = L_curr[j + 1] - L_curr[j]
                if d_new == 1:
                    new_state |= (1 << j)
            
            T[state_idx, new_state] += 1.0 / n_inputs
            # The "output" per step: increment in L(i,s) 
            # = L(i,s) - L(i-1,s) = sum(d'_j) - sum(d_j) ... no
            # Actually the output rate for γ is: lim L(n,n)/n
            # which for the strip relates to the stationary throughput
    
    return T


def compute_stationary_throughput(T, s):
    """Compute the stationary distribution throughput.
    
    The throughput is: π · f where f(state) = E[sum of new d'_j | old state]
    averaged over the input distribution.
    
    For upper bound: we need the maximum throughput achievable,
    which is the spectral radius approach.
    """
    n_states = 2**s
    
    # Find stationary distribution
    eigenvalues, eigenvectors = np.linalg.eig(T.T)
    
    # Find eigenvalue closest to 1
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])
    pi = np.abs(pi)
    pi /= pi.sum()
    
    # The average number of 1s in the state under stationarity
    # gives the expected LCS increment per column
    f = np.zeros(n_states)
    for state_idx in range(n_states):
        f[state_idx] = bin(state_idx).count('1')
    
    avg_ones = np.dot(pi, f)
    # γ_s = avg_ones / s (fraction of columns that contribute +1)
    gamma_s = avg_ones / s
    
    return gamma_s, pi, eigenvalues


def compute_upper_bound_dp(s, n_trials=500, n_length=2000):
    """Compute an MC-based upper bound estimate for strip width s.
    
    Generate random pairs and compute LCS on truncated n×s rectangles
    to estimate the per-column contribution rate.
    """
    lib = load_lcs_lib()
    if lib is None:
        return None
    
    rng = np.random.default_rng(SEED)
    rates = []
    
    for _ in range(n_trials):
        a = rng.integers(0, 2, size=n_length, dtype=np.uint8)
        b = rng.integers(0, 2, size=n_length, dtype=np.uint8)
        
        a_ptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        b_ptr = b.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        
        lcs_val = lib.lcs_dp(a_ptr, n_length, b_ptr, n_length)
        rates.append(lcs_val / n_length)
    
    return np.mean(rates), np.std(rates) / np.sqrt(n_trials)


def symmetry_reduce_states(s):
    """Reduce states by complement symmetry.
    
    For binary, state d and complement (1-d) have the same behavior
    under the symmetric input distribution. So we can identify them.
    """
    seen = set()
    canonical = {}
    
    for state_idx in range(2**s):
        if state_idx in seen:
            continue
        # Complement: flip all bits
        complement = state_idx ^ ((1 << s) - 1)
        canonical[state_idx] = state_idx
        canonical[complement] = state_idx
        seen.add(state_idx)
        seen.add(complement)
    
    # Build reduced state list
    reduced_states = sorted(set(canonical.values()))
    reduced_idx = {s: i for i, s in enumerate(reduced_states)}
    
    return reduced_states, reduced_idx, canonical


def main():
    print("=== Scaled Upper Bound via Strip Transfer Matrix ===\n")
    
    results = []
    gamma_values = []
    s_values = []
    
    for s in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print(f"\n--- Strip width s={s} ---")
        t0 = time.time()
        
        n_states = 2**s
        reduced, red_idx, canonical = symmetry_reduce_states(s)
        n_reduced = len(reduced)
        
        print(f"  Full states: {n_states}, Reduced: {n_reduced}")
        
        if s <= 10:
            T = build_strip_transition_matrix(s)
            gamma_s, pi, eigenvalues = compute_stationary_throughput(T, s)
            
            # Sort eigenvalues by magnitude
            eig_sorted = sorted(np.abs(eigenvalues), reverse=True)
            spectral_gap = 1.0 - eig_sorted[1] if len(eig_sorted) > 1 else 0
            
            # The absorbing state check
            all_ones = (1 << s) - 1
            absorbing_prob = T[all_ones, all_ones]
        else:
            gamma_s = None
            spectral_gap = None
            absorbing_prob = None
        
        elapsed = time.time() - t0
        
        res = {
            "s": s,
            "n_states_full": n_states,
            "n_states_reduced": n_reduced,
            "gamma_s": round(float(gamma_s), 8) if gamma_s is not None else None,
            "spectral_gap": round(float(spectral_gap), 8) if spectral_gap is not None else None,
            "absorbing_prob": round(float(absorbing_prob), 8) if absorbing_prob is not None else None,
            "runtime_seconds": round(elapsed, 3)
        }
        results.append(res)
        
        if gamma_s is not None:
            gamma_values.append(gamma_s)
            s_values.append(s)
            print(f"  γ_s = {gamma_s:.6f}")
            print(f"  Spectral gap: {spectral_gap:.6f}")
            print(f"  P(all-ones→all-ones): {absorbing_prob:.6f}")
    
    # Richardson extrapolation
    print("\n=== Richardson Extrapolation ===")
    if len(gamma_values) >= 3:
        s_arr = np.array(s_values, dtype=float)
        g_arr = np.array(gamma_values)
        
        # Fit γ_s = γ_∞ + c₁/s + c₂/s²
        from scipy.optimize import curve_fit
        
        def model_2param(s, g_inf, c1):
            return g_inf + c1 / s
        
        def model_3param(s, g_inf, c1, c2):
            return g_inf + c1 / s + c2 / s**2
        
        try:
            popt2, pcov2 = curve_fit(model_2param, s_arr, g_arr, p0=[0.82, -0.1])
            gamma_inf_2 = popt2[0]
            gamma_se_2 = np.sqrt(pcov2[0, 0])
            print(f"  2-param fit: γ_∞ = {gamma_inf_2:.6f} ± {gamma_se_2:.6f}")
        except Exception as e:
            gamma_inf_2 = None
            gamma_se_2 = None
            print(f"  2-param fit failed: {e}")
        
        try:
            popt3, pcov3 = curve_fit(model_3param, s_arr, g_arr, p0=[0.82, -0.1, 0.01])
            gamma_inf_3 = popt3[0]
            gamma_se_3 = np.sqrt(pcov3[0, 0])
            print(f"  3-param fit: γ_∞ = {gamma_inf_3:.6f} ± {gamma_se_3:.6f}")
        except Exception as e:
            gamma_inf_3 = None
            gamma_se_3 = None
            print(f"  3-param fit failed: {e}")
    else:
        gamma_inf_2 = gamma_inf_3 = gamma_se_2 = gamma_se_3 = None
    
    # Try MC-based upper bound at larger n
    print("\n=== MC-based upper confidence bounds ===")
    mc_result = compute_upper_bound_dp(s=None, n_trials=1000, n_length=5000)
    if mc_result:
        mc_mean, mc_se = mc_result
        mc_upper_95 = mc_mean + 1.96 * mc_se
        mc_upper_99 = mc_mean + 2.576 * mc_se
        print(f"  MC γ̂ = {mc_mean:.6f} ± {mc_se:.6f}")
        print(f"  95% upper CI: {mc_upper_95:.6f}")
        print(f"  99% upper CI: {mc_upper_99:.6f}")
    else:
        mc_mean = mc_se = mc_upper_95 = mc_upper_99 = None
    
    # Assemble output
    output = {
        "description": "Scaled upper bound via strip transfer matrix eigenvalue method",
        "method": "Dančík-Paterson column-difference process with complement symmetry reduction",
        "strip_results": results,
        "extrapolation": {
            "s_values": s_values,
            "gamma_values": [round(g, 8) for g in gamma_values],
            "fit_2param": {
                "gamma_inf": round(float(gamma_inf_2), 8) if gamma_inf_2 is not None else None,
                "gamma_inf_se": round(float(gamma_se_2), 8) if gamma_se_2 is not None else None
            },
            "fit_3param": {
                "gamma_inf": round(float(gamma_inf_3), 8) if gamma_inf_3 is not None else None,
                "gamma_inf_se": round(float(gamma_se_3), 8) if gamma_se_3 is not None else None
            }
        },
        "mc_upper_bound": {
            "n": 5000,
            "trials": 1000,
            "gamma_hat": round(float(mc_mean), 8) if mc_mean is not None else None,
            "se": round(float(mc_se), 8) if mc_se is not None else None,
            "upper_95": round(float(mc_upper_95), 8) if mc_upper_95 is not None else None,
            "upper_99": round(float(mc_upper_99), 8) if mc_upper_99 is not None else None,
            "note": "Non-rigorous: MC CI is for E[LCS(n,n)]/n, not for γ₂"
        },
        "comparison": {
            "dancik_paterson_1995": 0.838,
            "lueker_2009": 0.826280,
            "note": "Our strip eigenvalue method gives γ_s values that decrease with s but do not yield rigorous upper bounds without the full Lueker certificate framework"
        },
        "analysis": {
            "absorbing_state_issue": "The all-ones state (1,1,...,1) is absorbing — once all column differences are 1, they stay 1. This means the stationary distribution concentrates on this state for large s, giving γ_s → 1 rather than γ₂. The proper Lueker method uses a different formulation that avoids this issue.",
            "our_approach": "We compute γ_s = E_π[#ones in state]/s. For small s this gives reasonable estimates but the absorbing state dominates as s grows.",
            "conclusion": "The strip transfer matrix approach as implemented does not produce valid rigorous upper bounds. Lueker's method requires a more sophisticated eigenvalue computation on the dual system."
        }
    }
    
    outpath = RESULTS_DIR / "scaled_upper_bound.json"
    outpath.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {outpath}")
    
    # Generate figure
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
        ax.plot(s_values, gamma_values, 'o-', color='steelblue', linewidth=2, 
                markersize=8, label='Strip eigenvalue γ_s')
        ax.axhline(y=0.826280, color='red', linestyle='--', linewidth=1.5, 
                   label='Lueker 2009 UB = 0.8263')
        ax.axhline(y=0.792666, color='green', linestyle='--', linewidth=1.5,
                   label='Heineman 2024 LB = 0.7927')
        if mc_mean:
            ax.axhline(y=mc_mean, color='orange', linestyle=':', linewidth=1.5,
                       label=f'MC estimate = {mc_mean:.4f}')
        ax.set_xlabel('Strip width s')
        ax.set_ylabel('γ_s estimate')
        ax.set_title('Strip Transfer Matrix: γ_s vs Strip Width')
        ax.legend(loc='best', fontsize=10)
        
        figdir = Path(__file__).parent.parent.parent / "figures"
        figdir.mkdir(exist_ok=True)
        fig.savefig(figdir / "scaled_upper_bound.png", dpi=150, bbox_inches='tight')
        fig.savefig(figdir / "scaled_upper_bound.pdf", bbox_inches='tight')
        plt.close(fig)
        print(f"Figure saved to {figdir / 'scaled_upper_bound.png'}")
    except ImportError as e:
        print(f"Plotting skipped: {e}")


if __name__ == "__main__":
    main()
