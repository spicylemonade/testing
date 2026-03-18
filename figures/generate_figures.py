#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
from pathlib import Path
from statistics import mean

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"
ANALYSIS_DIR = RESULTS_DIR / "analysis"
ARTIFACT_DIR = RESULTS_DIR / "artifacts"
EXPERIMENT_DIR = RESULTS_DIR / "experiments"
METRICS_PATH = ANALYSIS_DIR / "paper_metrics.json"


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

METHOD_COLORS = {
    "parallel_gain_ca": PALETTE["teal"],
    "direct_greedy": PALETTE["navy"],
    "random_rule_ca": PALETTE["rust"],
    "random_walk": PALETTE["slate"],
}

BRANCH_COLORS = {
    "H1": PALETTE["navy"],
    "H2": PALETTE["rust"],
    "R1": PALETTE["teal"],
    "R2": PALETTE["sand"],
    "R3": PALETTE["olive"],
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
            "legend.fontsize": 9.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def bootstrap_interval(values, statistic="mean", draws=4000, seed=0):
    values = list(values)
    if not values:
        return [None, None]
    rng = random.Random(seed)
    if statistic == "mean":
        fn = lambda sample: sum(sample) / len(sample)
    elif statistic == "median":
        fn = lambda sample: float(np.median(sample))
    else:
        raise ValueError(f"unknown statistic {statistic}")
    estimates = []
    for _ in range(draws):
        sample = [rng.choice(values) for _ in values]
        estimates.append(fn(sample))
    estimates.sort()
    lo = estimates[int(0.025 * len(estimates))]
    hi = estimates[int(0.975 * len(estimates))]
    return [lo, hi]


def wilson_interval(successes: int, total: int, z: float = 1.96) -> list[float]:
    if total == 0:
        return [0.0, 0.0]
    phat = successes / total
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2 * total)) / denom
    radius = (
        z
        * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total)
        / denom
    )
    return [max(0.0, center - radius), min(1.0, center + radius)]


def grouped_runs(data: dict) -> dict[tuple[str, int], dict[str, dict]]:
    grouped: dict[tuple[str, int], dict[str, dict]] = {}
    for run in data["runs"]:
        key = (str(run["seed_family"]), int(run["deterministic_seed"]))
        grouped.setdefault(key, {})[str(run["method"])] = run
    return grouped


def compute_metrics() -> dict:
    control = load_json(ARTIFACT_DIR / "control_4x79.json")
    target = load_json(ARTIFACT_DIR / "target_167_weight_80.json")
    seed = load_json(ARTIFACT_DIR / "seed_668_mod64.json")
    h2_control = load_json(ARTIFACT_DIR / "h2_control_structured_n9.json")
    h1_control = load_json(EXPERIMENT_DIR / "h1_control_sweep.json")
    h1_target = load_json(EXPERIMENT_DIR / "h1_target_sweep.json")
    h2_ladder = load_json(EXPERIMENT_DIR / "h2_ladder.json")
    h2_seed = load_json(EXPERIMENT_DIR / "h2_seed_attempt.json")

    metrics: dict[str, object] = {
        "artifacts": {
            "control_4x79": {
                "length": control["length"],
                "fixed_weights": [item["weight"] for item in control["fixed_vectors"]],
                "solution_weight": control["solution"]["weight"],
            },
            "target_167_weight_80": {
                "length": target["length"],
                "fixed_weights": [item["weight"] for item in target["fixed_vectors"]],
                "required_weight": target["unknown_vector"]["required_weight"],
                "target_half": target["target_periodic_autocorrelation_half"],
            },
            "seed_668_mod64": {
                "length": seed["length"],
                "order": seed["order"],
                "two_adic_modulus": seed["two_adic_modulus"],
                "nonzero_defects": seed["nonzero_defects"],
            },
            "h2_control_structured_n9": {
                "length": h2_control["length"],
                "search_space": h2_control["search_space"],
                "lift_starts": [item["name"] for item in h2_control["lift_starts"]],
            },
        }
    }

    for label, data in [("h1_control", h1_control), ("h1_target", h1_target)]:
        block: dict[str, object] = {"methods": {}, "paired": {}, "best_steps": {}}
        grouped = grouped_runs(data)
        for method in ["direct_greedy", "parallel_gain_ca", "random_rule_ca", "random_walk"]:
            runs = [run for run in data["runs"] if run["method"] == method]
            distances = [int(run["best_state"]["closest_target_distance"]) for run in runs]
            orbits = [int(run["unique_orbits"]) for run in runs]
            accepted = [int(run["accepted_moves"]) for run in runs]
            best_steps = [int(run["best_step"]) for run in runs]
            block["methods"][method] = {
                "n": len(runs),
                "distance_mean": mean(distances),
                "distance_ci95": bootstrap_interval(distances, "mean", seed=hash(label + method) % 10000),
                "distance_values": distances,
                "unique_orbits_median": float(np.median(orbits)),
                "unique_orbits_ci95": bootstrap_interval(orbits, "median", seed=hash("orbit" + label + method) % 10000),
                "unique_orbits_values": orbits,
                "accepted_moves_median": float(np.median(accepted)),
                "best_steps": best_steps,
            }
            block["best_steps"][method] = best_steps
        pair_rows = []
        dg_wins = 0
        ca_wins = 0
        ties = 0
        for (seed_family, det_seed), pair in sorted(grouped.items()):
            if "direct_greedy" not in pair or "parallel_gain_ca" not in pair:
                continue
            dg = int(pair["direct_greedy"]["best_state"]["closest_target_distance"])
            ca = int(pair["parallel_gain_ca"]["best_state"]["closest_target_distance"])
            if dg < ca:
                dg_wins += 1
            elif ca < dg:
                ca_wins += 1
            else:
                ties += 1
            pair_rows.append(
                {
                    "seed_family": seed_family,
                    "deterministic_seed": det_seed,
                    "direct_greedy": dg,
                    "parallel_gain_ca": ca,
                    "delta_dg_minus_ca": dg - ca,
                }
            )
        block["paired"] = {
            "rows": pair_rows,
            "direct_greedy_wins": dg_wins,
            "parallel_gain_ca_wins": ca_wins,
            "ties": ties,
        }
        metrics[label] = block

    ladder_block: dict[str, object] = {"methods": {}}
    for method in ["parallel_gain_ca", "direct_greedy", "random_rule_ca", "random_walk"]:
        runs = [run for run in h2_ladder["runs"] if run["method"] == method]
        successes = sum(1 for run in runs if bool(run["goal_hit"]))
        best_l1 = [int(run["best_state"]["l1_defect"]) for run in runs]
        ladder_block["methods"][method] = {
            "n": len(runs),
            "goal_hit_rate": successes / len(runs),
            "goal_hit_ci95": wilson_interval(successes, len(runs)),
            "best_l1_values": best_l1,
            "best_l1_mean": mean(best_l1),
            "best_l1_ci95": bootstrap_interval(best_l1, "mean", seed=hash(method) % 10000),
        }
    metrics["h2_ladder"] = ladder_block

    seed_block: dict[str, object] = {"methods": {}}
    for run in h2_seed["runs"]:
        method = str(run["method"])
        seed_block["methods"][method] = {
            "best_step": int(run["best_step"]),
            "unique_orbits": int(run["unique_orbits"]),
            "accepted_moves": int(run["accepted_moves"]),
            "best_state": {
                "two_adic_modulus": int(run["best_state"]["two_adic_modulus"]),
                "l1_defect": int(run["best_state"]["l1_defect"]),
                "defect_count": int(run["best_state"]["defect_count"]),
                "max_defect_magnitude": int(run["best_state"]["max_defect_magnitude"]),
            },
            "final_state": {
                "two_adic_modulus": int(run["final_state"]["two_adic_modulus"]),
                "l1_defect": int(run["final_state"]["l1_defect"]),
                "defect_count": int(run["final_state"]["defect_count"]),
                "max_defect_magnitude": int(run["final_state"]["max_defect_magnitude"]),
            },
        }
    metrics["h2_seed_attempt"] = seed_block

    return metrics


def save_metrics(metrics: dict) -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))


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


def figure_problem_objects(metrics: dict) -> None:
    target = metrics["artifacts"]["target_167_weight_80"]["target_half"]
    defects = metrics["artifacts"]["seed_668_mod64"]["nonzero_defects"]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), constrained_layout=True)
    ax = axes[0]
    shifts = np.arange(1, len(target) + 1)
    ax.plot(shifts, target, color=PALETTE["navy"], lw=2.2)
    ax.fill_between(shifts, target, color=PALETTE["navy"], alpha=0.12)
    ax.set_title("Exact H1 Obstruction")
    ax.set_xlabel("Shift $k$")
    ax.set_ylabel(r"Target half-autocorrelation $\tau_k$")
    ax.grid(True, axis="y")
    ax.set_xlim(1, len(target))
    panel_label(ax, "a")

    ax = axes[1]
    x = [item["shift"] for item in defects]
    y = [item["value"] for item in defects]
    colors = [PALETTE["rust"] if value < 0 else PALETTE["teal"] for value in y]
    ax.axhline(0, color=PALETTE["ink"], lw=0.9)
    ax.vlines(x, [0], y, colors=colors, lw=2.0)
    ax.scatter(x, y, s=34, c=colors, zorder=3, edgecolors="white", linewidths=0.5)
    ax.set_title("Published Mod-64 Seed Defects")
    ax.set_xlabel("Shift")
    ax.set_ylabel("Combined aperiodic defect")
    ax.grid(True, axis="y")
    ax.set_xlim(0, 167)
    panel_label(ax, "b")

    save_figure(fig, "fig_problem_objects")


def add_box(ax, xy, width, height, text, facecolor, edgecolor=PALETTE["ink"], fontsize=10):
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


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, (0.04, 0.70), 0.18, 0.18, "User prompt:\n\"cellar automata\"\nfor Hadamard 668", PALETTE["cloud"])
    add_box(ax, (0.28, 0.70), 0.20, 0.18, "Interpretation split:\ncellular automata\nvs. literal reserve\n\"cellar\" reading", "#eef5f3")
    add_box(ax, (0.55, 0.76), 0.17, 0.12, "H1:\n167-cycle support CA", "#e8eef5")
    add_box(ax, (0.55, 0.56), 0.17, 0.12, "H2:\nmod-64 defect-transport CA", "#f7ece8")
    add_box(ax, (0.79, 0.76), 0.16, 0.12, "Matched baseline:\n`direct_greedy`", "#f0f3f6")
    add_box(ax, (0.79, 0.56), 0.16, 0.12, "Negative controls:\nrandom rule / walk", "#f0f3f6")
    add_box(ax, (0.29, 0.28), 0.22, 0.16, "Reserve R1:\nautocorrelation\ndebt pushdown\n(literal `cellar`)", "#e8f3ef")
    add_box(ax, (0.56, 0.28), 0.18, 0.16, "Reserve R2/R3:\nSAT-propagator / \nconvolution-slice", "#f2f5ea")
    add_box(ax, (0.80, 0.28), 0.15, 0.16, "Final gate:\nallow only a\nnarrow no-go claim", "#f7f2e8")
    add_box(ax, (0.56, 0.08), 0.18, 0.10, "H1 stop:\nloses on control\nand target", "#fbe8e6")
    add_box(ax, (0.79, 0.08), 0.16, 0.10, "H2 stop:\nties on the only\nreal 668 start", "#fbe8e6")

    add_arrow(ax, (0.22, 0.79), (0.28, 0.79))
    add_arrow(ax, (0.48, 0.82), (0.55, 0.82), color=PALETTE["navy"])
    add_arrow(ax, (0.48, 0.62), (0.55, 0.62), color=PALETTE["rust"])
    add_arrow(ax, (0.72, 0.82), (0.79, 0.82))
    add_arrow(ax, (0.72, 0.62), (0.79, 0.62))
    add_arrow(ax, (0.39, 0.70), (0.39, 0.44), color=PALETTE["teal"])
    add_arrow(ax, (0.64, 0.28), (0.64, 0.18), color=PALETTE["rust"])
    add_arrow(ax, (0.87, 0.28), (0.87, 0.18), color=PALETTE["navy"])
    add_arrow(ax, (0.51, 0.36), (0.56, 0.36))
    add_arrow(ax, (0.74, 0.36), (0.80, 0.36))

    ax.text(0.55, 0.92, "Executed branches", color=PALETTE["ink"], fontsize=11, fontweight="bold")
    ax.text(0.30, 0.50, "Reserve concepts remain unvalidated", color=PALETTE["teal"], fontsize=10.5, fontweight="bold")

    save_figure(fig, "fig_program_flow")


def figure_h1_mechanism() -> None:
    fig = plt.figure(figsize=(11.6, 5.2), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.2])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    ax0.set_aspect("equal")
    ax0.axis("off")
    n = 24
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(theta)
    y = np.sin(theta)
    support = {0, 1, 2, 4, 5, 7, 11, 12, 16, 18, 19, 21}
    for idx in range(n):
        ax0.add_patch(
            Circle(
                (x[idx], y[idx]),
                0.08,
                facecolor=PALETTE["navy"] if idx in support else "white",
                edgecolor=PALETTE["ink"],
                lw=1.1,
            )
        )
    phase_edges = {
        "phase 1": [(idx, idx + 1) for idx in range(0, n - 1, 2)],
        "phase 2": [(idx, idx + 1) for idx in range(1, n - 1, 2)],
        "phase 3": [(n - 1, 0)],
    }
    phase_cols = [PALETTE["teal"], PALETTE["sand"], PALETTE["rust"]]
    for (name, edges), color in zip(phase_edges.items(), phase_cols):
        for left, right in edges:
            ax0.plot([x[left], x[right]], [y[left], y[right]], color=color, lw=2.2, alpha=0.9)
    ax0.text(0, 1.34, "Stylized H1 state on a cycle", ha="center", fontsize=12, fontweight="bold")
    ax0.text(0, -1.35, "Support bits are conserved; only `01`/`10` edges may swap.", ha="center", fontsize=9.5)
    ax0.text(-1.28, 1.03, "Phase 1", color=phase_cols[0], fontsize=10.5, fontweight="bold")
    ax0.text(-1.28, 0.88, "Phase 2", color=phase_cols[1], fontsize=10.5, fontweight="bold")
    ax0.text(-1.28, 0.73, "Phase 3", color=phase_cols[2], fontsize=10.5, fontweight="bold")
    panel_label(ax0, "a")

    ax1.axis("off")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    add_box(ax1, (0.06, 0.73), 0.86, 0.16, "Enumerate admissible adjacent swaps on the active matching.", "#edf3f7")
    add_box(ax1, (0.06, 0.49), 0.86, 0.16, "Compute the exact change in the target-distance objective by updating only the affected cyclic products.", "#e9f4f1")
    add_box(ax1, (0.06, 0.25), 0.40, 0.16, "CA rule:\nselect locally dominant improving swaps,\nthen fire up to `phase_move_cap=4` in parallel.", "#e6f4ef")
    add_box(ax1, (0.52, 0.25), 0.40, 0.16, "Matched baseline:\nsort the same improving swaps by gain,\nthen take the top improving moves.", "#e7edf6")
    add_arrow(ax1, (0.49, 0.73), (0.49, 0.65))
    add_arrow(ax1, (0.49, 0.49), (0.49, 0.41))
    add_arrow(ax1, (0.49, 0.25), (0.49, 0.19), style="<|-|>")
    ax1.text(0.50, 0.08, "The fairness lock holds state, neighborhood, verifier, budget, and move cap fixed.", ha="center", fontsize=10)
    panel_label(ax1, "b")

    save_figure(fig, "fig_h1_mechanism")


def add_ci_bars(ax, x_positions, means, cis, colors):
    for xpos, mean_value, ci, color in zip(x_positions, means, cis, colors):
        lo, hi = ci
        ax.bar(xpos, mean_value, color=color, width=0.7, edgecolor="white")
        ax.errorbar(
            xpos,
            mean_value,
            yerr=[[mean_value - lo], [hi - mean_value]],
            fmt="none",
            ecolor=PALETTE["ink"],
            capsize=4,
            lw=1.0,
        )


def figure_h1_results(metrics: dict) -> None:
    fig = plt.figure(figsize=(12.2, 7.0), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)
    methods = ["direct_greedy", "parallel_gain_ca", "random_rule_ca", "random_walk"]
    labels = ["Direct", "CA", "Rnd-CA", "Rnd-walk"]

    for idx, block_name in enumerate(["h1_control", "h1_target"]):
        ax = fig.add_subplot(gs[0, idx])
        block = metrics[block_name]["methods"]
        means = [block[method]["distance_mean"] for method in methods]
        cis = [block[method]["distance_ci95"] for method in methods]
        colors = [METHOD_COLORS[method] for method in methods]
        add_ci_bars(ax, np.arange(len(methods)), means, cis, colors)
        ax.set_xticks(np.arange(len(methods)), labels)
        ax.set_ylabel("Best distance to target")
        ax.set_title("Control sweep" if block_name == "h1_control" else "Target sweep")
        ax.grid(True, axis="y")
        if block_name == "h1_control":
            panel_label(ax, "a")
        else:
            panel_label(ax, "b")

    for idx, block_name in enumerate(["h1_control", "h1_target"]):
        ax = fig.add_subplot(gs[1, idx])
        rows = metrics[block_name]["paired"]["rows"]
        for row in rows:
            seed_color = PALETTE["sand"] if row["seed_family"] == "perturbed_solution" else PALETTE["mist"]
            if row["seed_family"] == "modular_projection":
                seed_color = "#dbe8df"
            ax.plot([0, 1], [row["parallel_gain_ca"], row["direct_greedy"]], color=seed_color, lw=1.2, alpha=0.95)
            ax.scatter([0, 1], [row["parallel_gain_ca"], row["direct_greedy"]], c=[METHOD_COLORS["parallel_gain_ca"], METHOD_COLORS["direct_greedy"]], s=24, zorder=3, edgecolors="white", linewidths=0.4)
        ax.set_xticks([0, 1], ["CA", "Direct"])
        ax.set_ylabel("Best distance")
        ax.grid(True, axis="y")
        wins = metrics[block_name]["paired"]["direct_greedy_wins"]
        losses = metrics[block_name]["paired"]["parallel_gain_ca_wins"]
        ties = metrics[block_name]["paired"]["ties"]
        ax.set_title(f"Paired seeds: direct wins {wins}, CA wins {losses}, ties {ties}")
        if block_name == "h1_control":
            panel_label(ax, "c")
        else:
            panel_label(ax, "d")

    save_figure(fig, "fig_h1_results")


def ecdf(values):
    values = np.asarray(sorted(values), dtype=float)
    y = np.arange(1, len(values) + 1) / len(values)
    return values, y


def figure_h1_dynamics(metrics: dict) -> None:
    fig = plt.figure(figsize=(12.0, 5.6), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.0, 1.0])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[0, 2])

    blocks = [("h1_control", "Control"), ("h1_target", "Target")]
    x = np.arange(len(blocks))
    width = 0.18
    offsets = np.linspace(-1.5 * width, 1.5 * width, 4)
    for offset, method in zip(offsets, ["direct_greedy", "parallel_gain_ca", "random_rule_ca", "random_walk"]):
        medians = [metrics[name]["methods"][method]["unique_orbits_median"] for name, _ in blocks]
        cis = [metrics[name]["methods"][method]["unique_orbits_ci95"] for name, _ in blocks]
        means = medians
        add_ci_bars(ax0, x + offset, means, cis, [METHOD_COLORS[method]] * len(blocks))
    ax0.set_xticks(x, [label for _, label in blocks])
    ax0.set_ylabel("Median unique orbits")
    ax0.set_title("Reachability differs sharply")
    ax0.grid(True, axis="y")
    panel_label(ax0, "a")

    for ax, block_name, title, label in [
        (ax1, "h1_control", "Best-step ECDF on control", "b"),
        (ax2, "h1_target", "Best-step ECDF on target", "c"),
    ]:
        for method in ["parallel_gain_ca", "direct_greedy"]:
            xs, ys = ecdf(metrics[block_name]["best_steps"][method])
            ax.step(xs, ys, where="post", color=METHOD_COLORS[method], lw=2.0, label="CA" if method == "parallel_gain_ca" else "Direct")
        ax.set_xlabel("Step of best recorded state")
        ax.set_ylabel("Empirical CDF")
        ax.set_title(title)
        ax.grid(True)
        ax.legend(loc="lower right")
        panel_label(ax, label)

    save_figure(fig, "fig_h1_dynamics")


def figure_h2_mechanism_results(metrics: dict) -> None:
    fig = plt.figure(figsize=(12.4, 7.2), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    ax0.axis("off")
    ax0.set_xlim(0, 1)
    ax0.set_ylim(0, 1)
    add_box(ax0, (0.06, 0.72), 0.32, 0.14, "$q$ line\nflip affects $C,D$", "#eef1f7")
    add_box(ax0, (0.06, 0.46), 0.32, 0.14, "$s$ line\nflip affects $A,B,C,D$", "#eef8f5")
    add_box(ax0, (0.52, 0.72), 0.34, 0.14, "Derived sequences:\n$A=s$, $B=s_0$, $C=sq$, $D=(sq)_0$", "#f6f1e7")
    add_box(ax0, (0.52, 0.46), 0.34, 0.14, "Objective rank:\nmaximize modulus, then minimize $(\\ell_1,\\#\\mathrm{defects},\\max |d|)$", "#f5ece8")
    add_box(ax0, (0.24, 0.18), 0.46, 0.14, "Parity-phase search: evaluate one index family per step, cap accepted moves at 4.", "#edf3f7")
    add_arrow(ax0, (0.38, 0.79), (0.52, 0.79))
    add_arrow(ax0, (0.38, 0.53), (0.52, 0.53))
    add_arrow(ax0, (0.69, 0.46), (0.47, 0.32))
    panel_label(ax0, "a")

    methods = ["parallel_gain_ca", "direct_greedy", "random_rule_ca", "random_walk"]
    labels = ["CA", "Direct", "Rnd-CA", "Rnd-walk"]
    block = metrics["h2_ladder"]["methods"]
    rates = [block[m]["goal_hit_rate"] for m in methods]
    cis = [block[m]["goal_hit_ci95"] for m in methods]
    add_ci_bars(ax1, np.arange(len(methods)), rates, cis, [METHOD_COLORS[m] for m in methods])
    ax1.set_xticks(np.arange(len(methods)), labels)
    ax1.set_ylim(0, 1.08)
    ax1.set_ylabel("Goal-hit rate on $n=9$ ladder")
    ax1.set_title("Toy ladder is weakly discriminative")
    ax1.grid(True, axis="y")
    panel_label(ax1, "b")

    block = metrics["h2_seed_attempt"]["methods"]
    methods_seed = ["parallel_gain_ca", "direct_greedy", "random_rule_ca", "random_walk"]
    xpos = np.arange(len(methods_seed))
    best = [block[m]["best_state"]["l1_defect"] for m in methods_seed]
    final = [block[m]["final_state"]["l1_defect"] for m in methods_seed]
    ax2.bar(xpos - 0.18, best, width=0.36, color=[METHOD_COLORS[m] for m in methods_seed], alpha=0.95, label="Best state")
    ax2.bar(xpos + 0.18, final, width=0.36, color=[METHOD_COLORS[m] for m in methods_seed], alpha=0.28, label="Final state")
    ax2.set_xticks(xpos, labels)
    ax2.set_ylabel(r"$\ell_1$ defect on the real 668 run")
    ax2.set_title("Serious methods tie on the only real start")
    ax2.grid(True, axis="y")
    ax2.legend(loc="upper right")
    panel_label(ax2, "c")

    width = 0.28
    unique_orbits = [block[m]["unique_orbits"] for m in methods_seed]
    modulus = [block[m]["best_state"]["two_adic_modulus"] for m in methods_seed]
    ax3.bar(xpos - width / 2, unique_orbits, width=width, color=[METHOD_COLORS[m] for m in methods_seed], label="Unique orbits")
    ax3.bar(xpos + width / 2, modulus, width=width, color=PALETTE["gold"], label="Best modulus")
    ax3.set_xticks(xpos, labels)
    ax3.set_ylabel("Orbit count / modulus")
    ax3.set_title("Coverage grows for weak controls, not for the tied serious methods")
    ax3.grid(True, axis="y")
    ax3.legend(loc="upper left")
    panel_label(ax3, "d")

    save_figure(fig, "fig_h2_results")


def figure_branch_matrix() -> None:
    rows = [
        ("H1 executed", [1, 1, 1, 0, 0, 0]),
        ("H2 executed", [1, 1, 1, 0, 0, 0]),
        ("R1 cellar / pushdown", [1, 0, 0, 0, 0, 1]),
        ("R2 SAT-propagator", [0, 0, 0, 0, 0, 1]),
        ("R3 convolution-slice", [1, 0, 0, 0, 0, 1]),
    ]
    columns = [
        "Exact anchor",
        "Executed",
        "Matched baseline",
        "Positive result",
        "Validated contribution",
        "Reserve only",
    ]
    data = np.array([row[1] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10.8, 4.8), constrained_layout=True)
    cmap = mpl.colors.ListedColormap([PALETTE["cloud"], PALETTE["teal"]])
    ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(columns)), columns, rotation=20, ha="right")
    ax.set_yticks(np.arange(len(rows)), [row[0] for row in rows])
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, "yes" if data[i, j] else "no", ha="center", va="center", color=PALETTE["ink"], fontsize=9)
    ax.set_title("Executed and reserve branches separate cleanly")
    ax.set_xticks(np.arange(-0.5, len(columns), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    save_figure(fig, "fig_branch_matrix")


def main() -> int:
    configure_style()
    metrics = compute_metrics()
    save_metrics(metrics)
    figure_problem_objects(metrics)
    figure_pipeline()
    figure_h1_mechanism()
    figure_h1_results(metrics)
    figure_h1_dynamics(metrics)
    figure_h2_mechanism_results(metrics)
    figure_branch_matrix()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
