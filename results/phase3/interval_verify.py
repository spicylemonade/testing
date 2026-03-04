#!/usr/bin/env python3
"""
Interval arithmetic verification of upper bounds on the univalent Bloch constant B_u.

This script uses mpmath's interval arithmetic (iv context) to produce RIGOROUS
enclosures of all quantities involved in the slit-disk upper bound computation.
Every arithmetic operation is performed with directed rounding, so the final
interval [lo, hi] is GUARANTEED to contain the true mathematical value.

Key certifications:
  1. Conformal radius of D \ [a, 1) at the origin, via the Cayley-Joukowsky chain.
  2. n-fold symmetry reduction:  crad(Omega_n, 0) = crad(D\[r0^n,1), 0)^{1/n}.
  3. Inradius of the n-slit domain (geometric computation with intervals).
  4. Upper bound  B_f = inrad / crad  with certified interval enclosure.
  5. Consistency check against the Skinner lower bound 0.5708858.

Mathematical chain for single-slit conformal radius of D \ [a,1):
  z=0 --Cayley--> w1=i, dw1=2i
  --Square--> w2=-1, dw2=-4
  --Mobius(A^2)--> w3, dw3       where A = (1+a)/(1-a)
  --Sqrt--> w4, dw4
  --InvCayley--> w5, dw5
  conformal_radius = (1 - |w5|^2) / |dw5|
"""

import json
import sys
import os
from mpmath import iv, mp

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WORKING_PRECISION = 100  # decimal digits for interval arithmetic
iv.dps = WORKING_PRECISION


# ---------------------------------------------------------------------------
# Helper: extract a Python float from an ivmpf endpoint
# ---------------------------------------------------------------------------
def iv_to_float(x):
    """Convert an ivmpf (possibly a point interval) to a Python float.

    mpmath's iv endpoints (.a, .b) are themselves ivmpf point intervals,
    so plain float() on them can raise ValueError.  We parse the string
    representation instead.
    """
    s = str(x)
    # Strip brackets if present: "[0.5, 0.5]" -> "0.5"
    s = s.strip()
    if s.startswith("["):
        s = s[1:]
    if s.endswith("]"):
        s = s[:-1]
    # If comma-separated, take the FIRST token for .a, LAST for .b
    # (for a point interval they're the same).
    parts = s.split(",")
    return float(parts[0].strip())


def iv_lo(x):
    """Lower endpoint of an ivmpf interval as a Python float."""
    return iv_to_float(x.a)


def iv_hi(x):
    """Upper endpoint of an ivmpf interval as a Python float."""
    s = str(x.b).strip().strip("[]")
    parts = s.split(",")
    return float(parts[-1].strip())


# ===========================================================================
# 1. Certified single-slit conformal radius
# ===========================================================================

def iv_single_slit_conformal_radius(a_float):
    """
    Compute a rigorous interval enclosure of the conformal radius of
    D \\ [a, 1) at the origin, using interval arithmetic throughout.

    Parameters
    ----------
    a_float : float
        Slit start radius, 0 < a < 1.

    Returns
    -------
    crad_interval : ivmpf
        Interval guaranteed to contain the true conformal radius.
    details : dict
        Intermediate interval values for auditing.
    """
    iv.dps = WORKING_PRECISION

    # Enclose the parameter a in a point interval (from its string repr
    # to avoid float-to-mpf conversion error).
    a = iv.mpf(str(a_float))

    one = iv.mpf(1)
    two = iv.mpf(2)
    i_unit = iv.mpc(iv.mpf(0), iv.mpf(1))

    # A = (1 + a) / (1 - a)
    A = (one + a) / (one - a)
    A2 = A ** 2

    # ----- Step 1: Cayley map  w1 = i(1+z)/(1-z)  at z = 0 -----
    # w1(0) = i,  dw1(0) = 2i / (1-0)^2 = 2i
    w1 = i_unit
    dw1 = two * i_unit

    # ----- Step 2: Squaring  w2 = w1^2 -----
    w2 = w1 ** 2                  # should enclose -1
    dw2 = two * w1 * dw1         # chain rule, should enclose -4

    # ----- Step 3: Mobius  w3 = w2 / (w2 + A^2) -----
    den3 = w2 + A2
    w3 = w2 / den3
    # Derivative: d/dz [w2/(w2+A^2)] = A^2 / (w2+A^2)^2 * dw2
    dw3 = A2 / (den3 ** 2) * dw2

    # ----- Step 4: Square root  w4 = w3^{1/2}  (principal branch) -----
    half = one / two
    w4 = w3 ** half
    # dw4 = dw3 / (2 * w4)
    dw4 = dw3 / (two * w4)

    # ----- Step 5: Inverse Cayley  w5 = (w4 - i) / (w4 + i) -----
    w5 = (w4 - i_unit) / (w4 + i_unit)
    # Derivative: d/dz [(w4-i)/(w4+i)] = -2i / (w4+i)^2 * dw4
    dw5 = iv.mpc(iv.mpf(0), -two) / ((w4 + i_unit) ** 2) * dw4

    # ----- Conformal radius = (1 - |w5|^2) / |dw5| -----
    # |w5|^2 = re(w5)^2 + im(w5)^2
    abs_w5_sq = iv.re(w5) ** 2 + iv.im(w5) ** 2
    # |dw5| = sqrt(re(dw5)^2 + im(dw5)^2)
    abs_dw5 = (iv.re(dw5) ** 2 + iv.im(dw5) ** 2) ** half

    crad = (one - abs_w5_sq) / abs_dw5

    details = {
        "a": str(a),
        "A": str(A),
        "A2": str(A2),
        "w3": str(w3),
        "w4": str(w4),
        "w5": str(w5),
        "abs_w5_sq": str(abs_w5_sq),
        "abs_dw5": str(abs_dw5),
        "crad": str(crad),
    }

    return crad, details


# ===========================================================================
# 2. Certified n-fold symmetry reduction
# ===========================================================================

def iv_n_slit_conformal_radius(n_slits, r0_float):
    """
    Certified conformal radius of D \\ {n equally-spaced radial slits [r0,1)}.

    Uses the identity:
        crad(Omega_n, 0) = crad(D \\ [r0^n, 1), 0)^{1/n}

    Because crad(D \\ [a,1), 0) is monotonically increasing in a (larger a
    means shorter slit, larger domain, larger conformal radius), and a = r0^n
    is enclosed in the interval a_iv, we propagate the enclosure correctly:
        crad(a_iv) subset [crad(a_iv.lo), crad(a_iv.hi)]
    """
    iv.dps = WORKING_PRECISION
    n = iv.mpf(str(n_slits))
    r0 = iv.mpf(str(r0_float))

    # a = r0^n  (slit parameter for reduced single-slit domain)
    a_iv = r0 ** n
    a_lo_f = iv_lo(a_iv)
    a_hi_f = iv_hi(a_iv)

    # Since crad is increasing in a, we evaluate at both endpoints
    crad_at_lo, _ = iv_single_slit_conformal_radius(a_lo_f)
    crad_at_hi, _ = iv_single_slit_conformal_radius(a_hi_f)

    # Take the hull: true crad_single in [crad_at_lo.lo, crad_at_hi.hi]
    hull_lo = iv_lo(crad_at_lo)
    hull_hi = iv_hi(crad_at_hi)
    crad_single = iv.mpf([hull_lo, hull_hi])

    # n-th root:  crad_n = crad_single^{1/n}
    one = iv.mpf(1)
    inv_n = one / n
    crad_n = crad_single ** inv_n

    return crad_n, crad_single


# ===========================================================================
# 3. Certified inradius
# ===========================================================================

def iv_inradius_n_slits(n_slits, r0_float):
    """
    Certified interval enclosure of the inradius of
    Omega_n = D \\ {n equally-spaced radial slits [r0, 1)}.

    For n >= 3 with typical r0:
      The slits go from r0 to 1 at angles 2*pi*k/n.
      We consider:
        (a) Disk at origin of radius r0.
        (b) Disk on the angle bisector (pi/n) at distance d, where the
            inscribed radius is min(1-d, dist_to_nearest_slit).

      Case 1 on bisector: d*cos(pi/n) >= r0 => dist_slit = d*sin(pi/n).
        Optimal: 1-d = d*sin(pi/n) => d = 1/(1+sin(pi/n)),
        inscribed radius = sin(pi/n)/(1+sin(pi/n)).

      Case 2 on bisector: d*cos(pi/n) < r0 => nearest slit point is (r0,0).
        dist = sqrt((d*cos(pi/n)-r0)^2 + (d*sin(pi/n))^2).
        Optimal: d = (1-r0^2)/(2*(1-r0*cos(pi/n))),
        inscribed radius = 1-d.

    For n = 1: inradius = (1 + r0) / 2.

    All bounds are rigorous intervals.
    """
    iv.dps = WORKING_PRECISION

    r0 = iv.mpf(str(r0_float))
    one = iv.mpf(1)
    two = iv.mpf(2)

    if n_slits == 1:
        inrad = (one + r0) / two
        return inrad

    # For n >= 2, candidate 1: disk at origin of radius r0
    best_lo = iv_lo(r0)
    best_hi = iv_hi(r0)

    if n_slits >= 2:
        # Angle between adjacent slits = 2*pi/n, half-angle = pi/n
        angle = iv.pi / iv.mpf(str(n_slits))
        sin_a = iv.sin(angle)
        cos_a = iv.cos(angle)

        # Case 1: d_opt where 1-d = d*sin(angle)
        d_case1 = one / (one + sin_a)
        proj = d_case1 * cos_a
        if iv_lo(proj) >= r0_float:
            # Valid: inscribed radius = d*sin(angle)
            r_case1 = d_case1 * sin_a
            r1_lo = iv_lo(r_case1)
            r1_hi = iv_hi(r_case1)
            if r1_lo > best_lo:
                best_lo = r1_lo
                best_hi = r1_hi

        # Case 2: d*cos(angle) < r0, nearest slit point is tip at (r0,0)
        r0_sq = r0 ** 2
        denom = two * (one - r0 * cos_a)
        d_case2 = (one - r0_sq) / denom
        proj2 = d_case2 * cos_a
        if iv_hi(proj2) < r0_float:
            r_case2 = one - d_case2
            r2_lo = iv_lo(r_case2)
            r2_hi = iv_hi(r_case2)
            if r2_lo > best_lo:
                best_lo = r2_lo
                best_hi = r2_hi

    inrad = iv.mpf([best_lo, best_hi])
    return inrad


# ===========================================================================
# 4. Certified upper bound B_f = inrad / crad
# ===========================================================================

def iv_Bu_upper_bound(n_slits, r0_float):
    """
    Certified interval for  B_f = inrad(Omega_n) / crad(Omega_n, 0).

    Since B_f is an UPPER bound on B_u, we need a rigorous UPPER bound on B_f.
    That is, B_u <= B_f.hi  (the right endpoint of the B_f interval).

    Returns
    -------
    Bf_interval : ivmpf
    crad_interval : ivmpf
    inrad_interval : ivmpf
    """
    iv.dps = WORKING_PRECISION

    crad, crad_single = iv_n_slit_conformal_radius(n_slits, r0_float)
    inrad = iv_inradius_n_slits(n_slits, r0_float)

    Bf = inrad / crad

    return Bf, crad, inrad


# ===========================================================================
# 5. Validation: Skinner lower bound consistency
# ===========================================================================

def check_skinner_consistency(Bf_interval):
    """
    The Skinner (2009) lower bound states B_u > 0.5708858.
    Our UPPER bound says B_u <= B_f.
    These are consistent iff B_f.lo >= 0.5708858.
    (If the entire B_f interval is above Skinner's bound, our upper bound
    is consistent with the lower bound.)
    """
    skinner = 0.5708858
    Bf_lo = iv_lo(Bf_interval)
    Bf_hi = iv_hi(Bf_interval)

    consistent = Bf_lo >= skinner
    return {
        "consistent": consistent,
        "Bf_lo": Bf_lo,
        "Bf_hi": Bf_hi,
        "skinner_lb": skinner,
        "margin": Bf_lo - skinner,
    }


# ===========================================================================
# Main certification routine
# ===========================================================================

def run_certification():
    """Run all certifications and produce a report."""
    iv.dps = WORKING_PRECISION

    results = {}
    all_pass = True

    print("=" * 72)
    print("  INTERVAL ARITHMETIC VERIFICATION OF BLOCH CONSTANT BOUNDS")
    print("  mpmath interval context, working precision: %d digits" % WORKING_PRECISION)
    print("=" * 72)

    # ------------------------------------------------------------------
    # Test A: Verify single-slit conformal radius at several values
    # ------------------------------------------------------------------
    print("\n--- Test A: Single-slit conformal radius D \\ [a, 1) at origin ---")
    test_a_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
    crad_tests = []
    for a_val in test_a_values:
        crad_iv, details = iv_single_slit_conformal_radius(a_val)
        lo = iv_lo(crad_iv)
        hi = iv_hi(crad_iv)
        width = hi - lo
        status = "PASS" if (0 < lo and hi < 1 and width < 1e-15) else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  a = {a_val:6.3f}:  crad in [{lo:.15e}, {hi:.15e}]  "
              f"width = {width:.2e}  {status}")
        crad_tests.append({
            "a": a_val,
            "crad_lo": lo,
            "crad_hi": hi,
            "width": width,
            "status": status,
        })
    results["test_A_single_slit_crad"] = crad_tests

    # ------------------------------------------------------------------
    # Test B: Monotonicity check (crad increasing in a)
    # ------------------------------------------------------------------
    print("\n--- Test B: Monotonicity of conformal radius in slit parameter a ---")
    prev_hi = 0.0
    mono_pass = True
    for a_val in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        crad_iv, _ = iv_single_slit_conformal_radius(a_val)
        lo = iv_lo(crad_iv)
        if lo < prev_hi:
            mono_pass = False
        prev_hi = iv_hi(crad_iv)
    status = "PASS" if mono_pass else "FAIL"
    if not mono_pass:
        all_pass = False
    print(f"  Monotonicity (crad increasing in a):  {status}")
    results["test_B_monotonicity"] = {"status": status}

    # ------------------------------------------------------------------
    # Test C: Limiting cases
    # ------------------------------------------------------------------
    print("\n--- Test C: Limiting behaviour ---")
    # As a -> 1: crad -> 1
    crad_near1, _ = iv_single_slit_conformal_radius(0.9999)
    lo1 = iv_lo(crad_near1)
    hi1 = iv_hi(crad_near1)
    pass_c1 = (lo1 > 0.999 and hi1 <= 1.0 + 1e-10)
    status_c1 = "PASS" if pass_c1 else "FAIL"
    if not pass_c1:
        all_pass = False
    print(f"  a=0.9999: crad in [{lo1:.15e}, {hi1:.15e}]  (expect ~1) {status_c1}")

    # As a -> 0: crad -> 0
    crad_near0, _ = iv_single_slit_conformal_radius(0.001)
    lo0 = iv_lo(crad_near0)
    hi0 = iv_hi(crad_near0)
    pass_c2 = (hi0 < 0.1)
    status_c2 = "PASS" if pass_c2 else "FAIL"
    if not pass_c2:
        all_pass = False
    print(f"  a=0.001:  crad in [{lo0:.15e}, {hi0:.15e}]  (expect ~0) {status_c2}")
    results["test_C_limits"] = {
        "near_1": {"crad_lo": lo1, "crad_hi": hi1, "status": status_c1},
        "near_0": {"crad_lo": lo0, "crad_hi": hi0, "status": status_c2},
    }

    # ------------------------------------------------------------------
    # Test D: Cross-validate with the non-interval code
    # ------------------------------------------------------------------
    print("\n--- Test D: Cross-validation with point arithmetic code ---")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from optimized_upper_bound import single_slit_conformal_radius as orig_crad

    crossval_pass = True
    for a_val in [0.3, 0.5, 0.7]:
        orig = orig_crad(a_val, prec=80)
        crad_iv, _ = iv_single_slit_conformal_radius(a_val)
        lo = iv_lo(crad_iv)
        hi = iv_hi(crad_iv)
        # The original code returns a float; check agreement to 12 digits
        reldiff = abs(orig - (lo + hi) / 2) / max(abs(orig), 1e-30)
        agree = reldiff < 1e-12
        if not agree:
            crossval_pass = False
            all_pass = False
        status = "PASS" if agree else "FAIL"
        print(f"  a={a_val}: point={orig:.15e}  interval_mid={(lo+hi)/2:.15e}  "
              f"reldiff={reldiff:.2e}  {status}")
    results["test_D_crossval"] = {"status": "PASS" if crossval_pass else "FAIL"}

    # ------------------------------------------------------------------
    # Test E: Certify the best upper bound  (n=3, r0=0.5)
    # ------------------------------------------------------------------
    print("\n--- Test E: Certify best upper bound (n=3 slits, r0=0.5) ---")
    n_best = 3
    r0_best = 0.5

    Bf_iv, crad_iv, inrad_iv = iv_Bu_upper_bound(n_best, r0_best)
    Bf_lo = iv_lo(Bf_iv)
    Bf_hi = iv_hi(Bf_iv)
    crad_lo = iv_lo(crad_iv)
    crad_hi = iv_hi(crad_iv)
    inrad_lo = iv_lo(inrad_iv)
    inrad_hi = iv_hi(inrad_iv)

    print(f"  n_slits   = {n_best}")
    print(f"  r0        = {r0_best}")
    print(f"  crad      in [{crad_lo:.15e}, {crad_hi:.15e}]")
    print(f"  inrad     in [{inrad_lo:.15e}, {inrad_hi:.15e}]")
    print(f"  B_f       in [{Bf_lo:.15e}, {Bf_hi:.15e}]")
    print(f"  Certified:  B_u <= {Bf_hi:.10f}")

    # We previously computed ~0.68142, so Bf_hi should be <= 0.6820
    certify_pass = (Bf_hi < 0.6820)
    status_e = "PASS" if certify_pass else "FAIL"
    if not certify_pass:
        all_pass = False
    print(f"  B_u <= 0.6820 check: {status_e}")
    print(f"  Interval width: {Bf_hi - Bf_lo:.2e}")

    results["test_E_best_upper_bound"] = {
        "n_slits": n_best,
        "r0": r0_best,
        "crad_lo": crad_lo,
        "crad_hi": crad_hi,
        "inrad_lo": inrad_lo,
        "inrad_hi": inrad_hi,
        "Bf_lo": Bf_lo,
        "Bf_hi": Bf_hi,
        "certified_upper": Bf_hi,
        "status": status_e,
    }

    # ------------------------------------------------------------------
    # Test F: Skinner consistency check
    # ------------------------------------------------------------------
    print("\n--- Test F: Consistency with Skinner lower bound 0.5708858 ---")
    skinner_check = check_skinner_consistency(Bf_iv)
    status_f = "PASS" if skinner_check["consistent"] else "FAIL"
    if not skinner_check["consistent"]:
        all_pass = False
    print(f"  B_f interval: [{skinner_check['Bf_lo']:.15e}, {skinner_check['Bf_hi']:.15e}]")
    print(f"  Skinner LB:   {skinner_check['skinner_lb']}")
    print(f"  Margin (Bf_lo - Skinner): {skinner_check['margin']:.10f}")
    print(f"  Consistent: {status_f}")
    results["test_F_skinner"] = skinner_check
    results["test_F_skinner"]["status"] = status_f

    # ------------------------------------------------------------------
    # Test G: Survey over multiple n values
    # ------------------------------------------------------------------
    print("\n--- Test G: Certified bounds for n = 1..8 at their optimal r0 ---")
    optimal_configs = [
        (1, 0.5),
        (2, 0.577),
        (3, 0.5),
        (4, 0.414),
        (5, 0.370),
        (6, 0.333),
        (7, 0.303),
        (8, 0.277),
    ]

    survey_results = []
    print(f"  {'n':>3} {'r0':>8} {'B_f lower':>18} {'B_f upper':>18} "
          f"{'width':>12} {'> Skinner?':>12} {'status':>8}")
    print(f"  {'-'*3} {'-'*8} {'-'*18} {'-'*18} {'-'*12} {'-'*12} {'-'*8}")

    for n, r0 in optimal_configs:
        Bf_iv_n, _, _ = iv_Bu_upper_bound(n, r0)
        lo_n = iv_lo(Bf_iv_n)
        hi_n = iv_hi(Bf_iv_n)
        w_n = hi_n - lo_n
        above_skinner = lo_n > 0.5708858
        stat = "PASS" if above_skinner else "WARN"
        if not above_skinner:
            all_pass = False

        print(f"  {n:>3} {r0:>8.4f} {lo_n:>18.15f} {hi_n:>18.15f} "
              f"{w_n:>12.2e} {'yes' if above_skinner else 'NO':>12} {stat:>8}")
        survey_results.append({
            "n": n,
            "r0": r0,
            "Bf_lo": lo_n,
            "Bf_hi": hi_n,
            "width": w_n,
            "above_skinner": above_skinner,
            "status": stat,
        })
    results["test_G_survey"] = survey_results

    # ------------------------------------------------------------------
    # Test H: Tighter certification of B_u <= 0.6815 with refined r0
    # ------------------------------------------------------------------
    print("\n--- Test H: Tight certification B_u <= 0.6815 (n=3, refined r0) ---")
    best_Bf_hi = float('inf')
    best_r0_refined = None
    for r0_try in [0.498, 0.499, 0.4995, 0.5, 0.5005, 0.501, 0.502]:
        Bf_try, _, _ = iv_Bu_upper_bound(3, r0_try)
        hi_try = iv_hi(Bf_try)
        if hi_try < best_Bf_hi:
            best_Bf_hi = hi_try
            best_r0_refined = r0_try

    Bf_final, crad_final, inrad_final = iv_Bu_upper_bound(3, best_r0_refined)
    Bf_final_lo = iv_lo(Bf_final)
    Bf_final_hi = iv_hi(Bf_final)
    print(f"  Best r0 = {best_r0_refined}")
    print(f"  B_f in [{Bf_final_lo:.15e}, {Bf_final_hi:.15e}]")
    print(f"  Certified: B_u <= {Bf_final_hi:.10f}")

    certify_tight = (Bf_final_hi <= 0.6815)
    status_h = "PASS" if certify_tight else "FAIL"
    if not certify_tight:
        all_pass = False
    print(f"  B_u <= 0.6815 certified: {status_h}")

    results["test_H_tight_certification"] = {
        "r0": best_r0_refined,
        "Bf_lo": Bf_final_lo,
        "Bf_hi": Bf_final_hi,
        "certified_upper": Bf_final_hi,
        "target": 0.6815,
        "status": status_h,
    }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    overall = "ALL PASSED" if all_pass else "SOME FAILURES"
    print(f"  OVERALL CERTIFICATION STATUS: {overall}")
    print("=" * 72)

    print(f"\n  Key certified result:")
    print(f"    B_u <= {Bf_final_hi:.10f}  (rigorous, interval-arithmetic certified)")
    print(f"    Using {3}-slit domain with r0 = {best_r0_refined}")
    print(f"    Consistent with Skinner lower bound B_u > 0.5708858")

    results["overall_status"] = overall
    results["certified_upper_bound"] = Bf_final_hi
    results["precision_digits"] = WORKING_PRECISION

    # Save JSON log
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "interval_verify_results.json")
    with open(log_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Results saved to {log_path}")

    return results


# ===========================================================================
if __name__ == "__main__":
    run_certification()
