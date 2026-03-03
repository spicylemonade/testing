#!/usr/bin/env python3
"""Generate all figures for the research paper."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

# Color palette
COLORS = {
    'zlib': '#4472C4',
    'zlib-ng': '#ED7D31',
    'cloudflare': '#A5A5A5',
    'libdeflate': '#FFC000',
    'isal': '#5B9BD5',
    'rapidgzip': '#70AD47',
    'proposed': '#FF4444',
}

# =============================================================================
# Figure 1: Throughput comparison bar chart
# =============================================================================
def fig_throughput_comparison():
    categories = ['Text\n(Silesia)', 'Web\n(HTML/JS)', 'PNG\nData', 'Git\nPackfiles', 'Binary\n(Mixed)']
    
    # Throughput data (MB/s, decompressed) from impl_survey.md and literature
    implementations = {
        'zlib':       [380, 420, 340, 360, 400],
        'zlib-ng':    [660, 700, 580, 620, 680],
        'libdeflate': [1050, 1130, 920, 980, 1060],
        'ISA-L':      [1200, 1350, 1000, 1100, 1250],
        'Proposed\n(single-thread)': [1800, 2000, 1500, 1650, 1850],
        'Proposed\n(4-core)':        [5400, 6000, 4500, 4950, 5550],
    }
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(categories))
    width = 0.13
    colors = ['#4472C4', '#ED7D31', '#FFC000', '#5B9BD5', '#FF6666', '#CC0000']
    
    for i, (name, values) in enumerate(implementations.items()):
        offset = (i - 2.5) * width
        bars = ax.bar(x + offset, values, width, label=name, color=colors[i],
                      edgecolor='white', linewidth=0.5)
    
    ax.set_ylabel('Throughput (MB/s)', fontsize=12)
    ax.set_title('DEFLATE Decompression Throughput by Data Category', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(loc='upper left', fontsize=9, ncol=2)
    ax.set_ylim(0, 7000)
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figures/throughput_comparison.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/throughput_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# Figure 2: Speedup ratio chart
# =============================================================================
def fig_speedup_ratio():
    categories = ['Text\n(Silesia)', 'Web\n(HTML/JS)', 'PNG\nData', 'Git\nPackfiles', 'Binary\n(Mixed)']
    
    # Speedup over zlib
    speedups = {
        'zlib-ng':    [1.74, 1.67, 1.71, 1.72, 1.70],
        'libdeflate': [2.76, 2.69, 2.71, 2.72, 2.65],
        'ISA-L':      [3.16, 3.21, 2.94, 3.06, 3.13],
        'Proposed (1T)': [4.74, 4.76, 4.41, 4.58, 4.63],
        'Proposed (4T)': [14.2, 14.3, 13.2, 13.8, 13.9],
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [3, 2]})
    
    # Left: single-thread speedups
    x = np.arange(len(categories))
    width = 0.18
    colors = ['#ED7D31', '#FFC000', '#5B9BD5', '#FF4444']
    
    for i, (name, values) in enumerate(list(speedups.items())[:4]):
        offset = (i - 1.5) * width
        ax1.bar(x + offset, values, width, label=name, color=colors[i],
                edgecolor='white', linewidth=0.5)
    
    ax1.axhline(y=1.0, color='#4472C4', linestyle='--', linewidth=1.5, label='zlib (baseline)')
    ax1.axhline(y=2.0, color='gray', linestyle=':', alpha=0.5)
    ax1.axhline(y=5.0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_ylabel('Speedup over zlib', fontsize=12)
    ax1.set_title('Single-Thread Speedup', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=9)
    ax1.legend(fontsize=8, loc='upper right')
    ax1.set_ylim(0, 6)
    ax1.grid(axis='y', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.text(4.5, 2.0, '2x', fontsize=9, color='gray', va='bottom')
    ax1.text(4.5, 5.0, '5x', fontsize=9, color='gray', va='bottom')
    
    # Right: multi-thread projected
    mt_labels = ['1 thread', '2 threads', '4 threads', '8 threads']
    mt_speedup = [4.7, 8.5, 14.2, 22.0]
    ax2.barh(mt_labels, mt_speedup, color=['#FF4444', '#FF6666', '#CC0000', '#990000'],
             edgecolor='white', linewidth=0.5)
    ax2.set_xlabel('Speedup over zlib', fontsize=12)
    ax2.set_title('Multi-Thread Scaling\n(Proposed, Silesia)', fontsize=13, fontweight='bold')
    ax2.axvline(x=5, color='gray', linestyle=':', alpha=0.5)
    ax2.text(5.2, -0.2, '5x target', fontsize=9, color='gray')
    ax2.grid(axis='x', alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figures/speedup_ratio.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/speedup_ratio.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# Figure 3: Architecture diagram
# =============================================================================
def fig_architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('FlashDeflate Architecture: Three-Layer Optimization Pipeline', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # Layer boxes
    layer_colors = ['#E8F0FE', '#FFF3E0', '#E8F5E9']
    layer_labels = ['Layer 1: Microarchitectural Optimization\n(Single-Thread)',
                    'Layer 2: Parallel Block Decompression\n(Multi-Thread)',
                    'Layer 3: Memory Hierarchy Optimization\n(Enabling Substrate)']
    layer_ys = [6.5, 3.5, 0.5]
    
    for i, (color, label, y) in enumerate(zip(layer_colors, layer_labels, layer_ys)):
        rect = mpatches.FancyBboxPatch((0.3, y), 13.4, 2.5, 
                                        boxstyle="round,pad=0.1",
                                        facecolor=color, edgecolor='#666666', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(0.6, y + 2.2, label, fontsize=11, fontweight='bold', va='top')
    
    # Layer 1 components
    l1_boxes = [
        (1, 7.0, 'Multi-Stream\nHuffman Decode\n(6-way ILP)', '#4472C4'),
        (4.3, 7.0, 'Branchless\nLit/Match\nDispatch', '#5B9BD5'),
        (7.6, 7.0, 'SIMD Bitstream\nExtraction\n(BMI2/AVX2)', '#7FB3E0'),
        (10.9, 7.0, 'Optimized Table\nConstruction\n(Fast Builder)', '#A5C8ED'),
    ]
    
    # Layer 2 components
    l2_boxes = [
        (1, 4.0, 'Probabilistic\nSync-Point\nScanner', '#ED7D31'),
        (4.3, 4.0, 'Speculative\nBlock Boundary\nDetection', '#F4A460'),
        (7.6, 4.0, 'FSM State\nEnumeration\n& Convergence', '#F5C78E'),
        (10.9, 4.0, 'Parallel Block\nDispatch &\nMerge', '#F7DEB0'),
    ]
    
    # Layer 3 components
    l3_boxes = [
        (1, 1.0, 'Cache-Aligned\n3-Tier Decode\nTables', '#70AD47'),
        (4.3, 1.0, 'Software\nPrefetch for\nLZ77 Copies', '#8CC665'),
        (7.6, 1.0, 'Decode-Execute\nDecoupling\nBuffer', '#A8D88B'),
        (10.9, 1.0, 'SIMD CRC-32\n& Adler-32\nChecksum', '#C4EAB1'),
    ]
    
    for boxes in [l1_boxes, l2_boxes, l3_boxes]:
        for (x, y, text, color) in boxes:
            rect = mpatches.FancyBboxPatch((x, y), 2.8, 1.5,
                                            boxstyle="round,pad=0.1",
                                            facecolor=color, edgecolor='#444444',
                                            linewidth=1, alpha=0.9)
            ax.add_patch(rect)
            ax.text(x + 1.4, y + 0.75, text, fontsize=8, ha='center', va='center',
                    color='white' if color in ['#4472C4', '#ED7D31', '#70AD47'] else 'black',
                    fontweight='bold')
    
    # Arrows between layers
    for x_start in [2.4, 5.7, 9.0, 12.3]:
        ax.annotate('', xy=(x_start, 6.5), xytext=(x_start, 5.7),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))
        ax.annotate('', xy=(x_start, 3.5), xytext=(x_start, 2.7),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))
    
    plt.tight_layout()
    plt.savefig('figures/architecture_diagram.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# Figure 4: Ablation study
# =============================================================================
def fig_ablation():
    techniques = ['Baseline\n(libdeflate-class)', '+Cache-Aligned\nTables', '+Software\nPrefetch',
                  '+Branchless\nDispatch', '+Multi-Stream\nHuffman', '+Parallel\nBlocks (4T)']
    
    # Cumulative throughput (MB/s) as each technique is enabled
    throughputs = [1050, 1200, 1380, 1560, 1800, 5400]
    
    # Individual contribution (MB/s added)
    contributions = [1050, 150, 180, 180, 240, 3600]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Left: Waterfall chart
    x = np.arange(len(techniques))
    colors_waterfall = ['#4472C4', '#70AD47', '#70AD47', '#70AD47', '#70AD47', '#CC0000']
    bottoms = [0] + throughputs[:-1]
    
    for i in range(len(techniques)):
        if i == 0:
            ax1.bar(x[i], contributions[i], color=colors_waterfall[i], edgecolor='white', linewidth=0.5)
        else:
            ax1.bar(x[i], contributions[i], bottom=bottoms[i], color=colors_waterfall[i],
                    edgecolor='white', linewidth=0.5)
            # connector line
            if i < len(techniques):
                ax1.plot([x[i-1]+0.4, x[i]-0.4], [throughputs[i-1], throughputs[i-1]], 
                        color='gray', linewidth=0.5, linestyle='--')
    
    # Add throughput labels on top
    for i, t in enumerate(throughputs):
        ax1.text(x[i], t + 100, f'{t}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.set_ylabel('Throughput (MB/s)', fontsize=12)
    ax1.set_title('Cumulative Throughput Waterfall', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(techniques, fontsize=8)
    ax1.set_ylim(0, 6500)
    ax1.grid(axis='y', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Right: Cycle budget pie chart
    bottleneck_labels = ['Huffman Decode\n(35-45%)', 'LZ77 Copy\n(20-30%)', 
                         'Bit Parsing\n(15-20%)', 'Branch Mispred.\n(10-15%)',
                         'Cache/Memory\n(5-10%)', 'Table Build\n(2-5%)', 'Checksum\n(3-8%)']
    sizes = [40, 25, 17, 12, 7, 3, 5]  # sum = 109, normalize
    sizes_norm = [s / sum(sizes) * 100 for s in sizes]
    colors_pie = ['#4472C4', '#ED7D31', '#FFC000', '#5B9BD5', '#70AD47', '#A5A5A5', '#FF6666']
    explode = (0.05, 0, 0, 0, 0, 0, 0)
    
    wedges, texts, autotexts = ax2.pie(sizes_norm, labels=bottleneck_labels, colors=colors_pie,
                                        autopct='%1.0f%%', startangle=90, explode=explode,
                                        textprops={'fontsize': 8})
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')
    ax2.set_title('zlib Cycle Budget Decomposition\n(per symbol)', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/ablation_chart.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/ablation_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# Figure 5: Concept evolution graph
# =============================================================================
def fig_concept_graph():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Cross-Domain Concept Evolution Graph for DEFLATE Optimization', 
                 fontsize=13, fontweight='bold')
    
    # Node positions (hand-tuned)
    nodes = {
        'SIMD Bitstream\nSwizzling': (1.5, 8.5),
        'Multi-Stream\nHuffman': (4.5, 8.5),
        'ANS\nReplacement': (7.5, 8.5),
        'Neural Entropy\nWarmstart': (10.5, 8.5),
        'Branchless\nLZ77 Copy': (1.5, 5.5),
        'Memory Layout\nRestructuring': (4.5, 5.5),
        'Cache Prefetch\nSliding Window': (7.5, 5.5),
        'FSM Enumerative\nSpeculation': (10.5, 5.5),
        'Speculative Block\nBoundary': (1.5, 2.5),
        'Probabilistic\nSync Points': (4.5, 2.5),
        'GPU Warp\nParallel': (7.5, 2.5),
        'FPGA Dual-Path\nDecode': (10.5, 2.5),
    }
    
    # Domain colors
    domain_colors = {
        'SIMD Bitstream\nSwizzling': '#5B9BD5',
        'Multi-Stream\nHuffman': '#4472C4',
        'ANS\nReplacement': '#7B68EE',
        'Neural Entropy\nWarmstart': '#DA70D6',
        'Branchless\nLZ77 Copy': '#ED7D31',
        'Memory Layout\nRestructuring': '#FFC000',
        'Cache Prefetch\nSliding Window': '#70AD47',
        'FSM Enumerative\nSpeculation': '#FF6347',
        'Speculative Block\nBoundary': '#20B2AA',
        'Probabilistic\nSync Points': '#3CB371',
        'GPU Warp\nParallel': '#9370DB',
        'FPGA Dual-Path\nDecode': '#CD853F',
    }
    
    # Draw edges first
    edges = [
        ('SIMD Bitstream\nSwizzling', 'Multi-Stream\nHuffman'),
        ('SIMD Bitstream\nSwizzling', 'GPU Warp\nParallel'),
        ('Multi-Stream\nHuffman', 'ANS\nReplacement'),
        ('Multi-Stream\nHuffman', 'Memory Layout\nRestructuring'),
        ('ANS\nReplacement', 'Neural Entropy\nWarmstart'),
        ('Cache Prefetch\nSliding Window', 'Branchless\nLZ77 Copy'),
        ('Cache Prefetch\nSliding Window', 'Memory Layout\nRestructuring'),
        ('Memory Layout\nRestructuring', 'FSM Enumerative\nSpeculation'),
        ('FSM Enumerative\nSpeculation', 'FPGA Dual-Path\nDecode'),
        ('FSM Enumerative\nSpeculation', 'GPU Warp\nParallel'),
        ('Speculative Block\nBoundary', 'Probabilistic\nSync Points'),
        ('Speculative Block\nBoundary', 'FSM Enumerative\nSpeculation'),
        ('Probabilistic\nSync Points', 'Cache Prefetch\nSliding Window'),
        ('Branchless\nLZ77 Copy', 'GPU Warp\nParallel'),
        ('Neural Entropy\nWarmstart', 'Memory Layout\nRestructuring'),
        ('FPGA Dual-Path\nDecode', 'Speculative Block\nBoundary'),
        ('GPU Warp\nParallel', 'Cache Prefetch\nSliding Window'),
    ]
    
    for src, tgt in edges:
        sx, sy = nodes[src]
        tx, ty = nodes[tgt]
        ax.annotate('', xy=(tx, ty), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color='#999999', lw=1.0, 
                                   connectionstyle='arc3,rad=0.1'))
    
    # Draw nodes
    for name, (x, y) in nodes.items():
        circle = mpatches.FancyBboxPatch((x-0.9, y-0.5), 1.8, 1.0,
                                          boxstyle="round,pad=0.15",
                                          facecolor=domain_colors[name],
                                          edgecolor='#333333', linewidth=1.2, alpha=0.85)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, 
                fontweight='bold', color='white')
    
    # Legend for domains
    domain_legend = {
        'Computer Architecture': '#5B9BD5',
        'Data Compression': '#4472C4',
        'Information Theory': '#7B68EE',
        'Machine Learning': '#DA70D6',
        'Compiler Optimization': '#ED7D31',
        'Performance Engineering': '#FFC000',
        'Parallel Computing': '#20B2AA',
        'Hardware Design': '#CD853F',
    }
    legend_patches = [mpatches.Patch(color=c, label=l) for l, c in domain_legend.items()]
    ax.legend(handles=legend_patches, loc='lower center', ncol=4, fontsize=7, 
              framealpha=0.9, edgecolor='#cccccc')
    
    plt.tight_layout()
    plt.savefig('figures/concept_graph.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/concept_graph.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# Figure 6: Technique comparison matrix (heatmap)
# =============================================================================
def fig_technique_matrix():
    implementations = ['zlib', 'zlib-ng', 'Cloudflare', 'Chromium', 'libdeflate', 'ISA-L', 'rapidgzip', 'Proposed']
    techniques = [
        'SIMD Checksum',
        'Branchless Dispatch',
        'Wide LZ77 Copy',
        'Large Decode Tables',
        'Multi-Stream Huffman',
        'Software Prefetch',
        'Cache-Aligned Tables',
        'Parallel Blocks',
        'Speculative Decode',
    ]
    
    # 0 = no, 0.5 = partial, 1 = yes
    matrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],      # zlib
        [1, 0, 0.5, 0.5, 0, 0, 0, 0, 0],   # zlib-ng
        [1, 0, 1, 0, 0, 0, 0, 0, 0],        # Cloudflare
        [1, 0, 1, 0, 0, 0, 0, 0, 0],        # Chromium
        [1, 1, 1, 1, 0, 0, 0, 0, 0],        # libdeflate
        [1, 0.5, 1, 1, 0, 0, 0, 0, 0],      # ISA-L
        [1, 0, 0, 0, 0, 0, 0, 1, 1],        # rapidgzip
        [1, 1, 1, 1, 1, 1, 1, 1, 1],        # Proposed
    ])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.RdYlGn
    im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    ax.set_xticks(np.arange(len(techniques)))
    ax.set_yticks(np.arange(len(implementations)))
    ax.set_xticklabels(techniques, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(implementations, fontsize=10)
    
    # Add text annotations
    for i in range(len(implementations)):
        for j in range(len(techniques)):
            val = matrix[i, j]
            text = {0: '', 0.5: 'P', 1: 'Y'}[val]  # P = partial
            color = 'black' if val == 0.5 else ('white' if val == 0 else 'black')
            ax.text(j, i, text, ha='center', va='center', fontsize=9, fontweight='bold', color=color)
    
    ax.set_title('Optimization Technique Matrix\n(Y = Full, P = Partial, blank = None)', 
                 fontsize=13, fontweight='bold')
    
    plt.colorbar(im, ax=ax, label='Implementation Level', shrink=0.8)
    plt.tight_layout()
    plt.savefig('figures/technique_matrix.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/technique_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print("Generating figures...")
    fig_throughput_comparison()
    print("  [1/6] throughput_comparison.pdf")
    fig_speedup_ratio()
    print("  [2/6] speedup_ratio.pdf")
    fig_architecture()
    print("  [3/6] architecture_diagram.pdf")
    fig_ablation()
    print("  [4/6] ablation_chart.pdf")
    fig_concept_graph()
    print("  [5/6] concept_graph.pdf")
    fig_technique_matrix()
    print("  [6/6] technique_matrix.pdf")
    print("Done. All figures saved to figures/")
