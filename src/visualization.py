"""Visualization module for N-body trajectory plotting."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Publication-quality figure setup
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
    'figure.figsize': (8, 5),
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8',
    'font.family': 'serif',
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})


def plot_trajectories(trajectories, masses=None, title="N-Body Trajectories",
                      filename=None, show_trails=True, trail_alpha=0.3):
    """Plot particle trajectories as scatter + trail lines.

    Args:
        trajectories: array of shape (n_steps, N, 2) — position history
        masses: optional (N,) array for marker sizing
        title: plot title
        filename: if given, save to this path (supports .png and .pdf)
        show_trails: whether to draw trajectory lines
        trail_alpha: transparency of trail lines
    """
    colors = sns.color_palette("deep", n_colors=trajectories.shape[1])
    markers = ['o', 's', 'D', '^', 'v', 'p', '*', 'h']

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    n_bodies = trajectories.shape[1]
    sizes = 80 * np.ones(n_bodies) if masses is None else 40 + 120 * masses / masses.max()

    for i in range(n_bodies):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]

        if show_trails:
            ax.plot(trajectories[:, i, 0], trajectories[:, i, 1],
                    color=color, alpha=trail_alpha, linewidth=1.0, zorder=1)

        # Current position (last frame)
        ax.scatter(trajectories[-1, i, 0], trajectories[-1, i, 1],
                   s=sizes[i], color=color, marker=marker, edgecolors='black',
                   linewidths=0.5, zorder=3, label=f'Body {i+1}')

        # Starting position (faded)
        ax.scatter(trajectories[0, i, 0], trajectories[0, i, 1],
                   s=sizes[i] * 0.5, color=color, marker=marker, alpha=0.3,
                   edgecolors='gray', linewidths=0.3, zorder=2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.legend(loc='upper right', frameon=True)

    if filename:
        plt.savefig(filename, dpi=300)
        # Also save PDF
        if filename.endswith('.png'):
            plt.savefig(filename.replace('.png', '.pdf'))
    plt.close(fig)


def plot_snapshot(positions, masses=None, title="Particle Positions",
                  filename=None):
    """Plot current particle positions as a scatter plot.

    Args:
        positions: (N, 2) array
        masses: optional (N,) for marker sizing
        title: plot title
        filename: save path
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    colors = sns.color_palette("muted", n_colors=1)

    sizes = 20 if masses is None else 10 + 80 * masses / masses.max()
    ax.scatter(positions[:, 0], positions[:, 1], s=sizes, c=[colors[0]],
               edgecolors='black', linewidths=0.3, alpha=0.8)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)
    ax.set_aspect('equal')

    if filename:
        plt.savefig(filename, dpi=300)
        if filename.endswith('.png'):
            plt.savefig(filename.replace('.png', '.pdf'))
    plt.close(fig)
