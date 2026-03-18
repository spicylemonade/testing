#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hadamard668.cellar import control_79_panel, exposed_prefix_indices, panel_report

FIG_DIR = ROOT / "figures"
ANALYSIS_DIR = ROOT / "results" / "analysis"
EXPERIMENT_DIR = ROOT / "results" / "experiments"
METRICS_PATH = ANALYSIS_DIR / "cellar_paper_metrics.json"

PALETTE = {
    "navy": "#1f3b5b",
    "teal": "#2f7f6f",
    "sand": "#c8a977",
    "rust": "#b55d3e",
    "rose": "#c05a8f",
    "olive": "#7a8c4b",
    "ink": "#23262f",
    "slate": "#708090",
    "mist": "#dde4ea",
    "cloud": "#f3f5f7",
    "gold": "#d49b2f",
}

KIND_COLORS = {
    "h1_target_best": PALETTE["navy"],
    "seed_projection": PALETTE["rust"],
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.family": "DejaVu Serif",
            "mathtext.fontset": "stix",
            "font.size": 10.5,
            "axes.labelsize": 10.5,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.edgecolor": PALETTE["ink"],
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": PALETTE["ink"],
            "ytick.color": PALETTE["ink"],
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "grid.color": "#d8dee5",
            "grid.linewidth": 0.7,
            "grid.alpha": 0.9,
            "legend.frameon": False,
            "legend.fontsize": 9.2,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)



def panel_label(ax, label: str) -> None:
    ax.text(
        -0.08,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        color=PALETTE["ink"],
        va="bottom",
    )



def add_box(ax, xy, width, height, text, facecolor, edgecolor=PALETTE["ink"], fontsize=9.8):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=facecolor,
        edgecolor=edgecolor,
        lw=1.0,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=PALETTE["ink"],
        wrap=True,
    )



def add_arrow(ax, start, end, color=PALETTE["ink"], style="-|>"):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=12,
        lw=1.2,
        color=color,
        connectionstyle="arc3,rad=0.0",
    )
    ax.add_patch(arrow)



def exposure_matrix(length: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for prefix_index in range(length - 1):
        row: list[int] = []
        for cut in range(1, length):
            exposed = set(exposed_prefix_indices(length, cut))
            row.append(1 if prefix_index < cut and prefix_index in exposed else 0)
        matrix.append(row)
    return matrix



def compute_metrics() -> dict:
    phase6 = json.loads((EXPERIMENT_DIR / "cellar_phase6.json").read_text())
    control_family = {}
    for free_suffix_length in [10, 12, 14]:
        report = panel_report(control_79_panel(free_suffix_length=free_suffix_length))
        control_family[str(free_suffix_length)] = {
            "label": report["label"],
            "prefix_count": int(report["prefix_count"]),
            "exact_completion_count": int(report["exact_completion_count"]),
            "extendable_prefix_count": int(report["extendable_prefix_count"]),
            "boundary_frontier_size": int(report["boundary_debt_report"]["frontier_size"]),
            "cellar_frontier_size": int(report["cellar_report"]["frontier_size"]),
            "boundary_group_count": int(report["boundary_debt_report"]["group_count"]),
            "cellar_group_count": int(report["cellar_report"]["group_count"]),
            "boundary_prefix_identifying_ratio": int(report["boundary_debt_report"]["group_count"]) / float(int(report["prefix_count"])),
            "cellar_prefix_identifying_ratio": int(report["cellar_report"]["group_count"]) / float(int(report["prefix_count"])),
        }

    panels = []
    for panel in phase6["panels"]:
        panels.append(
            {
                "label": str(panel["label"]),
                "anchor_kind": str(panel["anchor_kind"]),
                "prefix_count": int(panel["prefix_count"]),
                "exact_completion_count": int(panel["exact_completion_count"]),
                "extendable_prefix_count": int(panel["extendable_prefix_count"]),
                "boundary_frontier_size": int(panel["boundary_debt_report"]["frontier_size"]),
                "cellar_frontier_size": int(panel["cellar_report"]["frontier_size"]),
                "boundary_group_count": int(panel["boundary_debt_report"]["group_count"]),
                "cellar_group_count": int(panel["cellar_report"]["group_count"]),
            }
        )

    metrics = {
        "regularity_claim": phase6["regularity_claim"],
        "control_family": control_family,
        "phase6_panels": panels,
        "exposure": {
            "79": exposure_matrix(79),
            "167": exposure_matrix(167),
        },
    }
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    return metrics



def figure_cellar_mechanism() -> None:
    fig = plt.figure(figsize=(12.2, 4.8), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.0, 1.1])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[0, 2])

    for ax in [ax0, ax1, ax2]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

    ax0.text(0.5, 0.92, "Tail-panel encoding", ha="center", fontsize=12, fontweight="bold")
    ax0.add_patch(Rectangle((0.08, 0.58), 0.74, 0.12, facecolor=PALETTE["cloud"], edgecolor=PALETTE["ink"], lw=1.0))
    ax0.add_patch(Rectangle((0.08, 0.58), 0.50, 0.12, facecolor="#e8eef5", edgecolor=PALETTE["ink"], lw=1.0))
    ax0.add_patch(Rectangle((0.58, 0.58), 0.24, 0.12, facecolor="#e8f3ef", edgecolor=PALETTE["ink"], lw=1.0))
    ax0.text(0.33, 0.64, "fixed base prefix\n$B>h$", ha="center", va="center", fontsize=9.5)
    ax0.text(0.70, 0.64, "free tail\n$m$", ha="center", va="center", fontsize=9.5)
    ax0.add_patch(Rectangle((0.08, 0.38), 0.22, 0.08, facecolor="#f6f1e7", edgecolor=PALETTE["ink"], lw=0.9))
    ax0.add_patch(Rectangle((0.42, 0.38), 0.22, 0.08, facecolor="#f6f1e7", edgecolor=PALETTE["ink"], lw=0.9))
    ax0.text(0.19, 0.42, "left boundary\n$\\lambda$", ha="center", va="center", fontsize=9.4)
    ax0.text(0.53, 0.42, "right boundary\n$\\rho$", ha="center", va="center", fontsize=9.4)
    add_arrow(ax0, (0.19, 0.58), (0.19, 0.46), color=PALETTE["sand"])
    add_arrow(ax0, (0.53, 0.58), (0.53, 0.46), color=PALETTE["sand"])
    add_box(ax0, (0.10, 0.12), 0.60, 0.16, "Boundary debt stores assigned pair vector, fixed left boundary bits, current right boundary bits, and remaining weight.", "#eef5f3")
    panel_label(ax0, "a")

    ax1.text(0.5, 0.92, "Dyadic cellar stack", ha="center", fontsize=12, fontweight="bold")
    bits = [(0.12, "1"), (0.24, "0"), (0.36, "1"), (0.48, "1"), (0.60, "0"), (0.72, "1")]
    for x, bit in bits:
        ax1.add_patch(Rectangle((x, 0.70), 0.08, 0.08, facecolor="white", edgecolor=PALETTE["ink"], lw=0.9))
        ax1.text(x + 0.04, 0.74, bit, ha="center", va="center")
    ax1.text(0.50, 0.82, "incoming suffix bits", ha="center", fontsize=9.4, color=PALETTE["ink"])
    add_box(ax1, (0.10, 0.46), 0.18, 0.10, "1", "#f5ece8")
    add_box(ax1, (0.30, 0.46), 0.18, 0.10, "0", "#f5ece8")
    add_box(ax1, (0.50, 0.46), 0.18, 0.10, "11", "#f5ece8")
    add_box(ax1, (0.22, 0.24), 0.26, 0.10, "10", "#edf3f7")
    add_box(ax1, (0.52, 0.24), 0.26, 0.10, "1101", "#edf3f7")
    add_arrow(ax1, (0.19, 0.46), (0.35, 0.34), color=PALETTE["teal"])
    add_arrow(ax1, (0.39, 0.46), (0.35, 0.34), color=PALETTE["teal"])
    add_arrow(ax1, (0.59, 0.46), (0.65, 0.34), color=PALETTE["teal"])
    add_arrow(ax1, (0.79, 0.46), (0.65, 0.34), color=PALETTE["teal"])
    ax1.text(0.50, 0.12, "Read one bit, push a length-1 cellar, then merge equal-size trailing blocks.", ha="center", fontsize=9.6)
    panel_label(ax1, "b")

    ax2.text(0.5, 0.92, "Matched comparator and exact oracle", ha="center", fontsize=12, fontweight="bold")
    add_box(ax2, (0.08, 0.68), 0.28, 0.14, "Cellar state\n(BD + stack)", "#e8f3ef", fontsize=9.3)
    add_box(ax2, (0.64, 0.68), 0.24, 0.14, "Static baseline\n(BD only)", "#e8eef5", fontsize=9.3)
    add_box(ax2, (0.26, 0.42), 0.48, 0.14, "Same tokenization, same exact tail-completion oracle, same canonical accounting, same budget.", "#f6f1e7")
    add_box(ax2, (0.26, 0.16), 0.48, 0.16, "Exact completion depends only on boundary debt plus the unread suffix.", "#edf3f7", fontsize=9.4)
    ax2.text(0.50, 0.08, r"$c_{axy}(k)=\alpha_x(k)+\beta^{\mathrm{cross}}_k(\rho_x,y)+\beta^{\mathrm{wrap}}_k(\lambda,y)+\beta^{\mathrm{int}}_k(y)$", ha="center", va="center", fontsize=8.9, color=PALETTE["ink"])
    add_arrow(ax2, (0.25, 0.68), (0.40, 0.56), color=PALETTE["teal"])
    add_arrow(ax2, (0.75, 0.68), (0.60, 0.56), color=PALETTE["navy"])
    add_arrow(ax2, (0.50, 0.42), (0.50, 0.32), color=PALETTE["ink"])
    panel_label(ax2, "c")

    save_figure(fig, "fig_cellar_mechanism")



def figure_cellar_results(metrics: dict) -> None:
    fig = plt.figure(figsize=(12.8, 8.4), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    cmap = LinearSegmentedColormap.from_list("cellar", [PALETTE["cloud"], PALETTE["teal"]])
    for ax, length, label in [(ax0, 79, "a"), (ax1, 167, "b")]:
        matrix = np.array(metrics["exposure"][str(length)])
        ax.imshow(matrix, origin="lower", aspect="auto", cmap=cmap, vmin=0, vmax=1)
        ax.set_title(f"Exposure map for n={length}")
        ax.set_xlabel("Cut position $t$")
        ax.set_ylabel("Prefix index $i$")
        xticks = [1, length // 4, length // 2, length - 1]
        yticks = [0, (length - 1) // 4, (length - 1) // 2, length - 2]
        ax.set_xticks([value - 1 for value in xticks], xticks)
        ax.set_yticks(yticks, yticks)
        panel_label(ax, label)

    suffixes = [10, 12, 14]
    exact = [metrics["control_family"][str(m)]["extendable_prefix_count"] for m in suffixes]
    boundary = [metrics["control_family"][str(m)]["boundary_frontier_size"] for m in suffixes]
    cellar = [metrics["control_family"][str(m)]["cellar_frontier_size"] for m in suffixes]
    ratio = [metrics["control_family"][str(m)]["boundary_prefix_identifying_ratio"] for m in suffixes]
    xpos = np.arange(len(suffixes))
    width = 0.22
    ax2.bar(xpos - width, exact, width=width, color=PALETTE["gold"], label="Exact extendable frontier")
    ax2.bar(xpos, boundary, width=width, color=PALETTE["navy"], label="Boundary debt")
    ax2.bar(xpos + width, cellar, width=width, color=PALETTE["teal"], label="Cellar stack")
    ax2.set_xticks(xpos, [f"tail {m}" for m in suffixes])
    ax2.set_ylabel("Frontier size on solved control")
    ax2.set_title("Held-out control family is already exact")
    ax2.grid(True, axis="y")
    ax2b = ax2.twinx()
    ax2b.plot(xpos, ratio, color=PALETTE["rust"], marker="o", lw=1.8)
    ax2b.set_ylim(0.0, 1.08)
    ax2b.set_ylabel("Boundary group count / prefix count")
    ax2.legend(loc="upper left")
    panel_label(ax2, "c")

    real_panels = [panel for panel in metrics["phase6_panels"] if panel["anchor_kind"] != "exact_control"]
    heat = np.array(
        [
            [panel["prefix_count"] for panel in real_panels],
            [panel["boundary_group_count"] for panel in real_panels],
            [panel["extendable_prefix_count"] for panel in real_panels],
            [panel["boundary_frontier_size"] for panel in real_panels],
            [panel["cellar_frontier_size"] for panel in real_panels],
        ],
        dtype=float,
    )
    shown = np.log10(heat + 1.0)
    im = ax3.imshow(shown, aspect="auto", cmap="Blues")
    labels = []
    for panel in real_panels:
        if panel["anchor_kind"] == "h1_target_best":
            labels.append(panel["label"].split("::")[-1])
        else:
            labels.append(panel["label"].split("::")[-1].replace("_mod", "\nmod "))
    ax3.set_xticks(np.arange(len(real_panels)), labels, rotation=25, ha="right")
    ax3.set_yticks(np.arange(5), ["weight-feasible\nprefixes", "boundary groups", "exact\nextendable", "boundary\nfrontier", "cellar\nfrontier"])
    ax3.set_title("Real-anchor stress packet: no surviving frontier")
    for row in range(shown.shape[0]):
        for col in range(shown.shape[1]):
            value = int(heat[row, col])
            ax3.text(col, row, str(value), ha="center", va="center", fontsize=8.8, color=PALETTE["ink"])
    for idx, panel in enumerate(real_panels):
        color = KIND_COLORS[panel["anchor_kind"]]
        ax3.add_patch(Rectangle((idx - 0.48, -0.62), 0.96, 0.08, facecolor=color, edgecolor="none", transform=ax3.transData, clip_on=False))
    ax3.text(0.02, -0.18, "navy = H1 best states, rust = degraded 668 seed projections", transform=ax3.transAxes, fontsize=8.8, color=PALETTE["ink"])
    panel_label(ax3, "d")

    cbar = fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label(r"$\log_{10}(\mathrm{count}+1)$")

    save_figure(fig, "fig_cellar_results")



def main() -> int:
    configure_style()
    metrics = compute_metrics()
    figure_cellar_mechanism()
    figure_cellar_results(metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
