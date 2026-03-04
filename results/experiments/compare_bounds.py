"""Systematic comparison of all computed bounds against known literature values."""

import json
from pathlib import Path


def main():
    base = Path(__file__).parent.parent
    
    # Load all results
    with open(base / "baseline" / "exact_expectations.json") as f:
        exact = json.load(f)
    with open(base / "baseline" / "mc_estimates.json") as f:
        mc = json.load(f)
    with open(base / "baseline" / "lueker_lower_bounds.json") as f:
        lueker = json.load(f)
    with open(base / "baseline" / "scaling_analysis.json") as f:
        scaling = json.load(f)
    with open(base / "novel" / "dfa_lower_bounds.json") as f:
        dfa = json.load(f)
    with open(base / "novel" / "entropy_upper_results.json") as f:
        entropy = json.load(f)
    with open(base / "novel" / "sdp_results.json") as f:
        sdp = json.load(f)
    with open(base / "novel" / "frog_dynamics_results.json") as f:
        frog = json.load(f)
    
    # Known bounds
    LOWER_BEST = 0.792665992  # Heineman 2024
    UPPER_BEST = 0.826280     # Lueker 2009
    
    bounds = []
    
    # 1. Exact computation bounds (rigorous lower)
    bounds.append({
        "method": "Exact E[L_n]/n (superadditivity)",
        "type": "lower",
        "value": exact["rigorous_lower_bound"],
        "parameter": f"n={exact['rigorous_lower_bound_n']}",
        "rigorous": True,
        "source": "This work (item_008)",
        "classification": "weaker than prior work"
    })
    
    # 2. MC estimates (non-rigorous estimate)
    for n_str in ["5000"]:
        if n_str in mc["results"]:
            r = mc["results"][n_str]
            bounds.append({
                "method": "Monte Carlo E[L_n]/n",
                "type": "estimate",
                "value": r["ratio_E_L_n_over_n"],
                "parameter": f"n={r['n']}, {r['num_samples']} samples",
                "rigorous": False,
                "source": "This work (item_007)",
                "classification": "consistent with prior work"
            })
    
    # 3. Finite-size scaling extrapolation
    for name, fit in scaling["scaling_fits"].items():
        if "gamma" in fit:
            bounds.append({
                "method": f"Scaling extrapolation ({name})",
                "type": "estimate",
                "value": fit["gamma"],
                "parameter": f"R²={fit['R_squared']:.6f}",
                "rigorous": False,
                "source": "This work (item_010)",
                "classification": "consistent with prior work"
            })
    
    # 4. Lueker E[LCS(ell)]/ell (rigorous lower)
    best_lueker = max(float(r["best_lower_bound"]) for r in lueker["results"].values())
    bounds.append({
        "method": "Lueker E[LCS(ell)]/ell baseline",
        "type": "lower",
        "value": best_lueker,
        "parameter": "ell=7",
        "rigorous": True,
        "source": "This work (item_009)",
        "classification": "weaker than prior work"
    })
    
    # 5. DFA optimal automaton bounds (rigorous lower)
    bounds.append({
        "method": "DFA optimal automaton (MDP value iteration)",
        "type": "lower",
        "value": dfa["best_bound"],
        "parameter": f"h={dfa['best_h']}",
        "rigorous": True,
        "source": "This work (item_017)",
        "classification": "weaker than prior work"
    })
    
    # 6. Kolmogorov upper bounds (rigorous upper)
    for name, b in entropy["bounds"].items():
        if name in ["kolmogorov_basic", "kolmogorov_refined"]:
            bounds.append({
                "method": f"Kolmogorov complexity ({name})",
                "type": "upper",
                "value": b["bound"],
                "parameter": "analytical",
                "rigorous": b.get("rigorous", True),
                "source": "This work (item_013)",
                "classification": "weaker than prior work" if b["bound"] > UPPER_BEST else "novel improvement"
            })
    
    # 7. Bernoulli LPP ceiling (conjectural upper)
    bounds.append({
        "method": "Bernoulli LPP ceiling 2(√2-1)",
        "type": "upper",
        "value": 0.82842712,
        "parameter": "theoretical (correlation conjecture)",
        "rigorous": False,
        "source": "This work (item_014), based on LPP theory",
        "classification": "comparable to prior work (conjectural)"
    })
    
    # 8. Bernoulli-LCS gap analysis
    if "200" in sdp["bernoulli_comparison"]:
        gap = sdp["bernoulli_comparison"]["200"]["gap"]
        conjectural_upper = 0.82842712 - gap
        bounds.append({
            "method": "Bernoulli LPP - correlation gap (conjectural)",
            "type": "upper",
            "value": round(conjectural_upper, 8),
            "parameter": f"n=200, gap={gap:.6f}",
            "rigorous": False,
            "source": "This work (item_014)",
            "classification": "novel improvement (conjectural)"
        })
    
    # 9. Frog dynamics bounds
    for name, r in frog["periodic_word_results"].items():
        bounds.append({
            "method": f"Frog dynamics gamma_W (W={name})",
            "type": "estimate (periodic-vs-random)",
            "value": r["gamma_W"],
            "parameter": f"period={r['period']}",
            "rigorous": False,
            "source": "This work (item_015)",
            "classification": "related but different problem"
        })
    
    # 10. Average gamma_W over random words
    for p, r in frog["random_average_results"].items():
        bounds.append({
            "method": f"Avg gamma_W over random period-{p} words",
            "type": "estimate (average periodic-vs-random)",
            "value": r["avg_gamma_W"],
            "parameter": f"{r['num_words']} words",
            "rigorous": False,
            "source": "This work (item_015)",
            "classification": "novel estimate"
        })
    
    # Classify each bound
    novel_improvements = [b for b in bounds if "novel improvement" in b["classification"]]
    
    # Print summary
    print("Bounds Comparison Summary")
    print("=" * 80)
    print(f"Known best lower bound: {LOWER_BEST} (Heineman 2024)")
    print(f"Known best upper bound: {UPPER_BEST} (Lueker 2009)")
    print(f"Gap: {UPPER_BEST - LOWER_BEST:.6f}")
    print()
    
    print("All computed bounds:")
    print("-" * 80)
    for b in sorted(bounds, key=lambda x: x["value"]):
        rig = "✓" if b["rigorous"] else "~"
        print(f"  {b['value']:.8f} [{b['type']:>10s}] {rig} {b['method'][:50]:50s} ({b['classification']})")
    
    print()
    if novel_improvements:
        print(f"Novel improvements found: {len(novel_improvements)}")
        for b in novel_improvements:
            print(f"  {b['method']}: {b['value']:.8f} ({b['classification']})")
    else:
        print("No rigorous novel improvements found.")
    
    # Best interval achieved
    rigorous_lowers = [b["value"] for b in bounds if b["type"] == "lower" and b["rigorous"]]
    rigorous_uppers = [b["value"] for b in bounds if b["type"] == "upper" and b["rigorous"]]
    
    best_lower = max(rigorous_lowers) if rigorous_lowers else 0
    best_upper = min(rigorous_uppers) if rigorous_uppers else 1
    
    print(f"\nBest rigorous interval from this work: [{best_lower:.8f}, {best_upper:.8f}]")
    print(f"Best known interval: [{LOWER_BEST}, {UPPER_BEST}]")
    
    output = {
        "description": "Systematic comparison of all computed bounds",
        "known_bounds": {"lower": LOWER_BEST, "upper": UPPER_BEST},
        "all_bounds": bounds,
        "novel_improvements": novel_improvements,
        "best_rigorous_interval_this_work": {
            "lower": best_lower,
            "upper": best_upper
        },
        "num_distinct_bounds": len(bounds)
    }
    
    outpath = Path(__file__).parent / "bounds_comparison.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
