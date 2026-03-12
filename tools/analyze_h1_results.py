#!/usr/bin/env python3
"""Generate publication-oriented analysis artifacts for the H1 startup lane."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


REPO_ROOT = Path(__file__).resolve().parents[1]
LANE_ROOT = REPO_ROOT / "results" / "concept_evolve" / "tree" / "001_packet_scout_handoff_root"
TABLE_ROOT = LANE_ROOT / "tables"
FIGURE_ROOT = REPO_ROOT / "figures"

STARTUP_RESULTS = TABLE_ROOT / "startup_results.csv"
FALSIFIER_RESULTS = TABLE_ROOT / "falsifier_results.csv"
ROBUSTNESS_RESULTS = TABLE_ROOT / "robustness_results.csv"

SENSITIVITY_TABLE = TABLE_ROOT / "analysis_sensitivity.csv"
PAIRWISE_TABLE = TABLE_ROOT / "analysis_pairwise.csv"
ABLATION_TABLE = TABLE_ROOT / "ablation_pairwise.csv"
ANALYSIS_SUMMARY = TABLE_ROOT / "analysis_summary.json"
ABLATION_SUMMARY = TABLE_ROOT / "ablation_summary.json"

FIG_PRIMARY = FIGURE_ROOT / "h1_primary_matrix_heatmap"
FIG_FALSIFIER = FIGURE_ROOT / "h1_falsifier_boundary"
FIG_ACCOUNTING = FIGURE_ROOT / "h1_metric_accounting"
FIG_ABLATION = FIGURE_ROOT / "h1_ablation_tradeoff"
FIG_ROBUSTNESS = FIGURE_ROOT / "h1_robustness_ci"

DESIGN_ORDER = ["champion", "fixed", "nonaware", "source_blind", "time_constant_ranked"]
DESIGN_LABELS = {
    "champion": "RC-Ranked",
    "fixed": "Fixed",
    "nonaware": "Nonaware",
    "source_blind": "Blind Packet",
    "time_constant_ranked": "TC Ranked",
}
PALETTE = {
    "champion": "#1b4f72",
    "fixed": "#9c6644",
    "nonaware": "#7f8c8d",
    "source_blind": "#0e7490",
    "time_constant_ranked": "#bc4b51",
}
FACTOR_SPECS = [
    ("polarity_mode", "Polarity", ["same", "mixed"]),
    ("ratio_b_to_a", "Impedance Ratio", [1, 5, 20]),
    ("ramp_mvps", "Ramp (mV/s)", [0.1, 1.0, 10.0, 100.0]),
]


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "axes.facecolor": "#fbfaf7",
        "figure.facecolor": "#fbfaf7",
        "savefig.facecolor": "#fbfaf7",
        "axes.edgecolor": "#334155",
        "axes.linewidth": 0.8,
        "grid.color": "#d6d3d1",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "legend.frameon": False,
        "xtick.color": "#1f2937",
        "ytick.color": "#1f2937",
    }
)
sns.set_theme(style="whitegrid")


def load_table(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    numeric_columns = [
        "voltage_mv",
        "voc_a_mv",
        "voc_b_mv",
        "ramp_mvps",
        "ratio_b_to_a",
        "startup_ok",
        "t_handoff_s",
        "t_handoff_fall_s",
        "t_handoff_rise2_s",
        "e_backdrive_j",
        "e_ctrl_j",
        "e_backdrive_full_j",
        "e_ctrl_full_j",
        "vstore_final_v",
    ]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def save_figure(fig: plt.Figure, path_stem: Path) -> None:
    path_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(path_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def summarize_sensitivity(startup: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for factor, _, values in FACTOR_SPECS:
        for value in values:
            for design in DESIGN_ORDER:
                subset = startup[(startup["design"] == design) & (startup[factor] == value)]
                if subset.empty:
                    continue
                success = subset[subset["startup_ok"] >= 0.5]
                rows.append(
                    {
                        "factor": factor,
                        "value": value,
                        "design": design,
                        "total_cases": int(len(subset)),
                        "startup_successes": int((subset["startup_ok"] >= 0.5).sum()),
                        "startup_success_rate": float((subset["startup_ok"] >= 0.5).mean()),
                        "median_t_handoff_s_success": success["t_handoff_s"].median(),
                        "median_e_ctrl_j_success": success["e_ctrl_j"].median(),
                        "median_e_ctrl_full_j_success": success["e_ctrl_full_j"].median(),
                    }
                )
    return pd.DataFrame(rows)


def summarize_pairwise(startup: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for baseline in ["fixed", "nonaware", "source_blind", "time_constant_ranked"]:
        for factor, _, values in FACTOR_SPECS:
            for value in values:
                champion = startup[(startup["design"] == "champion") & (startup[factor] == value)].set_index("case_id")
                rival = startup[(startup["design"] == baseline) & (startup[factor] == value)].set_index("case_id")
                common = champion.index.intersection(rival.index)
                if common.empty:
                    continue
                champion_common = champion.loc[common]
                rival_common = rival.loc[common]
                rows.append(
                    {
                        "comparison": baseline,
                        "factor": factor,
                        "value": value,
                        "total_cases": int(len(common)),
                        "champion_better_startup_cases": int((champion_common["startup_ok"] > rival_common["startup_ok"]).sum()),
                        "champion_faster_cases": int(
                            (
                                (champion_common["startup_ok"] >= 0.5)
                                & (rival_common["startup_ok"] >= 0.5)
                                & (champion_common["t_handoff_s"] < rival_common["t_handoff_s"])
                            ).sum()
                        ),
                        "champion_lower_ctrl_cases": int((champion_common["e_ctrl_j"] < rival_common["e_ctrl_j"]).sum()),
                        "champion_lower_backdrive_cases": int((champion_common["e_backdrive_j"] < rival_common["e_backdrive_j"]).sum()),
                    }
                )
    return pd.DataFrame(rows)


def summarize_ablation(startup: pd.DataFrame, falsifier: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    pairwise_rows = []
    summary: dict[str, dict[str, float | int | None]] = {}
    for suite_name, frame in [("startup", startup), ("falsifier", falsifier)]:
        suite_summary = {}
        for design in DESIGN_ORDER:
            subset = frame[frame["design"] == design]
            if subset.empty:
                continue
            suite_summary[design] = {
                "cases": int(len(subset)),
                "startup_successes": int((subset["startup_ok"] >= 0.5).sum()),
                "median_t_handoff_s_success": subset.loc[subset["startup_ok"] >= 0.5, "t_handoff_s"].median(),
                "median_e_ctrl_j": subset["e_ctrl_j"].median(),
                "median_e_backdrive_j": subset["e_backdrive_j"].median(),
            }
        summary[suite_name] = suite_summary

    for baseline in ["source_blind", "time_constant_ranked"]:
        champion = startup[startup["design"] == "champion"].set_index("case_id")
        rival = startup[startup["design"] == baseline].set_index("case_id")
        common = champion.index.intersection(rival.index)
        if common.empty:
            continue
        champion_common = champion.loc[common]
        rival_common = rival.loc[common]
        for case_id in common:
            pairwise_rows.append(
                {
                    "case_id": case_id,
                    "comparison": baseline,
                    "champion_startup_ok": champion_common.at[case_id, "startup_ok"],
                    "rival_startup_ok": rival_common.at[case_id, "startup_ok"],
                    "champion_t_handoff_s": champion_common.at[case_id, "t_handoff_s"],
                    "rival_t_handoff_s": rival_common.at[case_id, "t_handoff_s"],
                    "champion_e_ctrl_j": champion_common.at[case_id, "e_ctrl_j"],
                    "rival_e_ctrl_j": rival_common.at[case_id, "e_ctrl_j"],
                }
            )
    return pd.DataFrame(pairwise_rows), summary


def plot_primary_matrix(sensitivity: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.8), constrained_layout=True)
    cmap = sns.color_palette(["#f8fafc", "#d9f99d", "#4d7c0f"], as_cmap=True)
    for ax, (factor, title, values) in zip(axes, FACTOR_SPECS):
        pivot = (
            sensitivity[sensitivity["factor"] == factor]
            .pivot(index="design", columns="value", values="startup_success_rate")
            .reindex(DESIGN_ORDER)
        )
        annot = (
            sensitivity[sensitivity["factor"] == factor]
            .pivot(index="design", columns="value", values="startup_successes")
            .reindex(DESIGN_ORDER)
        )
        sns.heatmap(
            pivot,
            ax=ax,
            cmap=cmap,
            vmin=0,
            vmax=1,
            annot=annot,
            fmt=".0f",
            cbar=ax is axes[-1],
            linewidths=0.8,
            linecolor="#e5e7eb",
        )
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_yticklabels([DESIGN_LABELS.get(label.get_text(), label.get_text()) for label in ax.get_yticklabels()], rotation=0)
    fig.suptitle("Primary Startup Matrix: Grouped Success Counts", y=1.03, fontsize=16, fontweight="bold")
    save_figure(fig, FIG_PRIMARY)


def plot_falsifier_matrix(falsifier: pd.DataFrame) -> None:
    case_order = sorted(falsifier["case_id"].unique())
    design_order = [design for design in DESIGN_ORDER if design in falsifier["design"].unique()]
    matrix = (
        falsifier.assign(score=falsifier["startup_ok"].fillna(0) + (falsifier["t_handoff_fall_s"].notna() * 0.5))
        .pivot(index="design", columns="case_id", values="score")
        .reindex(index=design_order, columns=case_order)
    )
    fig, ax = plt.subplots(figsize=(14.5, 4.6), constrained_layout=True)
    sns.heatmap(matrix, ax=ax, cmap=sns.color_palette(["#991b1b", "#f59e0b", "#0f766e"], as_cmap=True), vmin=0, vmax=1.5, cbar=False, linewidths=0.8, linecolor="#e5e7eb")
    for y, design in enumerate(design_order):
        for x, case_id in enumerate(case_order):
            cell = falsifier[(falsifier["design"] == design) & (falsifier["case_id"] == case_id)].iloc[0]
            label = "S" if cell["startup_ok"] >= 0.5 else "F"
            extras = []
            if pd.notna(cell["t_handoff_fall_s"]):
                extras.append("fall")
            if pd.notna(cell["t_handoff_rise2_s"]):
                extras.append("rise2")
            subtitle = " / ".join(extras) if extras else f"B={cell['e_backdrive_j']:.1e}"
            ax.text(x + 0.5, y + 0.34, label, ha="center", va="center", fontsize=12, fontweight="bold", color="#111827")
            ax.text(x + 0.5, y + 0.72, subtitle, ha="center", va="center", fontsize=8, color="#111827")
    ax.set_title("Expanded Falsifier Matrix")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticklabels([DESIGN_LABELS[d] for d in design_order], rotation=0)
    save_figure(fig, FIG_FALSIFIER)


def plot_metric_accounting(startup: pd.DataFrame) -> None:
    summary = []
    for design in DESIGN_ORDER:
        subset = startup[(startup["design"] == design) & (startup["startup_ok"] >= 0.5)]
        if subset.empty:
            continue
        summary.append({"design": design, "metric": "Pre-handoff", "median_e_ctrl_j": subset["e_ctrl_j"].median()})
        summary.append({"design": design, "metric": "Full window", "median_e_ctrl_j": subset["e_ctrl_full_j"].median()})
    frame = pd.DataFrame(summary)
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    sns.barplot(
        data=frame,
        x="design",
        y="median_e_ctrl_j",
        hue="metric",
        palette=["#0f766e", "#9ca3af"],
        ax=ax,
    )
    ax.set_yscale("log")
    ax.set_xlabel("")
    ax.set_ylabel("Median Control Energy (J, log scale)")
    ax.set_xticklabels([DESIGN_LABELS[label.get_text()] for label in ax.get_xticklabels()], rotation=20, ha="right")
    ax.set_title("Metric Contract Repair: Pre-Handoff vs Full-Window Control Energy")
    save_figure(fig, FIG_ACCOUNTING)


def plot_ablation_tradeoff(startup: pd.DataFrame, falsifier: pd.DataFrame) -> None:
    rows = []
    for design in DESIGN_ORDER:
        startup_subset = startup[startup["design"] == design]
        falsifier_subset = falsifier[falsifier["design"] == design]
        if startup_subset.empty or falsifier_subset.empty:
            continue
        rows.append(
            {
                "design": design,
                "startup_successes": int((startup_subset["startup_ok"] >= 0.5).sum()),
                "falsifier_successes": int((falsifier_subset["startup_ok"] >= 0.5).sum()),
                "median_t_handoff_s": startup_subset.loc[startup_subset["startup_ok"] >= 0.5, "t_handoff_s"].median(),
                "median_e_ctrl_j": startup_subset["e_ctrl_j"].median(),
            }
        )
    frame = pd.DataFrame(rows)
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.4), constrained_layout=True)
    sns.barplot(data=frame, x="design", y="startup_successes", palette=PALETTE, ax=axes[0, 0])
    axes[0, 0].set_title("Startup Matrix Successes")
    sns.barplot(data=frame, x="design", y="falsifier_successes", palette=PALETTE, ax=axes[0, 1])
    axes[0, 1].set_title("Falsifier Successes")
    sns.barplot(data=frame, x="design", y="median_t_handoff_s", palette=PALETTE, ax=axes[1, 0])
    axes[1, 0].set_title("Median Startup Handoff Time")
    sns.barplot(data=frame, x="design", y="median_e_ctrl_j", palette=PALETTE, ax=axes[1, 1])
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_title("Median Pre-Handoff Control Energy")
    for ax in axes.flat:
        ax.set_xlabel("")
        ax.set_xticklabels([DESIGN_LABELS[label.get_text()] for label in ax.get_xticklabels()], rotation=20, ha="right")
    fig.suptitle("Ablation Tradeoffs Across the Expanded Evidence Pack", y=1.02, fontsize=16, fontweight="bold")
    save_figure(fig, FIG_ABLATION)


def plot_robustness(robustness: pd.DataFrame) -> None:
    if robustness.empty:
        return
    case_order = list(dict.fromkeys(robustness["case_id"].tolist()))
    fig, axes = plt.subplots(1, len(case_order), figsize=(4.2 * len(case_order), 4.8), constrained_layout=True)
    if len(case_order) == 1:
        axes = [axes]
    for ax, case_id in zip(axes, case_order):
        subset = robustness[robustness["case_id"] == case_id]
        rows = []
        for design in DESIGN_ORDER:
            design_subset = subset[subset["design"] == design]
            if design_subset.empty:
                continue
            successes = int((design_subset["startup_ok"] >= 0.5).sum())
            rate = successes / len(design_subset)
            z = 1.96
            denom = 1 + z**2 / len(design_subset)
            center = (rate + z**2 / (2 * len(design_subset))) / denom
            margin = z * np.sqrt((rate * (1 - rate) + z**2 / (4 * len(design_subset))) / len(design_subset)) / denom
            rows.append(
                {
                    "design": design,
                    "rate": rate,
                    "err_low": rate - max(0.0, center - margin),
                    "err_high": min(1.0, center + margin) - rate,
                }
            )
        frame = pd.DataFrame(rows)
        ax.bar(frame["design"], frame["rate"], color=[PALETTE[d] for d in frame["design"]], alpha=0.9)
        ax.errorbar(
            x=np.arange(len(frame)),
            y=frame["rate"],
            yerr=np.vstack([frame["err_low"], frame["err_high"]]),
            fmt="none",
            ecolor="#111827",
            capsize=3,
            linewidth=1.2,
        )
        ax.set_ylim(0, 1.05)
        ax.set_title(case_id)
        ax.set_xlabel("")
        ax.set_ylabel("Startup Probability")
        ax.set_xticks(np.arange(len(frame)))
        ax.set_xticklabels([DESIGN_LABELS[d] for d in frame["design"]], rotation=20, ha="right")
    fig.suptitle("Robustness Study: Startup Probability With 95% Wilson Intervals", y=1.03, fontsize=16, fontweight="bold")
    save_figure(fig, FIG_ROBUSTNESS)


def main() -> int:
    startup = load_table(STARTUP_RESULTS)
    falsifier = load_table(FALSIFIER_RESULTS)
    robustness = load_table(ROBUSTNESS_RESULTS) if ROBUSTNESS_RESULTS.exists() else pd.DataFrame()

    sensitivity = summarize_sensitivity(startup)
    pairwise = summarize_pairwise(startup)
    ablation_pairwise, ablation_summary = summarize_ablation(startup, falsifier)

    sensitivity.to_csv(SENSITIVITY_TABLE, index=False)
    pairwise.to_csv(PAIRWISE_TABLE, index=False)
    ablation_pairwise.to_csv(ABLATION_TABLE, index=False)
    ABLATION_SUMMARY.write_text(json.dumps(ablation_summary, indent=2) + "\n")

    plot_primary_matrix(sensitivity)
    plot_falsifier_matrix(falsifier)
    plot_metric_accounting(startup)
    plot_ablation_tradeoff(startup, falsifier)
    plot_robustness(robustness)

    summary = {
        "startup_source": str(STARTUP_RESULTS.relative_to(REPO_ROOT)),
        "falsifier_source": str(FALSIFIER_RESULTS.relative_to(REPO_ROOT)),
        "robustness_source": str(ROBUSTNESS_RESULTS.relative_to(REPO_ROOT)) if ROBUSTNESS_RESULTS.exists() else None,
        "sensitivity_table": str(SENSITIVITY_TABLE.relative_to(REPO_ROOT)),
        "pairwise_table": str(PAIRWISE_TABLE.relative_to(REPO_ROOT)),
        "ablation_table": str(ABLATION_TABLE.relative_to(REPO_ROOT)),
        "ablation_summary": str(ABLATION_SUMMARY.relative_to(REPO_ROOT)),
        "figures": [
            str(FIG_PRIMARY.with_suffix(".pdf").relative_to(REPO_ROOT)),
            str(FIG_FALSIFIER.with_suffix(".pdf").relative_to(REPO_ROOT)),
            str(FIG_ACCOUNTING.with_suffix(".pdf").relative_to(REPO_ROOT)),
            str(FIG_ABLATION.with_suffix(".pdf").relative_to(REPO_ROOT)),
            str(FIG_ROBUSTNESS.with_suffix(".pdf").relative_to(REPO_ROOT)) if ROBUSTNESS_RESULTS.exists() else None,
        ],
        "design_order": DESIGN_ORDER,
    }
    ANALYSIS_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")

    print(
        json.dumps(
            {
                "sensitivity_table": str(SENSITIVITY_TABLE.relative_to(REPO_ROOT)),
                "pairwise_table": str(PAIRWISE_TABLE.relative_to(REPO_ROOT)),
                "ablation_table": str(ABLATION_TABLE.relative_to(REPO_ROOT)),
                "summary": str(ANALYSIS_SUMMARY.relative_to(REPO_ROOT)),
                "primary_figure": str(FIG_PRIMARY.with_suffix(".pdf").relative_to(REPO_ROOT)),
                "falsifier_figure": str(FIG_FALSIFIER.with_suffix(".pdf").relative_to(REPO_ROOT)),
                "accounting_figure": str(FIG_ACCOUNTING.with_suffix(".pdf").relative_to(REPO_ROOT)),
                "ablation_figure": str(FIG_ABLATION.with_suffix(".pdf").relative_to(REPO_ROOT)),
                "robustness_figure": str(FIG_ROBUSTNESS.with_suffix(".pdf").relative_to(REPO_ROOT))
                if ROBUSTNESS_RESULTS.exists()
                else None,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
