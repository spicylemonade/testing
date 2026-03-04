#!/usr/bin/env python3
"""
Numerical computation of B_f for candidate univalent functions.

For a univalent f: D -> C with f'(0) = 1, B_f is the inradius of f(D):
    B_f = sup_{w in f(D)} dist(w, boundary f(D))

Key functions:
- identity: f(z) = z, B_f = 1
- Koebe: f(z) = z/(1-z)^2, f(D) = C \ (-inf, -1/4], B_f = inf (unbounded image)
  BUT the normalized Koebe with f'(0)=1 maps D onto C \ (-inf, -1/4], which has inradius = infinity
  So we consider the *restricted* problem: B_f for the normalized Koebe is infinity.
  For the Koebe function, the disk D(0, 1/4) is the largest disk centered at 0 in f(D),
  but the overall inradius is infinite.

For the univalent Bloch constant problem, we want B_f = inradius of f(D) for f univalent
with f'(0) = 1. The infimum of B_f over such f is B_u.
"""

import numpy as np
from numpy import pi
import sys


def boundary_points(f, n_pts=10000):
    """
    Compute boundary points of f(D) by evaluating f on |z| = r for r close to 1.
    
    Parameters:
        f: callable, the holomorphic function
        n_pts: number of points on the boundary
    
    Returns:
        Array of complex boundary points
    """
    theta = np.linspace(0, 2 * pi, n_pts, endpoint=False)
    r = 1.0 - 1e-10  # approach boundary
    z = r * np.exp(1j * theta)
    return f(z)


def inradius_numerical(f, n_boundary=10000, n_test=5000):
    """
    Compute the inradius of f(D) numerically.
    
    The inradius is sup_{w in f(D)} dist(w, partial f(D)).
    
    We approximate this by:
    1. Sampling boundary of f(D) densely
    2. Testing points inside f(D) for maximum distance to boundary
    
    Parameters:
        f: callable, the holomorphic function
        n_boundary: number of boundary sample points
        n_test: number of interior test points
    
    Returns:
        Approximate inradius and the optimal center
    """
    # Get boundary points
    bpts = boundary_points(f, n_boundary)
    
    # Generate interior test points at various radii
    best_r = 0.0
    best_center = 0.0 + 0.0j
    
    for r_frac in np.linspace(0.0, 0.999, 50):
        n_this = max(100, n_test // 50)
        theta = np.linspace(0, 2 * pi, n_this, endpoint=False)
        z_interior = r_frac * np.exp(1j * theta)
        w_interior = f(z_interior)
        
        for w in w_interior:
            # Distance from w to boundary
            dists = np.abs(bpts - w)
            min_dist = np.min(dists)
            if min_dist > best_r:
                best_r = min_dist
                best_center = w
    
    # Refine around the best center
    for _ in range(5):
        # Search in a small neighborhood
        offsets = np.linspace(-best_r * 0.1, best_r * 0.1, 20)
        for dx in offsets:
            for dy in offsets:
                w = best_center + dx + 1j * dy
                dists = np.abs(bpts - w)
                min_dist = np.min(dists)
                if min_dist > best_r:
                    best_r = min_dist
                    best_center = w
    
    return best_r, best_center


def inradius_identity():
    """
    For f(z) = z, f(D) = D, inradius = 1 (the disk itself is the maximal inscribed disk).
    """
    f = lambda z: z
    return inradius_numerical(f, n_boundary=20000, n_test=10000)


def koebe_function(z):
    """The Koebe function k(z) = z/(1-z)^2."""
    return z / (1 - z) ** 2


def inradius_koebe():
    """
    For the Koebe function k(z) = z/(1-z)^2:
    Image = C \ (-inf, -1/4]
    Inradius = infinity (unbounded domain)
    
    For practical computation on a bounded approximation, 
    the inradius grows without bound as we approach the boundary.
    """
    return float('inf'), 0.0


def slit_disk_function(z, n_slits=3, slit_depth=0.5):
    """
    Approximate conformal map from D onto a slit disk.
    
    We approximate the domain D \ (radial slits) by:
    - Using a polynomial approximation to the conformal map
    - The slits go from radius (1-slit_depth) to 1 at angles 2*pi*k/n_slits
    
    For exact computation, we would need Schwarz-Christoffel mapping.
    Here we use a perturbative approach.
    
    The function f(z) = z * prod_k (1 - c * z^n_slits)^alpha approximately
    maps D onto the slit domain for appropriate c, alpha.
    """
    # Simple model: f(z) = z - epsilon * z^(n_slits+1)
    # This creates a domain with approximate n-fold symmetry
    epsilon = slit_depth * 0.1  # small perturbation
    w = z - epsilon * z ** (n_slits + 1)
    return w


def inradius_slit_disk(n_slits=3, slit_depth=0.5):
    """Compute inradius for a slit-disk mapping."""
    f = lambda z: slit_disk_function(z, n_slits, slit_depth)
    return inradius_numerical(f, n_boundary=20000, n_test=10000)


def compute_Bf_from_boundary(boundary_pts, interior_pts=None):
    """
    Given boundary points of f(D), compute B_f = inradius.
    
    If interior_pts are given, find the point with maximum distance to boundary.
    Otherwise, use the centroid of the boundary as starting point and optimize.
    """
    if interior_pts is None:
        # Use centroid and nearby points
        centroid = np.mean(boundary_pts)
        # Generate a grid of test points
        x_range = np.linspace(np.min(boundary_pts.real), np.max(boundary_pts.real), 100)
        y_range = np.linspace(np.min(boundary_pts.imag), np.max(boundary_pts.imag), 100)
        
        best_r = 0.0
        best_w = centroid
        
        for x in x_range:
            for y in y_range:
                w = x + 1j * y
                dists = np.abs(boundary_pts - w)
                min_dist = np.min(dists)
                if min_dist > best_r:
                    best_r = min_dist
                    best_w = w
        
        return best_r, best_w
    else:
        best_r = 0.0
        best_w = 0.0
        for w in interior_pts:
            dists = np.abs(boundary_pts - w)
            min_dist = np.min(dists)
            if min_dist > best_r:
                best_r = min_dist
                best_w = w
        return best_r, best_w


# ---- Covering theorem approach for lower bound on B_u ----

def growth_lower(r):
    """Growth theorem lower bound: |f(z)| >= r/(1+r)^2 for f in S, |z|=r."""
    return r / (1 + r) ** 2


def growth_upper(r):
    """Growth theorem upper bound: |f(z)| <= r/(1-r)^2 for f in S, |z|=r."""
    return r / (1 - r) ** 2


def distortion_lower(r):
    """Distortion theorem lower bound: |f'(z)| >= (1-r)/(1+r)^3 for f in S, |z|=r."""
    return (1 - r) / (1 + r) ** 3


def distortion_upper(r):
    """Distortion theorem upper bound: |f'(z)| <= (1+r)/(1-r)^3 for f in S, |z|=r."""
    return (1 + r) / (1 - r) ** 3


def covering_radius_koebe(r):
    """
    The image f(D(0,r)) for f in S contains D(0, r/(1+r)^2) by the growth theorem.
    The covering radius from the Koebe theorem for the disk of radius r is:
    B_f(r) >= r/(1+r)^2  (as a lower bound on the inradius of f(D(0,r)))
    """
    return r / (1 + r) ** 2


def lower_bound_basic():
    """
    Basic lower bound on B_u using the Koebe 1/4 theorem.
    
    For any f in S, f(D) contains D(0, 1/4), so B_u >= 1/4.
    But actually B_f = inradius(f(D)) >= 1/4 for f(0) = 0.
    
    More refined: consider f(D(0,r)) for optimal r.
    """
    # The image f(D(0,r)) for f in S, f(0)=0, contains D(0, r/(1+r)^2)
    # Optimal r -> 1 gives the 1/4 theorem
    r_opt = np.linspace(0.01, 0.999, 10000)
    bounds = [covering_radius_koebe(r) for r in r_opt]
    best = max(bounds)
    return best


# ---- Unit tests ----

def test_identity():
    """Test that B_f = 1 for f(z) = z."""
    f = lambda z: z
    r, center = inradius_numerical(f, n_boundary=50000, n_test=20000)
    print(f"Identity: B_f = {r:.8f} (expected 1.000000)")
    assert abs(r - 1.0) < 0.01, f"Identity test failed: got {r}"
    return r


def test_koebe():
    """
    For the Koebe function, the image is C \ (-inf, -1/4].
    The largest disk centered at 0 has radius 1/4.
    But the inradius is infinite (the domain is unbounded).
    
    We verify that the Koebe quarter theorem disk D(0, 1/4) is in the image.
    """
    # Verify that f(z) = z/(1-z)^2 maps D to C \ (-inf, -1/4]
    # The point -1/4 should be on the boundary
    z_boundary = -1.0  # z = -1 maps to k(-1) = -1/4
    val = koebe_function(-1.0 + 0j)
    print(f"Koebe at z=-1: {val:.8f} (expected -0.25)")
    assert abs(val - (-0.25)) < 1e-6
    
    # For the standard B_f definition with the Koebe function,
    # B_f = infinity since the image is unbounded.
    # But the covering radius for D(0, 1/4) centered at 0 is 1/4.
    # The Koebe 1/4 theorem says inradius w.r.t. origin >= 1/4
    print(f"Koebe: B_f = infinity (image is C \\ (-inf, -1/4])")
    return float('inf')


def test_lower_bound():
    """Test the basic lower bound computation."""
    lb = lower_bound_basic()
    print(f"Basic lower bound (Koebe): B_u >= {lb:.8f} (expected 0.25)")
    assert abs(lb - 0.25) < 0.001
    return lb


def run_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("Running unit tests for compute_Bf.py")
    print("=" * 60)
    
    print("\nTest 1: Identity function")
    r_id = test_identity()
    
    print("\nTest 2: Koebe function")
    r_koebe = test_koebe()
    
    print("\nTest 3: Basic lower bound")
    lb = test_lower_bound()
    
    print("\nTest 4: Slit-disk mapping (3 slits)")
    r_slit, center = inradius_slit_disk(n_slits=3, slit_depth=0.3)
    print(f"3-slit disk: B_f = {r_slit:.8f}, center = ({center.real:.4f}, {center.imag:.4f})")
    
    print("\nTest 5: Slit-disk mapping (5 slits)")
    r_slit5, center5 = inradius_slit_disk(n_slits=5, slit_depth=0.3)
    print(f"5-slit disk: B_f = {r_slit5:.8f}, center = ({center5.real:.4f}, {center5.imag:.4f})")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
