#!/usr/bin/env python3
"""
Single-command reproducibility script for all Collatz research experiments.

Usage:
    python run_all.py

This script runs all experiments, generates all figures, runs statistical tests,
and produces a summary JSON. Expected runtime: 15-25 minutes on a standard machine.
"""

import os
import sys
import json
import time
import subprocess

RESULTS_DIR = "results"
FIGURES_DIR = "figures"


def ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "baseline"), exist_ok=True)


def run_step(name, module_path, func_name=None):
    """Run a research step and report timing."""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    t0 = time.time()
    try:
        if func_name:
            cmd = f"python -c \"import sys; sys.path.insert(0,'.'); from {module_path} import {func_name}; {func_name}()\""
        else:
            cmd = f"python {module_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
        elapsed = time.time() - t0
        if result.returncode != 0:
            print(f"  ERROR (exit {result.returncode}): {result.stderr[:500]}")
            return {"status": "error", "elapsed": elapsed, "error": result.stderr[:500]}
        print(f"  Completed in {elapsed:.1f}s")
        return {"status": "success", "elapsed": elapsed}
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"  TIMEOUT after {elapsed:.1f}s")
        return {"status": "timeout", "elapsed": elapsed}
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  EXCEPTION: {e}")
        return {"status": "exception", "elapsed": elapsed, "error": str(e)}


def collect_summary():
    """Collect key numerical findings from all result files into summary.json."""
    summary = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}

    # Significance results
    try:
        with open("results/significance.json") as f:
            sig = json.load(f)
        summary["significance"] = {
            "modular_resonance_debunked": all(
                not r["significant_at_001"] for r in sig["resonance_tests"]
            ),
            "lyapunov_significant": sig["lyapunov_test"]["significant_at_001"],
            "lyapunov_ks_statistic": sig["lyapunov_test"]["test_statistic"],
            "phase_transition_significant": sig["phase_transition_test"]["significant_at_001"],
            "phase_transition_effect": sig["phase_transition_test"]["effect_size"],
            "tda_significant": sig["tda_test"]["significant_at_001"],
        }
    except Exception as e:
        summary["significance"] = {"error": str(e)}

    # Deep dive results
    try:
        with open("results/deep_dive.json") as f:
            dd = json.load(f)
        summary["r2_linear_law"] = {
            "slope_alpha": dd["alpha"],
            "slope_std_err": dd["alpha_std_err"],
            "fit_r_squared": dd["fit_r_squared"],
            "max_n": dd["max_n"],
        }
    except Exception as e:
        summary["r2_linear_law"] = {"error": str(e)}

    # Scale invariance
    try:
        with open("results/scale_invariance.json") as f:
            si = json.load(f)
        summary["scale_invariance"] = {
            name: {
                "survives_all_scales": v["survives_all_scales"],
                "trend": v["trend"],
            }
            for name, v in si["findings"].items()
        }
    except Exception as e:
        summary["scale_invariance"] = {"error": str(e)}

    # Lyapunov
    try:
        with open("results/lyapunov_results.json") as f:
            lyap = json.load(f)
        summary["lyapunov"] = {
            "mean": lyap["mean_lyapunov"],
            "std": lyap["std_lyapunov"],
            "ks_statistic": lyap["ks_normal_statistic"],
            "ks_pvalue": lyap["ks_normal_pvalue"],
        }
    except Exception as e:
        summary["lyapunov"] = {"error": str(e)}

    # Phase transition
    try:
        with open("results/phase_transition.json") as f:
            pt = json.load(f)
        summary["phase_transition"] = {
            "a3_b1_convergence": pt["known_a3b1_converges"],
            "a5_b1_convergence": pt["known_a5b1_diverges"],
        }
    except Exception as e:
        summary["phase_transition"] = {"error": str(e)}

    # Verification
    try:
        result = subprocess.run(
            "python verify_discovery.py 100000",
            shell=True, capture_output=True, text=True, timeout=120
        )
        summary["verification"] = {
            "status": "passed" if "CONJECTURE VERIFIED" in result.stdout else "failed",
            "output_excerpt": result.stdout[-300:],
        }
    except Exception as e:
        summary["verification"] = {"error": str(e)}

    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary


def main():
    start = time.time()
    ensure_dirs()

    steps = [
        ("Baseline Metrics", "collatz_baseline.py", None),
        ("TDA Persistent Homology", "research/tda_collatz.py", None),
        ("Spectral Analysis", "research/spectral_collatz.py", None),
        ("Transfer Matrix Lyapunov", "research/transfer_matrix.py", None),
        ("Information Theory MI", "research/info_theory_collatz.py", None),
        ("Modular Resonance", "research/modular_resonance.py", None),
        ("Forbidden Patterns", "research/forbidden_patterns.py", None),
        ("Generalized Collatz Phase Diagram", "research/generalized_collatz.py", None),
        ("Significance Tests", "research/significance_tests.py", None),
        ("Scale Invariance", "research/scale_invariance.py", None),
        ("Deep Dive", "research/deep_dive.py", None),
    ]

    results = {}
    for name, module, func in steps:
        results[name] = run_step(name, module, func)

    print(f"\n{'='*60}")
    print(f"  Collecting Summary")
    print(f"{'='*60}")
    summary = collect_summary()

    total = time.time() - start
    print(f"\n{'='*60}")
    print(f"  ALL EXPERIMENTS COMPLETE")
    print(f"  Total time: {total:.0f}s ({total/60:.1f} min)")
    print(f"{'='*60}")

    # Print step results
    for name, r in results.items():
        status = r["status"].upper()
        elapsed = r.get("elapsed", 0)
        print(f"  [{status:>7s}] {name} ({elapsed:.1f}s)")

    # Print key findings
    print(f"\n  KEY FINDINGS:")
    if "r2_linear_law" in summary and "slope_alpha" in summary["r2_linear_law"]:
        alpha = summary["r2_linear_law"]["slope_alpha"]
        print(f"    R² linear law: α = {alpha:.4f}")
    if "significance" in summary and "lyapunov_ks_statistic" in summary["significance"]:
        print(f"    Lyapunov KS: {summary['significance']['lyapunov_ks_statistic']:.4f}")
    if "phase_transition" in summary and "a3_b1_convergence" in summary["phase_transition"]:
        a3 = summary["phase_transition"]["a3_b1_convergence"]
        a5 = summary["phase_transition"]["a5_b1_convergence"]
        print(f"    Phase transition: a=3 conv={a3:.3f}, a=5 conv={a5:.3f}")

    return results, summary


if __name__ == "__main__":
    main()
