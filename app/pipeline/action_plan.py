from pathlib import Path
from typing import List

from ..types import CreatorRecord, Job


def write_action_plan(path: Path, job: Job, records: List[CreatorRecord]) -> Path:
    """
    Lightweight action plan built from the top recommended creators.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    shortlist = [r for r in records if r.quality_flag == "Recommended"]
    shortlist = sorted(shortlist, key=lambda r: r.er_percent, reverse=True)[:20]

    lines = [
        f"# Action Plan — {job.job_id}",
        "",
        "## Priority Shortlist",
    ]
    if not shortlist:
        lines.append("No recommended creators available.")
    else:
        for idx, creator in enumerate(shortlist, start=1):
            lines.append(
                f"{idx}. {creator.username} — {creator.er_percent:.2f}% ER, {creator.followers} followers. Notes: {creator.reason_notes}"
            )

    lines.extend(
        [
            "",
            "## Testing Order",
            "Start outreach in batches of 10–15 creators, prioritizing higher ER% but keeping a mix across follower ranges.",
            "",
            "## Scale Guidance",
            "If results cluster around specific sub-niches or formats, expand adjacent keywords and repeat discovery for those segments.",
        ]
    )

    path.write_text("\n".join(lines))
    return path

