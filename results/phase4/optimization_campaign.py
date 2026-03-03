#!/usr/bin/env python3
"""
Optimization campaign for Bloch constant B_f minimization over univalent functions.

Parametrizes univalent functions as f(z) = z + sum_{n=2}^N a_n z^n with REAL coefficients.
Uses scipy.optimize.differential_evolution to minimize B_f across degrees N=5,7,10,15,20.

The minimum B_f found gives an upper bound: B_u <= min(B_f).
The known lower bound is B_u > 0.5708858 (Skinner).
"""

import numpy as np
import json
import time
from scipy.optimize import differential_evolution

np.random.seed(42)

# ---------------------------------------------------------------------------
# B_f computation via boundary sampling
# ---------------------------------------------------------------------------
def compute_Bf(coeffs, N_pts=5000):
    """
    Compute the Bloch constant B_f for f(z) = z + sum a_k z^k.
    
    B_f = sup_{w in f(D)} {largest r such that D(w,r) subset f(D)}
    
    We approximate by sampling f on the boundary circle |z|=0.999
    and for interior image points, finding the min distance to the boundary curve.
    """
    theta = np.linspace(0, 2 * np.pi, N_pts, endpoint=False)
    z_bnd = 0.999 * np.exp(1j * theta)
    
    # Evaluate f on boundary
    f_bnd = z_bnd.copy()
    for k, a in enumerate(coeffs, start=2):
        f_bnd = f_bnd + a * z_bnd**k
    
    # Grid search over interior points
    best = 0.0
    for r in np.linspace(0, 0.95, 20):
        if r == 0:
            z_int = np.array([0.0 + 0j])
        else:
            z_int = r * np.exp(1j * np.linspace(0, 2 * np.pi, 50, endpoint=False))
        
        f_int = z_int.copy()
        for k, a in enumerate(coeffs, start=2):
            f_int = f_int + a * z_int**k
        
        for w in f_int:
            d = np.min(np.abs(f_bnd - w))
            if d > best:
                best = d
    
    return best


# ---------------------------------------------------------------------------
# Univalence verification
# ---------------------------------------------------------------------------
def check_starlike(coeffs):
    """
    Check the starlike sufficient condition: sum_{k=2}^N k|a_k| <= 1.
    If satisfied, f is starlike hence univalent.
    """
    total = sum((k) * abs(a) for k, a in enumerate(coeffs, start=2))
    return total <= 1.0


def check_derivative_roots(coeffs):
    """
    Check that f'(z) has no zeros inside |z| < 1.
    
    f'(z) = 1 + 2*a_2*z + 3*a_3*z^2 + ... + N*a_N*z^{N-1}
    
    Returns True if all roots of f'(z) have |root| > 1.
    """
    N = len(coeffs) + 1  # degree of f
    if N <= 1:
        return True
    
    # Build polynomial coefficients for f'(z) in numpy convention: [highest, ..., constant]
    # f'(z) = N*a_N * z^{N-1} + ... + 2*a_2 * z + 1
    deriv_poly = np.zeros(N)  # degree N-1 polynomial has N coefficients
    deriv_poly[-1] = 1.0  # constant term
    for k, a in enumerate(coeffs, start=2):
        # k*a_k * z^{k-1}: coefficient of z^{k-1}
        # In numpy convention, index 0 = highest power = z^{N-1}
        # z^{k-1} has index (N-1) - (k-1) = N - k
        deriv_poly[N - k] = k * a
    
    roots = np.roots(deriv_poly)
    if len(roots) == 0:
        return True
    
    min_abs = np.min(np.abs(roots))
    return min_abs > 1.0


def check_winding_number(coeffs, n_test=20, n_boundary=2000):
    """
    Verify the winding number of f(r*e^{it}) around sample interior image points is exactly 1.
    """
    theta = np.linspace(0, 2 * np.pi, n_boundary, endpoint=False)
    r_bnd = 0.998
    z_bnd = r_bnd * np.exp(1j * theta)
    
    f_bnd = z_bnd.copy()
    for k, a in enumerate(coeffs, start=2):
        f_bnd = f_bnd + a * z_bnd**k
    
    test_radii = [0.0, 0.2, 0.5, 0.7]
    test_angles = np.linspace(0, 2 * np.pi, max(n_test // 4, 4), endpoint=False)
    
    for r in test_radii:
        if r == 0:
            z_pts = np.array([0.0 + 0j])
        else:
            z_pts = r * np.exp(1j * test_angles)
        
        f_pts = z_pts.copy()
        for k, a in enumerate(coeffs, start=2):
            f_pts = f_pts + a * z_pts**k
        
        for w in f_pts:
            diffs = f_bnd - w
            angles = np.angle(diffs)
            angle_diffs = np.diff(angles)
            angle_diffs = (angle_diffs + np.pi) % (2 * np.pi) - np.pi
            winding = np.sum(angle_diffs) / (2 * np.pi)
            if abs(winding - 1.0) > 0.1:
                return False
    
    return True


def verify_univalent(coeffs):
    """
    Verify univalence:
    1. Starlike condition (sufficient)
    2. f'(z) no zeros in D + winding number check
    
    Returns (is_univalent, method_used)
    """
    if check_starlike(coeffs):
        return True, "starlike"
    
    if not check_derivative_roots(coeffs):
        return False, "derivative_root_in_D"
    
    if not check_winding_number(coeffs):
        return False, "winding_number_fail"
    
    return True, "derivative_roots+winding"


# ---------------------------------------------------------------------------
# Two-phase objective: starlike-constrained and general
# ---------------------------------------------------------------------------
def objective_starlike(x, degree):
    """
    Objective for starlike-constrained search.
    We reparametrize: x in [-1,1]^{N-1}, then scale so that
    sum_{k=2}^N k * |a_k| = s for some target s <= 1.
    
    Actually, let's use a simpler approach:
    x = raw coefficients. If sum k|a_k| > 1, project onto the constraint.
    """
    coeffs = x.copy()
    
    # Project onto starlike constraint: sum k|a_k| <= 1
    total = sum(k * abs(a) for k, a in enumerate(coeffs, start=2))
    if total > 1.0:
        # Scale down
        coeffs = coeffs / total
    
    bf = compute_Bf(coeffs, N_pts=5000)
    return bf


def objective_general(x, degree):
    """
    General objective: check univalence via roots + winding.
    Returns B_f if univalent, large penalty otherwise.
    """
    coeffs = x
    
    # Check derivative roots first (fast)
    if not check_derivative_roots(coeffs):
        return 1e6
    
    # Quick winding number check
    if not check_winding_number(coeffs, n_test=8, n_boundary=500):
        return 1e6
    
    bf = compute_Bf(coeffs, N_pts=5000)
    return bf


# ---------------------------------------------------------------------------
# Main optimization campaign
# ---------------------------------------------------------------------------
def run_optimization(degree, max_evals, verbose=True):
    """
    Run differential_evolution to minimize B_f for degree N.
    Two phases:
    1. Starlike-constrained (guaranteed univalent, restrictive)
    2. General (derivative roots + winding number check)
    """
    n_coeffs = degree - 1  # a_2, ..., a_N
    
    # ---- Phase 1: Starlike-constrained ----
    # Bounds: |a_k| <= 1/k from starlike condition
    starlike_bounds = [(-1.0 / k, 1.0 / k) for k in range(2, degree + 1)]
    
    phase1_evals = max_evals // 2
    phase1_eval_count = [0]
    phase1_best_bf = [1e10]
    phase1_best_coeffs = [np.zeros(n_coeffs)]
    
    def wrapped_starlike(x):
        phase1_eval_count[0] += 1
        bf = objective_starlike(x, degree)
        if bf < phase1_best_bf[0]:
            phase1_best_bf[0] = bf
            phase1_best_coeffs[0] = x.copy()
        return bf
    
    popsize_1 = max(5, min(15, phase1_evals // (n_coeffs * 5)))
    pop_total_1 = popsize_1 * n_coeffs
    maxiter_1 = max(2, (phase1_evals - pop_total_1) // pop_total_1)
    
    if verbose:
        print(f"  Phase 1 (starlike): popsize={popsize_1}, maxiter={maxiter_1}")
    
    try:
        res1 = differential_evolution(
            wrapped_starlike,
            bounds=starlike_bounds,
            seed=42,
            maxiter=maxiter_1,
            popsize=popsize_1,
            tol=1e-10,
            mutation=(0.5, 1.5),
            recombination=0.9,
            polish=False,
        )
        star_coeffs = res1.x.copy()
        star_bf = res1.fun
    except Exception as e:
        if verbose:
            print(f"  Phase 1 error: {e}")
        star_coeffs = phase1_best_coeffs[0]
        star_bf = phase1_best_bf[0]
    
    # Ensure starlike constraint is satisfied
    total = sum(k * abs(a) for k, a in enumerate(star_coeffs, start=2))
    if total > 1.0:
        star_coeffs = star_coeffs / total
        star_bf = compute_Bf(star_coeffs, N_pts=5000)
    
    if verbose:
        print(f"  Phase 1 result: B_f = {star_bf:.6f}, evals = {phase1_eval_count[0]}")
    
    # ---- Phase 2: General search (wider bounds, root+winding check) ----
    phase2_evals = max_evals - phase1_eval_count[0]
    phase2_eval_count = [0]
    phase2_best_bf = [1e10]
    phase2_best_coeffs = [np.zeros(n_coeffs)]
    
    # Use wider bounds but not full de Branges
    general_bounds = [(-min(1.5, k * 0.5), min(1.5, k * 0.5)) for k in range(2, degree + 1)]
    
    def wrapped_general(x):
        phase2_eval_count[0] += 1
        bf = objective_general(x, degree)
        if bf < phase2_best_bf[0] and bf < 1e5:
            phase2_best_bf[0] = bf
            phase2_best_coeffs[0] = x.copy()
        return bf
    
    popsize_2 = max(5, min(15, phase2_evals // (n_coeffs * 5)))
    pop_total_2 = popsize_2 * n_coeffs
    maxiter_2 = max(2, (phase2_evals - pop_total_2) // pop_total_2)
    
    if verbose:
        print(f"  Phase 2 (general): popsize={popsize_2}, maxiter={maxiter_2}")
    
    try:
        res2 = differential_evolution(
            wrapped_general,
            bounds=general_bounds,
            seed=42 + degree,
            maxiter=maxiter_2,
            popsize=popsize_2,
            tol=1e-10,
            mutation=(0.5, 1.5),
            recombination=0.9,
            polish=False,
        )
        gen_coeffs = res2.x.copy()
        gen_bf = res2.fun
    except Exception as e:
        if verbose:
            print(f"  Phase 2 error: {e}")
        gen_coeffs = phase2_best_coeffs[0]
        gen_bf = phase2_best_bf[0]
    
    if verbose:
        print(f"  Phase 2 result: B_f = {gen_bf:.6f}, evals = {phase2_eval_count[0]}")
    
    total_evals = phase1_eval_count[0] + phase2_eval_count[0]
    
    # Pick best result
    if gen_bf < star_bf and gen_bf < 1e5:
        best_coeffs = gen_coeffs
        best_bf = gen_bf
    else:
        best_coeffs = star_coeffs
        best_bf = star_bf
    
    # Also check identity
    identity_bf = compute_Bf(np.zeros(n_coeffs), N_pts=5000)
    if identity_bf < best_bf:
        best_coeffs = np.zeros(n_coeffs)
        best_bf = identity_bf
    
    # Verify univalence of final answer
    is_univalent, method = verify_univalent(best_coeffs)
    
    # Recompute B_f with full precision
    best_bf = compute_Bf(best_coeffs, N_pts=5000)
    
    if verbose:
        print(f"  Final: B_f = {best_bf:.6f}, univalent={is_univalent} ({method}), "
              f"total_evals={total_evals}")
        top5 = np.argsort(np.abs(best_coeffs))[::-1][:5]
        for idx in top5:
            k = idx + 2
            print(f"    a_{k} = {best_coeffs[idx]:.6f}")
    
    return {
        "degree": degree,
        "best_Bf": float(best_bf),
        "best_coefficients": [float(c) for c in best_coeffs],
        "is_univalent_verified": is_univalent,
        "univalence_method": method,
        "evaluation_count": total_evals,
    }


def main():
    print("=" * 70)
    print("OPTIMIZATION CAMPAIGN: Minimizing B_f over univalent polynomials")
    print("=" * 70)
    print(f"Goal: Find upper bounds on B_u via B_u <= min(B_f)")
    print(f"Known lower bound (Skinner): B_u > 0.5708858")
    print()
    
    start_time = time.time()
    
    degrees = [5, 7, 10, 15, 20]
    # Larger budgets to ensure >= 1000 total
    eval_budgets = {
        5:  350,
        7:  350,
        10: 300,
        15: 250,
        20: 250,
    }
    
    results = {}
    total_evals = 0
    global_best_bf = 1e10
    global_best_degree = None
    
    for N in degrees:
        print(f"\n{'='*50}")
        print(f"Degree N = {N}")
        print(f"{'='*50}")
        
        res = run_optimization(N, eval_budgets[N], verbose=True)
        results[str(N)] = res
        total_evals += res["evaluation_count"]
        
        if res["is_univalent_verified"] and res["best_Bf"] < global_best_bf:
            global_best_bf = res["best_Bf"]
            global_best_degree = N
        
        elapsed = time.time() - start_time
        print(f"  Elapsed: {elapsed:.1f}s, total evals so far: {total_evals}")
    
    # If we haven't reached 1000 evals, do additional runs on low degrees
    if total_evals < 1000:
        print(f"\nTotal evals = {total_evals} < 1000. Running additional searches...")
        extra_needed = 1000 - total_evals
        for extra_N in [5, 7, 10]:
            if extra_needed <= 0:
                break
            budget = min(extra_needed + 50, 300)
            print(f"\n  Extra run: N={extra_N}, budget={budget}")
            res_extra = run_optimization(extra_N, budget, verbose=True)
            total_evals += res_extra["evaluation_count"]
            extra_needed -= res_extra["evaluation_count"]
            
            key = str(extra_N)
            if res_extra["is_univalent_verified"] and res_extra["best_Bf"] < results[key]["best_Bf"]:
                results[key] = res_extra
            if res_extra["is_univalent_verified"] and res_extra["best_Bf"] < global_best_bf:
                global_best_bf = res_extra["best_Bf"]
                global_best_degree = extra_N
            # Accumulate evaluation count
            results[key]["evaluation_count"] += res_extra["evaluation_count"]
    
    # Identity reference
    identity_bf = compute_Bf(np.zeros(1), N_pts=5000)
    print(f"\nReference: B_f(identity f(z)=z) = {identity_bf:.6f}")
    
    if global_best_bf >= 1e5:
        global_best_bf = identity_bf
    
    elapsed_total = time.time() - start_time
    
    # Compile output
    output = {
        "description": "Optimization campaign minimizing B_f over univalent polynomial maps",
        "method": "differential_evolution with real coefficients, two-phase (starlike + general)",
        "parametrization": "f(z) = z + sum_{n=2}^N a_n z^n, a_n real",
        "univalence_checks": [
            "starlike sufficient condition: sum k|a_k| <= 1",
            "f'(z) root check: all roots of f' outside unit disk",
            "winding number verification"
        ],
        "de_branges_bounds": "|a_n| <= n",
        "boundary_sampling": {"radius": 0.999, "points": 5000},
        "best_lower_bound": float(global_best_bf),
        "best_lower_bound_note": "This is min(B_f) over verified univalent candidates, giving B_u <= this value",
        "skinner_comparison": 0.5708858,
        "skinner_note": "Known lower bound B_u > 0.5708858",
        "total_evaluations": total_evals,
        "elapsed_seconds": round(elapsed_total, 2),
        "degrees": {},
    }
    
    for N in degrees:
        key = str(N)
        output["degrees"][key] = results[key]
    
    output_path = "results/phase4/optimization_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"Total evaluations: {total_evals}")
    print(f"Best B_f found (upper bound on B_u): {global_best_bf:.6f}")
    print(f"Skinner lower bound:                  0.5708858")
    if global_best_degree:
        print(f"Best degree: N={global_best_degree}")
    print(f"Elapsed time: {elapsed_total:.1f}s")
    print(f"Results saved to: {output_path}")
    
    for N in degrees:
        key = str(N)
        r = results[key]
        print(f"  N={N:2d}: B_f={r['best_Bf']:.6f}, univalent={r['is_univalent_verified']}, "
              f"evals={r['evaluation_count']}")
    
    print(f"\nDone.")


if __name__ == "__main__":
    main()
