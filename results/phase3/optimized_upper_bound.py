#!/usr/bin/env python3
"""
Optimized upper bound for B_u via slit-disk domain construction.

Carroll-Ortega-Cerda (2008) obtained B_u <= 0.6564 using 4-fold symmetric
curved-arc removal from the disk. Goodman (1945) and Beller-Hummel (1985)
used straight radial slits.

We test n-fold symmetric RADIAL SLIT configurations for n = 1, 2, ..., 12,
optimizing the slit start radius r0.

MATHEMATICAL SETUP:
For Omega_n = D \ {n equally-spaced radial slits from r0 to 1}:
  - Conformal map phi_n: D -> Omega_n with phi_n(0) = 0, phi_n'(0) > 0.
  - The normalized function g(z) = phi_n(z) / phi_n'(0) has g'(0) = 1.
  - B_g = inrad(Omega_n) / phi_n'(0) gives an upper bound on B_u.

KEY COMPUTATION: Conformal radius via symmetry reduction.
  - The map z -> z^n sends Omega_n to D \ [r0^n, 1) (single slit).
  - phi_n(z) = phi_1(z^n)^{1/n} where phi_1: D -> D \ [r0^n, 1).
  - conformal_radius(Omega_n, 0) = conformal_radius(D\[r0^n, 1), 0)^{1/n}.

SINGLE SLIT CONFORMAL RADIUS:
  For D \ [a, 1), the conformal radius at 0 is computed via the chain:
    psi: D \ [a,1) -> D  (explicitly via Cayley + square + Mobius + sqrt + inv-Cayley)
  Then conformal_radius = (1 - |psi(0)|^2) / |psi'(0)|.

INRADIUS:
  For Omega_n with n >= 2 slits, the largest inscribed disk may be centered
  either at the origin (radius r0) or on the angle bisector between two
  adjacent slits (radius min(1-d, d*sin(pi/n)) optimized over d).
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
import math
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from tracker import log_bound

# Use mpmath for high-precision conformal radius computation
from mpmath import mp, mpf, mpc, sqrt as mpsqrt, pi as mpi, cos as mpcos, sin as mpsin


def single_slit_conformal_radius(a, prec=50):
    """
    Compute the conformal radius of D \ [a, 1) at the origin.
    
    Uses the explicit chain of conformal maps:
      psi: D \ [a, 1) -> D
    via:
      1) Cayley: w1 = i(1+z)/(1-z) maps D to upper half-plane H
         Slit [a,1) maps to [iA, i*inf) where A = (1+a)/(1-a)
      2) Square: w2 = w1^2 maps H to C \ [0,inf)
         The slit [iA, i*inf) maps to (-inf, -A^2]
      3) Mobius: w3 = w2/(w2 + A^2) maps the doubly-slit plane to C \ [0,inf)
      4) Sqrt: w4 = sqrt(w3) maps C \ [0,inf) to H
      5) Inv-Cayley: w5 = (w4 - i)/(w4 + i) maps H to D
    
    Then conformal_radius = (1 - |psi(0)|^2) / |psi'(0)|.
    
    Parameters:
        a: slit start radius, 0 < a < 1
        prec: decimal precision for mpmath
    
    Returns:
        conformal_radius as float
    """
    mp.dps = prec
    a = mpf(a)
    A = (1 + a) / (1 - a)
    A2 = A**2
    
    # Track psi(0) and psi'(0) through the chain
    # Step 1: w1 = i(1+z)/(1-z), at z=0: w1 = i, dw1/dz = 2i/(1-0)^2 = 2i
    w1 = mpc(0, 1)
    dw1 = mpc(0, 2)
    
    # Step 2: w2 = w1^2
    w2 = w1**2           # = -1
    dw2 = 2 * w1 * dw1   # = 2 * i * 2i = -4
    
    # Step 3: w3 = w2 / (w2 + A^2)
    den = w2 + A2         # = -1 + A^2 = A^2 - 1
    w3 = w2 / den         # = -1 / (A^2 - 1)
    dw3 = A2 / den**2 * dw2  # chain rule: d/dz [w2/(w2+A2)] = A2/(w2+A2)^2 * dw2
    
    # Step 4: w4 = sqrt(w3) (principal branch)
    w4 = mpsqrt(w3)
    dw4 = dw3 / (2 * w4)
    
    # Step 5: w5 = (w4 - i) / (w4 + i)
    w5 = (w4 - mpc(0, 1)) / (w4 + mpc(0, 1))
    dw5 = mpc(0, -2) / (w4 + mpc(0, 1))**2 * dw4
    
    # Conformal radius of D \ [a, 1) at 0:
    # psi maps 0 in the slit-disk to w5 in D, with derivative dw5
    # conformal_radius = (1 - |w5|^2) / |dw5|
    abs_w5_sq = float(abs(w5)**2)
    abs_dw5 = float(abs(dw5))
    
    crad = (1.0 - abs_w5_sq) / abs_dw5
    
    return crad


def n_slit_conformal_radius(n_slits, r0, prec=50):
    """
    Conformal radius of D \ {n equally-spaced radial slits from r0 to 1} at origin.
    
    Uses n-fold symmetry reduction:
      The map z -> z^n sends Omega_n to D \ [r0^n, 1).
      phi_n(z) = phi_1(z^n)^{1/n}
      conformal_radius(Omega_n, 0) = conformal_radius(D\[r0^n, 1), 0)^{1/n}
    """
    a = r0**n_slits  # slit parameter for the reduced single-slit domain
    if a >= 1.0 - 1e-15:
        return 1.0  # degenerate: slit vanishes
    if a <= 1e-15:
        return 0.0  # degenerate: slit covers full radius
    
    c1_single = single_slit_conformal_radius(a, prec)
    c1_n = c1_single**(1.0 / n_slits)
    
    return c1_n


def inradius_n_slits(n_slits, r0):
    """
    Compute the inradius (largest inscribed disk radius) of 
    Omega_n = D \ {n equally-spaced radial slits from r0 to 1}.
    
    Slits are at angles 2*pi*k/n for k = 0, ..., n-1.
    
    We search along the angle bisector (angle pi/n from the real axis)
    and compare with the origin-centered disk.
    """
    if n_slits <= 0 or r0 <= 0 or r0 >= 1:
        return 0.0
    
    # Candidate 1: disk centered at origin, radius = r0
    best = r0
    
    if n_slits == 1:
        # Single slit [r0, 1) on real axis
        # The largest inscribed disk can be centered at a point on the negative real axis
        # At center (-d, 0): radius = min(1-d, sqrt(d^2 + r0^2 + 2*d*r0*cos(0)))
        # Actually for center (-d, 0): dist to slit [r0, 1) on positive axis is:
        # distance from (-d, 0) to [r0, 1) = d + r0 (since they're on opposite sides)
        # distance to unit circle = 1 - d
        # So inscribed disk radius = min(1-d, d+r0) = 1-d for small d (since d+r0 > 1-d for d > (1-r0)/2)
        # Optimal: 1-d = d+r0 => d = (1-r0)/2, radius = (1+r0)/2
        # But also need to check vertical direction: dist to boundary at (-d, 0) in 
        # direction perpendicular to slit: nearest boundary is unit circle at dist 1-d.
        # Wait, the slit is on [r0, 1), so from (-d, 0):
        # dist to nearest point on [r0, 1) = d + r0 (they're collinear, opposite sides of origin)
        # dist to unit circle = 1 - d
        # So min = min(1-d, d+r0). Set equal: d = (1-r0)/2, radius = (1+r0)/2.
        best = max(best, (1.0 + r0) / 2.0)
        return best
    
    if n_slits >= 2:
        # Search along the angle bisector between two adjacent slits
        angle = math.pi / n_slits  # half-angle between adjacent slits
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        
        def inscribed_radius_at_d(d):
            """Inscribed disk radius for center at distance d along angle bisector."""
            if d <= 0 or d >= 1:
                return 0.0
            
            # Distance to unit circle
            dist_circle = 1.0 - d
            
            # Distance to nearest slit
            # The nearest slit is at angle 0 (or 2*pi/n).
            # Center is at (d*cos(angle), d*sin(angle))
            px = d * cos_angle
            py = d * sin_angle
            
            if px >= r0:
                # The projection of center onto the slit line falls within [r0, 1)
                # Distance = perpendicular distance = py = d * sin(angle)
                dist_slit = py
            else:
                # The closest point on slit is the tip at (r0, 0)
                dist_slit = math.sqrt((px - r0)**2 + py**2)
            
            return min(dist_circle, dist_slit)
        
        # Optimize over d
        # The optimal d is where dist_circle = dist_slit
        # Case 1: px >= r0, so dist_slit = d*sin(angle)
        # 1-d = d*sin(angle) => d = 1/(1+sin(angle))
        d_opt_case1 = 1.0 / (1.0 + sin_angle)
        if d_opt_case1 * cos_angle >= r0 and d_opt_case1 < 1:
            r_case1 = inscribed_radius_at_d(d_opt_case1)
            best = max(best, r_case1)
        
        # Case 2: px < r0, search numerically
        # 1-d = sqrt((d*cos(angle) - r0)^2 + (d*sin(angle))^2)
        # (1-d)^2 = (d*cos_a - r0)^2 + d^2*sin_a^2
        # 1-2d+d^2 = d^2*cos_a^2 - 2d*r0*cos_a + r0^2 + d^2*sin_a^2
        # 1-2d+d^2 = d^2 - 2d*r0*cos_a + r0^2
        # 1-2d = -2d*r0*cos_a + r0^2
        # 2d*(r0*cos_a - 1) = r0^2 - 1
        # 2d*(r0*cos_a - 1) = -(1-r0^2)
        # d = (1-r0^2) / (2*(1-r0*cos_a))
        d_opt_case2 = (1.0 - r0**2) / (2.0 * (1.0 - r0 * cos_angle))
        if 0 < d_opt_case2 < 1 and d_opt_case2 * cos_angle < r0:
            r_case2 = inscribed_radius_at_d(d_opt_case2)
            best = max(best, r_case2)
        
        # Also do a fine grid search for safety
        for d_try in np.linspace(0.01, 0.99, 1000):
            r_try = inscribed_radius_at_d(d_try)
            if r_try > best:
                best = r_try
    
    return best


def Bu_upper_bound_slit_disk(n_slits, r0, prec=50):
    """
    Compute B_u upper bound from the n-slit-disk domain.
    
    B_f = inrad(Omega_n) / conformal_radius(Omega_n, 0)
    
    Returns (B_f, conformal_radius, inradius).
    """
    inrad = inradius_n_slits(n_slits, r0)
    crad = n_slit_conformal_radius(n_slits, r0, prec)
    
    if crad <= 0:
        return float('inf'), crad, inrad
    
    Bf = inrad / crad
    return Bf, crad, inrad


def optimize_upper_bound(n_slits, prec=50):
    """
    Optimize the inner radius r0 to minimize B_f = inrad / conformal_radius
    for a given number of slits.
    
    Returns (best_r0, best_Bf).
    """
    def objective(r0):
        if r0 <= 0.02 or r0 >= 0.98:
            return 10.0  # large value for boundary
        try:
            Bf, _, _ = Bu_upper_bound_slit_disk(n_slits, r0, prec)
            return Bf
        except Exception:
            return 10.0
    
    # Coarse search
    r0_values = np.linspace(0.05, 0.95, 100)
    Bf_values = np.array([objective(r0) for r0 in r0_values])
    
    best_idx = np.argmin(Bf_values)
    best_r0 = r0_values[best_idx]
    
    # Fine search around best
    r0_fine = np.linspace(max(0.03, best_r0 - 0.05), min(0.97, best_r0 + 0.05), 500)
    Bf_fine = np.array([objective(r0) for r0 in r0_fine])
    
    best_idx2 = np.argmin(Bf_fine)
    best_r0 = r0_fine[best_idx2]
    best_Bf = Bf_fine[best_idx2]
    
    # Ultra-fine search
    r0_uf = np.linspace(max(0.03, best_r0 - 0.005), min(0.97, best_r0 + 0.005), 500)
    Bf_uf = np.array([objective(r0) for r0 in r0_uf])
    
    best_idx3 = np.argmin(Bf_uf)
    best_r0 = r0_uf[best_idx3]
    best_Bf = Bf_uf[best_idx3]
    
    return best_r0, best_Bf


def verify_single_slit_conformal_radius():
    """
    Verification tests for the conformal radius computation.
    """
    print("VERIFICATION TESTS")
    print("-" * 50)
    
    # Test 1: As a -> 1 (no slit), conformal radius -> 1
    for a in [0.99, 0.999, 0.9999]:
        cr = single_slit_conformal_radius(a)
        print(f"  a={a}: crad = {cr:.10f} (expected -> 1.0)")
    
    # Test 2: As a -> 0 (full slit), conformal radius -> 0
    for a in [0.1, 0.01, 0.001]:
        cr = single_slit_conformal_radius(a)
        print(f"  a={a}: crad = {cr:.10f} (expected -> 0)")
    
    # Test 3: For n=1 slit, the conformal radius should be between 0 and 1
    for a in [0.3, 0.5, 0.7]:
        cr = single_slit_conformal_radius(a)
        ok = "OK" if 0 < cr < 1 else "FAIL"
        print(f"  a={a}: crad = {cr:.10f} (in (0,1)? {ok})")
    
    # Test 4: B_f = inrad / crad should be > 0.5 for reasonable parameters
    # For n=1 slit with r0=0.5: inrad = (1+0.5)/2 = 0.75, crad = single_slit_cr(0.5)
    r0 = 0.5
    cr = single_slit_conformal_radius(r0)
    inrad = (1.0 + r0) / 2.0
    Bf = inrad / cr
    print(f"  n=1, r0={r0}: inrad={inrad:.6f}, crad={cr:.6f}, B_f={Bf:.6f}")
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("OPTIMIZED UPPER BOUND ON B_u VIA SLIT-DISK DOMAINS")
    print("=" * 70)
    print(f"Current best: B_u <= 0.6564 (Carroll-Ortega-Cerda 2008)")
    print(f"Known lower:  B_u >  0.5708858 (Skinner 2009)")
    print()
    
    # Verify the conformal radius computation first
    verify_single_slit_conformal_radius()
    
    # Run optimization for each number of slits
    results = []
    
    print("OPTIMIZATION RESULTS")
    print("-" * 70)
    print(f"{'n_slits':>7} {'best_r0':>10} {'B_f':>12} {'crad':>12} {'inrad':>10} {'status':>12}")
    print("-" * 70)
    
    for n_slits in range(1, 13):
        best_r0, best_Bf = optimize_upper_bound(n_slits, prec=50)
        
        # Also get detailed values at the optimum
        Bf_check, c1, inrad = Bu_upper_bound_slit_disk(n_slits, best_r0, prec=50)
        
        status = ""
        if best_Bf < 0.6564:
            status = "< Carroll-OC"
        if best_Bf < 0.5708858:
            status = "IMPOSSIBLE"  # would contradict Skinner
        
        print(f"{n_slits:>7} {best_r0:>10.6f} {best_Bf:>12.8f} {c1:>12.8f} {inrad:>10.6f} {status:>12}")
        
        results.append({
            "n_slits": n_slits,
            "best_r0": float(best_r0),
            "best_Bf": float(best_Bf),
            "conformal_radius": float(c1),
            "inrad": float(inrad)
        })
    
    # Find best overall
    best_result = min(results, key=lambda r: r["best_Bf"])
    
    print()
    print("=" * 70)
    print(f"Best upper bound: B_u <= {best_result['best_Bf']:.10f}")
    print(f"  Achieved with {best_result['n_slits']} slits at r0 = {best_result['best_r0']:.6f}")
    print(f"  Conformal radius = {best_result['conformal_radius']:.10f}")
    print(f"  Inradius = {best_result['inrad']:.10f}")
    
    if best_result['best_Bf'] < 0.6564:
        print(f"  ** IMPROVEMENT over Carroll-Ortega-Cerda's 0.6564! **")
        improvement = 0.6564 - best_result['best_Bf']
        print(f"  Improvement: {improvement:.10f}")
    else:
        print(f"  (Not better than Carroll-Ortega-Cerda's 0.6564)")
    
    if best_result['best_Bf'] < 0.5708858:
        print(f"  ** WARNING: This would contradict Skinner's lower bound! Check computation. **")
    
    # Log the result
    log_bound(best_result['best_Bf'], "upper",
              f"slit_disk_{best_result['n_slits']}_slits_corrected",
              "results/phase3/optimized_upper_bound.py",
              f"Corrected slit-disk with {best_result['n_slits']} slits, r0={best_result['best_r0']:.6f}. "
              f"Conformal radius via exact Cayley+Joukowsky chain.")
    
    # Save detailed results
    import json
    results_path = "results/phase3/upper_bound_results.json"
    with open(results_path, "w") as f:
        json.dump({
            "method": "radial_slit_disk_domains",
            "conformal_radius_method": "exact_cayley_joukowsky_chain",
            "inradius_method": "geometric_bisector_optimization",
            "symmetry_reduction": "z^n_map_to_single_slit",
            "best_result": best_result,
            "all_results": results,
            "comparison": {
                "Carroll_Ortega_Cerda_2008": 0.6564,
                "Skinner_lower_bound_2009": 0.5708858,
                "our_best": best_result["best_Bf"]
            }
        }, f, indent=2)
    
    print(f"\nResults saved to {results_path}")
