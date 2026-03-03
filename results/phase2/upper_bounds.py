"""
Upper bounds on the univalent Bloch constant B_u.

Constructs explicit univalent functions f with f'(0)=1 designed to minimize B_f
(the inradius of the image domain f(D)). Any B_f < 1 is nontrivial; the
Carroll-Ortega-Cerda (2009) bound is B_u <= 0.6564 via slit disk constructions.

Four candidate families:
  1. Slit mappings:        f(z) = z + c*z^n (n-fold symmetric indentation)
  2. Spiral-like mappings: f(z) = z * exp(c*z^n/n), f'(0)=1
  3. Close-to-convex:      f'(z) = (1-z^n)^s, Taylor series evaluation
  4. Prescribed boundary:  truncated series with coefficients minimizing inradius

Univalence verification:
  - Starlike sufficient condition: sum_{k>=2} k|a_k| <= 1
  - f'(z) != 0 on D (sample |f'| on a grid)
  - Argument principle: winding number of f(e^{it}) around test points
"""

import numpy as np
from scipy.optimize import minimize
from scipy.special import comb
from scipy.spatial import cKDTree
import json
import os
import math
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

np.random.seed(42)

# =============================================================================
# Fast boundary sampling and inradius computation using KD-trees
# =============================================================================

def sample_boundary(f, N=4000):
    """Sample boundary of f(D) using r close to 1."""
    radii = [1.0 - 1e-4, 1.0 - 1e-5, 1.0 - 1e-6]
    all_pts = []
    n_per = N // len(radii)
    for r in radii:
        theta = np.linspace(0, 2 * np.pi, n_per, endpoint=False)
        z = r * np.exp(1j * theta)
        pts = f(z)
        mask = np.isfinite(pts) & (np.abs(pts) < 1e8)
        all_pts.append(pts[mask])
    return np.concatenate(all_pts) if all_pts else np.array([], dtype=complex)


def compute_inradius(f, N_bnd=4000, N_grid=20):
    """
    Compute B_f = inradius of f(D) using KD-tree for fast nearest-boundary queries.
    """
    bnd = sample_boundary(f, N=N_bnd)
    if len(bnd) < 50:
        return float('inf'), 0.0
    if np.max(np.abs(bnd)) > 1e6:
        return float('inf'), 0.0

    # Build KD-tree from boundary points (in R^2)
    bnd_xy = np.column_stack([bnd.real, bnd.imag])
    tree = cKDTree(bnd_xy)

    # Generate interior candidate centers: f(grid points in D)
    rr = np.linspace(0, 0.97, N_grid)
    aa = np.linspace(0, 2 * np.pi, N_grid, endpoint=False)
    R, A = np.meshgrid(rr, aa)
    z_grid = R.ravel() * np.exp(1j * A.ravel())
    z_grid = np.append(z_grid, 0.0 + 0j)
    w_grid = f(z_grid)
    mask = np.isfinite(w_grid)
    w_grid = w_grid[mask]

    # Query all at once
    w_xy = np.column_stack([w_grid.real, w_grid.imag])
    dists, _ = tree.query(w_xy)
    best_idx = np.argmax(dists)
    best_d = dists[best_idx]
    best_w = w_grid[best_idx]

    # Refine with Nelder-Mead
    def neg_inrad(xy):
        d, _ = tree.query([xy[0], xy[1]])
        return -d

    res = minimize(neg_inrad, [best_w.real, best_w.imag], method='Nelder-Mead',
                   options={'xatol': 1e-12, 'fatol': 1e-12, 'maxiter': 3000})
    return -res.fun, res.x[0] + 1j * res.x[1]


def compute_inradius_fast(f, N_bnd=3000, N_grid=15):
    """Faster version with lower resolution for coarse search."""
    bnd = sample_boundary(f, N=N_bnd)
    if len(bnd) < 50:
        return float('inf')
    if np.max(np.abs(bnd)) > 1e6:
        return float('inf')

    bnd_xy = np.column_stack([bnd.real, bnd.imag])
    tree = cKDTree(bnd_xy)

    rr = np.linspace(0, 0.95, N_grid)
    aa = np.linspace(0, 2 * np.pi, N_grid, endpoint=False)
    R, A = np.meshgrid(rr, aa)
    z_grid = R.ravel() * np.exp(1j * A.ravel())
    z_grid = np.append(z_grid, 0.0 + 0j)
    w_grid = f(z_grid)
    mask = np.isfinite(w_grid)
    w_grid = w_grid[mask]
    if len(w_grid) == 0:
        return float('inf')

    w_xy = np.column_stack([w_grid.real, w_grid.imag])
    dists, _ = tree.query(w_xy)
    best_idx = np.argmax(dists)
    best_d = dists[best_idx]
    best_w = w_grid[best_idx]

    # Quick refine
    def neg_inrad(xy):
        d, _ = tree.query([xy[0], xy[1]])
        return -d

    res = minimize(neg_inrad, [best_w.real, best_w.imag], method='Nelder-Mead',
                   options={'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 1000})
    return -res.fun


# =============================================================================
# Univalence verification
# =============================================================================

def check_starlike_condition(coeffs):
    """sum_{k>=2} k|a_k| <= 1 guarantees univalence. coeffs = [a_2, a_3, ...]."""
    total = sum((i + 2) * abs(a) for i, a in enumerate(coeffs))
    return total <= 1.0, total


def check_derivative_nonzero(f_prime, N=600):
    """Check f'(z) != 0 on D by dense sampling on circles and finding minimum."""
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    min_abs = float('inf')
    # Use dense radial sampling to not miss critical points
    for r in np.linspace(0.0, 0.999, 50):
        z = r * np.exp(1j * theta) if r > 0 else np.array([0.0+0j])
        fp = f_prime(z)
        finite = fp[np.isfinite(fp)]
        if len(finite) > 0:
            m = np.min(np.abs(finite))
            min_abs = min(min_abs, m)
    return min_abs > 1e-6, min_abs


def check_winding_number(f, w0, N=1200, r=0.999):
    """Winding number of f(r*e^{it}) around w0."""
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    z = r * np.exp(1j * theta)
    w = f(z) - w0
    dtheta = np.diff(np.unwrap(np.angle(w)))
    return int(round(np.sum(dtheta) / (2 * np.pi)))


def verify_univalence(f, f_prime=None, coeffs=None, name=""):
    """Comprehensive univalence check."""
    result = {"name": name, "univalent": True, "checks": {}}

    if coeffs is not None:
        is_star, val = check_starlike_condition(coeffs)
        result["checks"]["starlike_condition"] = {
            "sum_k_ak": round(val, 8), "satisfied": is_star
        }

    if f_prime is not None:
        ok, min_fp = check_derivative_nonzero(f_prime)
        result["checks"]["derivative_nonzero"] = {
            "min_abs_f_prime": round(min_fp, 10), "ok": ok
        }
        if not ok:
            result["univalent"] = False

    f0 = f(np.array([0.0 + 0j]))[0]
    wn = check_winding_number(f, f0)
    result["checks"]["winding_number_f0"] = {"value": wn, "ok": wn == 1}
    if wn != 1:
        result["univalent"] = False

    # Injectivity spot check
    for r_c in [0.5, 0.9]:
        theta = np.linspace(0, 2 * np.pi, 200, endpoint=False)
        w_c = f(r_c * np.exp(1j * theta))
        mask = np.isfinite(w_c)
        w_f = w_c[mask]
        if len(w_f) > 10:
            idx = np.random.choice(len(w_f), min(80, len(w_f)), replace=False)
            w_sub = w_f[idx]
            dists = np.abs(w_sub[:, None] - w_sub[None, :])
            np.fill_diagonal(dists, np.inf)
            if np.min(dists) < 1e-12:
                result["univalent"] = False
                result["checks"]["injectivity"] = {"ok": False, "r": r_c}

    if "injectivity" not in result["checks"]:
        result["checks"]["injectivity"] = {"ok": True}

    return result


# =============================================================================
# Family 1: Slit mappings f(z) = z + c * z^n
# =============================================================================

def search_slit_mappings():
    """Search f(z)=z+c*z^n for n=2..12, c in starlike range."""
    print("\n" + "=" * 70)
    print("FAMILY 1: Slit mappings f(z) = z + c * z^n")
    print("=" * 70)

    best_Bf = float('inf')
    best_params = {}
    all_results = []

    for n in range(2, 13):
        c_max = 1.0 / n

        def make_f(c, n=n):
            return lambda z: z + c * z**n
        def make_fp(c, n=n):
            return lambda z: 1.0 + c * n * z**(n - 1)

        # Coarse search
        c_vals = np.linspace(-c_max, c_max, 21)
        c_vals = c_vals[np.abs(c_vals) > 1e-15]

        best_c = None
        best_Bf_n = float('inf')

        for c in c_vals:
            Bf = compute_inradius_fast(make_f(c))
            if np.isfinite(Bf) and Bf < best_Bf_n:
                best_Bf_n = Bf
                best_c = c

        # Refine near best
        if best_c is not None:
            c_lo = max(best_c - 0.2 / n, -c_max)
            c_hi = min(best_c + 0.2 / n, c_max)
            for c in np.linspace(c_lo, c_hi, 15):
                if abs(c) < 1e-15:
                    continue
                Bf, _ = compute_inradius(make_f(c), N_bnd=5000, N_grid=25)
                if np.isfinite(Bf) and Bf < best_Bf_n:
                    best_Bf_n = Bf
                    best_c = c

            f_b = make_f(best_c)
            fp_b = make_fp(best_c)
            coeffs = [0.0] * (n - 2) + [best_c]
            uv = verify_univalence(f_b, fp_b, coeffs, f"slit_n{n}")
            entry = {
                "n": n, "c": round(float(best_c), 10),
                "Bf": round(float(best_Bf_n), 10),
                "univalent": uv["univalent"], "checks": uv["checks"]
            }
            all_results.append(entry)
            print(f"  n={n:2d}, c={best_c:+.8f}, B_f={best_Bf_n:.8f}, univ={uv['univalent']}")

            if uv["univalent"] and best_Bf_n < best_Bf:
                best_Bf = best_Bf_n
                best_params = {"n": n, "c": float(best_c)}

    print(f"\n  >>> Best slit: n={best_params.get('n')}, "
          f"c={best_params.get('c', 0):.8f}, B_f={best_Bf:.8f}")
    return best_Bf, best_params, all_results


# =============================================================================
# Family 2: Spiral-like mappings f(z) = z * exp(c * z^n / n)
# =============================================================================

def search_spiral_mappings():
    """Search spiral-like mappings for n=2..7, c real and imaginary."""
    print("\n" + "=" * 70)
    print("FAMILY 2: Spiral-like mappings f(z) = z * exp(c * z^n / n)")
    print("=" * 70)

    best_Bf = float('inf')
    best_params = {}
    all_results = []

    for n in range(2, 8):
        def make_f(c, n=n):
            return lambda z: z * np.exp(c * z**n / n)
        def make_fp(c, n=n):
            return lambda z: np.exp(c * z**n / n) * (1 + c * z**n)

        best_c = None
        best_Bf_n = float('inf')

        # For f(z) = z*exp(c*z^n/n), f'(z)=0 when z^n = -1/c.
        # Univalence requires |-1/c| >= 1, i.e. |c| <= 1.
        # (Actually univalence needs more, but this is necessary.)

        # Real c: restrict to |c| <= 1 for necessary condition f' != 0
        for c_r in np.linspace(-1.0, 1.0, 21):
            if abs(c_r) < 1e-15:
                continue
            fp = make_fp(c_r)
            ok, _ = check_derivative_nonzero(fp, N=400)
            if not ok:
                continue
            f = make_f(c_r)
            Bf = compute_inradius_fast(f)
            if np.isfinite(Bf) and Bf < best_Bf_n:
                wn = check_winding_number(f, f(np.array([0.0+0j]))[0], N=800)
                if wn == 1:
                    best_Bf_n = Bf
                    best_c = c_r

        # Imaginary c: |c| <= 1
        for c_i in np.linspace(-1.0, 1.0, 15):
            if abs(c_i) < 1e-15:
                continue
            c = 1j * c_i
            fp = make_fp(c)
            ok, _ = check_derivative_nonzero(fp, N=400)
            if not ok:
                continue
            f = make_f(c)
            Bf = compute_inradius_fast(f)
            if np.isfinite(Bf) and Bf < best_Bf_n:
                wn = check_winding_number(f, f(np.array([0.0+0j]))[0], N=800)
                if wn == 1:
                    best_Bf_n = Bf
                    best_c = c

        # Refine near best (real only)
        if best_c is not None and np.isreal(best_c):
            cc = float(np.real(best_c))
            c_lo = max(cc - 0.1, -1.0)
            c_hi = min(cc + 0.1, 1.0)
            for c in np.linspace(c_lo, c_hi, 15):
                if abs(c) < 1e-15:
                    continue
                fp = make_fp(c)
                ok, _ = check_derivative_nonzero(fp, N=400)
                if not ok:
                    continue
                f = make_f(c)
                Bf, _ = compute_inradius(f, N_bnd=5000, N_grid=25)
                if np.isfinite(Bf) and Bf < best_Bf_n:
                    wn = check_winding_number(f, f(np.array([0.0+0j]))[0], N=800)
                    if wn == 1:
                        best_Bf_n = Bf
                        best_c = c

        if best_c is not None:
            f_b = make_f(best_c)
            fp_b = make_fp(best_c)
            # Build coefficients
            max_idx = 50
            coeffs = [0.0] * max_idx
            for k in range(1, 8):
                idx = k * n + 1 - 2
                if 0 <= idx < max_idx:
                    coeffs[idx] = (best_c / n)**k / math.factorial(k)
            uv = verify_univalence(f_b, fp_b, coeffs, f"spiral_n{n}")
            entry = {
                "n": n,
                "c_real": round(float(np.real(best_c)), 10),
                "c_imag": round(float(np.imag(best_c)), 10),
                "Bf": round(float(best_Bf_n), 10),
                "univalent": uv["univalent"]
            }
            all_results.append(entry)
            print(f"  n={n:2d}, c={best_c}, B_f={best_Bf_n:.8f}, univ={uv['univalent']}")

            if uv["univalent"] and best_Bf_n < best_Bf:
                best_Bf = best_Bf_n
                best_params = {"n": n,
                               "c_real": float(np.real(best_c)),
                               "c_imag": float(np.imag(best_c))}

    print(f"\n  >>> Best spiral: B_f={best_Bf:.8f}")
    return best_Bf, best_params, all_results


# =============================================================================
# Family 3: Close-to-convex  f'(z) = (1-z^n)^s  via Taylor series
# =============================================================================

def make_ctc_power(s, n, K=40):
    """
    f'(z) = (1-z^n)^s.  f(z) = z + sum_{k>=1} binom(s,k)(-1)^k/(nk+1) z^{nk+1}.
    Evaluated via truncated Taylor series (vectorized, fast).
    """
    # Precompute nonzero coefficients: a_{nk+1} for k=1..K
    powers = []
    coeff_vals = []
    for k in range(1, K + 1):
        j = n * k + 1
        if j > 300:
            break
        val = float(comb(s, k, exact=False)) * (-1)**k / (n * k + 1)
        if abs(val) < 1e-30:
            continue
        powers.append(j)
        coeff_vals.append(val)

    def f(z):
        result = z.copy().astype(complex)
        for j, a in zip(powers, coeff_vals):
            result += a * z**j
        return result

    fp = lambda z: (1.0 - z**n)**s

    # Coefficients for starlike check
    max_p = max(powers) if powers else 2
    coeffs = [0.0] * (max_p - 1)
    for j, a in zip(powers, coeff_vals):
        coeffs[j - 2] = a

    return f, fp, coeffs


def search_close_to_convex():
    """Search close-to-convex f'(z) = (1-z^n)^s for n=2..7, s>0."""
    print("\n" + "=" * 70)
    print("FAMILY 3: Close-to-convex f'(z) = (1 - z^n)^s")
    print("=" * 70)

    best_Bf = float('inf')
    best_params = {}
    all_results = []

    for n in range(2, 8):
        s_max = 2.0 / n + 0.5
        s_values = np.linspace(0.1, s_max, 15)

        best_s = None
        best_Bf_n = float('inf')

        for s in s_values:
            f, fp, coeffs = make_ctc_power(s, n)
            try:
                wn = check_winding_number(f, f(np.array([0.0+0j]))[0], N=800)
                if wn != 1:
                    continue
                Bf = compute_inradius_fast(f)
            except Exception:
                continue
            if np.isfinite(Bf) and Bf < best_Bf_n:
                best_Bf_n = Bf
                best_s = s

        # Refine
        if best_s is not None:
            s_lo = max(0.05, best_s - 0.1)
            s_hi = min(s_max + 0.3, best_s + 0.1)
            for s in np.linspace(s_lo, s_hi, 11):
                f, fp, coeffs = make_ctc_power(s, n)
                try:
                    wn = check_winding_number(f, f(np.array([0.0+0j]))[0], N=800)
                    if wn != 1:
                        continue
                    Bf, _ = compute_inradius(f, N_bnd=5000, N_grid=25)
                except Exception:
                    continue
                if np.isfinite(Bf) and Bf < best_Bf_n:
                    best_Bf_n = Bf
                    best_s = s

            f_b, fp_b, co_b = make_ctc_power(best_s, n)
            uv = verify_univalence(f_b, fp_b, co_b, f"ctc_n{n}")
            entry = {
                "n": n, "s": round(float(best_s), 10),
                "Bf": round(float(best_Bf_n), 10),
                "univalent": uv["univalent"]
            }
            all_results.append(entry)
            print(f"  n={n:2d}, s={best_s:.6f}, B_f={best_Bf_n:.8f}, univ={uv['univalent']}")

            if uv["univalent"] and best_Bf_n < best_Bf:
                best_Bf = best_Bf_n
                best_params = {"n": n, "s": float(best_s)}

    print(f"\n  >>> Best close-to-convex: B_f={best_Bf:.8f}")
    return best_Bf, best_params, all_results


# =============================================================================
# Family 4: Truncated series with optimized coefficients
# =============================================================================

def search_truncated_series():
    """Optimize truncated Taylor series to minimize inradius under starlike constraint."""
    print("\n" + "=" * 70)
    print("FAMILY 4: Truncated series with optimized coefficients")
    print("=" * 70)

    best_Bf = float('inf')
    best_params = {}
    all_results = []

    for N_terms in [2, 3, 5]:
        print(f"\n  Optimizing {N_terms} coefficients (a_2 ... a_{N_terms+1})...")

        def make_f_from_x(x, Nt=N_terms):
            coeffs = [x[2*j] + 1j * x[2*j+1] for j in range(Nt)]
            total = sum((k+2)*abs(coeffs[k]) for k in range(len(coeffs)))
            if total > 1.0:
                sc = 0.99 / total
                coeffs = [c * sc for c in coeffs]
            def f(z):
                result = z.copy().astype(complex)
                zk = z * z
                for a_k in coeffs:
                    result += a_k * zk
                    zk = zk * z
                return result
            return f, coeffs

        def objective(x, Nt=N_terms):
            f, _ = make_f_from_x(x, Nt)
            try:
                Bf = compute_inradius_fast(f, N_bnd=1500, N_grid=10)
                return Bf if np.isfinite(Bf) else 10.0
            except Exception:
                return 10.0

        best_for_N = float('inf')
        best_x = None

        # Random starts (reduced)
        for trial in range(8):
            x0 = np.random.randn(2 * N_terms) * 0.1
            try:
                res = minimize(objective, x0, method='Nelder-Mead',
                               options={'maxiter': 120, 'xatol': 1e-3, 'fatol': 1e-3})
                if res.fun < best_for_N:
                    best_for_N = res.fun
                    best_x = res.x.copy()
            except Exception:
                continue

        # Structured starts: single nonzero coefficient at boundary
        for ns in range(2, N_terms + 2):
            idx = ns - 2
            if idx >= N_terms:
                continue
            c_max = 1.0 / ns
            for cv in [c_max * 0.99, -c_max * 0.99]:
                x0 = np.zeros(2 * N_terms)
                x0[2 * idx] = cv
                try:
                    res = minimize(objective, x0, method='Nelder-Mead',
                                   options={'maxiter': 120, 'xatol': 1e-3, 'fatol': 1e-3})
                    if res.fun < best_for_N:
                        best_for_N = res.fun
                        best_x = res.x.copy()
                except Exception:
                    continue

        if best_x is not None:
            f_b, coeffs_c = make_f_from_x(best_x, N_terms)
            Bf_final, _ = compute_inradius(f_b, N_bnd=5000, N_grid=25)
            best_for_N = Bf_final

            def make_fp(cc):
                def fp(z):
                    result = np.ones_like(z, dtype=complex)
                    zk = z.copy()
                    for i, a in enumerate(cc):
                        result += (i+2) * a * zk
                        zk = zk * z
                    return result
                return fp

            uv = verify_univalence(f_b, make_fp(coeffs_c), coeffs_c, f"trunc_{N_terms}")
            is_star, star_val = check_starlike_condition(coeffs_c)

            entry = {
                "N_terms": N_terms,
                "coeffs_real": [round(float(c.real), 10) for c in coeffs_c],
                "coeffs_imag": [round(float(c.imag), 10) for c in coeffs_c],
                "starlike_sum": round(float(star_val), 10),
                "Bf": round(float(best_for_N), 10),
                "univalent": uv["univalent"]
            }
            all_results.append(entry)
            print(f"    N={N_terms}: B_f={best_for_N:.8f}, star_sum={star_val:.6f}, "
                  f"univ={uv['univalent']}")

            if uv["univalent"] and np.isfinite(best_for_N) and best_for_N < best_Bf:
                best_Bf = best_for_N
                best_params = {
                    "N_terms": N_terms,
                    "coeffs_real": [float(c.real) for c in coeffs_c],
                    "coeffs_imag": [float(c.imag) for c in coeffs_c]
                }

    print(f"\n  >>> Best truncated series: B_f={best_Bf:.8f}")
    return best_Bf, best_params, all_results


# =============================================================================
# Bonus: Multi-slit constructions (Carroll-Ortega-Cerda style)
# =============================================================================

def search_multi_slit():
    """Search multi-slit constructions with mixed orders."""
    print("\n" + "=" * 70)
    print("BONUS: Multi-slit constructions (Carroll-Ortega-Cerda style)")
    print("=" * 70)

    best_Bf = float('inf')
    best_params = {}
    all_results = []

    combos = [
        [2, 3], [2, 4], [3, 4], [3, 5], [3, 6],
        [2, 3, 4], [2, 4, 6], [3, 5, 7],
    ]

    for n_list in combos:
        N_c = len(n_list)

        def make_f_nl(x, nl=n_list):
            c_list = [x[2*j] + 1j * x[2*j+1] for j in range(len(nl))]
            total = sum(nn * abs(cc) for nn, cc in zip(nl, c_list))
            if total > 1.0:
                sc = 0.99 / total
                c_list = [cc * sc for cc in c_list]
            def f(z, cl=c_list, nll=nl):
                result = z.copy().astype(complex)
                for c, nn in zip(cl, nll):
                    result += c * z**nn
                return result
            return f, c_list

        def obj(x, nl=n_list):
            f, _ = make_f_nl(x, nl)
            try:
                Bf = compute_inradius_fast(f, N_bnd=1500, N_grid=10)
                return Bf if np.isfinite(Bf) else 10.0
            except Exception:
                return 10.0

        best_combo = float('inf')
        best_x_c = None

        for trial in range(6):
            x0 = np.random.randn(2 * N_c) * 0.15
            try:
                res = minimize(obj, x0, method='Nelder-Mead',
                               options={'maxiter': 120, 'xatol': 1e-3, 'fatol': 1e-3})
                if res.fun < best_combo:
                    best_combo = res.fun
                    best_x_c = res.x.copy()
            except Exception:
                continue

        if best_x_c is not None:
            f_b, c_list = make_f_nl(best_x_c, n_list)
            Bf_final, _ = compute_inradius(f_b, N_bnd=5000, N_grid=25)

            max_n = max(n_list)
            coeffs = [0.0] * (max_n - 1)
            for c, nn in zip(c_list, n_list):
                coeffs[nn - 2] = c
            def make_fp_ml(cl, nl):
                def fp(z):
                    result = np.ones_like(z, dtype=complex)
                    for c, nn in zip(cl, nl):
                        result += c * nn * z**(nn-1)
                    return result
                return fp

            uv = verify_univalence(f_b, make_fp_ml(c_list, n_list), coeffs,
                                   f"multi_{n_list}")
            entry = {
                "n_list": n_list,
                "c_real": [round(float(c.real), 10) for c in c_list],
                "c_imag": [round(float(c.imag), 10) for c in c_list],
                "Bf": round(float(Bf_final), 10),
                "univalent": uv["univalent"]
            }
            all_results.append(entry)
            ns = "+".join(str(nn) for nn in n_list)
            print(f"  n=[{ns}]: B_f={Bf_final:.8f}, univ={uv['univalent']}")

            if uv["univalent"] and np.isfinite(Bf_final) and Bf_final < best_Bf:
                best_Bf = Bf_final
                best_params = {
                    "n_list": n_list,
                    "c_real": [float(c.real) for c in c_list],
                    "c_imag": [float(c.imag) for c in c_list]
                }

    print(f"\n  >>> Best multi-slit: B_f={best_Bf:.8f}")
    return best_Bf, best_params, all_results


# =============================================================================
# Reference: strip mapping
# =============================================================================

def compute_strip_Bf():
    """arctanh(z): D -> strip |Im(w)| < pi/4.  Inradius = pi/4."""
    print("\n" + "=" * 70)
    print("REFERENCE: Strip mapping f(z) = arctanh(z)")
    print("=" * 70)

    Bf_analytical = np.pi / 4
    f = lambda z: np.arctanh(z)

    bnd = sample_boundary(f, N=4000)
    mask = np.abs(bnd.real) < 3.0
    bnd_near = bnd[mask]
    if len(bnd_near) > 50:
        bnd_xy = np.column_stack([bnd_near.real, bnd_near.imag])
        tree = cKDTree(bnd_xy)
        d0, _ = tree.query([0.0, 0.0])
        print(f"  Analytical B_f = pi/4 = {Bf_analytical:.10f}")
        print(f"  Numerical d(0, boundary) = {d0:.10f}")
    else:
        print(f"  Analytical B_f = pi/4 = {Bf_analytical:.10f}")

    return Bf_analytical


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 70)
    print("UPPER BOUNDS ON THE UNIVALENT BLOCH CONSTANT B_u")
    print("=" * 70)
    print("Goal: Find univalent f with f'(0)=1 minimizing B_f = inradius(f(D))")
    print("Any B_f < 1 is nontrivial.")
    print("Carroll-Ortega-Cerda (2009): B_u <= 0.6564\n")

    results = {
        "description": "Upper bounds on the univalent Bloch constant B_u",
        "method": "Numerical search over parametric families of univalent functions",
        "reference_bound": 0.6564,
        "reference": "Carroll-Ortega-Cerda (2009)",
        "families": {}
    }

    strip_Bf = compute_strip_Bf()
    results["families"]["strip_mapping"] = {
        "description": "f(z) = arctanh(z), strip |Im(w)| < pi/4",
        "Bf": round(strip_Bf, 10), "analytical": True
    }

    Bf1, p1, d1 = search_slit_mappings()
    results["families"]["slit_mappings"] = {
        "description": "f(z) = z + c*z^n",
        "best_Bf": round(Bf1, 10) if np.isfinite(Bf1) else None,
        "best_params": p1, "all_results": d1
    }

    Bf2, p2, d2 = search_spiral_mappings()
    results["families"]["spiral_mappings"] = {
        "description": "f(z) = z*exp(c*z^n/n)",
        "best_Bf": round(Bf2, 10) if np.isfinite(Bf2) else None,
        "best_params": p2, "all_results": d2
    }

    Bf3, p3, d3 = search_close_to_convex()
    results["families"]["close_to_convex"] = {
        "description": "f'(z) = (1-z^n)^s",
        "best_Bf": round(Bf3, 10) if np.isfinite(Bf3) else None,
        "best_params": p3, "all_results": d3
    }

    Bf4, p4, d4 = search_truncated_series()
    results["families"]["truncated_series"] = {
        "description": "f(z) = z + sum a_k z^k, starlike constraint",
        "best_Bf": round(Bf4, 10) if np.isfinite(Bf4) else None,
        "best_params": p4, "all_results": d4
    }

    Bf5, p5, d5 = search_multi_slit()
    results["families"]["multi_slit"] = {
        "description": "f(z) = z + sum c_j z^{n_j}, multi-slit",
        "best_Bf": round(Bf5, 10) if np.isfinite(Bf5) else None,
        "best_params": p5, "all_results": d5
    }

    # Overall ranking
    cands = [
        ("strip_mapping", strip_Bf),
        ("slit_mappings", Bf1), ("spiral_mappings", Bf2),
        ("close_to_convex", Bf3), ("truncated_series", Bf4),
        ("multi_slit", Bf5),
    ]
    cands = [(n, b) for n, b in cands if np.isfinite(b)]
    cands.sort(key=lambda x: x[1])

    bf_name, bf_val = cands[0] if cands else ("none", float('inf'))

    results["overall_best"] = {
        "family": bf_name,
        "Bf": round(bf_val, 10) if np.isfinite(bf_val) else None,
        "is_nontrivial": bf_val < 1.0,
        "beats_reference": bf_val < 0.6564,
        "ranking": [{"family": n, "Bf": round(b, 10)} for n, b in cands]
    }

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for n, b in cands:
        marker = " ***" if n == bf_name else ""
        print(f"  {n:25s}: B_f = {b:.8f}{marker}")
    print(f"\n  Best upper bound: B_f = {bf_val:.8f} ({bf_name})")
    print(f"  Nontrivial (< 1.0): {bf_val < 1.0}")
    print(f"  vs Carroll-OC (0.6564): {'beats' if bf_val < 0.6564 else 'does not beat'}")

    # Write JSON
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "upper_bound_results.json")

    def clean(obj):
        if isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, complex):
            return {"real": round(obj.real, 10), "imag": round(obj.imag, 10)}
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif obj is None or isinstance(obj, (int, float, str, bool)):
            return obj
        else:
            return str(obj)

    with open(outpath, 'w') as fp:
        json.dump(clean(results), fp, indent=2)
    print(f"\n  Results written to {outpath}")

    return results


if __name__ == '__main__':
    main()
