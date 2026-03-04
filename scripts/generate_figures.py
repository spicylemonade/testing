#!/usr/bin/env python3
"""
Generate publication-grade figures for:
"Fast CSV Parsing via SIMD and Speculative Field Detection"

Outputs 4 figures (PNG + PDF each) into figures/.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
sns.set_style("whitegrid")
PALETTE = sns.color_palette("colorblind")
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,   # TrueType in PDF – editable text
    "ps.fonttype": 42,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT_DIR, exist_ok=True)


def save(fig, stem):
    """Save figure as both PNG (300 DPI) and vector PDF."""
    png = os.path.join(OUT_DIR, f"{stem}.png")
    pdf = os.path.join(OUT_DIR, f"{stem}.pdf")
    fig.savefig(png, dpi=300)
    fig.savefig(pdf)
    plt.close(fig)
    print(f"  {png}")
    print(f"  {pdf}")


# ===================================================================
# DATA
# ===================================================================
DATASETS = [
    "simple_uniform",
    "mixed_quoting",
    "embedded_newlines",
    "wide_table",
    "utf8_heavy",
]
DATASET_LABELS = [d.replace("_", "\n") for d in DATASETS]

PARSERS = ["python_csv", "pandas", "pyarrow", "scalar_baseline", "simd_parser"]
PARSER_LABELS = ["python\ncsv", "pandas", "pyarrow", "scalar\nbaseline", "SIMD\nparser"]

# Throughput matrix (MB/s) — rows = datasets, cols = parsers
# NaN means the parser failed on that dataset
THROUGHPUT = np.array([
    [  65.16, 103.07, 1243.52,  322.46, 1233.67],  # simple_uniform
    [  72.34,  43.43, 1443.14,  270.91, 1127.11],  # mixed_quoting
    [ 100.97,  60.10,     np.nan, 367.48, 3682.36],  # embedded_newlines
    [  85.78,  43.42,  768.94,  310.14, 1644.70],  # wide_table
    [  91.67,  30.25, 1398.55,  320.07, 1899.28],  # utf8_heavy
])

# Hardware counters (simple_uniform)
HW_METRICS = ["IPC", "Branch mispred\n/ 1K insn", "Bytes / cycle"]
HW_SCALAR = [0.9, 22.5, 0.11]
HW_SIMD   = [2.8,  1.2, 0.41]

# Thread scaling (Amdahl, parallel_frac=0.688)
THREADS = np.array([1, 2, 4, 8, 16])
SPEEDUP = np.array([1.0, 1.56, 2.27, 2.85, 3.10])
PARALLEL_FRAC = 0.688
BASE_THROUGHPUT_MBS = 1233.67  # simd_parser on simple_uniform

# Structural density vs throughput
DENSITY_DATASETS = [
    "embedded\nnewlines",
    "utf8\nheavy",
    "wide\ntable",
    "mixed\nquoting",
    "simple\nuniform",
]
BOUNDARIES_PER_BYTE = np.array([0.0136, 0.0437, 0.0644, 0.0732, 0.1250])
DENSITY_THROUGHPUT  = np.array([3682.36, 1899.28, 1644.70, 1127.11, 1233.67])

# Speculation accuracy
SPEC_DATASETS = DATASETS
BYTE_ACCURACY    = np.array([100.0, 76.16, 99.02, 99.99, 70.46])
ALLOC_REDUCTION  = np.array([10.0,   8.9,   8.0, 200.0,   6.9])


# ===================================================================
# Figure 1 — Throughput Comparison (grouped bar, log-y)
# ===================================================================
def fig_throughput():
    print("Figure 1: throughput_comparison")
    n_datasets = len(DATASETS)
    n_parsers  = len(PARSERS)
    x = np.arange(n_datasets)
    width = 0.15
    offsets = np.arange(n_parsers) - (n_parsers - 1) / 2

    fig, ax = plt.subplots(figsize=(10, 6))

    for j, (parser_label, color) in enumerate(zip(PARSER_LABELS, PALETTE)):
        vals = THROUGHPUT[:, j].copy()
        mask_nan = np.isnan(vals)
        vals_plot = np.where(mask_nan, 0, vals)
        bars = ax.bar(
            x + offsets[j] * width,
            vals_plot,
            width,
            label=parser_label.replace("\n", " "),
            color=color,
            edgecolor="white",
            linewidth=0.5,
            zorder=3,
        )
        # Annotate FAIL for NaN entries
        for i, is_nan in enumerate(mask_nan):
            if is_nan:
                ax.text(
                    x[i] + offsets[j] * width,
                    15,           # visible on log scale above y-min
                    "FAIL",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                    color="red",
                    rotation=90,
                    zorder=4,
                )

    ax.set_yscale("log")
    ax.set_ylabel("Throughput (MB/s)")
    ax.set_xlabel("Dataset")
    ax.set_xticks(x)
    ax.set_xticklabels(DATASET_LABELS)
    ax.set_title("CSV Parser Throughput Comparison Across Datasets", fontsize=13)
    ax.legend(loc="upper left", ncol=3, framealpha=0.9)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.set_ylim(bottom=10)
    ax.grid(axis="y", which="both", linewidth=0.4, alpha=0.6)

    save(fig, "throughput_comparison")


# ===================================================================
# Figure 2 — Hardware Comparison
# ===================================================================
def fig_hardware():
    print("Figure 2: hardware_comparison")
    n_metrics = len(HW_METRICS)
    x = np.arange(n_metrics)
    width = 0.30

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, HW_SCALAR, width,
                   label="scalar baseline", color=PALETTE[3], edgecolor="white", zorder=3)
    bars2 = ax.bar(x + width / 2, HW_SIMD, width,
                   label="SIMD parser", color=PALETTE[4], edgecolor="white", zorder=3)

    # Value labels
    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h * 1.03,
                    f"{h:g}", ha="center", va="bottom", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(HW_METRICS)
    ax.set_ylabel("Value")
    ax.set_title("Hardware Performance Counters: Scalar vs SIMD (simple_uniform)", fontsize=13)
    ax.legend()
    ax.set_ylim(0, max(max(HW_SCALAR), max(HW_SIMD)) * 1.25)
    ax.grid(axis="y", linewidth=0.4, alpha=0.6)

    save(fig, "hardware_comparison")


# ===================================================================
# Figure 3 — Scalability Analysis (two subplots)
# ===================================================================
def fig_scalability():
    print("Figure 3: scalability_analysis")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- (a) Thread scaling ---
    throughput_pred = BASE_THROUGHPUT_MBS * SPEEDUP
    ax1.plot(THREADS, throughput_pred, "o-", color=PALETTE[4],
             linewidth=2, markersize=7, label="Predicted (Amdahl)", zorder=3)

    # Continuous Amdahl curve
    t_cont = np.linspace(1, 16, 200)
    speedup_cont = 1.0 / ((1.0 - PARALLEL_FRAC) + PARALLEL_FRAC / t_cont)
    throughput_cont = BASE_THROUGHPUT_MBS * speedup_cont
    ax1.plot(t_cont, throughput_cont, "--", color=PALETTE[2],
             linewidth=1.2, alpha=0.7, label=f"Amdahl (p = {PARALLEL_FRAC})")

    # Linear scaling reference
    linear_throughput = BASE_THROUGHPUT_MBS * t_cont
    ax1.plot(t_cont, linear_throughput, ":", color="grey",
             linewidth=1, alpha=0.5, label="Linear scaling")

    ax1.set_xlabel("Threads")
    ax1.set_ylabel("Throughput (MB/s)")
    ax1.set_title("(a) Predicted Thread Scaling", fontsize=12)
    ax1.legend(fontsize=9)
    ax1.set_xticks(THREADS)
    ax1.set_xlim(0.5, 17)
    ax1.grid(linewidth=0.4, alpha=0.6)

    # --- (b) Structural density vs throughput ---
    ax2.scatter(BOUNDARIES_PER_BYTE, DENSITY_THROUGHPUT,
                s=80, color=PALETTE[4], zorder=4, edgecolors="black", linewidth=0.6)

    # Trend line (linear fit in log space for better visual)
    coeffs = np.polyfit(BOUNDARIES_PER_BYTE, DENSITY_THROUGHPUT, 1)
    x_fit = np.linspace(BOUNDARIES_PER_BYTE.min() * 0.8,
                        BOUNDARIES_PER_BYTE.max() * 1.1, 100)
    ax2.plot(x_fit, np.polyval(coeffs, x_fit), "--", color=PALETTE[1],
             linewidth=1.5, alpha=0.7, label="Linear trend")

    # Annotate points
    for lbl, bx, by in zip(DENSITY_DATASETS, BOUNDARIES_PER_BYTE, DENSITY_THROUGHPUT):
        ax2.annotate(lbl, (bx, by), textcoords="offset points",
                     xytext=(6, 8), fontsize=8, ha="left")

    ax2.set_xlabel("Structural Density (boundaries / byte)")
    ax2.set_ylabel("Throughput (MB/s)")
    ax2.set_title("(b) Throughput vs Structural Density", fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(linewidth=0.4, alpha=0.6)

    fig.tight_layout(w_pad=3)
    save(fig, "scalability_analysis")


# ===================================================================
# Figure 4 — Speculation Accuracy (dual y-axes)
# ===================================================================
def fig_speculation():
    print("Figure 4: speculation_accuracy")
    n = len(SPEC_DATASETS)
    x = np.arange(n)
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width / 2, BYTE_ACCURACY, width,
                    label="Byte prediction accuracy (%)",
                    color=PALETTE[0], edgecolor="white", zorder=3)
    bars2 = ax2.bar(x + width / 2, ALLOC_REDUCTION, width,
                    label="Allocation reduction factor",
                    color=PALETTE[2], edgecolor="white", zorder=3)

    # Value labels
    for bar, val in zip(bars1, BYTE_ACCURACY):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{val:.1f}%", ha="center", va="bottom", fontsize=9, color=PALETTE[0])
    for bar, val in zip(bars2, ALLOC_REDUCTION):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.02,
                 f"{val:g}×", ha="center", va="bottom", fontsize=9, color=PALETTE[2])

    ax1.set_xlabel("Dataset")
    ax1.set_ylabel("Byte Prediction Accuracy (%)", color=PALETTE[0])
    ax2.set_ylabel("Allocation Reduction Factor", color=PALETTE[2])
    ax1.set_xticks(x)
    ax1.set_xticklabels(DATASET_LABELS)
    ax1.set_ylim(0, 115)
    ax2.set_ylim(0, max(ALLOC_REDUCTION) * 1.20)
    ax1.set_title("Speculative Field Detection: Accuracy & Allocation Savings", fontsize=13)

    # Unified legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", framealpha=0.9)

    ax1.tick_params(axis="y", labelcolor=PALETTE[0])
    ax2.tick_params(axis="y", labelcolor=PALETTE[2])
    ax1.grid(axis="y", linewidth=0.4, alpha=0.6)

    save(fig, "speculation_accuracy")


# ===================================================================
# Main
# ===================================================================
def main():
    print(f"Generating figures in {os.path.abspath(OUT_DIR)} …\n")
    fig_throughput()
    fig_hardware()
    fig_scalability()
    fig_speculation()
    print("\nDone — 8 files generated.")


if __name__ == "__main__":
    main()
