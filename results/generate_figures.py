"""Generate all publication-quality figures for the research report.

Produces:
1. figures/bounds_timeline.png - Historical progression of bounds
2. figures/scaling_fit.png - Already exists (from item 010)
3. figures/lueker_convergence.png - Already exists (from item 019)
4. figures/approach_comparison.png - Bar chart comparing all methods
5. figures/dfa_ablation.png - Already exists (from item 020)
"""

import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    base = Path(__file__).parent
    data = {}
    for name, path in [
        ("bounds_comparison", "experiments/bounds_comparison.json"),
        ("scaling", "baseline/scaling_analysis.json"),
        ("exact", "baseline/exact_expectations.json"),
        ("mc", "baseline/mc_estimates.json"),
        ("dfa", "novel/dfa_lower_bounds.json"),
        ("entropy", "novel/entropy_upper_results.json"),
        ("sdp", "novel/sdp_results.json"),
        ("frog", "novel/frog_dynamics_results.json"),
        ("lueker", "baseline/lueker_lower_bounds.json"),
    ]:
        try:
            with open(base / path) as f:
                data[name] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found")
    return data


def fig_bounds_timeline(data):
    """Historical progression of upper and lower bounds on gamma_2."""
    sns.set_theme(style="whitegrid", font_scale=1.1)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Historical data points (year, lower_bound, upper_bound, author)
    history = [
        (1975, 0.5,    1.0,    "Chvátal–Sankoff"),
        (1994, 0.7239, 0.8672, "Dancik"),
        (1995, 0.7739, 0.8572, "Dancik–Paterson"),
        (2003, 0.7880, None,   "Lueker (lower)"),
        (2009, 0.7880, 0.8263, "Lueker (upper)"),
        (2024, 0.7927, None,   "Heineman et al."),
    ]

    years_l = [h[0] for h in history if h[1] is not None]
    lowers  = [h[1] for h in history if h[1] is not None]
    years_u = [h[0] for h in history if h[2] is not None]
    uppers  = [h[2] for h in history if h[2] is not None]

    ax.step(years_l, lowers, 'o-', color='C0', where='post', linewidth=2,
            markersize=8, label='Lower bounds', zorder=5)
    ax.step(years_u, uppers, 's-', color='C3', where='post', linewidth=2,
            markersize=8, label='Upper bounds', zorder=5)

    # Our conjectural bound
    ax.scatter([2026], [0.808], marker='*', color='gold', s=200, zorder=10,
               edgecolors='black', linewidths=0.8,
               label='This work: LPP gap (conjectural)')

    # MC estimate band
    ax.axhspan(0.810, 0.813, alpha=0.15, color='green', label='MC estimate range')

    # Annotations
    for year, lower, upper, author in history:
        if lower is not None and year in [1975, 1995, 2009, 2024]:
            ax.annotate(author, (year, lower), textcoords="offset points",
                       xytext=(5, -15), fontsize=7.5, color='C0')
        if upper is not None and year in [1975, 1995, 2009]:
            ax.annotate(author, (year, upper), textcoords="offset points",
                       xytext=(5, 8), fontsize=7.5, color='C3')

    ax.annotate('Bernoulli LPP − Δ\n(conjectural)', (2026, 0.808),
               textcoords="offset points", xytext=(10, 10), fontsize=8,
               color='goldenrod', fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='goldenrod'))

    ax.set_xlabel('Year')
    ax.set_ylabel(r'Bound on $\gamma_2$')
    ax.set_title(r'Historical Progression of Bounds on the Binary Chvátal–Sankoff Constant $\gamma_2$')
    ax.legend(loc='center right', fontsize=9)
    ax.set_xlim(1973, 2028)
    ax.set_ylim(0.45, 1.05)

    figpath = Path(__file__).parent.parent / "figures" / "bounds_timeline"
    fig.savefig(str(figpath) + ".png", dpi=150, bbox_inches='tight')
    fig.savefig(str(figpath) + ".pdf", bbox_inches='tight')
    plt.close()
    print(f"Saved {figpath}.png")


def fig_approach_comparison(data):
    """Bar chart comparing all methods' bounds."""
    sns.set_theme(style="whitegrid", font_scale=1.0)
    fig, ax = plt.subplots(figsize=(14, 7))

    methods = [
        ("Exact E[L₁₃]/13\n(rigorous lower)", 0.7129, "lower", True),
        ("Lueker baseline\nℓ=7", 0.6745, "lower", True),
        ("DFA h=6\n(rigorous lower)", 0.7616, "lower", True),
        ("Frog dynamics\nW='000111'", 0.7920, "estimate", False),
        ("Frog dynamics\nbest period-8", 0.8050, "estimate", False),
        ("MC n=5000", 0.8097, "estimate", False),
        ("Scaling extrap.\nβ=2/3", 0.8115, "estimate", False),
        ("Bernoulli LPP\n− gap (conj.)", 0.8076, "upper", False),
        ("Lueker 2009\nupper", 0.8263, "upper", True),
        ("Bernoulli LPP\nceiling", 0.8284, "upper", False),
        ("Kolmogorov\nupper", 0.9051, "upper", True),
    ]

    names = [m[0] for m in methods]
    values = [m[1] for m in methods]
    types = [m[2] for m in methods]
    rigorous = [m[3] for m in methods]

    colors = []
    for t, r in zip(types, rigorous):
        if t == "lower":
            colors.append('C0' if r else 'lightblue')
        elif t == "upper":
            colors.append('C3' if r else 'lightsalmon')
        else:
            colors.append('C2' if r else 'lightgreen')

    edgecolors = ['black' if r else 'gray' for r in rigorous]

    bars = ax.barh(range(len(methods)), values, color=colors,
                   edgecolor=edgecolors, linewidth=1.5)

    # Reference lines
    ax.axvline(x=0.792665992, color='C0', linestyle='--', alpha=0.7,
               label='Best known lower (0.7927)')
    ax.axvline(x=0.826280, color='C3', linestyle='--', alpha=0.7,
               label='Best known upper (0.8263)')
    ax.axvline(x=0.8115, color='C2', linestyle=':', alpha=0.5,
               label='MC estimate (0.8115)')

    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel(r'Bound value on $\gamma_2$')
    ax.set_title(r'Comparison of All Computed Bounds on $\gamma_2$')
    ax.legend(fontsize=8, loc='lower right')
    ax.set_xlim(0.6, 0.95)

    # Add value labels
    for i, (v, r) in enumerate(zip(values, rigorous)):
        rig_str = " ✓" if r else ""
        ax.text(v + 0.003, i, f'{v:.4f}{rig_str}', va='center', fontsize=8)

    ax.invert_yaxis()
    plt.tight_layout()

    figpath = Path(__file__).parent.parent / "figures" / "approach_comparison"
    fig.savefig(str(figpath) + ".png", dpi=150, bbox_inches='tight')
    fig.savefig(str(figpath) + ".pdf", bbox_inches='tight')
    plt.close()
    print(f"Saved {figpath}.png")


def main():
    data = load_data()
    print("Generating publication-quality figures...")

    fig_bounds_timeline(data)
    fig_approach_comparison(data)

    print("\nAll figures generated. Existing figures:")
    figdir = Path(__file__).parent.parent / "figures"
    for f in sorted(figdir.glob("*")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
