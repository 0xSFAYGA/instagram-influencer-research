from collections import Counter
from pathlib import Path
from typing import List

from ..types import CreatorRecord, Job, RunStats


def write_summary(path: Path, job: Job, records: List[CreatorRecord], stats: RunStats) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    counts = Counter([record.quality_flag for record in records])
    recommended = counts.get("Recommended", 0)
    review = counts.get("Review", 0)
    avoid = counts.get("Avoid", 0)

    lines = [
        f"# Summary — {job.job_id}",
        "",
        f"- Client: {job.client_name}",
        f"- Niche: {job.niche}",
        f"- Package: {job.package}",
        f"- Creators: {len(records)} (Recommended: {recommended}, Review: {review}, Avoid: {avoid})",
        f"- Total request units: {stats.total_request_units}",
        "",
        "## Notes",
        job.notes or "No additional notes provided.",
    ]

    path.write_text("\n".join(lines))
    return path

