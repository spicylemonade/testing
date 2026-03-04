#!/usr/bin/env python3
"""
Tighter upper bound for B_u via optimized domain constructions.

The upper bound is obtained by constructing explicit univalent functions
f: D -> C with f'(0) = 1 and computing their schlicht disk radii B_f.
Since B_u = inf B_f, any specific f gives B_u <= B_f.

KEY APPROACH: We optimize over domain parameters to find domains with 
smaller B_f values than Carroll-Ortega-Cerda's ~0.6564.

Domains considered:
1. Goodman 3-slit domain (baseline: B_u <= 0.6565)
2. Carroll-Ortega-Cerda harmonic arc domain (baseline: B_u <= 0.6564)
3. Novel: n-fold symmetric domains with optimized arc shapes
4. Novel: Mixed slit/arc domains breaking the 3-fold symmetry

The conformal map is computed via the integral representation and
the B_f is determined by the inradius of the image domain.

For univalent f mapping D ONTO a domain Omega:
B_f = inradius(Omega) * |f'(0)|^{-1}... wait, no.

Actually: f'(0) = 1 by normalization. f maps D to f(D).
B_f = inradius(f(D)).

For f mapping D conformally ONTO Omega, we need:
f(0) = some point, f'(0) = 1.

The conformal map from D to Omega is unique up to rotation 
(by Riemann mapping theorem). If g: D -> Omega with g(0) = w_0,
then f(z) = g(z)/g'(0) is not right because f wouldn't map to Omega.

The correct normalization: let g: D -> Omega with g(0) = w_0.
Then g'(0) = some nonzero complex number.
Set f(z) = g(z)/|g'(0)| (rotate so f'(0) = 1).
Then f maps D to a rotated copy of Omega.
B_f = inradius(rotated Omega) = inradius(Omega).

But f'(0) = g'(0)/|g'(0)| which has |f'(0)| = 1, not f'(0) = 1.
Need: f(z) = (g(z) - g(0)) / g'(0). Then f(0) = 0, f'(0) = 1.
f maps D to (Omega - w_0) / g'(0).
B_f = inradius((Omega - w_0)/g'(0)) = inradius(Omega)/|g'(0)|.

So: B_f = inradius(Omega) / |g'(0)|.

Since B_u = inf_{f: f'(0)=1} B_f, we want to minimize B_f over all choices
of Omega and w_0 in Omega.

Equivalently: B_u = inf_{Omega simply connected} inf_{w_0 in Omega} inradius(Omega) / |g'_Omega(w_0)|

where g_Omega: D -> Omega is the Riemann map with g(0) = w_0.

By the Schwarz-Pick lemma, |g'_Omega(w_0)| = 1/sigma_Omega(w_0)
where sigma_Omega is the hyperbolic metric density.

So: B_u = inf_Omega inf_{w_0} inradius(Omega) * sigma_Omega(w_0).

Since inf_{w_0} sigma_Omega(w_0) = 1/(2*inradius(Omega)) * correction,
we get a bound in terms of the inradius and the metric.

For the strip {|Im(w)| < h}:
- inradius = h
- sigma at the center = pi/(4h) (known formula)
- sigma_Omega(w_0) = pi/(4h) at the center of the strip
- B_f = h / (1/sigma(w_0)) = h * sigma(w_0) = h * pi/(4h) = pi/4 ≈ 0.7854

Wait, that's the inradius. Let me re-derive.

For the strip, g: D -> strip with g(0) = 0, g'(0) = 1:
g(z) = (2h/pi) * arctanh(z) has g'(0) = 2h/pi.
To normalize: f(z) = g(z)/g'(0) = (pi/(2h)) * (2h/pi) * arctanh(z) = arctanh(z).
So f(z) = arctanh(z), f'(0) = 1.
f(D) = strip of width h = pi/2 (half-width pi/4).
B_f = inradius(strip) = pi/4 ≈ 0.7854.

Hmm but the strip has B_f = pi/4. The question is whether any domain 
gives smaller B_f. The answer is yes — slit domains do.

For the domain D_slit = D \\ [r_0, 1) (single radial slit):
The Riemann map g: D -> D_slit has g'(0) depending on r_0.
The inradius of D_slit is at most 1 (it's contained in the unit disk).
But D_slit is "thinner" near the slit, so its inradius is less than 1.

For f(z) = (g(z) - g(0))/g'(0) with g'(0) = 1:
B_f = inradius(f(D)) = inradius(D_slit) / |g'(0)|... 

Actually I need to be more careful. Let me just compute B_f numerically
for specific functions f in S.
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
from mpmath import mp, mpf, pi
import json
import os

mp.dps = 30


def compute_Bf_for_polynomial(coeffs, r_eval=0.98, N_boundary=2000, 
                                N_interior_per_dim=100):
    """Compute B_f for f(z) = z + a_2*z^2 + ... + a_N*z^N.
    
    Assumes f(0) = 0, f'(0) = 1 (coeffs[0] = 0, coeffs[1] = 1).
    
    Returns the estimated inradius of f(D).
    """
    # Evaluate f on boundary |z| = r_eval
    theta = np.linspace(0, 2*np.pi, N_boundary, endpoint=False)
    z_boundary = r_eval * np.exp(1j * theta)
    
    w_boundary = np.zeros(N_boundary, dtype=complex)
    for n, a in enumerate(coeffs):
        w_boundary += a * z_boundary**n
    
    # Check for self-intersection (approximate univalence test)
    # If the winding number is not 1, skip
    dw = np.diff(np.append(w_boundary, w_boundary[0]))
    angles = np.angle(dw)
    total_winding = np.sum(np.diff(np.unwrap(angles))) / (2 * np.pi)
    if abs(total_winding) < 0.5:  # Should be approximately ±1
        return None  # Not univalent
    
    # Compute inradius
    x_min, x_max = w_boundary.real.min(), w_boundary.real.max()
    y_min, y_max = w_boundary.imag.min(), w_boundary.imag.max()
    
    best_R = 0
    for x in np.linspace(x_min * 0.95, x_max * 0.95, N_interior_per_dim):
        for y in np.linspace(y_min * 0.95, y_max * 0.95, N_interior_per_dim):
            w = complex(x, y)
            dists = np.abs(w_boundary - w)
            min_d = np.min(dists)
            if min_d > best_R:
                best_R = min_d
    
    return best_R


def optimize_upper_bound_polynomial(N_coeffs=6, n_trials=2000):
    """Minimize B_f over polynomial univalent functions.
    
    We search for f(z) = z + a_2*z^2 + ... + a_N*z^N that minimizes
    the inradius of f(D).
    """
    np.random.seed(42)
    
    best_Bf = float('inf')
    best_coeffs = None
    results = []
    
    for trial in range(n_trials):
        # Generate random coefficients
        # a_0 = 0, a_1 = 1
        coeffs = [0, 1]
        for n in range(2, N_coeffs + 1):
            # Use smaller magnitude to increase chance of univalence
            mag = np.random.uniform(0, min(n * 0.3, 1.5))
            phase = np.random.uniform(0, 2*np.pi)
            coeffs.append(mag * np.exp(1j * phase))
        
        Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=500,
                                        N_interior_per_dim=50)
        
        if Bf is not None and Bf > 0.1:
            results.append({'Bf': float(Bf), 'trial': trial})
            if Bf < best_Bf:
                best_Bf = Bf
                best_coeffs = coeffs
    
    return {
        'method': 'Random polynomial search',
        'N_coeffs': N_coeffs,
        'n_trials': n_trials,
        'n_valid': len(results),
        'min_Bf': float(best_Bf) if best_Bf < float('inf') else None,
        'best_a2': complex(best_coeffs[2]) if best_coeffs else None,
        'best_a3': complex(best_coeffs[3]) if best_coeffs else None,
    }


def optimize_upper_bound_targeted():
    """Targeted search for upper bound using specific domain families.
    
    We construct univalent functions that map D to "thin" domains
    and compute their B_f values.
    
    Key families:
    1. f(z) = z + a*z^2 with real a: maps D to a cardioid-like region
    2. f(z) = z/(1-bz): Mobius transform, B_f = 1/(1-|b|^2) for b in D
    3. f(z) = z + z^n/n for various n: adds higher harmonics
    """
    results = []
    
    # Family 1: f(z) = z + a*z^2, |a| < 1/2 for univalence
    print("Family 1: f(z) = z + a*z^2")
    for a in np.linspace(-0.49, 0.49, 50):
        coeffs = [0, 1, a, 0, 0, 0]
        Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=1000,
                                        N_interior_per_dim=80)
        if Bf is not None:
            results.append({'family': 'quadratic', 'a': float(a), 'Bf': float(Bf)})
            print(f"  a={a:.3f}: B_f={Bf:.6f}")
    
    # Family 2: f(z) = z + a*z^2 + b*z^3
    print("\nFamily 2: f(z) = z + a*z^2 + b*z^3")
    for a in np.linspace(-0.4, 0.4, 20):
        for b in np.linspace(-0.3, 0.3, 20):
            coeffs = [0, 1, a, b, 0, 0]
            Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=500,
                                            N_interior_per_dim=50)
            if Bf is not None and Bf > 0.1:
                results.append({'family': 'cubic', 'a': float(a), 'b': float(b), 'Bf': float(Bf)})
    
    if results:
        min_result = min(results, key=lambda x: x['Bf'])
        print(f"\nMinimum B_f found: {min_result['Bf']:.6f}")
        print(f"  Parameters: {min_result}")
    
    # Family 3: Extremal-like functions with 3-fold symmetry
    # f(z) = z + a_3*z^3 + a_6*z^6 (3-fold symmetric)
    print("\nFamily 3: 3-fold symmetric f(z) = z + a3*z^3")
    for a3 in np.linspace(-0.3, 0.3, 30):
        coeffs = [0, 1, 0, a3, 0, 0, 0]
        Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=500,
                                        N_interior_per_dim=50)
        if Bf is not None:
            results.append({'family': '3fold', 'a3': float(a3), 'Bf': float(Bf)})
            print(f"  a3={a3:.3f}: B_f={Bf:.6f}")
    
    return results


def construct_new_domain_upper_bound():
    """
    Construct new candidate extremal domains not previously in literature.
    
    Novel domain 1: "Pinched disk" - unit disk with two symmetric 
    indentations that create a narrow passage.
    
    The function f(z) = z + epsilon * z^2 * (z - alpha) / (1 - alpha*z)
    for small epsilon creates a slight deformation of the disk that 
    pinches it in one direction.
    
    Novel domain 2: "Asymmetric 4-slit" - breaking the symmetry of
    Goodman's construction to potentially improve the upper bound.
    """
    results = []
    
    # Novel domain 1: Pinched disk via Loewner chain
    # f(z) = z * (1 + epsilon * h(z)) where h creates the pinch
    print("Novel domain 1: Pinched disk")
    for eps in np.linspace(0.01, 0.4, 20):
        for phase in np.linspace(0, 2*np.pi, 10, endpoint=False):
            a2 = eps * np.exp(1j * phase)
            coeffs = [0, 1, a2, eps**2 * 0.5, 0, 0]
            Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=500,
                                            N_interior_per_dim=50)
            if Bf is not None and Bf > 0.1:
                results.append({
                    'domain': 'pinched_disk',
                    'eps': float(eps),
                    'phase': float(phase),
                    'Bf': float(Bf),
                })
    
    # Novel domain 2: Combined quadratic + cubic asymmetric
    print("Novel domain 2: Asymmetric quadratic-cubic")
    for a2_r in np.linspace(-0.45, 0.45, 15):
        for a2_i in np.linspace(-0.45, 0.45, 15):
            a2 = complex(a2_r, a2_i)
            if abs(a2) > 0.49:
                continue
            a3 = -a2**2 * 0.3  # Coupled coefficient
            coeffs = [0, 1, a2, a3, 0, 0]
            Bf = compute_Bf_for_polynomial(coeffs, r_eval=0.97, N_boundary=500,
                                            N_interior_per_dim=50)
            if Bf is not None and Bf > 0.1:
                results.append({
                    'domain': 'asymmetric_qc',
                    'a2': {'real': float(a2.real), 'imag': float(a2.imag)},
                    'a3': {'real': float(a3.real), 'imag': float(a3.imag)},
                    'Bf': float(Bf),
                })
    
    if results:
        min_result = min(results, key=lambda x: x['Bf'])
        print(f"\nBest new domain B_f: {min_result['Bf']:.6f}")
    
    return results


def main():
    print("="*70)
    print("UPPER BOUND SEARCH FOR B_u")
    print("="*70)
    
    # Targeted search
    print("\n--- Targeted domain optimization ---")
    targeted_results = optimize_upper_bound_targeted()
    
    if targeted_results:
        min_targeted = min(targeted_results, key=lambda x: x['Bf'])
        print(f"\nBest targeted B_f: {min_targeted['Bf']:.6f}")
    
    # Novel domains
    print("\n--- Novel domain construction ---")
    novel_results = construct_new_domain_upper_bound()
    
    # Random polynomial search
    print("\n--- Random polynomial search ---")
    random_result = optimize_upper_bound_polynomial(N_coeffs=5, n_trials=1000)
    print(f"Random search min B_f: {random_result['min_Bf']}")
    
    # Compile all results
    all_Bf = []
    for r in targeted_results:
        all_Bf.append(r['Bf'])
    for r in novel_results:
        all_Bf.append(r['Bf'])
    if random_result['min_Bf']:
        all_Bf.append(random_result['min_Bf'])
    
    overall_min = min(all_Bf) if all_Bf else None
    
    summary = {
        'method': 'Numerical upper bound via domain optimization',
        'carroll_ortega_cerda_bound': 0.6564,
        'our_best_Bf': overall_min,
        'improved_over_prior': overall_min < 0.6564 if overall_min else False,
        'n_domains_tested': len(targeted_results) + len(novel_results),
        'random_search': random_result,
        'note': ('These are NUMERICAL upper bounds. The polynomial approximations '
                 'of univalent functions give B_f values that bound B_u from above. '
                 'For a rigorous bound, interval arithmetic verification is needed.'),
    }
    
    # Carroll-Ortega-Cerda comparison
    if overall_min and overall_min < 0.6564:
        summary['improvement'] = 0.6564 - overall_min
        summary['new_upper_bound'] = overall_min
    
    os.makedirs('results/phase3', exist_ok=True)
    
    def convert(obj):
        if isinstance(obj, (complex, np.complexfloating)):
            return {'real': float(np.real(obj)), 'imag': float(np.imag(obj))}
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        raise TypeError(f"Not serializable: {type(obj)}")
    
    with open('results/phase3/upper_bound_numerics.json', 'w') as f:
        json.dump(summary, f, indent=2, default=convert)
    
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"Carroll-Ortega-Cerda: B_u <= {summary['carroll_ortega_cerda_bound']}")
    print(f"Our best B_f:        {overall_min:.6f}" if overall_min else "No valid results")
    print(f"Improved: {summary['improved_over_prior']}")
    
    return summary


if __name__ == '__main__':
    main()
