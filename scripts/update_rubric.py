#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_PATH = ROOT / "research_rubric.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_rubric() -> dict:
    return json.loads(RUBRIC_PATH.read_text())


def save_rubric(payload: dict) -> None:
    RUBRIC_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def iter_items(rubric: dict):
    for phase in rubric.get("phases", []):
        for item in phase.get("items", []):
            yield item


def recalc_summary(rubric: dict) -> None:
    counts = {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0}
    total = 0
    for item in iter_items(rubric):
        total += 1
        status = item.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    rubric["summary"] = {
        "total_items": total,
        "completed": counts.get("completed", 0),
        "in_progress": counts.get("in_progress", 0),
        "failed": counts.get("failed", 0),
        "pending": counts.get("pending", 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a research rubric item status.")
    parser.add_argument("item_id")
    parser.add_argument("status", choices=["pending", "in_progress", "completed", "failed"])
    parser.add_argument("--notes", default=None)
    parser.add_argument("--error", default=None)
    args = parser.parse_args()

    rubric = load_rubric()
    target = None
    for item in iter_items(rubric):
        if item.get("id") == args.item_id:
            target = item
            break

    if target is None:
        raise SystemExit(f"Unknown item id: {args.item_id}")

    target["status"] = args.status
    target["notes"] = args.notes
    target["error"] = args.error
    rubric["updated_at"] = utc_now()
    recalc_summary(rubric)
    save_rubric(rubric)
    print(json.dumps({"item_id": args.item_id, "status": args.status, "summary": rubric["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
