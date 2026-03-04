#!/usr/bin/env python3
"""
Grunsky-constrained adversarial search for extremal univalent functions.

Searches for univalent f in S that MINIMIZE inrad(f(D)), giving UPPER BOUNDS on B_u.

The Grunsky matrix constraint ||G_N||_op <= 1 is a necessary condition for
univalence (but not sufficient). Combined with de Branges bounds |a_n| <= n,
this constrains the feasible set of Taylor coefficients.

METHOD:
1. Parameterize f(z) = z + a_2 z^2 + ... + a_N z^N
2. Minimize inrad(f(D)) = min_{|z|=1} |f(z)| subject to:
   - ||G_K||_op <= 1  (Grunsky, K = small truncation)
   - |a_n| <= n (de Branges)
3. Verify univalence of best candidates numerically
"""

import numpy as np
from scipy.optimize import minimize as sp_minimize
import sys, os, json, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from tracker import log_bound

np.random.seed(42)

# Precompute boundary points
N_BDY = 4000
THETA = np.linspace(0, 2 * np.pi, N_BDY, endpoint=False)
Z_BDY = 0.9999 * np.exp(1j * THETA)
Z_POW = {}


def precompute_zpow(max_deg):
    global Z_POW
    Z_POW = {k: Z_BDY ** k for k in range(2, max_deg + 1)}


def compute_grunsky_2x2(a):
    """
    Compute the 2x2 normalized Grunsky matrix directly.
    Requires a_2, a_3, a_4, a_5 (indices 0-3 in a).
    
    b_{11} = a_2^2 - a_3
    b_{12} = b_{21} = -a_4 + 2*a_2*a_3 - a_2^3  
    b_{22} = -a_5 + 2*a_2*a_4 + 3/2*a_3^2 - 4*a_2^2*a_3 + 3/2*a_2^4
    
    G_{mn} = sqrt(m*n) * b_{mn}
    """
    a2 = a[0] if len(a) > 0 else 0.0
    a3 = a[1] if len(a) > 1 else 0.0
    a4 = a[2] if len(a) > 2 else 0.0
    a5 = a[3] if len(a) > 3 else 0.0
    
    b11 = a2**2 - a3
    b12 = -a4 + 2*a2*a3 - a2**3
    b22 = -a5 + 2*a2*a4 + 1.5*a3**2 - 4*a2**2*a3 + 1.5*a2**4
    
    # Normalized: G_{mn} = sqrt(m*n) * b_{mn}
    G = np.array([
        [1.0 * b11,        np.sqrt(2) * b12],
        [np.sqrt(2) * b12, 2.0 * b22       ]
    ], dtype=complex)
    
    return G


def compute_grunsky_3x3(a):
    """
    Compute the 3x3 normalized Grunsky matrix.
    Requires a_2, ..., a_7 (indices 0-5 in a).
    Uses the general bivariate log expansion.
    """
    N = 3
    n_a = len(a)
    max_k = 2*N + n_a + 3
    f = np.zeros(max_k, dtype=complex)
    f[1] = 1.0
    for k in range(2, min(max_k, n_a + 2)):
        f[k] = a[k - 2]
    
    M2 = 2*N + 2
    P = np.zeros((M2, M2), dtype=complex)
    for i in range(M2):
        for j in range(M2):
            idx = i + j + 1
            if idx < len(f):
                P[i, j] = f[idx]
    
    Q = P.copy()
    Q[0, 0] -= 1.0
    
    # log(1+Q) via formal power series
    logP = np.zeros((M2, M2), dtype=complex)
    Qpow = Q.copy()
    
    for k in range(1, M2 + 1):
        sign = (-1.0) ** (k + 1)
        logP += sign * Qpow / k
        if k < M2:
            new_Qpow = np.zeros((M2, M2), dtype=complex)
            for i in range(M2):
                for j in range(M2):
                    s = 0.0 + 0.0j
                    for ai in range(i + 1):
                        ci = i - ai
                        for bj in range(j + 1):
                            dj = j - bj
                            s += Qpow[ai, bj] * Q[ci, dj]
                    new_Qpow[i, j] = s
            Qpow = new_Qpow
    
    b = np.zeros((N, N), dtype=complex)
    for m in range(1, N + 1):
        for n in range(1, N + 1):
            b[m-1, n-1] = -logP[m, n]
    
    G = np.zeros_like(b)
    for m in range(N):
        for n in range(N):
            G[m, n] = np.sqrt((m+1)*(n+1)) * b[m, n]
    return G


def grunsky_norm_2x2(a):
    """Fast 2x2 Grunsky norm using direct formulas."""
    G = compute_grunsky_2x2(a)
    return np.linalg.norm(G, ord=2)


def grunsky_norm_3x3(a):
    """3x3 Grunsky norm (slower, needs a_2,...,a_7)."""
    G = compute_grunsky_3x3(a)
    return np.linalg.norm(G, ord=2)


def fast_inradius(a_coeffs):
    """Inradius centered at 0: min |f(z)| on |z|~1."""
    fz = Z_BDY.copy()
    for k in range(len(a_coeffs)):
        if k + 2 in Z_POW:
            fz = fz + a_coeffs[k] * Z_POW[k + 2]
    return np.min(np.abs(fz))


def full_inradius(a_coeffs, n_bdy=20000):
    """Inradius with center search."""
    theta = np.linspace(0, 2*np.pi, n_bdy, endpoint=False)
    z = 0.9999 * np.exp(1j * theta)
    fz = z.copy()
    for k in range(len(a_coeffs)):
        fz += a_coeffs[k] * z**(k+2)
    
    inrad_0 = np.min(np.abs(fz))
    best = inrad_0
    best_c = 0.0
    
    cx = np.linspace(-0.8, 0.8, 50)
    cy = np.linspace(-0.8, 0.8, 50)
    for x in cx:
        shifted = fz[np.newaxis, :] - (x + 1j * cy[:, np.newaxis])
        mins = np.min(np.abs(shifted), axis=1)
        idx = np.argmax(mins)
        if mins[idx] > best:
            best = mins[idx]
            best_c = x + 1j * cy[idx]
    
    return best, best_c


def verify_univalence_strict(a_coeffs, n_grid=200):
    """
    Strict univalence check:
    1. f'(z) != 0 on D (local univalence)
    2. Winding number of f(|z|=r) around 0 is exactly 1 (for f(0)=0)
    3. Boundary curve has no self-intersections
    """
    n_coeffs = len(a_coeffs)
    
    # Check f' != 0
    r_vals = np.linspace(0, 0.99, n_grid // 2)
    theta_vals = np.linspace(0, 2*np.pi, n_grid, endpoint=False)
    
    min_fp = float('inf')
    for r in r_vals:
        z = r * np.exp(1j * theta_vals)
        fprime = np.ones_like(z, dtype=complex)
        for k in range(n_coeffs):
            fprime += (k+2) * a_coeffs[k] * z**(k+1)
        mfp = np.min(np.abs(fprime))
        if mfp < min_fp:
            min_fp = mfp
    
    if min_fp < 1e-6:
        return False, min_fp
    
    # Check winding number of f(boundary) around 0
    n_bdy = 10000
    theta_bdy = np.linspace(0, 2*np.pi, n_bdy, endpoint=False)
    z_bdy = 0.9999 * np.exp(1j * theta_bdy)
    fz = z_bdy.copy()
    for k in range(n_coeffs):
        fz += a_coeffs[k] * z_bdy**(k+2)
    
    # Winding number around 0
    angles = np.angle(fz)
    dangle = np.diff(angles)
    dangle = np.mod(dangle + np.pi, 2*np.pi) - np.pi
    winding = np.sum(dangle) / (2*np.pi)
    
    if abs(winding - 1.0) > 0.1:  # not winding once around 0
        return False, min_fp
    
    # Check for self-intersections of boundary curve
    # Use spatial proximity check: points far apart in parameter
    # should not be close in image
    pts = np.column_stack([fz.real, fz.imag])
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    pairs = tree.query_pairs(r=0.005)
    
    for (i, j) in pairs:
        param_dist = min(abs(i-j), n_bdy - abs(i-j))
        if param_dist > n_bdy // 10:  # far in parameter, close in image
            return False, min_fp
    
    return True, min_fp


def adversarial_search(N, n_restarts=15, verbose=True):
    """Search for min-inrad univalent f at polynomial degree N."""
    n_coeffs = N - 1
    precompute_zpow(N)
    
    # Use 2x2 Grunsky for speed (requires a_2,...,a_5)
    use_3x3 = (N >= 8)  # only use 3x3 for high degree
    
    best_inrad = float('inf')
    best_a = None
    best_gnorm = None
    penalty_w = 500.0
    
    # Precompute a fine boundary for winding checks
    n_wind = 2000
    theta_w = np.linspace(0, 2*np.pi, n_wind, endpoint=False)
    z_w = 0.9999 * np.exp(1j * theta_w)
    z_w_pow = {k: z_w**k for k in range(2, N+1)}
    
    def objective(x):
        a_re = x[:n_coeffs]
        a_im = x[n_coeffs:]
        a = a_re + 1j * a_im
        
        # De Branges penalty
        db_pen = sum(max(0, abs(a[k]) - (k+2))**2 for k in range(n_coeffs))
        
        # Grunsky penalty
        try:
            gnorm = grunsky_norm_2x2(a)
            g_pen = max(0, gnorm - 1.0)**2
        except Exception:
            g_pen = 10.0
        
        # Evaluate f on boundary
        fz_bdy = z_w.copy()
        for k in range(n_coeffs):
            fz_bdy = fz_bdy + a[k] * z_w_pow[k + 2]
        
        # Winding number penalty (HARD: must be exactly 1)
        angles = np.angle(fz_bdy)
        dangle = np.diff(angles)
        dangle = np.mod(dangle + np.pi, 2*np.pi) - np.pi
        winding = np.sum(dangle) / (2*np.pi)
        winding_pen = (winding - 1.0)**2
        
        # If winding is wrong, return huge penalty immediately
        if abs(winding - 1.0) > 0.3:
            return 100.0 + penalty_w * winding_pen
        
        # Inradius at origin (only meaningful if winding = 1)
        ir = np.min(np.abs(fz_bdy))
        
        # Also check for self-crossings: the argument of f(z) should be 
        # monotonically increasing (simple curve condition)
        arg_fz = np.unwrap(np.angle(fz_bdy))
        darg = np.diff(arg_fz)
        # For a simple closed curve traversed once, darg should be mostly positive
        # Count backwards steps
        backwards = np.sum(darg < -0.01)
        backwards_pen = backwards / n_wind  # fraction of backwards steps
        
        return ir + penalty_w * (g_pen + db_pen + winding_pen + backwards_pen)
    
    for restart in range(n_restarts):
        if restart == 0:
            x0 = np.zeros(2 * n_coeffs)
        elif restart == 1:
            # Near Koebe (scaled down to stay univalent)
            x0 = np.zeros(2 * n_coeffs)
            for k in range(n_coeffs):
                x0[k] = (k+2) * 0.15
        elif restart == 2:
            x0 = np.zeros(2 * n_coeffs)
            x0[0] = 1.9  # near Bieberbach bound
        elif restart == 3:
            x0 = np.zeros(2 * n_coeffs)
            x0[0] = -1.9
        elif restart == 4:
            x0 = np.zeros(2 * n_coeffs)
            x0[n_coeffs] = 1.9  # imaginary a_2
        elif restart == 5:
            # Near the conjectured extremal (slit-like)
            x0 = np.zeros(2 * n_coeffs)
            x0[0] = 2.0  # a_2 = 2
            if n_coeffs > 1:
                x0[1] = 3.0  # a_3 = 3 (Koebe-like)
        else:
            scale = np.array([1.5 / (k+2) for k in range(n_coeffs)])
            x0 = np.concatenate([
                np.random.randn(n_coeffs) * scale,
                np.random.randn(n_coeffs) * scale
            ])
        
        # Two-phase optimization
        res1 = sp_minimize(objective, x0, method='Nelder-Mead',
                          options={'maxiter': 30000, 'xatol': 1e-10, 
                                   'fatol': 1e-10, 'adaptive': True})
        res2 = sp_minimize(objective, res1.x, method='Powell',
                          options={'maxiter': 15000, 'xtol': 1e-10})
        
        x_best = res2.x if res2.fun < res1.fun else res1.x
        a = x_best[:n_coeffs] + 1j * x_best[n_coeffs:]
        
        ir = fast_inradius(a)
        try:
            gnorm = grunsky_norm_2x2(a)
        except Exception:
            gnorm = 999.0
        
        if gnorm <= 1.02 and ir < best_inrad:
            best_inrad = ir
            best_a = a.copy()
            best_gnorm = gnorm
            
            if verbose:
                is_u, mfp = verify_univalence_strict(a, n_grid=100)
                print(f"  Restart {restart:3d}: inrad={ir:.8f}, "
                      f"||G2||={gnorm:.6f}, univ={is_u}, min|f'|={mfp:.6f}")
    
    return best_a, best_inrad, best_gnorm


def test_basic():
    """Quick verification."""
    print("VERIFICATION")
    print("-" * 50)
    
    # b_11 for f(z)=z+0.5z^2
    a = np.array([0.5, 0.0, 0.0, 0.0], dtype=complex)
    G = compute_grunsky_2x2(a)
    print(f"  z+0.5z^2: G_11 = {G[0,0]:.4f} (expect 0.25), ||G|| = {np.linalg.norm(G,ord=2):.4f}")
    
    # Koebe a_n=n, should have ||G||=1
    a_k = np.array([2,3,4,5], dtype=complex)
    G_k = compute_grunsky_2x2(a_k)
    print(f"  Koebe: ||G_2|| = {np.linalg.norm(G_k,ord=2):.6f} (expect 1.0)")
    
    # Identity
    a_id = np.array([0,0,0,0], dtype=complex)
    precompute_zpow(5)
    ir = fast_inradius(a_id)
    print(f"  Identity inrad: {ir:.6f} (expect ~1.0)")
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("GRUNSKY-CONSTRAINED ADVERSARIAL SEARCH")
    print("=" * 70)
    print(f"Known: 0.5708858 < B_u <= 0.6564")
    print()
    
    test_basic()
    
    all_results = []
    
    for N in [3, 4, 5, 6, 7, 8, 10]:
        t0 = time.time()
        print(f"\n{'='*60}")
        print(f"Degree N = {N}")
        print(f"{'='*60}")
        
        n_rst = 20 if N <= 6 else 12
        best_a, best_inrad, best_gnorm = adversarial_search(
            N, n_restarts=n_rst, verbose=True
        )
        
        elapsed = time.time() - t0
        
        if best_a is not None:
            inrad_full, center = full_inradius(best_a)
            is_u, mfp = verify_univalence_strict(best_a, n_grid=200)
            
            coeff_str = ", ".join(f"a{k+2}={c:.4f}" for k, c in enumerate(best_a[:5]))
            print(f"\n  BEST N={N}: inrad={inrad_full:.10f} (full), "
                  f"||G2||={best_gnorm:.6f}, univ={is_u}")
            print(f"  Coefficients: {coeff_str}")
            print(f"  Time: {elapsed:.1f}s")
            
            result = {
                "N": N,
                "inradius_fast": float(best_inrad),
                "inradius_full": float(inrad_full),
                "grunsky_norm": float(best_gnorm),
                "is_univalent": bool(is_u),
                "min_abs_fprime": float(mfp),
                "coefficients_real": [float(c.real) for c in best_a],
                "coefficients_imag": [float(c.imag) for c in best_a],
                "best_center": [float(center.real), float(center.imag)],
                "time_seconds": elapsed
            }
            all_results.append(result)
            
            if is_u and best_gnorm <= 1.02:
                log_bound(float(inrad_full), "upper",
                          f"grunsky_adversarial_N{N}",
                          "results/phase3/grunsky_extremal_search.py",
                          f"Adversarial search N={N}, gnorm={best_gnorm:.6f}, "
                          f"univ={is_u}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"{'N':>5} {'inrad(full)':>12} {'inrad(0)':>12} {'||G2||':>10} {'univ':>6} {'time':>8}")
    print("-" * 60)
    for r in all_results:
        print(f"{r['N']:>5} {r['inradius_full']:>12.8f} {r['inradius_fast']:>12.8f} "
              f"{r['grunsky_norm']:>10.6f} {'Y' if r['is_univalent'] else 'N':>6} "
              f"{r['time_seconds']:>7.1f}s")
    
    if all_results:
        valid = [r for r in all_results if r['is_univalent'] and r['grunsky_norm'] <= 1.02]
        if valid:
            best = min(valid, key=lambda r: r['inradius_full'])
            print(f"\nBest valid: N={best['N']}, B_u <= {best['inradius_full']:.10f}")
            if best['inradius_full'] < 0.6564:
                print("** IMPROVES Carroll-OC upper bound 0.6564! **")
            if best['inradius_full'] < 0.5708858:
                print("** WARNING: Below Skinner's lower bound! Verify carefully. **")
        else:
            print("\nNo valid univalent results found.")
    
    with open("results/phase3/grunsky_search_results.json", "w") as f:
        json.dump({"method": "grunsky_adversarial_search",
                    "results": all_results,
                    "timestamp": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    
    print(f"\nSaved to results/phase3/grunsky_search_results.json")
