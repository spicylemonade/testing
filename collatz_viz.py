"""Publication-quality visualization toolkit for Collatz dynamics."""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Publication-quality defaults
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
    'figure.figsize': (8, 5), 'figure.dpi': 300,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'axes.labelsize': 13,
    'axes.titlesize': 14, 'axes.titleweight': 'bold',
    'xtick.labelsize': 11, 'ytick.labelsize': 11,
    'legend.fontsize': 11, 'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8', 'font.family': 'serif',
    'grid.alpha': 0.3, 'grid.linewidth': 0.5,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})

from collatz_engine import collatz_trajectory, batch_stopping_times
from collatz_features import encode_trajectory_binary

COLORS = sns.color_palette("deep")


def plot_trajectory(n, output_path="figures/trajectory.png"):
    """Plot the Collatz trajectory for starting value n."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    traj = collatz_trajectory(n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True,
                                    gridspec_kw={'height_ratios': [3, 1]})

    # Top: trajectory values
    ax1.plot(range(len(traj)), traj, color=COLORS[0], linewidth=0.8, alpha=0.9)
    ax1.fill_between(range(len(traj)), traj, alpha=0.15, color=COLORS[0])
    ax1.set_ylabel("Value")
    ax1.set_title(f"Collatz Trajectory for n = {n:,} (stopping time = {len(traj)-1})")
    ax1.set_xlim(0, len(traj) - 1)

    # Bottom: log-scale trajectory
    log_traj = [np.log10(max(v, 1)) for v in traj]
    ax2.plot(range(len(log_traj)), log_traj, color=COLORS[2], linewidth=0.8)
    ax2.set_xlabel("Step")
    ax2.set_ylabel("log₁₀(value)")
    ax2.set_xlim(0, len(traj) - 1)

    plt.savefig(output_path, dpi=300)
    pdf_path = output_path.replace('.png', '.pdf')
    plt.savefig(pdf_path)
    plt.close()
    return output_path


def plot_stopping_time_heatmap(N, p=7, q=11, output_path="figures/stopping_time_heatmap.png"):
    """Create 2D heatmap of stopping times arranged by (n mod p, n mod q)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    stop_times = batch_stopping_times(N)

    grid = np.zeros((p, q))
    counts = np.zeros((p, q))
    for n in range(1, N + 1):
        r_p = n % p
        r_q = n % q
        grid[r_p, r_q] += stop_times[n]
        counts[r_p, r_q] += 1

    counts[counts == 0] = 1
    mean_grid = grid / counts

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
    im = ax.imshow(mean_grid, cmap="viridis", aspect='auto', origin='lower')
    ax.set_xlabel(f"n mod {q}")
    ax.set_ylabel(f"n mod {p}")
    ax.set_title(f"Mean Stopping Time by Residue Class (N = {N:,})")
    ax.set_xticks(range(q))
    ax.set_yticks(range(p))
    cbar = plt.colorbar(im, ax=ax, label="Mean Stopping Time")

    plt.savefig(output_path, dpi=300)
    plt.savefig(output_path.replace('.png', '.pdf'))
    plt.close()
    return output_path


def plot_parity_spectrogram(n_range, output_path="figures/parity_spectrogram.png"):
    """Create spectrogram of parity sequences for a range of starting values."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    start, end = n_range[0], n_range[-1]

    # Collect parity sequences, pad to same length
    max_len = 0
    sequences = []
    for n in range(start, end + 1):
        ps = encode_trajectory_binary(n)
        sequences.append(ps)
        if len(ps) > max_len:
            max_len = len(ps)

    max_len = min(max_len, 300)  # Cap for visualization
    matrix = np.zeros((len(sequences), max_len))
    for i, ps in enumerate(sequences):
        length = min(len(ps), max_len)
        matrix[i, :length] = ps[:length]

    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    im = ax.imshow(matrix, cmap="RdBu_r", aspect='auto', interpolation='nearest',
                   vmin=0, vmax=1)
    ax.set_xlabel("Trajectory Step")
    ax.set_ylabel(f"Starting Value n ({start} to {end})")
    ax.set_title("Parity Sequence Spectrogram (blue=even, red=odd)")
    # Reduce y-tick density
    ytick_step = max(1, len(sequences) // 10)
    yticks = range(0, len(sequences), ytick_step)
    ax.set_yticks(list(yticks))
    ax.set_yticklabels([str(start + t) for t in yticks])
    plt.colorbar(im, ax=ax, label="Parity (0=even, 1=odd)")

    plt.savefig(output_path, dpi=300)
    plt.savefig(output_path.replace('.png', '.pdf'))
    plt.close()
    return output_path


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)

    # Demo 1: Trajectory plot
    p1 = plot_trajectory(27, "figures/trajectory_27.png")
    print(f"Saved: {p1}")

    # Demo 2: Stopping time heatmap
    p2 = plot_stopping_time_heatmap(100000, p=7, q=11, output_path="figures/stopping_time_heatmap.png")
    print(f"Saved: {p2}")

    # Demo 3: Parity spectrogram
    p3 = plot_parity_spectrogram(range(1, 201), "figures/parity_spectrogram.png")
    print(f"Saved: {p3}")

    print("All visualizations generated!")
