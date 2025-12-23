import json
import shutil
from pathlib import Path
from typing import Any, Dict

from ..types import FollowerRange, Job
from .artifacts import input_copy_path


def _parse_follower_range(data: Dict[str, Any]) -> FollowerRange:
    if not data:
        return FollowerRange()
    return FollowerRange(minimum=data.get("min"), maximum=data.get("max"))


def load_job(path: Path) -> Job:
    with path.open() as f:
        payload = json.load(f)

    job_id = payload["job_id"]

    follower_range = _parse_follower_range(payload.get("follower_range", {}))

    return Job(
        job_id=job_id,
        client_name=payload.get("client_name", ""),
        niche=payload.get("niche", ""),
        keywords=payload.get("keywords", []) or [],
        location=payload.get("location"),
        language=payload.get("language"),
        goals=payload.get("goals"),
        exclude_accounts=payload.get("exclude_accounts", []) or [],
        follower_range=follower_range,
        min_er_percent=payload.get("min_er_percent"),
        package=payload.get("package", "starter"),
        notes=payload.get("notes"),
        seed_handles=payload.get("seed_handles", []) or [],
        posts_sample=payload.get("posts_sample"),
    )


def copy_input_to_job(job: Job, source_path: Path) -> Path:
    destination = input_copy_path(job.job_id)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination)
    return destination

