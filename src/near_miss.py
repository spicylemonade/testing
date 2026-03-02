"""Near-miss scoring and statistical analysis for the perfect cuboid problem.

Collects Euler bricks from all search methods, scores them by how close
their space diagonal is to an integer, and performs statistical analysis
to assess whether the distribution is consistent with random or shows
systematic avoidance of zero (evidence for non-existence).
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import Cuboid


def near_miss_score(a: int, b: int, c: int) -> float:
    """Compute near-miss score: min(frac, 1-frac) of space diagonal.

    Returns 0 for a perfect cuboid, approaches 0.5 for maximally non-integer.
    """
    sd = math.sqrt(a * a + b * b + c * c)
    frac = sd - math.floor(sd)
    return min(frac, 1.0 - frac)


def collect_near_misses(brick_list: list) -> list:
    """Score and rank a list of Euler bricks by near-miss quality.

    Args:
        brick_list: List of dicts with "edges" key [a, b, c].

    Returns:
        Sorted list of near-miss records (closest first).
    """
    scored = []
    for brick in brick_list:
        edges = brick["edges"]
        a, b, c = edges[0], edges[1], edges[2]
        cuboid = Cuboid(a, b, c)

        if not cuboid.is_euler_brick():
            continue

        sd = cuboid.space_diagonal()
        gap = near_miss_score(a, b, c)

        scored.append({
            "edges": edges,
            "face_diagonals": [
                math.isqrt(cuboid.face_diagonal_ab_sq),
                math.isqrt(cuboid.face_diagonal_ac_sq),
                math.isqrt(cuboid.face_diagonal_bc_sq),
            ],
            "space_diagonal": sd,
            "space_diagonal_sq": cuboid.space_diagonal_sq,
            "gap": gap,
            "source": brick.get("family", brick.get("source", "unknown")),
        })

    scored.sort(key=lambda x: x["gap"])
    return scored


def analyze_distribution(near_misses: list) -> dict:
    """Statistical analysis of near-miss score distribution.

    Tests whether the distribution is consistent with uniform random
    on [0, 0.5] or shows systematic avoidance of zero.
    """
    if not near_misses:
        return {"error": "No near-misses to analyze"}

    gaps = [nm["gap"] for nm in near_misses]
    n = len(gaps)

    # Basic statistics
    mean_gap = sum(gaps) / n
    var_gap = sum((g - mean_gap) ** 2 for g in gaps) / n
    std_gap = math.sqrt(var_gap)
    min_gap = min(gaps)
    max_gap = max(gaps)
    median_gap = sorted(gaps)[n // 2]

    # Under uniform distribution on [0, 0.5]:
    # Expected mean = 0.25, variance = 1/48 ≈ 0.0208, std ≈ 0.1443
    expected_mean = 0.25
    expected_std = math.sqrt(1.0 / 48.0)

    # Bin into 10 equal-width bins on [0, 0.5]
    num_bins = 10
    bin_width = 0.5 / num_bins
    bins = [0] * num_bins
    for g in gaps:
        bin_idx = min(int(g / bin_width), num_bins - 1)
        bins[bin_idx] += 1

    # Chi-squared test against uniform
    expected_per_bin = n / num_bins
    chi_sq = sum((obs - expected_per_bin) ** 2 / expected_per_bin for obs in bins)

    # Count how many are very close (gap < 0.01)
    very_close = sum(1 for g in gaps if g < 0.01)

    return {
        "n": n,
        "mean": mean_gap,
        "std": std_gap,
        "median": median_gap,
        "min": min_gap,
        "max": max_gap,
        "expected_mean_uniform": expected_mean,
        "expected_std_uniform": expected_std,
        "mean_deviation_from_uniform": abs(mean_gap - expected_mean),
        "histogram_bins": bins,
        "bin_width": bin_width,
        "chi_squared": chi_sq,
        "chi_squared_dof": num_bins - 1,
        "very_close_count": very_close,
        "very_close_fraction": very_close / n if n > 0 else 0,
        "interpretation": (
            "consistent_with_random" if chi_sq < 16.9  # chi2(9, 0.05)
            else "deviates_from_uniform"
        ),
    }


def create_histogram(near_misses: list, output_path: str):
    """Create publication-quality histogram of near-miss scores."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    mpl.rcParams.update({
        'figure.figsize': (8, 5),
        'figure.dpi': 300,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.8,
        'font.family': 'serif',
        'grid.alpha': 0.3,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
    })

    gaps = [nm["gap"] for nm in near_misses]

    fig, ax = plt.subplots(figsize=(8, 5))
    palette = sns.color_palette("deep")

    ax.hist(gaps, bins=20, range=(0, 0.5), color=palette[0], edgecolor='white',
            linewidth=0.5, alpha=0.8, label=f'Euler bricks (n={len(gaps)})')

    # Add uniform reference line
    expected = len(gaps) / 20
    ax.axhline(y=expected, color=palette[3], linestyle='--', linewidth=1.5,
               alpha=0.7, label=f'Uniform expectation ({expected:.1f})')

    ax.set_xlabel('Near-Miss Score (min fractional part of space diagonal)')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Space Diagonal Near-Miss Scores for Euler Bricks')
    ax.legend(frameon=True, loc='upper right')

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.savefig(output_path.replace('.png', '.pdf'))
    plt.close()


def main():
    # Load Euler bricks from all sources
    all_bricks = []

    # From brute force
    bf_path = os.path.join("results", "baseline_benchmarks.json")
    if os.path.exists(bf_path):
        with open(bf_path) as f:
            data = json.load(f)
            all_bricks.extend(data.get("euler_bricks", []))

    # From parametric families
    param_path = os.path.join("results", "parametric_bricks.json")
    if os.path.exists(param_path):
        with open(param_path) as f:
            data = json.load(f)
            all_bricks.extend(data.get("parametric_bricks", []))

    if not all_bricks:
        print("No Euler bricks found in results/. Run brute_force.py and parametric.py first.")
        return

    near_misses = collect_near_misses(all_bricks)
    stats = analyze_distribution(near_misses)

    print(f"Near-miss analysis: {stats['n']} Euler bricks")
    print(f"  Mean gap: {stats['mean']:.6f} (expected uniform: {stats['expected_mean_uniform']:.6f})")
    print(f"  Std gap: {stats['std']:.6f} (expected uniform: {stats['expected_std_uniform']:.6f})")
    print(f"  Min gap: {stats['min']:.10f}")
    print(f"  Chi-squared: {stats['chi_squared']:.2f} (dof={stats['chi_squared_dof']})")
    print(f"  Interpretation: {stats['interpretation']}")

    # Save
    os.makedirs("results", exist_ok=True)
    with open("results/near_miss_results.json", "w") as f:
        json.dump({"near_misses": near_misses[:50], "statistics": stats}, f, indent=2)

    create_histogram(near_misses, "figures/near_miss_distribution.png")
    print("Histogram saved to figures/near_miss_distribution.png")


if __name__ == "__main__":
    main()
