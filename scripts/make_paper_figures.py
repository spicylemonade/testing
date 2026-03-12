#!/usr/bin/env python3
"""Generate programmatic TikZ/PGFPlots figures and render them to PDF/PNG."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
DATA_DIR = FIGURES / "data"
SRC_DIR = FIGURES / "src"


def load_json(path: Path):
    return json.loads(path.read_text())


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    lines = ["\t".join(header)]
    for row in rows:
        lines.append("\t".join(str(item) for item in row))
    write_text(path, "\n".join(lines) + "\n")


def latex_preamble() -> str:
    return dedent(
        r"""
        \documentclass[tikz,border=6pt]{standalone}
        \usepackage{pgfplots}
        \usepgfplotslibrary{groupplots}
        \usetikzlibrary{arrows.meta,calc,positioning,backgrounds}
        \pgfplotsset{compat=1.18}
        \definecolor{ink}{HTML}{16324F}
        \definecolor{rowc}{HTML}{1B4965}
        \definecolor{colc}{HTML}{A44A3F}
        \definecolor{accent}{HTML}{D9A441}
        \definecolor{sage}{HTML}{4F6D5B}
        \definecolor{sand}{HTML}{E7DFC6}
        \definecolor{mist}{HTML}{F4F1EA}
        \definecolor{gridc}{HTML}{D7D3C8}
        \pagecolor{mist}
        \begin{document}
        """
    )


def latex_end() -> str:
    return "\n\\end{document}\n"


def render_figure(stem: str) -> None:
    tex_path = SRC_DIR / f"{stem}.tex"
    subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            str(SRC_DIR),
            str(tex_path),
        ],
        check=True,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
    )
    pdf_src = SRC_DIR / f"{stem}.pdf"
    pdf_dst = FIGURES / f"{stem}.pdf"
    shutil.copy2(pdf_src, pdf_dst)
    subprocess.run(
        [
            "mutool",
            "draw",
            "-q",
            "-r",
            "600",
            "-o",
            str(FIGURES / f"{stem}.png"),
            str(pdf_dst),
            "1",
        ],
        check=True,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
    )


def build_figure1(table: list[list[int]]) -> None:
    x_cells = len(table[0])
    y_cells = len(table)
    cell_w = 0.85
    cell_h = 0.78
    lines = [latex_preamble(), r"\begin{tikzpicture}[font=\small]"]
    lines.append(r"\node[font=\bfseries\Large, anchor=west] at (0,4.9) {A. Initial $5\times 11$ block of $T$};")
    for i, row in enumerate(table):
        for j, value in enumerate(row):
            x = j * cell_w
            y = -i * cell_h
            fill = "white"
            if i == 0:
                fill = "rowc!20"
            elif j == 0:
                fill = "colc!20"
            lines.append(
                rf"\filldraw[fill={fill}, draw=gridc, line width=0.4pt] ({x:.3f},{y:.3f}) rectangle ({x+cell_w:.3f},{y-cell_h:.3f});"
            )
            lines.append(
                rf"\node[font=\scriptsize] at ({x + cell_w/2:.3f},{y - cell_h/2:.3f}) {{{value}}};"
            )
    lines.append(
        rf"\draw[rowc, line width=1.4pt] (0,0) rectangle ({x_cells*cell_w:.3f},{-cell_h:.3f});"
    )
    lines.append(
        rf"\draw[colc, line width=1.4pt] (0,0) rectangle ({cell_w:.3f},{-y_cells*cell_h:.3f});"
    )
    lines.append(r"\node[rowc, font=\bfseries] at (7.6,0.45) {first row $r_n$};")
    lines.append(r"\node[colc, font=\bfseries, rotate=90] at (-0.55,-2.0) {first column $c_n$};")

    shift = 11.0
    lines.append(rf"\begin{{scope}}[xshift={shift}cm]")
    lines.append(r"\node[font=\bfseries\Large, anchor=west] at (0,4.9) {B. Frontier structure at step $n$};")
    lines.append(r"\draw[ink, line width=0.8pt] (0.4,2.0) -- (8.6,2.0);")
    tick_positions = {"1": 0.8, "r_n": 2.7, "c_n": 4.1, "r_{n+1}": 5.8, "c_{n+1}": 7.6}
    for label, x in tick_positions.items():
        lines.append(rf"\draw[ink, line width=0.8pt] ({x},1.7) -- ({x},2.3);")
        lines.append(rf"\node at ({x},1.35) {{$ {label} $}};")
    lines.append(r"\fill[sand] (0.8,2.55) rectangle (5.8,3.1);")
    lines.append(r"\fill[colc!10] (5.8,2.55) rectangle (7.6,3.1);")
    lines.append(r"\node at (3.3,2.82) {covered in $P_n$};")
    lines.append(r"\node[align=center] at (6.7,2.82) {covered except\\$r_{n+1},c_{n+1}$};")
    lines.append(r"\fill[rowc] (2.7,2.0) circle (2.2pt);")
    lines.append(r"\fill[colc] (4.1,2.0) circle (2.2pt);")
    lines.append(r"\fill[rowc] (5.8,2.0) circle (2.2pt);")
    lines.append(r"\fill[colc] (7.6,2.0) circle (2.2pt);")
    lines.append(r"\draw[-{Latex[length=2.0mm]}, rowc, line width=1.0pt] (6.2,0.8) -- (5.85,1.85);")
    lines.append(r"\draw[-{Latex[length=2.0mm]}, colc, line width=1.0pt] (7.9,3.9) -- (7.65,2.15);")
    lines.append(r"\node[rowc, anchor=west] at (6.2,0.7) {first mex of $P_n$};")
    lines.append(r"\node[colc, anchor=east] at (7.9,4.05) {second mex of $P_n$};")
    lines.append(
        r"\node[align=left, text width=8.0cm, anchor=north west] at (0.2,0.15) {"
        r"$r_n<c_n<r_{n+1}<c_{n+1}$, the interval $(r_n,r_{n+1})$ contains the unique column term $c_n$, "
        r"and adjoining $r_{n+1}$ immediately does not change the next column choice.};"
    )
    lines.append(r"\end{scope}")
    lines.append(r"\end{tikzpicture}")
    lines.append(latex_end())
    write_text(SRC_DIR / "figure1_construction.tex", "\n".join(lines))


def build_figure2() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=1.8cm},
          width=7.2cm,
          height=6.2cm,
          grid=major,
          grid style={draw=gridc},
          tick style={black},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. Exact interleaving of the axis terms},
          xlabel={index $n$},
          ylabel={value},
          legend style={draw=none, fill=none, at={(0.03,0.97)}, anchor=north west},
        ]
        \addplot[rowc, very thick] table[x=n,y=row]{figures/data/figure2_interleaving.tsv};
        \addplot[colc, very thick] table[x=n,y=column]{figures/data/figure2_interleaving.tsv};
        \legend{$r_n$,$c_n$}

        \nextgroupplot[
          title={B. Offset $\delta_n=c_n-r_n$ up to $n=10^6$},
          xlabel={index $n$},
          ylabel={offset},
          xmode=log,
        ]
        \addplot[ink, very thick] table[x=n,y=offset]{figures/data/figure2_offsets.tsv};
        \node[draw=gridc, fill=white, rounded corners=2pt, anchor=north west] at (rel axis cs:0.03,0.97)
          {max offset $=24$};
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure2_interleaving.tex", tex)


def build_figure3() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=1.8cm},
          width=7.15cm,
          height=6.2cm,
          grid=major,
          grid style={draw=gridc},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. Record-gap trajectory in the baseline run},
          xlabel={step $n$},
          ylabel={record gap $g_n$},
          xmode=log,
        ]
        \addplot[rowc, very thick, mark=*, mark size=1.8pt] table[x=step,y=gap]{figures/data/figure3_record_gaps.tsv};

        \nextgroupplot[
          title={B. Waiting time between successive record gaps},
          xlabel={record index},
          ylabel={step increment},
          ymode=log,
          xtick=data,
          xticklabels from table={figures/data/figure3_waits.tsv}{label},
          x tick label style={rotate=45, anchor=east},
          ymin=1,
        ]
        \addplot[ybar, bar width=6pt, fill=sage, draw=sage] table[x=idx,y=wait]{figures/data/figure3_waits.tsv};
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure3_gap_trajectory.tex", tex)


def build_figure4() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=2.0cm},
          width=7.15cm,
          height=6.4cm,
          grid=major,
          grid style={draw=gridc},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. Witness composition across baseline record gaps},
          xlabel={record gap},
          ylabel={skipped values},
          ybar stacked,
          bar width=8pt,
          symbolic x coords={13,17,19,20,21,25,28,30},
          xtick=data,
          legend style={draw=none, fill=none, at={(0.02,0.98)}, anchor=north west, font=\scriptsize},
        ]
        \addplot[fill=colc, draw=mist] table[x=gap,y=axis1_marker]{figures/data/figure4_composition.tsv};
        \addplot[fill=rowc!85, draw=mist] table[x=gap,y=tiny_singleton]{figures/data/figure4_composition.tsv};
        \addplot[fill=rowc!45, draw=mist] table[x=gap,y=tiny_redundant]{figures/data/figure4_composition.tsv};
        \addplot[fill=sage!85, draw=mist] table[x=gap,y=mesoscopic_singleton]{figures/data/figure4_composition.tsv};
        \addplot[fill=sage!45, draw=mist] table[x=gap,y=mesoscopic_redundant]{figures/data/figure4_composition.tsv};
        \addplot[fill=accent!90, draw=mist] table[x=gap,y=balanced_singleton]{figures/data/figure4_composition.tsv};
        \addplot[fill=accent!55, draw=mist] table[x=gap,y=balanced_redundant]{figures/data/figure4_composition.tsv};
        \legend{axis-1 marker,tiny singleton,tiny redundant,mesoscopic singleton,mesoscopic redundant,balanced singleton,balanced redundant}

        \nextgroupplot[
          title={B. Compression fails as balanced witnesses rise},
          xlabel={record gap},
          ylabel={share of skipped values},
          symbolic x coords={13,17,19,20,21,25,28,30},
          xtick=data,
          ymin=0, ymax=1,
          legend style={draw=none, fill=none, at={(0.98,0.98)}, anchor=north east, font=\scriptsize},
        ]
        \addplot[ink, very thick, mark=*] table[x=gap,y=singleton_share]{figures/data/figure4_shares.tsv};
        \addplot[rowc, very thick, mark=square*] table[x=gap,y=tiny_share]{figures/data/figure4_shares.tsv};
        \addplot[accent!90!black, very thick, mark=triangle*] table[x=gap,y=balanced_share]{figures/data/figure4_shares.tsv};
        \legend{singleton share,tiny-factor share,balanced-factor share}
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure4_gap_composition.tex", tex)


def build_figure5() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=1.9cm},
          width=7.1cm,
          height=6.2cm,
          grid=major,
          grid style={draw=gridc},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. Full witness hypergraphs stay sparse},
          xlabel={record gap},
          ylabel={count},
          ybar,
          bar width=6pt,
          symbolic x coords={21,25,28,30},
          xtick=data,
          legend style={draw=none, fill=none, at={(0.02,0.98)}, anchor=north west, font=\scriptsize},
        ]
        \addplot[fill=ink, draw=ink] table[x=gap,y=total_pairs]{figures/data/figure5_hypergraph.tsv};
        \addplot[fill=rowc, draw=rowc] table[x=gap,y=distinct_rows]{figures/data/figure5_hypergraph.tsv};
        \addplot[fill=colc, draw=colc] table[x=gap,y=distinct_cols]{figures/data/figure5_hypergraph.tsv};
        \legend{all admissible pairs,distinct row factors,distinct column factors}

        \nextgroupplot[
          title={B. Singleton-dominated multiplicity persists},
          xlabel={witness multiplicity},
          ylabel={skipped values},
          ybar,
          bar width=5pt,
          xtick={1,2,3,4,5},
          legend style={draw=none, fill=none, at={(0.98,0.98)}, anchor=north east, font=\scriptsize},
        ]
        \addplot[fill=rowc!85, draw=rowc!85] table[x=multiplicity,y=gap21]{figures/data/figure5_multiplicity.tsv};
        \addplot[fill=colc!85, draw=colc!85] table[x=multiplicity,y=gap25]{figures/data/figure5_multiplicity.tsv};
        \addplot[fill=sage!85, draw=sage!85] table[x=multiplicity,y=gap28]{figures/data/figure5_multiplicity.tsv};
        \addplot[fill=accent!90, draw=accent!90] table[x=multiplicity,y=gap30]{figures/data/figure5_multiplicity.tsv};
        \legend{gap 21,gap 25,gap 28,gap 30}
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure5_hypergraph.tex", tex)


def build_figure6() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=1.8cm},
          width=7.1cm,
          height=6.2cm,
          grid=major,
          grid style={draw=gridc},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. The row-immediate rule is exactly identical},
          xlabel={baseline term},
          ylabel={row-immediate term},
        ]
        \addplot[draw=gridc, dashed, domain=1:1400] {x};
        \addplot[only marks, mark=*, mark size=1.3pt, rowc] table[x=baseline_row,y=row_immediate_row]{figures/data/figure6_identities.tsv};
        \addplot[only marks, mark=square*, mark size=1.2pt, colc] table[x=baseline_col,y=row_immediate_col]{figures/data/figure6_identities.tsv};
        \node[draw=gridc, fill=white, rounded corners=2pt, anchor=south east] at (rel axis cs:0.98,0.03)
          {$y=x$ in both clouds};

        \nextgroupplot[
          title={B. The column-immediate rule is the axis swap},
          xlabel={baseline term},
          ylabel={column-immediate term},
        ]
        \addplot[draw=gridc, dashed, domain=1:1400] {x};
        \addplot[only marks, mark=triangle*, mark size=1.6pt, colc] table[x=baseline_col,y=column_immediate_row]{figures/data/figure6_identities.tsv};
        \addplot[only marks, mark=diamond*, mark size=1.5pt, rowc] table[x=baseline_row,y=column_immediate_col]{figures/data/figure6_identities.tsv};
        \node[draw=gridc, fill=white, rounded corners=2pt, anchor=south east] at (rel axis cs:0.98,0.03)
          {axis swap};
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure6_variant_identities.tex", tex)


def build_figure7() -> None:
    tex = latex_preamble() + dedent(
        r"""
        \begin{tikzpicture}
        \begin{groupplot}[
          group style={group size=2 by 1, horizontal sep=1.8cm},
          width=7.15cm,
          height=6.2cm,
          grid=major,
          grid style={draw=gridc},
          xlabel near ticks,
          ylabel near ticks,
        ]
        \nextgroupplot[
          title={A. Distribution of all first-row gaps up to $10^6$ steps},
          xlabel={gap size},
          ylabel={frequency},
          ybar,
          bar width=4.5pt,
        ]
        \addplot[fill=sage, draw=sage] table[x=gap,y=count]{figures/data/figure7_gap_histogram.tsv};

        \nextgroupplot[
          title={B. Empirical survival function of gap sizes},
          xlabel={gap threshold},
          ylabel={$\Pr(G\ge t)$},
          ymode=log,
          ymin=0.000001,
        ]
        \addplot[ink, very thick, mark=*] table[x=gap,y=survival]{figures/data/figure7_gap_histogram.tsv};
        \end{groupplot}
        \end{tikzpicture}
        """
    ) + latex_end()
    write_text(SRC_DIR / "figure7_gap_distribution.tex", tex)


def export_data() -> None:
    baseline_dir = RESULTS / "experiments" / "run_1000000"
    row_immediate_dir = RESULTS / "experiments" / "row_immediate_1000000"
    column_immediate_dir = RESULTS / "experiments" / "column_immediate_1000000"
    table = load_json(RESULTS / "baseline" / "smoke_11" / "table_preview.json")
    baseline_rows = load_json(baseline_dir / "row_terms.json")
    baseline_cols = load_json(baseline_dir / "column_terms.json")
    record_gaps = load_json(baseline_dir / "record_gaps.json")
    record_gap_summary = load_json(baseline_dir / "record_gap_summary.json")["gaps"]
    hypergraphs = load_json(RESULTS / "analysis" / "full_witness_hypergraphs_gap21_25_28_30.json")["gaps"]
    row_immediate_rows = load_json(row_immediate_dir / "row_terms.json")
    row_immediate_cols = load_json(row_immediate_dir / "column_terms.json")
    column_immediate_rows = load_json(column_immediate_dir / "row_terms.json")
    column_immediate_cols = load_json(column_immediate_dir / "column_terms.json")

    first = 60
    write_tsv(
        DATA_DIR / "figure2_interleaving.tsv",
        ["n", "row", "column"],
        [[i + 1, baseline_rows[i], baseline_cols[i]] for i in range(first)],
    )
    sample_step = 2000
    write_tsv(
        DATA_DIR / "figure2_offsets.tsv",
        ["n", "offset"],
        [
            [i + 1, baseline_cols[i] - baseline_rows[i]]
            for i in range(0, len(baseline_rows), sample_step)
        ],
    )

    write_tsv(
        DATA_DIR / "figure3_record_gaps.tsv",
        ["step", "gap"],
        [[entry["step"], entry["gap"]] for entry in record_gaps],
    )
    waits = []
    for idx, (prev, current) in enumerate(zip(record_gaps[:-1], record_gaps[1:]), start=1):
        waits.append([idx, current["step"] - prev["step"], str(current["gap"])])
    write_tsv(DATA_DIR / "figure3_waits.tsv", ["idx", "wait", "label"], waits)

    late = [entry for entry in record_gap_summary if entry["gap"] >= 13]
    comp_rows = []
    share_rows = []
    for entry in late:
        hist = entry["signature_histogram"]
        comp_rows.append(
            [
                entry["gap"],
                hist.get("axis1_marker", 0),
                hist.get("tiny_singleton", 0),
                hist.get("tiny_redundant", 0),
                hist.get("mesoscopic_singleton", 0),
                hist.get("mesoscopic_redundant", 0),
                hist.get("balanced_singleton", 0),
                hist.get("balanced_redundant", 0),
            ]
        )
        share_rows.append(
            [
                entry["gap"],
                f"{entry['singleton_share']:.12f}",
                f"{entry['min_factor_le_10_share']:.12f}",
                f"{entry['min_factor_gt_100_share']:.12f}",
            ]
        )
    write_tsv(
        DATA_DIR / "figure4_composition.tsv",
        [
            "gap",
            "axis1_marker",
            "tiny_singleton",
            "tiny_redundant",
            "mesoscopic_singleton",
            "mesoscopic_redundant",
            "balanced_singleton",
            "balanced_redundant",
        ],
        comp_rows,
    )
    write_tsv(DATA_DIR / "figure4_shares.tsv", ["gap", "singleton_share", "tiny_share", "balanced_share"], share_rows)

    write_tsv(
        DATA_DIR / "figure5_hypergraph.tsv",
        ["gap", "total_pairs", "distinct_rows", "distinct_cols"],
        [
            [
                entry["gap"],
                entry["total_full_pairs"],
                entry["distinct_row_factors_used"],
                entry["distinct_column_factors_used"],
            ]
            for entry in hypergraphs
        ],
    )
    multiplicities = [1, 2, 3, 4, 5]
    mult_rows = []
    gap_map = {entry["gap"]: entry["pair_count_histogram"] for entry in hypergraphs}
    for m in multiplicities:
        mult_rows.append(
            [
                m,
                gap_map[21].get(str(m), 0),
                gap_map[25].get(str(m), 0),
                gap_map[28].get(str(m), 0),
                gap_map[30].get(str(m), 0),
            ]
        )
    write_tsv(DATA_DIR / "figure5_multiplicity.tsv", ["multiplicity", "gap21", "gap25", "gap28", "gap30"], mult_rows)

    sample = 300
    write_tsv(
        DATA_DIR / "figure6_identities.tsv",
        [
            "baseline_row",
            "baseline_col",
            "row_immediate_row",
            "row_immediate_col",
            "column_immediate_row",
            "column_immediate_col",
        ],
        [
            [
                baseline_rows[i],
                baseline_cols[i],
                row_immediate_rows[i],
                row_immediate_cols[i],
                column_immediate_rows[i],
                column_immediate_cols[i],
            ]
            for i in range(sample)
        ],
    )

    gaps = [baseline_rows[i + 1] - baseline_rows[i] for i in range(len(baseline_rows) - 1)]
    counts = Counter(gaps)
    total = len(gaps)
    hist_rows = []
    for gap in sorted(counts):
        survival = sum(v for g, v in counts.items() if g >= gap) / total
        hist_rows.append([gap, counts[gap], f"{survival:.12f}"])
    write_tsv(DATA_DIR / "figure7_gap_histogram.tsv", ["gap", "count", "survival"], hist_rows)

    build_figure1(table)
    build_figure2()
    build_figure3()
    build_figure4()
    build_figure5()
    build_figure6()
    build_figure7()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    export_data()
    for stem in [
        "figure1_construction",
        "figure2_interleaving",
        "figure3_gap_trajectory",
        "figure4_gap_composition",
        "figure5_hypergraph",
        "figure6_variant_identities",
        "figure7_gap_distribution",
    ]:
        render_figure(stem)


if __name__ == "__main__":
    main()
