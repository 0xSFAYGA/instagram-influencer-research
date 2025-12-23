import json
from datetime import datetime
from pathlib import Path

from ..types import RunStats


def write_run_log(path: Path, stats: RunStats) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    events = [
        {
            "timestamp": stats.started_at.isoformat(),
            "event": "run_started",
            "job_id": stats.job_id,
        }
    ]

    if stats.ended_at:
        events.append(
            {
                "timestamp": stats.ended_at.isoformat(),
                "event": "run_finished",
                "job_id": stats.job_id,
                "total_request_units": stats.total_request_units,
                "cost_by_endpoint": stats.cost_by_endpoint,
                "cache_hits": stats.cache_hits,
                "cache_misses": stats.cache_misses,
            }
        )

    with path.open("w") as f:
        for event in events:
            json.dump(event, f)
            f.write("\n")

    return path

