#!/usr/bin/env python3
"""
Experiment tracking utility for B_u bound results.

Appends new bound results to results/phase2/metrics.json with fields:
- bound_value, bound_type (lower/upper), method_name, timestamp, script_path, notes
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

METRICS_FILE = Path(__file__).resolve().parent.parent / "phase2" / "metrics.json"


def _load_metrics():
    """Load metrics from file, or return default structure."""
    if METRICS_FILE.exists():
        with open(METRICS_FILE) as f:
            return json.load(f)
    return {
        "known_bounds": {
            "best_lower": 0.5708858,
            "best_lower_ref": "Skinner 2009",
            "best_upper": 0.6564,
            "best_upper_ref": "Carroll-Ortega-Cerda 2008",
            "trivial_upper": 1.0
        },
        "our_bounds": [],
        "best_certified_lower": None,
        "best_certified_upper": None
    }


def _save_metrics(data):
    """Save metrics to file."""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def log_bound(bound_value, bound_type, method_name, script_path="", notes="", certified=False):
    """
    Log a new bound result.
    
    Parameters:
        bound_value: float, the bound value
        bound_type: str, 'lower' or 'upper'
        method_name: str, name of the method
        script_path: str, path to the script that produced this
        notes: str, additional notes
        certified: bool, whether the bound is rigorously certified
    
    Returns:
        The updated metrics dict
    """
    data = _load_metrics()
    
    entry = {
        "bound_value": bound_value,
        "bound_type": bound_type,
        "method_name": method_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script_path": script_path,
        "notes": notes,
        "certified": certified
    }
    
    data["our_bounds"].append(entry)
    
    # Update best certified bounds
    if certified:
        if bound_type == "lower":
            if data["best_certified_lower"] is None or bound_value > data["best_certified_lower"]:
                data["best_certified_lower"] = bound_value
        elif bound_type == "upper":
            if data["best_certified_upper"] is None or bound_value < data["best_certified_upper"]:
                data["best_certified_upper"] = bound_value
    
    _save_metrics(data)
    
    improvement = ""
    if bound_type == "lower" and bound_value > data["known_bounds"]["best_lower"]:
        improvement = f" ** IMPROVEMENT over Skinner's {data['known_bounds']['best_lower']}! **"
    elif bound_type == "upper" and bound_value < data["known_bounds"]["best_upper"]:
        improvement = f" ** IMPROVEMENT over Carroll-OC's {data['known_bounds']['best_upper']}! **"
    
    cert_str = " [CERTIFIED]" if certified else " [numerical]"
    print(f"Logged {bound_type} bound: B_u {'>' if bound_type == 'lower' else '<='} {bound_value:.10f}"
          f" ({method_name}){cert_str}{improvement}")
    
    return data


def get_best_bounds():
    """Return the current best bounds (known + ours)."""
    data = _load_metrics()
    
    best_lower = data["known_bounds"]["best_lower"]
    best_upper = data["known_bounds"]["best_upper"]
    
    for entry in data["our_bounds"]:
        if entry["bound_type"] == "lower" and entry["bound_value"] > best_lower:
            best_lower = entry["bound_value"]
        elif entry["bound_type"] == "upper" and entry["bound_value"] < best_upper:
            best_upper = entry["bound_value"]
    
    return {
        "best_lower": best_lower,
        "best_upper": best_upper,
        "gap": best_upper - best_lower,
        "best_certified_lower": data.get("best_certified_lower"),
        "best_certified_upper": data.get("best_certified_upper")
    }


def init_metrics():
    """Initialize the metrics file with known bounds."""
    data = _load_metrics()
    _save_metrics(data)
    print(f"Metrics initialized at {METRICS_FILE}")
    print(f"Known lower bound: {data['known_bounds']['best_lower']} (Skinner 2009)")
    print(f"Known upper bound: {data['known_bounds']['best_upper']} (Carroll-Ortega-Cerda 2008)")
    return data


# Test
def _test():
    init_metrics()
    log_bound(0.5708858, "lower", "Skinner reproduction", "results/phase2/reproduce_skinner.py", "Baseline reproduction")
    bounds = get_best_bounds()
    print(f"\nBest bounds: {bounds['best_lower']:.10f} < B_u <= {bounds['best_upper']:.10f}")
    print(f"Gap: {bounds['gap']:.10f}")


if __name__ == "__main__":
    _test()
