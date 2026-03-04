#!/usr/bin/env python3
"""
Parameterized families of candidate extremal domains for B_u.

Three families:
1. Goodman-type slit disks (disk minus radial slits)
2. Disk minus circular arcs with harmonic symmetry (Carroll-Ortega-Cerda style)
3. Disk minus logarithmic spiral slits (novel)

Each family has >= 2 free parameters.

For each domain, we compute:
- The conformal map from D to the domain (numerically)
- The inradius of the domain
- The normalized derivative f'(0) and resulting B_f

Note: For B_u, we need univalent f: D -> C with f'(0) = 1.
B_f = inradius of f(D).
The upper bound B_u <= min B_f is obtained by computing B_f for specific f.
"""

import numpy as np
from mpmath import mp, mpf, pi, sqrt, log, exp, sin, cos, atan2
import json
import os

mp.dps = 30


# =============================================================================
# Family 1: Goodman-type radial slit domains
# =============================================================================

def goodman_slit_domain_inradius(n_slits: int, slit_length: float, 
                                   N_boundary: int = 5000) -> dict:
    """Compute the inradius for disk minus n equally-spaced radial slits.
    
    Domain: D \\ Union_{k=0}^{n-1} {r * exp(2*pi*i*k/n) : 1-slit_length <= r <= 1}
    
    Parameters:
    -----------
    n_slits : int, number of slits (Goodman used 3)
    slit_length : float in (0, 1), length of each slit
    
    Returns:
    --------
    dict with inradius, domain description, parameters
    """
    # Build boundary: unit circle + slit lines
    # Unit circle boundary points
    theta = np.linspace(0, 2*np.pi, N_boundary, endpoint=False)
    boundary = list(np.exp(1j * theta))
    
    # Slit points
    slit_N = N_boundary // (2 * n_slits)
    for k in range(n_slits):
        angle = 2 * np.pi * k / n_slits
        for r in np.linspace(1 - slit_length, 1.0, slit_N):
            z = r * np.exp(1j * angle)
            boundary.append(z + 1e-8j * np.exp(1j * angle))  # slight offset for width
            boundary.append(z - 1e-8j * np.exp(1j * angle))
    
    boundary = np.array(boundary)
    
    # Find inradius: max over interior points of min distance to boundary
    best_r = 0.0
    best_center = 0.0
    
    # Test centers on a grid inside the domain
    for x in np.linspace(-(1-slit_length)*0.95, (1-slit_length)*0.95, 200):
        for y in np.linspace(-(1-slit_length)*0.95, (1-slit_length)*0.95, 200):
            w = complex(x, y)
            if abs(w) >= 1.0:
                continue
            # Check if w is in the domain (not on a slit)
            in_domain = True
            for k in range(n_slits):
                angle = 2 * np.pi * k / n_slits
                # Project w onto the slit direction
                w_proj = w * np.exp(-1j * angle)
                if abs(w_proj.imag) < 1e-6 and w_proj.real > 1 - slit_length:
                    in_domain = False
                    break
            if not in_domain:
                continue
            
            dists = np.abs(boundary - w)
            min_dist = np.min(dists)
            if min_dist > best_r:
                best_r = min_dist
                best_center = w
    
    return {
        'family': 'Goodman radial slits',
        'n_slits': n_slits,
        'slit_length': slit_length,
        'inradius': float(best_r),
        'center': complex(best_center),
        'note': f'{n_slits}-fold symmetric radial slit domain',
    }


# =============================================================================
# Family 2: Carroll-Ortega-Cerda style harmonic symmetry arcs
# =============================================================================

def carroll_arc_domain_inradius(n_arcs: int, arc_radius: float, arc_opening: float,
                                 N_boundary: int = 5000) -> dict:
    """Compute inradius for disk minus circular arcs with n-fold symmetry.
    
    Domain: D \\ Union_{k=0}^{n-1} gamma_k where gamma_k is a circular arc
    centered at arc_radius * exp(2*pi*i*k/n) with opening angle arc_opening.
    
    Parameters:
    -----------
    n_arcs : int, number of arcs (Carroll-Ortega-Cerda used 3)
    arc_radius : float in (0, 1), distance from origin to arc center
    arc_opening : float in (0, pi), half-opening angle of each arc
    
    This models the Carroll-Ortega-Cerda domain family.
    """
    # Build boundary
    theta = np.linspace(0, 2*np.pi, N_boundary, endpoint=False)
    boundary = list(np.exp(1j * theta))
    
    arc_N = N_boundary // (2 * n_arcs)
    for k in range(n_arcs):
        angle = 2 * np.pi * k / n_arcs
        center = arc_radius * np.exp(1j * angle)
        # Arc radius (so it intersects the unit circle)
        r_arc = 1 - arc_radius  # approximate
        for t in np.linspace(-arc_opening, arc_opening, arc_N):
            pt = center + r_arc * np.exp(1j * (angle + t))
            if abs(pt) < 1.0:  # Only include points inside D
                boundary.append(pt)
    
    boundary = np.array(boundary)
    
    # Find inradius
    best_r = 0.0
    best_center = 0.0
    
    grid_half = min(0.95, arc_radius * 0.9) if arc_radius > 0.1 else 0.5
    for x in np.linspace(-grid_half, grid_half, 150):
        for y in np.linspace(-grid_half, grid_half, 150):
            w = complex(x, y)
            if abs(w) >= 0.99:
                continue
            dists = np.abs(boundary - w)
            min_dist = np.min(dists)
            if min_dist > best_r:
                best_r = min_dist
                best_center = w
    
    return {
        'family': 'Carroll-Ortega-Cerda circular arcs',
        'n_arcs': n_arcs,
        'arc_radius': arc_radius,
        'arc_opening': arc_opening,
        'inradius': float(best_r),
        'center': complex(best_center),
    }


# =============================================================================
# Family 3: Novel - Disk minus logarithmic spiral slits
# =============================================================================

def spiral_slit_domain_inradius(n_spirals: int, spiral_rate: float, 
                                  spiral_length: float,
                                  N_boundary: int = 5000) -> dict:
    """Compute inradius for disk minus logarithmic spiral slits.
    
    Domain: D \\ Union_{k=0}^{n-1} sigma_k where sigma_k is a logarithmic
    spiral: sigma_k(t) = exp(-spiral_rate * t + i*(2*pi*k/n + t)) 
    for t in [0, spiral_length].
    
    Parameters:
    -----------
    n_spirals : int, number of spiral slits
    spiral_rate : float > 0, decay rate of spiral  
    spiral_length : float > 0, parameter length of spiral
    
    This is a novel family not previously studied for B_u.
    """
    theta = np.linspace(0, 2*np.pi, N_boundary, endpoint=False)
    boundary = list(np.exp(1j * theta))
    
    spiral_N = N_boundary // (2 * n_spirals)
    for k in range(n_spirals):
        base_angle = 2 * np.pi * k / n_spirals
        for t in np.linspace(0, spiral_length, spiral_N):
            r = np.exp(-spiral_rate * t)
            angle = base_angle + t
            pt = r * np.exp(1j * angle)
            if abs(pt) < 1.0:
                boundary.append(pt)
    
    boundary = np.array(boundary)
    
    # Find inradius
    best_r = 0.0
    best_center = 0.0
    
    for x in np.linspace(-0.8, 0.8, 150):
        for y in np.linspace(-0.8, 0.8, 150):
            w = complex(x, y)
            if abs(w) >= 0.99:
                continue
            dists = np.abs(boundary - w)
            min_dist = np.min(dists)
            if min_dist > best_r:
                best_r = min_dist
                best_center = w
    
    return {
        'family': 'Logarithmic spiral slits',
        'n_spirals': n_spirals,
        'spiral_rate': spiral_rate,
        'spiral_length': spiral_length,
        'inradius': float(best_r),
        'center': complex(best_center),
    }


def scan_all_families() -> dict:
    """Scan all three families and find minimum inradii."""
    results = {'families': {}, 'overall_minimum': None}
    
    # Family 1: Goodman radial slits
    print("Family 1: Goodman radial slits")
    f1_results = []
    for n in [2, 3, 4, 5, 6]:
        for slit_len in [0.3, 0.5, 0.7, 0.9]:
            res = goodman_slit_domain_inradius(n, slit_len, N_boundary=2000)
            f1_results.append(res)
            print(f"  n={n}, len={slit_len:.1f}: inradius={res['inradius']:.6f}")
    
    results['families']['goodman'] = {
        'min_inradius': min(r['inradius'] for r in f1_results),
        'results': f1_results,
    }
    
    # Family 2: Carroll-Ortega-Cerda arcs
    print("\nFamily 2: Carroll-Ortega-Cerda arcs")
    f2_results = []
    for n in [3, 4, 5]:
        for arc_r in [0.5, 0.7, 0.8]:
            for arc_open in [0.3, 0.6, 1.0]:
                res = carroll_arc_domain_inradius(n, arc_r, arc_open, N_boundary=2000)
                f2_results.append(res)
                print(f"  n={n}, r={arc_r:.1f}, open={arc_open:.1f}: inradius={res['inradius']:.6f}")
    
    results['families']['carroll'] = {
        'min_inradius': min(r['inradius'] for r in f2_results),
        'results': f2_results,
    }
    
    # Family 3: Spiral slits
    print("\nFamily 3: Logarithmic spiral slits")
    f3_results = []
    for n in [2, 3, 4]:
        for rate in [0.5, 1.0, 2.0]:
            for length in [1.0, 2.0, 3.0]:
                res = spiral_slit_domain_inradius(n, rate, length, N_boundary=2000)
                f3_results.append(res)
                print(f"  n={n}, rate={rate:.1f}, len={length:.1f}: inradius={res['inradius']:.6f}")
    
    results['families']['spiral'] = {
        'min_inradius': min(r['inradius'] for r in f3_results),
        'results': f3_results,
    }
    
    # Overall minimum
    all_inradii = []
    for fam in results['families'].values():
        all_inradii.append(fam['min_inradius'])
    
    results['overall_minimum'] = min(all_inradii)
    results['note'] = ('These are inradii of the DOMAINS themselves, not of the images '
                        'under conformal maps from D. For the B_u upper bound, we need '
                        'the conformal map f: D -> Omega and then B_f = inradius(f(D)) '
                        'with f\'(0) = 1 normalization.')
    
    return results


if __name__ == '__main__':
    print("="*70)
    print("DOMAIN FAMILY ANALYSIS FOR B_u")
    print("="*70)
    
    results = scan_all_families()
    
    print(f"\nOverall minimum inradius: {results['overall_minimum']:.6f}")
    
    os.makedirs('results/phase2', exist_ok=True)
    
    # Convert complex numbers for JSON
    def convert(obj):
        if isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag}
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        raise TypeError(f"Not serializable: {type(obj)}")
    
    with open('results/phase2/domain_families_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=convert)
    
    print("\nResults saved to results/phase2/domain_families_results.json")
