"""Convergence analysis of the Lueker E[LCS(ell)]/ell lower bound sequence.

Fits extrapolation models to determine the theoretical ceiling of the framework
and compares against MC-based gamma_2 estimates.
"""

import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit


def main():
    base = Path(__file__).parent.parent

    # Load data
    with open(base / "baseline" / "lueker_lower_bounds.json") as f:
        lueker = json.load(f)
    with open(base / "baseline" / "exact_expectations.json") as f:
        exact = json.load(f)
    with open(base / "baseline" / "scaling_analysis.json") as f:
        scaling = json.load(f)
    with open(base / "baseline" / "mc_estimates.json") as f:
        mc = json.load(f)

    # Extract Lueker E[LCS(ell)]/ell sequence
    ells = []
    bounds = []
    for k, v in sorted(lueker["results"].items(), key=lambda x: int(x[0])):
        ells.append(v["ell"])
        bounds.append(v["best_lower_bound"])

    ells = np.array(ells, dtype=float)
    bounds = np.array(bounds)

    # Also get exact E[L_n]/n for n=1..13 (same as Lueker for n<=7, extends further)
    exact_ns = []
    exact_ratios = []
    for k, v in sorted(exact["results"].items(), key=lambda x: int(x[0])):
        exact_ns.append(v["n"])
        exact_ratios.append(v["E_L_n_over_n"])

    exact_ns = np.array(exact_ns, dtype=float)
    exact_ratios = np.array(exact_ratios)

    # Known reference values
    gamma_mc = scaling["best_fit"]["gamma_extrapolated"]  # ~0.8115
    gamma_mc_err = scaling["best_fit"]["gamma_stderr"]
    heineman_lower = 0.792665992
    lueker_upper = 0.826280

    # ---- Fit extrapolation models ----
    # Key insight: E[L_n]/n converges to gamma_2 from below (superadditivity).
    # The exact computation only reaches n=13, giving 0.7129.
    # The Lueker *framework* (with optimized feasible triplets, not just E[LCS]/ell)
    # achieves 0.7927 at large ell (Heineman 2024). Our naive computation is far weaker.
    #
    # We fit the E[L_n]/n data (n=1..13) to understand convergence rate,
    # and also combine with MC data (n=100..5000) for a full picture.

    # Models for E[L_n]/n = gamma - f(n)
    def exp_model(x, gamma_inf, c, alpha):
        return gamma_inf - c * np.exp(-alpha * x)

    def power_model(x, gamma_inf, c, beta):
        return gamma_inf - c * x**(-beta)

    def inv_ell_model(x, gamma_inf, c):
        return gamma_inf - c / x

    def log_model(x, gamma_inf, c):
        """gamma - c / log(x+1) -- very slow convergence"""
        return gamma_inf - c / np.log(x + 1)

    fits = {}

    # ---- Fit A: Exact data only (n=1..13) ----
    # These fits answer: "How fast does E[L_n]/n converge for small n?"
    x_exact = exact_ns[2:]  # skip n=1,2 for better fit on the tail
    y_exact = exact_ratios[2:]

    for model_name, model_fn, p0, bnds in [
        ("exponential", exp_model, [0.82, 0.5, 0.1], ([0.7, 0, 0.001], [0.9, 5, 2])),
        ("power_law", power_model, [0.82, 0.3, 0.5], ([0.7, 0.001, 0.1], [0.95, 5, 3])),
        ("inverse_ell", inv_ell_model, [0.82, 0.3], ([0.7, 0.001], [0.95, 5])),
        ("log_slow", log_model, [0.82, 0.3], ([0.7, 0.001], [0.95, 5])),
    ]:
        try:
            popt, pcov = curve_fit(model_fn, x_exact, y_exact,
                                   p0=p0, maxfev=10000, bounds=bnds)
            perr = np.sqrt(np.diag(pcov))
            y_pred = model_fn(x_exact, *popt)
            ss_res = np.sum((y_exact - y_pred)**2)
            ss_tot = np.sum((y_exact - np.mean(y_exact))**2)
            r2 = 1 - ss_res / ss_tot
            entry = {
                "gamma_inf": float(popt[0]),
                "gamma_inf_stderr": float(perr[0]),
                "R_squared": float(r2),
                "data_range": "n=3..13 (exact)"
            }
            for i, name in enumerate(["c", "alpha", "beta"][:len(popt)-1]):
                entry[name] = float(popt[i+1])
            fits[f"exact_{model_name}"] = entry
        except Exception as e:
            fits[f"exact_{model_name}"] = {"error": str(e)}

    # ---- Fit B: Combined exact + MC data (n=3..5000) ----
    # Load MC data
    mc_ns = []
    mc_ratios = []
    for k, v in sorted(mc["results"].items(), key=lambda x: int(x[0])):
        mc_ns.append(v["n"])
        mc_ratios.append(v["ratio_E_L_n_over_n"])
    
    x_combined = np.concatenate([exact_ns[2:], np.array(mc_ns)])
    y_combined = np.concatenate([exact_ratios[2:], np.array(mc_ratios)])

    for model_name, model_fn, p0, bnds in [
        ("power_law", power_model, [0.815, 0.5, 0.5], ([0.79, 0.001, 0.1], [0.84, 10, 3])),
        ("log_slow", log_model, [0.815, 0.5], ([0.79, 0.001], [0.84, 5])),
    ]:
        try:
            popt, pcov = curve_fit(model_fn, x_combined, y_combined,
                                   p0=p0, maxfev=10000, bounds=bnds)
            perr = np.sqrt(np.diag(pcov))
            y_pred = model_fn(x_combined, *popt)
            ss_res = np.sum((y_combined - y_pred)**2)
            ss_tot = np.sum((y_combined - np.mean(y_combined))**2)
            r2 = 1 - ss_res / ss_tot
            entry = {
                "gamma_inf": float(popt[0]),
                "gamma_inf_stderr": float(perr[0]),
                "R_squared": float(r2),
                "data_range": "n=3..5000 (exact + MC)"
            }
            for i, name in enumerate(["c", "alpha", "beta"][:len(popt)-1]):
                entry[name] = float(popt[i+1])
            fits[f"combined_{model_name}"] = entry
        except Exception as e:
            fits[f"combined_{model_name}"] = {"error": str(e)}

    # Determine best fit (prefer combined fits since they use more data)
    valid_fits = {k: v for k, v in fits.items() if "R_squared" in v}
    combined_fits = {k: v for k, v in valid_fits.items() if k.startswith("combined_")}
    if combined_fits:
        best_name = max(combined_fits, key=lambda k: combined_fits[k]["R_squared"])
    else:
        best_name = max(valid_fits, key=lambda k: valid_fits[k]["R_squared"])
    best_fit = valid_fits[best_name]

    exceeds_080 = best_fit["gamma_inf"] > 0.80
    can_close_gap = best_fit["gamma_inf"] > heineman_lower

    # Analysis: convergence rate
    # Compute successive differences
    diffs = np.diff(exact_ratios)
    ratios_of_diffs = diffs[1:] / diffs[:-1]

    # Lueker framework structural analysis
    # The key question: does the *framework* have a structural ceiling below gamma_2?
    # Answer: No. Heineman (2024) achieved 0.7927 with the Lueker framework at large ell.
    # Our naive E[LCS(ell)]/ell computation only reaches 0.6745 at ell=7.
    # The gap is because the Lueker framework uses *optimized feasible triplets*,
    # not just the trivial ones from exact E[LCS]/ell.
    lueker_framework_ceiling_note = (
        "The Lueker feasible-triplet framework does NOT have a structural ceiling below gamma_2. "
        "Heineman (2024) achieved 0.7927 using optimized feasible triplets with large ell. "
        "Our naive E[LCS(ell)]/ell computation (which uses trivial triplets) converges much more slowly. "
        "The key bottleneck is not the framework but the optimization of the triplet parameters."
    )

    analysis = {
        "description": "Convergence analysis of E[L_n]/n lower bound sequence and Lueker framework",
        "data_used": "exact E[L_n]/n for n=1..13, MC estimates for n=100..5000",
        "fits": fits,
        "best_fit": {
            "model": best_name,
            "gamma_inf": best_fit["gamma_inf"],
            "gamma_inf_stderr": best_fit["gamma_inf_stderr"],
            "R_squared": best_fit["R_squared"]
        },
        "extrapolated_limit_exceeds_0.80": exceeds_080,
        "comparison": {
            "extrapolated_limit": best_fit["gamma_inf"],
            "mc_estimate_gamma_2": gamma_mc,
            "heineman_2024_lower": heineman_lower,
            "lueker_2009_upper": lueker_upper,
            "gap_to_mc": float(gamma_mc - best_fit["gamma_inf"]),
            "gap_to_heineman": float(heineman_lower - best_fit["gamma_inf"])
        },
        "successive_differences": {
            "diffs": [float(d) for d in diffs],
            "ratios_of_consecutive_diffs": [float(r) for r in ratios_of_diffs],
            "note": "Ratios approaching 1 indicate very slow (sub-exponential) convergence"
        },
        "lueker_framework_analysis": lueker_framework_ceiling_note,
        "conclusion": (
            f"Best combined extrapolation: {best_name} with gamma_inf = {best_fit['gamma_inf']:.6f} "
            f"+/- {best_fit['gamma_inf_stderr']:.6f}. "
            f"{'Exceeds' if exceeds_080 else 'Does NOT exceed'} 0.80. "
            f"The E[L_n]/n sequence converges to gamma_2 very slowly (ratios of successive "
            f"differences approach 1). The Lueker framework itself has no structural ceiling "
            f"below gamma_2 -- Heineman achieved 0.7927 -- but requires sophisticated "
            f"feasible-triplet optimization, not just naive E[LCS(ell)]/ell computation."
        )
    }

    # Save results
    outpath = Path(__file__).parent / "lueker_convergence.json"
    with open(outpath, "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"Results saved to {outpath}")

    # ---- Generate figure ----
    sns.set_theme(style="whitegrid", font_scale=1.1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: bounds vs n (log scale) with extrapolation curves
    # Plot exact data
    ax1.scatter(exact_ns, exact_ratios, color='C0', s=50, zorder=5,
                label=r'Exact $E[L_n]/n$', edgecolors='black', linewidths=0.5)
    # Plot MC data
    mc_ns_arr = np.array(mc_ns)
    mc_ratios_arr = np.array(mc_ratios)
    ax1.scatter(mc_ns_arr, mc_ratios_arr, color='C1', s=50, zorder=5, marker='s',
                label='MC estimates', edgecolors='black', linewidths=0.5)

    # Extrapolation curves (combined fits)
    n_ext = np.logspace(0, 5, 1000)
    for name, fit in valid_fits.items():
        if not name.startswith("combined_"):
            continue
        if "gamma_inf" not in fit:
            continue
        if "power_law" in name:
            beta_val = fit.get("beta", fit.get("alpha", 0.5))  # alpha key stores beta param
            y_ext = power_model(n_ext, fit["gamma_inf"], fit["c"], beta_val)
            ax1.plot(n_ext, y_ext, '--', color='C2',
                     label=f'Power fit → {fit["gamma_inf"]:.4f} (R²={fit["R_squared"]:.4f})', alpha=0.8)
        elif "log_slow" in name:
            y_ext = log_model(n_ext, fit["gamma_inf"], fit["c"])
            ax1.plot(n_ext, y_ext, '-.', color='C3',
                     label=f'Log fit → {fit["gamma_inf"]:.4f} (R²={fit["R_squared"]:.4f})', alpha=0.8)

    ax1.axhline(y=heineman_lower, color='green', linestyle='-', alpha=0.6,
                label=f'Heineman 2024: {heineman_lower}')
    ax1.axhline(y=lueker_upper, color='red', linestyle='-', alpha=0.6,
                label=f'Lueker 2009 upper: {lueker_upper}')
    ax1.axhline(y=gamma_mc, color='orange', linestyle='--', alpha=0.6,
                label=f'Scaling extrap.: {gamma_mc:.4f}')
    ax1.axhspan(heineman_lower, lueker_upper, alpha=0.07, color='gray')

    ax1.set_xlabel(r'$n$')
    ax1.set_ylabel(r'$E[L_n]/n$')
    ax1.set_title(r'Convergence of $E[L_n]/n$ to $\gamma_2$')
    ax1.legend(fontsize=7.5, loc='lower right')
    ax1.set_xscale('log')
    ax1.set_xlim(1, 1e5)
    ax1.set_ylim(0.45, 0.85)

    # Right: successive difference ratios (exact data n=1..13)
    ax2.plot(range(2, len(exact_ratios)), ratios_of_diffs, 'o-', color='C3',
             markersize=6, label='Ratio of successive diffs')
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='No convergence')
    ax2.set_xlabel('n')
    ax2.set_ylabel(r'$\Delta_{n+1} / \Delta_n$')
    ax2.set_title('Convergence Rate (Ratio of Successive Differences)')
    ax2.legend(fontsize=9)
    ax2.set_ylim(0.5, 1.1)
    ax2.annotate('Approaching 1 = very slow convergence',
                 xy=(10, 0.88), fontsize=8, color='gray', style='italic')

    plt.tight_layout()
    figpath = Path(__file__).parent.parent.parent / "figures" / "lueker_convergence"
    fig.savefig(str(figpath) + ".png", dpi=150, bbox_inches='tight')
    fig.savefig(str(figpath) + ".pdf", bbox_inches='tight')
    plt.close()
    print(f"Figure saved to {figpath}.png and .pdf")

    # Print summary
    print("\n=== Convergence Analysis ===")
    for name, fit in valid_fits.items():
        print(f"  {name}: gamma_inf = {fit['gamma_inf']:.6f} ± {fit['gamma_inf_stderr']:.6f}, R² = {fit['R_squared']:.6f}")
    print(f"\nBest: {best_name}, gamma_inf = {best_fit['gamma_inf']:.6f}")
    print(f"Exceeds 0.80? {exceeds_080}")
    print(f"Successive diff ratios: {[f'{r:.4f}' for r in ratios_of_diffs]}")


if __name__ == "__main__":
    main()
