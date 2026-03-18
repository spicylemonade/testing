#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
ANALYSIS_DIR = ROOT / "results" / "analysis"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from hadamard_ca.h1_ca import _packet_delta_vector
from hadamard_ca.search import apply_packet, objective_with_score, packet_count
from hadamard_ca.seed import published_frontier_coefficients, published_frontier_sequences


PALETTE = {
    "ink": "#14213d",
    "blue": "#235789",
    "cyan": "#4f8fba",
    "teal": "#2a6f6b",
    "gold": "#f6bd60",
    "orange": "#f28f3b",
    "red": "#c8553d",
    "rose": "#a23b72",
    "sand": "#f4f1de",
    "fog": "#edf2f4",
    "slate": "#6c757d",
    "green": "#7fb069",
}

METHOD_ORDER = [
    "H1_defect_syndrome_ca_64m",
    "greedy",
    "tabu",
    "simulated_annealing",
    "stochastic_hillclimb",
]

METHOD_LABELS = {
    "H1_defect_syndrome_ca_64m": "H1 CA",
    "greedy": "Greedy",
    "tabu": "Tabu",
    "simulated_annealing": "Simulated\nAnnealing",
    "stochastic_hillclimb": "Stochastic\nHillclimb",
}

METHOD_COLORS = {
    "H1_defect_syndrome_ca_64m": PALETTE["rose"],
    "greedy": PALETTE["blue"],
    "tabu": PALETTE["orange"],
    "simulated_annealing": PALETTE["teal"],
    "stochastic_hillclimb": PALETTE["green"],
}


def configure_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.family": "DejaVu Serif",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": PALETTE["slate"],
            "axes.labelcolor": PALETTE["ink"],
            "xtick.color": PALETTE["ink"],
            "ytick.color": PALETTE["ink"],
            "text.color": PALETTE["ink"],
            "axes.grid": True,
            "grid.color": "#d9dde3",
            "grid.linewidth": 0.6,
            "grid.alpha": 0.7,
            "legend.frameon": False,
        }
    )


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def save_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2))


def save_markdown(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n")


def save_figure(fig: plt.Figure, stem: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"{stem}.{ext}", dpi=600, bbox_inches="tight")
    plt.close(fig)


def compute_locality_scan() -> dict[str, object]:
    frontier = published_frontier_sequences()
    q = frontier["q"]
    s = frontier["s"]
    seed = objective_with_score(q, s)
    records: list[dict[str, object]] = []

    for packet in range(packet_count(len(q))):
        channel = "q" if packet < len(q) else "s"
        local_index = int(packet if channel == "q" else packet - len(q))
        delta = _packet_delta_vector(q, s, packet)
        changed_lag_count = int(np.count_nonzero(delta[1:]))
        candidate_q, candidate_s = apply_packet(q, s, packet)
        objective = objective_with_score(candidate_q, candidate_s)

        if objective["score"] < seed["score"]:
            score_comparison = "better"
        elif objective["score"] == seed["score"]:
            score_comparison = "equal"
        else:
            score_comparison = "worse"

        if objective["support_size"] < seed["support_size"]:
            support_comparison = "lower"
        elif objective["support_size"] == seed["support_size"]:
            support_comparison = "equal"
        else:
            support_comparison = "higher"

        records.append(
            {
                "packet": int(packet),
                "channel": channel,
                "local_index": local_index,
                "changed_lag_count": changed_lag_count,
                "score_comparison": score_comparison,
                "support_comparison": support_comparison,
                "objective": objective,
            }
        )

    def summarize_counts(key: str) -> dict[str, int]:
        values = sorted({str(record[key]) for record in records})
        return {value: int(sum(1 for record in records if str(record[key]) == value)) for value in values}

    def summarize_changed(channel: str | None = None) -> dict[str, float]:
        values = [
            int(record["changed_lag_count"])
            for record in records
            if channel is None or record["channel"] == channel
        ]
        array = np.asarray(values, dtype=np.float64)
        return {
            "min": float(np.min(array)),
            "median": float(np.median(array)),
            "mean": float(np.mean(array)),
            "max": float(np.max(array)),
        }

    neutral_packets = [
        {
            "packet": int(record["packet"]),
            "channel": str(record["channel"]),
            "local_index": int(record["local_index"]),
            "changed_lag_count": int(record["changed_lag_count"]),
        }
        for record in records
        if record["score_comparison"] == "equal"
    ]

    payload = {
        "seed_objective": seed,
        "one_packet_scan": {
            "packet_count": int(len(records)),
            "score_comparison_counts": summarize_counts("score_comparison"),
            "support_comparison_counts": summarize_counts("support_comparison"),
            "changed_lag_summary": {
                "overall": summarize_changed(),
                "q_channel": summarize_changed("q"),
                "s_channel": summarize_changed("s"),
            },
            "neutral_packets": neutral_packets,
            "records": records,
        },
    }
    return payload


def write_locality_summary(scan: dict[str, object]) -> None:
    one_packet = scan["one_packet_scan"]
    score_counts = one_packet["score_comparison_counts"]
    support_counts = one_packet["support_comparison_counts"]
    changed = one_packet["changed_lag_summary"]
    neutral_packets = one_packet["neutral_packets"]
    lines = [
        "# Frontier Locality Scan",
        "",
        "Exact one-packet scan on the canonical order-668 frontier seed.",
        "",
        f"- Seed objective: support `{scan['seed_objective']['support_size']}`, "
        f"`l1 = {scan['seed_objective']['l1']}`, `max_abs = {scan['seed_objective']['max_abs']}`.",
        f"- Packets scanned: `{one_packet['packet_count']}`.",
        f"- Score comparison counts: better `{score_counts.get('better', 0)}`, "
        f"equal `{score_counts.get('equal', 0)}`, worse `{score_counts.get('worse', 0)}`.",
        f"- Support comparison counts: lower `{support_counts.get('lower', 0)}`, "
        f"equal `{support_counts.get('equal', 0)}`, higher `{support_counts.get('higher', 0)}`.",
        f"- Changed-lag count summary (overall): min `{int(changed['overall']['min'])}`, "
        f"median `{changed['overall']['median']:.1f}`, mean `{changed['overall']['mean']:.2f}`, "
        f"max `{int(changed['overall']['max'])}`.",
        f"- Changed-lag count summary (`q` channel): min `{int(changed['q_channel']['min'])}`, "
        f"median `{changed['q_channel']['median']:.1f}`, mean `{changed['q_channel']['mean']:.2f}`, "
        f"max `{int(changed['q_channel']['max'])}`.",
        f"- Changed-lag count summary (`s` channel): min `{int(changed['s_channel']['min'])}`, "
        f"median `{changed['s_channel']['median']:.1f}`, mean `{changed['s_channel']['mean']:.2f}`, "
        f"max `{int(changed['s_channel']['max'])}`.",
        "",
        "Neutral packet(s):",
    ]
    for packet in neutral_packets:
        lines.append(
            f"- packet `{packet['packet']}` (`{packet['channel']}[{packet['local_index']}]`) "
            f"changes `{packet['changed_lag_count']}` lag coefficients."
        )
    save_markdown(ANALYSIS_DIR / "frontier_locality_scan.md", "\n".join(lines))


def make_seed_profile_figure() -> None:
    sequences = published_frontier_sequences()
    coeffs = published_frontier_coefficients()[1:]
    nonzero_lags = np.flatnonzero(coeffs) + 1

    fig = plt.figure(figsize=(10.8, 5.9))
    gs = GridSpec(3, 1, figure=fig, height_ratios=[0.7, 0.7, 2.4], hspace=0.25)
    cmap = ListedColormap([PALETTE["blue"], PALETTE["gold"]])

    for row, (label, values) in enumerate((("q", sequences["q"]), ("s", sequences["s"]))):
        ax = fig.add_subplot(gs[row, 0])
        ax.imshow((np.asarray(values) > 0).astype(int)[None, :], aspect="auto", cmap=cmap, vmin=0, vmax=1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_xlim(-0.5, len(values) - 0.5)
        ax.set_ylabel(label, rotation=0, labelpad=14, fontweight="bold")
        ax.set_title(
            "Canonical order-668 frontier seed: compact q/s encoding and exceptional correlation profile"
            if row == 0
            else ""
        )
        ax.text(
            0.99,
            0.15,
            f"{len(values)} signs",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            color=PALETTE["ink"],
            fontsize=9,
        )

    ax = fig.add_subplot(gs[2, 0])
    ax.axhline(0.0, color=PALETTE["slate"], linewidth=1.0)
    colors = [PALETTE["red"] if value < 0 else PALETTE["teal"] for value in coeffs]
    ax.bar(np.arange(1, len(coeffs) + 1), coeffs, color=colors, width=0.85, edgecolor="white", linewidth=0.3)
    ax.set_xlim(0.5, len(coeffs) + 0.5)
    ax.set_xlabel("Lag")
    ax.set_ylabel("Combined correlation coefficient")
    ax.set_xticks([1, 20, 40, 60, 80, 100, 120, 140, 160])
    for lag in nonzero_lags.tolist():
        ax.text(
            lag,
            coeffs[lag - 1] + (24 if coeffs[lag - 1] >= 0 else -24),
            str(lag),
            ha="center",
            va="bottom" if coeffs[lag - 1] >= 0 else "top",
            fontsize=8,
            color=PALETTE["ink"],
        )
    ax.text(
        0.99,
        0.95,
        "13 nonzero lags; 153 zeros",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["fog"], "edgecolor": "#d0d7de"},
    )

    save_figure(fig, "fig01_frontier_seed_profile")


def _draw_box(ax: plt.Axes, xy: tuple[float, float], text: str, width: float, height: float, face: str) -> None:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.0,
        edgecolor=PALETTE["slate"],
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2.0,
        xy[1] + height / 2.0,
        text,
        ha="center",
        va="center",
        fontsize=9,
        wrap=True,
    )


def make_pipeline_figure() -> None:
    fig, ax = plt.subplots(figsize=(11.0, 4.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        ((0.03, 0.56), 0.14, 0.22, "Canonical seed\nq, s in {+1,-1}^167", PALETTE["sand"]),
        ((0.21, 0.56), 0.16, 0.22, "Derived quadruple\n(A, B, C, D)\n= (s, s', sq, (sq)')", PALETTE["fog"]),
        ((0.41, 0.56), 0.16, 0.22, "Lag-syndrome field\nc_1, ..., c_166\nand active mask", "#eef7f6"),
        ((0.61, 0.56), 0.16, 0.22, "Exact packet deltas\nplus spill-aware\nraw pressure", "#fff3e6"),
        ((0.81, 0.56), 0.16, 0.22, "Coupled pressure,\nrefractory memory,\nlocal maxima", "#fceef5"),
        ((0.41, 0.14), 0.20, 0.20, "Asynchronous packet flip,\nobjective update,\nstagnation / budget gate", "#f1f8ec"),
    ]
    for xy, width, height, text, face in boxes:
        _draw_box(ax, xy, text, width, height, face)

    arrows = [
        ((0.17, 0.67), (0.21, 0.67)),
        ((0.37, 0.67), (0.41, 0.67)),
        ((0.57, 0.67), (0.61, 0.67)),
        ((0.77, 0.67), (0.81, 0.67)),
        ((0.89, 0.56), (0.60, 0.34)),
        ((0.51, 0.34), (0.51, 0.56)),
    ]
    for start, end in arrows:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=10,
                linewidth=1.1,
                color=PALETTE["slate"],
                connectionstyle="arc3,rad=0.0",
            )
        )

    callouts = [
        ((0.06, 0.18), "Conserved quantities:\nlength 167, binary alphabet,\nfixed prime involution,\nfixed packet graph"),
        ((0.74, 0.15), "Continuation gate:\nexact hit first;\notherwise H1 must beat\nall matched baselines on\nsupport and magnitude"),
    ]
    for (x, y), text in callouts:
        _draw_box(ax, (x, y), text, 0.22, 0.18, "white")

    ax.text(
        0.02,
        0.95,
        "H1 defect-syndrome CA pipeline in the shared q/s coordinate system",
        fontsize=13,
        fontweight="bold",
        ha="left",
        va="top",
    )

    for center in ((0.13, 0.27), (0.85, 0.24)):
        ax.add_patch(Circle(center, 0.008, color=PALETTE["rose"]))

    save_figure(fig, "fig02_h1_pipeline")


def make_control_figure(control_summary: dict[str, object]) -> None:
    runs = control_summary["runs"]
    methods = METHOD_ORDER
    controls = ["control_n5_q0", "control_n7_q0"]
    exact_matrix = np.zeros((len(methods), len(controls)))
    eval_matrix = np.zeros((len(methods), len(controls)), dtype=int)

    for row, method in enumerate(methods):
        for col, control in enumerate(controls):
            for run in runs:
                if run["method"] == method and run["seed"] == control:
                    exact_matrix[row, col] = 1.0 if run["exact_hit"] else 0.0
                    eval_matrix[row, col] = int(run["objective_evaluations"])
                    break

    fig = plt.figure(figsize=(10.8, 5.0))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.05, 0.95], wspace=0.28)

    ax = fig.add_subplot(gs[0, 0])
    exact_cmap = LinearSegmentedColormap.from_list("exactness", [PALETTE["fog"], PALETTE["teal"]])
    ax.imshow(exact_matrix, cmap=exact_cmap, vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(np.arange(len(controls)))
    ax.set_xticklabels(["n=5 q[0] flip", "n=7 q[0] flip"])
    ax.set_yticks(np.arange(len(methods)))
    ax.set_yticklabels([METHOD_LABELS[method] for method in methods])
    ax.set_title("Exact-hit outcome on the two matched solved controls")
    for row, method in enumerate(methods):
        for col, control in enumerate(controls):
            exact_label = "Y" if exact_matrix[row, col] > 0.5 else "N"
            ax.text(
                col,
                row,
                f"{exact_label}\n{eval_matrix[row, col]} eval",
                ha="center",
                va="center",
                fontsize=8,
                color="white" if exact_matrix[row, col] > 0.5 else PALETTE["ink"],
                fontweight="bold" if exact_matrix[row, col] > 0.5 else None,
            )

    ax = fig.add_subplot(gs[0, 1])
    method_summary = {row["method"]: row for row in control_summary["method_summary"]}
    exact_rates = [float(method_summary[method]["exact_hit_rate"]) for method in methods]
    med_evals = [
        float(np.median(method_summary[method]["objective_evaluations"]))
        for method in methods
    ]
    x = np.arange(len(methods))
    ax.bar(x, exact_rates, color=[METHOD_COLORS[method] for method in methods], width=0.72)
    ax.set_ylim(0.0, 1.15)
    ax.set_ylabel("Exact-hit rate")
    ax.set_title("Aggregate control success and median evaluation use")
    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_LABELS[method] for method in methods])
    ax2 = ax.twinx()
    ax2.plot(x, med_evals, color=PALETTE["ink"], marker="o", linewidth=1.6)
    ax2.set_ylabel("Median evaluations")
    ax2.grid(False)
    for idx, rate in enumerate(exact_rates):
        ax.text(idx, rate + 0.03, f"{rate:.2f}", ha="center", va="bottom", fontsize=8)
        ax2.text(idx, med_evals[idx] + 1.0, f"{med_evals[idx]:.0f}", ha="center", va="bottom", fontsize=8, color=PALETTE["ink"])

    save_figure(fig, "fig03_control_results")


def make_frontier_figure(frontier_summary: dict[str, object]) -> None:
    methods = frontier_summary["methods"]
    seed = frontier_summary["seed_objective"]

    fig = plt.figure(figsize=(12.5, 4.8))
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1.0, 1.0, 1.05], wspace=0.3)
    fig.suptitle(
        "Canonical frontier batch: seed preservation, support diffusion, and runtime mismatch",
        fontsize=13,
        y=1.02,
    )
    support_max_offsets = {
        "greedy": (0.6, 2.8),
        "simulated_annealing": (0.6, 5.2),
        "tabu": (0.6, 2.4),
        "stochastic_hillclimb": (0.8, 2.8),
        "H1_defect_syndrome_ca_64m": (0.8, 2.0),
    }
    support_l1_offsets = {
        "greedy": (0.6, 10.0),
        "simulated_annealing": (0.6, 18.0),
        "tabu": (0.6, 10.0),
        "stochastic_hillclimb": (0.8, 8.0),
        "H1_defect_syndrome_ca_64m": (0.8, 8.0),
    }
    runtime_offsets = {
        "greedy": (1.2, 0.02),
        "tabu": (1.2, 0.04),
        "simulated_annealing": (1.2, 0.02),
        "stochastic_hillclimb": (1.2, 0.02),
        "H1_defect_syndrome_ca_64m": (1.2, 0.02),
    }

    ax = fig.add_subplot(gs[0, 0])
    ax.scatter(
        seed["support_size"],
        seed["max_abs"],
        marker="*",
        s=220,
        color=PALETTE["gold"],
        edgecolors=PALETTE["ink"],
        linewidths=0.8,
        label="Published seed",
        zorder=5,
    )
    ax.text(seed["support_size"] + 0.8, seed["max_abs"] - 1.0, "Seed", fontsize=8)
    for method in methods:
        name = method["method_name"]
        ax.scatter(
            method["terminal_support_median"],
            method["terminal_max_abs_median"],
            s=95,
            color=METHOD_COLORS[name],
            edgecolors="white",
            linewidths=0.8,
            zorder=4,
        )
        dx, dy = support_max_offsets[name]
        ax.text(
            method["terminal_support_median"] + dx,
            method["terminal_max_abs_median"] + dy,
            METHOD_LABELS[name].replace("\n", " "),
            fontsize=8,
        )
    ax.set_xlabel("Median terminal support")
    ax.set_ylabel("Median terminal max defect")
    ax.set_title("Terminal support vs. max defect")
    ax.legend(loc="upper right")

    ax = fig.add_subplot(gs[0, 1])
    ax.scatter(
        seed["support_size"],
        seed["l1"],
        marker="*",
        s=220,
        color=PALETTE["gold"],
        edgecolors=PALETTE["ink"],
        linewidths=0.8,
        zorder=5,
    )
    ax.text(seed["support_size"] + 0.8, seed["l1"] + 8.0, "Seed", fontsize=8)
    for method in methods:
        name = method["method_name"]
        ax.scatter(
            method["terminal_support_median"],
            method["terminal_l1_median"],
            s=95,
            color=METHOD_COLORS[name],
            edgecolors="white",
            linewidths=0.8,
            zorder=4,
        )
        dx, dy = support_l1_offsets[name]
        ax.text(
            method["terminal_support_median"] + dx,
            method["terminal_l1_median"] + dy,
            METHOD_LABELS[name].replace("\n", " "),
            fontsize=8,
        )
    ax.set_xlabel("Median terminal support")
    ax.set_ylabel("Median terminal l1 defect")
    ax.set_title("Terminal support vs. l1 defect")

    ax = fig.add_subplot(gs[0, 2])
    for method in methods:
        name = method["method_name"]
        ax.scatter(
            method["objective_evaluations"],
            method["wall_seconds"],
            s=115,
            color=METHOD_COLORS[name],
            edgecolors="white",
            linewidths=0.8,
        )
        dx, dy = runtime_offsets[name]
        ax.text(
            method["objective_evaluations"] + dx,
            method["wall_seconds"] + dy,
            METHOD_LABELS[name].replace("\n", " "),
            fontsize=8,
        )
    ax.set_xlabel("Objective evaluations")
    ax.set_ylabel("Wall time (s)")
    ax.set_title("Evaluations vs. wall time")

    save_figure(fig, "fig04_frontier_comparison")


def make_locality_figure(scan: dict[str, object]) -> None:
    records = scan["one_packet_scan"]["records"]
    q_counts = [record["changed_lag_count"] for record in records if record["channel"] == "q"]
    s_counts = [record["changed_lag_count"] for record in records if record["channel"] == "s"]
    score_counts = scan["one_packet_scan"]["score_comparison_counts"]
    support_counts = scan["one_packet_scan"]["support_comparison_counts"]

    fig = plt.figure(figsize=(12.2, 4.8))
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1.2, 0.9, 0.9], wspace=0.28)

    ax = fig.add_subplot(gs[0, 0])
    bins = np.arange(-0.5, 84.5, 4.0)
    ax.hist(q_counts, bins=bins, alpha=0.75, color=PALETTE["blue"], label="q-packets")
    ax.hist(s_counts, bins=bins, alpha=0.7, color=PALETTE["orange"], label="s-packets")
    ax.axvline(np.median(q_counts + s_counts), color=PALETTE["ink"], linestyle="--", linewidth=1.2)
    ax.text(
        np.median(q_counts + s_counts) + 1.5,
        ax.get_ylim()[1] * 0.9,
        f"median = {np.median(q_counts + s_counts):.1f}",
        fontsize=8,
        color=PALETTE["ink"],
    )
    ax.set_xlabel("Lag coefficients changed by one packet flip")
    ax.set_ylabel("Packet count")
    ax.set_title("Single packets are syntactically local but globally disruptive")
    ax.legend(loc="upper right")

    ax = fig.add_subplot(gs[0, 1])
    score_categories = ["better", "equal", "worse"]
    score_values = [score_counts.get(category, 0) for category in score_categories]
    ax.bar(
        np.arange(len(score_categories)),
        score_values,
        color=[PALETTE["green"], PALETTE["gold"], PALETTE["red"]],
        width=0.72,
    )
    ax.set_xticks(np.arange(len(score_categories)))
    ax.set_xticklabels(score_categories)
    ax.set_ylabel("Count")
    ax.set_title("One-packet score outcomes")
    for idx, value in enumerate(score_values):
        ax.text(idx, value + 4, str(value), ha="center", va="bottom", fontsize=9)

    ax = fig.add_subplot(gs[0, 2])
    support_categories = ["lower", "equal", "higher"]
    support_values = [support_counts.get(category, 0) for category in support_categories]
    ax.bar(
        np.arange(len(support_categories)),
        support_values,
        color=[PALETTE["green"], PALETTE["gold"], PALETTE["red"]],
        width=0.72,
    )
    ax.set_xticks(np.arange(len(support_categories)))
    ax.set_xticklabels(support_categories)
    ax.set_ylabel("Count")
    ax.set_title("One-packet support outcomes")
    for idx, value in enumerate(support_values):
        ax.text(idx, value + 4, str(value), ha="center", va="bottom", fontsize=9)

    save_figure(fig, "fig05_locality_scan")


def make_h1_dynamics_figure(h1_run: dict[str, object], sensitivity_probe: dict[str, object]) -> None:
    trace = h1_run["trace"]
    restarts = sorted({int(entry["restart"]) for entry in trace})
    fig = plt.figure(figsize=(12.2, 6.2))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0], wspace=0.28, hspace=0.3)

    ax = fig.add_subplot(gs[:, 0])
    seed_support = trace[0]["support_size"]
    seed_max_abs = trace[0]["max_abs"]
    ax.scatter(
        seed_support,
        seed_max_abs,
        marker="*",
        s=240,
        color=PALETTE["gold"],
        edgecolors=PALETTE["ink"],
        linewidths=0.8,
        zorder=5,
        label="Seed / best state",
    )
    restart_colors = [PALETTE["rose"], PALETTE["blue"], PALETTE["orange"]]
    for color, restart in zip(restart_colors, restarts):
        series = [entry for entry in trace if int(entry["restart"]) == restart]
        xs = [entry["support_size"] for entry in series]
        ys = [entry["max_abs"] for entry in series]
        ax.plot(xs, ys, marker="o", color=color, linewidth=1.8, markersize=4.8, label=f"Restart {restart}")
    ax.set_xlabel("Support size")
    ax.set_ylabel("Max defect magnitude")
    ax.set_title("H1 frontier trajectories: lower magnitude only via higher support")
    ax.legend(loc="upper right")

    ax = fig.add_subplot(gs[0, 1])
    for color, restart in zip(restart_colors, restarts):
        series = [entry for entry in trace if int(entry["restart"]) == restart]
        steps = list(range(len(series)))
        supports = [entry["support_size"] for entry in series]
        ax.plot(steps, supports, marker="o", color=color, linewidth=1.8, markersize=4.2)
    ax.axhline(seed_support, color=PALETTE["slate"], linestyle="--", linewidth=1.0)
    ax.set_xlabel("Accepted state index within restart")
    ax.set_ylabel("Support size")
    ax.set_title("Support diffuses on every completed restart")

    ax = fig.add_subplot(gs[1, 1])
    rows = sensitivity_probe["rows"]
    labels = [row["config"]["name"] for row in rows]
    evaluations = [int(row["objective_evaluations"]) for row in rows]
    field_evaluations = [int(row["ca_field_evaluations"]) for row in rows]
    y = np.arange(len(rows))
    ax.barh(y + 0.18, field_evaluations, height=0.34, color=PALETTE["cyan"], label="CA field evals")
    ax.barh(y - 0.18, evaluations, height=0.34, color=PALETTE["rose"], label="Objective evals")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Evaluation count")
    ax.set_title("Sensitivity probe: all eight variants stayed pinned to the seed")
    ax.legend(loc="lower right")
    for idx, row in enumerate(rows):
        ax.text(
            field_evaluations[idx] + 55,
            idx + 0.18,
            "best delta = 0",
            va="center",
            fontsize=8,
        )

    save_figure(fig, "fig06_h1_dynamics")


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)
    ANALYSIS_DIR.mkdir(exist_ok=True)
    configure_style()

    frontier_summary = load_json(ROOT / "results" / "experiments" / "order_668_64m" / "summary.json")
    control_summary = load_json(ROOT / "results" / "experiments" / "controls" / "summary.json")
    h1_run = load_json(ROOT / "results" / "experiments" / "order_668_64m" / "runs" / "H1_defect_syndrome_ca_64m.json")
    sensitivity_probe = load_json(ROOT / "results" / "branches" / "H1_frontier_sensitivity_probe.json")

    locality_scan = compute_locality_scan()
    save_json(ANALYSIS_DIR / "frontier_locality_scan.json", locality_scan)
    write_locality_summary(locality_scan)

    make_seed_profile_figure()
    make_pipeline_figure()
    make_control_figure(control_summary)
    make_frontier_figure(frontier_summary)
    make_locality_figure(locality_scan)
    make_h1_dynamics_figure(h1_run, sensitivity_probe)


if __name__ == "__main__":
    main()
