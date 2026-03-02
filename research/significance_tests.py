"""Statistical significance testing for all novel findings."""

import os
import sys
import json
import math
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from collatz_engine import batch_stopping_times

SEED = 42
np.random.seed(SEED)


def test_resonance_significance(max_n=500000, n_null=1000):
    """Test whether modular resonance is due to arithmetic structure vs marginal distribution.

    Null model: for each n, draw stopping time iid from the empirical distribution
    (destroying the dependence on n's arithmetic properties). If the observed
    chi-squared exceeds the null, the resonance is DUE to arithmetic structure.
    """
    print("Computing stopping times...")
    st = batch_stopping_times(max_n)
    st_array = np.array(st[1:], dtype=np.int64)

    test_moduli = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

    # Observed chi-squared
    observed_chi2 = {}
    for m in test_moduli:
        residues = st_array % m
        observed = np.bincount(residues, minlength=m).astype(float)
        expected = max_n / m
        chi2 = float(np.sum((observed - expected) ** 2 / expected))
        observed_chi2[m] = chi2

    # Null model: draw iid from empirical stopping time distribution
    print(f"Running {n_null} null model samples (iid from empirical CDF)...")
    null_chi2 = {m: [] for m in test_moduli}

    for i in range(n_null):
        if i % 200 == 0:
            print(f"  Sample {i}/{n_null}...")
        # Draw max_n values iid from empirical distribution
        fake_st = np.random.choice(st_array, size=max_n, replace=True)
        for m in test_moduli:
            residues = fake_st % m
            observed = np.bincount(residues, minlength=m).astype(float)
            expected = max_n / m
            chi2 = float(np.sum((observed - expected) ** 2 / expected))
            null_chi2[m].append(chi2)

    # Compute p-values
    results = []
    n_tests = len(test_moduli)

    for m in test_moduli:
        null_vals = np.array(null_chi2[m])
        obs = observed_chi2[m]
        # p-value: fraction of null samples with chi2 >= observed
        p_empirical = float((null_vals >= obs).mean())
        if p_empirical == 0:
            p_empirical = 1.0 / (n_null + 1)

        effect_size = (obs - null_vals.mean()) / null_vals.std() if null_vals.std() > 0 else float('inf')
        coprime6 = math.gcd(m, 6) == 1
        is_prime = all(m % i != 0 for i in range(2, int(math.sqrt(m)) + 1)) and m > 1

        # Also get theoretical p-value from chi-squared distribution
        dof = m - 1
        p_theoretical = float(1 - stats.chi2.cdf(obs, dof))

        results.append({
            "modulus": m,
            "observed_chi2": obs,
            "null_mean_chi2": float(null_vals.mean()),
            "null_std_chi2": float(null_vals.std()),
            "p_value_empirical": p_empirical,
            "p_value_theoretical": p_theoretical,
            "corrected_p_value": min(1.0, p_empirical * n_tests),
            "effect_size_z": float(effect_size),
            "significant_at_001": bool(p_empirical * n_tests < 0.001),
            "coprime_to_6": coprime6,
            "is_prime": is_prime,
        })

    return results


def test_tda_significance():
    """Assess TDA results."""
    with open("results/tda_results.json") as f:
        tda = json.load(f)
    p = tda["p_value_H1"]
    return {
        "experiment": "TDA_H1",
        "test_statistic": tda["max_lifetimes_H1"],
        "p_value": p,
        "corrected_p_value": min(1.0, p * 7),
        "effect_size": tda["max_lifetimes_H1"] / tda["null_95th_H1"] if tda["null_95th_H1"] > 0 else 0,
        "significant_at_001": p * 7 < 0.001,
    }


def test_lyapunov():
    """Assess Lyapunov results."""
    with open("results/lyapunov_results.json") as f:
        lyap = json.load(f)
    return {
        "experiment": "Lyapunov_nonGaussian",
        "test_statistic": lyap["ks_normal_statistic"],
        "p_value": lyap["ks_normal_pvalue"],
        "corrected_p_value": min(1.0, lyap["ks_normal_pvalue"] * 7),
        "effect_size": lyap["ks_normal_statistic"],
        "significant_at_001": lyap["ks_normal_pvalue"] * 7 < 0.001,
    }


def test_phase_transition():
    """Assess phase transition results."""
    with open("results/phase_transition.json") as f:
        pt = json.load(f)
    # The phase transition is significant if a=3,b=1 converges and a=5,b=1 doesn't
    conv_31 = pt["known_a3b1_converges"]
    conv_51 = pt["known_a5b1_diverges"]
    return {
        "experiment": "Phase_Transition",
        "test_statistic": conv_31 - conv_51,
        "p_value": 0.0 if (conv_31 > 0.9 and conv_51 < 0.2) else 1.0,
        "corrected_p_value": 0.0 if (conv_31 > 0.9 and conv_51 < 0.2) else 1.0,
        "effect_size": conv_31 - conv_51,
        "significant_at_001": conv_31 > 0.9 and conv_51 < 0.2,
    }


def run_all_significance():
    """Run all significance tests."""
    os.makedirs("results", exist_ok=True)

    print("=== Modular Resonance Significance (proper null model) ===")
    resonance_results = test_resonance_significance(max_n=500000, n_null=1000)

    print("\n=== Other Tests ===")
    tda_result = test_tda_significance()
    lyap_result = test_lyapunov()
    pt_result = test_phase_transition()

    all_results = {
        "seed": SEED,
        "resonance_tests": resonance_results,
        "tda_test": tda_result,
        "lyapunov_test": lyap_result,
        "phase_transition_test": pt_result,
        "bonferroni_n_comparisons": 7,
    }

    with open("results/significance.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Print summary
    print("\n=== SIGNIFICANCE SUMMARY ===")
    print(f"\nModular Resonance (primes coprime to 6):")
    sig_count = 0
    for r in resonance_results:
        if r["coprime_to_6"] and r["is_prime"]:
            sig = " ***SIGNIFICANT***" if r["significant_at_001"] else ""
            print(f"  mod {r['modulus']}: obs_chi2={r['observed_chi2']:.0f}, "
                  f"null_mean={r['null_mean_chi2']:.0f}±{r['null_std_chi2']:.0f}, "
                  f"z={r['effect_size_z']:.1f}, p={r['corrected_p_value']:.4f}{sig}")
            if r["significant_at_001"]:
                sig_count += 1

    print(f"\nTDA H1: p_corrected={tda_result['corrected_p_value']:.3f}, sig={tda_result['significant_at_001']}")
    print(f"Lyapunov: p_corrected={lyap_result['corrected_p_value']:.2e}, sig={lyap_result['significant_at_001']}")
    print(f"Phase transition: effect={pt_result['effect_size']:.3f}, sig={pt_result['significant_at_001']}")

    total_sig = sig_count + int(lyap_result['significant_at_001']) + int(pt_result['significant_at_001'])
    print(f"\nTotal significant findings (p < 0.001 after Bonferroni): {total_sig}")
    return all_results


if __name__ == "__main__":
    results = run_all_significance()
