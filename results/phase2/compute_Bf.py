"""
Numerical computation of B_f for parametric families of univalent functions.

B_f = radius of the largest univalent disk contained in f(D).
For univalent f, this equals the inradius: sup_w d(w, partial f(D)),
where the sup is over all w in f(D) and d is the Euclidean distance to the boundary.

Key insight: For unbounded simply connected domains (Koebe, half-plane), B_f = infinity.
The univalent Bloch constant B_u is the infimum over univalent f with f'(0) = 1.
The interesting extremal functions must have BOUNDED images with finite inradius.

Following Carroll & Ortega-Cerda (2009), the candidate extremal domains are disks
with arcs removed. We focus on such bounded domains plus the standard test cases.
"""

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import ellipk, ellipe
import json
import sys

# =============================================================================
# Core computation: inradius of f(D) for univalent f with bounded image
# =============================================================================

def compute_boundary_points(f, N=4000):
    """
    Compute boundary points of f(D) by evaluating f on |z| = r for r close to 1.
    Uses multiple radii and keeps only finite points.
    """
    radii = [1.0 - 10**(-k) for k in range(3, 8)]
    all_pts = []
    n_per = N // len(radii)
    for r in radii:
        theta = np.linspace(0, 2 * np.pi, n_per, endpoint=False)
        z = r * np.exp(1j * theta)
        pts = f(z)
        mask = np.isfinite(pts)
        all_pts.append(pts[mask])
    return np.concatenate(all_pts)


def compute_inradius_at_point(w, boundary_points):
    """Distance from point w to the closest boundary point."""
    return np.min(np.abs(boundary_points - w))


def compute_Bf(f, N_boundary=6000, N_interior=600, refine=True):
    """
    Compute B_f = inradius(f(D)) = sup_w d(w, partial f(D)).
    
    For bounded domains this is the standard inradius.
    For unbounded domains, returns a large number (effectively infinity).
    """
    boundary = compute_boundary_points(f, N_boundary)
    
    if len(boundary) < 50:
        return float('inf'), 0.0
    
    # Check if domain is bounded
    max_bnd = np.max(np.abs(boundary))
    if max_bnd > 1e6:
        return float('inf'), 0.0
    
    # Grid search over interior points
    best_d = 0.0
    best_w = 0.0 + 0j
    
    radii = np.linspace(0, 0.95, 25)
    n_angles = max(N_interior // 25, 20)
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    
    for r in radii:
        if r == 0:
            z_vals = np.array([0.0 + 0j])
        else:
            z_vals = r * np.exp(1j * angles)
        w_vals = f(z_vals)
        for w in w_vals:
            if not np.isfinite(w):
                continue
            d = compute_inradius_at_point(w, boundary)
            if d > best_d:
                best_d = d
                best_w = w
    
    if not refine:
        return best_d, best_w
    
    # Refine with Nelder-Mead
    def neg_inradius(xy):
        w = xy[0] + 1j * xy[1]
        return -compute_inradius_at_point(w, boundary)
    
    x0 = [best_w.real, best_w.imag]
    result = minimize(neg_inradius, x0, method='Nelder-Mead',
                      options={'xatol': 1e-12, 'fatol': 1e-12, 'maxiter': 5000})
    
    best_d = -result.fun
    best_w = result.x[0] + 1j * result.x[1]
    
    return best_d, best_w


def compute_Bf_bounded(f, R_image, N_boundary=6000, N_interior=600):
    """
    Compute B_f for a function known to map D into D(0, R_image).
    Uses dense boundary sampling and refined optimization.
    """
    boundary = compute_boundary_points(f, N_boundary)
    
    # Also add boundary of D(0, R_image) if the image is contained in it
    theta_extra = np.linspace(0, 2 * np.pi, 1000, endpoint=False)
    circle_bnd = R_image * np.exp(1j * theta_extra)
    
    # Filter: only keep circle points that are actually outside f(D)
    # (approximate: keep all of them as extra boundary)
    boundary = np.concatenate([boundary, circle_bnd])
    
    # Grid search
    best_d = 0.0
    best_w = 0.0 + 0j
    
    radii = np.linspace(0, 0.98, 30)
    n_angles = 30
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    
    for r in radii:
        if r == 0:
            z_vals = np.array([0.0 + 0j])
        else:
            z_vals = r * np.exp(1j * angles)
        w_vals = f(z_vals)
        for w in w_vals:
            if not np.isfinite(w):
                continue
            d = compute_inradius_at_point(w, boundary)
            if d > best_d:
                best_d = d
                best_w = w
    
    # Refine
    def neg_inradius(xy):
        w = xy[0] + 1j * xy[1]
        return -compute_inradius_at_point(w, boundary)
    
    x0 = [best_w.real, best_w.imag]
    result = minimize(neg_inradius, x0, method='Nelder-Mead',
                      options={'xatol': 1e-12, 'fatol': 1e-12, 'maxiter': 5000})
    
    return -result.fun, result.x[0] + 1j * result.x[1]


# =============================================================================
# Parametric families
# =============================================================================

def identity(z):
    """f(z) = z. Image is D. B_f = 1."""
    return z


def koebe(z):
    """
    Koebe function k(z) = z/(1-z)^2.
    Maps D onto C minus (-inf, -1/4]. B_f = infinity (unbounded image).
    """
    return z / (1 - z) ** 2


def koebe_rotated(z, theta=0.0):
    """Rotated Koebe: z / (1 - e^{i*theta} * z)^2. B_f = infinity."""
    return z / (1 - np.exp(1j * theta) * z) ** 2


def convex_function(z, theta=0.0):
    """z / (1 - e^{i*theta} * z). Maps D to a half-plane. B_f = infinity."""
    return z / (1 - np.exp(1j * theta) * z)


def bounded_convex(z, R=2.0):
    """
    A bounded convex univalent function: maps D into a bounded domain.
    f(z) = R * z / (R - z) normalized so f'(0) = 1.
    Actually: f(z) = z / (1 - z/R). f'(0) = 1. f maps D onto D(0, R/(R-1))... 
    Not quite right. Let's use:
    f(z) = R * tanh(z / R) with appropriate normalization.
    """
    # Simple bounded univalent: f(z) = R * (1 - (1 - z/R)) is trivial
    # Better: use a mapping to an ellipse
    # f(z) = z + c*z^2 for small c (still univalent for |c| < 1/2)
    pass


def disk_mapping(z, R=1.0):
    """
    Map D onto D(0, R) conformally with f(0)=0, f'(0)=1.
    This requires R >= 1 to have f'(0) = 1 (scaling).
    For R = 1: f(z) = z (identity). B_f = 1.
    In general: f(z) = R*z maps D to D(0, R) with f'(0) = R.
    To get f'(0) = 1 mapping to D(0, R) we need R = 1, so f = id.
    
    For R < 1: no univalent map from D onto D(0,R) has f'(0) = 1.
    (By Schwarz lemma, |f'(0)| <= R for f: D -> D(0,R), with equality only for rotations.)
    """
    return z  # Only R=1 works with f'(0)=1


def slit_disk_mapping(z, R=0.8, n_slits=2, slit_length=0.3):
    """
    Approximate mapping to a disk of radius R with radial slits removed.
    This is a model for the candidate extremal domains of B_u.
    
    We use a perturbation approach: start with the map to D(0, R) and
    add a correction to create slits.
    
    For proper implementation, we'd need Schwarz-Christoffel or similar.
    Here we approximate using a power series approach.
    
    f(z) = z + sum_{k>=2} a_k z^k, with f univalent and f(D) ≈ D(0,R)\\slits.
    """
    # Simple model: use a polynomial perturbation
    # f(z) = z - c * z^{n_slits+1} which creates n_slits-fold symmetric deformation
    # Choose c to make the image approximately disk-minus-slits
    c = slit_length / (n_slits + 1)
    return z - c * z ** (n_slits + 1)


def strip_mapping(z):
    """
    f(z) = arctanh(z) = (1/2) * log((1+z)/(1-z)).
    Maps D onto the strip {w : |Im(w)| < pi/4}.
    f'(0) = 1.
    B_f = pi/4 ≈ 0.7854 (distance from center of strip to boundary).
    
    Note: This is unbounded in the real direction, but for B_f we need
    the largest inscribed disk, which for a strip of half-width pi/4 is pi/4.
    """
    return np.arctanh(z)


def lens_mapping(z, alpha=np.pi/2):
    """
    Map D onto a lens (intersection of two disks) with opening angle alpha.
    f(z) = ((1+z)^beta - (1-z)^beta) / (2*beta) where beta = 1 - alpha/pi.
    f'(0) = 1. For alpha = pi: identity. For alpha < pi: narrower lens.
    
    The inradius decreases as alpha decreases.
    """
    beta = 1.0 - alpha / np.pi
    if abs(beta) < 1e-10:
        return z
    # Using principal branch
    return ((1 + z)**beta - (1 - z)**beta) / (2 * beta)


def sector_mapping(z, alpha=np.pi):
    """
    Map D onto a sector of opening angle alpha*pi at the origin.
    Standard: f(z) = ((1+z)/(1-z))^alpha - 1, appropriately normalized.
    For alpha = 1: maps to right half-plane (shifted by 1).
    
    We need careful normalization. Let g(z) = ((1+z)/(1-z))^alpha.
    g(0) = 1, g'(0) = 2*alpha.
    So f(z) = (g(z) - 1)/(2*alpha) has f(0) = 0, f'(0) = 1.
    """
    g = ((1 + z) / (1 - z))**alpha
    return (g - 1) / (2 * alpha)


# =============================================================================
# Unit tests
# =============================================================================

def test_identity():
    """Test: B_f(identity) = 1."""
    Bf, center = compute_Bf(identity, N_boundary=6000, N_interior=600)
    print(f"B_f(identity) = {Bf:.8f} (expected: 1.0)")
    assert abs(Bf - 1.0) < 0.01, f"B_f(identity) = {Bf}, expected ~1.0"
    return Bf


def test_koebe():
    """
    Test: B_f(Koebe) is infinite (slit plane domain).
    We verify the distance from origin to the slit tip at -1/4.
    """
    # Check that the slit tip is at -1/4
    # The boundary of the Koebe image near the tip:
    theta = np.linspace(np.pi - 0.1, np.pi + 0.1, 1000)
    r = 1 - 1e-5
    z = r * np.exp(1j * theta)
    w = koebe(z)
    # The minimum real part should be close to -1/4
    min_re = np.min(w.real)
    print(f"Koebe slit tip: min Re(f(z)) = {min_re:.6f} (expected: -0.25)")
    assert abs(min_re - (-0.25)) < 0.01, f"Slit tip at {min_re}, expected -0.25"
    
    # For the normalized definition, B_f(Koebe) = infinity since image is unbounded
    Bf, _ = compute_Bf(koebe)
    print(f"B_f(Koebe) = {Bf} (expected: inf)")
    assert Bf > 100 or Bf == float('inf'), f"B_f(Koebe) should be very large/inf, got {Bf}"
    return float('inf')


def test_strip():
    """
    Test: B_f(arctanh) = pi/4 ≈ 0.7854.
    Strip mapping: D -> strip of half-width pi/4.
    The inradius of the strip is pi/4 (at any point on the real axis).
    
    For the numerical computation, we need to handle the unbounded domain.
    The strip extends to ±infinity along the real axis but has finite width.
    """
    # Analytical: B_f = pi/4
    expected = np.pi / 4
    
    # Numerical check: sample boundary near origin
    # The boundary consists of lines Im(w) = ±pi/4
    boundary_pts = compute_boundary_points(strip_mapping, 6000)
    # Only keep points near the origin (|Re| < 5)
    mask = np.abs(boundary_pts.real) < 5.0
    boundary_pts = boundary_pts[mask]
    
    if len(boundary_pts) > 0:
        d0 = compute_inradius_at_point(0.0, boundary_pts)
        print(f"d(0, boundary) for strip = {d0:.6f} (expected: {expected:.6f})")
        assert abs(d0 - expected) < 0.05, f"d = {d0}, expected {expected}"
    else:
        print("Warning: could not sample strip boundary near origin")
    
    print(f"B_f(strip) = {expected:.8f} (analytical)")
    return expected


def test_slit_disk():
    """Test slit disk mapping gives finite B_f < 1."""
    f = lambda z: slit_disk_mapping(z, R=0.8, n_slits=3, slit_length=0.2)
    Bf, center = compute_Bf(f, N_boundary=6000, N_interior=600)
    print(f"B_f(slit_disk, R=0.8, 3 slits) = {Bf:.8f}")
    assert Bf < 1.0 and Bf > 0.1, f"B_f = {Bf}, expected between 0.1 and 1.0"
    return Bf


def test_lens():
    """Test lens mapping."""
    f = lambda z: lens_mapping(z, alpha=np.pi/2)
    Bf, center = compute_Bf(f, N_boundary=6000, N_interior=600)
    print(f"B_f(lens, alpha=pi/2) = {Bf:.8f}")
    assert 0.1 < Bf < 2.0, f"B_f = {Bf}, expected reasonable value"
    return Bf


def run_all_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("Running unit tests for B_f computation")
    print("=" * 60)
    
    results = {}
    
    print("\n--- Test: Identity function ---")
    results['identity'] = test_identity()
    
    print("\n--- Test: Koebe function ---")
    results['koebe'] = test_koebe()
    
    print("\n--- Test: Strip mapping ---")
    results['strip'] = test_strip()
    
    print("\n--- Test: Slit disk mapping ---")
    results['slit_disk'] = test_slit_disk()
    
    print("\n--- Test: Lens mapping ---")
    results['lens'] = test_lens()
    
    # Additional: polynomial perturbation
    print("\n--- Polynomial perturbation: f(z) = z + 0.4*z^2 ---")
    f_poly = lambda z: z + 0.4 * z**2
    Bf, center = compute_Bf(f_poly, N_boundary=6000, N_interior=600)
    print(f"B_f(z + 0.4*z^2) = {Bf:.8f}")
    results['poly_perturbation'] = Bf
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    
    return results


if __name__ == '__main__':
    results = run_all_tests()
    
    # Convert inf to string for JSON
    json_results = {}
    for k, v in results.items():
        if v == float('inf'):
            json_results[k] = "infinity"
        else:
            json_results[k] = round(v, 8)
    
    print(f"\nSummary: {json.dumps(json_results, indent=2)}")
