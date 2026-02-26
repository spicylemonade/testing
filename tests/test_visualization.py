"""Tests for visualization module."""

import os
import tempfile
import numpy as np
from src.visualization import plot_trajectories, plot_snapshot


def test_plot_trajectories_saves_png():
    trajectories = np.random.randn(10, 3, 2)  # 10 steps, 3 bodies, 2D
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fname = f.name
    try:
        plot_trajectories(trajectories, filename=fname)
        assert os.path.exists(fname)
        assert os.path.getsize(fname) > 0
    finally:
        os.unlink(fname)
        pdf = fname.replace(".png", ".pdf")
        if os.path.exists(pdf):
            os.unlink(pdf)


def test_plot_trajectories_with_masses():
    trajectories = np.random.randn(5, 2, 2)
    masses = np.array([1.0, 2.0])
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fname = f.name
    try:
        plot_trajectories(trajectories, masses=masses, filename=fname, show_trails=False)
        assert os.path.exists(fname)
    finally:
        os.unlink(fname)
        pdf = fname.replace(".png", ".pdf")
        if os.path.exists(pdf):
            os.unlink(pdf)


def test_plot_snapshot_saves_png():
    positions = np.random.randn(20, 2)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fname = f.name
    try:
        plot_snapshot(positions, filename=fname)
        assert os.path.exists(fname)
        assert os.path.getsize(fname) > 0
    finally:
        os.unlink(fname)
        pdf = fname.replace(".png", ".pdf")
        if os.path.exists(pdf):
            os.unlink(pdf)


def test_plot_snapshot_with_masses():
    positions = np.random.randn(10, 2)
    masses = np.array([1.0] * 10)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fname = f.name
    try:
        plot_snapshot(positions, masses=masses, filename=fname)
        assert os.path.exists(fname)
    finally:
        os.unlink(fname)
        pdf = fname.replace(".png", ".pdf")
        if os.path.exists(pdf):
            os.unlink(pdf)
