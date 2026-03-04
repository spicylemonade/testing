#!/usr/bin/env python3
"""Systematic comparison of all upper bound approaches for γ₂.

Collects results from:
  - Phase 2: MC-based upper bounds
  - Phase 3: Strip eigenvalue, Entropy methods

Compares against SOTA: Lueker 2009 upper bound = 0.826280

References:
  - [L2009] Lueker 2009
  - [DP1995] Dančík & Paterson 1995
  - [H2024] Heineman et al. 2024
  - [B2001] Bundschuh 2001
"""

import json
from pathlib import Path

RESULTS_DIR = Path(__file__).parent
BASELINES_DIR = RESULTS_DIR.parent / "baselines"
NOVEL_DIR = RESULTS_DIR.parent / "novel"
FIGURES_DIR = RESULTS_DIR.parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

SOTA_UPPER = 0.826280  # Lueker 2009


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return None


def main():
    print("=== Systematic Comparison of Upper Bound Approaches ===\n")
    
    approaches = []
    
    # 1. MC-based upper bounds (Phase 2)
    mc_data = load_json(BASELINES_DIR / "upper_bounds.json")
    if mc_data:
        results = mc_data.get("results", mc_data.get("estimates", []))
        if results:
            best_mc = min(results, key=lambda x: x.get("upper_ci_95", 
                          x.get("gamma_estimate", 99) + 1.96 * x.get("gamma_se", 0.1)), default={})
            upper = best_mc.get("upper_ci_95", 
                    best_mc.get("gamma_estimate", 0) + 1.96 * best_mc.get("gamma_se", 0))
            approaches.append({
                "name": "Monte Carlo 95% CI Upper",
                "method": "E[LCS(n,n)]/n + 1.96·SE from MC trials",
                "best_bound": round(float(upper), 6),
                "parameters": f"n={best_mc.get('n', '?')}, trials={best_mc.get('trials', '?')}",
                "rigorous": False,
                "computational_cost": "O(n² · trials)",
                "notes": "Non-rigorous: CI bounds E[LCS(n,n)]/n, not γ₂. Since γ_n > γ₂ for finite n, this is actually a non-rigorous LOWER bound on the upper bound.",
                "references": ["B2001"]
            })
    
    # 2. Strip eigenvalue (Phase 3)
    strip_data = load_json(NOVEL_DIR / "scaled_upper_bound.json")
    if strip_data:
        mc_ub = strip_data.get("mc_upper_bound", {})
        approaches.append({
            "name": "Strip Transfer Matrix",
            "method": "Column-difference Markov chain stationary throughput",
            "best_bound": 1.0,
            "parameters": "s=2..10",
            "rigorous": False,
            "computational_cost": "O(2^s × 2^(s+1)) per s",
            "notes": "FAILED: absorbing all-ones state makes γ_s = 1.0 for all s. The column-difference formulation has an absorbing state that concentrates the stationary distribution.",
            "references": ["DP1995", "L2009"]
        })
        if mc_ub.get("upper_99"):
            approaches.append({
                "name": "MC 99% CI Upper (n=5000)",
                "method": "E[LCS(5000,5000)]/5000 + 2.576·SE",
                "best_bound": round(float(mc_ub["upper_99"]), 6),
                "parameters": f"n=5000, trials=1000",
                "rigorous": False,
                "computational_cost": "O(n² · trials)",
                "notes": "Non-rigorous MC upper bound from strip computation script",
                "references": ["B2001"]
            })
    
    # 3. Entropy bounds (Phase 3)
    entropy_data = load_json(NOVEL_DIR / "entropy_upper_bound.json")
    if entropy_data:
        methods = entropy_data.get("methods", {})
        for method_name, method_data in methods.items():
            bound = method_data.get("bound", 1.0)
            if bound < 1.0:
                approaches.append({
                    "name": f"Entropy: {method_name}",
                    "method": method_data.get("explanation", "")[:100],
                    "best_bound": round(float(bound), 6),
                    "parameters": method_name,
                    "rigorous": True,
                    "computational_cost": "Analytic",
                    "notes": method_data.get("explanation", ""),
                    "references": ["DP1995", "L2009"]
                })
    
    # 4. Literature SOTA
    approaches.append({
        "name": "Lueker 2009 (Literature SOTA)",
        "method": "Eigenvalue of column-difference recurrence with DFA certificate",
        "best_bound": SOTA_UPPER,
        "parameters": "Optimized dual system",
        "rigorous": True,
        "computational_cost": "~days of computation",
        "notes": "Current best known rigorous upper bound",
        "references": ["L2009"]
    })
    
    approaches.append({
        "name": "Dančík-Paterson 1995 Analytic",
        "method": "Analytic bound from recurrence structure",
        "best_bound": 0.838,
        "parameters": "Closed-form",
        "rigorous": True,
        "computational_cost": "None (analytic)",
        "notes": "First non-trivial computational upper bound",
        "references": ["DP1995"]
    })
    
    # Sort by bound quality (lower is better for upper bounds)
    approaches.sort(key=lambda x: x["best_bound"])
    
    # Filter out trivial bound = 1.0 from ranking
    nontrivial = [a for a in approaches if a["best_bound"] < 1.0]
    
    for i, a in enumerate(nontrivial):
        a["rank"] = i + 1
        a["gap_to_sota"] = round(a["best_bound"] - SOTA_UPPER, 8)
        print(f"  #{i+1}: {a['name']}")
        print(f"       Bound: γ₂ ≤ {a['best_bound']:.6f}  (gap to SOTA: {a['gap_to_sota']:+.6f})")
        print(f"       Rigorous: {a['rigorous']}")
        print()
    
    # Our best rigorous upper bound
    our_rigorous = [a for a in nontrivial 
                    if a["rigorous"] and "Literature" not in a["name"] 
                    and "1995" not in a["name"]]
    our_best = min(our_rigorous, key=lambda x: x["best_bound"], default=None) if our_rigorous else None
    
    analysis = {
        "our_best_upper_bound": our_best["best_bound"] if our_best else None,
        "our_best_method": our_best["name"] if our_best else None,
        "sota_upper_bound": SOTA_UPPER,
        "improvement_achieved": False,
        "most_promising_for_scaling": "Strip Transfer Matrix (with corrected formulation)",
        "reasoning": (
            "None of our approaches improved on Lueker's 0.826280. The strip transfer "
            "matrix failed due to the absorbing all-ones state. The entropy bounds are "
            "structurally limited to ~0.854 without exploiting the column-difference "
            "monotonicity. The correct approach would implement Lueker's dual certificate "
            "system, which avoids the absorbing state by working in a different state space "
            "that tracks the 'potential function' rather than the raw column differences."
        )
    }
    
    output = {
        "description": "Systematic comparison of all upper bound approaches for γ₂",
        "sota_comparison": f"Lueker 2009: γ₂ ≤ {SOTA_UPPER}",
        "approaches": nontrivial,
        "failed_approaches": [a for a in approaches if a["best_bound"] >= 1.0],
        "analysis": analysis,
        "references_used": ["DP1995", "L2009", "H2024", "B2001"]
    }
    
    outpath = RESULTS_DIR / "upper_bound_comparison.json"
    outpath.write_text(json.dumps(output, indent=2))
    print(f"Results saved to {outpath}")
    
    # Generate figure
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        names = [a["name"].replace(" (Literature SOTA)", "\n(SOTA)") for a in nontrivial]
        bounds = [a["best_bound"] for a in nontrivial]
        colors = ['gold' if a["best_bound"] == SOTA_UPPER else 
                  'steelblue' if a["rigorous"] else 'lightcoral' for a in nontrivial]
        
        bars = ax.barh(range(len(nontrivial)), bounds, color=colors, 
                       edgecolor='black', linewidth=0.5)
        ax.set_yticks(range(len(nontrivial)))
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlabel('Upper Bound on γ₂')
        ax.set_title('Comparison of Upper Bound Approaches for γ₂')
        ax.axvline(x=SOTA_UPPER, color='red', linestyle='--', linewidth=1.5, 
                   label=f'SOTA = {SOTA_UPPER}')
        ax.axvline(x=0.812, color='gray', linestyle=':', linewidth=1,
                   label='γ₂ ≈ 0.812 (empirical)')
        ax.legend(loc='lower right')
        
        for i, (b, a) in enumerate(zip(bounds, nontrivial)):
            ax.text(b + 0.002, i, f'{b:.4f}', va='center', fontsize=9)
        
        plt.tight_layout()
        fig.savefig(FIGURES_DIR / "upper_bound_comparison.png", dpi=150, bbox_inches='tight')
        fig.savefig(FIGURES_DIR / "upper_bound_comparison.pdf", bbox_inches='tight')
        plt.close(fig)
        print(f"Figure saved to {FIGURES_DIR / 'upper_bound_comparison.png'}")
    except ImportError as e:
        print(f"Plotting skipped: {e}")


if __name__ == "__main__":
    main()
