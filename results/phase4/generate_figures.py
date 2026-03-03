#!/usr/bin/env python3
"""
Generate publication-quality figures for the Bloch constant project.

Produces 4 figures saved to figures/ as both PNG (300 DPI) and PDF.
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style='whitegrid', context='paper', font_scale=1.2)
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
})

# Ensure output directory exists
FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)


def save_figure(fig, name):
    """Save figure as both PNG and PDF."""
    png_path = os.path.join(FIGURES_DIR, f'{name}.png')
    pdf_path = os.path.join(FIGURES_DIR, f'{name}.pdf')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
    print(f"  Saved {png_path}")
    print(f"  Saved {pdf_path}")
    plt.close(fig)


# ============================================================================
# Figure 1: Timeline of B_u lower and upper bounds
# ============================================================================
def figure1_bounds_timeline():
    print("Generating Figure 1: bounds_timeline ...")

    # Lower bound data
    lb_years =  [1929,    1935,     1956,   1985,     2009]
    lb_values = [0.50,    0.50,     0.501,  0.5705,   0.5708858]
    lb_labels = ['Landau', 'Robinson', 'Reich', 'Beller &\nHummel', 'Skinner']

    # Upper bound data
    ub_years =  [2009]
    ub_values = [0.6564]
    ub_labels = ['Carroll &\nOrtega-Cerdà']

    fig, ax = plt.subplots(figsize=(10, 5))

    # Shade the current gap
    ax.axhspan(0.5708858, 0.6564, alpha=0.12, color='#888888',
               label=r'Current gap $[0.5709, 0.6564]$')

    # Horizontal dashed lines at current best bounds
    ax.axhline(0.5708858, color='steelblue', ls='--', lw=0.8, alpha=0.6)
    ax.axhline(0.6564, color='firebrick', ls='--', lw=0.8, alpha=0.6)

    # Plot lower bounds
    ax.scatter(lb_years, lb_values, s=90, marker='o', color='steelblue',
               edgecolors='k', linewidths=0.5, zorder=5, label='Lower bounds')
    ax.plot(lb_years, lb_values, color='steelblue', lw=1.2, alpha=0.5, zorder=4)

    # Plot upper bounds
    ax.scatter(ub_years, ub_values, s=110, marker='D', color='firebrick',
               edgecolors='k', linewidths=0.5, zorder=5, label='Upper bounds')

    # Add year/author labels for lower bounds
    offsets_lb = [
        (0, -0.022),   # Landau
        (0, 0.015),    # Robinson
        (0, -0.022),   # Reich
        (0, 0.015),    # Beller-Hummel
        (0, -0.028),   # Skinner
    ]
    for yr, val, lbl, (dx, dy) in zip(lb_years, lb_values, lb_labels, offsets_lb):
        ax.annotate(f'{lbl}\n({yr})', xy=(yr, val), xytext=(yr + dx, val + dy),
                    fontsize=8, ha='center', va='center',
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5)
                    if abs(dy) > 0.02 else None)

    # Label upper bound
    ax.annotate(f'{ub_labels[0]}\n({ub_years[0]})',
                xy=(ub_years[0], ub_values[0]),
                xytext=(ub_years[0] - 12, ub_values[0] + 0.025),
                fontsize=8, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.7))

    ax.set_xlabel('Year')
    ax.set_ylabel(r'$\mathcal{B}_u$ bound value')
    ax.set_title(r'Timeline of bounds on the univalent Bloch constant $\mathcal{B}_u$')
    ax.set_xlim(1920, 2020)
    ax.set_ylim(0.44, 0.72)
    ax.legend(loc='upper left', framealpha=0.9)

    save_figure(fig, 'bounds_timeline')


# ============================================================================
# Figure 2: Image domain of a near-extremal univalent function
# ============================================================================
def figure2_extremal_function():
    print("Generating Figure 2: extremal_function ...")

    # f(z) = z - 0.21 * z^3  (univalent since |c|=0.21 < 1)
    def f(z):
        return z - 0.21 * z**3

    t = np.linspace(0, 2 * np.pi, 1000)
    radii = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
    cmap = plt.cm.viridis

    fig, ax = plt.subplots(figsize=(7, 7))

    # Plot level curves f(r * e^{it}) coloured by radius
    for i, r in enumerate(radii):
        z = r * np.exp(1j * t)
        w = f(z)
        color = cmap(i / (len(radii) - 1))
        lw = 2.5 if r == 0.99 else 1.0
        alpha = 1.0 if r == 0.99 else 0.7
        ax.plot(w.real, w.imag, color=color, lw=lw, alpha=alpha,
                label=f'$r = {r}$')

    # Compute the largest inscribed disk
    # For f(z) = z - 0.21 z^3, f'(z) = 1 - 0.63 z^2
    # The Bloch radius is min_{|z|<1} (1-|z|^2) |f'(z)|
    # We approximate numerically
    r_grid = np.linspace(0, 0.999, 2000)
    t_grid = np.linspace(0, 2 * np.pi, 500)
    R, T = np.meshgrid(r_grid, t_grid)
    Z = R * np.exp(1j * T)
    Fprime = 1 - 0.63 * Z**2
    bloch_vals = (1 - R**2) * np.abs(Fprime)
    min_idx = np.unravel_index(np.argmin(bloch_vals), bloch_vals.shape)
    B_f = bloch_vals[min_idx]
    z_min = Z[min_idx]
    center = f(z_min)

    # Draw inscribed disk
    disk_t = np.linspace(0, 2 * np.pi, 500)
    disk_x = center.real + B_f * np.cos(disk_t)
    disk_y = center.imag + B_f * np.sin(disk_t)
    ax.plot(disk_x, disk_y, 'r--', lw=1.5, alpha=0.8, label=f'Inscribed disk ($r_B \\approx {B_f:.4f}$)')
    ax.fill(disk_x, disk_y, color='red', alpha=0.06)

    # Mark center of inscribed disk
    ax.plot(center.real, center.imag, 'r+', markersize=10, mew=1.5)

    ax.set_xlabel('Re $f(z)$')
    ax.set_ylabel('Im $f(z)$')
    ax.set_title(r'Image domain of $f(z) = z - 0.21\,z^3$')
    ax.set_aspect('equal')
    ax.legend(loc='lower left', fontsize=8, framealpha=0.9)

    # Colorbar for radius
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('$r = |z|$')

    save_figure(fig, 'extremal_function')


# ============================================================================
# Figure 3: Optimization landscape for f(z) = z + a*z^2 + b*z^3
# ============================================================================
def figure3_optimization_landscape():
    print("Generating Figure 3: optimization_landscape ...")

    Na, Nb = 200, 200
    a_vals = np.linspace(-0.5, 0.5, Na)
    b_vals = np.linspace(-0.33, 0.33, Nb)
    A, B_ = np.meshgrid(a_vals, b_vals)

    # For f(z) = z + a z^2 + b z^3:
    #   f'(z) = 1 + 2a z + 3b z^2
    #   Sufficient univalence condition: 2|a| + 3|b| <= 1
    #   Bloch radius: min_{|z|<1} (1-|z|^2)|f'(z)|
    # We compute on a polar grid
    Nr, Nt = 200, 100
    r_grid = np.linspace(0, 0.995, Nr)
    t_grid = np.linspace(0, 2 * np.pi, Nt)

    Bf_map = np.full_like(A, np.nan)
    min_Bf = np.inf
    min_ab = (0, 0)

    for i in range(Nb):
        for j in range(Na):
            a = A[i, j]
            b = B_[i, j]
            # Check univalence
            if 2 * abs(a) + 3 * abs(b) > 1:
                continue
            # Compute Bloch radius
            best = np.inf
            for r in r_grid:
                z = r * np.exp(1j * t_grid)
                fp = 1 + 2 * a * z + 3 * b * z**2
                vals = (1 - r**2) * np.abs(fp)
                m = vals.min()
                if m < best:
                    best = m
            Bf_map[i, j] = best
            if best < min_Bf:
                min_Bf = best
                min_ab = (a, b)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Masked array for NaN (outside univalence region)
    masked = np.ma.masked_invalid(Bf_map)

    im = ax.pcolormesh(a_vals, b_vals, masked, cmap='RdYlBu_r', shading='auto')
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label(r'$\mathcal{B}_f$')

    # Mark minimum
    ax.plot(min_ab[0], min_ab[1], marker='*', color='gold', markersize=18,
            markeredgecolor='k', markeredgewidth=0.8, zorder=10,
            label=f'Min $\\mathcal{{B}}_f \\approx {min_Bf:.4f}$')

    # Show univalence boundary: 2|a| + 3|b| = 1
    # This is a diamond: |a| <= 0.5, |b| <= 1/3
    # Vertices: (0.5, 0), (0, 1/3), (-0.5, 0), (0, -1/3)
    diamond_a = [0.5, 0, -0.5, 0, 0.5]
    diamond_b = [0, 1/3, 0, -1/3, 0]
    ax.plot(diamond_a, diamond_b, 'k--', lw=1.2, alpha=0.7,
            label=r'Univalence boundary ($2|a|+3|b|=1$)')

    ax.set_xlabel(r'$a$ (coefficient of $z^2$)')
    ax.set_ylabel(r'$b$ (coefficient of $z^3$)')
    ax.set_title(r'Bloch radius $\mathcal{B}_f$ for $f(z) = z + az^2 + bz^3$')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    save_figure(fig, 'optimization_landscape')


# ============================================================================
# Figure 4: Horizontal bar chart comparing methods
# ============================================================================
def figure4_method_comparison():
    print("Generating Figure 4: method_comparison ...")

    # Data
    lower_methods = ['Koebe', 'Beller-Hummel', 'Skinner', 'Our hyperbolic']
    lower_values =  [0.25,    0.5705,          0.5709,    0.25]

    upper_methods = ['Trivial', 'Strip', 'Our polynomial', 'Carroll-OC']
    upper_values =  [1.0,       0.7854,  0.6808,           0.6564]

    # Combine: lower bounds first (bottom), then upper bounds (top)
    methods = lower_methods + upper_methods
    values = lower_values + upper_values
    colors = ['steelblue'] * len(lower_methods) + ['firebrick'] * len(upper_methods)

    fig, ax = plt.subplots(figsize=(9, 5.5))

    y_pos = np.arange(len(methods))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='k', linewidth=0.4,
                   height=0.6, alpha=0.85)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    ax.set_xlabel(r'Bound on $\mathcal{B}_u$')
    ax.set_title('Comparison of lower and upper bounds by method')

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(val + 0.012, bar.get_y() + bar.get_height() / 2,
                f'{val:.4f}', va='center', ha='left', fontsize=9)

    # Vertical lines at best known bounds
    ax.axvline(0.5709, color='steelblue', ls='--', lw=1.2, alpha=0.7,
               label=r'Best lower bound ($0.5709$)')
    ax.axvline(0.6564, color='firebrick', ls='--', lw=1.2, alpha=0.7,
               label=r'Best upper bound ($0.6564$)')

    # Shade the gap
    ax.axvspan(0.5709, 0.6564, alpha=0.08, color='gray')

    ax.set_xlim(0, 1.12)
    ax.legend(loc='lower right', framealpha=0.9)

    # Add a dividing line between lower and upper bound groups
    ax.axhline(len(lower_methods) - 0.5, color='gray', ls=':', lw=0.8, alpha=0.5)
    ax.text(1.05, len(lower_methods) - 0.8, 'Lower\nbounds', fontsize=8,
            color='steelblue', ha='center', va='top')
    ax.text(1.05, len(lower_methods) - 0.2, 'Upper\nbounds', fontsize=8,
            color='firebrick', ha='center', va='bottom')

    save_figure(fig, 'method_comparison')


# ============================================================================
# Main
# ============================================================================
if __name__ == '__main__':
    print(f"Output directory: {FIGURES_DIR}")
    print("=" * 60)
    figure1_bounds_timeline()
    figure2_extremal_function()
    figure3_optimization_landscape()
    figure4_method_comparison()
    print("=" * 60)
    print("All 4 figures generated successfully (8 files total).")
