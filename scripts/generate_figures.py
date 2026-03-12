#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
import numpy as np
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.slopes import floor_value, get_slope


FIG_DIR = ROOT / "figures"
FULL_PANEL = json.loads((ROOT / "results" / "experiments" / "full_panel_results.json").read_text())
METRICS = json.loads((ROOT / "results" / "experiments" / "metrics_full_panel.json").read_text())
ABLATION = json.loads((ROOT / "results" / "experiments" / "claim_sensitive_ablation.json").read_text())

STATUS_COLORS = {
    "exact_recurrence": "#1f7a72",
    "sparse_subsequence_leak": "#d39b34",
    "prefix_fit": "#db7b5f",
    "selector_shadow_failure": "#9a3b43",
    "no_candidate": "#7f8c99",
    "waived": "#d7dde5",
}

STATUS_TO_INT = {
    "waived": 0,
    "no_candidate": 1,
    "selector_shadow_failure": 2,
    "prefix_fit": 3,
    "sparse_subsequence_leak": 4,
    "exact_recurrence": 5,
}

INT_TO_STATUS = {value: key for key, value in STATUS_TO_INT.items()}

SLOPE_ORDER = [
    "rational_2",
    "rational_3_over_2",
    "rational_5_over_3",
    "half",
    "phi_minus_1",
    "phi",
    "sqrt2",
    "one_plus_sqrt2",
    "plastic",
    "salem_quartic",
    "e",
]

SLOPE_LABELS = {
    "rational_2": r"$2$",
    "rational_3_over_2": r"$3/2$",
    "rational_5_over_3": r"$5/3$",
    "half": r"$1/2$",
    "phi_minus_1": r"$\varphi-1$",
    "phi": r"$\varphi$",
    "sqrt2": r"$\sqrt{2}$",
    "one_plus_sqrt2": r"$1+\sqrt{2}$",
    "plastic": "plastic",
    "salem_quartic": "Salem",
    "e": r"$e$",
}

SELECTOR_ORDER = [
    "ap_1_0",
    "ap_2_0",
    "ap_3_1",
    "ap_5_2",
    "union_mod3_01",
    "union_mod5_02",
    "union_mod6_013",
    "fib_indices",
    "pell_indices",
    "padovan_indices",
    "ost_single_nonzero_digit",
    "ost_suffix_01",
    "ost_suffix_001",
    "quadratic_convergent_even",
    "beta_endpoint_suffix_10",
]

SELECTOR_LABELS = {
    "ap_1_0": "AP(1,0)",
    "ap_2_0": "AP(2,0)",
    "ap_3_1": "AP(3,1)",
    "ap_5_2": "AP(5,2)",
    "union_mod3_01": "U3{0,1}",
    "union_mod5_02": "U5{0,2}",
    "union_mod6_013": "U6{0,1,3}",
    "fib_indices": "Fib",
    "pell_indices": "Pell",
    "padovan_indices": "Padovan",
    "ost_single_nonzero_digit": "O1",
    "ost_suffix_01": "O01",
    "ost_suffix_001": "O001",
    "quadratic_convergent_even": r"$q_{2k}$",
    "beta_endpoint_suffix_10": "beta10",
}


def setup_style() -> None:
    sns.set_theme(style="whitegrid", context="paper", font="DejaVu Serif")
    mpl.rcParams.update(
        {
            "figure.facecolor": "#fbfaf7",
            "axes.facecolor": "#fbfaf7",
            "savefig.facecolor": "#fbfaf7",
            "axes.edgecolor": "#556270",
            "axes.labelcolor": "#24313f",
            "xtick.color": "#24313f",
            "ytick.color": "#24313f",
            "grid.color": "#d7dde3",
            "font.family": "DejaVu Serif",
            "font.size": 10.5,
            "axes.titlesize": 12,
            "axes.titleweight": "semibold",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 8.5,
            "figure.titlesize": 14,
            "axes.titlepad": 8,
            "axes.grid.axis": "y",
            "grid.linewidth": 0.7,
        }
    )


def save_figure(fig: Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(FIG_DIR / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def classification_matrix() -> np.ndarray:
    rows = FULL_PANEL["cases"]
    lookup = {}
    for row in rows:
        key = (row.get("slope_id"), row.get("selector_id"))
        if row.get("status") == "waived":
            lookup[key] = STATUS_TO_INT["waived"]
        else:
            lookup[key] = STATUS_TO_INT[row["shadow_probe"]["classification"]]
    matrix = np.zeros((len(SLOPE_ORDER), len(SELECTOR_ORDER)), dtype=int)
    for i, slope_id in enumerate(SLOPE_ORDER):
        for j, selector_id in enumerate(SELECTOR_ORDER):
            matrix[i, j] = lookup[(slope_id, selector_id)]
    return matrix


def fig1_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(13, 5.8))
    ax.set_axis_off()

    boxes = {
        "problem": (0.03, 0.28, 0.18, 0.42, "Problem\n$\\lfloor n r\\rfloor$ contains an\nordered recurrence subsequence?", "#d9e8e3"),
        "lock": (0.28, 0.58, 0.19, 0.22, "Definition Lock\nordered values, integer coefficients,\nstructured selector families", "#e8e3d9"),
        "theorem": (0.54, 0.58, 0.19, 0.22, "Theorem Lane\neventually periodic gaps\n$\\Longleftrightarrow$ rational $r$", "#d7efe7"),
        "empirical": (0.54, 0.20, 0.19, 0.22, "Sparse Lane\nexact certificates vs long holdouts\nquadratic selectors only", "#f3e4d8"),
        "screen": (0.28, 0.20, 0.19, 0.22, "Benchmark Screen\nexact recurrence fit + holdout\nmodular-shadow replay", "#dce7f2"),
        "claims": (0.80, 0.35, 0.17, 0.30, "Released Claims\n(1) proved periodic-gap theorem\n(2) four certified quadratic examples\n(3) empirical sparse holdouts", "#e8ddd9"),
    }
    for x, y, w, h, label, color in boxes.values():
        patch = FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", fc=color, ec="#36454f", lw=1.4
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", color="#23303f", linespacing=1.5)

    arrows = [
        ((0.21, 0.49), (0.28, 0.68)),
        ((0.21, 0.49), (0.28, 0.31)),
        ((0.47, 0.69), (0.54, 0.69)),
        ((0.47, 0.31), (0.54, 0.31)),
        ((0.73, 0.69), (0.80, 0.52)),
        ((0.73, 0.31), (0.80, 0.48)),
    ]
    for start, end in arrows:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, lw=1.6, color="#3d556e"))

    ax.text(0.03, 0.90, "Research pipeline and claim hierarchy", fontsize=18, fontweight="bold", color="#24313f")
    ax.text(
        0.03,
        0.84,
        "The paper separates a proof-complete periodic-gap obstruction theorem from a sparse quadratic example lane that remains partly empirical.",
        fontsize=11,
        color="#4a5a6a",
    )
    save_figure(fig, "fig1_pipeline")


def fig2_periodic_gap_decomposition() -> None:
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={"height_ratios": [1.0, 1.0]})
    indices = [1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18]
    colors = ["#1f7a72", "#c98f1c", "#7a5ea8"]
    groups = {0: [], 1: [], 2: []}
    for idx, value in enumerate(indices):
        groups[idx % 3].append(value)

    ax_top.set_title("Eventually periodic gaps decompose into arithmetic residue lanes")
    ax_top.hlines(0, 0, 19, color="#607182", lw=1.4)
    for n in range(1, 19):
        ax_top.vlines(n, -0.06, 0.06, color="#d0d6dd", lw=0.8)
    for idx, value in enumerate(indices):
        ax_top.scatter(value, 0, s=80, color=colors[idx % 3], zorder=3, edgecolors="#24313f", linewidths=0.6)
    ax_top.text(0.2, 0.18, "selector = residues {0,1,3} mod 6", color="#324454")
    ax_top.text(0.2, -0.28, r"gap word repeats as $(2,1,2)$", color="#324454")
    ax_top.set_xlim(0, 19)
    ax_top.set_ylim(-0.4, 0.35)
    ax_top.set_yticks([])
    ax_top.set_xlabel("ambient index $n$")

    y_levels = [2, 1, 0]
    for group_id, y_level in zip(sorted(groups), y_levels):
        values = groups[group_id]
        ax_bottom.plot(values, [y_level] * len(values), marker="o", color=colors[group_id], lw=2.4)
        for x in values:
            ax_bottom.text(x, y_level + 0.16, str(x), ha="center", va="bottom", fontsize=9, color="#24313f")
    ax_bottom.set_xlim(0, 19)
    ax_bottom.set_ylim(-0.4, 2.6)
    ax_bottom.set_yticks(y_levels, [r"$n_{3t+2}=6t+4$", r"$n_{3t+1}=6t+3$", r"$n_{3t}=6t+1$"])
    ax_bottom.set_xlabel("ambient index $n$")
    ax_bottom.set_title("Each phase class becomes a genuine arithmetic progression")
    ax_bottom.grid(axis="x", linestyle=":", alpha=0.6)

    save_figure(fig, "fig2_periodic_gap_decomposition")


def fig3_difference_sequences() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.8), sharex=True)

    k = np.arange(1, 33)
    rational_values = [floor_value("rational_3_over_2", int(n)) for n in k]
    irrational_values = [floor_value("phi", int(2 * n)) for n in k]
    rational_diff = np.diff(rational_values)
    irrational_diff = np.diff(irrational_values)

    axes[0].step(k[1:], rational_diff, where="mid", color="#1f7a72", lw=2.2)
    axes[0].scatter(k[1:], rational_diff, color="#1f7a72", s=24)
    axes[0].set_ylabel(r"$\Delta b_k$")
    axes[0].set_title(r"Rational slope: $r=3/2$, arithmetic selector $n_k=k$ gives periodic first differences")
    axes[0].grid(True, linestyle=":", alpha=0.5)
    axes[0].text(2, 2.18, "period-2 shadow", color="#1f7a72")

    axes[1].step(k[1:], irrational_diff, where="mid", color="#9a3b43", lw=2.2)
    axes[1].scatter(k[1:], irrational_diff, color="#9a3b43", s=24)
    axes[1].set_ylabel(r"$\Delta b_k$")
    axes[1].set_xlabel(r"subsequence index $k$")
    axes[1].set_title(r"Irrational slope: $r=\varphi$, arithmetic selector $n_k=2k$ yields an aperiodic mechanical two-letter difference word")
    axes[1].grid(True, linestyle=":", alpha=0.5)
    axes[1].text(2, 4.2, "non-eventually periodic", color="#9a3b43")
    save_figure(fig, "fig3_difference_sequences")


def fig4_full_panel_heatmap() -> None:
    matrix = classification_matrix()
    cmap = mcolors.ListedColormap([STATUS_COLORS[INT_TO_STATUS[idx]] for idx in range(6)])
    norm = mcolors.BoundaryNorm(np.arange(-0.5, 6.5, 1.0), cmap.N)

    fig, ax = plt.subplots(figsize=(13.2, 7.1))
    fig.subplots_adjust(left=0.11, right=0.98, top=0.88, bottom=0.30)
    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(len(SELECTOR_ORDER)), [SELECTOR_LABELS[key] for key in SELECTOR_ORDER], rotation=35, ha="right")
    ax.set_yticks(np.arange(len(SLOPE_ORDER)), [SLOPE_LABELS[key] for key in SLOPE_ORDER])
    ax.set_title("Full panel classifications", loc="left")
    ax.set_xlabel("selector template")
    ax.set_ylabel("slope")

    for i in range(matrix.shape[0] + 1):
        ax.axhline(i - 0.5, color="#fbfaf7", lw=0.8)
    for j in range(matrix.shape[1] + 1):
        ax.axvline(j - 0.5, color="#fbfaf7", lw=0.8)

    for boundary in [3.5, 6.5, 9.5, 13.5]:
        ax.axvline(boundary, color="#fbfaf7", lw=2.2)

    family_centers = [
        (1.5, "AP"),
        (5.0, "FUAP"),
        (8.0, "LR"),
        (11.5, "Ostrowski"),
        (14.0, "beta"),
    ]
    for center, label in family_centers:
        x_fraction = (center + 0.5) / len(SELECTOR_ORDER)
        ax.text(x_fraction, -0.18, label, transform=ax.transAxes, ha="center", va="top", color="#4a5a6a", fontsize=8.5)

    legend_handles = [
        Patch(color=STATUS_COLORS[name], label=label)
        for name, label in [
            ("exact_recurrence", "exact"),
            ("sparse_subsequence_leak", "sparse leak"),
            ("prefix_fit", "prefix fit"),
            ("selector_shadow_failure", "shadow fail"),
            ("no_candidate", "none"),
            ("waived", "waived"),
        ]
    ]
    ax.legend(handles=legend_handles, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.28), frameon=False)
    save_figure(fig, "fig4_full_panel_heatmap")


def fig5_outcome_breakdown() -> None:
    rows = [row for row in FULL_PANEL["cases"] if row.get("status") == "executed"]
    by_selector_family = Counter()
    for row in rows:
        if row["shadow_probe"]["classification"] == "exact_recurrence":
            by_selector_family[row["selector_family"]] += 1

    family_order = ["arithmetic_progression", "finite_union_of_arithmetic_progressions", "linear_recursive"]
    family_labels = ["AP", "FUAP", "sparse"]
    family_values = [by_selector_family.get(key, 0) for key in family_order]

    by_slope_family = defaultdict(Counter)
    for row in rows:
        slope_kind = get_slope(row["slope_id"]).kind
        if slope_kind.startswith("rational"):
            bucket = "rational"
        elif "quadratic" in slope_kind:
            bucket = "quadratic"
        else:
            bucket = "higher-degree / control"
        by_slope_family[bucket][row["shadow_probe"]["classification"]] += 1

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(13.5, 5.5), gridspec_kw={"width_ratios": [0.9, 1.4]})

    bars = ax_left.bar(family_labels, family_values, color=["#4b8c7f", "#7aa999", "#d39b34"], width=0.65)
    for bar, value in zip(bars, family_values):
        ax_left.text(bar.get_x() + bar.get_width() / 2, value + 0.6, str(value), ha="center", color="#24313f")
    ax_left.set_title("Exact-certified cases by selector family")
    ax_left.set_ylabel("count")
    ax_left.set_ylim(0, max(family_values) + 6)
    ax_left.grid(axis="y", linestyle=":", alpha=0.5)
    ax_left.text(0.03, 0.94, "28 degenerate rational certificates\n4 nondegenerate quadratic certificates", transform=ax_left.transAxes, va="top", color="#4a5a6a")

    slope_groups = ["rational", "quadratic", "higher-degree / control"]
    stack_order = ["exact_recurrence", "sparse_subsequence_leak", "prefix_fit", "selector_shadow_failure", "no_candidate"]
    bottoms = np.zeros(len(slope_groups))
    for status in stack_order:
        values = np.array([by_slope_family[group].get(status, 0) for group in slope_groups])
        ax_right.bar(slope_groups, values, bottom=bottoms, color=STATUS_COLORS[status], label=status.replace("_", " "))
        bottoms += values
    ax_right.set_title("Outcome mix by slope family")
    ax_right.set_ylabel("executed cases")
    ax_right.grid(axis="y", linestyle=":", alpha=0.5)
    ax_right.legend(ncol=2, frameon=False, loc="upper right")

    save_figure(fig, "fig5_outcome_breakdown")


def fig6_claim_sensitive_ablations() -> None:
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(13.5, 6.9), gridspec_kw={"width_ratios": [1.0, 1.18]})
    fig.subplots_adjust(left=0.08, right=0.98, top=0.80, bottom=0.24, wspace=0.34)
    fig.suptitle("Claim-sensitive ablations", x=0.08, y=0.95, ha="left", fontsize=14, fontweight="semibold")
    fig.text(
        0.08,
        0.89,
        "Higher-order fitting creates false candidates; longer holdouts keep only the certified quadratic identities and persistent empirical leaks.",
        color="#4a5a6a",
        fontsize=9.2,
    )

    order_keys = ["d_leq_4", "d_leq_6", "d_leq_8"]
    statuses = ["exact_recurrence", "sparse_subsequence_leak", "prefix_fit", "selector_shadow_failure", "no_candidate"]
    x = np.arange(len(order_keys))
    bottoms = np.zeros(len(order_keys))
    for status in statuses:
        values = np.array([ABLATION["order_cap_ablation"][key]["classification_counts"][status] for key in order_keys])
        ax_left.bar(x, values, bottom=bottoms, color=STATUS_COLORS[status], width=0.72, label=status.replace("_", " "))
        bottoms += values
    ax_left.set_xticks(x, [r"$d\leq 4$", r"$d\leq 6$", r"$d\leq 8$"])
    ax_left.set_ylabel("executed cases")
    ax_left.set_title("Order-cap sensitivity")
    ax_left.grid(axis="y", linestyle=":", alpha=0.5)
    for idx, key in enumerate(order_keys[1:], start=1):
        flips = ABLATION["order_cap_ablation"][key]["flip_count_vs_d_leq_4"]
        ax_left.text(idx, 143.5, f"{flips} flips", ha="center", color="#24313f", fontsize=8.5)

    case_order = [
        "phi::quadratic_convergent_even",
        "phi_minus_1::quadratic_convergent_even",
        "sqrt2::quadratic_convergent_even",
        "one_plus_sqrt2::quadratic_convergent_even",
        "phi::fib_indices",
        "phi_minus_1::fib_indices",
        "sqrt2::pell_indices",
        "one_plus_sqrt2::pell_indices",
        "salem_quartic::ost_suffix_001",
        "plastic::ap_1_0",
        "plastic::union_mod3_01",
    ]
    case_labels = [
        r"$\varphi / q_{2k}$",
        r"$(\varphi-1)/q_{2k}$",
        r"$\sqrt{2} / q_{2k}$",
        r"$(1+\sqrt{2}) / q_{2k}$",
        r"$\varphi$/Fib",
        r"$(\varphi-1)$/Fib",
        r"$\sqrt{2}$/Pell",
        r"$(1+\sqrt{2})$/Pell",
        "Salem/O001",
        "plastic/AP",
        "plastic/U3",
    ]
    lengths = [str(length) for length in ABLATION.get("holdout_lengths", [20, 40, 80, 160, 320])]
    heat = np.zeros((len(case_order), len(lengths)), dtype=int)
    for i, case_key in enumerate(case_order):
        for j, length in enumerate(lengths):
            heat[i, j] = STATUS_TO_INT[ABLATION["holdout_length_ablation"][case_key][length]["classification"]]
    cmap = mcolors.ListedColormap([STATUS_COLORS[INT_TO_STATUS[idx]] for idx in range(6)])
    norm = mcolors.BoundaryNorm(np.arange(-0.5, 6.5, 1.0), cmap.N)
    ax_right.imshow(heat, cmap=cmap, norm=norm, aspect="auto")
    ax_right.set_xticks(np.arange(len(lengths)), lengths)
    ax_right.set_yticks(np.arange(len(case_order)), case_labels)
    ax_right.set_xlabel("exact holdout length")
    ax_right.set_title("Long-holdout stability")
    for i in range(heat.shape[0] + 1):
        ax_right.axhline(i - 0.5, color="#fbfaf7", lw=0.8)
    for j in range(heat.shape[1] + 1):
        ax_right.axvline(j - 0.5, color="#fbfaf7", lw=0.8)

    handles = [Patch(color=STATUS_COLORS[name], label=name.replace("_", " ")) for name in statuses]
    fig.legend(handles=handles, frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 0.06), ncol=3)
    save_figure(fig, "fig6_claim_sensitive_ablations")


def fig7_variant_matrix() -> None:
    slopes = ["phi", "phi_minus_1", "sqrt2", "one_plus_sqrt2", "plastic", "e"]
    variants = ["even", "odd", "even_shift1", "every_third"]
    heat = np.zeros((len(slopes), len(variants)), dtype=int)
    annotations = [["" for _ in variants] for _ in slopes]
    for i, slope_id in enumerate(slopes):
        for j, variant in enumerate(variants):
            entry = ABLATION["quadratic_variant_ablation"][slope_id][variant]
            heat[i, j] = STATUS_TO_INT[entry["classification"]]
            coeffs = entry.get("coefficients") or []
            if coeffs == [1, -3, 1]:
                annotations[i][j] = "3"
            elif coeffs == [1, -6, 1]:
                annotations[i][j] = "6"
            elif coeffs == [-1, 4, -4, 1]:
                annotations[i][j] = "4"
            elif coeffs == [-1, 7, -7, 1]:
                annotations[i][j] = "7"
            elif coeffs:
                annotations[i][j] = "fit"
    cmap = mcolors.ListedColormap([STATUS_COLORS[INT_TO_STATUS[idx]] for idx in range(6)])
    norm = mcolors.BoundaryNorm(np.arange(-0.5, 6.5, 1.0), cmap.N)

    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    fig.subplots_adjust(left=0.16, right=0.98, top=0.80, bottom=0.24)
    fig.suptitle("Convergent-selector variants", x=0.16, y=0.95, ha="left", fontsize=14, fontweight="semibold")
    fig.text(
        0.16,
        0.89,
        "Only the certified even-convergent lane keeps exact identities; nearby variants remain empirical checks.",
        color="#4a5a6a",
        fontsize=9.2,
    )
    ax.imshow(heat, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(len(variants)), ["even", "odd", "even +1", "every 3rd"])
    ax.set_yticks(np.arange(len(slopes)), [SLOPE_LABELS[key] for key in slopes])
    ax.set_title("Variant matrix")
    ax.set_xlabel("convergent template")
    ax.set_ylabel("slope")
    for i in range(len(slopes)):
        for j in range(len(variants)):
            ax.text(j, i, annotations[i][j], ha="center", va="center", color="#fbfaf7" if heat[i, j] <= 2 else "#24313f", fontsize=10)
    for i in range(heat.shape[0] + 1):
        ax.axhline(i - 0.5, color="#fbfaf7", lw=0.8)
    for j in range(heat.shape[1] + 1):
        ax.axvline(j - 0.5, color="#fbfaf7", lw=0.8)
    ax.text(0.0, -0.18, "Annotation = leading recurrence coefficient for the fitted low-order relation when a holdout survives.", transform=ax.transAxes, color="#4a5a6a", fontsize=8.7)
    save_figure(fig, "fig7_variant_matrix")


def fig8_prior_art_matrix() -> None:
    branches = [
        "Quadratic Beatty\ndecidability",
        "Symbolic LR /\nS-adic",
        "Generalised\npolynomials",
        "SML / zero-set\nrigidity",
        "Self-matching\nBeatty",
        "This paper",
    ]
    features = [
        "ordered\nvalue subseq.",
        "exact homogeneous\nrecurrence",
        "selector-class\nfreezing",
        "proof-complete\nperiodic-gap lane",
        "sparse quadratic\nexamples",
    ]
    matrix = np.array(
        [
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
    )
    cmap = mcolors.ListedColormap(["#e8edf2", "#33658a"])
    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(features)), features)
    ax.set_yticks(np.arange(len(branches)), branches)
    ax.set_title("Curated prior-art positioning used in the paper")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, "yes" if matrix[i, j] else "no", ha="center", va="center", color="#fbfaf7" if matrix[i, j] else "#24313f")
    for i in range(matrix.shape[0] + 1):
        ax.axhline(i - 0.5, color="#fbfaf7", lw=0.8)
    for j in range(matrix.shape[1] + 1):
        ax.axvline(j - 0.5, color="#fbfaf7", lw=0.8)
    save_figure(fig, "fig8_prior_art_matrix")


def main() -> None:
    setup_style()
    fig1_pipeline()
    fig2_periodic_gap_decomposition()
    fig3_difference_sequences()
    fig4_full_panel_heatmap()
    fig5_outcome_breakdown()
    fig6_claim_sensitive_ablations()
    fig7_variant_matrix()
    fig8_prior_art_matrix()
    print(FIG_DIR)


if __name__ == "__main__":
    main()
