#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


VALID_STATUSES = {"pending", "in_progress", "completed", "failed"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def recompute_summary(data: dict) -> None:
    counts = {"completed": 0, "in_progress": 0, "failed": 0, "pending": 0}
    for phase in data.get("phases", []):
        for item in phase.get("items", []):
            counts[item["status"]] += 1
    counts["total_items"] = sum(counts.values())
    data["summary"] = counts


def update_item(data: dict, item_id: str, status: str, notes: str | None, error: str | None) -> None:
    found = False
    for phase in data.get("phases", []):
        for item in phase.get("items", []):
            if item.get("id") != item_id:
                continue
            item["status"] = status
            item["notes"] = notes
            item["error"] = error
            found = True
            break
        if found:
            break
    if not found:
        raise SystemExit(f"Unknown rubric item: {item_id}")


def update_agent(data: dict, status: str) -> None:
    researcher = data.setdefault("agent_status", {}).setdefault("researcher", {})
    researcher["status"] = status
    if status == "completed":
        researcher["completed_at"] = now()
    elif status == "in_progress" and not researcher.get("started_at"):
        researcher["started_at"] = now()


def main() -> None:
    parser = argparse.ArgumentParser(description="Update a research rubric item")
    parser.add_argument("item_id")
    parser.add_argument("status", choices=sorted(VALID_STATUSES))
    parser.add_argument("--notes", default=None)
    parser.add_argument("--error", default=None)
    parser.add_argument("--complete-agent", action="store_true")
    args = parser.parse_args()

    path = Path(__file__).resolve().parents[1] / "research_rubric.json"
    data = json.loads(path.read_text())
    update_item(data, args.item_id, args.status, args.notes, args.error)
    if args.complete_agent:
        update_agent(data, "completed")
    else:
        update_agent(data, "in_progress")
    data["updated_at"] = now()
    recompute_summary(data)
    path.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
