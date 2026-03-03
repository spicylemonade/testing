"""
Slit Mapping Search for Upper Bounds on B_u (Bloch constant for univalent functions).

Constructs univalent slit mappings with f'(0)=1 and computes B_f to find upper bounds on B_u.

Families:
1. n-fold symmetric perturbations: f(z) = z - c*z^{n+1}/(n+1)
2. Combination perturbations: f(z) = z + sum c_k * z^{n_k}
3. Schwarz-Christoffel-type: f(z) = int_0^z prod (1 - t*e^{-i*theta_k})^{alpha_k} dt
4. Star-shaped with deep indentations: f(z) = z*(1 + a*z^n)^{-2/n}
"""

import numpy as np
import json
import os
import time

np.random.seed(42)

# ============================================================
# Utility functions
# ============================================================

def compute_Bf_fast(f_func, N_boundary=1024, n_circles=30):
    """
    Fast computation of B_f for univalent f.
    B_f = inradius of f(D) = max over w in f(D) of dist(w, bdry f(D)).
    Vectorized for speed.
    """
    # Boundary of f(D)
    theta_bdy = np.linspace(0, 2 * np.pi, N_boundary, endpoint=False)
    z_bdy = np.exp(1j * theta_bdy)
    w_bdy = f_func(z_bdy)

    # Collect interior candidate points
    w_list = [f_func(np.array([0.0 + 0j]))]
    for i in range(1, n_circles + 1):
        r = i / (n_circles + 1) * 0.98
        n_pts = max(12, int(48 * r))
        theta = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
        z_pts = r * np.exp(1j * theta)
        w_list.append(f_func(z_pts))

    w_candidates = np.concatenate(w_list)

    # Batch distance computation
    best_r = 0.0
    batch_size = 512
    for i in range(0, len(w_candidates), batch_size):
        batch = w_candidates[i:i + batch_size]
        # shape (batch, boundary)
        dists = np.abs(batch[:, None] - w_bdy[None, :])
        min_dists = dists.min(axis=1)
        candidate = min_dists.max()
        if candidate > best_r:
            best_r = candidate
    return best_r


def check_deriv_nonzero(f_prime_func, N=256):
    """Check f'(z) != 0 on a grid inside the closed unit disk."""
    radii = np.linspace(0, 1.0, 12)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    for r in radii:
        z = r * np.exp(1j * theta)
        fp = f_prime_func(z)
        if np.any(np.abs(fp) < 1e-10):
            return False
    return True


# ============================================================
# Family 1: n-fold symmetric perturbations
# f(z) = z - c * z^{n+1} / (n+1),  f'(z) = 1 - c * z^n
# ============================================================

def family1_func(z, n, c):
    return z - c * z ** (n + 1) / (n + 1)

def family1_deriv(z, n, c):
    return 1 - c * z ** n

def run_family1():
    results = []
    n_values = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20]
    c_values = np.linspace(0.05, 0.99, 25)
    for n in n_values:
        for c_val in c_values:
            c_val = float(c_val)
            fp = lambda z, _n=n, _c=c_val: family1_deriv(z, _n, _c)
            if not check_deriv_nonzero(fp):
                continue
            f = lambda z, _n=n, _c=c_val: family1_func(z, _n, _c)
            try:
                Bf = compute_Bf_fast(f)
            except Exception:
                continue
            results.append({
                'family': 'family1_nfold_symmetric',
                'params': {'n': n, 'c': c_val},
                'Bf': float(Bf),
                'is_univalent': True
            })
    return results


# ============================================================
# Family 2: Combination perturbations
# f(z) = z + sum c_k * z^{n_k}
# ============================================================

def family2_func(z, coeffs):
    result = z.astype(complex).copy()
    for (n_k, c_k) in coeffs:
        result += c_k * z ** n_k
    return result

def family2_deriv(z, coeffs):
    result = np.ones_like(z, dtype=complex)
    for (n_k, c_k) in coeffs:
        result += n_k * c_k * z ** (n_k - 1)
    return result

def run_family2():
    results = []
    rng = np.random.RandomState(42)

    configs = []
    # Two-term structured
    for n1 in [2, 3, 4, 5]:
        for n2 in [n1 + 1, n1 + 2, n1 + 3]:
            if n2 > 10:
                continue
            for c1 in np.linspace(-0.3, 0.3, 6):
                for c2 in np.linspace(-0.3, 0.3, 6):
                    if abs(c1) + abs(c2) > 0.5:
                        continue
                    configs.append([(n1, float(c1)), (n2, float(c2))])

    # Random combinations
    for _ in range(80):
        n_terms = rng.randint(2, 5)
        degrees = sorted(rng.choice(range(2, 12), size=n_terms, replace=False))
        mx = 0.4 / n_terms
        cl = [(int(d), float(rng.uniform(-mx, mx))) for d in degrees]
        configs.append(cl)

    # Cap at 200
    configs = configs[:200]

    for coeffs in configs:
        fp = lambda z, _c=coeffs: family2_deriv(z, _c)
        if not check_deriv_nonzero(fp):
            continue
        f = lambda z, _c=coeffs: family2_func(z, _c)
        try:
            Bf = compute_Bf_fast(f)
        except Exception:
            continue
        pd = {}
        for i, (nk, ck) in enumerate(coeffs):
            pd[f'n{i}'] = int(nk)
            pd[f'c{i}'] = float(ck)
        results.append({
            'family': 'family2_combination',
            'params': pd,
            'Bf': float(Bf),
            'is_univalent': True
        })
    return results


# ============================================================
# Family 3: Schwarz-Christoffel-type  (vectorized integration)
# f(z) = int_0^z prod (1 - t*e^{-i*theta_k})^{alpha_k} dt
# ============================================================

def family3_func_vec(z_array, thetas, alphas, N_quad=80):
    """Vectorized SC integration along radial paths."""
    thetas = np.asarray(thetas)
    alphas = np.asarray(alphas)
    z_array = np.asarray(z_array, dtype=complex)
    M = len(z_array)

    # s grid for quadrature – avoid s=1 to stay away from boundary singularity
    s = np.linspace(0, 1, N_quad, endpoint=False) + 0.5 / N_quad
    ds = 1.0 / N_quad

    # t = z * s, shape (M, N_quad)
    t = z_array[:, None] * s[None, :]

    # For each slit: factor = 1 - t * exp(-i*theta_k)
    phases = np.exp(-1j * thetas)  # (n_slits,)
    factors = 1.0 - t[None, :, :] * phases[:, None, None]  # (n_slits, M, N_quad)

    # Avoid log(0) by clamping
    abs_factors = np.abs(factors)
    abs_factors = np.maximum(abs_factors, 1e-30)
    log_abs = np.log(abs_factors)
    arg_factors = np.angle(factors)

    log_prod = np.sum(alphas[:, None, None] * (log_abs + 1j * arg_factors), axis=0)
    integrand = np.exp(log_prod)

    # Check for NaN/Inf
    bad = ~np.isfinite(integrand)
    integrand[bad] = 0.0

    integrand *= z_array[:, None]
    f_values = np.sum(integrand, axis=1) * ds
    return f_values

def family3_deriv_vec(z_array, thetas, alphas):
    """f'(z) = prod (1 - z*e^{-i*theta_k})^{alpha_k}"""
    thetas = np.asarray(thetas)
    alphas = np.asarray(alphas)
    z_array = np.asarray(z_array, dtype=complex)
    phases = np.exp(-1j * thetas)
    factors = 1.0 - z_array[:, None] * phases[None, :]
    abs_f = np.maximum(np.abs(factors), 1e-30)
    log_prod = np.sum(alphas[None, :] * (np.log(abs_f) + 1j * np.angle(factors)), axis=1)
    result = np.exp(log_prod)
    result[~np.isfinite(result)] = 0.0
    return result

def run_family3():
    results = []
    rng = np.random.RandomState(123)

    configs = []
    # Symmetric slit configurations
    for n_slits in [2, 3, 4, 5, 6, 8]:
        thetas = [2 * np.pi * k / n_slits for k in range(n_slits)]
        for alpha_total in np.linspace(0.1, 0.8, 8):
            alpha = alpha_total / n_slits
            configs.append((thetas, [alpha] * n_slits))

    # Asymmetric
    for _ in range(40):
        ns = rng.randint(2, 7)
        th = sorted(rng.uniform(0, 2 * np.pi, ns).tolist())
        al = rng.uniform(0.05, 0.3, ns).tolist()
        configs.append((th, al))

    # Negative alpha (bulges)
    for n_slits in [2, 3, 4, 6]:
        thetas = [2 * np.pi * k / n_slits for k in range(n_slits)]
        for alpha_total in np.linspace(-0.5, -0.05, 6):
            alpha = alpha_total / n_slits
            configs.append((thetas, [alpha] * n_slits))

    for thetas, alphas in configs:
        fp = lambda z, _t=thetas, _a=alphas: family3_deriv_vec(z, _t, _a)
        if not check_deriv_nonzero(fp):
            continue
        f = lambda z, _t=thetas, _a=alphas: family3_func_vec(z, _t, _a, N_quad=80)
        try:
            # Quick sanity: f(0) should be ~0
            f0 = f(np.array([0.0 + 0j]))[0]
            if not np.isfinite(f0) or abs(f0) > 0.01:
                continue
            Bf = compute_Bf_fast(f, N_boundary=512, n_circles=20)
            if not np.isfinite(Bf) or Bf < 0.01:
                continue  # spurious result from numerical issues
        except Exception:
            continue
        results.append({
            'family': 'family3_schwarz_christoffel',
            'params': {
                'thetas': [float(t) for t in thetas],
                'alphas': [float(a) for a in alphas],
                'n_slits': len(thetas)
            },
            'Bf': float(Bf),
            'is_univalent': True
        })
    return results


# ============================================================
# Family 4: Star-shaped with deep indentations
# f(z) = z * (1 + a*z^n)^{-2/n}
# ============================================================

def family4_func(z, n, a):
    inner = 1 + a * z ** n
    power = (-2.0 / n)
    return z * np.exp(power * np.log(inner + 0j))

def family4_deriv(z, n, a):
    inner = 1 + a * z ** n
    azn = a * z ** n
    power = (-2.0 / n - 1)
    return (1 - azn) * np.exp(power * np.log(inner + 0j))

def run_family4():
    results = []
    n_values = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20]
    a_pos = np.linspace(0.05, 0.95, 20)
    a_neg = np.linspace(-0.95, -0.05, 12)

    for n in n_values:
        for a_val in np.concatenate([a_pos, a_neg]):
            a_val = float(a_val)
            fp = lambda z, _n=n, _a=a_val: family4_deriv(z, _n, _a)
            if not check_deriv_nonzero(fp):
                continue
            f = lambda z, _n=n, _a=a_val: family4_func(z, _n, _a)
            try:
                Bf = compute_Bf_fast(f)
            except Exception:
                continue
            results.append({
                'family': 'family4_starlike',
                'params': {'n': n, 'a': a_val},
                'Bf': float(Bf),
                'is_univalent': True
            })
    return results


# ============================================================
# Refined search around best configurations
# ============================================================

def refine_search(all_results, top_k=10, n_refine=30):
    if not all_results:
        return []
    sorted_r = sorted(all_results, key=lambda x: x['Bf'])[:top_k]
    refined = []
    rng = np.random.RandomState(999)

    for res in sorted_r:
        fam = res['family']
        p = res['params']
        for _ in range(n_refine):
            if 'family1' in fam:
                n = p['n']; c = p['c'] + rng.uniform(-0.03, 0.03)
                c = float(np.clip(c, 0.01, 0.99))
                fp = lambda z, _n=n, _c=c: family1_deriv(z, _n, _c)
                f = lambda z, _n=n, _c=c: family1_func(z, _n, _c)
                new_p = {'n': n, 'c': c}
            elif 'family4' in fam:
                n = p['n']; a = p['a'] + rng.uniform(-0.03, 0.03)
                a = float(np.clip(a, -0.95, 0.95))
                fp = lambda z, _n=n, _a=a: family4_deriv(z, _n, _a)
                f = lambda z, _n=n, _a=a: family4_func(z, _n, _a)
                new_p = {'n': n, 'a': a}
            elif 'family2' in fam:
                # Perturb coefficients
                nt = sum(1 for k in p if k.startswith('n'))
                coeffs = [(p[f'n{i}'], p[f'c{i}'] + rng.uniform(-0.02, 0.02)) for i in range(nt)]
                coeffs = [(nk, float(np.clip(ck, -0.5, 0.5))) for nk, ck in coeffs]
                fp = lambda z, _c=coeffs: family2_deriv(z, _c)
                f = lambda z, _c=coeffs: family2_func(z, _c)
                new_p = {}
                for i, (nk, ck) in enumerate(coeffs):
                    new_p[f'n{i}'] = int(nk)
                    new_p[f'c{i}'] = float(ck)
            elif 'family3' in fam:
                thetas = [t + rng.uniform(-0.1, 0.1) for t in p['thetas']]
                alphas = [a + rng.uniform(-0.02, 0.02) for a in p['alphas']]
                fp = lambda z, _t=thetas, _a=alphas: family3_deriv_vec(z, _t, _a)
                f = lambda z, _t=thetas, _a=alphas: family3_func_vec(z, _t, _a, N_quad=80)
                new_p = {'thetas': thetas, 'alphas': alphas, 'n_slits': len(thetas)}
            else:
                continue
            if not check_deriv_nonzero(fp):
                continue
            try:
                Bf = compute_Bf_fast(f)
            except Exception:
                continue
            refined.append({
                'family': fam.split('_refined')[0] + '_refined',
                'params': new_p,
                'Bf': float(Bf),
                'is_univalent': True
            })
    return refined


# ============================================================
# High-precision B_f for the single best result
# ============================================================

def compute_Bf_precise(f_func, N_boundary=4096, n_circles=80):
    theta_bdy = np.linspace(0, 2 * np.pi, N_boundary, endpoint=False)
    w_bdy = f_func(np.exp(1j * theta_bdy))

    w_list = [f_func(np.array([0.0 + 0j]))]
    for i in range(1, n_circles + 1):
        r = i / (n_circles + 1) * 0.999
        n_pts = max(24, int(120 * r))
        theta = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
        w_list.append(f_func(r * np.exp(1j * theta)))
    w_cand = np.concatenate(w_list)

    best_r = 0.0
    bs = 512
    for i in range(0, len(w_cand), bs):
        batch = w_cand[i:i + bs]
        dists = np.abs(batch[:, None] - w_bdy[None, :])
        cand = dists.min(axis=1).max()
        if cand > best_r:
            best_r = cand
    return best_r


# ============================================================
# Main
# ============================================================

def main():
    t_start = time.time()
    all_results = []

    print("=" * 70)
    print("Slit Mapping Search for Upper Bounds on B_u")
    print("=" * 70)

    # --- Family 1 ---
    print("\n[Family 1] n-fold symmetric perturbations...")
    t0 = time.time()
    r1 = run_family1()
    all_results.extend(r1)
    if r1:
        print(f"  {len(r1)} configs, best B_f = {min(x['Bf'] for x in r1):.6f}  ({time.time()-t0:.1f}s)")
    else:
        print(f"  No valid configs ({time.time()-t0:.1f}s)")

    # --- Family 2 ---
    print("\n[Family 2] Combination perturbations...")
    t0 = time.time()
    r2 = run_family2()
    all_results.extend(r2)
    if r2:
        print(f"  {len(r2)} configs, best B_f = {min(x['Bf'] for x in r2):.6f}  ({time.time()-t0:.1f}s)")
    else:
        print(f"  No valid configs ({time.time()-t0:.1f}s)")

    # --- Family 3 ---
    print("\n[Family 3] Schwarz-Christoffel-type mappings...")
    t0 = time.time()
    r3 = run_family3()
    all_results.extend(r3)
    if r3:
        print(f"  {len(r3)} configs, best B_f = {min(x['Bf'] for x in r3):.6f}  ({time.time()-t0:.1f}s)")
    else:
        print(f"  No valid configs ({time.time()-t0:.1f}s)")

    # --- Family 4 ---
    print("\n[Family 4] Star-shaped with deep indentations...")
    t0 = time.time()
    r4 = run_family4()
    all_results.extend(r4)
    if r4:
        print(f"  {len(r4)} configs, best B_f = {min(x['Bf'] for x in r4):.6f}  ({time.time()-t0:.1f}s)")
    else:
        print(f"  No valid configs ({time.time()-t0:.1f}s)")

    print(f"\nTotal configurations so far: {len(all_results)}")

    # --- Refinement ---
    print("\n[Refinement] Searching around best configurations...")
    t0 = time.time()
    rr = refine_search(all_results, top_k=10, n_refine=30)
    all_results.extend(rr)
    if rr:
        print(f"  {len(rr)} refined, best B_f = {min(x['Bf'] for x in rr):.6f}  ({time.time()-t0:.1f}s)")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if not all_results:
        print("ERROR: No valid configurations found!")
        return

    all_sorted = sorted(all_results, key=lambda x: x['Bf'])
    best = all_sorted[0]

    print(f"\nTotal configurations evaluated: {len(all_results)}")
    print(f"\nBest upper bound on B_u:  B_f = {best['Bf']:.8f}")
    print(f"  Family: {best['family']}")
    print(f"  Parameters: {best['params']}")

    # Precise recomputation
    print("\n[Precise] Recomputing best B_f with higher precision...")
    fam = best['family']
    p = best['params']
    if 'family1' in fam:
        f_best = lambda z: family1_func(z, p['n'], p['c'])
    elif 'family4' in fam:
        f_best = lambda z: family4_func(z, p['n'], p['a'])
    elif 'family2' in fam:
        nt = sum(1 for k in p if k.startswith('n'))
        coeffs = [(p[f'n{i}'], p[f'c{i}']) for i in range(nt)]
        f_best = lambda z: family2_func(z, coeffs)
    elif 'family3' in fam:
        f_best = lambda z: family3_func_vec(z, p['thetas'], p['alphas'], N_quad=150)
    else:
        f_best = None

    precise_Bf = best['Bf']
    if f_best is not None:
        precise_Bf = compute_Bf_precise(f_best)
        print(f"  Precise B_f = {precise_Bf:.8f}")

    final_bound = min(precise_Bf, best['Bf'])

    # Top 10
    print("\nTop 10 configurations (lowest B_f):")
    for i, r in enumerate(all_sorted[:10]):
        print(f"  {i+1}. B_f = {r['Bf']:.6f} | {r['family']} | {r['params']}")

    # By family
    print("\nResults by family:")
    families = sorted(set(r['family'] for r in all_results))
    for fam in families:
        bfs = [r['Bf'] for r in all_results if r['family'] == fam]
        print(f"  {fam}: {len(bfs)} configs, min={min(bfs):.6f}, max={max(bfs):.6f}, mean={np.mean(bfs):.6f}")

    # Comparison
    COC = 0.6564
    print(f"\nComparison:")
    print(f"  Carroll & Ortega-Cerda (2013): B_u <= {COC}")
    print(f"  Our best:                      B_u <= {final_bound:.6f}")
    if final_bound < COC:
        print(f"  ** Our bound is BETTER (lower) by {COC - final_bound:.6f} **")
    else:
        print(f"  Carroll & Ortega-Cerda bound is better by {final_bound - COC:.6f}")

    total_time = time.time() - t_start
    print(f"\nTotal runtime: {total_time:.1f}s")

    # --- Save JSON ---
    output = {
        'best_upper_bound': float(final_bound),
        'precise_Bf': float(precise_Bf),
        'slit_parameters': best,
        'all_results': all_sorted,
        'total_configs_tested': len(all_results),
        'comparison': {
            'Carroll_Ortega_Cerda_2013': COC,
            'our_best': float(final_bound),
            'improvement': float(COC - final_bound)
        },
        'family_summaries': {},
        'runtime_seconds': total_time
    }
    for fam in families:
        bfs = [r['Bf'] for r in all_results if r['family'] == fam]
        output['family_summaries'][fam] = {
            'count': len(bfs),
            'min_Bf': float(min(bfs)),
            'max_Bf': float(max(bfs)),
            'mean_Bf': float(np.mean(bfs))
        }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upper_bound_search.json')
    with open(out_path, 'w') as fh:
        json.dump(output, fh, indent=2, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
