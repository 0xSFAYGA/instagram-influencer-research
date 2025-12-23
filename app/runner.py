from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import load_settings
from .export.csv import write_csv
from .export.excel import write_excel
from .export.run_log import write_run_log
from .export.summary import write_summary
from .hiker.client import HikerAPIClient
from .pipeline.action_plan import write_action_plan
from .pipeline.discovery import discover_candidates
from .pipeline.enrich import enrich_candidates
from .storage.artifacts import (
    action_plan_path,
    output_csv_path,
    output_excel_path,
    run_log_path,
    summary_path,
)
from .storage.jobs import copy_input_to_job, load_job
from .types import RunStats


def run_job(job_file: Path, env_file: Optional[Path] = None, cache_ttl_seconds: int = 86_400) -> Path:
    job = load_job(job_file)
    copy_input_to_job(job, job_file)

    settings = load_settings(env_file)
    stats = RunStats(job_id=job.job_id, started_at=datetime.utcnow())

    posts_sample = job.posts_sample or settings.default_posts_sample
    posts_sample = max(posts_sample, 1)

    candidates = discover_candidates(job)
    if not candidates:
        print("No candidates found; outputs will be empty unless seed_handles are provided.")

    with HikerAPIClient(settings, stats=stats, cache_ttl_seconds=cache_ttl_seconds) as client:
        records = enrich_candidates(candidates, job, client, posts_sample)

    stats.ended_at = datetime.utcnow()

    rows = [asdict(record) for record in records]

    output_csv = write_csv(output_csv_path(job.job_id), rows)
    output_excel = write_excel(output_excel_path(job.job_id), rows)
    summary = write_summary(summary_path(job.job_id), job, records, stats)

    if job.package.lower() == "advanced":
        write_action_plan(action_plan_path(job.job_id), job, records)

    write_run_log(run_log_path(job.job_id), stats)

    print(f"Wrote CSV to {output_csv}")
    print(f"Wrote Excel to {output_excel}")
    print(f"Wrote summary to {summary}")

    return output_csv.parent

