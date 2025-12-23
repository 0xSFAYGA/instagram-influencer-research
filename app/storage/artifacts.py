from pathlib import Path


def jobs_root() -> Path:
    root = Path("data") / "jobs"
    root.mkdir(parents=True, exist_ok=True)
    return root


def job_dir(job_id: str) -> Path:
    path = jobs_root() / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def input_copy_path(job_id: str) -> Path:
    return job_dir(job_id) / "input.json"


def output_csv_path(job_id: str) -> Path:
    return job_dir(job_id) / "output.csv"


def output_excel_path(job_id: str) -> Path:
    return job_dir(job_id) / "output.xlsx"


def summary_path(job_id: str) -> Path:
    return job_dir(job_id) / "summary.md"


def action_plan_path(job_id: str) -> Path:
    return job_dir(job_id) / "action_plan.md"


def run_log_path(job_id: str) -> Path:
    return job_dir(job_id) / "run_log.jsonl"

