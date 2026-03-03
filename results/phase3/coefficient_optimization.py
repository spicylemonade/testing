#!/usr/bin/env python3
"""
Coefficient optimization for the Bloch-Landau constant.

Parametrizes univalent functions as f(z) = z + sum_{n=2}^N a_n z^n,
uses scipy.optimize.differential_evolution to maximize B_f (the inradius),
and checks univalence via critical point analysis.

Outputs results to stdout and saves to results/phase3/coefficient_results.json.
"""

import json
import os
import time

import numpy as np
from scipy.optimize import differential_evolution
from scipy.spatial import cKDTree

np.random.seed(42)

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
N_VALUES = [5, 7, 10, 15, 20]
N_BOUNDARY = 5000          # boundary sample points
R_BOUNDARY = 0.999         # radius for boundary approximation
PENALTY = 1e6              # penalty for non-univalent maps

# Pre-compute boundary angles (shared across calls)
_t_boundary = np.linspace(0, 2 * np.pi, N_BOUNDARY, endpoint=False)
_z_boundary = R_BOUNDARY * np.exp(1j * _t_boundary)

# Interior sampling for B_f: use a coarser grid during optimization,
# then refine for the final result.
_N_INT_RADII_FAST = 15
_N_INT_ANGLES_FAST = 80
_R_INT_MAX = 0.99

_radii_fast = np.linspace(0.0, _R_INT_MAX, _N_INT_RADII_FAST + 1)
_angles_fast = np.linspace(0, 2 * np.pi, _N_INT_ANGLES_FAST, endpoint=False)

# For final (accurate) evaluation
_N_INT_RADII_FINE = 30
_N_INT_ANGLES_FINE = 200
_radii_fine = np.linspace(0.0, _R_INT_MAX, _N_INT_RADII_FINE + 1)
_angles_fine = np.linspace(0, 2 * np.pi, _N_INT_ANGLES_FINE, endpoint=False)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def eval_poly(coeffs, z):
    """
    Evaluate f(z) = z + a2*z^2 + a3*z^3 + ... given coeffs = [a2, a3, ...].
    """
    result = z.copy().astype(complex)
    zn = z * z  # z^2
    for a in coeffs:
        result += a * zn
        zn *= z
    return result


def check_univalence(coeffs):
    """
    Check univalence by finding roots of f'(z).
    Returns (is_univalent, min_root_abs).
    """
    N = len(coeffs) + 1
    # f'(z) coefficients in descending order
    deriv_coeffs = []
    for k in range(N, 1, -1):
        deriv_coeffs.append(k * coeffs[k - 2])
    deriv_coeffs.append(1.0)

    if len(deriv_coeffs) < 2:
        return True, float('inf')

    # Strip leading near-zeros
    while len(deriv_coeffs) > 1 and abs(deriv_coeffs[0]) < 1e-15:
        deriv_coeffs.pop(0)

    if len(deriv_coeffs) < 2:
        return True, float('inf')

    roots = np.roots(deriv_coeffs)
    if len(roots) == 0:
        return True, float('inf')

    abs_roots = np.abs(roots)
    min_root_abs = float(np.min(abs_roots))

    return (min_root_abs >= 1.0), min_root_abs


def compute_Bf(coeffs, fine=False):
    """
    Compute B_f (the inradius) using a KD-tree for fast nearest-boundary queries.
    """
    w_boundary = eval_poly(coeffs, _z_boundary)
    # Build KD-tree on boundary points (real, imag)
    bnd_xy = np.column_stack([w_boundary.real, w_boundary.imag])
    tree = cKDTree(bnd_xy)

    radii = _radii_fine if fine else _radii_fast
    angles = _angles_fine if fine else _angles_fast

    max_dist = 0.0

    # Origin: f(0) = 0
    d_origin, _ = tree.query([0.0, 0.0])
    max_dist = d_origin

    for r in radii:
        if r == 0.0:
            continue
        z_int = r * np.exp(1j * angles)
        w_int = eval_poly(coeffs, z_int)
        pts = np.column_stack([w_int.real, w_int.imag])
        dists, _ = tree.query(pts)
        d = float(np.max(dists))
        if d > max_dist:
            max_dist = d

    return max_dist


def objective(params):
    """
    Objective for DE. Minimizes B_f (we seek the univalent function with
    the smallest inradius, giving an upper bound on the Landau constant).
    Non-univalent maps receive a large penalty.
    """
    is_univ, min_root_abs = check_univalence(params)

    if not is_univ:
        violation = 1.0 - min_root_abs
        return PENALTY * (1.0 + violation)

    try:
        bf = compute_Bf(params, fine=False)
    except Exception:
        return PENALTY

    # We want to MINIMIZE B_f to find the tightest upper bound
    return bf


def make_initial_population(N, pop_size):
    """
    Seed the DE population with known univalent functions.
    """
    n_params = N - 1
    population = []
    rng = np.random.RandomState(42)

    # 1. Identity: all zeros
    population.append(np.zeros(n_params))

    # 2. Truncated Koebe: a_k = k
    koebe = np.array([float(k) for k in range(2, N + 1)])
    population.append(koebe)

    # 3. Negative Koebe (rotation by pi)
    neg_koebe = np.array([float(k) * ((-1) ** k) for k in range(2, N + 1)])
    population.append(neg_koebe)

    # 4. Half-plane map z/(1-z): a_k = 1
    population.append(np.ones(n_params))

    # 5. Starlike (sum k|ak| <= 1)
    for scale in [0.1, 0.3, 0.5, 0.8]:
        c = np.zeros(n_params)
        rem = 1.0
        for i in range(n_params):
            k = i + 2
            c[i] = scale * rem / k
            rem -= k * abs(c[i])
            if rem <= 0:
                break
        population.append(c)
        population.append(-c)

    # 6. Scaled Koebe
    for s in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7]:
        population.append(s * koebe)

    # 7. Small random perturbations
    for _ in range(10):
        population.append(rng.uniform(-0.3, 0.3, n_params))

    # 8. Medium random
    for _ in range(5):
        population.append(np.array([
            rng.uniform(-k * 0.3, k * 0.3) for k in range(2, N + 1)
        ]))

    # Fill rest randomly within moderate bounds
    while len(population) < pop_size:
        population.append(np.array([
            rng.uniform(-k * 0.4, k * 0.4) for k in range(2, N + 1)
        ]))

    population = population[:pop_size]
    lo = np.array([-float(k) for k in range(2, N + 1)])
    hi = np.array([float(k) for k in range(2, N + 1)])
    for i in range(len(population)):
        population[i] = np.clip(population[i], lo, hi)

    return np.array(population)


def get_de_params(N):
    """Adaptive DE parameters based on problem dimension."""
    n_params = N - 1
    if N <= 7:
        return {"maxiter": 200, "popsize_mult": 15, "min_pop": 40}
    elif N <= 10:
        return {"maxiter": 150, "popsize_mult": 12, "min_pop": 40}
    elif N <= 15:
        return {"maxiter": 100, "popsize_mult": 10, "min_pop": 40}
    else:
        return {"maxiter": 80, "popsize_mult": 8, "min_pop": 40}


def run_optimization(N):
    """
    Run optimization for polynomial degree N.
    """
    n_params = N - 1
    bounds = [(-k, k) for k in range(2, N + 1)]
    de_params = get_de_params(N)
    pop_size = max(de_params["popsize_mult"] * n_params, de_params["min_pop"])
    max_iter = de_params["maxiter"]

    print(f"\n{'='*60}")
    print(f"Optimizing for N = {N} ({n_params} parameters)")
    print(f"Population: {pop_size}, Max iter: {max_iter}")
    print(f"{'='*60}")
    sys.stdout.flush()

    init_pop = make_initial_population(N, pop_size)

    t0 = time.time()

    rng_state = np.random.RandomState(42)
    result = differential_evolution(
        objective,
        bounds=bounds,
        seed=rng_state,
        maxiter=max_iter,
        tol=1e-6,
        init=init_pop,
        mutation=(0.5, 1.5),
        recombination=0.9,
        polish=True,
        disp=False,
    )

    elapsed = time.time() - t0
    best_coeffs = result.x.tolist()
    is_univ, min_root_abs = check_univalence(np.array(best_coeffs))

    # Recompute B_f with fine grid for accurate result
    if is_univ and result.fun < PENALTY / 2:
        best_Bf = compute_Bf(np.array(best_coeffs), fine=True)
    else:
        best_Bf = result.fun if result.fun < PENALTY / 2 else float('inf')

    print(f"  Best B_f          = {best_Bf:.8f}")
    print(f"  Univalent         = {is_univ}")
    print(f"  Min |root of f'|  = {min_root_abs:.6f}")
    print(f"  Time              = {elapsed:.2f} s")
    print(f"  Coefficients:")
    for k, a in enumerate(best_coeffs, start=2):
        print(f"    a{k} = {a:+.8f}  (bound: {k})")
    print(f"  DE converged      = {result.success}")
    print(f"  DE message        = {result.message}")
    sys.stdout.flush()

    return {
        "N": N,
        "best_Bf": round(best_Bf, 10),
        "best_coefficients": {
            f"a{k}": round(a, 10)
            for k, a in enumerate(best_coeffs, start=2)
        },
        "is_univalent": is_univ,
        "min_root_abs": round(min_root_abs, 6),
        "computation_time": round(elapsed, 2),
        "de_converged": bool(result.success),
        "de_message": result.message,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
import sys  # noqa: E402 (re-import for flush usage above)


def main():
    print("Coefficient Optimization for the Bloch-Landau Constant")
    print("=" * 60)
    print(f"Boundary samples     : {N_BOUNDARY}")
    print(f"Boundary radius      : {R_BOUNDARY}")
    print(f"Interior (fast)      : {_N_INT_RADII_FAST} radii x {_N_INT_ANGLES_FAST} angles")
    print(f"Interior (fine)      : {_N_INT_RADII_FINE} radii x {_N_INT_ANGLES_FINE} angles")
    print(f"Degree values        : {N_VALUES}")
    sys.stdout.flush()

    all_results = []

    for N in N_VALUES:
        entry = run_optimization(N)
        all_results.append(entry)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'N':>4}  {'B_f':>12}  {'Univalent':>10}  {'Min|root|':>10}  {'Time (s)':>10}")
    print(f"{'-'*4}  {'-'*12}  {'-'*10}  {'-'*10}  {'-'*10}")
    for r in all_results:
        print(f"{r['N']:>4}  {r['best_Bf']:>12.8f}  "
              f"{str(r['is_univalent']):>10}  "
              f"{r['min_root_abs']:>10.4f}  "
              f"{r['computation_time']:>10.2f}")

    print(f"\nComparison with known results (upper bounds on the Landau constant):")
    print(f"  Skinner (1994)             : 0.5708858")
    print(f"  Carroll & Ortega-Cerda     : 0.6564")
    # The best upper bound is the minimum B_f found (smallest inradius over univalent class)
    finite_results = [r["best_Bf"] for r in all_results if r["best_Bf"] < 1e5]
    if finite_results:
        best_overall = min(finite_results)
    else:
        best_overall = float('inf')
    print(f"  Best from this optimization: {best_overall:.8f}")

    if best_overall < float('inf'):
        if best_overall <= 0.5708858:
            print("  -> Improves on or matches Skinner's bound!")
        elif best_overall <= 0.6564:
            print("  -> Between Skinner and Carroll-Ortega-Cerda bounds")
        else:
            print("  -> Above Carroll-Ortega-Cerda (need sharper optimization)")
    else:
        print("  -> No valid univalent minimizer found")

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "coefficient_results.json")

    output_data = {
        "description": "Coefficient optimization for the Bloch-Landau constant",
        "parameters": {
            "N_boundary": N_BOUNDARY,
            "R_boundary": R_BOUNDARY,
            "N_interior_radii_fast": _N_INT_RADII_FAST,
            "N_interior_angles_fast": _N_INT_ANGLES_FAST,
            "N_interior_radii_fine": _N_INT_RADII_FINE,
            "N_interior_angles_fine": _N_INT_ANGLES_FINE,
        },
        "known_bounds": {
            "Skinner_1994": 0.5708858,
            "Carroll_OrtegaCerda": 0.6564,
        },
        "results": all_results,
        "best_overall_Bf": best_overall,
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
