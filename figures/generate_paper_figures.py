#!/usr/bin/env python3
"""Generate publication-style figures for the exact arithmetic-Kakeya CA paper."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
RESULTS = ROOT / "results"
THEORY = RESULTS / "theory"

COLORS = {
    "ink": "#1f2430",
    "navy": "#204060",
    "teal": "#1b7f79",
    "green": "#5d8c63",
    "gold": "#c9932d",
    "orange": "#d9743a",
    "rose": "#c4515f",
    "slate": "#6b7280",
    "mist": "#e8eef2",
    "cream": "#f7f4ee",
    "sand": "#efe4d2",
    "white": "#ffffff",
}

DECISION_COLOR = {
    "promote": COLORS["teal"],
    "hold": COLORS["gold"],
    "retire": COLORS["rose"],
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "axes.edgecolor": COLORS["slate"],
        "axes.linewidth": 0.8,
        "axes.facecolor": COLORS["white"],
        "figure.facecolor": COLORS["cream"],
        "savefig.facecolor": COLORS["cream"],
        "grid.color": "#d3dae1",
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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def rounded_box(
    ax,
    xy,
    width,
    height,
    text,
    fc,
    ec=None,
    text_color=None,
    fontsize=11,
    lw=1.2,
):
    if ec is None:
        ec = fc
    if text_color is None:
        text_color = COLORS["white"]
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


def corpus_summary() -> dict:
    return load_json(THEORY / "forcing_traces" / "tiny_2x2_full_seeds_le3" / "corpus_summary.json")


def trace_index() -> dict:
    return load_json(THEORY / "forcing_traces" / "index.json")


def representative_class() -> dict:
    return load_json(THEORY / "forcing_traces" / "tiny_2x2_full_seeds_le3" / "class_001.json")


def load_bridge_candidates() -> list[dict]:
    return load_json(RESULTS / "concept_evolve" / "bridge_candidates.json")


def parse_search_runs() -> list[dict[str, object]]:
    path = RESULTS / "experiments" / "h1_exact_advantage.md"
    pattern = re.compile(
        r"- `(?P<geometry>\d+ x \d+)`(?P<extra>[^:]*): best exact forced count `(?P<num>\d+)/(?P<den>\d+)`"
    )
    runs = []
    for line in path.read_text().splitlines():
        match = pattern.search(line)
        if not match:
            continue
        geometry = match.group("geometry").replace(" x ", "x")
        extra = match.group("extra").strip()
        label = geometry if not extra else f"{geometry}{extra}"
        runs.append(
            {
                "label": label,
                "geometry": geometry,
                "group": "2xN ladders" if geometry.startswith("2x") else "3xN strips",
                "forced": int(match.group("num")),
                "total": int(match.group("den")),
                "fraction": int(match.group("num")) / int(match.group("den")),
            }
        )
    return runs


def signature_labels(summary: dict) -> tuple[list[str], list[int]]:
    labels = []
    counts = []
    for signature, count in sorted(summary["trace_signature_histogram"].items(), key=lambda item: item[0]):
        parsed = ast.literal_eval(signature)
        first_corner = tuple(parsed[0][0])
        labels.append(f"first {first_corner}")
        counts.append(count)
    return labels, counts


def draw_grid_state(ax, witness: dict, forced_vertices: set[tuple[int, int]], title: str) -> None:
    coords = {(1, 1): (0.0, 1.0), (1, 2): (1.0, 1.0), (2, 1): (0.0, 0.0), (2, 2): (1.0, 0.0)}
    seed_map = {}
    for entry in witness["R"]:
        for raw_vertex, label in entry.items():
            vertex = tuple(ast.literal_eval(raw_vertex))
            seed_map[vertex] = tuple(label)

    stage1 = tuple(witness["f"][0]["(1,)"])
    stage2_top = tuple(witness["f"][1]["(1, 1)"])
    stage2_bottom = tuple(witness["f"][1]["(2, 1)"])

    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.7, 1.6)
    ax.set_aspect("equal")
    ax.set_axis_off()

    for vertex, (x, y) in coords.items():
        fill = COLORS["gold"] if vertex in forced_vertices else COLORS["white"]
        edge = COLORS["orange"] if vertex in forced_vertices else COLORS["navy"]
        rect = Rectangle((x - 0.38, y - 0.38), 0.76, 0.76, facecolor=fill, edgecolor=edge, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(x, y + 0.17, f"{vertex}", ha="center", va="center", fontsize=10, weight="bold")
        if vertex in seed_map:
            ax.text(
                x,
                y - 0.12,
                f"seed {seed_map[vertex]}",
                ha="center",
                va="center",
                fontsize=9,
                color=COLORS["teal"],
            )

    for x in (0.0, 1.0):
        ax.plot([x, x], [0.38, 0.62], color=COLORS["navy"], linewidth=2.0)
        ax.text(x + 0.08, 0.50, str(stage1), fontsize=9, color=COLORS["navy"], va="center")

    ax.plot([0.38, 0.62], [1.0, 1.0], color=COLORS["teal"], linewidth=2.0)
    ax.plot([0.38, 0.62], [0.0, 0.0], color=COLORS["green"], linewidth=2.0)
    ax.text(0.50, 1.10, str(stage2_top), fontsize=9, color=COLORS["teal"], ha="center")
    ax.text(0.50, 0.10, str(stage2_bottom), fontsize=9, color=COLORS["green"], ha="center")

    ax.text(0.50, 1.45, title, ha="center", va="center", fontsize=12, weight="bold")


def fig_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(14.5, 7.8))
    ax.set_axis_off()

    rounded_box(
        ax,
        (0.03, 0.66),
        0.18,
        0.16,
        "Task Prompt\nExact witness target\nscore ≤ 1.675",
        COLORS["navy"],
    )
    rounded_box(
        ax,
        (0.27, 0.66),
        0.18,
        0.16,
        "Stage-Indexed CA\nproof-carrying\ncandidate states",
        COLORS["teal"],
    )
    rounded_box(
        ax,
        (0.51, 0.66),
        0.18,
        0.16,
        "No-Repair Decoder\nsix-line witness\n(X,G,R,T)",
        COLORS["green"],
    )
    rounded_box(
        ax,
        (0.75, 0.66),
        0.20,
        0.16,
        "Exact Verifier\nrational-span trace\nnormal form",
        COLORS["gold"],
        text_color=COLORS["ink"],
    )

    rounded_box(
        ax,
        (0.04, 0.34),
        0.22,
        0.16,
        "Exhaustive 2x2 corpus\n44,608 checked\n48 exact-valid",
        COLORS["mist"],
        ec=COLORS["navy"],
        text_color=COLORS["ink"],
    )
    rounded_box(
        ax,
        (0.39, 0.34),
        0.22,
        0.16,
        "Local strip atlas\n256 + 8,192 states\n0 strict improvements",
        COLORS["mist"],
        ec=COLORS["rose"],
        text_color=COLORS["ink"],
    )
    rounded_box(
        ax,
        (0.73, 0.34),
        0.22,
        0.16,
        "Larger exact search\nno promoted family\nbelow 1.675",
        COLORS["mist"],
        ec=COLORS["slate"],
        text_color=COLORS["ink"],
    )

    rounded_box(
        ax,
        (0.24, 0.08),
        0.52,
        0.13,
        "Current admissible frontier: coupled multi-boundary strips, typed macrocells, or wider exact blocks.\nUnilateral width-2/3 strip waves are ruled out in the audited classes.",
        COLORS["sand"],
        ec=COLORS["gold"],
        text_color=COLORS["ink"],
        fontsize=11,
    )

    arrow(ax, (0.21, 0.74), (0.27, 0.74))
    arrow(ax, (0.45, 0.74), (0.51, 0.74))
    arrow(ax, (0.69, 0.74), (0.75, 0.74))
    arrow(ax, (0.85, 0.66), (0.16, 0.50), COLORS["navy"])
    arrow(ax, (0.85, 0.66), (0.50, 0.50), COLORS["rose"])
    arrow(ax, (0.85, 0.66), (0.84, 0.50), COLORS["slate"])
    arrow(ax, (0.50, 0.34), (0.50, 0.21), COLORS["gold"])

    ax.text(
        0.50,
        0.93,
        "Exact cellular-automaton pipeline after the verifier pivot",
        ha="center",
        va="center",
        fontsize=17,
        weight="bold",
    )
    save(fig, "fig_pipeline_overview")


def fig_architecture() -> None:
    fig, ax = plt.subplots(figsize=(14.0, 7.8))
    ax.set_axis_off()

    rounded_box(ax, (0.05, 0.74), 0.20, 0.12, "Registry fiber\nactive labels in X", COLORS["navy"])
    rounded_box(ax, (0.05, 0.54), 0.20, 0.12, "Edge fibers\nstage-wise f_i entries", COLORS["teal"])
    rounded_box(ax, (0.05, 0.34), 0.20, 0.12, "Vertex fiber\nT bits + singleton seeds", COLORS["green"])
    rounded_box(
        ax,
        (0.37, 0.46),
        0.24,
        0.20,
        "No-repair decoder\nreject malformed supports,\nforbidden labels, and bad keys",
        COLORS["sand"],
        ec=COLORS["gold"],
        text_color=COLORS["ink"],
    )
    rounded_box(
        ax,
        (0.70, 0.56),
        0.22,
        0.14,
        "Exact verifier\nGaussian elimination over Q",
        COLORS["gold"],
        text_color=COLORS["ink"],
    )
    rounded_box(
        ax,
        (0.70, 0.34),
        0.22,
        0.14,
        "Trace normal form\nF_0, Δ_0, F_1, ...",
        COLORS["rose"],
    )
    rounded_box(
        ax,
        (0.70, 0.12),
        0.22,
        0.14,
        "Score accounting\n(m+r)/(n-t)",
        COLORS["mist"],
        ec=COLORS["slate"],
        text_color=COLORS["ink"],
    )

    arrow(ax, (0.25, 0.80), (0.37, 0.60))
    arrow(ax, (0.25, 0.60), (0.37, 0.56))
    arrow(ax, (0.25, 0.40), (0.37, 0.52))
    arrow(ax, (0.61, 0.56), (0.70, 0.63), COLORS["gold"])
    arrow(ax, (0.81, 0.56), (0.81, 0.48), COLORS["rose"])
    arrow(ax, (0.81, 0.34), (0.81, 0.26), COLORS["slate"])

    ax.text(
        0.50,
        0.92,
        "Witness-faithful CA architecture used in the active H1 lane",
        ha="center",
        va="center",
        fontsize=17,
        weight="bold",
    )
    ax.text(
        0.50,
        0.03,
        "The architectural commitment is local but exact: the automaton proposes only typed witness data, the decoder never repairs it,\n"
        "and all mathematical claims pass through the same rational-span verifier and score function.",
        ha="center",
        va="bottom",
        fontsize=11,
    )
    save(fig, "fig_h1_architecture")


def fig_exact_nucleus() -> None:
    witness = representative_class()["canonical_witness"]
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.4))

    draw_grid_state(axes[0], witness, set(), "Seeded witness")
    draw_grid_state(axes[1], witness, {(2, 2)}, "After layer 0")
    draw_grid_state(axes[2], witness, {(1, 1), (1, 2), (2, 1), (2, 2)}, "After layer 1")

    fig.suptitle(
        "Representative exact-valid 2x2 nucleus (score 7/4)",
        fontsize=17,
        weight="bold",
        y=0.98,
    )
    save(fig, "fig_exact_nucleus")


def fig_trace_rigidity() -> None:
    summary = corpus_summary()
    checked = summary["raw_witnesses_checked"]
    valid = summary["exact_valid_witnesses"]
    invalid = checked - valid
    sig_labels, sig_counts = signature_labels(summary)

    fig, axes = plt.subplots(1, 3, figsize=(17.0, 5.6))

    axes[0].barh(["audited regime"], [invalid], color=COLORS["mist"], edgecolor=COLORS["slate"], height=0.44)
    axes[0].barh(["audited regime"], [valid], left=[invalid], color=COLORS["gold"], edgecolor=COLORS["gold"], height=0.44)
    axes[0].set_xlim(0, checked * 1.02)
    axes[0].set_title("Exact-valid classes inside the 2x2 audit")
    axes[0].set_xlabel("Witness count")
    axes[0].grid(axis="x")
    axes[0].text(checked * 0.55, 0, f"{invalid:,} invalid", ha="center", va="center", fontsize=10)
    axes[0].text(
        invalid + valid * 0.5,
        0,
        f"{valid} valid\n({100 * valid / checked:.3f}%)",
        ha="center",
        va="center",
        fontsize=10,
        color=COLORS["ink"],
        weight="bold",
    )

    score_items = list(summary["score_histogram"].items())
    axes[1].bar(
        [label for label, _ in score_items],
        [count for _, count in score_items],
        color=COLORS["teal"],
        edgecolor=COLORS["white"],
        linewidth=1.5,
        yerr=[0 for _ in score_items],
        capsize=4,
    )
    axes[1].set_title("Score histogram of exact-valid classes")
    axes[1].set_ylabel("Class count")
    axes[1].grid(axis="y")

    axes[2].bar(sig_labels, sig_counts, color=COLORS["navy"], edgecolor=COLORS["white"], linewidth=1.5, yerr=[0] * len(sig_counts), capsize=4)
    axes[2].set_title("Trace-signature histogram")
    axes[2].set_ylabel("Class count")
    axes[2].grid(axis="y")
    axes[2].tick_params(axis="x", rotation=18)

    fig.suptitle("Rigidity of the exhaustive 2x2 micro-regime", fontsize=17, weight="bold", y=0.99)
    save(fig, "fig_trace_rigidity")


def fig_coverability_modes() -> None:
    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    ax.set_axis_off()

    rounded_box(ax, (0.07, 0.28), 0.16, 0.28, "left column\nalready active", COLORS["mist"], ec=COLORS["navy"], text_color=COLORS["ink"])
    rounded_box(ax, (0.40, 0.28), 0.20, 0.28, "fresh width-2 column\nno seeds inside", COLORS["sand"], ec=COLORS["gold"], text_color=COLORS["ink"])
    rounded_box(ax, (0.77, 0.28), 0.16, 0.28, "right column\narbitrary state", COLORS["mist"], ec=COLORS["navy"], text_color=COLORS["ink"])

    ax.add_patch(Circle((0.50, 0.51), 0.02, color=COLORS["navy"]))
    ax.add_patch(Circle((0.50, 0.33), 0.02, color=COLORS["navy"]))
    ax.add_patch(Circle((0.14, 0.51), 0.02, color=COLORS["navy"]))
    ax.add_patch(Circle((0.14, 0.33), 0.02, color=COLORS["navy"]))
    ax.add_patch(Circle((0.86, 0.51), 0.02, color=COLORS["navy"]))
    ax.add_patch(Circle((0.86, 0.33), 0.02, color=COLORS["navy"]))

    arrow(ax, (0.16, 0.51), (0.48, 0.51), COLORS["teal"], lw=2.4)
    arrow(ax, (0.16, 0.33), (0.48, 0.33), COLORS["teal"], lw=2.4)
    arrow(ax, (0.84, 0.51), (0.52, 0.51), COLORS["teal"], lw=2.4)
    arrow(ax, (0.84, 0.33), (0.52, 0.33), COLORS["teal"], lw=2.4)
    ax.text(0.50, 0.59, "symmetric rail mode", ha="center", va="center", fontsize=12, color=COLORS["teal"], weight="bold")

    ax.plot([0.50, 0.50], [0.35, 0.49], color=COLORS["orange"], linewidth=3.0)
    ax.text(0.53, 0.42, "single rung\nantisymmetric mode", ha="left", va="center", fontsize=11, color=COLORS["orange"], weight="bold")

    rounded_box(
        ax,
        (0.32, 0.73),
        0.36,
        0.12,
        "To force one vertex, the target needs a diagonal antisymmetric component A_j(1,-1).\nA seedless column only carries A_j(v_j), where v_j is the rung label.",
        COLORS["rose"],
        fontsize=10,
    )
    rounded_box(
        ax,
        (0.31, 0.08),
        0.38,
        0.11,
        "Because every nonzero label satisfies a+b ≠ 0, v_j is never parallel to (1,-1).\nThe missing diagonal component blocks the first activation in a seedless column.",
        COLORS["mist"],
        ec=COLORS["rose"],
        text_color=COLORS["ink"],
        fontsize=10,
    )

    ax.text(
        0.50,
        0.94,
        "Width-2 coverability mechanism behind the unilateral strip obstruction",
        ha="center",
        va="center",
        fontsize=17,
        weight="bold",
    )
    save(fig, "fig_coverability_modes")


def fig_strip_no_go() -> None:
    index = trace_index()["local_strip_states"]
    heights = ["height 2", "height 3"]
    checked = [index["width2"]["checked_cases"], index["width3"]["checked_cases"]]
    improved = [index["width2"]["strict_improvement_cases"], index["width3"]["strict_improvement_cases"]]
    factor_labels = ["4 × 16 × 4", "16 × 64 × 8"]

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.6))

    x = range(len(heights))
    axes[0].bar(x, checked, color=[COLORS["navy"], COLORS["teal"]], edgecolor=COLORS["white"], linewidth=1.5, yerr=[0, 0], capsize=4)
    axes[0].set_xticks(list(x), [f"{h}\n{f}" for h, f in zip(heights, factor_labels)])
    axes[0].set_ylabel("Enumerated local states")
    axes[0].set_title("Complete one-sided state spaces")
    axes[0].grid(axis="y")
    for idx, value in enumerate(checked):
        axes[0].text(idx, value + max(checked) * 0.03, f"{value:,}", ha="center", va="bottom", fontsize=10)

    axes[1].barh(heights, improved, color=COLORS["rose"], edgecolor=COLORS["white"], linewidth=1.5)
    axes[1].set_xlim(0, 1)
    axes[1].set_xticks([0, 0.5, 1.0], ["0", "0.5", "1.0"])
    axes[1].set_title("Strict-improvement counts")
    axes[1].set_xlabel("Exact improving states")
    axes[1].grid(axis="x")
    for idx, value in enumerate(improved):
        axes[1].text(0.03, idx, f"0 / {checked[idx]:,}\nexact rate = 0", va="center", fontsize=10, color=COLORS["ink"])

    fig.suptitle("Exhaustive no-go atlas for one-sided fresh-column activation", fontsize=17, weight="bold", y=0.99)
    save(fig, "fig_strip_no_go")


def fig_search_frontier() -> None:
    runs = parse_search_runs()
    ladder_runs = [run for run in runs if run["group"] == "2xN ladders"]
    strip_runs = [run for run in runs if run["group"] == "3xN strips"]

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.8), sharey=True)

    for ax, title, subset, color in (
        (axes[0], "2xN ladders", ladder_runs, COLORS["navy"]),
        (axes[1], "3xN strips", strip_runs, COLORS["orange"]),
    ):
        labels = [run["label"].replace(",", "\n,") for run in subset]
        values = [run["fraction"] for run in subset]
        numerators = [f'{run["forced"]}/{run["total"]}' for run in subset]
        ax.bar(range(len(subset)), values, color=color, edgecolor=COLORS["white"], linewidth=1.5, yerr=[0] * len(subset), capsize=4)
        ax.axhline(1.0, color=COLORS["rose"], linestyle="--", linewidth=1.5)
        ax.set_ylim(0, 1.05)
        ax.set_xticks(range(len(subset)), labels)
        ax.set_title(title)
        ax.set_ylabel("Best forced fraction")
        ax.grid(axis="y")
        for idx, value in enumerate(values):
            ax.text(idx, value + 0.03, numerators[idx], ha="center", va="bottom", fontsize=10)

    fig.suptitle("Best exact forcing fractions in the logged larger-scale search families", fontsize=17, weight="bold", y=0.99)
    save(fig, "fig_search_frontier")


def fig_bridge_decisions() -> None:
    bridges = load_bridge_candidates()
    order_value = {"promote": 0, "hold": 1, "retire": 2}
    bridges = sorted(bridges, key=lambda item: (order_value[item["promotion_decision"]], item["bridge"]))

    labels = [item["bridge"].replace("_", "\n") for item in bridges]
    decision_score = {"promote": 3, "hold": 2, "retire": 1}
    scores = [decision_score[item["promotion_decision"]] for item in bridges]
    colors = [DECISION_COLOR[item["promotion_decision"]] for item in bridges]

    fig, ax = plt.subplots(figsize=(14.0, 8.0))
    ax.barh(range(len(labels)), scores, color=colors, edgecolor=COLORS["white"], linewidth=1.5)
    ax.set_yticks(range(len(labels)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 3.4)
    ax.set_xticks([1, 2, 3], ["Retire", "Hold", "Promote"])
    ax.set_xlabel("Bridge disposition after exact-trace narrowing")
    ax.set_title("Remaining CA-compatible research directions")
    ax.grid(axis="x")

    for idx, item in enumerate(bridges):
        ax.text(scores[idx] + 0.05, idx, item["risk"], va="center", fontsize=10, color=COLORS["ink"])

    legend = [
        Line2D([0], [0], color=DECISION_COLOR["promote"], lw=8, label="Promote"),
        Line2D([0], [0], color=DECISION_COLOR["hold"], lw=8, label="Hold"),
        Line2D([0], [0], color=DECISION_COLOR["retire"], lw=8, label="Retire"),
    ]
    ax.legend(handles=legend, loc="lower right", frameon=False)
    save(fig, "fig_bridge_decisions")


def main() -> None:
    ensure_dirs()
    fig_pipeline()
    fig_architecture()
    fig_exact_nucleus()
    fig_trace_rigidity()
    fig_coverability_modes()
    fig_strip_no_go()
    fig_search_frontier()
    fig_bridge_decisions()


if __name__ == "__main__":
    main()
