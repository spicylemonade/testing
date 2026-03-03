"""
Visualization module for the N-body gravity simulator.
=====================================================

Generates 2D scatter plot animations and static figures from simulation output.

Usage:
    python src/visualize.py results/baseline/ --output figures/baseline_animation.gif
    python src/visualize.py results/baseline/ --static --output figures/baseline_snapshot.png
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless rendering
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Publication-grade styling
import seaborn as sns
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.figsize": (8, 8),
    "figure.facecolor": "white",
})


def load_positions(data_dir):
    """Load position data from simulation output."""
    pos_path = os.path.join(data_dir, "positions.npy")
    if not os.path.exists(pos_path):
        raise FileNotFoundError(f"No positions.npy found in {data_dir}")
    return np.load(pos_path)


def load_energy(data_dir):
    """Load energy data from CSV."""
    import csv
    energy_path = os.path.join(data_dir, "energy_drift.csv")
    if not os.path.exists(energy_path):
        return None
    steps, totals, kinetics, potentials = [], [], [], []
    with open(energy_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            steps.append(int(row["timestep"]))
            totals.append(float(row["total_energy"]))
            kinetics.append(float(row["kinetic_energy"]))
            potentials.append(float(row["potential_energy"]))
    return {
        "steps": np.array(steps),
        "total": np.array(totals),
        "kinetic": np.array(kinetics),
        "potential": np.array(potentials),
    }


def create_animation(positions, output_path, fps=30, every_n=1, title="N-body Simulation"):
    """
    Create animated GIF of body positions over time.

    Parameters
    ----------
    positions : ndarray, shape (n_frames, N, 2)
    output_path : str
    fps : int
    every_n : int, render every nth frame to reduce file size
    title : str
    """
    frames = positions[::every_n]
    n_frames = len(frames)

    # Compute axis limits from all frames
    all_x = positions[:, :, 0].flatten()
    all_y = positions[:, :, 1].flatten()
    margin = 0.1
    x_range = all_x.max() - all_x.min()
    y_range = all_y.max() - all_y.min()
    xlim = (all_x.min() - margin * x_range, all_x.max() + margin * x_range)
    ylim = (all_y.min() - margin * y_range, all_y.max() + margin * y_range)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    scatter = ax.scatter([], [], s=15, c="steelblue", alpha=0.8, edgecolors="navy",
                         linewidth=0.5)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.set_aspect("equal")
    time_text = ax.text(0.02, 0.98, "", transform=ax.transAxes, fontsize=10,
                        verticalalignment="top",
                        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    def init():
        scatter.set_offsets(np.empty((0, 2)))
        time_text.set_text("")
        return scatter, time_text

    def update(frame_idx):
        scatter.set_offsets(frames[frame_idx])
        time_text.set_text(f"Step {frame_idx * every_n}/{len(positions) - 1}")
        return scatter, time_text

    anim = animation.FuncAnimation(fig, update, init_func=init,
                                   frames=n_frames, interval=1000 // fps,
                                   blit=True)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                exist_ok=True)

    if output_path.endswith(".gif"):
        anim.save(output_path, writer="pillow", fps=fps)
    elif output_path.endswith(".mp4"):
        anim.save(output_path, writer="ffmpeg", fps=fps)
    else:
        anim.save(output_path, writer="pillow", fps=fps)

    plt.close(fig)
    print(f"Animation saved to {output_path}")


def create_static_snapshot(positions, output_path, frame_indices=None,
                           title="N-body Simulation"):
    """
    Create a static multi-panel figure showing snapshots at different times.

    Parameters
    ----------
    positions : ndarray, shape (n_frames, N, 2)
    output_path : str
    frame_indices : list of int, frames to show (default: 4 evenly spaced)
    title : str
    """
    n_frames = len(positions)
    if frame_indices is None:
        frame_indices = [0, n_frames // 4, n_frames // 2, n_frames - 1]

    n_panels = len(frame_indices)
    fig, axes = plt.subplots(1, n_panels, figsize=(4 * n_panels, 4))
    if n_panels == 1:
        axes = [axes]

    # Global limits
    all_x = positions[:, :, 0].flatten()
    all_y = positions[:, :, 1].flatten()
    margin = 0.1
    x_range = all_x.max() - all_x.min()
    y_range = all_y.max() - all_y.min()
    xlim = (all_x.min() - margin * x_range, all_x.max() + margin * x_range)
    ylim = (all_y.min() - margin * y_range, all_y.max() + margin * y_range)

    for ax, fidx in zip(axes, frame_indices):
        ax.scatter(positions[fidx, :, 0], positions[fidx, :, 1],
                   s=15, c="steelblue", alpha=0.8, edgecolors="navy",
                   linewidth=0.5)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"t = {fidx}")
        ax.set_aspect("equal")

    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")

    # Also save PDF
    pdf_path = output_path.rsplit(".", 1)[0] + ".pdf"
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Static figure saved to {output_path} and {pdf_path}")


def plot_energy_drift(data_dir, output_path):
    """
    Plot energy drift over time.

    Parameters
    ----------
    data_dir : str
    output_path : str
    """
    energy = load_energy(data_dir)
    if energy is None:
        print("No energy data found.")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Total energy
    ax1.plot(energy["steps"], energy["total"], color="black", linewidth=1,
             label="Total")
    ax1.plot(energy["steps"], energy["kinetic"], color="tab:red", linewidth=0.8,
             alpha=0.7, label="Kinetic")
    ax1.plot(energy["steps"], energy["potential"], color="tab:blue", linewidth=0.8,
             alpha=0.7, label="Potential")
    ax1.set_ylabel("Energy")
    ax1.set_title("Energy Components Over Time")
    ax1.legend()

    # Relative drift
    e0 = energy["total"][0]
    if abs(e0) > 1e-30:
        drift = (energy["total"] - e0) / abs(e0) * 100
    else:
        drift = energy["total"] - e0
    ax2.plot(energy["steps"], drift, color="tab:orange", linewidth=1)
    ax2.set_xlabel("Timestep")
    ax2.set_ylabel("Relative Energy Drift (%)")
    ax2.set_title("Energy Conservation")
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)

    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    pdf_path = output_path.rsplit(".", 1)[0] + ".pdf"
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Energy plot saved to {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="N-body Simulation Visualization")
    parser.add_argument("data_dir", type=str, help="Directory containing simulation output")
    parser.add_argument("--output", type=str, default="figures/animation.gif",
                        help="Output file path")
    parser.add_argument("--static", action="store_true",
                        help="Generate static snapshot instead of animation")
    parser.add_argument("--energy", action="store_true",
                        help="Plot energy drift")
    parser.add_argument("--fps", type=int, default=30, help="Animation FPS")
    parser.add_argument("--every-n", type=int, default=1,
                        help="Render every nth frame")
    parser.add_argument("--title", type=str, default="N-body Simulation",
                        help="Figure title")

    args = parser.parse_args()

    if args.energy:
        plot_energy_drift(args.data_dir, args.output)
    elif args.static:
        positions = load_positions(args.data_dir)
        create_static_snapshot(positions, args.output, title=args.title)
    else:
        positions = load_positions(args.data_dir)
        create_animation(positions, args.output, fps=args.fps,
                         every_n=args.every_n, title=args.title)


if __name__ == "__main__":
    main()
