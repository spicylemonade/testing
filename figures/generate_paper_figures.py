#!/usr/bin/env python3
"""Generate publication-style figures for the arithmetic-Kakeya CA writeup.

The repository contains no successful exact benchmark outputs, so these
figures emphasize architecture, audit structure, bridge selection, and the
explicit blocker state. Every numeric panel is sourced from audited artifact
counts rather than fabricated performance metrics.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
RESULTS = ROOT / "results"

COLORS = {
    "navy": "#19324a",
    "teal": "#1f8a8a",
    "green": "#4f8f67",
    "gold": "#d8a84c",
    "rust": "#c25b3f",
    "rose": "#c44e52",
    "slate": "#5d6d7e",
    "mist": "#e9eef2",
    "cream": "#f7f4ee",
    "ink": "#1c1c1c",
    "grey": "#9aa3ab",
}

DECISION_COLOR = {
    "promote": COLORS["teal"],
    "hold": COLORS["gold"],
    "retire": COLORS["rose"],
}


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "axes.edgecolor": COLORS["slate"],
        "axes.linewidth": 0.8,
        "axes.facecolor": "white",
        "figure.facecolor": COLORS["cream"],
        "savefig.facecolor": COLORS["cream"],
        "grid.color": "#d7dde3",
        "grid.linewidth": 0.8,
        "grid.alpha": 0.9,
        "xtick.color": COLORS["ink"],
        "ytick.color": COLORS["ink"],
        "text.color": COLORS["ink"],
    }
)


def ensure_dirs() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def rounded_box(ax, xy, width, height, text, fc, ec=None, text_color=None, fontsize=11, lw=1.2):
    if ec is None:
        ec = fc
    if text_color is None:
        text_color = "white"
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=lw,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        color=text_color,
        fontsize=fontsize,
        weight="bold" if fontsize >= 11 else None,
        wrap=True,
    )
    return patch


def arrow(ax, start, end, color=COLORS["slate"], lw=1.6, style="-|>"):
    patch = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=12, linewidth=lw, color=color)
    ax.add_patch(patch)
    return patch


def load_bridge_candidates():
    path = RESULTS / "concept_evolve" / "bridge_candidates.json"
    return json.loads(path.read_text())


def fig_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(13.5, 7.0))
    ax.set_axis_off()

    rounded_box(ax, (0.04, 0.66), 0.18, 0.16, "Problem Statement\nArithmetic Kakeya target\nscore ≤ 1.675", COLORS["navy"])
    rounded_box(ax, (0.28, 0.66), 0.19, 0.16, "Witness Spec\nSix-line schema,\nforcing rules,\nexact score", COLORS["teal"])
    rounded_box(ax, (0.53, 0.66), 0.19, 0.16, "H1 Design\nProof-carrying,\nstage-indexed CA\nwith no repair", COLORS["green"])
    rounded_box(ax, (0.78, 0.66), 0.18, 0.16, "Exact Decoder /\nVerifier\n(required)", COLORS["rust"])

    rounded_box(ax, (0.04, 0.34), 0.18, 0.16, "Literature &\nprior-art boundary", COLORS["gold"], text_color=COLORS["ink"])
    rounded_box(ax, (0.28, 0.34), 0.19, 0.16, "ConceptEvolve\nbridge search\nand reframing", COLORS["gold"], text_color=COLORS["ink"])
    rounded_box(ax, (0.53, 0.34), 0.19, 0.16, "Benchmark plan\nlabel shuffle,\ndecoder match,\nOOD, complexity", COLORS["mist"], ec=COLORS["slate"], text_color=COLORS["ink"])
    rounded_box(ax, (0.78, 0.34), 0.18, 0.16, "Final assessment\npivot to verifier\nrecovery", COLORS["mist"], ec=COLORS["rust"], text_color=COLORS["ink"])

    arrow(ax, (0.22, 0.74), (0.28, 0.74), COLORS["slate"])
    arrow(ax, (0.47, 0.74), (0.53, 0.74), COLORS["slate"])
    arrow(ax, (0.72, 0.74), (0.78, 0.74), COLORS["slate"])
    arrow(ax, (0.13, 0.50), (0.13, 0.66), COLORS["gold"])
    arrow(ax, (0.375, 0.50), (0.375, 0.66), COLORS["gold"])
    arrow(ax, (0.625, 0.50), (0.625, 0.66), COLORS["slate"])
    arrow(ax, (0.87, 0.66), (0.87, 0.50), COLORS["rust"], style="<|-")
    arrow(ax, (0.72, 0.42), (0.78, 0.42), COLORS["slate"])

    ax.text(
        0.78,
        0.90,
        "Observed blocker:\nno shared exact integer decoder/verifier\nin the snapshot",
        ha="center",
        va="center",
        fontsize=12,
        color=COLORS["rust"],
        weight="bold",
    )
    ax.text(
        0.50,
        0.10,
        "All empirical claims route through the exact decoder/verifier box. Its absence propagates a deliberate block to phase-4 evaluation, preserving negative results instead of substituting proxy metrics.",
        ha="center",
        va="center",
        fontsize=11,
        color=COLORS["ink"],
        wrap=True,
    )
    save(fig, "fig_pipeline_overview")


def fig_architecture() -> None:
    fig, ax = plt.subplots(figsize=(13.5, 8.0))
    ax.set_axis_off()

    rounded_box(ax, (0.06, 0.76), 0.22, 0.13, "Registry Fiber\nactive labels in X\nplus legality tag a+b ≠ 0", COLORS["navy"])
    rounded_box(ax, (0.06, 0.51), 0.22, 0.13, "Edge Fiber E₁\nprefix keys in d₁−1\nedge_label ∈ X ∪ {(0,0)}", COLORS["teal"])
    rounded_box(ax, (0.06, 0.33), 0.22, 0.13, "Edge Fiber E₂\nprefix keys in d₁×(d₂−1)", COLORS["teal"])
    rounded_box(ax, (0.06, 0.15), 0.22, 0.13, "⋮\nEdge Fiber E_k", COLORS["teal"])

    rounded_box(ax, (0.40, 0.53), 0.22, 0.18, "Vertex Fiber V\nseed_label\nforced_bit\nproof_tag\nmask_tag", COLORS["green"])
    rounded_box(ax, (0.74, 0.62), 0.18, 0.11, "Decode X", COLORS["mist"], ec=COLORS["navy"], text_color=COLORS["ink"])
    rounded_box(ax, (0.74, 0.48), 0.18, 0.11, "Decode f_i", COLORS["mist"], ec=COLORS["teal"], text_color=COLORS["ink"])
    rounded_box(ax, (0.74, 0.34), 0.18, 0.11, "Decode T", COLORS["mist"], ec=COLORS["green"], text_color=COLORS["ink"])
    rounded_box(ax, (0.74, 0.20), 0.18, 0.11, "Decode R", COLORS["mist"], ec=COLORS["gold"], text_color=COLORS["ink"])

    rounded_box(ax, (0.40, 0.18), 0.22, 0.16, "No-repair gate\nreject malformed labels,\nout-of-range keys,\nnon-singleton R seeds", COLORS["rust"])

    for y in (0.83, 0.58, 0.40, 0.22):
        arrow(ax, (0.28, y), (0.40, 0.62 if y > 0.60 else 0.26 if y < 0.30 else 0.58), COLORS["slate"])

    arrow(ax, (0.62, 0.62), (0.74, 0.67), COLORS["navy"])
    arrow(ax, (0.28, 0.58), (0.74, 0.53), COLORS["teal"])
    arrow(ax, (0.62, 0.58), (0.74, 0.39), COLORS["green"])
    arrow(ax, (0.62, 0.58), (0.74, 0.25), COLORS["gold"])
    arrow(ax, (0.51, 0.34), (0.51, 0.53), COLORS["rust"], style="<|-")

    ax.text(
        0.50,
        0.93,
        "Stage-indexed proof-carrying CA used by H1",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
        color=COLORS["ink"],
    )
    ax.text(
        0.50,
        0.06,
        "The key architectural choice is to align the automaton with the witness grammar itself: edge fibers emit partial f_i dictionaries, vertex fibers emit T and singleton-supported R seeds, and the decoder rejects rather than repairs any malformed state.",
        ha="center",
        va="center",
        fontsize=11,
        wrap=True,
    )
    save(fig, "fig_h1_architecture")


def fig_gate_state() -> None:
    fig, ax = plt.subplots(figsize=(13.5, 7.5))
    ax.set_axis_off()

    rounded_box(ax, (0.08, 0.58), 0.22, 0.15, "H1 champion lane\nactive in design,\nblocked at exact gate", COLORS["green"])
    rounded_box(ax, (0.39, 0.58), 0.22, 0.15, "H2 backup lane\nclosed until H1\nfails exact gate", COLORS["gold"], text_color=COLORS["ink"])
    rounded_box(ax, (0.70, 0.58), 0.22, 0.15, "H3 reserve lane\nclosed unless H1/H2 fail\nand an invariant appears", COLORS["mist"], ec=COLORS["slate"], text_color=COLORS["ink"])

    rounded_box(ax, (0.08, 0.26), 0.18, 0.12, "Missing verifier\nshared blocker", COLORS["rust"])
    rounded_box(ax, (0.31, 0.24), 0.18, 0.16, "Kill gates\nlabel shuffle\nOOD failure\nbounded slope", COLORS["mist"], ec=COLORS["rose"], text_color=COLORS["ink"])
    rounded_box(ax, (0.54, 0.24), 0.18, 0.16, "Keep gates\nexact decode\nbaseline win\nshuffle collapse", COLORS["mist"], ec=COLORS["teal"], text_color=COLORS["ink"])
    rounded_box(ax, (0.77, 0.24), 0.15, 0.16, "Pivot\nrecover exact\nverifier", COLORS["navy"])

    arrow(ax, (0.19, 0.58), (0.17, 0.38), COLORS["rust"])
    arrow(ax, (0.39, 0.66), (0.30, 0.66), COLORS["grey"], style="<|-")
    arrow(ax, (0.61, 0.66), (0.70, 0.66), COLORS["grey"])
    arrow(ax, (0.19, 0.58), (0.40, 0.40), COLORS["rose"])
    arrow(ax, (0.19, 0.58), (0.63, 0.40), COLORS["teal"])
    arrow(ax, (0.17, 0.26), (0.84, 0.40), COLORS["rust"])

    ax.text(0.50, 0.90, "Lane-governance state machine", ha="center", va="center", fontsize=16, weight="bold")
    ax.text(
        0.50,
        0.08,
        "The repository never opened H2 or H3 because H1 was blocked by missing infrastructure rather than killed by an exact experiment. The correct transition is therefore a pivot to verifier recovery, not lane expansion.",
        ha="center",
        va="center",
        fontsize=11,
        wrap=True,
    )
    save(fig, "fig_lane_gates")


def fig_bridge_decisions() -> None:
    bridges = load_bridge_candidates()
    order_value = {"promote": 0, "hold": 1, "retire": 2}
    bridges = sorted(bridges, key=lambda item: (order_value[item["promotion_decision"]], item["bridge"]))

    labels = [item["bridge"].replace("_", "\n") for item in bridges]
    decision_score = {"promote": 3, "hold": 2, "retire": 1}
    scores = [decision_score[item["promotion_decision"]] for item in bridges]
    colors = [DECISION_COLOR[item["promotion_decision"]] for item in bridges]

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.barh(range(len(labels)), scores, color=colors, edgecolor="white", linewidth=1.5)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 3.4)
    ax.set_xticks([1, 2, 3], ["Retire", "Hold", "Promote"])
    ax.set_xlabel("Bridge disposition after iterate pass")
    ax.set_title("ConceptEvolve bridge triage")
    ax.grid(axis="x")

    for idx, item in enumerate(bridges):
        ax.text(
            scores[idx] + 0.05,
            idx,
            item["risk"],
            va="center",
            fontsize=10,
            color=COLORS["ink"],
        )

    legend = [
        Line2D([0], [0], color=DECISION_COLOR["promote"], lw=8, label="Promote"),
        Line2D([0], [0], color=DECISION_COLOR["hold"], lw=8, label="Hold"),
        Line2D([0], [0], color=DECISION_COLOR["retire"], lw=8, label="Retire"),
    ]
    ax.legend(handles=legend, loc="lower right", frameon=False)
    save(fig, "fig_bridge_decisions")


def fig_blocker_budget() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.5))

    planned = [3, 1000, 1000, 5]
    executed = [0, 0, 0, 0]
    labels = ["H1 families", "Decodes/\nfamily", "Baseline\nbudget", "Control\nblocks"]
    x = range(len(labels))
    w = 0.35

    axes[0].bar([i - w / 2 for i in x], planned, width=w, color=COLORS["navy"], label="Planned")
    axes[0].bar([i + w / 2 for i in x], executed, width=w, color=COLORS["rust"], label="Executed")
    axes[0].set_xticks(list(x), labels)
    axes[0].set_ylabel("Count")
    axes[0].set_title("Phase-4 budget: planned versus spent")
    axes[0].grid(axis="y")
    axes[0].legend(frameon=False, loc="upper right")

    metric_names = ["Verified hit rate", "Best score", "Median score", "OOD robustness"]
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(-0.5, len(metric_names) - 0.5)
    axes[1].set_yticks(range(len(metric_names)))
    axes[1].set_yticklabels(metric_names)
    axes[1].set_xticks([])
    axes[1].set_title("Measured outputs")
    for i, name in enumerate(metric_names):
        rect = Rectangle((0.08, i - 0.32), 0.84, 0.64, facecolor=COLORS["mist"], edgecolor=COLORS["slate"])
        axes[1].add_patch(rect)
        axes[1].text(0.50, i, "not available", ha="center", va="center", fontsize=11, color=COLORS["ink"])
    axes[1].invert_yaxis()
    for spine in axes[1].spines.values():
        spine.set_visible(False)

    fig.suptitle("Audited blocker outcome", fontsize=16, weight="bold", y=0.98)
    save(fig, "fig_blocker_budget")


def fig_prior_art() -> None:
    rows = [
        ("Katz-Tao (1999)", [1, 0, 0, 0, 0]),
        ("Green-Ruzsa (2019)", [1, 0, 0, 0, 0]),
        ("Cowen-Breen et al. (2020)", [0, 1, 0, 0, 0]),
        ("Pohoata-Zakharov (2024)", [0, 1, 0, 0, 0]),
        ("Tao (2025)", [1, 0, 0, 0, 0]),
        ("Bond-Levine (2016)", [0, 0, 0, 1, 0]),
        ("Dennunzio et al. (2023)", [0, 0, 0, 1, 0]),
        ("AlphaEvolve (2025)", [0, 0, 1, 0, 0]),
        ("Georgiev et al. (2025)", [0, 0, 1, 0, 0]),
        ("Malformed watchlist", [0, 0, 0, 0, 1]),
    ]
    cols = [
        "Math.\ndirect",
        "Math.\nadjacent",
        "Method.\ndirect",
        "Method.\nadjacent",
        "False\noverlap",
    ]

    data = [item[1] for item in rows]
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    cmap = matplotlib.colors.ListedColormap(["#f4f1ea", COLORS["teal"]])
    ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), [item[0] for item in rows])
    ax.set_title("Prior-art pressure map used in the manuscript")

    for y in range(len(rows)):
        for x in range(len(cols)):
            if data[y][x]:
                ax.text(x, y, "●", ha="center", va="center", color="white", fontsize=16)

    ax.set_xticks([i - 0.5 for i in range(1, len(cols))], minor=True)
    ax.set_yticks([i - 0.5 for i in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    save(fig, "fig_prior_art_map")


def main() -> None:
    ensure_dirs()
    fig_pipeline()
    fig_architecture()
    fig_gate_state()
    fig_bridge_decisions()
    fig_blocker_budget()
    fig_prior_art()


if __name__ == "__main__":
    main()
