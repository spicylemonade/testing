"""Finite-size scaling analysis to extrapolate gamma_2 from MC data.

Tests scaling forms:
  E[L_n]/n = gamma + a*n^(-beta)

for beta in {1/3, 1/2, 2/3} corresponding to KPZ, diffusive, and intermediate 
universality classes.

Reference: Bundschuh (2001) for the scaling form.
"""

import numpy as np
from scipy.optimize import curve_fit
import json
import time
from pathlib import Path

# Publication-quality plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Configure publication-quality plots
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.figsize': (8, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})
sns.set_palette("colorblind")


def scaling_form(n, gamma, a, beta):
    """E[L_n]/n = gamma + a * n^(-beta)"""
    return gamma + a * n**(-beta)


def fit_scaling(n_values, ratio_values, beta_fixed):
    """Fit gamma and a for fixed beta."""
    def model(n, gamma, a):
        return gamma + a * n**(-beta_fixed)
    
    try:
        popt, pcov = curve_fit(model, n_values, ratio_values, p0=[0.81, -1.0],
                               maxfev=10000)
        gamma_est, a_est = popt
        gamma_err = np.sqrt(pcov[0, 0])
        
        # R^2
        residuals = ratio_values - model(n_values, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((ratio_values - np.mean(ratio_values))**2)
        r_squared = 1 - ss_res / ss_tot
        
        return {
            "gamma": float(gamma_est),
            "gamma_stderr": float(gamma_err),
            "a": float(a_est),
            "beta": float(beta_fixed),
            "R_squared": float(r_squared),
            "residuals_rms": float(np.sqrt(np.mean(residuals**2)))
        }
    except Exception as e:
        return {"error": str(e), "beta": float(beta_fixed)}


def main():
    print("Finite-Size Scaling Analysis")
    print("=" * 60)
    
    # Load MC estimates
    mc_path = Path(__file__).parent / "mc_estimates.json"
    with open(mc_path) as f:
        mc_data = json.load(f)
    
    # Also load exact data for small n
    exact_path = Path(__file__).parent / "exact_expectations.json"
    with open(exact_path) as f:
        exact_data = json.load(f)
    
    # Combine: use exact data for small n, MC for large n
    all_n = []
    all_ratio = []
    all_ci = []
    
    # Exact data (very precise)
    for n_str, data in exact_data["results"].items():
        n = int(n_str)
        if n >= 5:  # Skip very small n for scaling fit
            all_n.append(n)
            all_ratio.append(data["E_L_n_over_n"])
            all_ci.append(0.0)  # Exact, no CI
    
    # MC data
    for n_str, data in mc_data["results"].items():
        n = int(n_str)
        all_n.append(n)
        all_ratio.append(data["ratio_E_L_n_over_n"])
        all_ci.append((data["ci_95_upper"] - data["ci_95_lower"]) / 2)
    
    n_arr = np.array(all_n, dtype=float)
    ratio_arr = np.array(all_ratio, dtype=float)
    ci_arr = np.array(all_ci, dtype=float)
    
    # Sort by n
    sort_idx = np.argsort(n_arr)
    n_arr = n_arr[sort_idx]
    ratio_arr = ratio_arr[sort_idx]
    ci_arr = ci_arr[sort_idx]
    
    print(f"Data points: {len(n_arr)}")
    for i in range(len(n_arr)):
        print(f"  n={int(n_arr[i]):>5d}: E[L_n]/n = {ratio_arr[i]:.8f}")
    
    # Fit scaling forms for different beta values
    betas = {"KPZ (beta=1/3)": 1/3, "Diffusive (beta=1/2)": 1/2, "Intermediate (beta=2/3)": 2/3}
    
    # Use only MC data (n >= 100) for the scaling fit to avoid small-n effects
    mc_mask = n_arr >= 100
    n_mc = n_arr[mc_mask]
    ratio_mc = ratio_arr[mc_mask]
    
    fit_results = {}
    best_r2 = -1
    best_beta_name = None
    
    for name, beta in betas.items():
        result = fit_scaling(n_mc, ratio_mc, beta)
        fit_results[name] = result
        
        if "gamma" in result:
            print(f"\n{name}:")
            print(f"  gamma = {result['gamma']:.8f} ± {result['gamma_stderr']:.8f}")
            print(f"  a = {result['a']:.4f}")
            print(f"  R² = {result['R_squared']:.8f}")
            
            if result["R_squared"] > best_r2:
                best_r2 = result["R_squared"]
                best_beta_name = name
    
    print(f"\nBest fit: {best_beta_name} (R² = {best_r2:.8f})")
    
    # Generate plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: data with fits
    ax1.errorbar(n_arr, ratio_arr, yerr=ci_arr, fmt='ko', markersize=4, 
                 capsize=2, label='Data (exact + MC)', zorder=5)
    
    n_smooth = np.linspace(5, 6000, 500)
    colors = {'KPZ (beta=1/3)': '#1b9e77', 'Diffusive (beta=1/2)': '#d95f02', 
              'Intermediate (beta=2/3)': '#7570b3'}
    
    for name, beta in betas.items():
        if "gamma" in fit_results[name]:
            r = fit_results[name]
            y_fit = scaling_form(n_smooth, r["gamma"], r["a"], r["beta"])
            ax1.plot(n_smooth, y_fit, '-', color=colors[name], linewidth=1.5,
                    label=f'{name}: γ={r["gamma"]:.5f}')
    
    # Reference lines
    ax1.axhline(y=0.826280, color='red', linestyle='--', alpha=0.5, linewidth=1, 
                label='Upper bound (Lueker 2009)')
    ax1.axhline(y=0.792666, color='blue', linestyle='--', alpha=0.5, linewidth=1,
                label='Lower bound (Heineman 2024)')
    ax1.axhline(y=0.8117, color='gray', linestyle=':', alpha=0.5, linewidth=1,
                label='MC estimate (Bundschuh 2001)')
    
    ax1.set_xlabel('String length n')
    ax1.set_ylabel('E[L_n]/n')
    ax1.set_title('Finite-size scaling of E[L_n]/n')
    ax1.legend(fontsize=9, loc='lower right')
    ax1.set_ylim(0.64, 0.83)
    
    # Right: residuals vs n^(-beta) for best fit
    best_result = fit_results[best_beta_name]
    beta_best = best_result["beta"]
    
    ax2.plot(n_arr**(-beta_best), ratio_arr, 'ko', markersize=5)
    x_line = np.linspace(0, max(n_arr**(-beta_best)) * 1.1, 100)
    y_line = best_result["gamma"] + best_result["a"] * x_line
    ax2.plot(x_line, y_line, 'r-', linewidth=1.5, label=f'Linear fit: γ={best_result["gamma"]:.6f}')
    ax2.axhline(y=best_result["gamma"], color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel(f'n^(-{beta_best:.4f})')
    ax2.set_ylabel('E[L_n]/n')
    ax2.set_title(f'Scaling collapse ({best_beta_name})')
    ax2.legend()
    
    plt.tight_layout()
    
    # Save figures
    fig_dir = Path(__file__).parent.parent.parent / "figures"
    fig_dir.mkdir(exist_ok=True)
    fig.savefig(fig_dir / "scaling_fit.png", dpi=300)
    fig.savefig(fig_dir / "scaling_fit.pdf")
    plt.close()
    
    print(f"\nFigures saved to figures/scaling_fit.png and .pdf")
    
    # Save results
    output = {
        "description": "Finite-size scaling analysis of E[L_n]/n",
        "data_sources": ["exact_expectations.json (n=5..13)", "mc_estimates.json (n=100..5000)"],
        "scaling_fits": fit_results,
        "best_fit": {
            "name": best_beta_name,
            "R_squared": best_r2,
            "gamma_extrapolated": best_result["gamma"],
            "gamma_stderr": best_result["gamma_stderr"],
            "in_valid_range": 0.79 <= best_result["gamma"] <= 0.83
        },
        "conclusion": f"Best scaling form: {best_beta_name}. Extrapolated gamma_2 = {best_result['gamma']:.8f} ± {best_result['gamma_stderr']:.8f}"
    }
    
    outpath = Path(__file__).parent / "scaling_analysis.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to {outpath}")


if __name__ == "__main__":
    main()
