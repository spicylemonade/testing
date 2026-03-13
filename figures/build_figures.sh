#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

figs=(
  fig_frontier_timeline
  fig_h1_pipeline
  fig_prior_work_matrix
  fig_experiment_ladder
  fig_bridge_status
  fig_evidence_dashboard
)

for fig in "${figs[@]}"; do
  pdflatex -interaction=nonstopmode -halt-on-error "${fig}.tex" >/dev/null
  mutool draw -q -r 600 -o "${fig}.png" "${fig}.pdf" 1
  rm -f "${fig}.aux" "${fig}.log"
done
