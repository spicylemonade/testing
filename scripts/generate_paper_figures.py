#!/usr/bin/env python3
"""Generate publication-style figures for the arithmetic Kakeya paper."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


PALETTE = {
    "ink": "#1F2933",
    "muted": "#66788A",
    "panel": "#F8F4EC",
    "grid": "#D5CCBC",
    "blue": "#3A6EA5",
    "teal": "#1F9D8A",
    "green": "#4C9F70",
    "orange": "#D97706",
    "gold": "#C8A64E",
    "red": "#C44536",
    "purple": "#6C5B9A",
    "sand": "#EFE4D0",
}


LABEL_COLOR = {
    "(0,0)": "#D8D5CF",
    "(0,1)": "#4C9F70",
    "(1,0)": "#3A6EA5",
    "(1,1)": "#6C5B9A",
    "(2,-1)": "#D97706",
    "(2,1)": "#C08A00",
    "(1,2)": "#0E7490",
    "(3,-2)": "#C44536",
}


mpl.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "mathtext.fontset": "dejavuserif",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": PALETTE["muted"],
        "axes.linewidth": 1.0,
        "axes.labelcolor": PALETTE["ink"],
        "xtick.color": PALETTE["ink"],
        "ytick.color": PALETTE["ink"],
        "text.color": PALETTE["ink"],
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.8,
        "axes.grid": True,
        "axes.axisbelow": True,
        "legend.frameon": False,
        "figure.dpi": 140,
    }
)


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text())


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / f"{stem}.png", bbox_inches="tight", dpi=600)
    plt.close(fig)


def panel_label(ax: plt.Axes, text: str) -> None:
    ax.text(
        -0.08,
        1.05,
        text,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
    )


def rounded_box(
    ax: plt.Axes,
    xy: Tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    fc: str,
    ec: str,
    text_size: int = 10,
) -> None:
    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.4,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2.0,
        xy[1] + height / 2.0,
        text,
        ha="center",
        va="center",
        fontsize=text_size,
        linespacing=1.25,
    )


def arrow(ax: plt.Axes, start: Tuple[float, float], end: Tuple[float, float], color: str) -> None:
    patch = patches.FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.6,
        color=color,
        connectionstyle="arc3,rad=0.0",
    )
    ax.add_patch(patch)


def fig_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    rounded_box(
        ax,
        (0.02, 0.62),
        0.16,
        0.22,
        "Benchmark task\nscore $\\leq 1.675$",
        fc=PALETTE["sand"],
        ec=PALETTE["muted"],
    )
    rounded_box(
        ax,
        (0.22, 0.62),
        0.17,
        0.22,
        "Exact grid compiler\nand rational-span\nverifier",
        fc="#EAF2FB",
        ec=PALETTE["blue"],
    )
    rounded_box(
        ax,
        (0.43, 0.62),
        0.18,
        0.22,
        "Phase 4 pilot\nH1 one-seed kill,\nH2 local null",
        fc="#FDECEC",
        ec=PALETTE["red"],
    )
    rounded_box(
        ax,
        (0.65, 0.62),
        0.19,
        0.22,
        "Phase 6 audits\nH4/H5/H6, ledger,\ncontroller parity",
        fc="#FCF7EA",
        ec=PALETTE["gold"],
    )
    rounded_box(
        ax,
        (0.02, 0.20),
        0.20,
        0.22,
        "Direct asymmetric\ncontrols survive:\n$13/7$, $13/7$, $14/7$",
        fc="#EDF6EF",
        ec=PALETTE["green"],
    )
    rounded_box(
        ax,
        (0.29, 0.20),
        0.20,
        0.22,
        "Width-8 ledger:\nall matched reruns\nempty; legacy $29/14$\nunmatched",
        fc="#F7F2E8",
        ec=PALETTE["orange"],
    )
    rounded_box(
        ax,
        (0.56, 0.20),
        0.18,
        0.22,
        "Formal route kills:\none-seed and\nrow-quotient\ntheorems",
        fc="#F0ECF7",
        ec=PALETTE["purple"],
    )
    rounded_box(
        ax,
        (0.78, 0.20),
        0.18,
        0.22,
        "Final identity:\nbenchmark-and-\nfalsification paper,\nnot a CA solution",
        fc="#FDECEC",
        ec=PALETTE["red"],
    )

    arrow(ax, (0.18, 0.73), (0.22, 0.73), PALETTE["muted"])
    arrow(ax, (0.39, 0.73), (0.43, 0.73), PALETTE["muted"])
    arrow(ax, (0.61, 0.73), (0.65, 0.73), PALETTE["muted"])
    arrow(ax, (0.74, 0.62), (0.38, 0.42), PALETTE["muted"])
    arrow(ax, (0.50, 0.62), (0.65, 0.42), PALETTE["muted"])
    arrow(ax, (0.74, 0.20), (0.78, 0.31), PALETTE["muted"])
    arrow(ax, (0.22, 0.31), (0.29, 0.31), PALETTE["muted"])
    arrow(ax, (0.49, 0.31), (0.56, 0.31), PALETTE["muted"])

    ax.text(
        0.49,
        0.53,
        "same exact verifier\nfor proofs, search,\nand route audits",
        ha="center",
        va="center",
        fontsize=9,
        color=PALETTE["blue"],
    )
    ax.text(
        0.73,
        0.52,
        "no CA route beats\nmatched direct search",
        ha="center",
        va="center",
        fontsize=9,
        color=PALETTE["red"],
    )

    ax.text(
        0.02,
        0.95,
        "Repository endpoint after Phase 6: the exact pipeline eliminates every tested CA-positive lane and leaves only direct low-height asymmetric certificates above the target.",
        fontsize=12,
        ha="left",
        va="top",
    )
    save(fig, "figure1_pipeline")


def h1_identity_word(level: int) -> Tuple[str, ...]:
    word = ("L_a", "R_a")
    sigma = {
        "L_a": ("L_a", "M_a"),
        "M_a": ("M_a", "M_a"),
        "R_a": ("M_a", "R_a"),
    }
    for _ in range(level):
        word = tuple(symbol for state in word for symbol in sigma[state])
    return word


def draw_level1_word(ax: plt.Axes) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 4.8)
    ax.set_ylim(0, 1.7)
    word = h1_identity_word(1)
    face = {
        "L_a": "#EAF2FB",
        "M_a": "#F6F1E8",
        "R_a": "#EDF6EF",
    }
    incoming = ["closed", "carry_a", "carry_a", "carry_a"]
    outgoing = ["carry_a", "carry_a", "carry_a", "closed"]
    for i, state in enumerate(word):
        x = 0.25 + i * 1.1
        rounded_box(
            ax,
            (x, 0.45),
            0.8,
            0.55,
            state.replace("_", "\n"),
            fc=face[state],
            ec=PALETTE["muted"],
        )
        ax.text(x + 0.4, 1.18, incoming[i], ha="center", va="bottom", fontsize=9, color=PALETTE["muted"])
        ax.text(x + 0.4, 0.25, outgoing[i], ha="center", va="top", fontsize=9, color=PALETTE["muted"])
        ax.text(x + 0.4, 1.43, f"col {i + 1}", ha="center", va="bottom", fontsize=8)
    ax.text(0.25, 1.55, "Frozen H1 level-1 identity word", fontsize=11, ha="left", va="top")
    ax.text(0.25, 0.05, "Interfaces compose only by exact equality; the left seed is unique.", fontsize=9, ha="left")


def draw_extracted_h1(ax: plt.Axes) -> None:
    ax.set_axis_off()
    ax.set_xlim(0.4, 4.8)
    ax.set_ylim(-0.25, 1.45)
    width = 4
    for col in range(1, width + 1):
        x = col
        ax.plot([x, x], [0, 1], color=PALETTE["orange"], lw=3)
        ax.text(x + 0.07, 0.52, "$z$", fontsize=9, color=PALETTE["orange"])
        ax.scatter([x, x], [1, 0], s=62, color="white", edgecolors=PALETTE["ink"], zorder=3)
    for col in range(1, width):
        ax.plot([col, col + 1], [1, 1], color=PALETTE["blue"], lw=4)
        ax.text(col + 0.5, 1.08, "$u$", fontsize=9, color=PALETTE["blue"], ha="center")
        ax.plot([col, col + 1], [0, 0], color=PALETTE["grid"], lw=4)
        ax.text(col + 0.5, -0.08, "$0$", fontsize=9, color=PALETTE["muted"], ha="center")
    ax.scatter([1], [1], marker="s", s=120, color=PALETTE["red"], zorder=5)
    ax.text(0.55, 1.32, "Compiled corridor instance", fontsize=11, ha="left", va="top")
    ax.text(0.55, 1.10, "$f_1(1)=z$, $f_2(1,c)=u$, $f_2(2,c)=0$, $T=\\varnothing$.", fontsize=9, ha="left")
    ax.text(0.55, -0.20, "Every edge contributes zero total label; only the seed contributes nonzero total mass.", fontsize=9, ha="left")


def fig_h1_grammar() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(11.8, 4.5))
    draw_level1_word(axs[0])
    draw_extracted_h1(axs[1])
    panel_label(axs[0], "a")
    panel_label(axs[1], "b")
    save(fig, "figure2_h1_grammar")


def fig_obstruction() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12.4, 4.8), gridspec_kw={"width_ratios": [1.0, 1.05]})

    ax = axs[0]
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    rounded_box(
        ax,
        (0.04, 0.28),
        0.24,
        0.42,
        "Initial data\none singleton seed $x$\nwith $x_1+x_2\\neq 0$",
        fc="#FDECEC",
        ec=PALETTE["red"],
        text_size=11,
    )
    rounded_box(
        ax,
        (0.38, 0.22),
        0.24,
        0.54,
        "Rule 1 adds only edge\ngenerators of total label\n$(0,0)$, and rule 3 takes\ninteger linear combinations.\n\nEvery derived relation\ntherefore has total label\n$k x$ for some $k\\in\\mathbb{Z}$.",
        fc="#EAF2FB",
        ec=PALETTE["blue"],
        text_size=10,
    )
    rounded_box(
        ax,
        (0.72, 0.28),
        0.24,
        0.42,
        "Rule 2 needs a singleton\nanti-diagonal vector\n$(a,-a)$ with $a\\neq 0$,\nwhose coordinate sum is $0$.",
        fc="#FCF7EA",
        ec=PALETTE["gold"],
        text_size=11,
    )
    arrow(ax, (0.28, 0.49), (0.38, 0.49), PALETTE["muted"])
    arrow(ax, (0.62, 0.49), (0.72, 0.49), PALETTE["muted"])
    ax.text(0.50, 0.82, "One-seed obstruction", fontsize=13, fontweight="bold", ha="center")
    ax.text(
        0.50,
        0.12,
        "If $k x=(a,-a)$ then $k(x_1+x_2)=0$. Because $x_1+x_2\\neq 0$, we get $k=0$, hence $(a,-a)=(0,0)$, impossible.",
        fontsize=10.5,
        ha="center",
    )
    panel_label(ax, "a")

    ax = axs[1]
    ax.set_axis_off()
    ax.set_xlim(0.5, 4.8)
    ax.set_ylim(-0.25, 2.35)
    for row in (1, 2, 3):
        y = 3.0 - row
        for col in range(1, 5):
            if row == 2:
                face = "#F6F1E8"
            elif row == 1:
                face = "#EAF2FB"
            else:
                face = "#EDF6EF"
            ax.scatter([col], [y], s=86, color=face, edgecolors=PALETTE["ink"], zorder=4)
    for col in range(1, 5):
        ax.plot([col, col], [0, 1], color=PALETTE["orange"], lw=3)
        ax.plot([col, col], [1, 2], color=PALETTE["orange"], lw=3)
        ax.text(col + 0.06, 1.48, "$c$", fontsize=8.5, color=PALETTE["orange"])
        ax.text(col + 0.06, 0.48, "$c$", fontsize=8.5, color=PALETTE["orange"])
    for col in range(1, 4):
        ax.plot([col, col + 1], [2, 2], color=PALETTE["blue"], lw=3.2)
        ax.plot([col, col + 1], [0, 0], color=PALETTE["green"], lw=3.2)
        ax.plot([col, col + 1], [1, 1], color=PALETTE["grid"], lw=3.2, ls="--")
    ax.scatter([1, 4], [2, 0], marker="s", s=150, facecolors="none", edgecolors=PALETTE["red"], linewidths=1.8, zorder=5)
    ax.text(0.65, 2.20, "Passive-middle $H=3$ family", fontsize=11, ha="left", va="top")
    ax.text(0.65, 2.00, "Seeds and initial $T$ stay on rows 1 and 3; row 2 has no horizontal labels.", fontsize=8.8, ha="left")
    ax.text(0.65, 1.78, "At every middle-row vertex, every generator contributes either $0$ or $\\pm c$.", fontsize=8.8, ha="left")
    ax.text(2.50, -0.18, "Any middle-row singleton must lie in $\\mathbb{Z}c$; if $c_1+c_2\\neq 0$, it can never be anti-diagonal.", fontsize=9, ha="center")
    ax.text(2.50, 2.28, "Row-quotient obstruction", fontsize=13, fontweight="bold", ha="center")
    panel_label(ax, "b")
    save(fig, "figure3_obstruction")


def extract_history(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    payload = load_json(path)
    xs = []
    ys = []
    current = np.nan
    for row in payload["history"]:
        xs.append(row["trial"])
        score = row["best_score_so_far"]
        current = np.nan if score is None else float(score)
        ys.append(current)
    return np.array(xs), np.array(ys, dtype=float)


def fig_frontier() -> None:
    width4 = load_json(RESULTS / "phase4_width4_seed601.json")["best"]
    width6 = load_json(RESULTS / "phase4_width6_seed602.json")["best"]
    width8 = load_json(RESULTS / "phase4_width8_seed501.json")["best"]
    h5 = load_json(RESULTS / "phase6_h5_affine_shell.json")
    asym_rows = {row["family_id"]: row["direct_baseline"]["best"] for row in h5["family_results"]}
    complexity = load_json(RESULTS / "phase6_complexity_frontier.json")

    fig, axs = plt.subplots(1, 2, figsize=(12.4, 5.0), gridspec_kw={"width_ratios": [1.1, 1.0]})

    ax = axs[0]
    labels = ["2x4", "2x6", "asym_a", "asym_b", "asym_c", "legacy 2x8"]
    scores = [
        width4["score"],
        width6["score"],
        asym_rows["asym_a"]["score"],
        asym_rows["asym_b"]["score"],
        asym_rows["asym_c"]["score"],
        width8["score"],
    ]
    colors = [
        PALETTE["blue"],
        PALETTE["teal"],
        PALETTE["green"],
        PALETTE["green"],
        PALETTE["gold"],
        PALETTE["orange"],
    ]
    xpos = np.arange(len(labels))
    ax.scatter(xpos, scores, s=100, c=colors, zorder=4)
    ax.plot(xpos[:5], scores[:5], color=PALETTE["muted"], lw=1.4, zorder=2)
    ax.axhline(1.675, color=PALETTE["red"], lw=1.8, ls="--", label="target 1.675")
    ax.set_xticks(xpos, labels)
    ax.set_ylim(1.70, 2.16)
    ax.set_ylabel("Exact score $(m+r)/(n-t)$")
    ax.set_title("Best saved exact certificates")
    annotations = ["2.0", "2.0", "$13/7$", "$13/7$", "$14/7$", "$29/14$"]
    for idx, (xv, score, text) in enumerate(zip(xpos, scores, annotations)):
        dy = 0.025 if idx not in (1, 4) else -0.04
        ax.text(xv, score + dy, text, ha="center", va="center", fontsize=9)
    ax.text(
        xpos[-1],
        scores[-1] + 0.06,
        "exploratory,\nunmatched",
        ha="center",
        va="center",
        fontsize=8.5,
        color=PALETTE["orange"],
    )
    ax.legend(loc="upper right")
    panel_label(ax, "a")

    ax = axs[1]
    rows = complexity["rows"]
    jitter = {
        "same_palette_2x8": -0.18,
        "low_height_asymmetric_2x8": -0.06,
        "bounded_slope_2x8": 0.06,
        "slowly_growing_x_2x8": 0.18,
        "legacy_exploratory_width8_3label": 0.0,
    }
    short = {
        "same_palette_2x8": "same\npalette",
        "low_height_asymmetric_2x8": "low-height\nasym.",
        "bounded_slope_2x8": "bounded\nslope",
        "slowly_growing_x_2x8": "slowly\ngrowing $X$",
        "legacy_exploratory_width8_3label": "legacy\n29/14",
    }
    y_null = 2.15
    for row in rows:
        x = row["x_size"] + jitter[row["family_id"]]
        if row["score"] is None:
            ax.scatter(x, y_null, marker="x", s=110, linewidths=2.0, color=PALETTE["red"], zorder=4)
            ax.text(x, y_null + 0.03, short[row["family_id"]], ha="center", va="bottom", fontsize=8.5, color=PALETTE["red"])
        else:
            ax.scatter(x, row["score"], s=100, color=PALETTE["orange"], zorder=4)
            ax.text(x, row["score"] + 0.04, short[row["family_id"]], ha="center", va="bottom", fontsize=8.5, color=PALETTE["orange"])
            ax.text(x, row["score"] - 0.05, "$29/14$", ha="center", va="top", fontsize=8.5)
    ax.axhline(1.675, color=PALETTE["red"], lw=1.8, ls="--")
    ax.axhline(y_null, color=PALETTE["muted"], lw=1.2, ls=":")
    ax.text(7.35, y_null + 0.01, "no forcing witness", fontsize=8.5, ha="right", va="bottom", color=PALETTE["muted"])
    ax.set_xlim(3.6, 7.4)
    ax.set_ylim(1.70, 2.22)
    ax.set_xticks([4, 5, 6, 7])
    ax.set_xlabel("$|X|$ in the width-8 ledger")
    ax.set_ylabel("Score (crosses denote empty rows)")
    ax.set_title("Complexity-accounted width-8 ledger")
    ax.text(
        5.0,
        1.76,
        "All matched reruns at fixed budget are empty.\nOnly the saved 3-label width-8 witness scores,\nbut it sits outside the matched envelope.",
        fontsize=8.8,
        ha="left",
        va="bottom",
        bbox={"boxstyle": "round,pad=0.3", "fc": PALETTE["panel"], "ec": PALETTE["grid"]},
    )
    panel_label(ax, "b")
    save(fig, "figure4_frontier")


def heatmap_with_annotations(
    ax: plt.Axes,
    values: np.ndarray,
    row_labels: Sequence[str],
    col_labels: Sequence[str],
    annotations: Sequence[Sequence[str]],
) -> None:
    cmap = LinearSegmentedColormap.from_list("paper", ["#F6F2E9", "#D7E7F6", "#3A6EA5"])
    im = ax.imshow(values, cmap=cmap, aspect="auto", vmin=0.0, vmax=1.0)
    ax.set_xticks(np.arange(len(col_labels)), labels=col_labels)
    ax.set_yticks(np.arange(len(row_labels)), labels=row_labels)
    ax.tick_params(axis="x", rotation=30)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            ax.text(
                j,
                i,
                annotations[i][j],
                ha="center",
                va="center",
                fontsize=9,
                color=PALETTE["ink"],
            )
    return im


def fig_h2_screen() -> None:
    payload = load_json(RESULTS / "phase4_h2_screen.json")
    rows = payload["h1_rows"] + payload["control_rows"]
    row_labels = [
        "H1 L1",
        "H1 L2",
        "width 4 control",
        "width 6 control",
    ]
    numeric = np.array(
        [
            [
                row["support_size"],
                row["target_solvable_vertices"],
                row["edge_density"],
                row["smith_diagonal"][-1] if row["smith_diagonal"] else 0,
                1.0 if row["forcing"] else 0.0,
            ]
            for row in rows
        ],
        dtype=float,
    )
    scale = numeric.max(axis=0)
    scale[scale == 0] = 1.0
    normalized = numeric / scale
    annotations = []
    for row in rows:
        annotations.append(
            [
                str(row["support_size"]),
                str(row["target_solvable_vertices"]),
                f"{row['edge_density']:.3f}",
                str(row["smith_diagonal"][-1] if row["smith_diagonal"] else 0),
                "yes" if row["forcing"] else "no",
            ]
        )

    fig, axs = plt.subplots(1, 2, figsize=(12.2, 4.9), gridspec_kw={"width_ratios": [1.1, 0.9]})
    ax = axs[0]
    heatmap_with_annotations(
        ax,
        normalized,
        row_labels,
        ["support", "target-solvable", "edge density", "Smith tail", "forcing"],
        annotations,
    )
    ax.set_title("Raw features already separate H1 from the controls", fontsize=13)
    panel_label(ax, "a")

    ax = axs[1]
    support = [row["support_size"] for row in rows]
    solvable = [row["target_solvable_vertices"] for row in rows]
    rank = [row["rank"] for row in rows]
    for idx, row in enumerate(rows):
        marker = "o" if row["forcing"] else "X"
        color = PALETTE["teal"] if row["forcing"] else PALETTE["red"]
        ax.scatter(
            support[idx],
            solvable[idx],
            s=22 * math.sqrt(rank[idx]),
            marker=marker,
            color=color,
            edgecolors="white",
            linewidths=0.8,
            zorder=4,
        )
        ax.text(
            support[idx] + 0.12,
            solvable[idx] + 0.03,
            row_labels[idx],
            fontsize=9,
            ha="left",
            va="bottom",
        )
    ax.set_xlabel("Seed support size $r$")
    ax.set_ylabel("Target-solvable vertices")
    ax.set_title("No extra screening lift", fontsize=13)
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.1, 2.2)
    ax.grid(True, linestyle=":")
    panel_label(ax, "b")
    save(fig, "figure5_h2_screen")


def wilson_interval(successes: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    phat = successes / total
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2.0 * total)) / denom
    radius = (
        z
        * math.sqrt(phat * (1.0 - phat) / total + z * z / (4.0 * total * total))
        / denom
    )
    return center - radius, center + radius


def fig_ablations() -> None:
    payload = load_json(RESULTS / "phase4_ablations.json")
    fig, axs = plt.subplots(1, 2, figsize=(12.4, 5.2), gridspec_kw={"width_ratios": [1.25, 0.95]})

    ax = axs[0]
    rows = [
        ("base", payload["base"]["score"], True),
        ("isotropic\ntop->bottom", payload["isotropic"][0]["score"], payload["isotropic"][0]["forcing"]),
        ("isotropic\nbottom->top", None, False),
        ("boundary\nseed removal", None, False),
        ("freeze $X$\nwidth 6", None, False),
        ("freeze $X$\nwidth 8", None, False),
    ]
    xs = np.arange(len(rows))
    for idx, (label, score, forcing) in enumerate(rows):
        if forcing and score is not None:
            ax.scatter(idx, score, s=95, color=PALETTE["blue"] if idx == 0 else PALETTE["orange"], zorder=4)
            ax.text(idx, score + 0.035, f"{score:.3f}".rstrip("0").rstrip("."), ha="center", fontsize=9)
        else:
            ax.scatter(idx, 2.31, marker="x", s=120, linewidths=2.1, color=PALETTE["red"], zorder=4)
            ax.text(idx, 2.345, "fail", ha="center", fontsize=9, color=PALETTE["red"])
    ax.axhline(2.0, color=PALETTE["muted"], lw=1.2, ls=":")
    ax.set_xticks(xs, [label for label, _, _ in rows])
    ax.set_ylim(1.92, 2.40)
    ax.set_ylabel("Exact score (failures shown at top)")
    ax.set_title("Saved width-4 control under ablation", fontsize=13)
    panel_label(ax, "a")

    ax = axs[1]
    groups = {
        "randomize $R$": (0, 4),
        "randomize $T$": (0, 4),
        "randomize $X$": (3, 4),
        "boundary\nwidth-8 stress": (0, 16),
    }
    labels = list(groups)
    means = [groups[label][0] / groups[label][1] for label in labels]
    lows = []
    highs = []
    for succ, total in groups.values():
        lo, hi = wilson_interval(succ, total)
        lows.append((succ / total) - lo)
        highs.append(hi - (succ / total))
    xpos = np.arange(len(labels))
    ax.bar(xpos, means, color=[PALETTE["red"], PALETTE["red"], PALETTE["green"], PALETTE["purple"]], alpha=0.8)
    ax.errorbar(xpos, means, yerr=[lows, highs], fmt="none", ecolor=PALETTE["ink"], elinewidth=1.4, capsize=4)
    ax.set_ylim(0.0, 1.05)
    ax.set_ylabel("Success rate with 95% Wilson interval")
    ax.set_xticks(xpos, labels)
    ax.set_title("Randomization and boundary stress", fontsize=13)
    for idx, label in enumerate(labels):
        succ, total = groups[label]
        ax.text(idx, means[idx] + 0.05, f"{succ}/{total}", ha="center", fontsize=9)
    panel_label(ax, "b")
    save(fig, "figure6_ablations")


def fig_route_audits() -> None:
    h4 = load_json(RESULTS / "phase6_h4_typed_residue_interfaces.json")
    h5 = load_json(RESULTS / "phase6_h5_affine_shell.json")
    h6 = load_json(RESULTS / "phase6_h6_defect_transport.json")
    controller = load_json(RESULTS / "phase6_boundary_controller.json")
    metastability = load_json(RESULTS / "phase6_metastability.json")

    fig, axs = plt.subplots(1, 3, figsize=(14.2, 4.9), gridspec_kw={"width_ratios": [1.0, 0.95, 1.1]})

    ax = axs[0]
    audit_groups = [
        ("H4 route", h4["level1"]["forcing_count"], h4["level1"]["candidate_count"], PALETTE["red"]),
        ("H4 direct", h4["matched_direct_width8"]["forcing_trials"], h4["matched_direct_width8"]["total_trials"], PALETTE["muted"]),
        (
            "H5 shell",
            sum(len(row["word_audit"]["forcing_rows"]) for row in h5["family_results"]),
            sum(row["word_audit"]["canonical_word_count"] for row in h5["family_results"]),
            PALETTE["red"],
        ),
        (
            "H5 direct",
            sum(row["direct_baseline"]["forcing_trials"] for row in h5["family_results"]),
            sum(row["direct_baseline"]["total_trials"] for row in h5["family_results"]),
            PALETTE["green"],
        ),
    ]
    labels = [item[0] for item in audit_groups]
    means = [succ / total if total else 0.0 for _, succ, total, _ in audit_groups]
    lows = []
    highs = []
    for _, succ, total, _ in audit_groups:
        lo, hi = wilson_interval(succ, total)
        means_i = succ / total if total else 0.0
        lows.append(means_i - lo)
        highs.append(hi - means_i)
    xpos = np.arange(len(labels))
    ax.bar(xpos, means, color=[item[3] for item in audit_groups], alpha=0.82)
    ax.errorbar(xpos, means, yerr=[lows, highs], fmt="none", ecolor=PALETTE["ink"], elinewidth=1.3, capsize=4)
    ax.set_ylim(0.0, 0.30)
    ax.set_ylabel("Forcing hit rate with 95% Wilson interval")
    ax.set_xticks(xpos, labels)
    ax.set_title("Interface and shell audits")
    for idx, (_, succ, total, _) in enumerate(audit_groups):
        ax.text(idx, means[idx] + 0.02, f"{succ}/{total}", ha="center", fontsize=9)
    panel_label(ax, "a")

    ax = axs[1]
    schedule_rows = [
        ("H6 periodic", h6["height2"]["periodic"]["score"], h6["height2"]["periodic"]["forcing"], PALETTE["muted"]),
        ("H6 SDP", h6["height2"]["aperiodic"]["score"], h6["height2"]["aperiodic"]["forcing"], PALETTE["green"]),
        (
            "controller best",
            controller["controller_solver_h2"]["best"]["score"],
            controller["controller_solver_h2"]["best"] is not None,
            PALETTE["gold"],
        ),
        ("matched direct", controller["direct_solver_h2"]["best_score"], True, PALETTE["blue"]),
        ("H3 lift", None, False, PALETTE["red"]),
    ]
    xpos = np.arange(len(schedule_rows))
    y_fail = 2.12
    for idx, (label, score, forcing, color) in enumerate(schedule_rows):
        if forcing and score is not None:
            ax.scatter(idx, score, s=95, color=color, zorder=4)
            ax.text(idx, score + 0.03, "$13/7$" if abs(score - (13 / 7)) < 1e-9 else f"{score:.3f}", ha="center", fontsize=8.8)
        else:
            ax.scatter(idx, y_fail, marker="x", s=120, linewidths=2.0, color=PALETTE["red"], zorder=4)
            ax.text(idx, y_fail + 0.03, "fail", ha="center", fontsize=8.5, color=PALETTE["red"])
    ax.axhline(1.675, color=PALETTE["red"], lw=1.6, ls="--")
    ax.set_ylim(1.72, 2.18)
    ax.set_xticks(xpos, [row[0] for row in schedule_rows])
    ax.set_ylabel("Exact score (failures shown at top)")
    ax.set_title("No H6 mechanism lift over direct search")
    ax.text(
        2.5,
        1.75,
        f"{controller['controller_solver_h2']['forcing_programs']} of {controller['controller_solver_h2']['total_programs']} controller programs force,\nbut the best score matches the direct archive exactly.",
        fontsize=8.5,
        ha="center",
        va="bottom",
        bbox={"boxstyle": "round,pad=0.25", "fc": PALETTE["panel"], "ec": PALETTE["grid"]},
    )
    panel_label(ax, "b")

    ax = axs[2]
    rows = metastability["rows"]
    y_fail = 2.12
    for row in rows:
        if row["forcing"] and row["score"] is not None:
            color = PALETTE["green"] if row["word"] == "SDP" else PALETTE["teal"]
            ax.scatter(row["closure_time"], row["score"], s=70, color=color, alpha=0.9, zorder=4)
            if row["word"] in {"DPS", "PDS", "SDP", "SPD"}:
                ax.text(row["closure_time"] + 0.05, row["score"] + 0.015, row["word"], fontsize=8.2)
        else:
            ax.scatter(row["closure_time"], y_fail, s=45, color=PALETTE["muted"], alpha=0.55, zorder=2)
    ax.axhline(1.675, color=PALETTE["red"], lw=1.6, ls="--")
    ax.axhline(y_fail, color=PALETTE["muted"], lw=1.2, ls=":")
    ax.text(6.9, y_fail + 0.02, "nonforcing words", fontsize=8.5, ha="right", va="bottom", color=PALETTE["muted"])
    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(1.72, 2.18)
    ax.set_xlabel("Closure time of the best audited program")
    ax.set_ylabel("Exact score")
    ax.set_title("Metastability does not predict score")
    panel_label(ax, "c")
    save(fig, "figure6_route_audits")


def draw_corridor_certificate(
    ax: plt.Axes,
    *,
    width: int,
    vertical: Sequence[int],
    top: Sequence[Sequence[int]],
    bottom: Sequence[Sequence[int]],
    seeds: Sequence[Sequence[Sequence[int]]],
    initial_t: Sequence[Sequence[int]],
    title: str,
    score: float,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0.6, width + 0.4)
    ax.set_ylim(-0.45, 1.55)

    def node_xy(vertex: Sequence[int]) -> Tuple[float, float]:
        row, col = vertex
        return float(col), 2.0 - float(row)

    def label_str(label: Sequence[int]) -> str:
        return f"({label[0]},{label[1]})"

    for col in range(1, width + 1):
        x = float(col)
        vlabel = label_str(vertical)
        color = LABEL_COLOR.get(vlabel, PALETTE["muted"])
        ax.plot([x, x], [0.0, 1.0], color=color, lw=2.5, zorder=1)
        if vertical != [0, 0]:
            ax.text(x + 0.06, 0.5, vlabel, fontsize=7.5, color=color)

    for idx, label in enumerate(top, start=1):
        if label == [0, 0]:
            continue
        color = LABEL_COLOR.get(label_str(label), PALETTE["muted"])
        ax.plot([idx, idx + 1], [1.0, 1.0], color=color, lw=3.2, solid_capstyle="round")
        ax.text(idx + 0.5, 1.08, label_str(label), fontsize=7.5, color=color, ha="center")

    for idx, label in enumerate(bottom, start=1):
        if label == [0, 0]:
            continue
        color = LABEL_COLOR.get(label_str(label), PALETTE["muted"])
        ax.plot([idx, idx + 1], [0.0, 0.0], color=color, lw=3.2, solid_capstyle="round")
        ax.text(idx + 0.5, -0.11, label_str(label), fontsize=7.5, color=color, ha="center")

    initial_t_set = {tuple(vertex) for vertex in initial_t}
    seed_map: Dict[Tuple[int, int], List[str]] = {}
    for vertex, label in seeds:
        seed_map.setdefault(tuple(vertex), []).append(label_str(label))

    for row in (1, 2):
        for col in range(1, width + 1):
            vx = (row, col)
            x, y = node_xy(vx)
            if vx in initial_t_set:
                ax.scatter([x], [y], s=140, color=PALETTE["gold"], edgecolors=PALETTE["ink"], zorder=4)
            else:
                ax.scatter([x], [y], s=80, color="white", edgecolors=PALETTE["ink"], zorder=4)
            if vx in seed_map:
                ax.scatter([x], [y], s=170, marker="s", facecolors="none", edgecolors=PALETTE["red"], linewidths=1.8, zorder=5)
                ax.text(x, y - 0.19, "\n".join(seed_map[vx]), ha="center", va="top", fontsize=7.3, color=PALETTE["red"])

    ax.text(0.68, 1.42, title, fontsize=11, ha="left", va="top")
    ax.text(0.68, 1.27, f"score = {score:.6g}", fontsize=9, ha="left")
    ax.text(0.68, -0.34, "gold = initial $T$; red squares = singleton seeds in $R$", fontsize=8.5, ha="left")


def fig_certificates() -> None:
    h5 = load_json(RESULTS / "phase6_h5_affine_shell.json")
    row_map = {row["family_id"]: row["direct_baseline"]["best"] for row in h5["family_results"]}
    asym_a = row_map["asym_a"]
    asym_c = row_map["asym_c"]

    fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.8))
    draw_corridor_certificate(
        axs[0],
        width=4,
        vertical=asym_a["vertical"][0],
        top=asym_a["horizontal"][0],
        bottom=asym_a["horizontal"][1],
        seeds=asym_a["seeds"],
        initial_t=asym_a["initial_t"],
        title="Best direct low-height control: asym_a",
        score=asym_a["score"],
    )
    draw_corridor_certificate(
        axs[1],
        width=4,
        vertical=asym_c["vertical"][0],
        top=asym_c["horizontal"][0],
        bottom=asym_c["horizontal"][1],
        seeds=asym_c["seeds"],
        initial_t=asym_c["initial_t"],
        title="Best direct low-height control: asym_c",
        score=asym_c["score"],
    )
    panel_label(axs[0], "a")
    panel_label(axs[1], "b")
    save(fig, "figure7_certificates")


def main() -> None:
    fig_pipeline()
    fig_h1_grammar()
    fig_obstruction()
    fig_frontier()
    fig_h2_screen()
    fig_route_audits()
    fig_certificates()


if __name__ == "__main__":
    main()
