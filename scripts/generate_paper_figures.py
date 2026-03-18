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
    "(2,-1)": "#D97706",
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
        (0.03, 0.60),
        0.18,
        0.22,
        "Benchmark task\nscore $\\leq 1.675$",
        fc=PALETTE["sand"],
        ec=PALETTE["muted"],
    )
    rounded_box(
        ax,
        (0.27, 0.60),
        0.18,
        0.22,
        "Frozen H1 macrocell\nsubstitution route",
        fc="#FDECEC",
        ec=PALETTE["red"],
    )
    rounded_box(
        ax,
        (0.51, 0.60),
        0.18,
        0.22,
        "Exact compiler and\nlinear-span verifier",
        fc="#EAF2FB",
        ec=PALETTE["blue"],
    )
    rounded_box(
        ax,
        (0.75, 0.60),
        0.20,
        0.22,
        "Verified outcome\nH1 impossible;\ndirect controls near 2.0",
        fc="#EDF6EF",
        ec=PALETTE["green"],
    )

    rounded_box(
        ax,
        (0.27, 0.20),
        0.18,
        0.20,
        "Matched direct\ncorridor search",
        fc="#F7F2E8",
        ec=PALETTE["orange"],
    )
    rounded_box(
        ax,
        (0.51, 0.20),
        0.18,
        0.20,
        "H2 abelian\nscreening pass",
        fc="#F0ECF7",
        ec=PALETTE["purple"],
    )
    rounded_box(
        ax,
        (0.75, 0.20),
        0.20,
        0.20,
        "Ablations:\nboundary-sensitive,\nnon-scaling controls",
        fc="#FCF7EA",
        ec=PALETTE["gold"],
    )
    rounded_box(
        ax,
        (0.03, 0.18),
        0.18,
        0.10,
        "H3 reserve route\nnot activated",
        fc="white",
        ec=PALETTE["muted"],
        text_size=9,
    )

    arrow(ax, (0.21, 0.71), (0.27, 0.71), PALETTE["muted"])
    arrow(ax, (0.45, 0.71), (0.51, 0.71), PALETTE["muted"])
    arrow(ax, (0.69, 0.71), (0.75, 0.71), PALETTE["muted"])
    arrow(ax, (0.36, 0.60), (0.36, 0.40), PALETTE["red"])
    arrow(ax, (0.60, 0.60), (0.60, 0.40), PALETTE["blue"])
    arrow(ax, (0.69, 0.30), (0.75, 0.30), PALETTE["muted"])
    arrow(ax, (0.45, 0.30), (0.51, 0.30), PALETTE["muted"])

    ax.text(
        0.36,
        0.49,
        "exact one-seed\nobstruction",
        ha="center",
        va="center",
        fontsize=9,
        color=PALETTE["red"],
    )
    ax.text(
        0.60,
        0.49,
        "same verifier\nfor all claims",
        ha="center",
        va="center",
        fontsize=9,
        color=PALETTE["blue"],
    )

    ax.text(
        0.03,
        0.95,
        "Pipeline audited in the repository: a pre-registered CA route, exact verification, matched direct controls, and a negative final disposition.",
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
    fig, ax = plt.subplots(figsize=(11.2, 4.5))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    rounded_box(
        ax,
        (0.04, 0.28),
        0.24,
        0.42,
        "Initial data\none singleton seed $x$\nwith $x_1+x_2=1$",
        fc="#FDECEC",
        ec=PALETTE["red"],
        text_size=11,
    )
    rounded_box(
        ax,
        (0.38, 0.22),
        0.24,
        0.54,
        "Closure under rule 1 and\ninteger linear combinations\nadds only edge relations of\ntotal label $(0,0)$.\n\nHence every derived relation\nhas total label $k x$\nfor some $k\\in\\mathbb{Z}$.",
        fc="#EAF2FB",
        ec=PALETTE["blue"],
        text_size=10,
    )
    rounded_box(
        ax,
        (0.72, 0.28),
        0.24,
        0.42,
        "Rule 2 needs a singleton\nanti-diagonal vector\n$(a,-a)$ with $a\\neq 0$.\n\nIts total coordinate sum is $0$.",
        fc="#FCF7EA",
        ec=PALETTE["gold"],
        text_size=11,
    )
    arrow(ax, (0.28, 0.49), (0.38, 0.49), PALETTE["muted"])
    arrow(ax, (0.62, 0.49), (0.72, 0.49), PALETTE["muted"])

    ax.text(0.50, 0.80, "Coordinate-sum invariant", fontsize=13, fontweight="bold", ha="center")
    ax.text(
        0.50,
        0.12,
        "If $k x=(a,-a)$ then $k(x_1+x_2)=0$. Since $x_1+x_2=1$, we obtain $k=0$, hence $(a,-a)=(0,0)$, contradicting rule 2.",
        fontsize=11,
        ha="center",
    )
    ax.text(0.84, 0.15, "No new vertex can ever enter $T$.", fontsize=11, color=PALETTE["red"], ha="center")
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
    width4 = load_json(RESULTS / "phase4_width4_seed601.json")
    width6 = load_json(RESULTS / "phase4_width6_seed602.json")
    width8 = load_json(RESULTS / "phase4_width8_seed501.json")
    width8b = load_json(RESULTS / "phase4_sparse_unrestricted_seed502.json")

    fig, axs = plt.subplots(1, 2, figsize=(12.2, 4.9), gridspec_kw={"width_ratios": [1.15, 1.0]})

    ax = axs[0]
    xvals = np.array([4, 6, 8, 8.12])
    yvals = np.array(
        [
            width4["best"]["score"],
            width6["best"]["score"],
            width8["best"]["score"],
            width8b["best"]["score"],
        ]
    )
    colors = [PALETTE["blue"], PALETTE["teal"], PALETTE["orange"], PALETTE["purple"]]
    ax.scatter(xvals, yvals, s=90, c=colors, zorder=4)
    ax.plot(xvals[:3], yvals[:3], color=PALETTE["muted"], lw=1.5, zorder=2)
    ax.axhline(1.675, color=PALETTE["red"], lw=1.8, ls="--", label="target 1.675")
    ax.axhline(1.70, color=PALETTE["gold"], lw=1.2, ls=":", label="1.70 neighborhood")
    ax.set_xlim(3.4, 8.6)
    ax.set_ylim(1.62, 2.22)
    ax.set_xticks([4, 6, 8])
    ax.set_xlabel("Corridor width $W$")
    ax.set_ylabel("Exact score $(m+r)/(n-t)$")
    ax.set_title("Exact direct-control frontier")
    annotations = [
        "width 4\n$2.0$",
        "width 6\n$2.0$",
        "width 8\n$29/14$",
        "exploratory\n$30/14$",
    ]
    offsets = [(0.0, 0.035), (0.0, -0.055), (0.0, 0.035), (0.20, 0.015)]
    for xv, yv, text, (dx, dy) in zip(xvals, yvals, annotations, offsets):
        ax.text(xv + dx, yv + dy, text, ha="center", va="center", fontsize=9)
    ax.scatter([4, 8], [2.18, 2.18], marker="x", s=100, color=PALETTE["red"], linewidths=2.2)
    ax.text(4, 2.205, "H1 L1 fail", ha="center", va="bottom", fontsize=9, color=PALETTE["red"])
    ax.text(8, 2.205, "H1 L2 fail", ha="center", va="bottom", fontsize=9, color=PALETTE["red"])
    ax.legend(loc="lower right")
    panel_label(ax, "a")

    ax = axs[1]
    x4, y4 = extract_history(RESULTS / "phase4_width4_seed601.json")
    x6, y6 = extract_history(RESULTS / "phase4_width6_seed602.json")
    ax.step(x4, y4, where="post", color=PALETTE["blue"], lw=2.2, label="width 4, seed 601")
    ax.step(x6, y6, where="post", color=PALETTE["teal"], lw=2.2, label="width 6, seed 602")
    ax.axhline(1.675, color=PALETTE["red"], lw=1.6, ls="--")
    ax.set_xlim(1, 50)
    ax.set_ylim(1.95, 2.12)
    ax.set_xlabel("Random-search trial")
    ax.set_ylabel("Best score so far")
    ax.set_title("Search trajectories of saved exact runs")
    ax.legend(loc="upper right")
    ax.text(
        2,
        2.105,
        "Both saved runs hit a forcing witness on trial 1;\nonly width 6 improves from $2.1$ to $2.0$ later in the run.",
        fontsize=9,
        ha="left",
        va="top",
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
    width4 = load_json(RESULTS / "phase4_width4_seed601.json")["best"]
    width6 = load_json(RESULTS / "phase4_width6_seed602.json")["best"]

    fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.8))
    draw_corridor_certificate(
        axs[0],
        width=4,
        vertical=width4["vertical"],
        top=width4["top"],
        bottom=width4["bottom"],
        seeds=width4["seeds"],
        initial_t=width4["initial_t"],
        title="Best exact width-4 control",
        score=width4["score"],
    )
    draw_corridor_certificate(
        axs[1],
        width=6,
        vertical=width6["vertical"],
        top=width6["top"],
        bottom=width6["bottom"],
        seeds=width6["seeds"],
        initial_t=width6["initial_t"],
        title="Best exact width-6 control",
        score=width6["score"],
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
    fig_ablations()
    fig_certificates()


if __name__ == "__main__":
    main()
