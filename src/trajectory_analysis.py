#!/usr/bin/env python3
"""Statistical analysis and publication-quality figures for Collatz delay records.

Generates:
1. Delay vs bit-length plot with regression
2. Trajectory visualization for key records
3. Delay record growth pattern analysis
"""

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Publication-quality styling
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 15,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.figsize': (10, 7),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "experiments"

# All 148 known delay records from Roosendaal
DELAY_RECORDS_RAW = """2 3 6 7 9 18 25 27 54 73 97 129 171 231 313 327 649 703 871 1161 2223 2463 2919 3711 6171 10971 13255 17647 23529 26623 34239 35655 52527 77031 106239 142587 156159 216367 230631 410011 511935 626331 837799 1117065 1501353 1723519 2298025 3064033 3542887 3732423 5649499 6649279 8400511 11200681 14934241 15733191 31466382 36791535 63728127 127456254 169941673 226588897 268549803 537099606 670617279 1341234558 1412987847 1674652263 2610744987 4578853915 4890328815 9780657630 12212032815 12235060455 13371194527 17828259369 31694683323 63389366646 75128138247 133561134663 158294678119 166763117679 202485402111 404970804222 426635908975 568847878633 674190078379 881715740415 989345275647 1122382791663 1444338092271 1899148184679 2081751768559 2775669024745 3700892032993 3743559068799 7487118137598 7887663552367 10516884736489 14022512981985 19536224150271 26262557464201 27667550250351 38903934249727 48575069253735 51173735510107 60650353197163 80867137596217 100759293214567 134345724286089 223656998090055 397612441048987 530149921398649 706866561864865 942488749153153 1256651665537537 1675535554050049 2234047405400065 2978729873866753 3586720916237671 4320515538764287 4861718551722727 6482291402296969 7579309213675935 12769884180266527 17026512240355369 22702016320473825 45404032640947650 46785696846401151 93571393692802302 104899295810901231 209798591621802462 279731455495736617 372975273994315489 497300365325753985 539483373894066267 931386509544713451 1278775404785934855 1339302163616345727 2678604327232691454 3571472436310255273 4761963248413673697 5065931099926693735 5977996304343501855 9781262575275081247 13041683433700108329 14727207461063895711 28019077177231758495"""


def delay_combined(n: int) -> int:
    """Delay using combined steps."""
    x = n
    s = 0
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
            s += 2
        else:
            x >>= 1
            s += 1
    return s


def max_excursion(n: int) -> int:
    peak = n
    x = n
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
        else:
            x >>= 1
        if x > peak:
            peak = x
    return peak


def compute_record_data():
    """Compute delay and properties for all known records."""
    records = [int(x) for x in DELAY_RECORDS_RAW.split()]
    data = []
    for n in records:
        d = delay_combined(n)
        bits = n.bit_length()
        data.append({
            "n": n,
            "delay": d,
            "bits": bits,
            "log10_n": math.log10(n) if n > 0 else 0,
        })
    return data


def plot_delay_vs_bitlength(data):
    """Create delay vs bit-length scatter plot with regression."""
    bits = np.array([d["bits"] for d in data])
    delays = np.array([d["delay"] for d in data])
    
    # Linear regression
    coeffs = np.polyfit(bits, delays, 1)
    poly = np.poly1d(coeffs)
    x_fit = np.linspace(bits.min(), bits.max(), 100)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Color by whether below/above 10^19
    colors = ['#2196F3' if d["n"] < 10**19 else '#F44336' for d in data]
    
    ax.scatter(bits, delays, c=colors, s=20, alpha=0.7, edgecolors='none', zorder=3)
    ax.plot(x_fit, poly(x_fit), 'k--', alpha=0.5, linewidth=1.5, 
            label=f'Linear fit: delay = {coeffs[0]:.1f} * bits + {coeffs[1]:.0f}')
    
    # Highlight key records
    highlights = {
        63728127: "a(8)=63,728,127",
        931386509544713451: "a(18)",
        9781262575275081247: "Best < 10^19",
        28019077177231758495: "Record #148",
    }
    for d in data:
        if d["n"] in highlights:
            ax.annotate(highlights[d["n"]], (d["bits"], d["delay"]),
                       textcoords="offset points", xytext=(10, 5),
                       fontsize=9, color='darkred',
                       arrowprops=dict(arrowstyle='->', color='darkred', lw=0.8))
    
    ax.set_xlabel('Bit-length of n')
    ax.set_ylabel('Total stopping time (delay)')
    ax.set_title('Collatz Delay Records: Stopping Time vs Bit-Length\n(148 known records from Roosendaal database)')
    ax.legend(loc='upper left')
    
    # Add color legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#2196F3', markersize=8, label='Below 10^19'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#F44336', markersize=8, label='Above 10^19'),
    ]
    ax.legend(handles=legend_elements + [ax.get_legend().legend_handles[0]], 
              loc='upper left')
    
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / "delay_vs_bitlength.png")
    fig.savefig(FIGURES_DIR / "delay_vs_bitlength.pdf")
    plt.close(fig)
    print(f"  Saved delay_vs_bitlength.png/pdf")
    
    return {"slope": float(coeffs[0]), "intercept": float(coeffs[1])}


def plot_record_growth(data):
    """Plot delay record growth pattern: log(n) vs delay."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    log10_n = np.array([d["log10_n"] for d in data])
    delays = np.array([d["delay"] for d in data])
    record_nums = np.arange(1, len(data) + 1)
    
    # Left: delay vs log10(n)
    ax1.scatter(log10_n, delays, c='#2196F3', s=15, alpha=0.7, edgecolors='none')
    coeffs = np.polyfit(log10_n, delays, 1)
    x_fit = np.linspace(log10_n.min(), log10_n.max(), 100)
    ax1.plot(x_fit, np.poly1d(coeffs)(x_fit), 'k--', alpha=0.5, lw=1.5,
             label=f'Fit: delay = {coeffs[0]:.1f} * log10(n) + {coeffs[1]:.0f}')
    ax1.axvline(x=19, color='red', linestyle=':', alpha=0.5, label='10^19 boundary')
    ax1.set_xlabel('log₁₀(n)')
    ax1.set_ylabel('Total stopping time')
    ax1.set_title('Delay Records: Growth Pattern')
    ax1.legend(loc='upper left')
    
    # Right: gap ratios between consecutive records
    ns = np.array([d["n"] for d in data], dtype=float)
    ratios = ns[1:] / ns[:-1]
    ax2.scatter(record_nums[1:], ratios, c='#4CAF50', s=15, alpha=0.7, edgecolors='none')
    ax2.axhline(y=np.median(ratios), color='red', linestyle='--', alpha=0.5,
                label=f'Median ratio = {np.median(ratios):.3f}')
    ax2.axhline(y=2.0, color='gray', linestyle=':', alpha=0.3, label='Double (ratio=2)')
    ax2.set_xlabel('Record number')
    ax2.set_ylabel('N_{k+1} / N_k')
    ax2.set_title('Gap Ratios Between Consecutive Records')
    ax2.set_ylim(0.9, 3.0)
    ax2.legend()
    
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "record_growth_pattern.png")
    fig.savefig(FIGURES_DIR / "record_growth_pattern.pdf")
    plt.close(fig)
    print(f"  Saved record_growth_pattern.png/pdf")
    
    return {
        "delay_per_decade_slope": float(coeffs[0]),
        "median_gap_ratio": float(np.median(ratios)),
        "mean_gap_ratio": float(np.mean(ratios)),
    }


def plot_trajectory(n, label=""):
    """Plot the full trajectory of n."""
    traj = [n]
    x = n
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
        else:
            x >>= 1
        traj.append(x)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    steps = range(len(traj))
    log_traj = [math.log10(max(v, 1)) for v in traj]
    
    ax.plot(steps, log_traj, linewidth=0.5, color='#1565C0', alpha=0.8)
    ax.axhline(y=math.log10(n), color='red', linestyle='--', alpha=0.4, 
               label=f'Starting value (log₁₀ = {math.log10(n):.1f})')
    ax.fill_between(steps, 0, log_traj, alpha=0.1, color='#1565C0')
    
    ax.set_xlabel('Step number')
    ax.set_ylabel('log₁₀(value)')
    ax.set_title(f'Collatz Trajectory: n = {n:,}\n{label}')
    ax.legend()
    
    safe_name = str(n)[:20]
    fig.savefig(FIGURES_DIR / f"trajectory_{safe_name}.png")
    fig.savefig(FIGURES_DIR / f"trajectory_{safe_name}.pdf")
    plt.close(fig)
    print(f"  Saved trajectory_{safe_name}.png/pdf")


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=== Trajectory Analysis ===\n")
    
    print("Computing record data...")
    data = compute_record_data()
    print(f"  {len(data)} records processed")
    
    print("\nGenerating figures...")
    regression = plot_delay_vs_bitlength(data)
    growth = plot_record_growth(data)
    
    print("\nPlotting key trajectories...")
    plot_trajectory(9781262575275081247, 
                    "Highest delay record below 10^19 (delay=2426)")
    plot_trajectory(63728127,
                    "Classic benchmark a(8) (delay=949)")
    
    # Statistics
    below_19 = [d for d in data if d["n"] < 10**19]
    above_19 = [d for d in data if d["n"] >= 10**19]
    
    stats = {
        "total_records": len(data),
        "records_below_1e19": len(below_19),
        "records_above_1e19": len(above_19),
        "max_delay_below_1e19": max(d["delay"] for d in below_19),
        "max_delay_overall": max(d["delay"] for d in data),
        "regression": regression,
        "growth_pattern": growth,
        "records_per_decade": {
            str(i): sum(1 for d in data if i <= d["log10_n"] < i+1)
            for i in range(0, 20)
        },
    }
    
    out_path = RESULTS_DIR / "trajectory_statistics.json"
    out_path.write_text(json.dumps(stats, indent=2))
    print(f"\nStatistics saved to {out_path}")
    print(f"Figures saved to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
