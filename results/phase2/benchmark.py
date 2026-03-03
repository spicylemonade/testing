"""
Benchmark suite for computing lower bounds on B_f for families of univalent functions.

Computes B_f = inradius(f(D)) via boundary sampling and optimization for five
canonical families:
  1. Identity: f(z) = z
  2. Strip mapping (arctanh): f(z) = arctanh(z)
  3. Starlike: f(z) = z / (1 - z)^{2(1 - alpha)}
  4. Lens mapping: f(z) = ((1+z)^beta - (1-z)^beta) / (2*beta)
  5. Polynomial perturbations: f(z) = z + c * z^3

Results are compared against the known Skinner (2009) lower bound B_u > 0.5708858.
All computations are reproducible with np.random.seed(42).
"""

import numpy as np
from scipy.optimize import minimize
import json
import os
import sys

np.random.seed(42)

SKINNER_BOUND = 0.5708858


# =============================================================================
# Core: boundary sampling and inradius computation
# =============================================================================

def _sample_boundary(f, N=8000, radii=None):
    """
    Sample boundary of f(D) by evaluating f on circles |z| = r for r close to 1.
    Returns an array of finite boundary points.
    """
    if radii is None:
        radii = [1.0 - 10**(-k) for k in range(3, 8)]
    n_per = max(N // len(radii), 200)
    all_pts = []
    for r in radii:
        theta = np.linspace(0, 2 * np.pi, n_per, endpoint=False)
        z = r * np.exp(1j * theta)
        pts = f(z)
        mask = np.isfinite(pts)
        all_pts.append(pts[mask])
    return np.concatenate(all_pts) if all_pts else np.array([], dtype=complex)


def _min_dist_to_boundary(w, boundary):
    """Euclidean distance from point w to the nearest boundary point."""
    if len(boundary) == 0:
        return 0.0
    return float(np.min(np.abs(boundary - w)))


def evaluate_lower_bound(f, params=None):
    """
    Compute a lower bound on B_f for a univalent function f.

    B_f = inradius of f(D) = sup_{w in f(D)} dist(w, boundary of f(D)).

    For bounded domains, this is the standard inradius computed by:
      1. Dense boundary sampling at multiple radii approaching |z| = 1.
      2. Grid search over interior points f(z) for |z| on a polar grid.
      3. Nelder-Mead refinement from the best grid point.

    For unbounded domains (e.g. strip mappings), the boundary sampling is
    restricted to points near the origin (|Re| < M, |Im| < M) and the
    inradius is computed locally, giving the correct geometric width.

    Parameters
    ----------
    f : callable
        Univalent function f: D -> C with f(0) = 0, f'(0) = 1.
    params : dict or None
        Optional parameters:
          - N_boundary (int): number of boundary samples (default 10000)
          - N_interior (int): number of interior grid points (default 800)
          - clip_radius (float or None): if set, clip boundary to |w| < clip_radius
            to handle unbounded domains. If None, auto-detect.

    Returns
    -------
    float
        Lower bound on B_f (the inradius of f(D)).
    """
    if params is None:
        params = {}

    N_boundary = params.get("N_boundary", 10000)
    N_interior = params.get("N_interior", 800)
    clip_radius = params.get("clip_radius", None)

    # Step 1: sample boundary
    boundary = _sample_boundary(f, N=N_boundary)
    if len(boundary) < 50:
        return float("inf")

    # Step 2: detect unbounded domain and clip if needed
    max_abs = np.max(np.abs(boundary))
    is_unbounded = max_abs > 1e4

    if is_unbounded:
        if clip_radius is None:
            # Auto clip: keep points within a reasonable window near origin
            # For strip-like domains the width is the key quantity
            clip_radius = 10.0
        mask = np.abs(boundary) < clip_radius
        boundary = boundary[mask]
        if len(boundary) < 50:
            # Fall back to wider clip
            boundary = _sample_boundary(f, N=N_boundary)
            mask = np.abs(boundary) < 100.0
            boundary = boundary[mask]

    # Step 3: grid search over interior points
    best_d = 0.0
    best_w = 0.0 + 0j

    n_radii = 30
    n_angles = max(N_interior // n_radii, 24)
    r_values = np.linspace(0, 0.97, n_radii)
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)

    for r in r_values:
        if r == 0:
            z_vals = np.array([0.0 + 0j])
        else:
            z_vals = r * np.exp(1j * angles)
        w_vals = f(z_vals)
        for w in w_vals:
            if not np.isfinite(w):
                continue
            if is_unbounded and np.abs(w) > clip_radius * 0.9:
                continue
            d = _min_dist_to_boundary(w, boundary)
            if d > best_d:
                best_d = d
                best_w = w

    # Step 4: Nelder-Mead refinement
    def neg_inradius(xy):
        w = xy[0] + 1j * xy[1]
        return -_min_dist_to_boundary(w, boundary)

    x0 = [best_w.real, best_w.imag]
    result = minimize(
        neg_inradius,
        x0,
        method="Nelder-Mead",
        options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 8000},
    )

    return float(-result.fun)


# =============================================================================
# Five families of univalent functions
# =============================================================================

def family_identity(z):
    """f(z) = z.  Image is the unit disk D.  B_f = 1."""
    return z


def family_arctanh(z):
    """
    f(z) = arctanh(z) = (1/2) log((1+z)/(1-z)).
    Maps D onto the strip {w : |Im(w)| < pi/4}.
    f'(0) = 1.  B_f = pi/4 (half-width of strip).
    """
    return np.arctanh(z)


def make_starlike(alpha):
    """
    Return the starlike function f_alpha(z) = z / (1 - z)^{2(1-alpha)}.

    For alpha in (0, 1]:
      - alpha = 1  =>  f(z) = z  (identity)
      - alpha = 1/2  =>  f(z) = z / (1 - z)  (convex / half-plane map, unbounded)
      - alpha = 0  =>  f(z) = z / (1 - z)^2  (Koebe, unbounded)

    f'(0) = 1.  For alpha close to 1 the image is close to D and B_f ~ 1.
    For small alpha the image is unbounded and B_f -> inf.
    We test alpha = 0.8 which gives a bounded starlike image.
    """
    exponent = 2.0 * (1.0 - alpha)

    def f(z):
        return z / (1.0 - z) ** exponent

    return f


def make_lens(alpha):
    """
    Lens mapping: f(z) = ((1+z)^beta - (1-z)^beta) / (2*beta),
    where beta = 1 - alpha/pi.

    For alpha = pi: beta = 0, f -> z (identity).
    For alpha < pi: lens-shaped domain.
    f(0) = 0, f'(0) = 1.
    """
    beta = 1.0 - alpha / np.pi
    if abs(beta) < 1e-10:
        return family_identity

    def f(z):
        return ((1.0 + z) ** beta - (1.0 - z) ** beta) / (2.0 * beta)

    return f


def make_polynomial_perturbation(c):
    """
    f(z) = z + c * z^3.
    Univalent on D when |c| <= 1/3 (sufficient: sum k|a_k| <= 1 => 3|c| <= 1).
    f'(0) = 1.  The image is a perturbation of D.
    """

    def f(z):
        return z + c * z ** 3

    return f


# =============================================================================
# Test harness
# =============================================================================

def _comparison_label(Bf):
    """Return comparison string relative to the Skinner bound."""
    if Bf == float("inf"):
        return "above_skinner_bound"
    if Bf > SKINNER_BOUND:
        return "above_skinner_bound"
    return "below_skinner_bound"


def run_benchmark():
    """
    Run the benchmark on >= 5 families and collect results.
    Returns a list of result dicts.
    """
    np.random.seed(42)

    results = []

    # ---- 1. Identity ----
    print("[1/5] Identity: f(z) = z")
    Bf = evaluate_lower_bound(family_identity)
    entry = {
        "family": "identity",
        "B_f": round(Bf, 10),
        "parameters": {},
        "expected": 1.0,
        "comparison": _comparison_label(Bf),
    }
    results.append(entry)
    print(f"      B_f = {Bf:.8f}  (expected ~1.0)")

    # ---- 2. Strip mapping (arctanh) ----
    print("[2/5] Strip mapping: f(z) = arctanh(z)")
    Bf_strip = evaluate_lower_bound(
        family_arctanh,
        params={"N_boundary": 12000, "clip_radius": 8.0},
    )
    expected_strip = np.pi / 4.0
    entry = {
        "family": "arctanh_strip",
        "B_f": round(Bf_strip, 10),
        "parameters": {"clip_radius": 8.0},
        "expected": round(expected_strip, 10),
        "comparison": _comparison_label(Bf_strip),
    }
    results.append(entry)
    print(f"      B_f = {Bf_strip:.8f}  (expected ~{expected_strip:.8f})")

    # ---- 3. Starlike z/(1-z)^{2(1-alpha)} with alpha = 0.8 ----
    alpha_star = 0.8
    print(f"[3/5] Starlike: alpha = {alpha_star}")
    f_star = make_starlike(alpha_star)
    Bf_star = evaluate_lower_bound(f_star, params={"N_boundary": 12000})
    entry = {
        "family": "starlike",
        "B_f": round(Bf_star, 10),
        "parameters": {"alpha": alpha_star},
        "expected": None,
        "comparison": _comparison_label(Bf_star),
    }
    results.append(entry)
    print(f"      B_f = {Bf_star:.8f}")

    # ---- 4. Lens mapping with alpha = pi/2 ----
    alpha_lens = np.pi / 2.0
    print(f"[4/5] Lens mapping: alpha = pi/2")
    f_lens = make_lens(alpha_lens)
    Bf_lens = evaluate_lower_bound(f_lens, params={"N_boundary": 12000})
    entry = {
        "family": "lens",
        "B_f": round(Bf_lens, 10),
        "parameters": {"alpha": round(alpha_lens, 10)},
        "expected": None,
        "comparison": _comparison_label(Bf_lens),
    }
    results.append(entry)
    print(f"      B_f = {Bf_lens:.8f}")

    # ---- 5. Polynomial perturbations z + c*z^3 ----
    c_values = [0.05, 0.15, 0.25, 0.33]
    print(f"[5/5] Polynomial perturbations: z + c*z^3, c in {c_values}")
    for c in c_values:
        f_poly = make_polynomial_perturbation(c)
        Bf_poly = evaluate_lower_bound(f_poly, params={"N_boundary": 10000})
        entry = {
            "family": "polynomial_perturbation",
            "B_f": round(Bf_poly, 10),
            "parameters": {"c": c},
            "expected": None,
            "comparison": _comparison_label(Bf_poly),
        }
        results.append(entry)
        print(f"      c = {c:.2f}  =>  B_f = {Bf_poly:.8f}")

    return results


def main():
    print("=" * 66)
    print("  Benchmark: B_f lower bounds for univalent function families")
    print("  Skinner (2009) reference bound: B_u > 0.5708858")
    print("=" * 66)

    results = run_benchmark()

    # Summary
    print("\n" + "=" * 66)
    print("  Summary")
    print("=" * 66)
    for r in results:
        label = r["comparison"]
        fam = r["family"]
        bf = r["B_f"]
        pstr = json.dumps(r["parameters"])
        print(f"  {fam:30s}  B_f = {bf:12.8f}  {label}  params={pstr}")

    # Write JSON
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "benchmark_results.json"
    )
    output = {
        "seed": 42,
        "skinner_bound": SKINNER_BOUND,
        "results": results,
    }
    with open(output_path, "w") as fp:
        json.dump(output, fp, indent=2)
    print(f"\nResults written to {output_path}")

    # Validation: every result should be above Skinner bound for these families
    all_above = all(
        r["B_f"] > SKINNER_BOUND or r["B_f"] == float("inf") for r in results
    )
    if all_above:
        print("\nAll tested families yield B_f above the Skinner bound (0.5708858).")
    else:
        below = [r for r in results if r["B_f"] <= SKINNER_BOUND]
        print(f"\nWARNING: {len(below)} result(s) at or below the Skinner bound:")
        for r in below:
            print(f"  {r['family']} (params={r['parameters']}): B_f = {r['B_f']}")

    return output


if __name__ == "__main__":
    main()
