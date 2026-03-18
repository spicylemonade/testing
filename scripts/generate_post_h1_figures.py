#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


PALETTE = {
    "ink": "#18222f",
    "navy": "#1f4e5f",
    "teal": "#278c82",
    "green": "#77a65a",
    "gold": "#e6b655",
    "orange": "#d97841",
    "brick": "#b5483a",
    "rose": "#8c3b5d",
    "fog": "#f3f5f7",
    "mist": "#d9e1e8",
    "slate": "#6b7786",
    "white": "#ffffff",
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
            "grid.color": "#d7dce2",
            "grid.linewidth": 0.6,
            "grid.alpha": 0.75,
            "legend.frameon": False,
        }
    )


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"{stem}.{ext}", dpi=600, bbox_inches="tight")
    plt.close(fig)


def _objective_tuple(payload: dict[str, object]) -> tuple[int, int, int]:
    objective = payload["objective"]
    assert isinstance(objective, dict)
    return (
        int(objective["support_size"]),
        int(objective["l1"]),
        int(objective["max_abs"]),
    )


def _score(payload: dict[str, object]) -> int:
    objective = payload["objective"]
    assert isinstance(objective, dict)
    return int(objective["score"])


def make_retained_library_figure() -> None:
    atlas = load_json(RESULTS_DIR / "analysis" / "composite_packet_locality_atlas.json")
    retained = load_json(RESULTS_DIR / "analysis" / "composite_packet_retained_library.json")
    assert isinstance(atlas, dict)
    assert isinstance(retained, dict)

    seed_objective = atlas["frontier"]["seed_objective"]
    cutoff = float(atlas["frontier"]["low_splash_cutoff"])
    family_summaries = atlas["frontier"]["family_summaries"]
    family_by_name = {entry["family"]: entry for entry in family_summaries}
    labels = [
        "One-packet",
        "Pair",
        "Balanced-4",
        "Boundary quad",
        "S-bound pair",
        "Q-bound pair",
        "Retained",
    ]
    medians = [
        float(atlas["frontier"]["one_packet_summary"]["changed_lag_summary"]["median"]),
        float(family_by_name["pair"]["changed_lag_summary"]["median"]),
        float(family_by_name["balanced4"]["changed_lag_summary"]["median"]),
        float(family_by_name["boundary_quad"]["changed_lag_summary"]["median"]),
        float(family_by_name["s_boundary_pair"]["changed_lag_summary"]["median"]),
        float(family_by_name["q_boundary_pair"]["changed_lag_summary"]["median"]),
        float(retained["changed_lag_summary"]["median"]),
    ]
    count_labels = [
        "334",
        f"{family_by_name['pair']['low_splash_count']}/{family_by_name['pair']['candidate_count']}",
        f"{family_by_name['balanced4']['low_splash_count']}/{family_by_name['balanced4']['candidate_count']}",
        f"{family_by_name['boundary_quad']['low_splash_count']}/{family_by_name['boundary_quad']['candidate_count']}",
        f"{family_by_name['s_boundary_pair']['low_splash_count']}/{family_by_name['s_boundary_pair']['candidate_count']}",
        f"{family_by_name['q_boundary_pair']['low_splash_count']}/{family_by_name['q_boundary_pair']['candidate_count']}",
        f"{len(retained['records'])}",
    ]

    support_palette = {
        0: PALETTE["teal"],
        1: PALETTE["gold"],
        2: PALETTE["orange"],
        3: PALETTE["brick"],
    }
    records = retained["records"]
    x = np.asarray([int(record["changed_lag_count"]) for record in records], dtype=float)
    l1_gain = np.asarray([int(seed_objective["l1"]) - int(record["objective"]["l1"]) for record in records], dtype=float)
    support_flux = np.asarray(
        [int(record["objective"]["support_size"]) - int(seed_objective["support_size"]) for record in records],
        dtype=int,
    )
    max_gain = np.asarray([int(seed_objective["max_abs"]) - int(record["objective"]["max_abs"]) for record in records], dtype=float)
    colors = [support_palette.get(int(value), PALETTE["rose"]) for value in support_flux.tolist()]
    sizes = 70.0 + 6.0 * np.maximum(max_gain, 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.4), gridspec_kw={"width_ratios": [1.15, 1.0]})

    ax = axes[0]
    x_pos = np.arange(len(labels))
    bar_colors = [
        PALETTE["navy"],
        PALETTE["navy"],
        PALETTE["teal"],
        PALETTE["teal"],
        PALETTE["green"],
        PALETTE["green"],
        PALETTE["rose"],
    ]
    bars = ax.bar(x_pos, medians, color=bar_colors, edgecolor=PALETTE["white"], linewidth=0.8)
    ax.axhline(cutoff, color=PALETTE["brick"], linewidth=1.2, linestyle="--", label=f"Low-splash cutoff = {cutoff:.1f}")
    ax.set_xticks(x_pos, labels, rotation=20, ha="right")
    ax.set_ylabel("Median changed-lag count")
    ax.set_title("Actuator redesign cuts the lag footprint before it cuts the score")
    ax.set_ylim(0, 60)
    for bar, count_text, median in zip(bars, count_labels, medians):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            float(median) + 1.4,
            count_text,
            ha="center",
            va="bottom",
            fontsize=8,
            color=PALETTE["ink"],
        )
    ax.text(
        0.01,
        0.98,
        "Labels above bars show retained/total\ncandidates for composite families.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["fog"], "edgecolor": PALETTE["mist"]},
    )
    ax.legend(loc="upper right")

    ax = axes[1]
    ax.scatter(x, l1_gain, s=sizes, c=colors, edgecolors=PALETTE["ink"], linewidths=0.6, zorder=3)
    ax.axhline(0.0, color=PALETTE["slate"], linewidth=1.0)
    ax.axvline(cutoff, color=PALETTE["brick"], linewidth=1.0, linestyle="--")
    for idx, record in enumerate(records):
        if idx not in {0, 3, 7, 8}:
            continue
        ax.text(
            x[idx] + 0.25,
            l1_gain[idx] + 4.0,
            f"A{idx}",
            fontsize=9,
            color=PALETTE["ink"],
            weight="bold",
        )
    ax.set_xlabel("Changed-lag count")
    ax.set_ylabel(r"$\Delta \ell_1 = 2880 - \ell_1(\mathrm{action})$")
    ax.set_title("No retained single actuator improves lexicographically")
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-20, 260)
    legend_lines = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["teal"], markeredgecolor=PALETTE["ink"], markersize=7, label=r"$\Delta$ support $= 0$"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["gold"], markeredgecolor=PALETTE["ink"], markersize=7, label=r"$\Delta$ support $= +1$"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["orange"], markeredgecolor=PALETTE["ink"], markersize=7, label=r"$\Delta$ support $= +2$"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["brick"], markeredgecolor=PALETTE["ink"], markersize=7, label=r"$\Delta$ support $\geq +3$"),
    ]
    ax.legend(handles=legend_lines, loc="upper left", fontsize=8)
    ax.text(
        0.98,
        0.03,
        "A0 = neutral pair\nA3, A7 = the two actions in the\nfirst improving depth-2 cone",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["fog"], "edgecolor": PALETTE["mist"]},
    )

    fig.suptitle("Retained composite library on the canonical order-668 frontier seed", y=1.02, fontsize=13)
    save_figure(fig, "fig07_retained_library")


def _draw_state_box(ax: plt.Axes, center: tuple[float, float], title: str, body: str, face: str) -> None:
    width = 0.23
    height = 0.36
    x0 = center[0] - width / 2.0
    y0 = center[1] - height / 2.0
    patch = FancyBboxPatch(
        (x0, y0),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.1,
        edgecolor=PALETTE["slate"],
        facecolor=face,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(center[0], center[1] + 0.10, title, ha="center", va="center", fontsize=11, weight="bold")
    ax.text(center[0], center[1] - 0.03, body, ha="center", va="center", fontsize=8.8, linespacing=1.35)


def make_barrier_and_transfer_figure() -> None:
    barrier = load_json(RESULTS_DIR / "verification" / "radius_limited_locality_barrier.json")
    retained = load_json(RESULTS_DIR / "analysis" / "composite_packet_retained_library.json")
    hypergraph = load_json(RESULTS_DIR / "experiments" / "order_668_hypergraph_ca" / "summary.json")
    orbit = load_json(RESULTS_DIR / "experiments" / "order_668_orbit_ca" / "summary.json")
    population = load_json(RESULTS_DIR / "experiments" / "order_668_population_ca" / "summary.json")
    assert isinstance(barrier, dict)
    assert isinstance(retained, dict)
    assert isinstance(hypergraph, dict)
    assert isinstance(orbit, dict)
    assert isinstance(population, dict)

    counterexample = barrier["radius_limited_counterexample"]["first_counterexample"]
    record3 = retained["records"][3]
    middle_objective = record3["objective"]
    start_objective = barrier["canonical_seed_objective"]
    end_objective = counterexample["end_state"]["objective"]

    state_labels = [
        "canonical_frontier",
        "barrier_ladder_01",
        "barrier_ladder_02",
        "barrier_ladder_03",
        "barrier_ladder_04",
        "barrier_ladder_05",
    ]
    state_titles = ["Seed", "B1", "B2", "B3", "B4", "B5"]
    method_labels = [
        ("raw_coordinate_baseline", "Raw"),
        ("scorer_only", "Scorer"),
        ("hypergraph_causal_cone_ca", "Hypergraph"),
        ("orbit_quotient_ca", "Orbit"),
        ("population_median", "Pop med"),
        ("zero_coupling_median", "Zero med"),
    ]

    def state_payload_from_population(label: str, key: str) -> dict[str, object]:
        payload = population["results"][label]
        if key == "population_median":
            return {"objective": payload["population_median"]}
        if key == "zero_coupling_median":
            return {"objective": payload["zero_coupling_median"]}
        raise KeyError(key)

    improvement = np.zeros((len(method_labels), len(state_labels)), dtype=float)
    annotations: list[list[str]] = []
    for method_index, (method_key, _) in enumerate(method_labels):
        row: list[str] = []
        for state_index, label in enumerate(state_labels):
            if method_key in {"population_median", "zero_coupling_median"}:
                best_payload = state_payload_from_population(label, method_key)
                start_payload = population["results"][label]["population_runs"][0]["start_state"]
            elif method_key == "hypergraph_causal_cone_ca":
                best_payload = hypergraph["method_results"][label][method_key]["best_state"]
                start_payload = hypergraph["method_results"][label][method_key]["start_state"]
            else:
                best_payload = orbit["runs"][label][method_key]["best_state"]
                start_payload = orbit["runs"][label][method_key]["start_state"]
            delta = _score(start_payload) - _score(best_payload)
            improvement[method_index, state_index] = float(delta)
            if delta <= 0:
                row.append("=")
            else:
                objective = best_payload["objective"]
                row.append(
                    f"{int(objective['support_size'])}/{int(objective['l1'])}/{int(objective['max_abs'])}"
                )
        annotations.append(row)

    cmap = LinearSegmentedColormap.from_list(
        "frontier_gain",
        [PALETTE["fog"], "#d9ecf2", "#8bc6d4", PALETTE["teal"], PALETTE["navy"]],
    )

    fig = plt.figure(figsize=(13.2, 6.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.35], wspace=0.28)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_axis_off()
    _draw_state_box(
        ax,
        (0.18, 0.56),
        "Canonical seed",
        "state 0\n13 / 2880 / 512",
        PALETTE["fog"],
    )
    _draw_state_box(
        ax,
        (0.50, 0.56),
        "After A3",
        "A3 = [q53, q136]\nstate 3\n14 / 2820 / 496",
        "#fff3d8",
    )
    _draw_state_box(
        ax,
        (0.82, 0.56),
        "After cone [3,7]",
        "A7 = [q29, s29, q114, s114]\nstate 53\n13 / 2744 / 480",
        "#dff0eb",
    )
    arrows = [
        ((0.29, 0.56), (0.39, 0.56), "apply A3"),
        ((0.61, 0.56), (0.71, 0.56), "apply A7"),
    ]
    for start, end, label in arrows:
        arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15, linewidth=1.2, color=PALETTE["slate"])
        ax.add_patch(arrow)
        ax.text((start[0] + end[0]) / 2.0, 0.66, label, ha="center", va="bottom", fontsize=9.2)
    ax.text(
        0.50,
        0.18,
        "The barrier certificate checks 55,954 depth-1 single actuators.\n"
        "No depth-1 actuator improves the seed; only the retained radius-1,\n"
        "depth-2 cone class escapes, and the first certified edge is [3,7].\n"
        "The same six-packet end state recurs in the\n"
        "hypergraph, lattice-gas, and orbit branches.",
        ha="center",
        va="center",
        fontsize=9.2,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": PALETTE["fog"], "edgecolor": PALETTE["mist"]},
    )
    ax.set_title("Certified counterexample path", pad=12)

    ax = fig.add_subplot(gs[0, 1])
    im = ax.imshow(improvement, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(len(state_labels)), state_titles)
    ax.set_yticks(np.arange(len(method_labels)), [label for _, label in method_labels])
    ax.set_title("Best objective reached on the frontier perturbation ladder")
    ax.set_xlabel("Frontier state")
    ax.set_ylabel("Method")
    for i in range(len(method_labels)):
        for j in range(len(state_labels)):
            text_color = PALETTE["white"] if improvement[i, j] > 600_000 else PALETTE["ink"]
            ax.text(j, i, annotations[i][j], ha="center", va="center", fontsize=7.6, color=text_color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r"Score improvement relative to start state ($\Delta$ score)")
    ax.text(
        0.01,
        -0.22,
        "Cells show the best support/l1/max triple when a method improves; '=' means no change from the start state.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
    )

    fig.suptitle("Barrier certificate and post-H1 retained-basis outcomes", y=1.02, fontsize=13)
    save_figure(fig, "fig08_barrier_and_transfer")


def _wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0:
        return (0.0, 0.0)
    phat = float(k) / float(n)
    denom = 1.0 + z * z / float(n)
    centre = (phat + z * z / (2.0 * float(n))) / denom
    radius = (z / denom) * np.sqrt(phat * (1.0 - phat) / float(n) + z * z / (4.0 * float(n) * float(n)))
    return (float(centre - radius), float(centre + radius))


def make_population_phase_figure() -> None:
    phase_map = load_json(RESULTS_DIR / "analysis" / "frontier_population_phase_map.json")
    population = load_json(RESULTS_DIR / "experiments" / "order_668_population_ca" / "summary.json")
    assert isinstance(phase_map, dict)
    assert isinstance(population, dict)

    couplings = sorted({float(cell["coupling_strength"]) for cell in phase_map["cells"]})
    thresholds = sorted({float(cell["contraction_threshold"]) for cell in phase_map["cells"]})
    grid = np.zeros((len(thresholds), len(couplings)), dtype=float)
    for cell in phase_map["cells"]:
        i = thresholds.index(float(cell["contraction_threshold"]))
        j = couplings.index(float(cell["coupling_strength"]))
        grid[i, j] = float(cell["contraction_fraction"])

    canonical = population["results"]["canonical_frontier"]
    runs = {
        "Population": canonical["population_runs"],
        "Zero-coupling": canonical["zero_coupling_runs"],
    }
    metrics = [
        ("Improve", lambda run: int(run["best_state"]["objective"]["score"]) < int(run["start_state"]["objective"]["score"])),
        ("Contract", lambda run: any(step["phase"] == "contraction" for step in run["trace"])),
    ]

    fig = plt.figure(figsize=(11.8, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.30)

    ax = fig.add_subplot(gs[0, 0])
    cmap = LinearSegmentedColormap.from_list("phase", [PALETTE["fog"], "#cedde6", PALETTE["teal"], PALETTE["navy"]])
    im = ax.imshow(grid, cmap=cmap, vmin=0.0, vmax=0.4, aspect="auto")
    ax.set_xticks(np.arange(len(couplings)), [f"{value:.2f}" for value in couplings])
    ax.set_yticks(np.arange(len(thresholds)), [f"{value:.2f}" for value in thresholds])
    ax.set_xlabel("Coupling strength")
    ax.set_ylabel("Contraction threshold")
    ax.set_title("Population phase map stays in diffusion")
    for i in range(len(thresholds)):
        for j in range(len(couplings)):
            ax.text(j, i, f"{grid[i, j]:.3f}", ha="center", va="center", fontsize=9, color=PALETTE["ink"])
    selected = phase_map["selected_operating_point"]
    ax.scatter(
        couplings.index(float(selected["coupling_strength"])),
        thresholds.index(float(selected["contraction_threshold"])),
        s=140,
        marker="s",
        facecolors="none",
        edgecolors=PALETTE["brick"],
        linewidths=1.8,
    )
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Contraction fraction")

    ax = fig.add_subplot(gs[0, 1])
    x = np.arange(len(metrics), dtype=float)
    offsets = [-0.10, 0.10]
    method_colors = [PALETTE["rose"], PALETTE["slate"]]
    for offset, (method_name, method_runs), color in zip(offsets, runs.items(), method_colors):
        values = []
        lower = []
        upper = []
        for _, predicate in metrics:
            successes = sum(1 for run in method_runs if predicate(run))
            total = len(method_runs)
            rate = successes / float(total)
            lo, hi = _wilson_interval(successes, total)
            values.append(rate)
            lower.append(rate - lo)
            upper.append(hi - rate)
        ax.errorbar(
            x + offset,
            values,
            yerr=[lower, upper],
            fmt="o",
            capsize=4,
            color=color,
            markersize=7,
            linewidth=1.4,
            label=method_name,
        )
    ax.set_xticks(x, [label for label, _ in metrics])
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Rate with Wilson 95% interval")
    ax.set_title("Canonical-seed stochastic outcomes are identical")
    ax.axhline(0.5, color=PALETTE["mist"], linewidth=1.0, linestyle="--")
    ax.legend(loc="upper right")
    ax.text(
        0.03,
        0.06,
        "Both methods improve 3/5 frontier seeds and contract 3/5 times.\n"
        "Population strict wins over zero-coupling: 0/5 canonical, 0/5 ladder states.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.6,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["fog"], "edgecolor": PALETTE["mist"]},
    )

    fig.suptitle("Population self-stabilization does not separate from zero-coupling", y=1.02, fontsize=13)
    save_figure(fig, "fig09_population_phase")


def main() -> int:
    configure_style()
    make_retained_library_figure()
    make_barrier_and_transfer_figure()
    make_population_phase_figure()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
