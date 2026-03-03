#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures" / "final"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def setup_style() -> None:
    sns.set_theme(style="whitegrid", context="talk", font="DejaVu Sans")
    plt.rcParams.update(
        {
            "figure.facecolor": "#fbfaf7",
            "axes.facecolor": "#f6f4ee",
            "axes.edgecolor": "#2f3e46",
            "axes.labelcolor": "#1b2631",
            "xtick.color": "#1b2631",
            "ytick.color": "#1b2631",
            "grid.color": "#d8d3c3",
            "grid.alpha": 0.7,
            "axes.titleweight": "bold",
            "axes.labelweight": "semibold",
            "legend.frameon": True,
            "legend.facecolor": "#fffdf8",
            "legend.edgecolor": "#c9c2ad",
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{stem}.png"
    pdf = FIG_DIR / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, dpi=300, bbox_inches="tight")


def figure_claim_01(symplectic_eval: dict) -> None:
    row = next(r for r in symplectic_eval["scenarios"] if r["scenario"] == "two_body")
    baseline_drift = row["medians"]["baseline_max_energy_drift_pct"]
    symp_drift = row["medians"]["symplectic_max_energy_drift_pct"]
    baseline_rt = row["medians"]["baseline_runtime_per_step_ms"]
    symp_rt = row["medians"]["symplectic_runtime_per_step_ms"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    methods = ["Baseline", "Symplectic"]
    colors = ["#c97a40", "#2a9d8f"]

    axes[0].bar(methods, [baseline_drift, symp_drift], color=colors)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Median Max Energy Drift (%)")
    axes[0].set_title("Two-Body Drift Reduction")

    axes[1].bar(methods, [baseline_rt, symp_rt], color=colors)
    axes[1].set_ylabel("Median Runtime per Step (ms)")
    axes[1].set_title("Runtime Parity")

    fig.suptitle("Claim 01: Symplectic Two-Body Fidelity", fontsize=16)
    save(fig, "claim_01_two_body_drift_runtime")
    plt.close(fig)


def figure_claim_02(symplectic_eval: dict) -> None:
    row = next(r for r in symplectic_eval["scenarios"] if r["scenario"] == "three_body")
    baseline_drift = row["medians"]["baseline_max_energy_drift_pct"]
    symp_drift = row["medians"]["symplectic_max_energy_drift_pct"]
    baseline_rt = row["medians"]["baseline_runtime_per_step_ms"]
    symp_rt = row["medians"]["symplectic_runtime_per_step_ms"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    methods = ["Baseline", "Symplectic"]
    colors = ["#8d5524", "#1d7874"]

    axes[0].bar(methods, [baseline_drift, symp_drift], color=colors)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Median Max Energy Drift (%)")
    axes[0].set_title("Three-Body Relative Improvement")

    axes[1].bar(methods, [baseline_rt, symp_rt], color=colors)
    axes[1].set_ylabel("Median Runtime per Step (ms)")
    axes[1].set_title("Runtime Comparison")

    fig.suptitle("Claim 02: Three-Body Symplectic Tradeoff", fontsize=16)
    save(fig, "claim_02_three_body_energy_runtime")
    plt.close(fig)


def figure_claim_03(scaling_eval: dict) -> None:
    points = scaling_eval["error_speed_tradeoff_curve"]
    fig, ax = plt.subplots(figsize=(7.4, 5.2))

    n_values = sorted({int(p["n"]) for p in points if int(p["n"]) >= 512})
    palette = {n: c for n, c in zip(n_values, ["#264653", "#e76f51", "#2a9d8f", "#e9c46a"])}
    marker_map = {0.5: "o", 0.8: "s", 1.2: "^"}

    for n in n_values:
        subset = [p for p in points if int(p["n"]) == n]
        subset = sorted(subset, key=lambda x: float(x["theta"]))
        x = [p["final_position_error_pct"] for p in subset]
        y = [p["speedup_vs_baseline"] for p in subset]
        ax.plot(x, y, color=palette[n], linewidth=2, alpha=0.9, label=f"N={n}")
        for p in subset:
            ax.scatter(
                p["final_position_error_pct"],
                p["speedup_vs_baseline"],
                color=palette[n],
                s=80,
                marker=marker_map.get(float(p["theta"]), "o"),
                edgecolors="#111111",
                linewidths=0.4,
            )

    ax.axhline(1.0, color="#b23a48", linestyle="--", linewidth=1.5, label="No speedup")
    ax.set_xlabel("Final Position Error (%)")
    ax.set_ylabel("Speedup vs Baseline (x)")
    ax.set_title("Barnes-Hut Error-Speed Tradeoff (N>=512)")
    ax.legend(loc="upper right", fontsize=10)

    save(fig, "claim_03_barnes_hut_speed_error_tradeoff")
    plt.close(fig)


def figure_claim_04(stats: dict, baseline_metrics: dict) -> None:
    grid = stats["sensitivity"]["grid"]
    dt_values = sorted({float(r["dt"]) for r in grid})
    soft_values = sorted({float(r["softening"]) for r in grid})

    mat = np.zeros((len(soft_values), len(dt_values)), dtype=np.float64)
    for r in grid:
        i = soft_values.index(float(r["softening"]))
        j = dt_values.index(float(r["dt"]))
        mat[i, j] = float(r["median_energy_drift_pct"])

    runtime_n256 = next(row for row in baseline_metrics["results"] if int(row["n"]) == 256)["mean_step_time_ms"]

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8))
    hm = axes[0].imshow(mat, cmap="YlOrRd", aspect="auto")
    axes[0].set_xticks(range(len(dt_values)), [f"{v:.4f}" for v in dt_values])
    axes[0].set_yticks(range(len(soft_values)), [f"{v:.4f}" for v in soft_values])
    axes[0].set_xlabel("dt")
    axes[0].set_ylabel("softening")
    axes[0].set_title("Median Energy Drift (%)")
    fig.colorbar(hm, ax=axes[0], fraction=0.046, pad=0.04)

    axes[1].bar(["Observed N=256", "Threshold"], [runtime_n256, 1.0], color=["#457b9d", "#2a9d8f"])
    axes[1].set_ylabel("Runtime per Step (ms)")
    axes[1].set_title("Runtime Threshold Gap")
    axes[1].axhline(1.0, color="#1b4332", linestyle="--", linewidth=1.2)

    fig.suptitle("Claim 04: Sensitivity and Runtime Constraint", fontsize=16)
    save(fig, "claim_04_sensitivity_and_runtime_gap")
    plt.close(fig)


def main() -> int:
    setup_style()
    symplectic_eval = load_json(ROOT / "results" / "research" / "symplectic_eval.json")
    scaling_eval = load_json(ROOT / "results" / "research" / "scaling_eval.json")
    stats = load_json(ROOT / "results" / "experiments" / "statistics.json")
    baseline_metrics = load_json(ROOT / "results" / "baseline" / "metrics.json")

    figure_claim_01(symplectic_eval)
    figure_claim_02(symplectic_eval)
    figure_claim_03(scaling_eval)
    figure_claim_04(stats, baseline_metrics)
    print(json.dumps({"figures": str(FIG_DIR)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
