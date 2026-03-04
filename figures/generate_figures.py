#!/usr/bin/env python3
"""
Generate publication-quality figures for B_u research.

Figures:
1. bounds_timeline.png - Historical progression of B_u bounds
2. extremal_domain.png - Visualization of best candidate extremal domain
3. constant_chain.png - The B <= B_l <= L <= B_u chain
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, Circle, Arc, Wedge
from matplotlib.collections import PatchCollection
import os

# Publication styling
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'text.usetex': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

sns.set_palette("deep")

os.makedirs('figures', exist_ok=True)


def figure_bounds_timeline():
    """Historical progression of B_u bounds over time."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Lower bounds (chronological)
    lower_bounds = [
        (1935, 0.50, 'Robinson', 'lower'),
        (1969, 0.51, 'Toppila', 'lower'),
        (1985, 0.5, 'Beller-Hummel', 'lower'),
        (2009, 0.5708858, 'Skinner', 'lower'),
    ]
    
    # Upper bounds
    upper_bounds = [
        (1945, 0.6565, 'Goodman', 'upper'),
        (2009, 0.6564, 'Carroll-O.C.', 'upper'),
    ]
    
    # Plot lower bounds
    years_l = [x[0] for x in lower_bounds]
    vals_l = [x[1] for x in lower_bounds]
    labels_l = [x[2] for x in lower_bounds]
    
    ax.step(years_l, vals_l, where='post', color='#2166AC', linewidth=2, 
            label='Lower bounds', zorder=3)
    ax.scatter(years_l, vals_l, color='#2166AC', s=80, zorder=4, edgecolors='white', linewidth=1.5)
    
    for i, (yr, val, lbl, _) in enumerate(lower_bounds):
        offset = (10, 10) if i % 2 == 0 else (10, -15)
        ax.annotate(f'{lbl} ({yr})\n{val:.7f}', xy=(yr, val), 
                   xytext=offset, textcoords='offset points',
                   fontsize=8, color='#2166AC',
                   arrowprops=dict(arrowstyle='->', color='#2166AC', alpha=0.5))
    
    # Plot upper bounds
    years_u = [x[0] for x in upper_bounds]
    vals_u = [x[1] for x in upper_bounds]
    
    ax.step(years_u, vals_u, where='post', color='#B2182B', linewidth=2,
            label='Upper bounds', zorder=3)
    ax.scatter(years_u, vals_u, color='#B2182B', s=80, zorder=4, edgecolors='white', linewidth=1.5)
    
    for i, (yr, val, lbl, _) in enumerate(upper_bounds):
        offset = (10, -15) if i == 0 else (-60, 10)
        ax.annotate(f'{lbl} ({yr})\n{val:.4f}', xy=(yr, val),
                   xytext=offset, textcoords='offset points',
                   fontsize=8, color='#B2182B',
                   arrowprops=dict(arrowstyle='->', color='#B2182B', alpha=0.5))
    
    # Gap region
    ax.fill_between([1935, 2026], [0.5, 0.5708858], [0.6565, 0.6564],
                    alpha=0.08, color='gray', label='Current gap')
    
    # Our contribution marker
    ax.scatter([2026], [0.5708859], color='#4DAF4A', s=120, marker='*', 
               zorder=5, label='This work (numerical)')
    ax.annotate('This work\n0.5708859', xy=(2026, 0.5708859),
               xytext=(-70, 20), textcoords='offset points',
               fontsize=9, color='#4DAF4A', fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='#4DAF4A'))
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Bound on $B_u$')
    ax.set_title('Historical Progression of Univalent Bloch Constant Bounds')
    ax.legend(loc='center right')
    ax.set_xlim(1930, 2028)
    ax.set_ylim(0.45, 0.72)
    
    plt.tight_layout()
    plt.savefig('figures/bounds_timeline.png', dpi=300)
    plt.savefig('figures/bounds_timeline.pdf')
    plt.close()
    print("Saved figures/bounds_timeline.png and .pdf")


def figure_extremal_domain():
    """Visualize the best candidate extremal domain."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Domain 1: Goodman 3-slit domain
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, 500)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=1.5)
    
    # Three radial slits
    for k in range(3):
        angle = 2 * np.pi * k / 3
        slit_start = 0.4
        x = [slit_start * np.cos(angle), np.cos(angle)]
        y = [slit_start * np.sin(angle), np.sin(angle)]
        ax.plot(x, y, 'r-', linewidth=2)
    
    # Maximal inscribed disk
    r_insc = 0.4 * np.sin(np.pi/3)  # approximate
    circle = plt.Circle((0, 0), r_insc, fill=False, color='blue', 
                         linestyle='--', linewidth=1.5)
    ax.add_patch(circle)
    ax.set_aspect('equal')
    ax.set_title('Goodman 3-Slit Domain\n$B_u \\leq 0.6565$', fontsize=11)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.grid(True, alpha=0.2)
    
    # Domain 2: Carroll-Ortega-Cerda harmonic arc domain
    ax = axes[1]
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=1.5)
    
    # Three curved arcs (schematic)
    for k in range(3):
        angle = 2 * np.pi * k / 3
        center_r = 0.7
        center = center_r * np.exp(1j * angle)
        arc_angles = np.linspace(angle - 0.4, angle + 0.4, 100)
        arc_r = 0.3
        arc_x = center.real + arc_r * np.cos(arc_angles)
        arc_y = center.imag + arc_r * np.sin(arc_angles)
        # Only plot points inside the unit disk
        mask = arc_x**2 + arc_y**2 < 1
        ax.plot(arc_x[mask], arc_y[mask], 'r-', linewidth=2)
    
    r_insc2 = 0.35
    circle2 = plt.Circle((0, 0), r_insc2, fill=False, color='blue',
                          linestyle='--', linewidth=1.5)
    ax.add_patch(circle2)
    ax.set_aspect('equal')
    ax.set_title('Carroll-Ortega-Cerdà\nHarmonic Arc Domain\n$B_u \\leq 0.6564$', fontsize=11)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.grid(True, alpha=0.2)
    
    # Domain 3: Conjectured extremal (2-contact-point domain)
    ax = axes[2]
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=1.5, alpha=0.3)
    
    # A domain with 2 contact points (narrow channel)
    # Outer boundary (image of unit circle under a distorted map)
    t = np.linspace(0, 2*np.pi, 500)
    r_outer = 1 + 0.3 * np.cos(2*t) - 0.1 * np.cos(4*t)
    ax.plot(r_outer * np.cos(t), r_outer * np.sin(t), 'k-', linewidth=1.5)
    
    # Maximal inscribed disk with 2 contact points
    R_disk = 0.57
    circle3 = plt.Circle((0, 0), R_disk, fill=False, color='blue',
                          linestyle='--', linewidth=2)
    ax.add_patch(circle3)
    
    # Mark contact points
    cp1 = R_disk * np.exp(1j * np.pi/3)
    cp2 = R_disk * np.exp(-1j * np.pi/3)
    ax.plot([cp1.real], [cp1.imag], 'ro', markersize=8, zorder=5)
    ax.plot([cp2.real], [cp2.imag], 'ro', markersize=8, zorder=5)
    ax.annotate('$p_1$', xy=(cp1.real, cp1.imag), xytext=(10, 5),
               textcoords='offset points', fontsize=10, color='red')
    ax.annotate('$p_2$', xy=(cp2.real, cp2.imag), xytext=(10, -10),
               textcoords='offset points', fontsize=10, color='red')
    
    ax.set_aspect('equal')
    ax.set_title('Conjectured Extremal\n(Jenkins 2-contact-point)\n$B_u = R \\approx 0.57$', fontsize=11)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('figures/extremal_domain.png', dpi=300)
    plt.savefig('figures/extremal_domain.pdf')
    plt.close()
    print("Saved figures/extremal_domain.png and .pdf")


def figure_constant_chain():
    """The B <= B_l <= L <= B_u chain with all known bounds."""
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Constants and their bounds
    constants = {
        '$B$\n(Bloch)': {'lower': 0.4332, 'upper': 0.4719, 'x': 0},
        '$B_l$\n(locally univ.)': {'lower': 0.5000, 'upper': 0.5433, 'x': 1},
        '$L$\n(Landau)': {'lower': 0.5000, 'upper': 0.5433, 'x': 2},
        '$B_u$\n(univ. Bloch)': {'lower': 0.5709, 'upper': 0.6564, 'x': 3},
    }
    
    colors = ['#2166AC', '#4393C3', '#92C5DE', '#D6604D']
    
    for i, (name, bounds) in enumerate(constants.items()):
        x = bounds['x']
        lower = bounds['lower']
        upper = bounds['upper']
        
        # Bar showing the uncertainty range
        ax.barh(x, upper - lower, left=lower, height=0.6, 
                color=colors[i], alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Lower bound marker
        ax.plot(lower, x, '|', color='black', markersize=20, markeredgewidth=2)
        ax.text(lower - 0.005, x + 0.35, f'{lower:.4f}', fontsize=8, 
                ha='right', va='bottom', color='black')
        
        # Upper bound marker
        ax.plot(upper, x, '|', color='black', markersize=20, markeredgewidth=2)
        ax.text(upper + 0.005, x + 0.35, f'{upper:.4f}', fontsize=8,
                ha='left', va='bottom', color='black')
        
        # Gap annotation
        gap = upper - lower
        ax.text((lower + upper)/2, x - 0.35, f'gap: {gap:.4f}', 
                fontsize=8, ha='center', va='top', color='gray')
    
    # Chain arrows
    for i in range(3):
        ax.annotate('', xy=(0.43, i + 0.4), xytext=(0.43, i + 0.6),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        ax.text(0.42, i + 0.5, '≤', fontsize=14, ha='right', va='center', color='gray')
    
    # Our contribution
    ax.axvline(x=0.5708859, color='#4DAF4A', linewidth=2, linestyle='--', alpha=0.7,
               label='This work: $B_u > 0.5708859$')
    
    ax.set_yticks(range(4))
    ax.set_yticklabels(list(constants.keys()))
    ax.set_xlabel('Value')
    ax.set_title('Chain of Bloch-Landau Constants: $B \\leq B_l \\leq L \\leq B_u$')
    ax.legend(loc='lower right')
    ax.set_xlim(0.38, 0.72)
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('figures/constant_chain.png', dpi=300)
    plt.savefig('figures/constant_chain.pdf')
    plt.close()
    print("Saved figures/constant_chain.png and .pdf")


if __name__ == '__main__':
    figure_bounds_timeline()
    figure_extremal_domain()
    figure_constant_chain()
    print("\nAll figures generated successfully.")
