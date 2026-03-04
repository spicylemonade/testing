#!/usr/bin/env python3
"""Generate publication-quality visualizations of the best BB(6) candidate.

Produces:
  - figures/spacetime_diagram.png / .pdf
  - figures/state_transition_graph.png / .pdf
  - figures/tape_growth.png / .pdf
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np

from src.tm_simulator import TuringMachine


# Publication-quality rcParams
plt.rcParams.update({
    "font.size": 11,
    "font.family": "serif",
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

BEST_CANDIDATE = "1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE"
STATE_NAMES = list("ABCDEFZ")
STATE_COLORS = sns.color_palette("deep", 7)


def parse_notation(notation):
    """Parse compact notation into {(state_idx, symbol): (write, dir, next_state_idx)} dict."""
    states_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'Z': -1}
    dir_map = {'L': -1, 'R': 1}
    table = {}
    groups = notation.split('_')
    for state_idx, group in enumerate(groups):
        for sym in range(2):
            entry = group[sym * 3:(sym + 1) * 3]
            write = int(entry[0])
            direction = dir_map[entry[1]]
            next_state = states_map[entry[2]]
            table[(state_idx, sym)] = (write, direction, next_state)
    return table


def simulate_with_history(notation, max_steps=3000):
    """Simulate TM recording full history for visualization."""
    table = parse_notation(notation)
    tape = {}
    head = 0
    state = 0
    
    history = []
    tape_positions = set()
    head_positions = []
    state_sequence = []
    tape_ones_over_time = []
    tape_extent = []
    
    for step in range(max_steps):
        sym = tape.get(head, 0)
        tape_positions.add(head)
        head_positions.append(head)
        state_sequence.append(state)
        tape_ones_over_time.append(sum(1 for v in tape.values() if v == 1))
        
        positions = list(tape_positions)
        tape_extent.append((min(positions) if positions else 0, max(positions) if positions else 0))
        
        history.append({
            "step": step,
            "head": head,
            "state": state,
            "symbol": sym,
            "tape": dict(tape),
        })
        
        key = (state, sym)
        if key not in table:
            break
        
        write, direction, next_state = table[key]
        tape[head] = write
        
        if next_state == -1:  # HALT
            tape_ones_over_time.append(sum(1 for v in tape.values() if v == 1))
            head_positions.append(head)
            state_sequence.append(-1)
            break
        
        head += direction
        state = next_state
    
    return {
        "history": history,
        "head_positions": head_positions,
        "state_sequence": state_sequence,
        "tape_ones": tape_ones_over_time,
        "tape_extent": tape_extent,
        "final_tape": tape,
        "total_steps": len(history),
    }


def plot_spacetime_diagram(sim_data, max_display_steps=500):
    """Space-time diagram: x=tape position, y=step, color=cell value, marker=head."""
    history = sim_data["history"][:max_display_steps]
    
    if not history:
        return
    
    # Determine tape bounds
    all_heads = [h["head"] for h in history]
    min_pos = min(all_heads) - 2
    max_pos = max(all_heads) + 2
    width = max_pos - min_pos + 1
    n_steps = len(history)
    
    # Build grid
    grid = np.zeros((n_steps, width))
    head_grid = np.full((n_steps, width), -1)  # -1 = no head
    
    tape = {}
    for i, h in enumerate(history):
        # Update tape from history
        tape = h["tape"]
        for pos in range(min_pos, max_pos + 1):
            grid[i, pos - min_pos] = tape.get(pos, 0)
        head_grid[i, h["head"] - min_pos] = h["state"]
    
    fig, ax = plt.subplots(figsize=(min(14, width * 0.06 + 2), min(10, n_steps * 0.02 + 1)))
    
    # Show tape as background
    cmap = mcolors.ListedColormap(["#f0f0f0", "#2c3e50"])
    ax.imshow(grid, aspect="auto", cmap=cmap, interpolation="nearest",
              extent=[min_pos - 0.5, max_pos + 0.5, n_steps - 0.5, -0.5])
    
    # Overlay head positions with state-colored markers
    for i, h in enumerate(history):
        if i % max(1, n_steps // 200) == 0:  # Don't overcrowd
            color = STATE_COLORS[h["state"]] if h["state"] < 7 else "red"
            ax.plot(h["head"], i, ".", color=color, markersize=1.5)
    
    ax.set_xlabel("Tape Position")
    ax.set_ylabel("Step")
    ax.set_title(f"Space-Time Diagram (first {n_steps} steps)\n{BEST_CANDIDATE}")
    
    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/spacetime_diagram.png", dpi=300)
    fig.savefig("figures/spacetime_diagram.pdf")
    plt.close(fig)
    print("Saved figures/spacetime_diagram.png and .pdf")


def plot_state_transition_graph(notation):
    """State transition diagram as a directed graph."""
    table = parse_notation(notation)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    n_states = 6
    # Position states in a circle
    angles = np.linspace(0, 2 * np.pi, n_states, endpoint=False) - np.pi / 2
    positions = {i: (np.cos(a) * 2.5, np.sin(a) * 2.5) for i, a in enumerate(angles)}
    # Add halt state at center
    positions[-1] = (0, 0)
    
    # Draw edges
    edge_counts = {}  # (from, to) -> list of labels
    for (state, sym), (write, direction, next_state) in table.items():
        key = (state, next_state)
        dir_char = "R" if direction >= 1 else "L"
        label = f"{sym}/{write}{dir_char}"
        edge_counts.setdefault(key, []).append(label)
    
    drawn_edges = set()
    for (s_from, s_to), labels in edge_counts.items():
        x1, y1 = positions[s_from]
        x2, y2 = positions[s_to]
        
        if s_from == s_to:
            # Self-loop
            angle = angles[s_from] if s_from >= 0 else 0
            loop_x = x1 + np.cos(angle) * 0.8
            loop_y = y1 + np.sin(angle) * 0.8
            ax.annotate("", xy=(x1, y1),
                       xytext=(loop_x, loop_y),
                       arrowprops=dict(arrowstyle="->", color="gray",
                                      connectionstyle="arc3,rad=0.5"))
            ax.text(loop_x, loop_y, ", ".join(labels), fontsize=7,
                   ha="center", va="center",
                   bbox=dict(boxstyle="round,pad=0.2", facecolor="lightyellow", alpha=0.8))
        else:
            # Offset for bidirectional edges
            reverse = (s_to, s_from) in drawn_edges
            rad = 0.2 if reverse else 0.1
            
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            ax.annotate("",
                       xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle="->", color="gray",
                                      connectionstyle=f"arc3,rad={rad}"))
            
            # Label
            offset_x = (y2 - y1) * 0.08 * (1 if not reverse else -1)
            offset_y = -(x2 - x1) * 0.08 * (1 if not reverse else -1)
            ax.text(mid_x + offset_x, mid_y + offset_y, ", ".join(labels),
                   fontsize=7, ha="center", va="center",
                   bbox=dict(boxstyle="round,pad=0.2", facecolor="lightyellow", alpha=0.8))
        
        drawn_edges.add((s_from, s_to))
    
    # Draw nodes
    for state_id, (x, y) in positions.items():
        if state_id == -1:
            color = "#e74c3c"
            label = "HALT"
        else:
            color = STATE_COLORS[state_id]
            label = STATE_NAMES[state_id]
        
        circle = plt.Circle((x, y), 0.4, color=color, ec="black", linewidth=2, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=12,
               fontweight="bold", color="white" if state_id != -1 else "white", zorder=6)
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"State Transition Graph\n{BEST_CANDIDATE}", fontsize=12)
    
    fig.savefig("figures/state_transition_graph.png", dpi=300)
    fig.savefig("figures/state_transition_graph.pdf")
    plt.close(fig)
    print("Saved figures/state_transition_graph.png and .pdf")


def plot_tape_growth(sim_data):
    """Tape growth over time: ones count and tape extent."""
    sns.set_theme(style="whitegrid")
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    
    steps = range(len(sim_data["tape_ones"]))
    
    # Panel 1: Number of 1s over time
    ax = axes[0]
    ax.plot(steps, sim_data["tape_ones"], color=STATE_COLORS[0], linewidth=1)
    ax.fill_between(steps, sim_data["tape_ones"], alpha=0.2, color=STATE_COLORS[0])
    ax.set_ylabel("Number of 1s on Tape")
    ax.set_title(f"Tape Growth Over Time — {BEST_CANDIDATE}")
    ax.axhline(y=80, color="red", linestyle="--", alpha=0.5, label="Final sigma=80")
    ax.legend()
    
    # Panel 2: Tape extent (head position range)
    ax = axes[1]
    head_pos = sim_data["head_positions"][:len(steps)]
    # Pad if needed
    while len(head_pos) < len(steps):
        head_pos.append(head_pos[-1])
    ax.plot(range(len(head_pos)), head_pos, color=STATE_COLORS[2], linewidth=0.5, alpha=0.7)
    ax.set_xlabel("Step")
    ax.set_ylabel("Head Position")
    ax.set_title("Tape Head Position Over Time")
    
    plt.tight_layout()
    fig.savefig("figures/tape_growth.png", dpi=300)
    fig.savefig("figures/tape_growth.pdf")
    plt.close(fig)
    print("Saved figures/tape_growth.png and .pdf")


def main():
    print("Simulating best candidate for visualization...")
    sim_data = simulate_with_history(BEST_CANDIDATE, max_steps=3000)
    print(f"  Simulated {sim_data['total_steps']} steps")
    
    print("\nGenerating space-time diagram...")
    plot_spacetime_diagram(sim_data, max_display_steps=500)
    
    print("\nGenerating state transition graph...")
    plot_state_transition_graph(BEST_CANDIDATE)
    
    print("\nGenerating tape growth plot...")
    plot_tape_growth(sim_data)
    
    print("\nAll visualizations complete.")


if __name__ == "__main__":
    main()
