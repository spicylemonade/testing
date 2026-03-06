from __future__ import annotations

from hashlib import sha256
import json
from typing import Any


def _round_value(value: Any) -> Any:
    if isinstance(value, float):
        return float(f"{value:.15e}")
    if isinstance(value, list):
        return [_round_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _round_value(value[key]) for key in sorted(value)}
    return value


def _fingerprint(payload: dict[str, Any]) -> str:
    canonical = json.dumps(_round_value(payload), sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def terminal_state_fingerprint(result: dict[str, Any]) -> str:
    terminal = result["diagnostics"][-1]
    payload = {
        "scenario_id": result["metadata"]["scenario_id"],
        "dt": result["metadata"]["dt"],
        "positions": terminal["positions"],
        "velocities": terminal["velocities"],
    }
    return _fingerprint(payload)


def trajectory_fingerprint(result: dict[str, Any]) -> str:
    payload = {
        "scenario_id": result["metadata"]["scenario_id"],
        "dt": result["metadata"]["dt"],
        "diagnostics": [
            {
                "time": row["time"],
                "positions": row["positions"],
                "velocities": row["velocities"],
            }
            for row in result["diagnostics"]
        ],
    }
    return _fingerprint(payload)
