#!/usr/bin/env bash
set -euo pipefail

# Reproducible research stack for simulation, analysis, and plotting.
python3 -m pip install --user --upgrade pip
python3 -m pip install --user numpy pandas matplotlib seaborn psutil scipy
