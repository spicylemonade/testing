#!/usr/bin/env python3
"""Generate figure assets and lightweight paper-analysis tables."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / 'figures'
DATA_DIR = FIG_DIR / 'data'
SRC_DIR = FIG_DIR / 'src'
PDF_DIR = FIG_DIR / 'pdf'
PNG_DIR = FIG_DIR / 'png'


def load_json(path: str):
    with (ROOT / path).open() as fh:
        return json.load(fh)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


def compile_figure(name: str) -> None:
    tex_path = SRC_DIR / f'{name}.tex'
    subprocess.run(
        [
            'pdflatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            f'-output-directory={PDF_DIR}',
            str(tex_path),
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    pdf_path = PDF_DIR / f'{name}.pdf'
    png_path = PNG_DIR / f'{name}.png'
    subprocess.run(
        [
            'mutool', 'draw', '-q', '-r', '600', '-o', str(png_path), str(pdf_path), '1'
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def figure_preamble() -> str:
    return r'''
\documentclass[tikz,border=6pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{mathpazo}
\usepackage{amsmath,amssymb,booktabs}
\usepackage{xcolor}
\usepackage{pagecolor}
\usepackage{pgfplots}
\usepackage{pgfplotstable}
\usepgfplotslibrary{groupplots}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,backgrounds,calc,decorations.pathreplacing,fit,matrix,positioning,shapes.geometric}
\pgfplotsset{compat=1.18}
\definecolor{ink}{HTML}{1F2937}
\definecolor{teal}{HTML}{1D7874}
\definecolor{rust}{HTML}{C75C36}
\definecolor{gold}{HTML}{D9A441}
\definecolor{sage}{HTML}{6C9A8B}
\definecolor{berry}{HTML}{9E2A2B}
\definecolor{sand}{HTML}{F3E9D2}
\definecolor{mist}{HTML}{E7EEF3}
\definecolor{charcoal}{HTML}{3C4858}
\pagecolor{white}
\color{ink}
\pgfplotsset{paperaxis/.style={
    font=\small,
    tick label style={font=\small},
    label style={font=\small},
    title style={font=\small\bfseries},
    every axis plot/.append style={line width=1.2pt},
    grid=both,
    major grid style={draw=mist},
    minor grid style={draw=mist!60},
    grid style={line width=0.2pt},
    axis line style={draw=charcoal},
    tick style={draw=charcoal},
    legend style={draw=none, fill=white, font=\small, row sep=2pt, column sep=4pt}
}}
'''


def write_frontier_structure(prefix_table: list[list[int]]) -> None:
    matrix_rows = []
    for i, row in enumerate(prefix_table):
        formatted = []
        for j, value in enumerate(row):
            if i == 0 or j == 0:
                formatted.append(r'\textcolor{teal}{\bfseries %s}' % value)
            else:
                formatted.append(str(value))
        matrix_rows.append(' & '.join(formatted) + r' \\')
    matrix_body = '\n'.join(matrix_rows)
    tex = figure_preamble() + rf'''
\begin{{document}}
\begin{{tikzpicture}}[font=\small]
  \fill[sand] (-0.5,-6.7) rectangle (17.1,6.1);
  \node[anchor=west,font=\bfseries\large] at (-0.1,5.5) {{Prime-separator frontiers and the interleaving theorem}};

  \node[anchor=west,font=\bfseries] at (0.0,4.9) {{A. Published $5\times 11$ prefix}};
  \matrix[matrix of nodes,
          nodes={{draw=white, minimum width=0.82cm, minimum height=0.58cm, anchor=center}},
          column sep=1pt,row sep=1pt,
          nodes in empty cells,
          anchor=north west] (tbl) at (0.0,4.55) {{
{matrix_body}
  }};
  \node[anchor=west, align=left, text width=6.2cm] at (0.0,-1.9) {{
    Border terms are shown in teal. Every interior entry is a product $b_i a_j$, so the
    finite square is completely determined by the first row and first column.
  }};

  \node[anchor=west,font=\bfseries] at (8.2,4.9) {{B. One update step}};
  \node[draw=teal, rounded corners=4pt, fill=white, minimum width=3.4cm, minimum height=1.1cm, align=center] (pn) at (10.2,3.8) {{$P_n = A_n B_n$\\$[1,b_n]\subseteq P_n$}};
  \node[draw=rust, rounded corners=4pt, fill=white, minimum width=3.2cm, minimum height=1.0cm, align=center] (an) at (14.0,3.8) {{$a_{{n+1}}=\mathrm{{mex}}(P_n)$}};
  \node[draw=gold, rounded corners=4pt, fill=white, minimum width=3.2cm, minimum height=1.0cm, align=center] (bn) at (14.0,1.9) {{$b_{{n+1}}=\mathrm{{mex}}(P_n\cup\{{a_{{n+1}}\}})$}};
  \node[draw=sage, rounded corners=4pt, fill=white, minimum width=3.6cm, minimum height=1.15cm, align=center] (upd) at (10.2,0.9) {{append $a_{{n+1}}$ and $b_{{n+1}}$\\mark new products}};
  \draw[-{{Latex[length=3mm]}}, thick, charcoal] (pn.east) -- (an.west);
  \draw[-{{Latex[length=3mm]}}, thick, charcoal] (an.south) -- (bn.north);
  \draw[-{{Latex[length=3mm]}}, thick, charcoal] (bn.west) -- (upd.east);
  \draw[-{{Latex[length=3mm]}}, thick, charcoal] (upd.north) -- ++(0,0.75) -| (pn.south);

  \node[anchor=west,font=\bfseries] at (8.2,-0.1) {{C. Proven order of the borders}};
  \draw[charcoal, line width=0.8pt] (8.5,-1.0) -- (16.2,-1.0);
  \foreach \x/\lab/\col in {{9.1/{{$a_n$}}/teal, 10.6/{{$b_n$}}/gold, 12.8/{{$a_{{n+1}}$}}/rust, 14.9/{{$b_{{n+1}}$}}/sage}} {{
    \draw[\col, line width=1.4pt] (\x,-0.82) -- (\x,-1.18);
    \node[anchor=north, text=\col] at (\x,-1.24) {{\lab}};
  }}
  \draw[decorate, decoration={{brace, amplitude=5pt}}, teal] (10.6,-1.55) -- node[below=6pt, align=center, text width=3.0cm] {{every row gap contains\\exactly one column border term}} (12.8,-1.55);

  \node[anchor=west, align=left, text width=7.7cm] at (8.3,-3.1) {{
    The key inductive invariant is the frontier coverage statement $[1,b_n]\subseteq P_n$.
    It forces strict interleaving:
    $a_n < b_n < a_{{n+1}} < b_{{n+1}}$ for every $n\ge 2$.
    The empirically observed axis-1 marker therefore has a formal explanation:
    the unique border term inside the row gap $(a_n,a_{{n+1}})$ is always $b_n$ itself.
  }};
\end{{tikzpicture}}
\end{{document}}
'''
    write_text(SRC_DIR / 'frontier_structure.tex', tex)


def write_record_gap_timeline() -> None:
    tex = figure_preamble() + r'''
\begin{document}
\begin{tikzpicture}
\begin{axis}[
  paperaxis,
  width=16cm,
  height=9cm,
  xmode=log,
  log basis x=10,
  xlabel={step $n$},
  ylabel={record gap $a_{n+1}-a_n$},
  ymin=0,
  ymax=33,
  xmin=1,
  xmax=1100000,
  legend pos=north west,
  title={Record-gap growth through $10^6$ steps}
]
  \addplot+[only marks, mark=*, mark size=2.3pt, teal]
    table[x=step,y=gap,col sep=tab] {figures/data/baseline_record_gaps.tsv};
  \addlegendentry{baseline}
  \addplot+[only marks, mark=square*, mark size=2.3pt, rust]
    table[x=step,y=gap,col sep=tab] {figures/data/row_immediate_record_gaps.tsv};
  \addlegendentry{row\_immediate}
  \addplot+[only marks, mark=triangle*, mark size=2.6pt, gold]
    table[x=step,y=gap,col sep=tab] {figures/data/column_immediate_record_gaps.tsv};
  \addlegendentry{column\_immediate}
\end{axis}
\end{tikzpicture}
\end{document}
'''
    write_text(SRC_DIR / 'record_gap_timeline.tex', tex)


def write_gap_composition() -> None:
    tex = figure_preamble() + r'''
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=1 by 3, vertical sep=1.65cm},
  paperaxis,
  width=15cm,
  height=4.2cm,
  xmin=0,
  xmax=31,
  xtick={1,5,10,15,20,25,30},
]
\nextgroupplot[
  title={Singleton-heavy coverage persists},
  ylabel={singleton share},
  ymin=0.60,
  ymax=0.95
]
  \addplot+[mark=*, mark size=2.2pt, teal]
    table[x=gap,y=singleton_share,col sep=tab] {figures/data/baseline_gap_metrics.tsv};

\nextgroupplot[
  title={Tiny factors fade while balanced witnesses rise},
  ylabel={share of skipped values},
  ymin=0,
  ymax=0.70,
  legend pos=north east
]
  \addplot+[mark=square*, mark size=2.2pt, rust]
    table[x=gap,y=tiny_share,col sep=tab] {figures/data/baseline_gap_metrics.tsv};
  \addlegendentry{min factor $\le 10$}
  \addplot+[mark=triangle*, mark size=2.4pt, gold]
    table[x=gap,y=balanced_share,col sep=tab] {figures/data/baseline_gap_metrics.tsv};
  \addlegendentry{min factor $>100$}

\nextgroupplot[
  title={Large records can be composite-only},
  xlabel={record gap},
  ylabel={skipped primes},
  ymin=-0.2,
  ymax=2.2
]
  \addplot+[ybar, bar width=6pt, fill=berry!75, draw=berry]
    table[x=gap,y=skipped_prime_count,col sep=tab] {figures/data/baseline_gap_metrics.tsv};
\end{groupplot}
\end{tikzpicture}
\end{document}
'''
    write_text(SRC_DIR / 'gap_composition.tex', tex)


def write_frontier_offsets() -> None:
    tex = figure_preamble() + r'''
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=1 by 2, vertical sep=1.7cm},
  paperaxis,
  width=15cm,
  height=5.0cm,
]
\nextgroupplot[
  title={Offset trajectory $b_n-a_n$ along the baseline run},
  xmode=log,
  log basis x=10,
  ylabel={offset},
  xmin=1,
  xmax=1000000,
  ymin=0,
  ymax=26
]
  \addplot+[teal]
    table[x=step,y=offset,col sep=tab] {figures/data/offset_samples.tsv};
  \addplot+[only marks, mark=*, mark size=1.8pt, rust]
    table[x=step,y=offset_before,col sep=tab] {figures/data/baseline_record_gaps.tsv};

\nextgroupplot[
  title={Each record gap strictly exceeds its incoming offset},
  xlabel={offset before the record},
  ylabel={record gap},
  xmin=0,
  xmax=24,
  ymin=0,
  ymax=32
]
  \addplot+[only marks, mark=diamond*, mark size=2.4pt, gold]
    table[x=offset_before,y=gap,col sep=tab] {figures/data/baseline_record_gaps.tsv};
  \addplot+[domain=0:24, samples=2, charcoal, dashed] {x};
\end{groupplot}
\end{tikzpicture}
\end{document}
'''
    write_text(SRC_DIR / 'frontier_offsets.tex', tex)


def write_hypergraph_metrics() -> None:
    tex = figure_preamble() + r'''
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=1 by 2, vertical sep=1.3cm},
  paperaxis,
  width=15cm,
  height=5.3cm,
  symbolic x coords={21,25,28,30},
  xtick=data,
]
\nextgroupplot[
  title={Full-witness pair-count histograms for late baseline records},
  xlabel={record gap},
  ylabel={skipped values},
  ymin=0,
  ymax=21,
  ybar stacked,
  bar width=11pt,
  legend columns=4,
  legend to name=pairlegend,
  legend style={/tikz/every even column/.append style={column sep=4pt}}
]
  \addplot+[fill=teal!80, draw=teal] table[x=gap,y=pair1,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{1 pair}
  \addplot+[fill=sage!90, draw=sage] table[x=gap,y=pair2,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{2 pairs}
  \addplot+[fill=gold!90, draw=gold] table[x=gap,y=pair3,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{3 pairs}
  \addplot+[fill=berry!85, draw=berry] table[x=gap,y=pair4plus,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{$\ge 4$ pairs}

\nextgroupplot[
  title={Factor reuse remains weak after full enumeration},
  xlabel={record gap},
  ylabel={count},
  ymin=0,
  ymax=46,
  ybar,
  bar width=7pt,
  enlarge x limits=0.2,
  legend pos=north west
]
  \addplot+[fill=teal!85, draw=teal] table[x=gap,y=total_full_pairs,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{total admissible pairs}
  \addplot+[fill=rust!80, draw=rust] table[x=gap,y=distinct_row_factors_used,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{distinct row factors}
  \addplot+[fill=gold!85, draw=gold] table[x=gap,y=distinct_column_factors_used,col sep=tab] {figures/data/hypergraph_metrics.tsv};
  \addlegendentry{distinct column factors}
\end{groupplot}
\node at ($(group c1r2.south)!0.5!(group c1r1.north)$) [anchor=south, yshift=-0.2cm] {\pgfplotslegendfromname{pairlegend}};
\end{tikzpicture}
\end{document}
'''
    write_text(SRC_DIR / 'hypergraph_metrics.tex', tex)


def write_variant_runtime() -> None:
    tex = figure_preamble() + r'''
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=1 by 2, vertical sep=1.3cm},
  paperaxis,
  width=15cm,
  height=5.0cm,
  symbolic x coords={baseline,row-immediate,column-immediate},
  xtick=data,
  xticklabel style={rotate=8, anchor=east},
]
\nextgroupplot[
  title={Tracked structural outputs by recurrence rule},
  xlabel={rule},
  ylabel={count},
  ymin=0,
  ymax=34,
  ybar,
  bar width=9pt,
  enlarge x limits=0.18,
  legend pos=north west
]
  \addplot+[fill=teal!85, draw=teal] table[x=label,y=largest_record_gap,col sep=tab] {figures/data/variant_summary.tsv};
  \addlegendentry{largest record gap}
  \addplot+[fill=gold!85, draw=gold] table[x=label,y=record_gap_count,col sep=tab] {figures/data/variant_summary.tsv};
  \addlegendentry{record-gap count}

\nextgroupplot[
  title={Repeated million-step runtimes (mean $\pm$ 95\% CI)},
  xlabel={rule},
  ylabel={seconds},
  ymin=8.8,
  ymax=10.5
]
  \addplot+[
    only marks,
    mark=*,
    mark size=3.0pt,
    teal,
    error bars/.cd,
      y dir=both,
      y explicit,
  ] table[x=label,y=mean_seconds,y error=ci95_half_width_seconds,col sep=tab] {figures/data/variant_summary.tsv};
\end{groupplot}
\end{tikzpicture}
\end{document}
'''
    write_text(SRC_DIR / 'variant_runtime.tex', tex)


def build_tables() -> tuple[list[str], list[list[int]]]:
    baseline_contract = load_json('results/experiments/run_1000000/contract.json')
    baseline_record_gaps = load_json('results/experiments/run_1000000/record_gaps.json')
    baseline_summary = load_json('results/experiments/run_1000000/record_gap_summary.json')
    row_contract = load_json('results/experiments/row_immediate_1000000/contract.json')
    col_contract = load_json('results/experiments/column_immediate_1000000/contract.json')
    hyper = load_json('results/analysis/full_witness_hypergraphs_gap21_25_28_30.json')
    runtime = load_json('results/experiments/runtime_repeats_1000000.json')
    row_terms = load_json('results/experiments/run_1000000/row_terms.json')
    col_terms = load_json('results/experiments/run_1000000/column_terms.json')
    table_preview = load_json('results/baseline/smoke_11/table_preview.json')

    write_tsv(
        DATA_DIR / 'baseline_record_gaps.tsv',
        ['step', 'gap', 'offset_before', 'offset_after'],
        [
            {'step': item['step'], 'gap': item['gap'], 'offset_before': item['offset_before'], 'offset_after': item['offset_after']}
            for item in baseline_record_gaps
        ],
    )
    write_tsv(
        DATA_DIR / 'row_immediate_record_gaps.tsv',
        ['step', 'gap'],
        [{'step': item['step'], 'gap': item['gap']} for item in load_json('results/experiments/row_immediate_1000000/record_gaps.json')],
    )
    write_tsv(
        DATA_DIR / 'column_immediate_record_gaps.tsv',
        ['step', 'gap'],
        [{'step': item['step'], 'gap': item['gap']} for item in load_json('results/experiments/column_immediate_1000000/record_gaps.json')],
    )

    summary_by_gap = {item['gap']: item for item in baseline_summary['gaps']}
    baseline_metric_rows: list[dict[str, object]] = []
    for item in baseline_record_gaps:
        gap = item['gap']
        if gap not in summary_by_gap:
            continue
        summary = summary_by_gap[gap]
        baseline_metric_rows.append(
            {
                'gap': gap,
                'singleton_share': summary['singleton_share'],
                'tiny_share': summary['min_factor_le_10_share'],
                'balanced_share': summary['min_factor_gt_100_share'],
                'skipped_prime_count': summary['skipped_prime_count'],
            }
        )
    write_tsv(
        DATA_DIR / 'baseline_gap_metrics.tsv',
        ['gap', 'singleton_share', 'tiny_share', 'balanced_share', 'skipped_prime_count'],
        baseline_metric_rows,
    )

    sampled_offsets = []
    sample_stride = 5000
    for idx in range(0, len(row_terms), sample_stride):
        sampled_offsets.append({'step': idx + 1, 'offset': col_terms[idx] - row_terms[idx]})
    if sampled_offsets[-1]['step'] != len(row_terms):
        sampled_offsets.append({'step': len(row_terms), 'offset': col_terms[-1] - row_terms[-1]})
    write_tsv(DATA_DIR / 'offset_samples.tsv', ['step', 'offset'], sampled_offsets)

    hyper_rows = []
    for item in hyper['gaps']:
        pair_hist = {int(k): v for k, v in item['pair_count_histogram'].items()}
        hyper_rows.append(
            {
                'gap': item['gap'],
                'pair1': pair_hist.get(1, 0),
                'pair2': pair_hist.get(2, 0),
                'pair3': pair_hist.get(3, 0),
                'pair4plus': sum(v for k, v in pair_hist.items() if k >= 4),
                'total_full_pairs': item['total_full_pairs'],
                'distinct_row_factors_used': item['distinct_row_factors_used'],
                'distinct_column_factors_used': item['distinct_column_factors_used'],
            }
        )
    write_tsv(
        DATA_DIR / 'hypergraph_metrics.tsv',
        ['gap', 'pair1', 'pair2', 'pair3', 'pair4plus', 'total_full_pairs', 'distinct_row_factors_used', 'distinct_column_factors_used'],
        hyper_rows,
    )

    runtime_by_label = {'baseline': runtime['benchmark']['runs'][0], 'row-immediate': runtime['benchmark']['runs'][1], 'column-immediate': runtime['benchmark']['runs'][2]}
    variant_rows = []
    for label, contract in [('baseline', baseline_contract), ('row-immediate', row_contract), ('column-immediate', col_contract)]:
        variant_rows.append(
            {
                'label': label,
                'largest_record_gap': contract['largest_record_gap'],
                'record_gap_count': contract['record_gap_count'],
                'mean_seconds': runtime_by_label[label]['mean_seconds'],
                'ci95_half_width_seconds': runtime_by_label[label]['ci95_half_width_seconds'],
            }
        )
    write_tsv(
        DATA_DIR / 'variant_summary.tsv',
        ['label', 'largest_record_gap', 'record_gap_count', 'mean_seconds', 'ci95_half_width_seconds'],
        variant_rows,
    )

    paper_metrics = {
        'baseline_contract': baseline_contract,
        'row_immediate_contract': row_contract,
        'column_immediate_contract': col_contract,
        'baseline_gap_metrics': baseline_metric_rows,
        'hypergraph_metrics': hyper_rows,
        'runtime_repeats': runtime,
        'figure_files': [
            'frontier_structure',
            'record_gap_timeline',
            'gap_composition',
            'frontier_offsets',
            'hypergraph_metrics',
            'variant_runtime',
        ],
        'prefix_table': table_preview,
    }
    write_text(ROOT / 'results' / 'analysis' / 'paper_metrics.json', json.dumps(paper_metrics, indent=2) + '\n')
    return paper_metrics['figure_files'], table_preview


def main() -> int:
    for path in [DATA_DIR, SRC_DIR, PDF_DIR, PNG_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    figure_files, prefix_table = build_tables()
    write_frontier_structure(prefix_table)
    write_record_gap_timeline()
    write_gap_composition()
    write_frontier_offsets()
    write_hypergraph_metrics()
    write_variant_runtime()

    for name in figure_files:
        compile_figure(name)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
