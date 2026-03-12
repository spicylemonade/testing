#!/usr/bin/env python3
"""Generate manuscript-only schematic figures for the H1 paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURE_ROOT = REPO_ROOT / "figures"

PALETTE = {
    "source": "#0f766e",
    "route": "#1d4ed8",
    "join": "#9a3412",
    "selector": "#7c3aed",
    "pump": "#0f172a",
    "store": "#9f1239",
    "note": "#334155",
    "bg": "#fbfaf7",
    "panel": "#f8f5ef",
}


def rounded_box(ax, x, y, w, h, label, fc, ec="#334155", fontsize=12, lw=1.8):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fontsize, color="#0f172a")
    return patch


def arrow(ax, x0, y0, x1, y1, color="#334155", lw=2.0, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle=style,
            mutation_scale=14,
            linewidth=lw,
            color=color,
        )
    )


def draw_panel(ax, title, variant):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(PALETTE["panel"])
    ax.text(0.03, 0.95, title, fontsize=15, fontweight="bold", ha="left", va="top", color="#111827")

    rounded_box(ax, 0.05, 0.68, 0.18, 0.16, "Source A", PALETTE["source"])
    rounded_box(ax, 0.05, 0.28, 0.18, 0.16, "Source B", PALETTE["source"])

    if variant == "fixed":
        rounded_box(ax, 0.30, 0.68, 0.18, 0.16, "FW\nRouter", "#dbeafe")
        rounded_box(ax, 0.56, 0.68, 0.18, 0.16, "Startup\nPump", "#e2e8f0")
        rounded_box(ax, 0.80, 0.68, 0.14, 0.16, "$C_{store}$", "#ffe4e6")
        arrow(ax, 0.23, 0.76, 0.30, 0.76, PALETTE["route"])
        arrow(ax, 0.48, 0.76, 0.56, 0.76, PALETTE["pump"])
        arrow(ax, 0.74, 0.76, 0.80, 0.76, PALETTE["store"])
        ax.text(0.38, 0.55, "Only one routed branch participates.", fontsize=11, ha="center", color=PALETTE["note"])
        ax.text(0.14, 0.16, "Branch B is measured but unused.", fontsize=10.5, ha="left", color=PALETTE["note"])

    elif variant == "nonaware":
        rounded_box(ax, 0.28, 0.68, 0.16, 0.16, "FW\nRouter", "#dbeafe")
        rounded_box(ax, 0.28, 0.28, 0.16, 0.16, "FW\nRouter", "#dbeafe")
        rounded_box(ax, 0.52, 0.45, 0.16, 0.18, "Hard\nJoin", "#fed7aa")
        rounded_box(ax, 0.76, 0.45, 0.16, 0.18, "Startup\nPump", "#e2e8f0")
        rounded_box(ax, 0.76, 0.14, 0.16, 0.14, "$C_{store}$", "#ffe4e6")
        arrow(ax, 0.23, 0.76, 0.28, 0.76, PALETTE["route"])
        arrow(ax, 0.23, 0.36, 0.28, 0.36, PALETTE["route"])
        arrow(ax, 0.44, 0.76, 0.52, 0.58, PALETTE["join"])
        arrow(ax, 0.44, 0.36, 0.52, 0.50, PALETTE["join"])
        arrow(ax, 0.68, 0.54, 0.76, 0.54, PALETTE["pump"])
        arrow(ax, 0.84, 0.45, 0.84, 0.28, PALETTE["store"])
        ax.text(0.58, 0.22, "Joined buses can leak or\nfight before handoff.", fontsize=11, ha="center", color=PALETTE["note"])

    else:
        rounded_box(ax, 0.28, 0.68, 0.16, 0.16, "FW\nRouter", "#dbeafe")
        rounded_box(ax, 0.28, 0.28, 0.16, 0.16, "FW\nRouter", "#dbeafe")
        rounded_box(ax, 0.52, 0.45, 0.18, 0.18, "Packet\nSelector", "#ede9fe")
        rounded_box(ax, 0.78, 0.45, 0.14, 0.18, "Startup\nPump", "#e2e8f0")
        rounded_box(ax, 0.78, 0.14, 0.14, 0.14, "$C_{store}$", "#ffe4e6")
        arrow(ax, 0.23, 0.76, 0.28, 0.76, PALETTE["route"])
        arrow(ax, 0.23, 0.36, 0.28, 0.36, PALETTE["route"])
        arrow(ax, 0.44, 0.76, 0.52, 0.58, PALETTE["selector"])
        arrow(ax, 0.44, 0.36, 0.52, 0.50, PALETTE["selector"])
        arrow(ax, 0.70, 0.54, 0.78, 0.54, PALETTE["pump"])
        arrow(ax, 0.85, 0.45, 0.85, 0.28, PALETTE["store"])
        ax.text(0.62, 0.18, "$w_A(t), w_B(t) \\geq 0$ and $w_A+w_B=1$", fontsize=11, ha="center", color=PALETTE["note"])
        ax.text(0.03, 0.16, "RC-ranked: scout RC windows", fontsize=10.5, ha="left", color=PALETTE["note"])
        ax.text(0.03, 0.10, "Blind packet: fixed 0.5 / 0.5 weights", fontsize=10.5, ha="left", color=PALETTE["note"])
        ax.text(0.03, 0.04, "TC-ranked: fast-slow dual-window score", fontsize=10.5, ha="left", color=PALETTE["note"])


def make_topology_figure():
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.8), facecolor=PALETTE["bg"])
    for ax in axes:
        ax.set_facecolor(PALETTE["bg"])

    draw_panel(axes[0], "Fixed Startup Path", "fixed")
    draw_panel(axes[1], "Nonaware Hard Join", "nonaware")
    draw_panel(axes[2], "Packet-Gated Family", "packet")

    fig.suptitle(
        "Topology Contrast Behind the H1 Falsification Result",
        fontsize=19,
        fontweight="bold",
        y=0.98,
        color="#111827",
    )
    fig.text(
        0.5,
        0.005,
        "The decisive comparison is not fixed versus RC-ranked; it is hard join versus packetized isolation, and then source-aware ranking versus blind packet allocation.",
        ha="center",
        fontsize=11.5,
        color=PALETTE["note"],
    )

    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    stem = FIGURE_ROOT / "h1_topology_contrast"
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_topology_figure()
